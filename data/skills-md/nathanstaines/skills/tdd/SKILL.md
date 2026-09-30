---
name: tdd
description: Test-driven development, the red → green loop. Use when the user wants to build features or fix bugs test-first, or wants integration tests.
---

# Test-driven development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns and the rules of the loop. Every section applies on every cycle; consult them before and during the loop, not after.

Where tests live and which runner to use comes from the `### Testing` stance in the Agent skills block (if the stance is missing, re-run `/setup-skills`). When the recorded stance is test-free, surface the contradiction before writing any tests; if the user wants to proceed, update the stance to match. When the stance says tests are welcome but none exist yet, the loop's first tests set the pattern; once they land, update the stance line to record where they live and which runner.

When exploring the codebase, use the project's domain glossary vocabulary in test names and interface language and respect any ADRs in the area you're touching (see `docs/agents/domain.md`).

## What a good test is

Tests verify behaviour through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification ("user can checkout with valid cart" tells you exactly what capability exists) and survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is where a module's interface lives: the place you test at, observing behaviour without reaching inside. Tests live at seams, never against internals. Run the `/codebase-design` skill for the seam vocabulary and the rules for choosing one.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. When a spec from `/to-spec` already records the agreed seams, those count as confirmed; don't re-ask. No test is written at an unconfirmed seam. You can't test everything; agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behaviour hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
  - **Existence check**: `toBeDefined()`, `toBeTruthy()` or a not-null assertion passes for almost any output, so it can't disagree with the code either; assert the value itself.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behaviour: you test the _shape_ of things rather than user-facing behaviour, the tests go insensitive to real changes and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **Watch it fail.** Run the new test and confirm it fails for the expected reason before implementing; a test that fails from a typo or missing import proves nothing.
- **Green means the whole suite.** A slice is done when every test passes, not just the new one.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **A bug fix starts at red too.** Reproduce the bug as a failing test at an agreed seam, then fix until it goes green; the test stays as a regression guard.
- **Refactoring is not part of the loop.** It belongs to a separate review pass (`/code-review`) once the loop ends, not the red → green implementation cycle.

## If a failing test is impractical

Some changes have no seam where a test is cheap: it would need broad harness setup, production-only state, slow end-to-end infrastructure, vague reproduction steps or large unrelated fixture churn. Then take the closest executable check that can still go red: a targeted script, a reproduction command, browser automation, a snapshot comparison, a log assertion or a focused integration check. Propose it alongside the seams so the user confirms the fallback too.

A red check beats a bad test. Beyond the anti-patterns above, a test is bad when it depends on timing or unrelated global state, needs expensive infrastructure for a small change or would be deleted as soon as it proved the fix.

## Final response

Report the evidence, not just the outcome:

- **Red**: the test or check that failed before the change, and the failure it produced.
- **Green**: the passing run, and any nearby validation.
- **No red**: if failing-before evidence couldn't be shown, why, and which check stood in for it.
