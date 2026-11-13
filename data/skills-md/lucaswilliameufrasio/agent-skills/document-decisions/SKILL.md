---
name: document-decisions
description: >-
  Record architectural and product/technical decisions before non-trivial
  implementation, and retrieve the rationale for prior decisions. Use when a
  task has meaningful trade-offs, crosses module boundaries, introduces a
  dependency or data flow, or the user asks what was previously decided. Skip
  trivial fixes and purely mechanical changes.
---

# Document decisions

Record durable decisions where future maintainers will find them. First inspect
the repository's existing documentation structure and decision records; update
the established location rather than introducing a competing convention.

## Decide what needs a record

Write a decision record when a future contributor could reasonably ask why one
approach was chosen over another. This usually includes cross-cutting or costly
to reverse choices, architectural boundaries, integrations, data flows, and
changes to build, test, deployment, security, or public contracts.

Do not create decision records for routine implementation details, trivial bug
fixes, mechanical dependency updates, or cosmetic changes unless they expose a
real trade-off.

## Choose the right document

- Use an **ADR** for durable, cross-cutting decisions that are difficult to
  reverse. Keep accepted, deprecated, and superseded records so history remains
  understandable.
- Use a **feature/design note** for decisions and open questions local to one
  feature.
- Keep **domain glossaries** focused on terms, entities, and relationships.
- Keep **agent/repository instructions** focused on standing conventions and
  tools, not as a substitute for rationale or decision history.

Use the repository's own filenames, numbering, and template if present. Do not
invent an ADR number or mark a proposal accepted before the decision is made.

## Decision record contents

For a substantive decision, capture:

1. Context and the problem being solved.
2. The decision and its rationale.
3. Meaningful alternatives and why they were rejected.
4. Consequences, trade-offs, and follow-up work.
5. Status, date, and evidence/source when the repository's template uses them.
6. A condition that should trigger revisiting the decision, when useful.

## Workflow

1. Before implementing a non-trivial change, check for an existing decision.
2. If the decision is already settled, follow it and link the record.
3. If it is unresolved, surface the real alternatives and ask the user when
   their choice affects behavior or architecture.
4. Record the choice after it is confirmed, then implement. If a decision
   changes, supersede the old record instead of silently rewriting history.
