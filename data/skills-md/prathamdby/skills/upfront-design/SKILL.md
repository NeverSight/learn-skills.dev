---
name: upfront-design
description: >
  upfront-design to agree phased designs before coding, resume drafts, or verify approved milestones.
---

# Upfront design

## Route and persistence

A design has request/status frontmatter and a `# Design:` title.
New request → design; draft → first missing section; approved → check next
open milestone; another status → `BLOCKED`. A named revision phase removes
later sections only after the user authorizes that revision.

Resolve this skill's absolute anchor. Store new designs at
`<anchor>/designs/<basename>-<slug>-<YYYY-MM-DD-HHmmss>.md`, outside repos.
`<basename>` is the first repo's root directory name.
After a path exists, persist approved phases and the ledger through sibling
temporary files and atomic rename before advancing. Record
`request | size | design | phase | approvals | ADR offers | terminal`.
Keep the ledger at `<design>.ledger` on `AWAITING_USER`; remove on other terminals.

Small means one module, no contract/data/public-signature change, and a
one-sentence outcome. Return `DIRECT` plus that sentence without a file/ledger.
Otherwise find ADR trees (`docs/adr/`, `adr/`, `doc/adr/`, `docs/decisions/`);
absence is silent. Create the document using `references/design.md`.
Done when route, size, path/frontmatter, and relevant ADRs are fixed.

## Design phases

Each phase pauses with `AWAITING_USER`; write its approved content before
the next starts. Resume at the first missing or explicitly revised phase.

1. **Product:** concrete pain, measurable Success, bold one-line solution,
   supplied mockup or draft text wireframe/state table for user-facing work,
   delivery paragraph. Ask the entire question frontier in one numbered round,
   recommending an answer per question. Done when approved content is persisted.
2. **System:** bold shape + cited pattern, NEW/CHANGED layer roles, sources
   and constraints with cost reasons, phase-banded sequence. Name ADR conflicts,
   not overrides. Done when approved content is persisted.
3. **Program:** changed boundary contracts, constraints, real signatures,
   usage, and roles, not bodies. Cite patterns or assumptions; compare two
   uncertain layouts, choose one, and record why the other lost.
   For multiple boundaries, changed dispatch, or unclear async order,
   apply Wiring views in `references/design.md`.
   Done when each Success maps to symbols/results and approval is persisted.
4. **Slices:** after prefactoring, start with a thin end-to-end contract/check.
   One reviewable vertical PR per milestone; name symbols, expected success
   and relevant failures, assertions/manual proof, repo order, and one open
   checkbox. Only the user defers/skips; wide refactors expand then contract.
   Done when every symbol is assigned and approved milestones are persisted.
5. **Finalize:** set approved. Offer ADRs only for decisions hard to reverse,
   surprising without context, and chosen over a real alternative. On approval
   use `references/decisions.md`. Done with `DESIGNED` when all five document
   sections exist and each ADR offer is written or declined. Report design/ADR
   paths, peer-review, and milestone check route.

## Check

For an approved design, follow `references/check.md` for the first open,
non-deferred/non-skipped milestone. Show exact commands and obtain approval
before running them. Tick only with outcome proof and matching symbols,
not a successful exit. Open manual boxes or ambiguous legacy outcomes pause.
Never edit product files to make a check pass. Done with `CHECKED` if ticked
or all complete, otherwise `AWAITING_USER`.

Terminals: `DIRECT` (router no-op success), `AWAITING_USER`, `DESIGNED`,
`CHECKED`, `BLOCKED`. Revise via draft status and a named phase.
