# Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings

[![arXiv](https://img.shields.io/badge/arXiv-2606.07552-b31b1b.svg)](https://arxiv.org/abs/2606.07552)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20338937-blue.svg)](https://doi.org/10.5281/zenodo.20338937)

## Abstract

Large language models exhibit innate behavioral tendencies when deployed as strategic agents — notably a risk-averse "turtle" bias toward defensive play. We show that symbolic reasoning frameworks, injected as per-round reflective prompts into one agent, differentially modulate this bias and reshape the multi-agent ecosystem to produce framework-specific winner distributions. In a 7-player Warring States Diplomacy variant (41 games, 4 conditions, single-campaign memory accumulation), each framework produces a distinct ecosystem signature: under control, Yan dominates (7/11, 64%); under I-Ching yarrow divination, Yan and Chu co-dominate while Qin is completely suppressed (0/10); under Tarot, Qin dominates (5/10, Fisher vs. pooled p = 0.006); under scrambled-text ablation (incoherent oracle text preserving prompt structure), Qi dominates (5/10, Fisher vs. pooled p = 0.006). The framework-receiving agent (Han) never wins and shows no survival difference across conditions (Fisher p = 1.0), but Tarot consistently elevates Han's peak territory (mean 3.0 SCs vs. 2.1–2.5 others, Kruskal-Wallis p = 0.010). Neither framework's content predicts subsequent actions — hexagram themes (chi-squared p = 0.95) and Tarot card postures (chi-squared p = 0.69) are both independent of action choice — suggesting the modulation operates through the reflective process, not content-following. We present this as an observation paper establishing that alignment-framework choice at the agent level produces distinctive system-level consequences in multi-agent settings.

## Paper

- [arXiv:2606.07552](https://arxiv.org/abs/2606.07552)
- [LaTeX source](paper/main.tex)
- [References](paper/references.bib)

Companion to: [Statistical Properties of the King Wen Sequence](https://doi.org/10.5281/zenodo.14679537) (Chan, 2026)

## Reproducing Results

```bash
pip install -r requirements.txt
python scripts/reproduce_all.py
```

Generates all figures and tables from `data/`.

## Data

- `data/game_outcomes.csv` — per-game outcomes (condition, winner, Han survival, peak SCs)
- `data/reasoning_lengths.csv` — per-game, per-state mean reasoning character counts
- `data/han_orders.csv` — per-order Han action data (984 orders across 41 games)
- `data/oracle_casts.csv` — per-round oracle cast data (284 casts)

## Game Engine

The Warring States game engine is at [warringstates-engine](https://github.com/digital-rain-tech/warringstates-engine). This repo contains only the data and analysis needed to reproduce the paper.

## Citation

```bibtex
@article{Chan2026symbolic,
  title={Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings},
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
