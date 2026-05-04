#!/usr/bin/env python3
"""Section 5: Perturbativeness Gradient — reasoning length dose-response."""
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kruskal, mannwhitneyu
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "reasoning_lengths.csv"
OUT = ROOT / "paper" / "figures" / "reasoning-length-gradient.pdf"


def main():
    df = pd.read_csv(DATA)

    # Non-Han only (the perturbativeness gradient is about OTHER agents' reasoning)
    non_han = df[df.state != "han"]

    # Per-game weighted mean (weight by n_orders so each individual order counts equally)
    def weighted_mean(group):
        total_chars = (group.mean_reasoning_chars * group.n_orders).sum()
        total_orders = group.n_orders.sum()
        return total_chars / total_orders if total_orders > 0 else 0.0

    per_game = non_han.groupby(["game_id", "condition"]).apply(weighted_mean).reset_index()
    per_game.columns = ["game_id", "condition", "mean_reasoning_chars"]

    print("="*60)
    print("Non-Han Reasoning Length by Condition (per-game means)")
    print("="*60)

    cond_order = ["control", "yarrow", "tarot", "scrambled"]
    for cond in cond_order:
        vals = per_game[per_game.condition == cond].mean_reasoning_chars
        print(f"  {cond:10s}: mean={vals.mean():.1f}, median={vals.median():.1f}, n={len(vals)}")

    # Kruskal-Wallis
    groups = [per_game[per_game.condition == c].mean_reasoning_chars.values for c in cond_order]
    h, p = kruskal(*groups)
    print(f"\n  Kruskal-Wallis (4-way): H={h:.3f}, p={p:.6f}")

    # Pairwise MWU
    print("\n  Pairwise MWU:")
    for i in range(len(cond_order)):
        for j in range(i+1, len(cond_order)):
            u, p = mannwhitneyu(groups[i], groups[j], alternative="two-sided")
            print(f"    {cond_order[i]} vs {cond_order[j]}: U={u:.1f}, p={p:.4f}")

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    positions = range(len(cond_order))
    bp = ax.boxplot([groups[i] for i in range(len(cond_order))],
                    positions=positions, widths=0.6, patch_artist=True)

    colors = ['#888888', '#4477AA', '#CC6677', '#999933']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_xticks(positions)
    ax.set_xticklabels(["Control", "Yarrow\n(I Ching)", "Tarot", "Scrambled"])
    ax.set_ylabel("Mean reasoning chars per order (non-Han agents)")
    ax.set_title("Perturbativeness Gradient: Non-Han Reasoning Length")
    ax.axhline(y=per_game[per_game.condition == "control"].mean_reasoning_chars.mean(),
               color='gray', linestyle='--', alpha=0.5, label='Control mean')

    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=150, bbox_inches='tight')
    print(f"\n  Saved: {OUT}")


if __name__ == "__main__":
    main()
