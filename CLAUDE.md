# CLAUDE.md

## Project

Paper repo for "Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings" — a cs.MA/cs.AI paper showing that symbolic reasoning frameworks injected into one LLM agent produce distinct, framework-specific winner distributions in a multi-agent game, without benefiting the recipient.

Companion to the King Wen negative-result paper (king-wen-agi-framework repo, arXiv 2026).

## Commands

```bash
pip install -r requirements.txt
python scripts/reproduce_all.py          # All figures + tables
python scripts/table_local_outcomes.py   # Section 4 tables
python scripts/table_ecosystem_outcomes.py # Section 4 tables + Fisher tests
python scripts/figure_gradient.py        # Reasoning-length figure
python scripts/figure_winners.py         # Winner distribution bars
python scripts/figure_peak_scs.py        # Peak SC boxplot
python scripts/power_analysis.py         # Supplementary power analysis
```

## Architecture

```
paper/          # LaTeX source, figures, references
data/           # Summary CSVs + raw order files (no diplomacy transcripts)
  orders/       # Per-condition per-game orders with reasoning text
scripts/        # One script per figure/table, plus reproduce_all.py
```

## Paper Structure

1. Introduction — ecosystem-signature differentiation as primary claim
2. Related Work — LLM biases, persona effects, multi-agent systems, risk aversion
3. Methods — game, agents, intervention design, conditions, dataset (N=41), statistics
4. Results
   - 4.1 Behavioral Baseline (turtle tendency)
   - 4.2 Framework-Specific Behavioral Modulation (yarrow, tarot, scrambled profiles)
   - 4.3 Content-Action Independence (hexagram χ² p=0.75, tarot χ² p=0.68)
   - 4.4 Ecosystem Signatures (winner distributions, Fisher tests)
   - 4.5 Ecosystem Mechanisms (speed bump, vacuum, stubborn holdout)
   - 4.6 Non-Han Reasoning Elevation
   - 4.7 Han Survival (null across all conditions)
5. Analysis — four mechanisms, reasoning length as negative indicator
6. Discussion — alignment implications, process vs content, risk aversion theory
7. Limitations
8. Future Work
9. Conclusion

## Key Findings (N=41: 11 control, 10 yarrow, 10 tarot, 10 scrambled — clean single-campaign dataset)

- **Ecosystem-signature differentiation**: control→Yan 7/11, yarrow→Yan/Chu co-dominant, tarot→Qin 5/10, scrambled→Qi 5/10
- **Tarot→Qin**: Fisher vs pooled p=0.006 (survives Bonferroni)
- **Scrambled→Qi**: Fisher vs pooled p=0.006 (survives Bonferroni)
- **Qin suppression under yarrow**: 0/10 (Fisher vs tarot p=0.033)
- **Tarot elevates Han peak territory**: KW p=0.010, tarot mean 3.0 vs 2.1–2.5 others
- **Han survival flat**: Fisher p=1.0 across all conditions (control 36%, yarrow 50%, tarot 30%, scrambled 40%)
- **Content-action independence**: hexagram themes χ² p=0.75, Tarot card postures χ² p=0.68
- **Decision-time effects dominate**: Qin suppression present in game-1 (no memory) yarrow games

## Data Source

Raw game data lives in the warringstates-engine repo. This repo contains extracted/summarized data sufficient to reproduce every figure and statistical test in the paper. Full game archives (diplomacy transcripts, agent prompts) are deliberately excluded — they may be used for future creative works.

## Dual-Timescale Intervention

The experimental intervention operates at two timescales:
1. **Decision-time (per-round)**: Agent receives oracle text + MANDATE to interpret before issuing orders. Control receives length-matched generic reflection prompt.
2. **Learning-time (between-game)**: Agent reflects on game through framework lens; insights stored in memory bank and retrieved in future games.

Suggestive evidence from first-in-campaign games (zero memory) indicates decision-time effects are the primary driver.

## Sibling Repos

- `king-wen-agi-framework` — Paper 1: King Wen statistical properties (negative result for neural training)
- `warringstates-engine` — Game engine, full game data, experimental orchestration
- `warringstates-day` — Blog series, state profiles, dispatches
