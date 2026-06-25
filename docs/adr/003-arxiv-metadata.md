# ADR-003: arXiv Submission Metadata

**Status:** v1 submitted (arXiv:2606.07552, 2026-05); v2 replacement metadata prepared below — not yet uploaded
**Date:** 2026-05-22 (v1); updated 2026-06-25 (v2)
**Author:** Augustin Chan

> **v2 is a replacement of arXiv:2606.07552**, not a new submission. The live paper's primary is now **cs.MA**: it was submitted as cs.LG (the only endorsed primary, via the king-wen paper) and arXiv moderators reclassified it to cs.MA a few weeks after posting. A replacement keeps that current classification — do not try to set the primary back to cs.LG. The fields below are updated to the v2 (N=61 emergent-reframe) content; paste these at upload time. The v1 values are preserved in the Notes section for history.

## Submission Details

- **Primary category:** cs.MA (live; moderators reclassified from the cs.LG submission ~weeks after v1 posted)
- **Cross-list:** cs.AI, cs.LG (verified live on arxiv.org/abs/2606.07552, 2026-06-25; cs.LG became a cross-list after the primary moved to cs.MA)
- **License:** CC BY 4.0
- **Zenodo DOI:** 10.5281/zenodo.20338937 (v1 release) — **cut a v2 version release and update this DOI before upload if you want v2 data attached**

## Metadata Fields

**Title:**
One Agent's Reasoning Framework Reshapes the Multi-Agent LLM Ecosystem

**Author(s):**
Augustin Chan

**Abstract:** *(v2, pure ASCII — verified against `paper/main.tex`)*
Large language models exhibit innate behavioral tendencies when deployed as strategic agents - notably a risk-averse "turtle" bias toward defensive play. We show that symbolic reasoning frameworks, injected as per-round reflective prompts into one agent, differentially modulate this bias and reshape the multi-agent ecosystem to produce framework-specific winner distributions. In a 7-player Warring States Diplomacy variant (61 games, 6 conditions, single-campaign memory accumulation), framework choice reshapes the winner distribution (Monte-Carlo permutation omnibus p approximately 0.001 over the four primary conditions), producing condition-associated ecosystem signatures: under control, Yan dominates (7/11, 64%); under I-Ching yarrow divination, Yan and Chu co-dominate while Qin is completely suppressed (0/10); under Tarot, Qin dominates (5/10); under scrambled-text ablation (incoherent oracle text preserving prompt structure), Qi dominates (5/10). The scrambled-to-Qi attractor is the most robust (significant against both a pooled denominator and control alone, p = 0.006 and 0.012); the tarot-to-Qin attractor is significant only against the pooled denominator (p = 0.006, vs. control alone p = 0.064). The framework-receiving agent (Han) never wins and shows no survival difference across conditions (Fisher p = 1.0), but Tarot consistently elevates Han's peak territory (mean 3.0 SCs vs. 2.1-2.5 others, Kruskal-Wallis p = 0.010). Neither framework's content predicts subsequent actions - hexagram themes (chi-squared p = 0.95) and Tarot card postures (chi-squared p = 0.69) are both independent of action choice. A memory-free decision-isolation probe (960 calls) further shows the modulation is emergent rather than per-decision: stripped of memory and multi-agent context the reflective process does not change the receiving agent's risk posture (hold-rate Friedman p = 0.45; the I-Ching changes no decisions beyond temperature noise, p = 0.60; Tarot perturbs move content but not risk posture, p = 0.021), locating the effect in memory accumulation and multi-agent dynamics rather than per-decision processing. A 2x2 factorial decomposition separating yarrow's decision-time (per-round oracle) and learning-time (between-game I-Ching reflection) components reveals a non-additive interaction: each component individually freezes the board (50-60% stalemate rate, Fisher p = 0.012 and 0.004 vs. control), but combined they produce zero stalemates (interaction p = 0.004). Direct testing relocates yarrow's Qin suppression from the framework-receiving agent's own cooperation to rival (Chu) expansion through a map corridor; a depth-matched follow-up then shows that expansion is governed by campaign memory depth, not the oracle (condition p = 0.55), so even this pathway is emergent rather than framework-specific. We present this as an observation paper establishing that alignment-framework choice at the agent level produces distinctive, non-additive system-level consequences in multi-agent settings, transmitted through emergent multi-agent and memory dynamics rather than the framework's per-decision effect on the receiving agent.

**Comments:**
24 pages, 3 figures, 9 tables, 6 listings. Code and data: https://doi.org/10.5281/zenodo.20338937
*(update the DOI here if a v2 Zenodo version is cut)*

> **v2 retitle note:** the title changed from "Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings" (v1) to "One Agent's Reasoning Framework Reshapes the Multi-Agent LLM Ecosystem" (v2). Rationale: v2's decision-isolation controls show the effect is emergent, not a per-decision modulation of the receiving agent's risk posture, so the v1 title overclaimed. The new title foregrounds the robust, novel result — the asymmetry (one agent's scaffold reshapes the whole system, without benefiting that agent) — and deliberately names no specific measured quantity ("winner distributions"/"signatures"), so it stays resistant to the planned Paper-3 campaign-variance correction (40-100% breach-rate spread across nominally identical campaigns) and the cross-cultural-following result. Consider noting the retitle briefly in the replacement's Comments so readers/citers see why it moved (the arXiv ID is unchanged).

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
