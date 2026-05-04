#!/usr/bin/env python3
"""Section 3: No Local Benefit — Han survival and peak SCs by condition."""
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "game_outcomes.csv"


def main():
    df = pd.read_csv(DATA)

    print("="*60)
    print("TABLE: Han Outcomes by Condition (Section 3)")
    print("="*60)

    for cond in ["control", "yarrow", "tarot", "scrambled"]:
        sub = df[df.condition == cond]
        n = len(sub)
        survived = sub.han_survived.sum()
        peak_mean = sub.han_peak_scs.mean()
        peak_vals = sorted(sub.han_peak_scs.tolist())
        print(f"\n  {cond:10s} (n={n})")
        print(f"    Survival (loose): {survived}/{n} = {100*survived/n:.0f}%")
        print(f"    Peak SCs: mean={peak_mean:.2f}, dist={peak_vals}")

    # Statistical tests
    print(f"\n{'='*60}")
    print("STATISTICAL TESTS")
    print(f"{'='*60}")

    groups = [df[df.condition == c].han_peak_scs.values for c in ["control", "yarrow", "tarot", "scrambled"]]
    h, p = kruskal(*groups)
    print(f"\n  Kruskal-Wallis (4-way peak SCs): H={h:.3f}, p={p:.4f}")

    h3, p3 = kruskal(*groups[:3])
    print(f"  Kruskal-Wallis (3-way, excl scrambled): H={h3:.3f}, p={p3:.4f}")

    tarot = df[df.condition == "tarot"].han_peak_scs.values
    others = df[df.condition != "tarot"].han_peak_scs.values
    u, p = mannwhitneyu(tarot, others, alternative="greater")
    print(f"  MWU tarot > all others: U={u:.1f}, p={p:.4f}")

    for other_cond in ["control", "yarrow", "scrambled"]:
        other = df[df.condition == other_cond].han_peak_scs.values
        u, p = mannwhitneyu(tarot, other, alternative="greater")
        print(f"  MWU tarot > {other_cond}: U={u:.1f}, p={p:.4f}")


if __name__ == "__main__":
    main()
