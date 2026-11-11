---
name: test-first-seams
description: Build a feature, fix a bug, or add tests to existing code test-first in red-green vertical slices at agreed seams. Use when the user asks for TDD, red-green, or test-first work, wants a bug proven by a failing test before the fix, or asks what tests a module needs and where to put them. Do not use to audit existing tests for proof value or redundancy.
---

# Test-First Seams

Tests verify behavior through public interfaces, so the code behind them can change
entirely while the tests keep passing. Discover the repository's own test runner
and conventions before writing anything; read `CONTEXT.md` and ADRs in the area if
they exist so test names use the domain vocabulary.

## Agree the seams first

A seam is the public boundary where behavior is observed without reaching inside.
Before the first test, list the seams under test and confirm them with the user.
Prefer existing seams, and the highest one that exercises the behavior; fewer seams
is better. When the shape of the interface itself is in question, use
`deep-module-design`.

## Before adding a test

By default add no new test. Add one when the user asked for tests or test-first
work, or when it protects a named behavior no existing test could catch; whether
the change is risky enough to need one is a question to answer, not a number.
Beyond what behavior the test protects and which regression turns it red, answer
two more questions; without an answer, do not add the test yet:

- Which existing test should already catch that regression, and why does it not?
  A contract gets one owning test at its strongest seam; a second one must be able
  to fail where the owner cannot. If the gap is just a missing input, add a row to
  the owner's table or fixture instead of a sibling test.
- Would the test only work through a hook, export, flag, or wrapper added for it
  alone? Then drop that seam and drive the test through the one production uses.

Pick the type by risk, one test each: pure logic with many edge cases gets one
property test instead of many examples, a main user flow a few end-to-end tests
run in CI. Mutation testing and fuzzing run only on request; the time budget for
checks is `quality-floor`'s.

## The loop

Work one vertical slice at a time: one test at one seam, then the least code that
turns it green, then the next test informed by what that cycle taught you.

1. Red: write one test and watch it fail for the expected reason.
2. Green: write only enough code to pass it, with no speculative features.
3. Run each new test more than once before calling it green; run the test file
   after each change, the typecheck regularly, and the full suite once at the end.

Writing all tests first and all implementation after tests imagined behavior and
locks in test structure before the design is understood.

For a bug, prove it first: write the test that reproduces the reported symptom,
watch it fail against the unfixed code, for the reason the bug report gives, then
fix. A reproduction that never failed proves nothing about the fix. Write one
regression test at the owner boundary, not one per layer the bug crosses. When
independence matters, have a subagent write that reproduction test from the bug
report alone, without seeing the intended fix.

Refactoring belongs to review, after the slice is green.

## What a kept test looks like

- It exercises the public interface and survives an internal refactor.
- It is deterministic: pin the seed and time, compare ordered collections in
  order, and wait on a condition instead of using fixed sleeps.
- It asserts the specific error or outcome, not merely that nothing was thrown;
  no error is swallowed inside the test.
- It covers one behaviour.
- Its name states the capability ("user can check out with a valid cart"), not the
  mechanism.
- It verifies through the interface: create a user, then fetch the user, rather
  than querying the database behind it.
- Its expected value comes from independent truth — a known literal, a worked
  example, the spec, the user's request, the bug report — never recomputed the way
  the code computes it. A test whose only source is the implementation it guards
  adds no proof; leave it out.
- It mocks only system boundaries: third-party APIs, time, randomness, and
  sometimes the database or filesystem. Prefer a real implementation, then a fake,
  then a stub. Internal collaborators you control stay real.
- At a boundary, one function per external operation (`getUser`, `createOrder`)
  keeps each mock a single shape, instead of one generic `fetch` whose mock needs
  conditional logic.

A test breaking during a refactor with unchanged behavior shows it was coupled to
the implementation; rewrite it at the seam.
