---
name: flow-test
description: "Behavior-focused tests. Use when adding coverage, writing a regression test first, or fixing flaky tests that fail randomly or intermittently. Hands off to `flow-work` for implementation or `flow-verify` for an acceptance gate."
metadata:
  stage: build
---

# Test

Test at the lowest level that exercises the real failure mode. A useful test rejects a wrong
observable result and survives a valid rewrite.

## Process

1. Read the requirement, changed code, test config, fixtures and repository commands. Identify
   the contract, risk and observation boundary before choosing a framework.
2. Unit tests for pure logic, integration for real module/protocol boundaries, end-to-end for
   critical user flows, browser component tests when DOM, layout or interaction is the risk.
   No fixed pyramid or E2E quota.
3. For an unclear contract, write a characterization test labeled with the behavior it
   preserves. Pin before you change, but do not freeze a known bug as intended behavior.
4. One reason to fail per test. Assert outputs, accessible behavior, effects or public
   contracts. Mock external boundaries deliberately, never the code under test. Realistic
   fixtures, no credentials or production data.
5. Run the targeted tests and confirm discovery. For a regression, show the failure before the
   fix (or a safe negative control) and check why it fails; a broken import proves nothing.
   Then run required gates and affected integration checks.
6. Report commands, environment, discovered tests, results and gaps. Coverage shows unexercised
   code, not correct assertions.

## Flakiness

Reproduce and isolate the nondeterminism: shared state, clock/timezone, randomness, ordering,
network, concurrency, resource cleanup. Control clocks and seeds, wait on observable readiness,
reset per-test state, and repeat enough to test the suspected cause. Never add a blind retry.
A quarantine needs an owner and reason and stays visible as missing coverage. In UI tests,
prefer semantic locators over sleeps; stabilize viewport, fonts and data before visual diffs
and still inspect meaningful differences.

## Red flags

- "I'll write the test after the fix": then you never saw it fail for the right reason.
- "It passes, so it works": check it would fail if the behavior broke.
- "Just add a retry": find the nondeterminism first, and say so when a retry is requested.
- "I need green today": a quarantine with an owner and visible missing coverage beats a retry that hides the bug.
- "Mock it to make it pass": mocking the unit under test proves nothing.

For pure logic with wide input ranges, consider property-based tests; to check that assertions
bite, mutate the code under test and confirm a test fails.

## Anti-patterns

- Snapshotting huge output without a contract or diff review.
- Asserting a heading or implementation string exists instead of behavior.
- Claiming a pass without running the real runner and checking discovery.
- Adding a dependency, retry policy or global coverage target without demonstrated need.

## Done when

- Tests exercise the identified contract and fail for meaningful violations.
- Actual runner results are recorded, including skipped or unavailable checks.
- Remaining flakiness or coverage gaps have a consequence and next action.

Continue with `flow-work` for implementation, or `flow-verify` when evidence must pass a separate gate.
