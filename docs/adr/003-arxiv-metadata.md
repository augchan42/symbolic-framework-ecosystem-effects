# ADR-003: arXiv Submission Metadata

**Status:** Submitted
**Date:** 2026-05-22
**Author:** Augustin Chan

## Submission Details

- **Primary category:** cs.LG (endorsed)
- **Cross-list:** cs.MA, cs.AI (not endorsed for these as primary)
- **License:** CC BY 4.0
- **Zenodo DOI:** 10.5281/zenodo.20338937

## Metadata Fields

**Title:**
Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings

**Author(s):**
Augustin Chan

**Abstract:**
Large language models exhibit innate behavioral tendencies when deployed as strategic agents -- notably a risk-averse "turtle" bias toward defensive play. We show that symbolic reasoning frameworks, injected as per-round reflective prompts into one agent, differentially modulate this bias and reshape the multi-agent ecosystem to produce framework-specific winner distributions. In a 7-player Warring States Diplomacy variant (41 games, 4 conditions, single-campaign memory accumulation), each framework produces a distinct ecosystem signature: under control, Yan dominates (7/11, 64%); under I-Ching yarrow divination, Yan and Chu co-dominate while Qin is completely suppressed (0/10); under Tarot, Qin dominates (5/10, Fisher vs. pooled p = 0.006); under scrambled-text ablation (incoherent oracle text preserving prompt structure), Qi dominates (5/10, Fisher vs. pooled p = 0.006). The framework-receiving agent (Han) never wins and shows no survival difference across conditions (Fisher p = 1.0), but Tarot consistently elevates Han's peak territory (mean 3.0 SCs vs. 2.1-2.5 others, Kruskal-Wallis p = 0.010). Neither framework's content predicts subsequent actions -- hexagram themes (chi-squared p = 0.95) and Tarot card postures (chi-squared p = 0.69) are both independent of action choice -- suggesting the modulation operates through the reflective process, not content-following. We present this as an observation paper establishing that alignment-framework choice at the agent level produces distinctive system-level consequences in multi-agent settings.

**Comments:**
17 pages, 3 figures, 6 tables, 6 listings. Code and data: https://doi.org/10.5281/zenodo.20338937

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
