---
name: test-design
description: "Use when tests are the main deliverable or uncertainty, including explicit TDD, proof-layer selection, coverage, assertions, and doubles. Excludes unknown-cause failures and routine implementation proof."
---

# Test design

## Overview

Design the smallest test set that can falsify the important behavior.
Keep routine implementation proof in `engineering`. Use this skill when the test shape is the deliverable or the main uncertainty.

## When to Use

- Explicit TDD or test-first feature work
- Selecting unit, integration, contract, property, state-machine, or end-to-end proof
- Designing assertions, fixtures, or real/fake/mock boundaries
- Adding focused tests for known behavior or legacy characterization

## When Not to Use

- Use `debugging` first when the failure or failing boundary is unknown
- Use `engineering` when test choice is routine support for an understood change
- Use `improve-test-suite` for a repo- or subsystem-wide test-suite audit

## Minimal Workflow

1. State the behavior claim, the failure risk, and the public or stable seam that can falsify it.
2. Inspect existing coverage, repository commands, incident history, and the real dependency boundary before adding tests.
3. Choose the cheapest layer that can fail for the target behavior. Prefer focused contract or integration proof over broad E2E and internal mock choreography.
4. Apply the [proof guidance](../engineering/references/proof.md) to ground setup and expected results, and establish how the test rejects a plausible broken implementation for material behavior.
5. Keep the boundary under test real. Fake slow or uncontrollable collaborators; mock only an understood external protocol, never the behavior being trusted.
6. Select only relevant cases: happy path, boundary partitions, invalid input, state transition, duplicate/retry, partial failure, permission denial, concurrency, or recovery.
7. For TDD, complete one vertical red-green-refactor slice at a time and observe the expected failure before production edits. Continue through the requested behavior; the first green slice does not end a larger task.
8. Run the focused tests and relevant surrounding gate. Finish when the target claim can fail for the right reason, coverage added or replaced by this task has no needless duplication, and material proof gaps are stated. Reuse earlier results only after confirming the tested code and relevant state are unchanged.

## Reference Routing

- Read [references/test-selection.md](references/test-selection.md) when the proof layer, doubles, oracle, or case matrix is consequential.
- Read [references/tdd.md](references/tdd.md) only for explicit TDD or a behavior change where a cheap trustworthy failing test is the chosen development loop.
- Read [references/browser-e2e.md](references/browser-e2e.md) for browser flows, selectors, visual evidence, or Playwright-style end-to-end work.
- Read [engineering/references/legacy-change.md](../engineering/references/legacy-change.md) for characterization seams in poorly understood code.

## Failure modes

- More tests without more trust
- Assertions coupled to private helpers, call order, or internal data shape
- Expected values copied from production logic
- Mocking away the boundary that fails in production
- Broad E2E flows for behavior a cheaper seam can prove
- Screenshot commands, typechecks, or coverage percentages treated as behavior proof
- Test suites that grow while obsolete or subsumed tests remain
