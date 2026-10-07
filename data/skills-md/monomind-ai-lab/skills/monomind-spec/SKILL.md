---
name: monomind-spec
description: "Create or update a living implementation specification after intent is clear. Use before coding when required behavior, failure scenarios, public test seams, interfaces, data changes, non-goals, acceptance proof, or rollback requirements need one observable contract. Skip mechanical changes with self-evident requirements."
---

# Monomind Spec

Turn confirmed intent and repository evidence into a durable contract for what will be built and how it will be proven.

## Establish the frame

1. Read project instructions, the relevant code and tests, domain vocabulary, and applicable decisions. Treat current behavior as evidence, not automatically as the desired behavior.
2. Name assumptions that could change scope, interface design, data compatibility, or rollout risk. Resolve material ones before finalizing the spec.
3. If the request contains several independently shippable and verifiable capabilities, propose a small capability map with stable ids, responsibilities, and dependency direction. Use one spec when the work is one capability; do not manufacture a hierarchy.
4. Identify public **seams** where behavior can be observed. Prefer existing seams. Introduce a new seam only when the required behavior cannot be verified cleanly through an existing one.
5. For version-sensitive framework or platform decisions, verify the detected version against current primary documentation and cite the decision source. Mark what remains unverified.

## Write the living spec

Use the project's established location and format. Otherwise use this structure:

```markdown
# <Capability>

## Problem and outcome
Who has the problem, why it matters now, and the observable outcome.

## Scenarios
Numbered normal, boundary, failure, and recovery scenarios in domain language.

## Requirements
Required behavior and invariants, each with an observable acceptance signal.

## Interfaces and data
Public contracts, ownership boundaries, compatibility, migrations, and error semantics.

## Verification
Agreed test seams, runtime evidence, quality gates, and success measurements.

## Operations
Observability, rollout, rollback, and data-recovery needs proportional to risk.

## Constraints and non-goals
The binding limits and what this effort intentionally excludes.

## Open decisions
Only unresolved choices that genuinely block or alter the work.
```

Avoid speculative file lists and working code samples that will age faster than the decision they represent. A compact schema, type shape, or state machine is appropriate when it expresses a settled contract more precisely than prose.

Record an architectural decision separately only when it is hard to reverse, surprising without context, and the result of a real tradeoff. Otherwise keep the rationale in the spec.

Update the spec when implementation evidence changes a decision. Record the change and its reason; do not let the code and spec silently diverge.

## Completion criteria

- Every requirement has an observable acceptance signal.
- Interfaces name their owner, compatibility expectations, and failure behavior.
- Test seams cover the important behavior without binding tests to internals.
- Risks have proportional verification and rollback treatment.
- Non-goals and unresolved decisions are explicit.
