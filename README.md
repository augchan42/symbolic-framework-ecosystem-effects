# Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings

Augustin Chan · `aug@iterative.day` · June 2026 (v2)

## Summary

Large language models exhibit a risk-averse "turtle" bias when deployed as strategic
agents. We inject symbolic reasoning frameworks (I-Ching yarrow divination, Tarot, and
a scrambled-text control) as per-round reflective prompts into **one** agent in a
7-player Warring States Diplomacy variant and measure ecosystem-level outcomes across
**61 games / 6 conditions** with single-campaign memory accumulation.

Framework choice reshapes the winner distribution (permutation omnibus *p* ≈ 0.001 over
the four primary conditions), producing condition-associated signatures: control → Yan
(7/11), I-Ching yarrow → Yan/Chu co-dominance with Qin fully suppressed (0/10), Tarot →
Qin (5/10), scrambled → Qi (5/10). The framework-receiving agent (Han) never wins and
shows no survival difference (Fisher *p* = 1.0).

**v2 core result — the modulation is emergent, not per-decision.** A memory-free
decision-isolation probe (960 calls) shows the reflective process does not change the
receiving agent's risk posture in isolation (hold-rate Friedman *p* = 0.45; the I-Ching
changes no decisions, *p* = 0.60; Tarot perturbs move content but not risk, *p* = 0.021).
A depth-matched follow-up shows the rival-expansion pathway behind Qin suppression is
governed by campaign memory depth, not the oracle (logistic condition *p* = 0.55). The
effects require memory accumulation and the multi-agent interaction — situating the
result in the 2026 memory-dominance literature. A 2×2 factorial separating yarrow's
decision-time and learning-time components reveals a non-additive stalemate interaction
(each component alone freezes the board 50–60% of games; combined, 0%; *p* = 0.004).

Companion (Paper 1) to: [Statistical Properties of the King Wen Sequence](https://doi.org/10.5281/zenodo.14679537) (Chan, 2026).

## Paper

- [LaTeX source](paper/main.tex) · [References](paper/references.bib)

## Reproducing results

```bash
pip install -r requirements.txt
python scripts/reproduce_all.py        # all figures + tables from data/
```

Every figure and statistical test reads from the committed summary CSVs in `data/`; no
engine checkout is needed to reproduce them. The `scripts/extract_*.py` scripts
(re)generate those CSVs from a local `warringstates-engine` checkout (set
`WARRINGSTATES_ENGINE` if it is not a sibling directory).

## Data

- `data/game_outcomes.csv` — per-game outcomes for the 41 core games (condition, winner, Han survival, peak SCs)
- `data/factorial_outcomes.csv` — the 20 factorial games (winner, terminal reason, stalemate flag)
- `data/reasoning_lengths.csv` — per-game, per-state mean reasoning character counts
- `data/han_orders.csv` — per-order Han action data
- `data/oracle_casts.csv` — per-round oracle cast data
- `data/decision_probes_summary.csv` — §4.3 memory-free decision-isolation probe (960 rows)
- `data/breach_depth.csv` — §4.5 per-game Chu→Qin home-breach vs campaign position

## Game engine

The Warring States game engine and full game archives are at
[warringstates-engine](https://github.com/augchan42/warringstates-engine). This repo
contains only the summarized data and analysis needed to reproduce the paper.

## Citation

```bibtex
@article{Chan2026symbolic,
  title={Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings},
  author={Augustin Chan},
  year={2026},
  note={arXiv:2606.07552}
}
```

## License

- Paper: CC BY 4.0
- Code: MIT
