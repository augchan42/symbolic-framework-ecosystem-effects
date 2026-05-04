# Who Wins When One Agent Reflects?

**Pass-Through Effects of Prompt Interventions in Multi-Agent Games**

## Abstract

We inject symbolic reasoning frameworks (I Ching, Tarot, scrambled-text control) into one agent in a 7-player Warring States diplomacy game and measure ecosystem-level outcomes. The intervention does not benefit its recipient (Han survival drops from 64% to 30-40%) but systematically redirects which *other* state wins: yarrow suppresses Qin (0/10, Fisher p=0.033 vs tarot), tarot elevates Qin (5/10), scrambled boosts Qi (6/10, Fisher p=0.040). A perturbativeness gradient in non-Han reasoning length (control 98 < yarrow 126 < tarot 152 < scrambled 197 chars/order, KW p<0.001) provides the mechanism. We name this pattern class **pass-through effects**: interventions that bypass their recipient and land on third parties.

## Paper

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
- `data/reasoning_lengths.csv` — per-order reasoning character counts by state and condition
- `data/orders/` — raw order files with reasoning text per game

## Game Engine

The Warring States game engine is at [warringstates-engine](https://github.com/digital-rain-tech/warringstates-engine). This repo contains only the data and analysis needed to reproduce the paper.

## Citation

```bibtex
@article{Chan2026passthrough,
  title={Who Wins When One Agent Reflects? Pass-Through Effects of Prompt Interventions in Multi-Agent Games},
  author={Augustin Chan},
  year={2026}
}
```

## License

- Paper: CC BY 4.0
- Code: MIT
