#!/usr/bin/env python3
"""Extract per-game, per-state reasoning lengths from warringstates-engine.

Reads order JSON files from the source game directories and writes
data/reasoning_lengths.csv with one row per (game, state) pair.
"""
import json
import os
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE_ROOT = Path.home() / "projects" / "warringstates-engine"
OUTPUT = ROOT / "data" / "reasoning_lengths.csv"

DATASET = {
    "control": [
        "games/control_opus_20260329_124001_df65",
        "games/control_opus_20260329_165843_aee4",
        "games/control_opus_20260403_125741_8c67",
        "games/control_opus_20260403_125743_cf36",
        "games/control_opus_20260404_101008_523c",
        "games/control_opus_20260404_101008_8291",
        "games/control_opus_20260405_163349_12a6",
        "games/control_opus_20260410_143545_eb4f",
        "games/control_opus_20260410_195001_d6ad",
        "games/macbook/control_opus_20260329_061949_c4e4",
        "games/macbook/control_opus_20260329_074444_c154",
    ],
    "yarrow": [
        "games/random_oracle_opus_20260329_124241_7b69",
        "games/random_oracle_opus_20260329_165843_fdb1",
        "games/random_oracle_opus_20260403_125734_f6d2",
        "games/random_oracle_opus_20260403_125737_c9b7",
        "games/random_oracle_opus_20260404_101008_0154",
        "games/random_oracle_opus_20260404_101008_ea16",
        "games/random_oracle_opus_20260405_163316_81f8",
        "games/random_oracle_opus_20260427_182540_65a1",
        "games/random_oracle_opus_20260503_174137_3c96",
        "games/random_oracle_opus_20260503_212155_c063",
    ],
    "tarot": [
        "games/tarot_opus_20260410_143545_2eba",
        "games/tarot_opus_20260410_195001_0fa6",
        "games/tarot_opus_20260411_113544_eacb",
        "games/tarot_opus_20260411_174138_b51a",
        "games/tarot_opus_20260416_070448_ceea",
        "games/tarot_opus_20260416_084349_35a7",
        "games/tarot_opus_20260417_064826_fbb9",
        "games/tarot_opus_20260417_064827_e0ff",
        "games/tarot_opus_20260417_064828_54d8",
        "games/tarot_opus_20260417_064828_ffa6",
    ],
    "scrambled": [
        "games/scrambled_text_opus_20260423_234641_7c92",
        "games/scrambled_text_opus_20260424_115648_1bfd",
        "games/scrambled_text_opus_20260424_232606_d1ae",
        "games/scrambled_text_opus_20260425_095615_296c",
        "games/scrambled_text_opus_20260425_234105_6338",
        "games/scrambled_text_opus_20260426_071651_9c0b",
        "games/scrambled_text_opus_20260426_141428_207d",
        "games/scrambled_text_opus_20260426_221514_422f",
        "games/scrambled_text_opus_20260427_064006_cb32",
        "games/scrambled_text_opus_20260427_100040_de3f",
    ],
}

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


def game_id_from_path(path_str):
    """Extract the canonical game_id from a path like 'games/macbook/control_...'."""
    basename = os.path.basename(path_str)
    return basename


def main():
    rows = []
    for cond, game_paths in DATASET.items():
        for rel_path in game_paths:
            game_dir = ENGINE_ROOT / rel_path
            game_id = game_id_from_path(rel_path)
            if not game_dir.is_dir():
                print(f"  WARNING: missing {game_dir}")
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
    print(f"  Conditions: {len(DATASET)}")


if __name__ == "__main__":
    main()
