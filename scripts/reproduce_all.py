#!/usr/bin/env python3
"""Reproduce all figures and tables from the paper.

Run from repo root:
    python scripts/reproduce_all.py

Outputs figures to paper/figures/ and prints tables to stdout.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "scripts/table_local_outcomes.py",
    "scripts/table_ecosystem_outcomes.py",
    "scripts/table_pressure_invariance.py",
    "scripts/table_content_independence.py",
    "scripts/figure_peak_scs.py",
    "scripts/figure_winners.py",
    "scripts/figure_gradient.py",
    "scripts/figure_factorial.py",
    "scripts/power_analysis.py",
]


def main():
    root = Path(__file__).resolve().parent.parent
    figures_dir = root / "paper" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    failed = []
    for script in SCRIPTS:
        path = root / script
        if not path.exists():
            print(f"  SKIP (not yet implemented): {script}")
            continue
        print(f"\n{'='*60}")
        print(f"  Running: {script}")
        print(f"{'='*60}")
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(root),
            capture_output=False,
        )
        if result.returncode != 0:
            failed.append(script)

    print(f"\n{'='*60}")
    if failed:
        print(f"FAILED: {failed}")
        sys.exit(1)
    else:
        print("All scripts completed successfully.")


if __name__ == "__main__":
    main()
