---
license: MIT
name: fix-commit-review
description: >
  Audit bug-fix commits for problem validity, completeness, proportional cost,
  scope, simplicity, ownership, and reuse. Separate existing-feature repairs
  from corrections to the reviewed commit.
---

# Fix Commit Review

Treat fix claims as hypotheses. Review behavior and design adoption; skip
formatting and linting. Apply changes only when authorized.

## Establish evidence

Identify the commit and base, normally its parent; clarify the comparison for
merges. Read the message, issue, contracts, diff, relevant implementation,
callers, and tests. Separate symptom, expected behavior, root cause, and scope.
Assess each substantive fix claim independently.

Trust descriptions only when substantive, and verify against code and consumers.
A claimed fix or refactor may add a feature; classify actual effects.

Prefer a focused reproduction that fails on the base and passes after the fix,
asserting the required result. Distinguish execution from inspection. Request
material missing requirements while continuing independent checks; keep affected
conclusions provisional. Never invent history, measurements, or test results.

## Audit criteria

- **Real problem:** Identify the violated contract, trigger, and affected users.
  Distinguish defects from unsupported use, deliberate tradeoffs, and accepted
  limitations using documentation, decisions, and callers. Age or a comment
  alone does not prove acceptance. Report conflicting contracts. Extending an
  accepted boundary is a capability or policy change, not automatically a fix.
- **Complete resolution:** Trace the cause across entry points, alternate
  callers, failures, state transitions, compatibility, and recovery. Check for
  bypasses and adjacent cases sharing the cause. Error suppression or mitigation
  is incomplete unless it satisfies the contract. Required wiring, migration,
  and acceptance cases cannot be deferred. Tests must detect the original
  defect through observable behavior; mocks must not hide it.
- **Worthwhile cost:** Weigh impact, frequency, and urgency against complexity,
  maintenance, compatibility, operational risk, runtime, and memory costs.
  Separate complexity inherent in the required repair from difficulty imposed by
  the existing architecture, and from avoidable machinery added by the fix.
  Cite contract and implementation evidence; allow mixed causes and mark unknowns.
  Compare bounded structural preparation with a direct repair before attributing
  the whole cost to the problem or recommending broad refactoring.
  Challenge expensive machinery or performance loss for minor, non-urgent
  problems. Compare smaller repairs, workarounds, or retaining an accepted
  limitation. Small defects can still merit repair. Support material performance
  tradeoffs with measurements or explicit uncertainty; required correctness can
  justify cost.
- **Clear boundary:** Separate unrelated fixes, additions, and substantial
  independent refactoring. Keep necessary wiring, cleanup, and regression
  coverage with the repair. Shared causes can justify multiple symptoms and
  cross-layer changes; shared files alone do not justify bundling.
- **Simple, effective solution:** Prefer the simplest design satisfying the
  contracts. Challenge redundant checks, duplicated state, configuration,
  special cases, and indirection. Propose concrete simplifications without
  removing required behavior or safeguards.
- **Right layer:** Find the layer owning the invariant. Consider fixing it
  lower down when shared enforcement serves relevant consumers. Check context,
  dependency direction, contracts, and compatibility. Keep caller-specific
  policy at the caller; lower is not automatically better.
- **Justified generalization:** Inspect sibling paths for the same cause.
  Separate adoption required for completeness from optional reuse. Share the
  smallest proven mechanism while preserving differing policies. Name foreseeable
  variations and extension seams; avoid speculative frameworks. Another path
  violating the promised invariant is incomplete repair, not optional adoption.

## Separate proposed repairs

Establish origin against the base, not changed-line proximity. Use two groups:

- **Existing-feature repairs:** Independent defects already present in the
  base. Propose separate changes with regression coverage; put prerequisites
  before the reviewed commit.
- **Reviewed-commit corrections:** Introduced regressions, incomplete claimed
  repairs, or necessary implementation, ownership, and scope adjustments.
  Keep corrections and coverage with the reviewed commit when revision is
  authorized; otherwise propose an attributed follow-up preserving history.

An incomplete claimed repair belongs in the second group even when its original
bug predates the commit. Do not relabel required completion as a separate
existing-feature follow-up. Label uncertain origins and needed evidence. Keep
optional extensions separate; order changes by dependencies and explain coupling.
Each proposed change must work without later repairs.

## Report

Lead with the claim's status: substantiated, partial, contradicted, or unverified,
and whether acceptance is blocked. Briefly cover each criterion with evidence
or uncertainty; do not manufacture findings.

For substantive findings, give location, trigger, consequence, evidence,
severity, origin, remedy, and focused validation. Separate blockers, questions,
and optional improvements. Group remedies as above and state dependencies.
Report executed checks, inspection, and verification limits. Passing a
reproduction alone does not establish acceptable scope, cost, or ownership.
