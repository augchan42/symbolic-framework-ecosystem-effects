# ADR-002: arXiv Submission Checklist

**Status:** In Progress
**Date:** 2026-05-22
**Author:** Augustin Chan

## Context

Preparing the paper "Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings" for arXiv submission. This checklist is derived from the king-wen-agi-framework submission (arXiv 2026-04-10, cs.LG) and standard arXiv preparation guidance.

## Submission Metadata

- **Primary category:** cs.MA (Multi-Agent Systems)
- **Cross-list:** cs.AI
- **License:** CC BY 4.0
- **Title:** Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings
- **Author:** Augustin Chan
- **Companion paper:** king-wen-agi-framework (already on arXiv)
- **Zenodo DOI:** *(create before arXiv submission, as with king-wen)*

## Pre-Bundle Checklist

### Source Integrity

- [ ] All figures compile correctly (no missing files)
- [ ] All citations resolve (no `[?]` in output) — **DONE** (fixed 2026-05-22)
- [ ] All cross-references resolve (no `??`)
- [ ] No LaTeX errors or warnings in final build
- [ ] Paper reads correctly end-to-end

### Content Review

- [ ] Abstract: remove LaTeX syntax for arXiv metadata field (e.g., `\citep`, `$p = 0.006$` → plain text)
- [ ] Title: use initial caps, remove LaTeX line break (`\\`)
- [ ] Author: plain text, no LaTeX formatting → `Augustin Chan`
- [ ] Bibliography entries are current (check if any cited preprints have since been published)
- [ ] Spellcheck: authors' names, proper nouns, abstract, section headings
- [ ] No journal-specific boilerplate (we use plain `article` class, so N/A)

### Stats / Data Integrity

- [ ] **§4.5 content-independence numbers match the reproducer** — Re-run the card/hexagram action-independence reproducer (`tarot_action_correlation.py`, currently in `warringstates-engine/scripts/`; port a copy into this repo's `scripts/` so v2 is self-contained) against the N=41 dataset and confirm every stat in §4.5 matches its output exactly: the hexagram advance-vs-non-advance Fisher (currently `OR = 1.40, p = 0.34`, `paper/main.tex:205`), the hexagram theme χ² (`p = 0.9454`, line 205), and the Tarot posture χ² (`p = 0.6860`, line 207).
  - *Why this is on the list:* the superseded n=28 draft (`warringstates-engine/docs/paper/framework-ecosystem-effects.tex`, the version currently on arXiv) reported `OR = 1.29, p = 0.47` for this same test, which matched **no** script output — the reproducer gave `OR ≈ 1.38, p ≈ 0.27`. That was a stale hand-edited statistic that survived into a submission. Don't let an unverified §4.5 number survive into v2. (Audit, 2026-05-31.)

## Bundle Preparation

### Step-by-step

1. **Create working copy**
   ```bash
   cp -r paper/ arxiv-submission/
   cd arxiv-submission/
   ```

2. **Flatten directory structure** — arXiv needs all files in root
   ```bash
   mv figures/*.pdf .
   rmdir figures/
   ```
   Then edit `main.tex`:
   - `figures/winner-distributions.pdf` → `winner-distributions.pdf`
   - `figures/peak-scs-by-condition.pdf` → `peak-scs-by-condition.pdf`
   *(Only two \includegraphics calls, both in figures/ subdir)*

3. **Remove comments from .tex files**
   - Remove the 3 header comment lines (lines 1-3: `% Symbolic Reasoning...`)
   - Remove all `% ====` section divider lines (13 total)
   - No inline comments exist (verified 2026-05-22)
   - Everything uploaded becomes public

4. **Keep the .bbl file** — arXiv does NOT run bibtex
   - `main.bbl` must be included in the bundle
   - Delete `references.bib` from the bundle (keep in repo, not in submission)

5. **Delete build artifacts and rendered PDF**
   ```bash
   rm -f main.aux main.blg main.log main.out main.pdf
   ```

6. **Delete hidden files**
   ```bash
   rm -rf .git .DS_Store ._*
   ```

7. **Add pdflatex multi-pass hint** — append after `\end{document}`:
   ```latex
   \typeout{get arXiv to do 4 passes: Label(s) may have changed. Rerun}
   ```

8. **Test compile in the flattened directory**
   ```bash
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   # Verify: no errors, no warnings, PDF looks correct
   ```

9. **Final cleanup after test compile**
   ```bash
   rm -f main.aux main.log main.out main.pdf
   # Keep only: main.tex, main.bbl, *.pdf (figures)
   ```

10. **Create tarball**
    ```bash
    tar -cvf arxiv-submission.tar *
    ```

### Expected bundle contents

```
arxiv-submission.tar
├── main.tex                        # LaTeX source (no comments, flat paths)
├── main.bbl                        # Pre-compiled bibliography
├── winner-distributions.pdf        # Figure 1
├── peak-scs-by-condition.pdf       # Figure 2
└── (no other files)
```

No `arxiv.sty` needed — we use plain `article` class (king-wen used `arxiv.sty` but we don't).

## arXiv Upload Checklist

- [ ] Upload `arxiv-submission.tar`
- [ ] Inspect extracted file list — remove anything arXiv flags as unnecessary
- [ ] Check pdflatex output log for errors
- [ ] Carefully review the compiled PDF arXiv generates

### Metadata fields (plain text, no LaTeX)

- [ ] **Title:** `Symbolic Reasoning Frameworks Modulate LLM Risk Aversion in Multi-Agent Strategic Settings`
- [ ] **Author:** `Augustin Chan`
- [ ] **Abstract:** Copy from paper, but:
  - Replace `\citep{...}` citations with inline text or remove
  - Replace `$p = 0.006$` with `p = 0.006` (no math mode)
  - Replace `$\chi^2$` with `chi-squared`
  - Replace `\emph{...}` with plain text
  - Remove all newline breaks and extra whitespace
  - Remove `\\` line breaks
- [ ] **Primary category:** cs.MA
- [ ] **Cross-list:** cs.AI
- [ ] **License:** CC BY 4.0
- [ ] **Comments field:** e.g., `17 pages, 3 figures, 6 tables, 6 listings`

## Post-Submission

- [ ] Verify PDF renders correctly on arXiv
- [ ] Send paper password to any co-authors for ownership claim
- [ ] Update repo README with arXiv link
- [ ] Create Zenodo release with DOI (if not done pre-submission)
- [ ] Cross-reference with king-wen paper if appropriate

## Known Pitfalls (from king-wen experience)

1. **`.bbl` version mismatch** — arXiv's TeX Live version may differ from local. If bibtex/biblatex versions clash, recompile `.bbl` with matching TeX Live version.
2. **Flattened paths** — forgetting to update `\includegraphics` paths after moving figures to root is the #1 cause of build failure.
3. **Hidden files** — `.DS_Store`, `._*` (macOS resource forks) will be included unless explicitly deleted.
4. **Font issues** — we use standard CM fonts (no `libertine`/`newtxmath`), so this should be clean.
5. **`listings` package** — we added this for Appendix A. Verify arXiv's TeX Live includes it (it's standard, should be fine).
6. **Unicode in listings** — our listings contain `→` and `←` which we handle via `literate` in `\lstset`. Verify these render on arXiv's pdflatex.
7. **Comments in listings** — the `%` inside `lstlisting` environments is literal, not a LaTeX comment. Do NOT strip these during comment removal.

## Differences from king-wen submission

| Aspect | king-wen | This paper |
|--------|----------|------------|
| Document class | `article` + `arxiv.sty` | `article` (plain) |
| Fonts | `libertine` + `newtxmath` | Standard CM |
| Figures | 2 PDF | 2 PDF (+ 6 listings in appendix) |
| Bibliography | `.bbl` only | `.bbl` only |
| Packages of note | — | `listings` (for appendix) |
| Primary category | cs.LG | cs.MA |
| Cross-list | cs.AI, cs.NE | cs.AI |
| Zenodo | Created first | *(TBD — create first)* |
