---
name: aizen-quality
description: Aizen knowledge pack (v24) — test strategy, levels, case design, bug reports, test lenses; independent review with blast radius and gating, code/security/supply-chain/infra/ui/release review, verification of reports. Loaded by Aizen roles through their brief; not a standalone skill, do not trigger it directly — use aizen-build.
---

# Testing and review knowledge — Aizen pack (v24)

Owns the topics `test`, `review`: every `references/<topic>/…`, `assets/<topic>/…` and `scripts/<topic>/…` path for them
lives here. Shared rules (authority, evidence, code quality, style) are in `aizen-core`; the flow and roles are in
`aizen-build`.

- **Used by:** tester; reviewer (every lens, `redteam`); the review route of aizen-build.
- **Entry points:** `references/test/method.md` · `references/review/method.md` — each has a "Guides" table; load only the rows the change touches.
- Templates: `assets/test/` (test plan, lens report) and `assets/review/` (review, security, verify reports).
