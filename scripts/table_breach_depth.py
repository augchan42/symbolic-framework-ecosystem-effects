#!/usr/bin/env python3
"""Reproduce the breach depth-vs-condition statistics (§4.5, ADR-018).

Reads data/breach_depth.csv (see scripts/extract_breach_depth.py) and shows that
Chu's breach of Qin's home is governed by campaign memory DEPTH (position), not by
the yarrow oracle:

  - Within-campaign trend (Spearman breach x position):
      yarrow.canonical  rho=+0.68 (p=0.003),  control.canonical rho=+0.79 (p=0.0002),
      yarrow_tiebreak_a rho=+0.87 (p=0.012).
  - Matched-depth condition test (canonical pair, n=34):
      first-10 games  yarrow 4/10 vs control 5/10 (Fisher p=1.0);
      games 11-17     yarrow 7/7  vs control 7/7  (Fisher p=1.0);
      logistic breach ~ position + condition -> position p=0.006, condition p=0.55.
  - Across 4 canonical-yarrow campaigns breach spans 40-100%.

Usage:
  python scripts/table_breach_depth.py
"""
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr, fisher_exact
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "breach_depth.csv"


def load():
    rows = []
    with open(CSV_PATH, newline="") as f:
        for r in csv.DictReader(f):
            r["position"] = int(r["position"])
            r["breach"] = int(r["breach"])
            rows.append(r)
    return rows


def main():
    if not CSV_PATH.exists():
        raise SystemExit(
            f"Missing {CSV_PATH.relative_to(ROOT)} — run "
            "scripts/extract_breach_depth.py first.")
    rows = load()
    by_camp = defaultdict(list)
    for r in rows:
        by_camp[r["campaign_id"]].append(r)
    for v in by_camp.values():
        v.sort(key=lambda r: r["position"])

    print("=== Breach: depth, not condition (§4.5, ADR-018) ===\n")

    print("Within-campaign trend (Spearman breach x campaign position):")
    for camp in ("chu_blockade_yarrow_canonical", "chu_blockade_control_canonical",
                 "yarrow_tiebreak_a", "yarrow_tiebreak_b"):
        v = by_camp.get(camp)
        if not v:
            continue
        pos = [r["position"] for r in v]
        br = [r["breach"] for r in v]
        if len(set(br)) > 1:
            rho, p = spearmanr(pos, br)
            print(f"  {camp:32} n={len(v):2} breach={sum(br)}/{len(v)}  "
                  f"rho={rho:+.2f} p={p:.4f}")
        else:
            print(f"  {camp:32} n={len(v):2} breach={sum(br)}/{len(v)}  "
                  f"(saturated — no variance)")

    print("\nMatched-depth condition test (canonical pair):")
    yc = by_camp["chu_blockade_yarrow_canonical"]
    cc = by_camp["chu_blockade_control_canonical"]
    for lo, hi, label in [(1, 10, "first-10 games"), (11, 17, "games 11-17")]:
        yb = sum(r["breach"] for r in yc if lo <= r["position"] <= hi)
        yn = sum(1 for r in yc if lo <= r["position"] <= hi)
        cb = sum(r["breach"] for r in cc if lo <= r["position"] <= hi)
        cn = sum(1 for r in cc if lo <= r["position"] <= hi)
        _, p = fisher_exact([[yb, yn - yb], [cb, cn - cb]])
        print(f"  {label:16} yarrow {yb}/{yn} vs control {cb}/{cn}  Fisher p={p:.3f}")

    # logistic breach ~ position + condition over the canonical pair (n=34)
    pair = yc + cc
    X = np.array([[1.0, r["position"], 1.0 if r["arm"] == "yarrow" else 0.0]
                  for r in pair])
    y = np.array([r["breach"] for r in pair], dtype=float)
    res = sm.Logit(y, X).fit(disp=0)
    names = ["intercept", "position", "condition(yarrow)"]
    print(f"\nLogistic breach ~ position + condition (n={len(pair)}):")
    for name, beta, p in zip(names, res.params, res.pvalues):
        print(f"  {name:18} beta={beta:+.2f}  p={p:.3f}")

    print("\nAcross 4 canonical-yarrow campaigns (breach rate):")
    for camp in ("chu_blockade_yarrow_canonical", "yarrow_tiebreak_a",
                 "yarrow_tiebreak_b", "v2_experiment_01_yarrow"):
        v = by_camp.get(camp, [])
        if not v:
            continue
        # report the first-10 rate for the deep canonical arm (the 40% reference)
        first10 = [r for r in v if r["position"] <= 10]
        b10, n10 = sum(r["breach"] for r in first10), len(first10)
        bf, nf = sum(r["breach"] for r in v), len(v)
        note = f" (first-10: {b10}/{n10}={100*b10/n10:.0f}%)" if nf > 10 else ""
        print(f"  {camp:32} {bf}/{nf} = {100*bf/nf:.0f}%{note}")

    print("\nConclusion: position drives breach (p=0.006); condition does not "
          "(p=0.55).\n  The '10/10 at R4.5' signature is a deep-memory sample, "
          "not a yarrow effect.")


if __name__ == "__main__":
    main()
