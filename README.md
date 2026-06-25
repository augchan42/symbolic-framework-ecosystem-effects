# Symbolic Reasoning Frameworks Trigger Memory-Mediated Ecosystem Dynamics in Multi-Agent LLM Systems

[![arXiv](https://img.shields.io/badge/arXiv-2606.07552-b31b1b.svg)](https://arxiv.org/abs/2606.07552)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20338937-blue.svg)](https://doi.org/10.5281/zenodo.20338937)

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

- [arXiv:2606.07552](https://arxiv.org/abs/2606.07552)
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

This repo contains only the summarized data and analysis needed to reproduce the paper.
The game engine and agent orchestration code are available from the author on reasonable
request. Full game archives (diplomatic transcripts and agent prompts) are withheld pending
planned creative works; individual game replays can be viewed online at
[warringstates.day/map](https://warringstates.day/map).

## Citation

```bibtex
@article{Chan2026symbolic,
  title={Symbolic Reasoning Frameworks Trigger Memory-Mediated Ecosystem Dynamics in Multi-Agent LLM Systems},
  author={Augustin Chan},
  year={2026},
  eprint={2606.07552},
  archivePrefix={arXiv},
  primaryClass={cs.MA},
  doi={10.48550/arXiv.2606.07552}
}
```

## License

- Paper: CC BY 4.0
- Code: MIT
