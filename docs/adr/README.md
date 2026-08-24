# ADR naming convention

This repository's ADR series is short (001–004) and is cited from, and cites into,
`warringstates-engine`, whose series runs to 025. A bare `ADR-001` is therefore
ambiguous — and had already been miscited across the boundary.

**Every ADR reference carries a repository code.** Filenames stay numeric, because
paths are cited from other repos and must keep resolving.

| Code | Repository | Series |
|------|-----------|--------|
| `SFEE` | this repo — the paper | ADR-SFEE-001 … 004 |
| `WSE` | `warringstates-engine` — the engine and experiments | ADR-WSE-000 … 025 |
| `SDE` | `say-do-eval` | *(no ADR series; see its `docs/status.md`)* |

The engine repo carries the full legend at `docs/adr/README.md`, including the
concrete miscitation that prompted the convention: `ADR-WSE-025` anchored its
central argument on "ADR-001 (2026-05-13)," meaning **this** repo's
`001-paper-claim-verification.md` (line 83, the `hexagram_action_correlation.py`
stale-game-list finding) — while that repo's own ADR-001 is an unrelated 2026-03-24
architecture document.
