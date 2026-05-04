# Re-Run Checklist: Campaign Consistency Fix

## Problem

Tarot and scrambled conditions were run as proper 10-game campaigns with full memory accumulation across games. Control and yarrow were run in smaller batches across multiple campaigns (memory resets between campaigns), creating a confound in the learning-time intervention.

| Condition | Current State | Campaign | Games Done | Memory Continuity |
|-----------|--------------|----------|------------|-------------------|
| Control | 6 games in primary campaign | `v2_experiment_01` | 6 of 10 | Clean (all 6 sequential) |
| Yarrow | 8 games in primary campaign | `v2_experiment_01_yarrow` | 8 of 10 | Clean (all 8 sequential) |
| Tarot | Complete | `v2_experiment_03_tarot` | 10 of 10 | Clean |
| Scrambled | Complete | `v2_experiment_04_scrambled` | 10 of 10 | Clean |

Games from other campaigns (v2_experiment_02_yan_control, v2_experiment_03_control, v2_smoke_01, etc.) are discarded from the analysis — they had independent memory banks.

## Goal

Resume the existing control and yarrow campaigns to reach 10 games each. Final design: N=40 (10 per cell × 4 conditions).

**Games remaining: 6 total** (4 control + 2 yarrow), ~18-30 hours of compute.

## Prerequisites (on VPS)

```bash
cd ~/projects/warringstates-engine
pip install -e ".[dev,analysis]"

# Rebuild memory DB to ensure all existing reflections are ingested
python3 -m src.orchestrator rebuild-memory --campaign v2_experiment_01
python3 -m src.orchestrator rebuild-memory --campaign v2_experiment_01_yarrow
```

### Verify memory state before resuming

```bash
# Should show 6 games with ~21 insights each
sqlite3 games/experiment.db \
  "SELECT game_id, COUNT(*) FROM memory_bank WHERE campaign_id='v2_experiment_01' GROUP BY game_id;"

# Should show 8 games with ~12-24 insights each
sqlite3 games/experiment.db \
  "SELECT game_id, COUNT(*) FROM memory_bank WHERE campaign_id='v2_experiment_01_yarrow' GROUP BY game_id;"

# Should show 0 pending
python3 -m src.orchestrator pending-reflections v2_experiment_01
python3 -m src.orchestrator pending-reflections v2_experiment_01_yarrow
```

## Execution Order

Run yarrow first (only 2 games), then control (4 games).

### Yarrow: Games 9 and 10

```bash
# Game 9
python3 -m src.orchestrator init --condition random_oracle --model opus --campaign v2_experiment_01_yarrow
# → run game loop (see below)
# → reflect + store-reflections

# Game 10
python3 -m src.orchestrator init --condition random_oracle --model opus --campaign v2_experiment_01_yarrow
# → run game loop
# → reflect + store-reflections
```

### Control: Games 7, 8, 9, 10

```bash
# Game 7
python3 -m src.orchestrator init --condition control --model opus --campaign v2_experiment_01
# → run game loop
# → reflect + store-reflections

# Game 8
python3 -m src.orchestrator init --condition control --model opus --campaign v2_experiment_01
# → run game loop
# → reflect + store-reflections

# Game 9
python3 -m src.orchestrator init --condition control --model opus --campaign v2_experiment_01
# → run game loop
# → reflect + store-reflections

# Game 10
python3 -m src.orchestrator init --condition control --model opus --campaign v2_experiment_01
# → run game loop
# → reflect + store-reflections
```

## Per-Game Loop

```
┌─────────────────────────────────────────────────────────────┐
│  ROUND LOOP (until terminal or round 20)                    │
│                                                             │
│  1. python3 -m src.orchestrator prompts <game_dir>          │
│  2. python3 -m src.orchestrator diplomacy <game_dir> --pass 1│
│     → Launch subagents, save to diplomacy/pass_1/           │
│  3. python3 -m src.orchestrator diplomacy <game_dir> --pass 2│
│     → Launch subagents, save to diplomacy/pass_2/           │
│  4. python3 -m src.orchestrator prompts <game_dir> --with-diplomacy│
│  5. Launch order agents (one per alive state)               │
│     → Save to round_NN/orders/<state>.json                  │
│  6. python3 -m src.orchestrator submit <game_dir>           │
│  7. python3 -m src.orchestrator status <game_dir>           │
│     → If terminal: exit loop                                │
│     → Else: next round                                      │
└─────────────────────────────────────────────────────────────┘
```

## Post-Game Reflection (after EVERY game)

```bash
# Phase 1: Generate reflection prompts
python3 -m src.orchestrator reflect <game_dir>

# Phase 2: Launch subagents to generate reflections
# (Claude Code dispatches agents for each state, saves to reflection/responses/)

# Phase 3: Store reflections in memory bank
python3 -m src.orchestrator store-reflections <game_dir>
```

**Critical**: Reflections MUST be stored before initializing the next game. The memory bank carries learning across games within the campaign.

## Validation After All 6 Games

```bash
# Each campaign should have exactly 10 games
python3 -m src.orchestrator pending-reflections v2_experiment_01
python3 -m src.orchestrator pending-reflections v2_experiment_01_yarrow

# Verify 10 entries per campaign
sqlite3 games/experiment.db \
  "SELECT campaign_id, COUNT(DISTINCT game_id) FROM memory_bank GROUP BY campaign_id;"

# Expected:
#   v2_experiment_01        | 10
#   v2_experiment_01_yarrow | 10
```

Check model consistency in new game_meta.json files:
```bash
for game in games/control_opus_2026050* games/random_oracle_opus_2026050*; do
  echo "$(basename $game): $(jq -r .model $game/game_meta.json)"
done
# All should show: claude-opus-4-6
```

## Updating the Paper Repo

After all 6 games complete, regenerate everything:

```bash
cd ~/projects/symbolic-framework-ecosystem-effects

# Rebuild game_outcomes.csv (include only the 10 games per condition from primary campaigns)
python3 scripts/extract_game_outcomes.py

# Rebuild reasoning_lengths.csv from order files
python3 scripts/extract_reasoning_lengths.py

# Regenerate all figures and tables
python3 scripts/reproduce_all.py

# Recompile paper
cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

**Important**: The extraction scripts must filter to only include games from the four primary campaigns:
- `v2_experiment_01` (control, games 1-10)
- `v2_experiment_01_yarrow` (yarrow, games 1-10)
- `v2_experiment_03_tarot` (tarot, games 1-10)
- `v2_experiment_04_scrambled` (scrambled, games 1-10)

## Notes

- Each game takes ~3-5 hours wall-clock (up to 20 rounds × 7 agents × diplomacy + orders)
- 6 games total: ~18-30 hours of compute
- Games can be paused mid-round (state persists on disk)
- The `--oracle-state han` flag defaults correctly but verify in game_meta.json
- Old scattered campaign games remain on disk but are excluded from analysis
