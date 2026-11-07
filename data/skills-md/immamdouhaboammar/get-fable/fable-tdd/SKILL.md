---
name: fable-tdd
description: "Drive testable behavior changes and bug fixes through disciplined red-green-refactor cycles with observable regression tests. Use when implementing new features with unit/integration tests, fixing reproducible bugs, modifying business logic, or writing test-first behavior contracts — even if the user does not explicitly say \"fable-tdd\" (e.g. \"fix this bug test-first\", \"write a test and make it pass\", \"add this feature with tests\", \"TDD this logic\"). Do NOT use for broad exploratory prototyping without clear assertions (use fable-discover or fable-plan) or for post-implementation reviews (use fable-review)."
version: 1.3.0
pack: build
inputs:
  - behavior_contract
requires:
  - test_harness
produces:
  - regression_test
  - behavior_change
gates:
  - red_observed
  - green_observed
fallback: fable-recover
mutatesWorkspace: true
parallelSafe: false
neural_links:
  precursors:
    - fable-plan
  continuations:
    - fable-execute
    - fable-verify
  lateral_peers:
    - fable-execute
  recovery: fable-recover
---

# Fable TDD

Prove the behavior is missing or broken before changing production code, then make the smallest change that satisfies the right test at the right level.

## Mission
TDD is not "write any failing test first." The red state must demonstrate the intended behavior gap through a trustworthy harness. A syntax error, broken fixture, stale build, or mock-only expectation does not earn the right to change production code.

The Skill optimizes for three things:
- **causal confidence**: the test fails because the behavior is wrong;
- **minimal intervention**: implementation changes only what the behavior requires;
- **durable regression proof**: the test would catch the bug if it returned.

## Activate When
- fixing a reproducible bug or regression;
- adding behavior with a stable enough contract to assert;
- changing validation, state transitions, calculations, API behavior, persistence, or integration semantics;
- refactoring where an invariant needs executable characterization first.

## Do Not Activate When
- the behavior cannot yet be located or reproduced (`fable-discover`);
- the main uncertainty is external API semantics (`fable-research`);
- the change is non-executable docs/metadata with no meaningful behavior test (`fable-execute`);
- the required test harness is itself broken or executing stale artifacts (`fable-recover`).

## Change Classification
Classify the behavior before choosing a test.

| Class | Preferred proof |
| --- | --- |
| Pure/domain logic | focused unit/property test |
| Boundary validation/error mapping | unit or contract test at boundary |
| Cross-module interaction | integration test through the changed contract |
| Database/queue/cache behavior | integration test with realistic boundary where feasible |
| HTTP/CLI/public API | contract/integration test at public entry point |
| UI user flow | component/integration first; E2E for high-value cross-boundary behavior |
| Concurrency/timing | deterministic coordination test, not sleep-and-hope |
| Legacy behavior with poor seams | characterization test at nearest stable boundary |
| Refactor/no intended behavior change | characterization/invariant tests before movement |

Use the lowest test level that proves the real behavior **without mocking away the thing under test**.

## Protocol

### Stage 1 — Write the behavior contract
State:
- initial state/input;
- trigger/action;
- expected observable result;
- relevant side effects;
- error/boundary behavior;
- invariant that must remain true.

For a bug, capture the concrete reproduction separately from the proposed implementation.

### Stage 2 — Validate the harness
Before RED, confirm the chosen test actually executes the relevant path.

Check when applicable:
- source vs built artifact;
- test discovery/config;
- fixture realism;
- feature flags/env;
- mock boundaries;
- asynchronous completion;
- cleanup/isolation;
- whether the assertion observes public behavior rather than an internal call count.

### Stage 3 — Choose the test level
Ask:
1. What production change would make this test fail again?
2. Does the test cross the contract where the bug actually lives?
3. Have I mocked the suspected failure away?
4. Can a narrower test prove the same user-visible behavior more deterministically?

If you cannot answer #1, the test is probably weak.

### Stage 4 — RED
Write the smallest test that captures the behavior contract and run it.

RED is valid only if:
- test executes;
- failure is deterministic enough to reason about;
- failure message/state matches the expected missing/broken behavior;
- it is not failing because of setup, syntax, import, environment, stale artifact, or unrelated test pollution.

If the failure reason is wrong, repair the test/harness and repeat RED. **Do not touch production code yet.**

### Stage 5 — Minimal GREEN
Change the smallest production surface that can satisfy the valid RED.

Do not:
- redesign adjacent APIs;
- add speculative flexibility;
- refactor unrelated code;
- weaken the assertion;
- replace real behavior with a mock to reach green.

Run the focused test until GREEN.

### Stage 6 — Adjacent falsification
Before refactor, probe the closest failure surfaces appropriate to the change:
- boundaries/empty/invalid input;
- error path;
- state transition ordering;
- idempotency/retry;
- concurrency/race;
- compatibility with prior format/API;
- persistence/transaction behavior.

Add tests only when they protect a meaningful contract; do not inflate count mechanically.

### Stage 7 — Refactor under green
Now improve structure if needed. Refactor in small steps and rerun the affected tests after each meaningful mutation.

### Stage 8 — Fresh handoff
Record final mutation and hand off to `fable-verify` with:
- behavior contract;
- exact RED evidence/reason;
- GREEN command/result;
- tests added/changed;
- production surfaces changed;
- adjacent cases probed;
- residual risks not covered by the focused test.

## Decision Rules
- Test passes before production change → it does not prove the requested gap; redesign the test or confirm behavior already exists.
- Test errors before assertion → fix harness/test, not production.
- Bug is nondeterministic → first control or instrument the nondeterminism; repeated random reruns are not a reliable RED.
- Concurrency bug → prefer barriers/latches/fake clocks/deterministic scheduling over arbitrary sleeps.
- Legacy code has no unit seam → test the nearest stable public boundary before introducing a seam; do not perform a broad refactor just to make unit testing aesthetically pure.
- External dependency cannot be exercised locally → use a contract/fake only after establishing what behavior the fake must preserve from primary evidence.
- User asks to "just patch it" → if executable behavior is changing, preserve RED discipline unless the absence of a viable harness is explicit and accepted.
- Test expectation conflicts with current agreed product contract → do not force implementation to an obsolete test; resolve the contract first.
- A test only asserts that a mock was called → add observable outcome/state evidence unless the call itself is the public contract.

## Invariants
- No production behavior mutation before a valid RED for testable changes.
- RED and GREEN refer to the same behavior contract.
- Tests are not weakened to make implementation pass.
- The suspected failure mechanism is not mocked away.
- Final GREEN is fresh after the last relevant mutation.
- Refactoring does not add behavior outside the accepted card.

## Failure Taxonomy
### Wrong RED
Failure comes from syntax/import/setup/fixture/environment rather than target behavior. Repair harness first.

### False GREEN
Test passes but does not cross the real failure boundary, often because a mock or stale artifact bypasses it. Strengthen/reposition the test.

### Flaky RED/GREEN
Outcome changes without relevant code mutation. Identify nondeterminism before treating either state as evidence.

### Untestable legacy surface
No narrow seam exists. Characterize at a stable boundary, then introduce the smallest seam supported by the test.

### Contract ambiguity
Expected behavior itself is disputed/unclear. Return to planning/research rather than encoding a guess as a test.

### Implementation loop
Valid RED exists but two materially similar fixes fail. Stop editing and route to `fable-recover` with the RED, attempts, and observed failure differences.

## Anti-Patterns
- writing implementation, then backfilling a test that immediately passes;
- accepting any failure as RED;
- changing expected output to match current implementation;
- asserting only mock interactions when user-visible state can be asserted;
- using sleeps to "test" a race;
- building an elaborate test abstraction before proving one behavior;
- broad legacy refactor before characterization;
- forcing unit tests where only an integration boundary can prove the behavior;
- skipping fresh GREEN after refactor;
- equating coverage percentage with regression proof.

## Evidence Packet

```text
Behavior contract:
Test level + why:
RED command/result + expected failure reason:
Production mutation:
GREEN command/result:
Adjacent cases probed:
Refactor mutations:
Final fresh GREEN:
Residual risk / verify next:
```

## Completion Criteria
TDD completes when:
- the behavior gap was demonstrated by a valid RED;
- production code changed only after that RED;
- focused GREEN is observed for the same contract;
- meaningful adjacent failure surfaces were considered;
- final tests are fresh after refactor/last mutation;
- `fable-verify` receives enough evidence to independently falsify the result.

## Progressive Resources
- Deep strategy: `references/test-strategy-and-hard-cases.md`
- Existing cycle reference: `references/red-green-refactor.md`
- Example: `examples/failing-test-first.md`
