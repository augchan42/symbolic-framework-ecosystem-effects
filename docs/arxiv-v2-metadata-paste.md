# arXiv v2 Replace — Metadata (copy-paste)

Replacement of **arXiv:2606.07552**. Three fields change from v1: **Title**, **Abstract**, **Comments**.
Categories are locked for a replace (primary cs.MA; cross-list cs.AI, cs.LG) — not editable on the metadata screen.

---

## ① Title — REPLACE

```
Symbolic Reasoning Frameworks Trigger Memory-Mediated Ecosystem Dynamics in Multi-Agent LLM Systems
```

## ② Author(s) — keep

```
Augustin Chan
```

## ③ Abstract — REPLACE (verbatim; ASCII, no math mode)

> Condensed to **1,901 chars** to fit arXiv's 1,920-char metadata limit. The PDF's full abstract (in `paper/main.tex`) is unchanged — arXiv only caps the *metadata* field, not the paper.

```
Large language models exhibit a risk-averse "turtle" bias as strategic agents. We show that injecting a symbolic reasoning framework as a per-round reflective prompt into one agent acts as a small perturbation whose consequences are not per-decision but emergent: the agent's risk posture is unchanged in isolation, yet over a campaign of accumulating memory and multi-agent interaction the conditions settle into distinct, condition-associated winner ecosystems. In a 7-player Warring States Diplomacy variant (61 games, 6 conditions), the winner distribution differs sharply across the four primary conditions (permutation omnibus p approximately 0.001): control -> Yan (7/11); I-Ching yarrow -> Yan/Chu co-dominance with Qin fully suppressed (0/10); Tarot -> Qin (5/10); scrambled-text ablation -> Qi (5/10). The scrambled->Qi attractor is robust (vs. pooled and control alone, p = 0.006 and 0.012); tarot->Qin is denominator-dependent (0.006 pooled, 0.064 vs. control). Han never wins and shows no survival difference (Fisher p = 1.0); neither framework's content predicts actions (chi-squared p = 0.95 hexagram, 0.69 Tarot). A memory-free decision-isolation probe (960 calls) shows the process does not change the agent's risk posture in isolation (Friedman p = 0.45; I-Ching p = 0.60; Tarot perturbs move content but not risk, p = 0.021). A 2x2 factorial separating yarrow's decision-time and learning-time components reveals a non-additive interaction: each alone freezes the board (50-60% stalemates), combined they produce zero (permutation p ~ 5e-5). Testing relocates Qin suppression to rival (Chu) expansion governed by campaign memory depth, not the oracle (p = 0.55). We present this as an observation paper: agent-level framework choice produces distinctive, non-additive system-level consequences, transmitted through emergent memory and multi-agent dynamics, not per-decision effects.
```

## ④ Comments — REPLACE (counts changed: 17→28 pages, etc.)

```
28 pages, 4 figures, 9 tables, 6 listings. Code and data: https://doi.org/10.5281/zenodo.20338937
```

## ⑤ Report number — leave blank
## ⑥ Journal reference — leave blank
## ⑦ External DOI — leave blank

## ⑧ ACM class — keep

```
I.2.11
```

## ⑨ MSC class — leave blank

---

**After pasting:** continue to Preview and confirm the rendered PDF is the 28-page v2 before Process. Upload artifact is `arxiv-submission.tar` (repo root).
