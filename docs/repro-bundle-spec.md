# Reproducibility bundle — what to share "on reasonable request"

When someone asks for the engine/data behind the paper, **do not hand over the
`warringstates-engine` repo** — ~98% of it (~110 MB) is content reserved for planned
creative works (diplomacy transcripts, agent prompts, raw reasoning). Instead produce a
**stripped reproducibility bundle**: the engine code plus structured per-game outcomes,
with all narrative content excluded.

## Include (verifiable code + structured data)

- `src/` — engine, agents, diplomacy resolver, memory, tarot, king_wen, `orchestrator.py`
- `scripts/` — analysis/extractor scripts
- `tests/`
- `docs/`
- `Makefile`, `pyproject.toml`, `uv.lock`, `README.md`, `.env.example`, `.gitignore`
- Per game: `games/*/game_meta.json`, `games/*/game_state.json`,
  `games/*/round_*/orders/` and `round_*/resolution.txt`, `games/*/round_*/orders.json`
  (structured moves + outcomes — needed to recompute winners, SCs, breach, action stats)

## Exclude (content — withhold)

- `games/*/round_*/diplomacy/`   — inter-agent negotiation transcripts (~40 MB)
- `games/*/round_*/prompts/`     — agent personas + oracle-injection design (~37 MB)
- `games/*/round_*/raw/`         — raw LLM reasoning traces (~6 MB)
- `games/*/round_*/observations/`— per-agent world views (~9 MB)
- `games/*/reflection/`          — between-game memory prompts + responses
- root `*.log`                   — campaign run logs
- `results/decision_probes_han.jsonl` — raw probe outputs (the *summary* CSV is public)

The requester gets everything to run the engine and recompute every statistic, and none of
the material reserved for creative works. Anything they still cannot reproduce is already in
the **public** paper repo as summary CSVs.

## One-command build

Drop `scripts/make_repro_bundle.sh` (below, also in this folder) into the engine repo root
and add to its `Makefile`:

```make
.PHONY: repro-bundle
repro-bundle:
	bash scripts/make_repro_bundle.sh
```

Then: `make repro-bundle` → produces `warringstates-repro-bundle.tar.gz` (code + structured
outcomes only). Review the printed file list before sending.
