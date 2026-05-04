# Re-Run Checklist: Campaign Consistency Fix

## Problem

Tarot and scrambled conditions were run as proper 10-game campaigns with full memory accumulation across games. Control and yarrow were run in smaller batches across multiple campaigns (memory resets between campaigns), creating a confound in the learning-time intervention.

| Condition | Current State | Campaigns Used | Memory Continuity |
|-----------|--------------|----------------|-------------------|
| Control | 11 games across 4 campaigns (6+1+2+2) | v2_experiment_01, _02_yan_control, _03_control, v2_smoke_01 | Broken |
| Yarrow | 10 games across 3 campaigns (8+1+1) | v2_experiment_01_yarrow, _02_yan_yarrow, _02_yarrow | Broken |
| Tarot | 10 games in 1 campaign | v2_experiment_03_tarot | Clean |
| Scrambled | 10 games in 1 campaign | v2_experiment_04_scrambled | Clean |

## Goal

Re-run control (10 games) and yarrow (10 games) as single 10-game campaigns with unbroken memory accumulation. Final design: N=40 (10 per cell × 4 conditions).

The v2_smoke_01 control game is discarded — it was a smoke test, not part of the experimental design.

## Prerequisites

```bash
cd ~/projects/warringstates-engine
pip install -e ".[dev,analysis]"
```

Ensure the memory DB path is correct (games/vps/experiment_*.db or a fresh DB for the new campaigns).

## Steps Per Campaign

### 1. Initialize Campaign

```bash
# Control (10 games)
python3 -m src.orchestrator init \
  --condition control \
  --model opus \
  --campaign v3_experiment_control

# Yarrow (10 games)
python3 -m src.orchestrator init \
  --condition random_oracle \
  --model opus \
  --campaign v3_experiment_yarrow
```

### 2. Run Each Game (repeat 10× per campaign)

For each game in the campaign, the loop is:

```
┌─────────────────────────────────────────────┐
│  ROUND LOOP (until terminal or round 20)    │
│                                             │
│  1. Generate prompts                        │
│     python3 -m src.orchestrator prompts <game_dir>           │
│                                             │
│  2. Diplomacy pass 1                        │
│     python3 -m src.orchestrator diplomacy <game_dir> --pass 1│
│     → Launch subagents for each alive state │
│     → Save responses to diplomacy/pass_1/   │
│                                             │
│  3. Diplomacy pass 2                        │
│     python3 -m src.orchestrator diplomacy <game_dir> --pass 2│
│     → Launch subagents                      │
│     → Save responses to diplomacy/pass_2/   │
│                                             │
│  4. Regenerate prompts with diplomacy inbox │
│     python3 -m src.orchestrator prompts <game_dir> --with-diplomacy│
│                                             │
│  5. Launch order agents (one per alive state)│
│     → Save to round_NN/orders/<state>.json  │
│                                             │
│  6. Submit and resolve                      │
│     python3 -m src.orchestrator submit <game_dir>            │
│                                             │
│  7. Check status                            │
│     python3 -m src.orchestrator status <game_dir>            │
│     → If terminal: exit loop                │
│     → Else: next round                      │
└─────────────────────────────────────────────┘
```

### 3. Post-Game Reflection (after each game completes)

```bash
# Phase 1: Generate reflection prompts
python3 -m src.orchestrator reflect <game_dir>

# Phase 2: Launch subagents to generate reflections
# (Claude Code dispatches agents for each state, saves to reflection/responses/)

# Phase 3: Store reflections in memory bank
python3 -m src.orchestrator store-reflections <game_dir>
```

**Critical**: Reflections MUST be stored before initializing the next game in the campaign. The memory bank is what carries learning across games.

### 4. Initialize Next Game in Same Campaign

```bash
python3 -m src.orchestrator init \
  --condition <same_condition> \
  --model opus \
  --campaign <same_campaign_id>
```

Then repeat from step 2.

### 5. After All 10 Games Complete

```bash
# Verify campaign completeness
python3 -m src.orchestrator pending-reflections <campaign_id>
# Should show 0 pending

# Verify memory bank has entries for all 10 games
sqlite3 games/vps/<db_file>.db \
  "SELECT game_id, COUNT(*) FROM memory_bank WHERE campaign_id='<campaign_id>' GROUP BY game_id;"
```

## Validation After Re-Run

1. **Campaign integrity**: Each campaign has exactly 10 games with sequential memory accumulation
2. **Model consistency**: All games use `claude-opus-4-6`
3. **Reflection completeness**: Every game has stored reflections (check `reflection/responses/` in each game dir)
4. **No cross-contamination**: New campaigns use fresh campaign IDs; old campaigns remain archived

## Updating the Paper Repo

After re-running, regenerate the summary data:

```bash
cd ~/projects/symbolic-framework-ecosystem-effects

# Rebuild game_outcomes.csv from new game_meta.json files
python3 scripts/extract_game_outcomes.py  # (may need to create/update)

# Rebuild reasoning_lengths.csv from new order files
python3 scripts/extract_reasoning_lengths.py

# Regenerate all figures and tables
python3 scripts/reproduce_all.py
```

Then recompile the paper:
```bash
cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## What to Archive

Keep old campaign data in place — do NOT delete. The old games are valid individual observations; the issue was only campaign structure (memory continuity). Tag the old data:

```bash
# In warringstates-engine
git tag v2-pre-rerun-archive
```

## Notes

- Each game takes ~3-5 hours wall-clock (20 rounds × 7 agents × diplomacy + orders)
- Full re-run (20 games): ~60-100 hours of compute
- Games can be paused mid-campaign (memory bank persists in SQLite)
- The `--oracle-state han` flag defaults correctly but verify in game_meta.json
