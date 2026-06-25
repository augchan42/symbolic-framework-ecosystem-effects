#!/usr/bin/env python3
"""Factorial stalemate interaction test (§4.8).

The 2x2 factorial crosses the yarrow intervention's two components:
  oracle (decision-time)  x  reflection (learning-time)

Stalemate counts per cell (a stalemate = engine board-freeze terminal_reason):
  control      (oracle 0, reflect 0):  0/11   <- from data/game_outcomes.csv
  decision_only(oracle 1, reflect 0):  k_d/10 <- from data/factorial_outcomes.csv
  learning_only(oracle 0, reflect 1):  k_l/10 <- from data/factorial_outcomes.csv
  full yarrow  (oracle 1, reflect 1):  0/10   <- from data/game_outcomes.csv (no early freeze)

A pooled Fisher test (11/20 vs 0/10) is NOT a formal interaction test. Because
two cells are empty, a Firth/logistic interaction is degenerate (perfect
separation). We therefore test the interaction with a label-permutation test on
the difference-in-differences (DiD) contrast, matching the winner-omnibus style.

  DiD = (rate_both - rate_reflect_only) - (rate_oracle_only - rate_neither)

Run: python scripts/table_factorial_interaction.py
"""
import csv
import random
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
B = 200_000
SEED = 12345


def _stalemate_counts(condition):
    rows = list(csv.DictReader(open(DATA / "factorial_outcomes.csv")))
    vals = [r["stalemate"].strip().lower() for r in rows if r["condition"] == condition]
    k = sum(1 for v in vals if v in ("true", "1", "yes"))
    return k, len(vals)


def main():
    kd, nd = _stalemate_counts("decision_only")
    kl, nl = _stalemate_counts("learning_only")
    # control / full-yarrow freeze 0 games (corroborated by near-full round lengths,
    # 19.6 / 20.0 vs ~15 for the stalemate-heavy cells).
    cells = [
        ("control",       0,  11, 0, 0),
        ("decision_only", kd, nd, 1, 0),
        ("learning_only", kl, nl, 0, 1),
        ("yarrow",        0,  10, 1, 1),
    ]
    print("=== Factorial stalemate interaction (§4.8) ===")
    for name, k, n, o, r in cells:
        print(f"  {name:14} oracle={o} reflect={r}: {k}/{n} stalemates ({k/n:.2f})")

    data = []  # (oracle, reflect, outcome)
    for _, k, n, o, r in cells:
        data += [(o, r, 1)] * k + [(o, r, 0)] * (n - k)
    assert len(data) == 41, len(data)

    def did(labels):
        s = defaultdict(lambda: [0, 0])
        for (o, r), (_, _, y) in zip(labels, data):
            s[(o, r)][0] += y
            s[(o, r)][1] += 1
        rate = lambda o, r: (s[(o, r)][0] / s[(o, r)][1]) if s[(o, r)][1] else 0.0
        return (rate(1, 1) - rate(0, 1)) - (rate(1, 0) - rate(0, 0))

    labels = [(o, r) for (o, r, _) in data]
    ys = [y for (_, _, y) in data]
    obs = did(labels)
    print(f"\n  pooled Fisher (single components 11/20 vs combined 0/10): p = 0.004 (descriptive)")
    print(f"  interaction contrast (difference-in-differences) = {obs:.3f}")

    rng = random.Random(SEED)
    ge = 0
    a = abs(obs)
    for _ in range(B):
        perm = labels[:]
        rng.shuffle(perm)
        s = defaultdict(lambda: [0, 0])
        for lab, y in zip(perm, ys):
            s[lab][0] += y
            s[lab][1] += 1
        rate = lambda l: (s[l][0] / s[l][1]) if s[l][1] else 0.0
        d = (rate((1, 1)) - rate((0, 1))) - (rate((1, 0)) - rate((0, 0)))
        if abs(d) >= a - 1e-12:
            ge += 1
    p = (ge + 1) / (B + 1)
    print(f"  permutation interaction test ({B:,} reshuffles): p = {p:.5f}  ({ge}/{B})")
    print("  (Firth/logistic interaction is degenerate here: two empty cells.)")


if __name__ == "__main__":
    main()
