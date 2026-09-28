---
name: architect
description: >-
  Design or review consequential software architecture decisions from concrete drivers,
  constraints, boundaries, runtime behavior, tradeoffs, and evolution. Use for storage authority,
  service/module boundaries, distributed behavior, cross-platform architecture, major
  dependencies, or other durable system decisions. Prefer existing architecture, use patterns only
  after the problem is clear, and produce an ADR when a decision is durable.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.1"
---


# Architect

Make consequential system decisions without turning routine implementation into architecture ceremony.

## Trigger

Use when the task materially changes system boundaries, data authority, runtime/process topology, distributed semantics, platform shape, cross-platform architecture, or a hard-to-reverse dependency.

Do not trigger for routine helper extraction, local naming, styling, or an implementation pattern that is already established by the repository.

## Workflow

1. Reality-check the current project architecture and accepted decisions. Explicit user technology choices and accepted ADRs are locked inputs unless new evidence, a blocker, changed requirements, or an explicit revisit justifies reopening them.
2. Frame the decision: desired outcome, constraints, reversibility, affected systems, and evidence gaps.
3. Express material qualities as observable scenarios rather than vague adjectives.
4. Compare candidate boundaries/approaches against the same drivers.
5. Make data authority, runtime behavior, consistency, failure/recovery, and operational consequences explicit when relevant.
6. Record the property the architecture requires without prematurely freezing an incidental mechanism. For example, if future independent devices require stable collision-resistant identity, record that requirement; choose UUID/ULID/package/encoding only when interoperability, storage, external contracts, or another real constraint requires it now.
7. Select patterns only after the concrete problem is named; prefer existing project patterns.
8. Record a durable ADR when the decision is consequential and likely to matter beyond the current task.
9. Re-read project orientation and related durable artifacts after the ADR. If an existing summary is now directly false, reconcile it minimally by replacing the stale statement with a pointer/brief current-state summary; do not duplicate the ADR.

## Outputs

Architecture brief, tradeoff decision, and optionally an ADR. Domain specialists may supply evidence, but this skill owns the architecture decision workflow.

## Stop

Stop when the decision, alternatives, consequences, evidence gaps, downstream implementation/migration handoffs, and directly affected project orientation are consistent. Do not continue polishing an already sufficient architecture record.
## Reference Guide

Load only the references needed for the current task:

- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [artifact model](references/_shared/artifacts/artifact-model.md)
- [boundaries](references/_shared/architecture/boundaries.md)
- [tradeoffs](references/_shared/architecture/tradeoffs.md)
- [pattern selection](references/_shared/architecture/pattern-selection.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
