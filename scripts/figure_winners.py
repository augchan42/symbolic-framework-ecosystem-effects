#!/usr/bin/env python3
"""Section 4: Winner distribution bar chart by condition."""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "game_outcomes.csv"
OUT = ROOT / "paper" / "figures" / "winner-distributions.pdf"

STATES = ["qin", "han", "wei", "zhao", "qi", "chu", "yan"]
COND_ORDER = ["control", "yarrow", "tarot", "scrambled"]
STATE_COLORS = {
    "qin": "#CC0000",
    "han": "#006600",
    "wei": "#FF8800",
    "zhao": "#0066CC",
    "qi": "#9900CC",
    "chu": "#009999",
    "yan": "#666666",
}


def main():
    df = pd.read_csv(DATA)

    fig, axes = plt.subplots(1, 4, figsize=(12, 3.5), sharey=True)

    for ax, cond in zip(axes, COND_ORDER):
        sub = df[df.condition == cond]
        n = len(sub)
        winners = Counter(sub.winner)

        bars = [winners.get(s, 0) for s in STATES]
        colors = [STATE_COLORS[s] for s in STATES]

        ax.bar(range(len(STATES)), bars, color=colors, alpha=0.8)
        ax.set_xticks(range(len(STATES)))
        ax.set_xticklabels([s.capitalize() for s in STATES], rotation=45, ha='right', fontsize=8)
        ax.set_title(f"{cond.capitalize()} (n={n})")
        ax.set_ylim(0, 7)
        ax.axhline(y=n/7, color='gray', linestyle='--', alpha=0.4)

    axes[0].set_ylabel("Games won")
    fig.suptitle("Winner Distributions: Each Framework Produces a Distinct Ecosystem", fontsize=11)
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=150, bbox_inches='tight')
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
