# ADR-001: Paper Claim Verification (v0.4 Dataset)

**Date:** 2026-05-13
**Status:** Resolved (all issues fixed in main.tex)
**Dataset:** N=41 clean single-campaign (11 control, 10 yarrow, 10 tarot, 10 scrambled)

## Context

Systematic verification of every quantitative claim in `paper/main.tex` against the data files in `data/`. Where summary data was insufficient, raw game data in the sibling `warringstates-engine` repo was consulted.

---

## Verified Correct

All claims below were reproduced exactly (within rounding) from the data.

### Winner Distributions (Table 4)
- Control: Yan 7, Zhao 2, Qin 1, Chu 1 — matches
- Yarrow: Yan 4, Chu 4, Qi 1, Draw 1, Qin 0 — matches
- Tarot: Qin 5, Yan 3, Qi 1, Zhao 1 — matches
- Scrambled: Qi 5, Qin 1, Yan 1, Zhao 1, Wei 1, Draw 1 — matches
- Han never wins — confirmed (0/41)

### Fisher's Exact Tests
| Test | Computed p | Paper p | Match |
|------|-----------|---------|-------|
| Tarot Qin vs pooled others | 0.0055 | 0.006 | Yes (rounding) |
| Scrambled Qi vs pooled others | 0.0055 | 0.006 | Yes (rounding) |
| Yarrow Qin (0/10) vs Tarot (5/10) | 0.0325 | 0.033 | Yes |
| Oracle pooled vs control survival | 1.0000 | 1.0 | Yes |

### Peak Supply Centers
| Condition | Computed mean | Paper mean | Range match |
|-----------|--------------|------------|-------------|
| Control | 2.45 | 2.45 | 2-4 yes |
| Yarrow | 2.30 | 2.30 | 2-3 yes |
| Tarot | 3.00 | 3.00 | 2-4 yes |
| Scrambled | 2.10 | 2.10 | 2-3 yes |

- KW p = 0.0103 (paper: 0.010) — matches
- Tarot vs scrambled MWU p = 0.0026 (paper: 0.003) — matches
- Tarot vs yarrow MWU p = 0.0216 (paper: 0.022) — matches
- Tarot vs control MWU p = 0.0712 (paper: 0.071) — matches

### Behavioral Profiles (Table 3)
All 16 cells (4 conditions x 4 action types) verified from `han_orders.csv` pooled rates.

### Pressure Invariance (Table 6)
All 20 cells verified using `pressure_pos` column (stable = SCs >= 2, losing = SCs < 2) and defensive = hold + self_support.

### Late-Game Support (Table 5)
All 12 cells verified.

### Han Reasoning Lengths
- Per-game means: control 309, yarrow 449, tarot 456, scrambled 633 — all match
- KW p = 0.0071 (paper: 0.007) — matches
- Note: paper uses mean-of-per-game-means, not pooled mean. Pooled means differ (284/465/426/616). Aggregation method not stated in paper.

### Non-Han Reasoning Elevation
- Order-weighted means: control 146, yarrow 142, tarot 152, scrambled 197 — all match
- KW p = 0.0477 (paper: 0.048) — matches
- Pairwise MWU: scrambled vs yarrow 0.0091 (0.009), scrambled vs tarot 0.0140 (0.014), scrambled vs control 0.0980 (0.098) — all match

### Tarot-Specific
- Tarot chi-squared p = 0.6750 — verified (correct 10-game dataset)
- Tarot card reference rate 81.6% — verified from raw reasoning text
- 58% of 78 Tarot cards have defensive postures — verified (hold 18 + retreat 10 + observe 17 = 45/78 = 57.7%, rounds to 58%)

---

## Issues Found

### CRITICAL: Stale Hexagram Statistics (wrong dataset)

Three Section 4.3 claims were computed from an obsolete 7-game yarrow dataset, not the current N=10 clean dataset:

| Claim | Paper value (7-game) | Correct value (10-game) | Line |
|-------|---------------------|------------------------|------|
| Hexagram chi-squared p | 0.7499 | ~0.80 (4-cat) or ~0.80 (6-cat) | 184 |
| Fisher OR advance vs non-advance | 0.94, p=1.0 | 0.87, p=0.73 | 184 |
| Hexagram reference rate | 70.2% | ~83.3% | 184 |

**Root cause:** `warringstates-engine/scripts/hexagram_action_correlation.py` was never updated when the yarrow game list changed from 7 to 10 games.

**Impact:** The qualitative conclusion (content-action independence) is unchanged — all p-values remain well above 0.05. But the specific numbers in the paper are wrong.

**Action required:** Rerun hexagram analysis with the correct 10-game clean dataset and update lines 41, 184 in `main.tex`.

### ERROR: Han Survival "All Pairwise p=1.0" Overclaimed

Line 295 claims "All pairwise Fisher exact tests return p = 1.0" but two of six pairs do not:
- Control (4/11) vs yarrow (5/10): p = 0.670
- Yarrow (5/10) vs tarot (3/10): p = 0.650

The other four pairs are exactly p = 1.0. The pooled oracle vs control test is exactly p = 1.0 as claimed.

**Impact:** Substantive conclusion unchanged (all pairs thoroughly non-significant). But the claim is technically incorrect.

**Action required:** Change to "All pairwise Fisher exact tests are non-significant (all p >= 0.65)" or similar.

### ERROR: "Deterministic" Overstates Finding

Lines 39 and 399 describe "deterministic, framework-specific winner-ecosystem signature." Winner distributions are probabilistic (e.g., Tarot produces Qin wins 5/10, not 10/10).

**Action required:** Replace "deterministic" with "robust" or "distinctive."

### ERROR: Bonferroni vs Holm-Bonferroni Inconsistency

- Methods (line 137): "Holm-Bonferroni adjusted p-values"
- Results (line 226), Limitations (line 370), Conclusion (line 403): "Bonferroni correction"

p = 0.006 survives both (Bonferroni threshold at 6 comparisons = 0.0083), but the paper should be internally consistent.

### ERROR: "6-Comparison Pairwise Level" Mislabeled

Line 226 says "6-comparison pairwise level" but the tests are each-condition-vs-pooled-others (4 tests), not pairwise between conditions (C(4,2) = 6). The correction still holds either way (0.006 < 0.05/6 = 0.0083 and 0.006 < 0.05/4 = 0.0125).

### ERROR: Methods Promise Unreported Statistics

Line 137 mentions "Cliff's delta effect sizes" and "Wilson confidence intervals" but neither appears anywhere in results. Remove from methods or add to results.

### ERROR: Supply Center Count Unclear

Line 72: "28 supply centers (19 state home SCs + 9 neutral)" and "Each player begins with 2 units and 2 home supply centers." But 7 states x 2 = 14, not 19. If some states have more home SCs than starting units, the distinction needs clarification.

### ERROR: Non-Han Reasoning Aggregation Mislabeled

Line 288: "Per-game pooling across non-Han states" but the numbers (146, 142, 152, 197) match order-weighted averages, not per-game means.

---

## Consistency Issues

| Issue | Location | Detail |
|-------|----------|--------|
| tarot/Tarot capitalization | Throughout | Mixed case; lowercase at lines 179, 214, 283, 288, 295, 337, 339, 343, 370 |
| Hexagram reference precision | Lines 41 vs 184 | "70%" vs "70.2%" for same statistic |
| Chi-squared p precision | Abstract vs Results | 2-decimal (0.75) vs 4-decimal (0.7499); methods says "exact p-values throughout" |
| Pooled vs per-game rates | Lines 149 vs 173 | Table 3 pooled (44.3%) vs MWU per-game (43.2%) without labeling |

---

## Copy-Editing Issues

| Issue | Line | Detail |
|-------|------|--------|
| Table 3 extra column spec | 160 | `{lccccc}` (6 cols) but table has 5; should be `{lcccc}` |
| Table 7 never referenced | 297 | `\label{tab:local}` exists but `\ref{tab:local}` never used |
| "No longer monotonic" | 288 | Implies prior state; should be "is not monotonic" |
| Section title mismatch | 329 | "Four Frameworks, Four Mechanisms" but only 3 get paragraphs |
| Prompt-length limitation | 374 | Conflates prompt input length with reasoning output length |
| Parenthetical ambiguity | 54 | "(longer reasoning, worse outcomes)" could imply Tarot has longest reasoning |
| Sentence fragment | 129 | "If from *structure*" missing "effects derive" |
| Victory condition ambiguous | 72 | "the most supply centers" — plurality or majority? |

---

## Data Sufficiency Notes

- The hexagram theme classification dictionary exists only in `warringstates-engine/scripts/hexagram_action_correlation.py`, not in this repo. Consider extracting it to `data/` for reproducibility.
- Reasoning text reference rates (70.2% hexagram, 81.6% tarot) require raw game JSON files, not reproducible from summary CSVs alone.
- `han_orders.csv` uses a 4-category action scheme (hold/move/self_support/other_support); the original chi-squared tests used a 6-category scheme. The 4-category scheme produces similar but not identical chi-squared values.
