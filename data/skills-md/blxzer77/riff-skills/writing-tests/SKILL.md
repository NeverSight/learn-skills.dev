---
name: writing-tests
description: Writes tests that catch regressions and preserve behavior. Use when fixing a bug, adding or changing behavior, refactoring (especially untested code), judging coverage, choosing a test strategy, or fixing flaky or over-mocked tests, even if tests aren't mentioned. Not for CI setup or load testing.
license: Apache-2.0
metadata:
  verified-on: "2026-10-30"
---

# Writing tests

Tests are what keep a codebase changeable. When a change alters observable
behavior, add or update a behavioral test unless existing coverage already protects
that behavior or a test is not applicable. For documentation, formatting, pure
renames, configuration-only changes, and other no-behavior changes, do not add a
redundant test; state the reason and retain the relevant existing checks.

## Workflow

**Bug fix**
- [ ] Reproduce the bug as a test through the public interface, using the user's
      scenario. Run it and **see it fail for the reported reason**. A test you never
      saw fail proves nothing.
- [ ] If the bug was found high (end-to-end, API), narrow it: keep the high-level
      reproduction if cheap, and add the smallest test that still fails.
- [ ] Fix the code. Run the new test, then the related suite.
- [ ] Report: the test name, that it failed before and passes now.

**New or changed behavior**
- [ ] List the changed observable behaviors: the normal case, relevant boundaries
      (empty, one, limit, limit+1), domain transitions such as month lengths,
      leap days, time zones, rounding, or encoding when applicable, invalid input,
      and user-visible error paths.
- [ ] Add or update enough tests to cover each meaningful risk, through the public
      API, at the smallest level that gives confidence (see below). Reuse an
      existing test when it is the right protection rather than duplicating it.
- [ ] Run them; delete or fix any new test that passes before the code exists when it
      is meant to expose a regression.

**Refactor**
- [ ] If the code lacks tests, first add persistent characterization tests to the
      project's normal test suite, pinning current observable behavior. Run that
      suite against the original code and see it pass before refactoring.
- [ ] Keep those tests unchanged while refactoring and run them again. An ad hoc
      comparison script or randomized probe can supplement the suite, but does not
      replace a durable test file in the project.

**Before reporting done**: run the tests you touched plus the nearest suite. Never
claim tests pass without running them; if you cannot run them, say so.

## What a good test looks like

- **Behavior, not structure.** Call the public API and assert on observable results
  (return values, state, output, persisted data). If a refactor that keeps behavior
  would break the test, the test is wrong. Needing to test a private function is a
  design signal, not a reason to expose it.
- **One behavior per test, named for it**: `charges_no_shipping_when_free_shipping_coupon_combined_with_percent_discount`,
  not `test_total_2`. Arrange / act / assert, visibly.
- **No logic in tests.** No loops or conditionals computing expected values;
  write the expected value literally. Repetition that keeps a test readable is fine.
- **Expected values come from the spec, not from the code.** Never run the code and
  paste its output into the assertion; that freezes bugs into the suite. The
  exception is a characterization test before a refactor, which pins today's output
  on purpose: name it as one, and point out any pinned output you think is wrong.
- **Deterministic and hermetic.** No real sleeps, wall-clock time, randomness without
  a seed, network, or shared state between tests. Inject a clock; use the runner's
  fake timers; build fresh state per test.
- **Fails with a useful message.** Assert on the specific value, not on truthiness.

## Choosing the level

Default to the smallest test that exercises the behavior with real collaborators.

| Situation | Test at | Why |
|---|---|---|
| Pure logic, parsing, pricing, state machines | unit | fast, precise failures |
| Code whose value is wiring: handlers, queries, UI components | integration (real DB in a container, real framework, in-process server) | mocks here test your assumptions, not the system |
| A user-visible flow that crosses processes | a few end-to-end tests | expensive and slow; cover only the critical paths |
| Contract between services you own on both sides | consumer-driven contract test | catches breaking changes without a full environment |

If a higher-level test finds a bug that no lower-level test catches, add the lower
one. Do not duplicate the same assertion at every level.

## Test doubles

Prefer, in order: the real implementation → a fake (working in-memory version) →
a stub (canned answers) → a mock (expected-call assertions). Use doubles at process
boundaries you do not own (payment APIs, email, clocks, randomness), not between
your own classes. Assert on interactions only when the interaction *is* the
behavior (an email was sent, a charge was made), never on how a result was computed.

## Never do these to get green

- Weaken, skip, or delete a failing test, or loosen its assertion, without
  establishing that the test itself is wrong. If it is, say so explicitly.
- Add retries or longer sleeps to a flaky test. Find the nondeterminism.
- Change production behavior to suit a test, such as moving a boundary from `>` to
  `>=`. Making code testable (injecting a clock) is fine; changing what it does is a
  separate decision the user must make. Propose it instead.
- Update snapshots or golden files without reading the diff.
- Write assertion-free tests to raise coverage.

## Gotchas

- Coverage measures lines executed, not behavior checked. A suite can reach 90% and
  catch nothing; judge it by whether it fails when the code is wrong. To check that
  on critical code, read `references/mutation-testing.md`.
- A new test passing on the first run, before any code change, usually means it
  tests the wrong thing.
- Over-mocked suites are brittle *and* blind: they break on refactors and pass on
  real breakage. Replacing mocks of your own code with real objects often fixes both.
- Timing-based assertions (`sleep(ttl)` then expect expiry) race against the clock.
- When the project has a test convention (runner, layout, naming, fixtures), follow
  it even if you would choose differently.
- For LLM-powered features, assert on structure and invariants (valid JSON, required
  fields, refusal on bad input) in normal tests; quality of generated text belongs
  in an eval suite, not in exact-match assertions.

## References

- `references/flaky-tests.md` — read when a test passes and fails without code changes.
- `references/property-based-testing.md` — read for parsers, serializers, math, data
  transformations, or any function with a clear invariant.
- `references/mutation-testing.md` — read when asked whether tests are good enough,
  or before trusting coverage on critical code.
- `references/test-strategy.md` — read when setting up testing for a new project or
  rebalancing a suite (sizes, pyramid vs. trophy, contracts, snapshots).
- `assets/agents-snippet.md` — offer it for the project's `AGENTS.md` so tests stay
  the default even when this skill is not loaded.
