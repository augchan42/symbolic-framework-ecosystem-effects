#!/usr/bin/env python3
"""Section 4.4: Pressure invariance — defensive shift under territory loss."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "han_orders.csv"


def main():
    df = pd.read_csv(DATA)

    print("=" * 60)
    print("TABLE: Pressure Invariance (§4.4)")
    print("  Defensive = hold + self_support")
    print("  Stable = post-round SCs >= 2, Losing = SCs < 2")
    print("=" * 60)

    print(f"\n  {'Condition':12s} {'Hold(stable)':>14s} {'Hold(losing)':>14s} {'Shift':>8s} {'Coop(s)':>9s} {'Coop(l)':>9s}")
    print("  " + "-" * 66)

    for cond in ["control", "yarrow", "tarot", "scrambled"]:
        sub = df[df.condition == cond]
        stable = sub[sub.pressure_pos == "stable"]
        losing = sub[sub.pressure_pos == "losing"]

        def defensive_rate(group):
            if len(group) == 0:
                return 0.0
            return (group.action.isin(["hold", "self_support"])).sum() / len(group) * 100

        def coop_rate(group):
            if len(group) == 0:
                return 0.0
            return (group.action == "other_support").sum() / len(group) * 100

        s_def = defensive_rate(stable)
        l_def = defensive_rate(losing)
        s_coop = coop_rate(stable)
        l_coop = coop_rate(losing)
        shift = l_def - s_def

        print(f"  {cond:12s} {s_def:>10.1f}% ({len(stable):>3d}) {l_def:>10.1f}% ({len(losing):>3d}) {shift:>+7.1f}pp {s_coop:>7.1f}% {l_coop:>7.1f}%")


if __name__ == "__main__":
    main()
