#!/usr/bin/env bash
# make_repro_bundle.sh — build a shareable reproducibility bundle of warringstates-engine.
#
# Ships engine code + structured per-game outcomes. EXCLUDES all content reserved for
# planned creative works (diplomacy transcripts, agent prompts, raw reasoning, observations,
# reflections, run logs, raw probe jsonl).
#
# Run from the warringstates-engine repo root:  bash scripts/make_repro_bundle.sh
# Output: warringstates-repro-bundle.tar.gz  (review the file list it prints before sending)

set -euo pipefail

OUT="warringstates-repro-bundle.tar.gz"
STAGE="$(mktemp -d)"
DEST="$STAGE/warringstates-repro-bundle"
mkdir -p "$DEST"

# --- code + top-level metadata (only if present) ---
for p in src scripts tests docs Makefile pyproject.toml uv.lock README.md .env.example .gitignore; do
  [ -e "$p" ] && cp -r --parents "$p" "$DEST"/ 2>/dev/null || true
done

# --- structured per-game outcomes only (NO diplomacy/prompts/raw/observations/reflection) ---
if [ -d games ]; then
  # game-root structured files
  find games -maxdepth 2 -type f \( -name 'game_meta.json' -o -name 'game_state.json' \) \
    -exec cp -r --parents {} "$DEST"/ \;
  # per-round structured files: orders/ and resolution.txt and orders.json
  find games -type d -path 'games/*/round_*/orders' \
    -exec cp -r --parents {} "$DEST"/ \;
  find games -type f \( -path 'games/*/round_*/resolution.txt' -o -path 'games/*/round_*/orders.json' \) \
    -exec cp -r --parents {} "$DEST"/ \;
  # campaigns index if present
  [ -f games/campaigns.json ] && cp -r --parents games/campaigns.json "$DEST"/ || true
fi

# --- safety sweep: delete any excluded dirs that slipped in ---
find "$DEST" -type d \( -name diplomacy -o -name prompts -o -name raw -o -name observations -o -name reflection \) \
  -prune -exec rm -rf {} + 2>/dev/null || true

# --- package ---
tar -czf "$OUT" -C "$STAGE" warringstates-repro-bundle
rm -rf "$STAGE"

echo "Built $OUT"
echo "Size: $(du -h "$OUT" | cut -f1)"
echo
echo "Top-level contents:"
tar -tzf "$OUT" | sed 's#warringstates-repro-bundle/##' | awk -F/ 'NF{print $1}' | sort -u
echo
echo "Sanity check — these should print NOTHING (content must be excluded):"
tar -tzf "$OUT" | grep -E '/(diplomacy|prompts|raw|observations|reflection)/' || echo "  clean: no content dirs in bundle"
