#!/usr/bin/env python3
"""Extract Han's per-round orders and oracle cast data from warringstates-engine.

Produces two CSVs:
  data/han_orders.csv     — every Han order with action classification
  data/oracle_casts.csv   — per-round oracle data (hexagram/tarot) for all conditions

These CSVs support reproducing the behavioral claims in §4.1–4.5:
  - Turtle tendency baseline (hold/move/support rates)
  - Framework-specific behavioral profiles (Table 3)
  - Late-game cooperation rates (Table 5)
  - Pressure invariance (defensive shift under territory loss)
  - Content-action independence (hexagram theme × action, tarot posture × action)
"""
import csv
import json
import glob
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = Path(os.environ.get(
    "WARRINGSTATES_ENGINE",
    ROOT.parent / "warringstates-engine",
))

from dataset import CLEAN_DATASET


def find_game_dir(game_id):
    """Find the game directory, checking games/ and games/macbook/."""
    for subdir in ["games", "games/macbook", "games/vps"]:
        candidate = ENGINE / subdir / game_id
        if candidate.is_dir():
            return candidate
    return None


def get_total_rounds(game_dir):
    """Count round directories to determine total rounds played."""
    return len(glob.glob(str(game_dir / "round_*")))


def get_han_sc_trajectory(game_dir):
    """Extract Han's SC count per round from game_meta.json.

    Returns dict mapping round_index (0-based position in round_history)
    to SC count. round_history[i] = standings after round i+1 resolves.
    """
    meta_path = game_dir / "game_meta.json"
    if not meta_path.exists():
        return []
    with open(meta_path) as f:
        meta = json.load(f)
    trajectory = []
    for rh in meta.get("round_history", []):
        standings = rh.get("standings", {})
        if "han" in standings:
            trajectory.append(standings["han"].get("supply_centers", 0))
        else:
            trajectory.append(0)
    return trajectory


def classify_phase(round_num, total_rounds):
    """Divide game into thirds: early, mid, late."""
    third = total_rounds / 3.0
    if round_num <= third:
        return "early"
    elif round_num <= 2 * third:
        return "mid"
    else:
        return "late"


def classify_action(order):
    """Classify Han order into action type.

    Categories (from v0.4 §3.6):
      hold         — hold in place
      self_support — support own unit (support_state == han)
      other_support— support another state's unit
      move         — any move order (includes reposition/expand/attack)
    """
    order_type = order.get("order", "").lower()
    if order_type == "hold":
        return "hold"
    elif order_type == "move":
        return "move"
    elif order_type == "support":
        support_state = order.get("support_state", "").lower()
        if support_state == "han":
            return "self_support"
        else:
            return "other_support"
    return "unknown"


def pressure_bucket(sc_delta):
    """Bucket SC delta into pressure level (matches warringstates-engine)."""
    if sc_delta <= -2:
        return "crisis"
    elif sc_delta == -1:
        return "losing"
    elif sc_delta == 0:
        return "stable"
    elif sc_delta == 1:
        return "gaining"
    return "surging"


def pressure_position(han_scs, starting_scs=2):
    """Absolute SC-position pressure (matches paper §4.4 pressure invariance).

    'losing' = below starting position, 'stable' = at or above.
    Uses post-round SCs paired with the same round's orders.
    """
    return "losing" if han_scs < starting_scs else "stable"


def extract_han_orders():
    """Extract all Han orders across the clean dataset."""
    rows = []
    for condition, game_ids in CLEAN_DATASET.items():
        for game_id in game_ids:
            game_dir = find_game_dir(game_id)
            if game_dir is None:
                print(f"  MISSING: {game_id}", file=sys.stderr)
                continue

            total_rounds = get_total_rounds(game_dir)
            sc_traj = get_han_sc_trajectory(game_dir)

            for rnd in range(1, total_rounds + 1):
                han_file = game_dir / f"round_{rnd:02d}" / "orders" / "han.json"
                if not han_file.exists():
                    continue

                with open(han_file) as f:
                    data = json.load(f)

                phase = classify_phase(rnd, total_rounds)
                r_idx = rnd - 1
                han_scs = sc_traj[r_idx] if r_idx < len(sc_traj) else 0
                prev_scs = sc_traj[r_idx - 1] if r_idx > 0 and r_idx - 1 < len(sc_traj) else 2
                sc_delta = han_scs - prev_scs
                pressure = pressure_bucket(sc_delta)

                pressure_pos = pressure_position(han_scs)

                for order in data.get("orders", []):
                    action = classify_action(order)
                    reasoning = order.get("reasoning", "")
                    rows.append({
                        "game_id": game_id,
                        "condition": condition,
                        "round": rnd,
                        "total_rounds": total_rounds,
                        "phase": phase,
                        "han_scs": han_scs,
                        "sc_delta": sc_delta,
                        "pressure": pressure,
                        "pressure_pos": pressure_pos,
                        "unit": order.get("unit", ""),
                        "order_type": order.get("order", ""),
                        "action": action,
                        "target": order.get("target", ""),
                        "support_state": order.get("support_state", ""),
                        "reasoning_chars": len(reasoning),
                    })
    return rows


def extract_oracle_casts():
    """Extract oracle cast data (hexagram/tarot) for every round."""
    rows = []
    for condition, game_ids in CLEAN_DATASET.items():
        for game_id in game_ids:
            game_dir = find_game_dir(game_id)
            if game_dir is None:
                continue

            total_rounds = get_total_rounds(game_dir)
            for rnd in range(1, total_rounds + 1):
                oracle_file = game_dir / f"round_{rnd:02d}" / "oracle_cast.json"
                if not oracle_file.exists():
                    continue

                with open(oracle_file) as f:
                    cast = json.load(f)

                method = cast.get("method", "")
                if method == "yarrow_stalk":
                    rows.append({
                        "game_id": game_id,
                        "condition": condition,
                        "round": rnd,
                        "method": method,
                        "hexagram_number": cast.get("hexagram_number", ""),
                        "card_1": "",
                        "card_2": "",
                        "card_3": "",
                        "posture_1": "",
                        "posture_2": "",
                        "posture_3": "",
                    })
                elif method == "tarot_spread":
                    cards = cast.get("card_names", ["", "", ""])
                    postures = cast.get("card_postures", ["", "", ""])
                    rows.append({
                        "game_id": game_id,
                        "condition": condition,
                        "round": rnd,
                        "method": method,
                        "hexagram_number": "",
                        "card_1": cards[0] if len(cards) > 0 else "",
                        "card_2": cards[1] if len(cards) > 1 else "",
                        "card_3": cards[2] if len(cards) > 2 else "",
                        "posture_1": postures[0] if len(postures) > 0 else "",
                        "posture_2": postures[1] if len(postures) > 1 else "",
                        "posture_3": postures[2] if len(postures) > 2 else "",
                    })
    return rows


def main():
    if not ENGINE.is_dir():
        print(f"ERROR: warringstates-engine not found at {ENGINE}", file=sys.stderr)
        print("Set WARRINGSTATES_ENGINE env var to the correct path.", file=sys.stderr)
        sys.exit(1)

    print("Extracting Han orders...")
    orders = extract_han_orders()
    orders_path = ROOT / "data" / "han_orders.csv"
    with open(orders_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "game_id", "condition", "round", "total_rounds", "phase",
            "han_scs", "sc_delta", "pressure", "pressure_pos",
            "unit", "order_type", "action", "target", "support_state",
            "reasoning_chars",
        ])
        writer.writeheader()
        writer.writerows(orders)
    print(f"  {len(orders)} orders -> {orders_path}")

    # Summary
    from collections import Counter
    by_cond = {}
    for r in orders:
        cond = r["condition"]
        if cond not in by_cond:
            by_cond[cond] = Counter()
        by_cond[cond][r["action"]] += 1

    for cond in ["control", "yarrow", "tarot", "scrambled"]:
        c = by_cond.get(cond, Counter())
        total = sum(c.values())
        print(f"  {cond} ({total} orders): "
              f"hold={c['hold']/total:.1%} move={c['move']/total:.1%} "
              f"self_support={c['self_support']/total:.1%} "
              f"other_support={c['other_support']/total:.1%}")

    # Pressure invariance (§4.4): defensive = hold+self_support, absolute SC position
    print("\n  Pressure invariance (hold+self_support, SCs<2 = losing):")
    for cond in ["control", "yarrow", "tarot", "scrambled"]:
        cr = [r for r in orders if r["condition"] == cond]
        stable = [r for r in cr if r["pressure_pos"] == "stable"]
        losing = [r for r in cr if r["pressure_pos"] == "losing"]
        def def_rate(subset):
            if not subset:
                return 0.0
            return sum(1 for r in subset if r["action"] in ("hold", "self_support")) / len(subset) * 100
        s, l = def_rate(stable), def_rate(losing)
        print(f"    {cond}: stable={s:.1f}% (n={len(stable)}), "
              f"losing={l:.1f}% (n={len(losing)}), shift={l-s:+.1f}pp")

    print("\nExtracting oracle casts...")
    casts = extract_oracle_casts()
    casts_path = ROOT / "data" / "oracle_casts.csv"
    with open(casts_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "game_id", "condition", "round", "method",
            "hexagram_number", "card_1", "card_2", "card_3",
            "posture_1", "posture_2", "posture_3",
        ])
        writer.writeheader()
        writer.writerows(casts)
    print(f"  {len(casts)} casts -> {casts_path}")

    by_method = Counter(r["method"] for r in casts)
    print(f"  yarrow_stalk: {by_method.get('yarrow_stalk', 0)}, "
          f"tarot_spread: {by_method.get('tarot_spread', 0)}")


if __name__ == "__main__":
    main()
