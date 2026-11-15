---
license: MIT
name: code-review
description: >
  Review code, pull requests, or commit stacks for requirement conformance,
  correctness, design adoption, and simplification. Classify findings and
  recommend coherent refactor and feature boundaries.
---

# Code Review

Review behavior and design adoption against the original requirements. Report
evidence-backed findings; do not spend review time on formatting or linter checks.

## Establish the review contract

- Identify the target, base, and scope. Inspect the whole change or stack before
  judging individual boundaries.
- Trust descriptions only when substantive, and verify against code and consumers.
  A `refactor` label may hide a new feature; classify actual effects.
- Find the original requirements, acceptance criteria, constraints, and
  exclusions in the conversation or supplied issue/specification. If missing,
  explicitly ask the user for them. Continue independent checks while waiting,
  but mark conformance as unverified. Code and tests do not replace requirements;
  keep inferred intent provisional and clarify material ambiguity.
- Consider the complete design and foreseeable interactions. Resolve gaps
  needed for correctness now; reserve relevant future extension points with
  concrete reasons, without speculative machinery. Do not label plans with `V1`.

## Review behavior and design adoption

Read the diff, final implementations, callers, interfaces, and relevant tests.
Trace success, failure, and boundary paths across components.

- **Requirements:** Map acceptance criteria to implementation and behavioral
  evidence. Identify partial, missing, or unverified behavior, scope expansion,
  and violations of exclusions.
- **Correctness and oversight:** Check relevant invariants, errors, state
  transitions, ownership, concurrency, compatibility, and migration. Look for
  omitted cases and interactions introduced by the change.
- **Adoption:** Verify that callers use the design coherently and obsolete paths
  disappear or have an explicit compatibility purpose. Flag unused abstractions,
  duplicated sources of truth, and incomplete migrations.
- **Complexity source:** Distinguish complexity inherent in required behavior
  from integration difficulty caused by the existing architecture. Cite the
  contracts and code responsible; both may contribute, and missing evidence
  leaves attribution open. Identify avoidable complexity introduced by this
  change separately. Compare bounded preparation with direct integration before
  recommending structural changes; preserve required behavior.
- **Simplification and quality:** Challenge redundant branches, duplicated logic,
  unnecessary state, indirection, configuration, and generic machinery. Assess
  responsibilities, dependency direction, API clarity, and testability. Propose
  a simpler viable design with concrete maintenance or risk benefits, preserving
  required behavior, invariants, and justified extension seams. Treat naming and
  documentation as findings only when they obscure meaning or contracts;
  preference for another valid design is not a defect.
- **Large modules:** Flag large modules that mix responsibilities or obscure
  independent subsystems. Propose cohesive splits with clear ownership, narrow
  interfaces, and acyclic dependencies, preserving behavior and invariants.
  Use responsibility and coupling, not arbitrary line counts; avoid mechanical
  fragmentation or catch-all utility modules.
- **Logical item order:** Check that related declarations and cases follow a
  coherent domain, lifecycle, or dependency order, especially enum variants and
  tests. Group related enum variants and place new ones with their semantic
  peers. Group tests by behavior and order cases so the progression from ordinary
  behavior to boundaries and failures is easy to follow. Use the domain and
  established local organization to choose the order; do not impose alphabetical
  sorting or flag an equally clear alternative. Explain how scattered or
  misplaced items obscure relationships or coverage. Before recommending a
  reorder, check implicit discriminants, derived ordering, serialization,
  iteration, and test execution dependencies; preserve required behavior and
  compatibility.

Use focused behavioral tests or reproductions to resolve material uncertainty,
and honor required repository checks. Distinguish execution from inspection.

## Classify findings

Assign one primary category per root cause. Severity and acceptance impact are
independent of category and effort.

| Category | Meaning | Disposition |
| --- | --- | --- |
| **Correctness Fix** | Implemented behavior violates a contract or invariant, or regresses. | Repair in the current work. |
| **Scope Completion** | A small missing feature or acceptance case completes agreed scope with little implementation and verification effort. | Include in current work when implementation is authorized. |
| **Feature Follow-up** | Missing capability needs substantial work or a product decision; also covers additions outside agreed scope. | Record as a separate addition for a later commit or follow-up change. |
| **Design Refinement** | Simplification or maintainability improvement preserves behavior. | Refine; separate substantial refactoring from features. |

- A large repair or structural remedy for broken behavior is still a Correctness
  Fix. Estimate completion effort by contracts, dependencies, migration, and
  verification, not line count.
- A required Feature Follow-up remains an unmet requirement until the user
  changes scope. Mark its acceptance impact; deferral cannot justify accepting
  an incomplete or unsafe feature.
- Optional refinements are not blockers without demonstrated harm. Small effort
  does not authorize product-scope expansion.

## Separate concerns and order changes

Split independently meaningful concerns by intent and dependencies, even when
they touch the same files. Keep necessary wiring and tests with their behavior.

- For a feature mixed with a notable refactor, put independent, behavior-preserving
  preparation first, verify it, then add the feature to the resulting structure.
  If part depends on the feature, explain the coupling; do not force a reversal.
- Separate unrelated fixes and additions; keep inseparable small cleanup with
  its implementation. Each boundary must work without later repairs and preserve
  necessary compatibility or migration stages.
- Reject fixture-only commits unless they add new fixtures to establish baseline
  behavior or contain a large test change with several new test modules. Harness
  or test-execution changes are not fixture-only. Otherwise, keep fixtures with
  the implementation they test.
- Give Feature Follow-ups distinct additions with acceptance criteria,
  prerequisites, and required extension seams. Dependencies take precedence
  over placing additions later. Avoid temporary structures and add-then-move churn.

### Review linear slices

For consecutive changes under review, inspect each parent diff and the base-to-tip
result. Trace additions through later changes; a correct tip can hide broken
boundaries or wasted work. Flag:

- Blank-line-only changes, including a single added or removed blank line.
  Treat these as restack artifacts: include necessary blank lines in the
  relevant implementation change and remove unrelated edits.
- Code added in one place and moved in a later commit, including within the
  same file. This leaves the restack unclean: add the code at its final location
  in the introducing commit. Keep an intermediate location only when a required
  migration or compatibility stage needs it.
- Features largely rewritten, design reversals, or repeated moves and renames
  without independent value. Introduce the settled design at its original boundary.
- Fixes to defects introduced within the slice. Put corrections and regression
  coverage in the introducing change; fixes to preexisting defects remain valid.
- Unused additions later deleted, temporary scaffolding, duplicate implementations,
  and add/revert/reintroduce cycles. Omit detours; add preparation with its first
  consumer unless independently useful, preserving justified extension seams.
- Deferred wiring, migrations, tests, or documentation needed to make an earlier
  boundary complete and credible.

Allow coherent extensions and added coverage. Necessary migration stages need
independent purpose, valid behavior, and a clear exit. Textual overlap alone is
not a defect; preserve distinct, durable features.

Cite introducing and later changes, explain the failure or churn, and propose
boundaries preserving intended final behavior. Classify history-only churn as
Design Refinement; distinguish broken intermediate states repaired later from
defects remaining at the tip.

### Review change descriptions

Check intent, behavior, material design decisions, and compatibility claims against
each change and its position. Flag stale claims, concatenated fixup narratives,
and promises fulfilled only later; ignore cosmetic preferences. Remove routine
CI obligations and pass claims (test counts, formatter/linter success); put
verification evidence and limits in the review. Retain substantive testing intent
or unusual validation constraints when they explain coverage or a tradeoff.

Recommend changes for review-only requests; carry out fixes or history changes
only within existing authorization and repository workflow. Local plan files
are deliberately untracked; do not check their tracking or reread them merely
to confirm they were written.

## Deliver an actionable review

Lead with requirement conformance and acceptance blockers, noting unavailable
requirements. Group findings by category, ordered by severity; omit empty groups.

For each finding, state category, severity, acceptance impact, location, evidence,
trigger and consequence, remedy, and verification. Distinguish confirmed defects
from questions and optional improvements; omit unsupported claims.

Include a proposed change sequence when splitting is needed, unresolved
requirement questions, and verification limits. If no substantive findings exist,
say so with the reviewed scope. Add future language or domain checks to the
review lenses while keeping the categories stable.
