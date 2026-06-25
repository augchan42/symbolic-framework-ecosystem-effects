# ADR-003: arXiv Submission Metadata

**Status:** v1 published (arXiv:2606.07552, 2026-05); v2 replacement metadata prepared below — not yet uploaded
**Date:** 2026-05-22 (v1); updated 2026-06-25 (v2)
**Author:** Augustin Chan

> **v2 is a replacement of arXiv:2606.07552**, not a new submission. The live paper's primary is now **cs.MA**: it was submitted as cs.LG (the only endorsed primary, via the king-wen paper) and arXiv moderators reclassified it to cs.MA a few weeks after posting. A replacement keeps that current classification — do not try to set the primary back to cs.LG. The fields below are updated to the v2 (N=61 emergent-reframe) content; paste these at upload time. The v1 values are preserved in the Notes section for history.

## Submission Details

- **arXiv ID:** 2606.07552 ([abs](https://arxiv.org/abs/2606.07552))
- **arXiv DOI:** 10.48550/arXiv.2606.07552
- **Primary category:** cs.MA — Multiagent Systems (live; moderators reclassified from the cs.LG submission ~weeks after v1 posted; a replacement cannot change it)
- **Cross-list:** cs.AI, cs.LG (verified live on arxiv.org/abs/2606.07552, 2026-06-25; cs.LG became a cross-list after the primary moved to cs.MA)
- **License:** CC BY 4.0
- **Zenodo DOI:** 10.5281/zenodo.20338937 (v1 release) — **cut a v2 version release and update this DOI before upload if you want v2 data attached**

> Note: submitted endorsed for cs.LG (from the king-wen paper); arXiv classified the published version with cs.MA as primary and cs.LG/cs.AI as cross-lists.

## Metadata Fields

**Title:**
Symbolic Reasoning Frameworks Trigger Memory-Mediated Ecosystem Dynamics in Multi-Agent LLM Systems

**Author(s):**
Augustin Chan

**Abstract:** *(v2, pure ASCII — verified against `paper/main.tex`)*
Large language models exhibit innate behavioral tendencies when deployed as strategic agents - notably a risk-averse "turtle" bias toward defensive play. We show that injecting a symbolic reasoning framework as a per-round reflective prompt into a single agent acts as a small cognitive perturbation whose consequences are not per-decision but emergent: the receiving agent's risk posture is unchanged in isolation, yet over a full campaign of accumulating memory and multi-agent interaction the conditions settle into different, condition-associated winner ecosystems - an effect we attribute to emergent memory and multi-agent dynamics rather than the framework's per-decision influence. In a 7-player Warring States Diplomacy variant (61 games, 6 conditions, single-campaign memory accumulation), the winner distribution differs sharply across the four primary conditions (Monte-Carlo permutation omnibus p approximately 0.001), forming condition-associated ecosystem signatures: under control, Yan dominates (7/11, 64%); under I-Ching yarrow divination, Yan and Chu co-dominate while Qin is completely suppressed (0/10); under Tarot, Qin dominates (5/10); under scrambled-text ablation (English commentary word-shuffled; hexagram name and Chinese judgment retained), Qi dominates (5/10). The scrambled-to-Qi attractor is the most robust (significant against both a pooled denominator and control alone, p = 0.006 and 0.012); the tarot-to-Qin attractor is significant only against the pooled denominator (p = 0.006, vs. control alone p = 0.064). The framework-receiving agent (Han) never wins and shows no survival difference across conditions (Fisher p = 1.0), but Tarot consistently elevates Han's peak territory (mean 3.0 SCs vs. 2.1-2.5 others, Kruskal-Wallis p = 0.010). Neither framework's content predicts subsequent actions - hexagram themes (chi-squared p = 0.95) and Tarot card postures (chi-squared p = 0.69) are both independent of action choice. A memory-free decision-isolation probe (960 calls) further shows the modulation is emergent rather than per-decision: stripped of memory and multi-agent context the reflective process does not change the receiving agent's risk posture (hold-rate Friedman p = 0.45; the I-Ching changes no decisions beyond temperature noise, p = 0.60; Tarot perturbs move content but not risk posture, p = 0.021), locating the effect in memory accumulation and multi-agent dynamics rather than per-decision processing. A 2x2 factorial decomposition separating yarrow's decision-time (per-round oracle) and learning-time (between-game I-Ching reflection) components reveals a non-additive interaction: each component individually freezes the board (50-60% stalemate rate, Fisher p = 0.012 and 0.004 vs. control), but combined they produce zero stalemates (negative interaction, permutation p approximately 5e-5). Direct testing relocates yarrow's Qin suppression from the framework-receiving agent's own cooperation to rival (Chu) expansion through a map corridor; a depth-matched follow-up then shows that expansion is governed by campaign memory depth, not the oracle (condition p = 0.55), so even this pathway is emergent rather than framework-specific. We present this as an observation paper establishing that alignment-framework choice at the agent level produces distinctive, non-additive system-level consequences in multi-agent settings, transmitted through emergent multi-agent and memory dynamics rather than the framework's per-decision effect on the receiving agent.

**Comments:**
28 pages, 4 figures, 9 tables, 6 listings. Code and data: https://doi.org/10.5281/zenodo.20338937
*(update the DOI here if a v2 Zenodo version is cut)*

> **v2 retitle note:** the title changed from "Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings" (v1) to "Symbolic Reasoning Frameworks Trigger Memory-Mediated Ecosystem Dynamics in Multi-Agent LLM Systems" (v2). Rationale: v2's decision-isolation controls show the effect is emergent, not a per-decision modulation of the receiving agent's risk posture, so the v1 title overclaimed. The new title names the paper's actual mechanism — the symbolic framework is a small perturbation and the ecosystem reorganization is the phenomenon, with the amplification supplied by **emergent memory and multi-agent dynamics** (the paper does not isolate which of those two channels carries the effect) — in intervention → mechanism → phenomenon order. Design choices for durability: "Trigger" (not "Produce") connotes a small initiator rather than the framework doing the heavy lifting; "Dynamics" (not "Signatures") avoids implying a stable reproducible per-condition pattern, keeping it resistant to the planned Paper-3 campaign-variance correction (40-100% breach-rate spread across nominally identical campaigns); and "memory-mediated" is *reinforced* by the planned work (Paper-3's breach result is itself memory-depth-driven), so it is the most future-proof element rather than a liability. The cross-cultural-following result (ADR-020) is likewise untouched, since the title makes no oracle/direction/content-following claim. Consider noting the retitle briefly in the replacement's Comments so readers/citers see why it moved (the arXiv ID is unchanged).

**Report number:** *(blank)*

**Journal reference:** *(blank)*

**External DOI:** *(blank)*

**ACM class:** I.2.11

**MSC class:** *(blank)*

## Notes

- Endorsed for cs.LG from king-wen paper (arXiv 2026-04-10)
- Not endorsed for cs.MA or cs.AI as primary categories
- ACM I.2.11 = Distributed Artificial Intelligence — Multiagent systems
- Companion paper: king-wen-agi-framework (Zenodo 10.5281/zenodo.14679537)
- **v1 history (superseded):** v1 was N=41 / 4 conditions, Comments "17 pages, 3 figures, 6 tables, 6 listings", and its abstract described "each framework produces a distinct ecosystem signature" without the emergent/factorial/decision-isolation results. v2 (above) is N=61 (41 core + 20 factorial), reframed around the emergent mechanism. Note the v1 references contained 17 hallucinated author names (corrected on `paper-v2`, commit 75bbd61) — this is why ADR-002 now carries a Citation Integrity check.
