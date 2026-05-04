# CLAUDE.md

## Project

Paper repo for "Who Wins When One Agent Reflects? Pass-Through Effects of Prompt Interventions in Multi-Agent Games" — a cs.AI paper showing that symbolic reasoning frameworks injected into one LLM agent redirect which *other* agent wins in a multi-agent game, without benefiting the recipient.

Companion to the King Wen negative-result paper (king-wen-agi-framework repo, arXiv 2026).

## Commands

```bash
pip install -r requirements.txt
python scripts/reproduce_all.py          # All figures + tables
python scripts/table_local_outcomes.py   # Section 3 tables
python scripts/table_ecosystem_outcomes.py # Section 4 tables + Fisher tests
python scripts/figure_gradient.py        # Section 5 reasoning-length figure
python scripts/figure_winners.py         # Section 4 winner distribution bars
python scripts/figure_peak_scs.py        # Section 3 peak SC boxplot
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

1. Introduction — lead with the punchline, cite paper 1
2. Experimental Setup — game, agents, dual-timescale intervention, 4 conditions, metrics
   - 2.1 Environment & Agents
   - 2.2 Intervention Design (decision-time + learning-time)
   - 2.3 Conditions & Controls
   - 2.4 Metrics (local vs system)
3. Results I — No Local Benefit (Han survival, peak SCs)
4. Results II — Ecosystem Redirection (winner distributions, Fisher tests)
5. Results III — Perturbativeness Gradient (reasoning-length dose-response)
6. Synthesis — Pass-Through Effects (define the pattern class, connect sections 3-5)
7. Discussion (alignment implications, generalizability)
8. Limitations (single game, prompt class, n=10)
9. Conclusion

## Key Findings (N=41: 11 control, 10 yarrow, 10 tarot, 10 scrambled)

- **Tarot elevates Han peak territory**: 4-way KW p=0.008, MWU tarot > others p<0.002
- **Qin suppression under yarrow**: 0/10 (Fisher vs tarot p=0.033)
- **Qi dominance under scrambled**: 6/10 (Fisher vs others p=0.040)
- **Perturbativeness gradient**: control 98 < yarrow 126 < tarot 152 < scrambled 197 chars/order (KW p<0.001)
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
