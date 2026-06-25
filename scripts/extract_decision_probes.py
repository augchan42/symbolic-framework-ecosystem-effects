#!/usr/bin/env python3
"""Extract the memory-free decision-isolation probe into a summary CSV.

Reads the raw probe log from warringstates-engine
(results/decision_probes_han.jsonl, 960 Han probes, ADR-019) and writes
data/decision_probes_summary.csv with one row per (scenario, arm, replicate).

The summary keeps everything needed to reproduce the §4.3 "memory-free decision
isolation" statistics without shipping the multi-MB raw LLM transcripts:
  - hold/move/support rates and reasoning length (the H2 risk-aversion DV), and
  - a canonical, set-serialized order signature (`order_set`) so the H1 Jaccard
    order-divergence vs. the control-vs-control noise floor can be recomputed.

Usage:
  WARRINGSTATES_ENGINE=/path/to/warringstates-engine \
      python scripts/extract_decision_probes.py
"""
import csv
import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = Path(os.environ.get(
    "WARRINGSTATES_ENGINE",
    ROOT.parent / "warringstates-engine",
))
SRC = ENGINE / "results" / "decision_probes_han.jsonl"
OUT = ROOT / "data" / "decision_probes_summary.csv"


def canon(order):
    """Canonical, hashable order tuple (mirrors the engine analyzer)."""
    if not isinstance(order, dict):
        return ("?",)
    return (str(order.get("unit", "")).strip().lower(),
            str(order.get("order", "")).strip().lower(),
            str(order.get("target", "") or "").strip().lower(),
            str(order.get("support_state", "") or "").strip().lower(),
            str(order.get("support_action", "") or "").strip().lower())


def serialize_order_set(orders):
    """Set semantics (frozenset in the engine): sorted, de-duplicated."""
    uniq = sorted({"|".join(canon(o)) for o in (orders or [])})
    return ";".join(uniq)


def count(orders, kind):
    """Raw count of a given order kind. Counts (not pre-divided rates) are
    stored so the table script can recompute rates at full float precision,
    matching the engine analyzer exactly (rounding rates here would perturb
    Friedman tie-ranking)."""
    return sum(1 for o in orders if isinstance(o, dict)
               and str(o.get("order", "")).lower() == kind)


def main():
    if not SRC.exists():
        raise SystemExit(
            f"Source not found: {SRC}\n"
            "Set WARRINGSTATES_ENGINE to the warringstates-engine checkout.")
    rows = []
    arm_counts = Counter()
    for line in SRC.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("orders") is None or r.get("error"):
            continue
        orders = r["orders"]
        rows.append(dict(
            scenario_id=r["scenario_id"],
            phase=r.get("phase", ""),
            arm=r["arm"],
            replicate=r.get("replicate", 0),
            n_orders=len(orders),
            hold_n=count(orders, "hold"),
            move_n=count(orders, "move"),
            support_n=count(orders, "support"),
            reasoning_len=r.get("reasoning_len", ""),
            order_set=serialize_order_set(orders),
        ))
        arm_counts[r["arm"]] += 1
    if not rows:
        raise SystemExit(
            f"No valid probe records in {SRC} (all rows were error/None-orders). "
            "Nothing written.")
    rows.sort(key=lambda x: (x["scenario_id"], x["arm"], x["replicate"]))
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {OUT.relative_to(ROOT)}")
    print(f"  arms: {dict(arm_counts)}")
    print(f"  scenarios: {len({r['scenario_id'] for r in rows})}")


if __name__ == "__main__":
    main()
