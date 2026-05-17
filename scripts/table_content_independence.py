#!/usr/bin/env python3
"""§4.3 Content-Action Independence: hexagram theme × action, tarot posture × action.

Methodology:
  - Unit of analysis: per-order (each Han order paired with its round's oracle cast)
  - Action categories: raw 4-category scheme (hold, move, self_support, other_support)
  - Hexagram themes: 64 hexagrams classified into advance/retreat/wait/cooperate
  - Tarot postures: dominant decision_posture from 3-card spread
"""

import pandas as pd
from scipy import stats
from collections import Counter

orders = pd.read_csv("data/han_orders.csv")
casts = pd.read_csv("data/oracle_casts.csv")

# Standard I Ching thematic groupings (advance/retreat/wait/cooperate)
HEX_THEMES = {
    1: "advance", 2: "wait", 3: "wait", 4: "wait", 5: "wait", 6: "retreat",
    7: "advance", 8: "cooperate", 9: "wait", 10: "advance", 11: "advance", 12: "retreat",
    13: "cooperate", 14: "advance", 15: "wait", 16: "advance", 17: "cooperate", 18: "retreat",
    19: "advance", 20: "wait", 21: "advance", 22: "wait", 23: "retreat", 24: "advance",
    25: "wait", 26: "advance", 27: "wait", 28: "advance", 29: "retreat", 30: "advance",
    31: "cooperate", 32: "wait", 33: "retreat", 34: "advance", 35: "advance", 36: "retreat",
    37: "cooperate", 38: "retreat", 39: "retreat", 40: "advance", 41: "retreat", 42: "advance",
    43: "advance", 44: "retreat", 45: "cooperate", 46: "advance", 47: "retreat", 48: "wait",
    49: "advance", 50: "wait", 51: "advance", 52: "wait", 53: "wait", 54: "retreat",
    55: "advance", 56: "retreat", 57: "wait", 58: "cooperate", 59: "retreat", 60: "wait",
    61: "cooperate", 62: "wait", 63: "wait", 64: "advance",
}

print("=" * 60)
print("CONTENT-ACTION INDEPENDENCE (§4.3)")
print("  Unit of analysis: per-order")
print("  Actions: hold / move / self_support / other_support")
print("=" * 60)

# --- HEXAGRAM THEME × ACTION ---
yarrow_casts = casts[casts["condition"] == "yarrow"].copy()
yarrow_casts["hexagram_number"] = pd.to_numeric(yarrow_casts["hexagram_number"], errors="coerce")
yarrow_casts = yarrow_casts.dropna(subset=["hexagram_number"])
yarrow_casts["hex_theme"] = yarrow_casts["hexagram_number"].astype(int).map(HEX_THEMES)

yarrow_orders = orders[orders["condition"] == "yarrow"].copy()

merged = yarrow_orders.merge(
    yarrow_casts[["game_id", "round", "hex_theme"]],
    on=["game_id", "round"], how="inner",
)

print(f"\nYarrow Han orders with hexagram: {len(merged)}")
print(f"  Theme distribution: {merged['hex_theme'].value_counts().to_dict()}")

ct = pd.crosstab(merged["hex_theme"], merged["action"])
print(f"\nHexagram theme × action contingency table:")
print(ct)

chi2, p, dof, expected = stats.chi2_contingency(ct)
print(f"\nPearson chi2 = {chi2:.4f}, dof = {dof}, p = {p:.4f}")

# Fisher for advance hexagram vs move action
merged["is_advance_hex"] = merged["hex_theme"] == "advance"
merged["is_move"] = merged["action"] == "move"
ct_fisher = pd.crosstab(merged["is_advance_hex"], merged["is_move"])
print(f"\nAdvance-hexagram × move-action 2×2:")
print(ct_fisher)
odds_ratio, fisher_p = stats.fisher_exact(ct_fisher)
print(f"Fisher exact: OR = {odds_ratio:.2f}, p = {fisher_p:.4f}")

# --- TAROT POSTURE × ACTION ---
print("\n" + "=" * 60)

tarot_casts = casts[casts["condition"] == "tarot"].copy()
tarot_orders = orders[orders["condition"] == "tarot"].copy()


def dominant_posture(row):
    postures = [row.get(f"posture_{i}", "") for i in range(1, 4)]
    postures = [p for p in postures if pd.notna(p) and p != ""]
    if not postures:
        return None
    return Counter(postures).most_common(1)[0][0]


tarot_casts["dominant_posture"] = tarot_casts.apply(dominant_posture, axis=1)
tarot_casts = tarot_casts.dropna(subset=["dominant_posture"])

merged_t = tarot_orders.merge(
    tarot_casts[["game_id", "round", "dominant_posture"]],
    on=["game_id", "round"], how="inner",
)

print(f"Tarot Han orders with posture: {len(merged_t)}")
print(f"  Posture distribution: {merged_t['dominant_posture'].value_counts().to_dict()}")

ct_t = pd.crosstab(merged_t["dominant_posture"], merged_t["action"])
print(f"\nTarot posture × action contingency table:")
print(ct_t)

chi2_t, p_t, dof_t, _ = stats.chi2_contingency(ct_t)
print(f"\nPearson chi2 = {chi2_t:.4f}, dof = {dof_t}, p = {p_t:.4f}")
