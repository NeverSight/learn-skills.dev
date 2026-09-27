---
name: tech-spec
description: Write a tech spec or implementation plan with typed contracts, call stacks, file ownership, and verification.
---

# Tech Spec

A tech spec makes implementation decisions reviewable before code changes. This skill is design-only: keep production files read-only and return the spec inline unless the user or calling workflow authorizes writing it.

## Frame The Change

Use the accepted request and any confirmed Feature Contract as behavioral authority. Inspect the repository instructions and only the code, tests, docs, and runtime constraints needed to design the affected path. Reuse project vocabulary and established patterns where they fit.

Resolve routine engineering choices and explain consequential tradeoffs. Ask when a missing product, public-contract, trust, data-lifecycle, deployment, ownership, or scope decision changes the intended result. Keep unresolved decisions visible; a `Confirmed - Blocked` Feature Contract cannot yield an implementation-ready spec while its blocker still affects the change.

State the current behavior, target outcome, callers, goals, non-goals, invariants, constraints, affected entrypoints and side effects, operational risks, and smallest independently shippable slice. Ground claims in accepted input or inspected evidence rather than repeating broad discovery.

## Subtract First

Before adding structure, identify what the slice can delete, collapse, inline, or narrow. A behavior-preserving refactor should pin current behavior and reduce reader load; separate any behavior change as a feature or fix.

Choose **Direct cutover** when no observed consumer, retained data, deployment constraint, or user requirement needs the old path, and leave one path. Choose **Protected evolution** only for a named obligation; place the compatibility mechanism at the narrowest seam and give temporary support a removal condition.

## Specify The Design

Prefer typed contracts and call stacks over broad prose. Present materially different alternatives only when an important interface, ownership seam, or runtime topology remains unsettled; otherwise state the locally coherent design and rationale.

Show every added, changed, or deleted boundary a caller must understand. Use the project's implementation language or typed pseudocode for domain values and states, application inputs and outcomes, expected failures, public APIs or messages, parsers and projections, owned ports and adapters, and persistence or protocol records. Name what each seam hides. A hypothetical second implementation does not justify a new abstraction.

Trace each changed behavior from its public entrypoint through ownership and side effects to its observable result:

```text
raw input
  -> boundary parser
  -> domain/application input
  -> owning module
  -> external adapter or persistence
  -> typed outcome
  -> boundary projection
  -> observable result
```

Show current versus proposed flow when behavior or ownership moves. Include only reachable failure, authorization, transaction, idempotency, retry, cancellation, concurrency, and resource-lifecycle branches.

Map files or modules to add, change, and delete, giving each one responsibility for a contract or call-stack step. Sequence safe deletion before construction and remove superseded paths in the same Direct cutover slice.

For observability, first state the operational question that must become answerable. Add signals and safe fields only when existing evidence cannot distinguish the relevant outcomes. Use `observability-logging` when detailed signal policy is part of the design.

## Plan Risk-Matched Proof

Choose the smallest set of meaningful evidence that discriminates the material risks. Prefer:

1. End-to-end through the affected public entrypoint.
2. Integration through the real boundary or adapter.
3. Focused contract or property tests for isolated domain behavior.
4. Unit tests for meaningful behavior not covered by a stronger seam.

A useful pre-change failure at a stable seam is strong evidence, but do not manufacture one. For configuration, migrations, generated output, behavior-preserving refactors with an existing pin, or runtime-only failures, choose a characterization test, repro, replay, equivalence harness, trace query, contract check, or repository-native command instead.

For each material risk, name the proving surface, expected evidence, and any gap that needs manual, runtime, migration, or deployment evidence. Cite an already-thorough suite when it proves the unchanged contract; add broader or repeated verification only when a new risk or observed failure justifies it.

## Deliver The Handoff

Organize the spec for the affected path and omit empty ceremony. Another engineer should be able to identify the exact behavior, chosen shape, typed contract changes, call flow, file ownership, deletion order, risk-matched proof, and unresolved blockers without repeating discovery.

Use direct file paths and one source of truth. Types and call stacks define what; prose explains why. Keep the design proportional to the changed behavior. The spec authorizes neither implementation nor unrequested durable mutation.
