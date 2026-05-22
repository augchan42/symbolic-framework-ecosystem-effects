#!/usr/bin/env python3
"""Extract per-game, per-state reasoning lengths from warringstates-engine.

Reads order JSON files from the source game directories and writes
data/reasoning_lengths.csv with one row per (game, state) pair.
"""
import json
import os
import csv
from pathlib import Path

from dataset import CLEAN_DATASET

ROOT = Path(__file__).resolve().parent.parent
ENGINE_ROOT = Path(os.environ.get(
    "WARRINGSTATES_ENGINE",
    ROOT.parent / "warringstates-engine",
))
OUTPUT = ROOT / "data" / "reasoning_lengths.csv"


def find_game_dir(game_id):
    """Find the game directory, checking games/ and games/macbook/."""
    for subdir in ["games", "games/macbook", "games/vps"]:
        candidate = ENGINE_ROOT / subdir / game_id
        if candidate.is_dir():
            return candidate
    return None

STATES = ["qin", "han", "wei", "zhao", "qi", "chu", "yan"]


def list_round_dirs(game_dir):
    if not game_dir.is_dir():
        return []
    return sorted(
        d for d in game_dir.iterdir()
        if d.name.startswith("round_") and d.is_dir()
    )


def extract_reasoning_lengths(game_dir, state):
    """Return (mean_reasoning_chars, n_orders) for a state in a game."""
    chars = []
    for round_dir in list_round_dirs(game_dir):
        order_file = round_dir / "orders" / f"{state}.json"
        if not order_file.exists():
            continue
        try:
            with open(order_file) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        for order in data.get("orders", []) or []:
            r = (order.get("reasoning") or "").strip()
            chars.append(len(r))
    if not chars:
        return 0.0, 0
    return sum(chars) / len(chars), len(chars)


def main():
    rows = []
    for cond, game_ids in CLEAN_DATASET.items():
        for game_id in game_ids:
            game_dir = find_game_dir(game_id)
            if game_dir is None:
                print(f"  WARNING: missing {game_id}")
                continue
            for state in STATES:
                mean_chars, n_orders = extract_reasoning_lengths(game_dir, state)
                rows.append({
                    "game_id": game_id,
                    "condition": cond,
                    "state": state,
                    "mean_reasoning_chars": round(mean_chars, 1),
                    "n_orders": n_orders,
                })

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["game_id", "condition", "state",
                                               "mean_reasoning_chars", "n_orders"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT}")
    print(f"  Games: {len(rows) // 7}")
    print(f"  Conditions: {len(CLEAN_DATASET)}")


if __name__ == "__main__":
    main()
