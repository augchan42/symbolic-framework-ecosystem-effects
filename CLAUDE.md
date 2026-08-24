# CLAUDE.md

## Project

Paper repo for "Symbolic Reasoning Frameworks Trigger Memory-Mediated Ecosystem Dynamics in Multi-Agent LLM Systems" — a cs.MA/cs.AI paper showing that symbolic reasoning frameworks injected into one LLM agent produce distinct, framework-specific winner distributions in a multi-agent game, without benefiting the recipient.

Companion to the King Wen negative-result paper (king-wen-agi-framework repo, arXiv 2026).

## Commands

```bash
pip install -r requirements.txt
python scripts/reproduce_all.py            # All figures + tables
python scripts/table_local_outcomes.py     # Han survival + peak SCs
python scripts/table_ecosystem_outcomes.py # winner distributions + Fisher tests
python scripts/table_pressure_invariance.py # pressure invariance
python scripts/table_content_independence.py # hexagram/tarot × action chi-squared
python scripts/table_decision_isolation.py # §4.3 memory-free decision isolation (ADR-WSE-019)
python scripts/table_breach_depth.py       # §4.5 breach depth-not-condition (ADR-WSE-018)
python scripts/figure_gradient.py          # reasoning-length boxplot
python scripts/figure_winners.py           # winner distribution bars
python scripts/figure_peak_scs.py          # peak SC boxplot
python scripts/figure_factorial.py         # §4.8 factorial winner bars
python scripts/power_analysis.py           # Supplementary power analysis
# Extractors (require a warringstates-engine checkout; CSVs above are committed):
python scripts/extract_han_orders.py       # → han_orders.csv + oracle_casts.csv
python scripts/extract_decision_probes.py  # → decision_probes_summary.csv (960 probes)
python scripts/extract_breach_depth.py     # → breach_depth.csv (per-game Chu breach)
```

## Architecture

```
paper/          # LaTeX source, figures, references
data/           # Summary CSVs (no diplomacy transcripts)
  game_outcomes.csv    # Per-game (N=41 core): winner, Han survival, peak SCs
  factorial_outcomes.csv # Per-game (20 factorial): winner, terminal_reason, stalemate
  reasoning_lengths.csv # Per-game per-state: mean reasoning chars, n_orders
  han_orders.csv       # Per-order: action, phase, pressure, reasoning length
  oracle_casts.csv     # Per-round: hexagram/tarot cast data
  decision_probes_summary.csv # §4.3 memory-free probe: per scenario×arm×replicate
                              #   (order counts + set-serialized orders; 960 rows)
  breach_depth.csv     # §4.5 per-game Chu→Qin home breach × campaign position
scripts/        # One script per figure/table, plus reproduce_all.py
  extract_han_orders.py      # engine → han_orders.csv + oracle_casts.csv
  extract_decision_probes.py # engine → decision_probes_summary.csv
  extract_breach_depth.py    # engine → breach_depth.csv
```

## Paper Structure

1. Introduction — ecosystem-signature differentiation as primary claim
2. Related Work — LLM biases, persona effects, multi-agent systems, risk aversion
3. Methods — game, agents, intervention design, conditions, dataset (N=61: 41 core + 20 factorial), statistics
4. Results
   - 4.1 Behavioral Baseline (turtle tendency)
   - 4.2 Framework-Specific Behavioral Modulation (yarrow, tarot, scrambled profiles)
   - 4.3 Content-Action Independence (hexagram χ² p=0.95, tarot χ² p=0.69) + **memory-free decision isolation** (ADR-WSE-019: process does NOT modulate risk posture, Friedman p=0.45)
   - 4.4 Ecosystem Signatures (winner distributions, permutation omnibus p≈0.001, Fisher tests)
   - 4.5 Ecosystem Mechanisms (rival expansion; **breach is memory-depth-driven not yarrow**, ADR-WSE-018: condition p=0.55)
   - 4.6 Non-Han Reasoning Elevation
   - 4.7 Han Survival (null across all conditions)
   - 4.8 Factorial Decomposition (decision-only vs learning-only; non-additive stalemate interaction p=0.004)
5. Analysis — four mechanisms, reasoning length as negative indicator, non-additive factorial
6. Discussion — alignment implications, **emergent (not per-decision) mechanism**, risk aversion theory
7. Limitations
8. Future Work
9. Conclusion

## Key Findings (N=61: 41 core [11 control, 10 yarrow/tarot/scrambled] + 20 factorial [10 decision-only, 10 learning-only])

- **Ecosystem-signature differentiation**: control→Yan 7/11, yarrow→Yan/Chu co-dominant, tarot→Qin 5/10, scrambled→Qi 5/10; permutation omnibus p≈0.0013 (global heterogeneity)
- **Scrambled→Qi** (robust attractor): pooled p=0.006 AND vs control-alone p=0.012
- **Tarot→Qin** (denominator-dependent): pooled p=0.006 but vs control-alone only p=0.064 — present as suggestive, needs out-of-sample replication
- **Qin suppression under yarrow**: 0/10 (Fisher vs tarot p=0.033)
- **Factorial stalemate interaction** (strongest result): decision-only 5/10 & learning-only 6/10 stalemates, combined yarrow 0/10 — non-additive, Fisher p=0.004
- **Han survival flat**: Fisher p=1.0 across all conditions (control 36%, yarrow 50%, tarot 30%, scrambled 40%)
- **Content-action independence**: hexagram themes χ² p=0.95, Tarot card postures χ² p=0.69
- **MECHANISM IS EMERGENT, NOT PER-DECISION (v2 core reframe)**:
  - Memory-free decision isolation (ADR-WSE-019, 960 probes): reflective process does NOT modulate risk posture (hold-rate Friedman p=0.45); I-Ching changes no decisions (p=0.60); Tarot perturbs move content (p=0.021) but not risk; only reasoning length rises (~+33%, both)
  - Breach mechanism (ADR-WSE-018) is memory-DEPTH-driven, not yarrow: logistic breach~position+condition → position p=0.006, condition p=0.55; breach spans 40–100% across 4 canonical-yarrow campaigns
  - Effects require memory accumulation + 7-agent interaction; situated in the 2026 memory-dominance literature (Memory Curse, etc.)

## Pressure Invariance Methodology (§4.5 Table 6)

- **Defensive** = hold + self_support (4-category action scheme)
- **Pressure definition**: absolute SC position — "losing" = SCs < 2 (below Han's starting position), "stable" = SCs >= 2
- **SC timing**: post-round (orders paired with the same round's resolved outcome, matching the engine's `han_sc_delta` pairing)

## Data Source

Raw game data lives in the warringstates-engine repo. This repo contains extracted/summarized data sufficient to reproduce every figure and statistical test in the paper. Full game archives (diplomacy transcripts, agent prompts) are deliberately excluded — they may be used for future creative works.

## Dual-Timescale Intervention

The experimental intervention operates at two timescales:
1. **Decision-time (per-round)**: Agent receives oracle text + MANDATE to interpret before issuing orders. Control receives length-matched generic reflection prompt.
2. **Learning-time (between-game)**: Agent reflects on game through framework lens; insights stored in memory bank and retrieved in future games.

**v2 update:** the per-decision channel is weak. The memory-free decision-isolation probe (ADR-WSE-019) shows the reflective process does not modulate the receiving agent's risk posture in isolation, and the factorial (§4.8) shows neither timescale alone reproduces the full signature (non-additive). The headline effects are **emergent** — they require campaign memory accumulation and the multi-agent interaction. (The earlier "decision-time primacy" reading from first-in-campaign games is superseded by this controlled test.)

## Sibling Repos

- `king-wen-agi-framework` — Paper 1: King Wen statistical properties (negative result for neural training)
- `warringstates-engine` — Game engine, full game data, experimental orchestration
- `warringstates-day` — Blog series, state profiles, dispatches
