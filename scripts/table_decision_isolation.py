#!/usr/bin/env python3
"""Reproduce the memory-free decision-isolation statistics (§4.3, ADR-019).

Reads data/decision_probes_summary.csv (see scripts/extract_decision_probes.py)
and recomputes the three results reported in the paper:

  H1  Process effect: Jaccard order-divergence (treatment vs control) judged
      against the control-vs-control noise floor, paired Wilcoxon per scenario.
        -> tarot 0.368 (p=0.021), yarrow 0.329 (p=0.60), floor 0.294.
  H2  The paper's DV (risk aversion = hold rate): scenario-level Friedman omnibus
      and per-arm Wilcoxon vs control, plus the predicted tarot>=yarrow>=control
      ordering. -> Friedman p=0.45 (null); ordering does NOT hold.
  Reasoning length: ~+33% under both frameworks, memory-free.

Scenario is the unit of analysis (per-scenario means) to avoid pseudoreplication.

Usage:
  python scripts/table_decision_isolation.py
"""
import csv
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "decision_probes_summary.csv"
CONTROL = "control"


def jaccard_dist(a, b):
    if not a and not b:
        return 0.0
    return 1.0 - len(a & b) / len(a | b)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def load():
    # data[scenario][arm] = list of rows (one per replicate)
    data = defaultdict(lambda: defaultdict(list))
    with open(CSV_PATH, newline="") as f:
        for r in csv.DictReader(f):
            r["replicate"] = int(r["replicate"])
            r["n_orders"] = int(r["n_orders"])
            r["reasoning_len"] = float(r["reasoning_len"]) if r["reasoning_len"] else None
            # Recompute the hold rate from counts at full precision (see extractor).
            r["hold_rate"] = (int(r["hold_n"]) / r["n_orders"]
                              if r["n_orders"] else None)
            r["order_set"] = frozenset(
                s for s in r["order_set"].split(";") if s)
            data[r["scenario_id"]][r["arm"]].append(r)
    for by_arm in data.values():
        for rows in by_arm.values():
            rows.sort(key=lambda r: r["replicate"])
    return data


def main():
    if not CSV_PATH.exists():
        raise SystemExit(
            f"Missing {CSV_PATH.relative_to(ROOT)} — run "
            "scripts/extract_decision_probes.py first.")
    data = load()
    arms = sorted({a for sc in data.values() for a in sc})
    treat = [a for a in arms if a != CONTROL]

    # per-scenario hold means + reasoning means (scenario = unit of analysis)
    sc_hold = {a: {} for a in arms}
    sc_rlen = {a: {} for a in arms}
    recs = []  # per scenario: floor + divergence vs control
    for sid, by_arm in data.items():
        for arm, rows in by_arm.items():
            sc_hold[arm][sid] = mean([r["hold_rate"] for r in rows])
            sc_rlen[arm][sid] = mean([r["reasoning_len"] for r in rows])
        c = by_arm.get(CONTROL, [])
        if len(c) < 2:
            continue
        c_sets = [r["order_set"] for r in c]
        rec = dict(floor=mean([jaccard_dist(a, b)
                               for a, b in combinations(c_sets, 2)]), div={})
        for arm in treat:
            t = [r["order_set"] for r in by_arm.get(arm, [])]
            if t:
                rec["div"][arm] = mean([jaccard_dist(a, b)
                                        for a, b in product(t, c_sets)])
        recs.append(rec)

    print("=== Memory-free decision isolation (§4.3, ADR-019) ===")
    print(f"scenarios: {len(data)} | arms: {arms}\n")

    print("H1 — does the reflective PROCESS change decisions (vs noise floor)?")
    floor = mean([r["floor"] for r in recs])
    print(f"  control<->control noise floor (Jaccard): {floor:.3f}")
    try:
        from scipy.stats import wilcoxon
        for arm in treat:
            pairs = [(r["div"][arm], r["floor"]) for r in recs if arm in r["div"]]
            d = [x for x, _ in pairs]
            fl = [f for _, f in pairs]
            gt = sum(1 for x, f in pairs if x > f)
            p = wilcoxon(d, fl)[1]
            print(f"  {arm:7} divergence {mean(d):.3f}  (> floor {gt}/{len(pairs)})  "
                  f"Wilcoxon p={p:.4f}")
    except ImportError:
        print("  (scipy unavailable — install requirements.txt)")

    print("\nH2 — the paper's DV: risk aversion (hold rate, scenario-mean)")
    for arm in arms:
        print(f"  {arm:7} hold {mean(list(sc_hold[arm].values())):.3f} | "
              f"reasoning {mean(list(sc_rlen[arm].values())):.0f} chars")
    try:
        from scipy.stats import friedmanchisquare, wilcoxon
        common = sorted(set.intersection(*[set(sc_hold[a]) for a in arms]))
        blocks = [[sc_hold[a][s] for s in common] for a in arms]
        print(f"  hold-rate Friedman (n={len(common)}): "
              f"p={friedmanchisquare(*blocks)[1]:.4f}")
        for arm in treat:
            shared = sorted(set(sc_hold[arm]) & set(sc_hold[CONTROL]))
            p = wilcoxon([sc_hold[arm][s] for s in shared],
                         [sc_hold[CONTROL][s] for s in shared])[1]
            print(f"  hold {arm} vs control (Wilcoxon, n={len(shared)}): p={p:.4f}")
        ho, hy, hc = (mean(list(sc_hold[a].values()))
                      for a in ("tarot", "yarrow", CONTROL))
        print(f"  predicted ordering tarot({ho:.3f}) >= yarrow({hy:.3f}) >= "
              f"control({hc:.3f}): {ho >= hy >= hc}")
    except ImportError:
        print("  (scipy unavailable — install requirements.txt)")

    print("\nInterpretation: H1 split (tarot perturbs content, yarrow inert) and "
          "H2 null (Friedman ~0.45)\n  => the frameworks do not modulate risk "
          "posture memory-free; the effect is emergent.")


if __name__ == "__main__":
    main()
