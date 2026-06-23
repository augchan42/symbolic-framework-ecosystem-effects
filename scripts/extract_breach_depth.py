#!/usr/bin/env python3
"""Extract per-game Chu->Qin home-breach data for the depth analysis (§4.5, ADR-018).

Reads game_meta.json from warringstates-engine for the chu-blockade follow-up
campaigns and writes data/breach_depth.csv with one row per game, ordered by
campaign position (start time within campaign). A "breach" is Chu ever owning a
Qin home supply center reachable through the three_gorges corridor
(hanzhong/bashu) — the metric defined in the engine's chu_blockade_analysis.py.

This supports the §4.5 finding that the breach is driven by campaign memory
DEPTH (position), not the yarrow oracle (condition).

Usage:
  WARRINGSTATES_ENGINE=/path/to/warringstates-engine \
      python scripts/extract_breach_depth.py
"""
import csv
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = Path(os.environ.get(
    "WARRINGSTATES_ENGINE",
    ROOT.parent / "warringstates-engine",
))
GAME_ROOTS = [ENGINE / "games", ENGINE / "games" / "macbook", ENGINE / "games" / "vps"]
OUT = ROOT / "data" / "breach_depth.csv"

QIN_HOME = {"hanzhong", "bashu"}  # Qin home SCs reachable via three_gorges

# campaign_id -> (arm, map)
CAMPAIGNS = {
    "chu_blockade_yarrow_canonical":  ("yarrow", "canonical"),
    "chu_blockade_control_canonical": ("control", "canonical"),
    "chu_blockade_yarrow_severed":    ("yarrow", "severed"),
    "chu_blockade_control_severed":   ("control", "severed"),
    "yarrow_tiebreak_a":              ("yarrow", "canonical"),
    "yarrow_tiebreak_b":              ("yarrow", "canonical"),
    "v2_experiment_01_yarrow":        ("yarrow", "canonical"),
}


def ownership_series(meta):
    out = {}
    for rh in meta.get("round_history", []):
        own = {}
        for st, info in rh.get("standings", {}).items():
            for t in info.get("territory_list", []):
                own[t] = st
        out[rh.get("round")] = own
    return out


def chu_breach(meta):
    """(ever_breached, first_breach_round_or_None, captures_from_qin)."""
    own = ownership_series(meta)
    first, from_qin, prev = None, 0, None
    for rn in sorted(own):
        cur = own[rn]
        if prev is not None:
            for t, o in cur.items():
                if o == "chu" and prev.get(t) == "qin":
                    from_qin += 1
        if first is None and any(cur.get(t) == "chu" for t in QIN_HOME):
            first = rn
        prev = cur
    return (first is not None), first, from_qin


def discover():
    metas = []
    seen = set()
    for root in GAME_ROOTS:
        if not root.exists():
            continue
        for d in sorted(root.iterdir()):
            mp = d / "game_meta.json"
            if not mp.exists():
                continue
            try:
                meta = json.load(open(mp))
            except (json.JSONDecodeError, OSError):
                continue
            if meta.get("campaign_id") not in CAMPAIGNS:
                continue
            gid = meta.get("game_id", d.name)
            if gid in seen:
                continue
            seen.add(gid)
            metas.append(meta)
    return metas


def main():
    metas = discover()
    if not metas:
        raise SystemExit(
            f"No campaign games found under {ENGINE}. "
            "Set WARRINGSTATES_ENGINE to the warringstates-engine checkout.")
    # group by campaign, order by start time -> campaign position
    by_camp = {}
    for m in metas:
        if not m.get("completed", True):
            continue
        by_camp.setdefault(m["campaign_id"], []).append(m)

    rows = []
    for camp, ms in sorted(by_camp.items()):
        # Campaign position = play order. Games in a campaign share a single
        # `started_at` (the campaign-launch stamp) but run sequentially while
        # memory accumulates, so completion time (`last_updated`) is the true
        # chronological order; `started_at` only breaks across-batch ties.
        ms.sort(key=lambda m: (str(m.get("started_at", "")),
                               str(m.get("last_updated", ""))))
        arm, mp = CAMPAIGNS[camp]
        for pos, m in enumerate(ms, 1):
            breached, first_round, from_qin = chu_breach(m)
            rows.append(dict(
                campaign_id=camp,
                arm=arm,
                map=mp,
                position=pos,
                breach=int(breached),
                first_breach_round=first_round if first_round is not None else "",
                captures_from_qin=from_qin,
                winner=str(m.get("winner", "")).strip().lower(),
                started_at=m.get("started_at", ""),
            ))
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} games -> {OUT.relative_to(ROOT)}")
    for camp, ms in sorted(by_camp.items()):
        n = sum(1 for r in rows if r["campaign_id"] == camp)
        b = sum(r["breach"] for r in rows if r["campaign_id"] == camp)
        print(f"  {camp:32} n={n:2}  breach={b}/{n}")


if __name__ == "__main__":
    main()
