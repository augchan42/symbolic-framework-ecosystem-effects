#!/usr/bin/env python3
"""Section 4: Ecosystem Redirection — winner distributions and Fisher tests."""
import pandas as pd
from scipy.stats import fisher_exact
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "game_outcomes.csv"


def main():
    df = pd.read_csv(DATA)

    print("="*60)
    print("TABLE: Winner Distributions by Condition (Section 4)")
    print("="*60)

    for cond in ["control", "yarrow", "tarot", "scrambled"]:
        sub = df[df.condition == cond]
        winners = Counter(sub.winner)
        n = len(sub)
        print(f"\n  {cond:10s} (n={n}): {dict(winners.most_common())}")

    print(f"\n{'='*60}")
    print("FISHER EXACT TESTS")
    print(f"{'='*60}")

    # Qin suppression under yarrow
    print("\n--- Qin Suppression ---")
    qin_y = (df[(df.condition == "yarrow") & (df.winner == "qin")].shape[0],
             df[df.condition == "yarrow"].shape[0])
    qin_t = (df[(df.condition == "tarot") & (df.winner == "qin")].shape[0],
             df[df.condition == "tarot"].shape[0])
    qin_c = (df[(df.condition == "control") & (df.winner == "qin")].shape[0],
             df[df.condition == "control"].shape[0])

    table = [[qin_y[0], qin_y[1] - qin_y[0]], [qin_t[0], qin_t[1] - qin_t[0]]]
    _, p = fisher_exact(table)
    print(f"  Yarrow vs Tarot: {qin_y[0]}/{qin_y[1]} vs {qin_t[0]}/{qin_t[1]}, Fisher p={p:.4f}")

    table = [[qin_y[0], qin_y[1] - qin_y[0]], [qin_c[0], qin_c[1] - qin_c[0]]]
    _, p = fisher_exact(table)
    print(f"  Yarrow vs Control: {qin_y[0]}/{qin_y[1]} vs {qin_c[0]}/{qin_c[1]}, Fisher p={p:.4f}")

    # vs all others
    qin_others = df[(df.condition != "yarrow") & (df.winner == "qin")].shape[0]
    n_others = df[df.condition != "yarrow"].shape[0]
    table = [[qin_y[0], qin_y[1] - qin_y[0]], [qin_others, n_others - qin_others]]
    _, p = fisher_exact(table)
    print(f"  Yarrow vs All others: {qin_y[0]}/{qin_y[1]} vs {qin_others}/{n_others}, Fisher p={p:.4f}")

    # Qi dominance under scrambled
    print("\n--- Qi Dominance ---")
    qi_s = (df[(df.condition == "scrambled") & (df.winner == "qi")].shape[0],
            df[df.condition == "scrambled"].shape[0])
    qi_others = df[(df.condition != "scrambled") & (df.winner == "qi")].shape[0]
    n_others = df[df.condition != "scrambled"].shape[0]
    table = [[qi_s[0], qi_s[1] - qi_s[0]], [qi_others, n_others - qi_others]]
    _, p = fisher_exact(table)
    print(f"  Scrambled vs All others: {qi_s[0]}/{qi_s[1]} vs {qi_others}/{n_others}, Fisher p={p:.4f}")

    # Tarot-Qin vs pooled others
    print("\n--- Tarot-Qin ---")
    qin_pooled = df[(df.condition != "tarot") & (df.winner == "qin")].shape[0]
    n_pooled = df[df.condition != "tarot"].shape[0]
    table = [[qin_t[0], qin_t[1] - qin_t[0]], [qin_pooled, n_pooled - qin_pooled]]
    _, p = fisher_exact(table)
    print(f"  Tarot vs Pooled others: {qin_t[0]}/{qin_t[1]} vs {qin_pooled}/{n_pooled}, Fisher p={p:.4f}")


if __name__ == "__main__":
    main()
