#!/usr/bin/env python3
"""Section 4 (factorial): Winner distribution across the 2x2 factorial decomposition.

Control and yarrow winners come from data/game_outcomes.csv (the 4 primary
conditions). Decision-only and learning-only winners come from
data/factorial_outcomes.csv, derived from the engine game_meta winner field
(army-tiebreaker; multi-state draws collapsed to "draw"), matching Table 6.
"""
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIMARY = ROOT / "data" / "game_outcomes.csv"
FACTORIAL = ROOT / "data" / "factorial_outcomes.csv"
OUT = ROOT / "paper" / "figures" / "factorial-winners.pdf"

STATES = ["qin", "han", "wei", "zhao", "qi", "chu", "yan", "draw"]
# Columns ordered as the 2x2 factorial reads: top row (no framework reflection),
# bottom row (framework reflection); left (no oracle), right (oracle).
COND_ORDER = ["control", "decision_only", "learning_only", "yarrow"]
COND_TITLE = {
    "control": "Control",
    "decision_only": "Decision-only",
    "learning_only": "Learning-only",
    "yarrow": "Yarrow (full)",
}
STATE_COLORS = {
    "qin": "#CC0000", "han": "#006600", "wei": "#FF8800", "zhao": "#0066CC",
    "qi": "#9900CC", "chu": "#009999", "yan": "#666666", "draw": "#BBBBBB",
}


def load():
    df = pd.concat([pd.read_csv(PRIMARY), pd.read_csv(FACTORIAL)], ignore_index=True)
    df["winner"] = df["winner"].str.strip().str.lower()
    df.loc[df.winner.str.startswith("draw"), "winner"] = "draw"
    return df


def main():
    df = load()
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.5), sharey=True)

    for ax, cond in zip(axes, COND_ORDER):
        sub = df[df.condition == cond]
        n = len(sub)
        winners = Counter(sub.winner)
        bars = [winners.get(s, 0) for s in STATES]
        colors = [STATE_COLORS[s] for s in STATES]
        ax.bar(range(len(STATES)), bars, color=colors, alpha=0.8)
        ax.set_xticks(range(len(STATES)))
        labels = [s.capitalize() if s != "draw" else "Draw" for s in STATES]
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.set_title(f"{COND_TITLE[cond]} (n={n})")
        ax.set_ylim(0, 7)
        ax.axhline(y=n / 7, color="gray", linestyle="--", alpha=0.4)

    axes[0].set_ylabel("Games won")
    fig.suptitle(
        "Factorial Decomposition: Decision-Time and Learning-Time Components "
        "Both Inflate Draws; Only Combined Yarrow Yields Chu/Yan Co-Dominance",
        fontsize=10,
    )
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=150, bbox_inches="tight")
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
