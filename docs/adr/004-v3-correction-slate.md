# ADR-SFEE-004: v3 Correction Slate

**Date:** 2026-08-24
**Status:** OPEN — one item applied, the rest outstanding. This is the gating list for the arXiv v3 replacement.
**Depends on:** ADR-SFEE-001 (paper claim verification), ADR-SFEE-002 (arXiv submission checklist), ADR-SFEE-003 (arXiv metadata)
**Upstream provenance:** `warringstates-engine/docs/adr/023-citation-rate-detector-defect.md`, `.../024-content-before-counts.md`, `.../025-launch-artifacts-are-not-games.md`

## Context

Between 2026-08-19 and 2026-08-24 four separate defects were found in the analysis
code behind this paper, in the sibling `warringstates-engine` repo and in the
`say-do-eval` Inspect port. Each is documented upstream. **None of that provenance
lived in this repo**, which carries the manuscript: a reader of `paper/main.tex`
could see a corrected number with no way to learn why it changed, what else is
pending, or which prior claims are superseded.

This ADR is that record. It exists so the v3 replacement is assembled from a list
rather than from memory.

## The slate

### 1. §4.3 citation comparator — ✅ APPLIED (`5a8963c`, 2026-08-24)

77.1% (131/170) → **70.6% (151/214)**, both `paper/main.tex` and
`arxiv-submission/main.tex`. Two defects running in opposite directions and
partly cancelling: a stale game set (deflating) and a **substring** detector
(inflating) that counted the contested supply centre *Luoyang* as an oracle
citation via `yang`. The corrected denominator now agrees with the χ²'s stated
`n = 214`, which the published pairing did not — the two statistics in that one
sentence were computed over different game sets sharing only 8 of 10 games.

The detector is now **stated in the text** (word-boundary match on the paper's own
nine keywords; 68.2% under a stricter oracle-only vocabulary). This satisfies
ADR-WSE-023 decision item 4 and is the substantive fix: the public artifact ships no
citation-rate code and `data/han_orders.csv` carries `reasoning_chars` but not the
reasoning text, so the published figure was **unfalsifiable by any external
reader**. A stated detector is auditable even without the data.

The independence result is untouched. The tarot companion figure (81.6%) was
audited and is **clean** — substring and word-boundary agree exactly, 0 spurious —
so the cards-vs-hexagrams contrast **widens** from 81.6/77.1 to 81.6/70.6, mildly
strengthening the paper's point.

### 2. Inter-rater agreement in the Han message coding — ⚠️ NOT IN THE PAPER YET

Fleiss' κ computed expected agreement from *items containing a label* rather than
*total ratings assigned it*, inflating κ on skewed label distributions. Corrected:

| dimension | published κ | corrected κ |
|---|---|---|
| register | 0.987 | **0.747** |
| posture | — | 0.939 |
| specificity | — | 0.977 |
| elaboration | 0.867 | **0.562** |

Majority-vote and Fisher results are unaffected. **Elaboration at 0.562 is only
*moderate* agreement**, and any v3 claim resting on that dimension needs to say so.
Fixed upstream in `warringstates-engine@0a7a0bf33`; the blind-coding content null
itself is confirmed.

### 3. Chu-blockade counterfactual — ⚠️ §10.2 MUST NOT BE CITED

The `three_gorges` severing test named in §Future Work item 4 has run to 72
completed games. Two findings in `warringstates-engine/docs/experiments/chu-blockade-experiment.md`
§10 are **superseded** (see ADR-WSE-025 upstream, and §11 of that doc):

- **§10.2's condition × map interaction does not replicate.** It was described
  there as "the strongest thing in the dataset." At full N both arms move the same
  direction: breach difference-in-differences **−0.174, permutation p = 0.483**;
  Qin-final-SC DiD **+0.52, p = 0.663**.
- **H2 passes pooled but is carried by four games.** Qin final SC severed 4.52
  (n=21) vs canonical 2.92 (n=24), MWU **p = 0.0106** — but split by launch wave,
  the balanced June wave (17 v 17) gives **p = 0.13**. The pooled p is an artifact
  of combining waves at different campaign depths.

**What this means for the manuscript:** §5.5 and §Limitations already state that
the corridor is load-bearing *topology* while its *use rate* is memory-depth-driven
rather than oracle-driven (condition p = 0.55). The counterfactual now supports
that from an **intervention** rather than an observation, and §Limitations'
"unconfirmed by counterfactual intervention" can be softened — but **only** to
"corridor confirmed as a general pathway," never to "yarrow-specific mechanism
confirmed." The interaction that would license the stronger claim is at p ≈ 0.5.

### 4. Methodology: content before counts — ⚠️ CONSIDER FOR §Limitations

ADR-WSE-024 (upstream) records that the Han divergence scan concluded "no divergence"
from order counts, message lengths and keyword hits **without reading a single
message**. The content layer and a blind coding run were added on review, and the
null held. Worth a sentence in §Limitations on how the outward-channel nulls were
established, since "we read the transcripts" is materially different evidence from
"we counted keywords."

## The pattern worth stating in the paper

Four defects, one shape: **an analysis trusting whatever the filesystem or a
substring happened to return, with nothing asserting what it should have
returned.** ADR-SFEE-001 (this repo, 2026-05-13) flagged the class; it recurred in
ADR-WSE-023, again in ADR-WSE-024, and a fourth time in ADR-WSE-025 — each time because the
prior fix was applied by hand with no regression test. Every one is now
test-guarded upstream.

Three of the four were caught only because the raw game archives are on one
machine. That is itself a finding about the artifact, and §Limitations should say
so plainly: **the published artifact is not sufficient to reproduce §4.3.**

## Decision

1. **Do not upload a v3 replacement until items 2–4 are dispositioned.** Item 1 is
   done; the others are either not in the manuscript or actively contradict text
   that is.
2. **Add a `Stats / Data Integrity` gate to ADR-SFEE-002** requiring §4.3's citation
   figure to be reproduced from `citation_detector.py` against `CLEAN_DATASET`,
   with the detector variant named. (Added with this ADR.)
3. **Port the citation-rate reproducer into this repo's `scripts/`,** as ADR-SFEE-002
   already requires for the independence reproducer, so §4.3 becomes checkable
   without the sibling repo. Currently it is not.
4. **Reconcile the upstream branches first.** — ✅ **DONE 2026-08-24.**
   `warringstates-engine` had ADR-WSE-023 and ADR-WSE-025 on `adr-023-citation-detector`
   and ADR-WSE-024 plus the Fleiss fix on `main`, with neither branch seeing the other's
   findings. Merged at `78922e695`. The reconciliation surfaced one thing this slate did
   not know: **ADR-023 had been written twice**, independently, on both branches. The two
   authorings agreed on every number but disagreed on tarot — `main`'s declared the tarot
   figure "out of scope, no defect reported," while the branch had actually audited it and
   found it clean (81.6%, identical under substring and word-boundary matching). The merged
   ADR carries the audit. Nothing in this slate changes as a result.

   The same duplication had happened here: this repo corrected §4.3 twice, on `main`
   (`bf7a7df`, a bare number swap) and on `paper-v2` (`5a8963c`, the swap plus the
   detector-stating footnote). Merged at `a12f167`, keeping the footnote — item 1's own
   gate requires it. Had the merge gone the other way, v3 would have shipped the corrected
   number with the method still unstated, which is the exact condition that let the
   original 77.1% survive review.

## Consequences

- v3 is a **magnitude correction plus a strengthened mechanism claim**, not a
  retraction. The say-do gap, the ecosystem signatures, and the independence
  results all stand.
- The §4.3 sentence is now longer and carries a footnote. That is deliberate: the
  original was short *because* it left the detector unstated, which is what made it
  unauditable.
- ADR-SFEE-002's citation-integrity precedent applies here too — that audit found 17 of
  21 v1 references with fabricated author first names, silent for an entire
  published version. Numbers deserve the same per-item verification as citations.
