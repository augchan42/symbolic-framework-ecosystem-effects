#!/usr/bin/env python3
"""Section 3: Han peak SC boxplot by condition."""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "game_outcomes.csv"
OUT = ROOT / "paper" / "figures" / "peak-scs-by-condition.pdf"

COND_ORDER = ["control", "yarrow", "tarot", "scrambled"]


def main():
    df = pd.read_csv(DATA)

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))

    groups = [df[df.condition == c].han_peak_scs.values for c in COND_ORDER]
    bp = ax.boxplot(groups, positions=range(len(COND_ORDER)), widths=0.6, patch_artist=True)

    colors = ['#888888', '#4477AA', '#CC6677', '#999933']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # Overlay individual points
    for i, (cond, vals) in enumerate(zip(COND_ORDER, groups)):
        jitter = 0.1 * (pd.Series(range(len(vals))) - len(vals)/2) / len(vals)
        ax.scatter([i] * len(vals) + jitter, vals, alpha=0.5, s=20, color='black', zorder=3)

    ax.axhline(y=2, color='gray', linestyle='--', alpha=0.5, label='Starting SCs (2)')
    ax.set_xticks(range(len(COND_ORDER)))
    ax.set_xticklabels(["Control", "Yarrow\n(I Ching)", "Tarot", "Scrambled"])
    ax.set_ylabel("Han Peak Supply Centers")
    ax.set_title("Han Peak Territory: Tarot Elevates, Others Do Not\n(KW p=0.008)")
    ax.legend(loc='upper right')

    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=150, bbox_inches='tight')
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
