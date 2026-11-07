---
name: test-quality
description: >-
  Framework-neutral standards for the quality of an individual automated test in
  TypeScript: assert on behavior not implementation, meaningful assertions, one
  outcome-named scenario per test, builders over shared fixtures, test doubles
  that earn their place, deterministic order-independent tests, coverage read as
  a map of the unverified. Use it when writing tests for new or changed code,
  reviewing the tests in a pull request, or fixing a weak, brittle, or flaky
  test — or when the user says "test quality", "unit test review", "these tests
  are brittle", "flaky test", "over-mocking", "testing implementation details",
  "AAA", "arrange act assert", or "assert on behavior".
license: CC-BY-4.0
metadata:
  author: danielteles
  version: "1.0"
---

# Test Quality — Engineering Skill

Framework-neutral standards for whether a single automated test is worth having: what it asserts,
how it is named and structured, what it fakes, and whether it runs the same way every time. The
rules hold for any runner (Vitest, Jest, `node:test`) and any framework; examples use TypeScript.

> **Builds on.** `core-typescript` (test code is code), `architecture-and-design` for suite
> *strategy* (the pyramid, unit vs integration), and `react` / `angular` / `vue` for the mechanics
> of rendering and querying a component. Load a sibling only when the task turns on its layer; if
> it is not loaded, apply that layer from general knowledge and do not block.

This SKILL.md is self-sufficient: the **Ruleset** below is the complete, enforceable list. Each
`references/<topic>.md` holds that group's reasoning and `❌ / ✅` code, and
`references/worked-example.md` a full review pass; open them for depth when your runtime allows.

---

## How to Use This Skill

Pick the mode that matches the task. Do the steps in order.

| Mode | Steps |
|---|---|
| **Write** — add tests for new or changed code | 1. For each public behavior, name the scenario and the expected result (`structure-and-naming`). 2. Arrange through the public API, act in one call, assert on the observable result (`behavior-not-implementation`, `assertions`). 3. Build inputs with a builder; fake only what `test-doubles` allows. 4. Run each new test red once — against the unfixed code or a deliberately broken line — before trusting the green. 5. Run the Ruleset as a checklist. Fix each fail before you hand off. |
| **Review** — check the tests in a pull request | 1. Run the Ruleset against the test diff. 2. Write one finding per fail, in the Output Format below. 3. Order the findings: `must-fix` first, then `consider`. 4. If nothing fails, say so in one line. Do not invent findings. |
| **Triage** — fix a weak, brittle, or flaky test | 1. Name why it is bad: asserts on internals, no real assertion, order-dependent, non-deterministic (`determinism`). 2. Change the test, not the code under test — unless the test found a real bug. 3. Quarantine a flake immediately; fix it within the sprint, not with a CI retry. |
| **Characterize** — add tests to untested code before changing it | 1. Write tests that pin the code's *current* observable behavior, quirks included — do not fix bugs yet. 2. Run them green against the unchanged code; this is the safety net. 3. Refactor or fix behind the net, updating a characterization test only when you deliberately change that behavior. |

### Output Format

Write one finding per line:

```
<severity> · <topic> · <file>:<line> — <what is wrong>. <the fix as an action>.
```

- `<severity>` is `must-fix` (breaks a rule in this skill) or `consider` (safe, but a rule prefers another form).
- `<topic>` is a Ruleset topic slug (`assertions`, `test-doubles`, `determinism`, …).

### What makes a test worth keeping

Judge every test on four properties, which trade against each other:

- **Regression protection** — it fails when a real behavior breaks.
- **Refactoring resistance** — it stays green when internals change but behavior does not.
- **Fast feedback** — it runs in milliseconds, so the suite runs on every save.
- **Maintainability** — the next reader understands it and can change it cheaply.

A test that scores low on two of these is a liability. Asserting on implementation trades away
refactoring resistance; real I/O trades away fast feedback and often protection (flakes); a giant
shared fixture trades away maintainability. Every rule below follows from protecting these four.

### Rules for Every Mode

- Name the Ruleset topic when you enforce a rule.
- State the reason, not only the rule. "This passes even when `total()` rejects" beats "await the promise".
- Name the rule and the change; do not rewrite the author's test in silence.
- A test exists to catch a regression a user would feel. A test that breaks on a rename and never on a behavior change is a cost, not an asset — say so.
- When a test and the code disagree, find out which is right before changing either.

---

## Ruleset

### behavior-not-implementation → `references/behavior-not-implementation.md`

- [ ] The test asserts on observable output — a return value, rendered result, a message published, a persisted record — never on a private field or an internal
      step.
- [ ] No assertion on how many times a collaborator was called, or with what, *as a stand-in* for checking the effect those calls produced — unless the call
      itself is the contract (an analytics event, an email sent).
- [ ] The test refers only to the unit's public API; renaming a private helper or reordering internal steps does not break it.
- [ ] The system under test is not spied on or partially mocked — its real code runs.
- [ ] Arrange sets up state through public constructors, factories, or API — not by reaching into internals.
- [ ] The test would survive a behavior-preserving refactor and would fail if the behavior changed.
- [ ] No test that only exercises a framework, library, or language feature you do not own — test *your* use of it, at your boundary, not that React renders or
      that `Array.map` maps.
- [ ] The unit under test is a unit of *behavior*, not a single class — a collaborator is not replaced with a double merely because it lives in another file.
      Real code runs unless `test-doubles` gives a reason to fake it.
- [ ] A private method is exercised through the public API. If it is complex enough to want its own test, it is extracted into its own unit — not tested through
      the back door.

### assertions → `references/assertions.md`

- [ ] Every test has at least one assertion; a "does not throw" test states that explicitly (`expect(fn).not.toThrow()`).
- [ ] One behavior per test — several `expect`s are fine when they describe one outcome, not unrelated ones.
- [ ] Specific matchers: `toEqual(3)` over `toBeTruthy()`; `toThrow(SpecificError)` over `toThrow()`; assert the contents when the contents matter, not just the
      length.
- [ ] The assertion checks the whole relevant result, not one convenient field of it.
- [ ] A collection is compared as an ordered list only when order is part of the contract; otherwise it is sorted first, compared as a set, or checked with
      `arrayContaining`.
- [ ] No assertion against a value the test computed with the same logic as the code under test — use a hand-worked literal.
- [ ] Error paths assert on the error type or message, not merely that *an* error occurred — via `toThrow(SpecificError)` / `.rejects`, never a `try/catch` that
      also passes when nothing is thrown.
- [ ] Async tests `await` the result and assert after it settles; a rejection is checked with `await expect(...).rejects`. No assertion can run before the
      promise resolves.
- [ ] A snapshot is small, stable, and reviewed on every change — never a large auto-generated blob accepted unread. An inline snapshot for a short value is
      fine; a serialized component tree is not an assertion.

### structure-and-naming → `references/structure-and-naming.md`

- [ ] The test name states the scenario and the expected result ("returns 0 for an empty cart"), not the method name ("test getTotal").
- [ ] Arrange / act / assert are visually distinct; the act step is a single call.
- [ ] No production logic in the test body — no `if` / `for` / `switch` / arithmetic that mirrors the implementation.
- [ ] Repeated cases are a data-driven table (`it.each`); one reason to fail per test.
- [ ] `beforeEach` holds only setup that every test in the file needs; anything scenario-specific stays in the test.
- [ ] No dependence on execution order or on state left by a previous test.
- [ ] No `.only` / `fit` / `fdescribe` committed, and no `.skip` / `xit` without a tracked ticket in a comment.

### test-data → `references/test-data.md`

- [ ] Objects are built with a factory or builder that fills sane defaults; the test sets only the fields under test. Start from `assets/builder.template.ts`.
- [ ] The values the assertion depends on are visible in the test, not buried in a shared fixture.
- [ ] No large shared fixture that many tests lean on in different, conflicting ways.
- [ ] Randomized data is seeded and printed on failure; otherwise use fixed, meaningful literals.
- [ ] Distinct roles get distinct values — an id and a quantity are not both `1`.

### test-doubles → `references/test-doubles.md`

- [ ] A double replaces a real collaborator only for a reason: it is slow, non-deterministic, has side effects, or does not exist yet.
- [ ] The network is stubbed at the boundary (MSW, a fake server), not by mocking your own modules.
- [ ] A fake (a working in-memory implementation) is preferred over a mock with scripted expectations for a collaborator used by many tests.
- [ ] A hand-written fake is covered by a contract test that runs against both the fake and the real implementation — otherwise it drifts and the suite passes
      while production breaks.
- [ ] The type under test is never mocked.
- [ ] A stub returns a realistic value that satisfies the collaborator's contract — not an `undefined` that happens to work.
- [ ] Mocks are reset between tests; no stub leaks into the next test or file.
- [ ] Time, randomness, the filesystem, and env vars are injected or faked, not reached for directly.

### determinism → `references/determinism.md`

- [ ] A unit test does no real I/O — no live network, database, disk, or wall clock. If a behavior genuinely needs one, it is an integration test and belongs in
      that layer.
- [ ] No real `sleep` or arbitrary timeout — fake timers or an awaited condition instead.
- [ ] Clock and randomness are controlled (fake timers, a seeded RNG, an injected `now()`).
- [ ] No dependence on real network, wall-clock date, locale, or timezone; the timezone is pinned in test config.
- [ ] Tests pass in any order and in parallel — no shared mutable file, DB row, or global.
- [ ] Cleanup is in `afterEach` and runs even when the test fails.

### coverage → `references/coverage.md`

- [ ] Coverage is read as a map of what is *unverified*, not a score to hit — a line counts only if an assertion depends on it.
- [ ] Branches and boundaries are tested, not only the happy path that lifts the line count.
- [ ] Critical logic (money, auth, permissions, migrations) is checked at its boundaries and, where it pays, mutation-tested.
- [ ] No test written only to raise the number; a test with no assertion, a tautological one, a duplicate, or one covering deleted code is removed.

---

## Limits

This skill judges the individual test. It does not cover:

- Suite strategy and the test pyramid — how much to unit- vs integration- vs end-to-end-test, contract testing, where coverage pays off most. That is the
  `testing` group in `architecture-and-design`.
- Framework mechanics — React Testing Library queries and `user-event`, Angular `TestBed` and `HttpTestingController`, Vue Testing Library and
  `@vue/test-utils`, component harnesses. Those live in the `testing` group of `react`, `angular`, and `vue`.
- End-to-end test design (Playwright, Cypress): selectors, per-worker data, retries, sharding. That is `e2e-testing`.
- Performance and load testing.
- Accessibility testing — a component test that queries by role doubles as an a11y check, but the full lens is in `accessibility`.
- Choosing and configuring a runner (Vitest, Jest, `node:test`), and CI parallelization.

This skill states what makes a test worth keeping. It is not a substitute for running the suite and reading what actually fails.

---

## References

This skill composes with:

- **`architecture-and-design`** — decides the suite shape and what to test at each layer. On a conflict it decides strategy, this skill decides the individual
  test.
- **`react`** / **`angular`** / **`vue`** — the framework mechanics for rendering, querying, and driving a component; this skill's rules about what to assert
  apply on top.
- **`core-typescript`** — test code is code: `strict`, no `any` in fixtures, typed builders, narrowed error assertions.
- **`accessibility`** — querying by role and accessible name is both a behavior assertion and an a11y signal; the full lens lives there.
