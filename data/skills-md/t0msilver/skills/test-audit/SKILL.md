---
name: test-audit
description: "Decide which tests are worth having. Use whenever writing, changing, reviewing, or pruning tests: a gate for every new test, and an audit workflow for tests that re-assert source, mirror the code under test, test mocks, duplicate stronger coverage, or keep test-only production code alive. Triggers: adding a regression test, 'clean up the tests', 'these tests are flaky/brittle', mock-heavy suites, coverage-driven tests."
---

# Test audit

A test earns its maintenance cost by catching a break someone would call a bug.
One bar applies both when writing tests and when deciding which existing ones
to delete. For pruning a whole subsystem's tests in one change, read
[reference/campaign.md](reference/campaign.md) first.

## Before writing a test

Answer all four; a missing answer means don't add the test yet.

1. **What production change makes it fail, and is that change a bug or a
   decision?** If only an intentional decision can fail it (a constant's
   value, exact wording, private structure), it is a change detector: it fires
   on redesign and sleeps through bugs. Test the behavior that depends on the
   decision instead: not `MAX_RETRIES == 5`, but "the sixth attempt never
   happens".
2. **Where is the expected value from?** A literal, a worked example, or the
   spec. Never the code under test or its helpers: `expect(f(x)).toBe(f(x))`
   passes by construction. An expectation that re-derives the value with the
   implementation's own formula shares that formula's bugs.
3. **Why doesn't existing coverage catch it already?** Each contract has one
   owning test at its strongest boundary, usually the public interface. A
   second layer needs a risk the owner can't reach, such as a transport or
   lifecycle failure. Prefer a new row in an existing table test over a
   near-duplicate test.
4. **Does it need a production seam that no production caller needs?** An
   export, flag, getter, reset hook or `destroy()` added for the test. If so,
   test at the real boundary instead; cleanup only tests need goes in test
   utilities.

Then check it against the [junk patterns](reference/junk-patterns.md). A
match fails the gate unless the
[retention bar](reference/junk-patterns.md#retention-bar) names the contract
it independently guards. A test that breaks under a behavior-preserving refactor is asserting
implementation; rewrite it at the owning boundary before landing it.

Don't test the framework (asserting your router calls the handler you
registered), and don't test trivial code: constructors, getters and plain
forwarding earn a test only when they validate, normalize, default, derive or
cause a side effect.

## Regression tests

A regression test must fail on the pre-fix code, for the reason the bug
describes, and pass after the fix. Run it against the old code to see it. An
error the bug doesn't cause (import failure, missing selector, broken setup)
proves nothing; fix it until the test fails the way the bug does. A regression test
that never failed proves the mock, not the fix. Write one, at the owning
boundary; don't replay the same scenario at every layer it crosses.

## Mocks

- Never assert on the mock. An assertion that passes when the mock exists and
  fails when it's removed says nothing about your code.
- Before mocking a method, list its side effects. Mock the slow or external
  level below the ones the test depends on, not the method itself.
- Mock responses mirror the complete real structure, not just the fields this
  test reads; a partial mock passes while integration breaks.
- When arguments, call counts or ordering are the contract, assert them. Give
  each branch (success, error, malformed) its own fixture, so the wrong branch
  can't satisfy the test.
- When mock setup outgrows the test, or you can't say why the mock is needed,
  use real components with a fake network or filesystem instead.

## Before finishing

Mentally mutate the production code: wrong constant or argument, wrong branch,
missing side effect, empty return, missing check for empty, zero, null,
unauthorized or malformed input. At least one test should fail for each. A
mutation nothing catches marks an unprotected behavior or a tautological test.

## Auditing existing tests

1. Read the root and scoped `AGENTS.md`/`CLAUDE.md`, then, for each
   candidate: the complete test, the production code it covers, its callers,
   overlapping tests, CI routing and `git log` for why it exists. If it claims
   dependency-backed behavior, read the dependency's source or types.
2. Keep discovery read-only. Prefer a few well-evidenced candidates over a
   long speculative list. For a broad scope, run parallel read-only agents
   split by area.
3. Record the [evidence](reference/junk-patterns.md#candidate-evidence) for
   each candidate before editing. A missing field means it isn't ready to
   delete.
4. Edit one coherent batch per change. Delete the test-only exports, flags,
   wrappers and dead production paths the deletion unlocks, rather than
   keeping aliases. Move retained regressions to their owning suite. Don't add
   replacement tests that restate the same implementation.
5. Run the smallest owning and sibling tests, then the gate the repo requires
   for changed files. For a deleted source-text assertion, run the script or
   dry-run that owns the real contract.
6. Report production and test line counts separately (`git diff --numstat`),
   plus the tests you kept that looked like junk, and why.

## Gotchas

- **Static or slow is not a reason to delete.** A test that reads source text
  can be the cheapest independent guard of a user-facing key, byte or path.
  Keep it if it fails when that contract changes and survives renaming an
  identifier. Keep the others the
  [retention bar](reference/junk-patterns.md#retention-bar) lists.
- **A deletion candidate that fails on the base branch is a possible product
  bug.** Reproduce it and fix the production code; don't delete the test that
  found it.
- **Judge a test by its assertions, not its name.** A test named "retires the
  window" once asserted that the window was *not* cleared.
- **Check negative tests for the right reason.** A denial from a different
  guard, or a rejection the production path never reaches, passes while
  protecting nothing.
- **Don't delete for the count.** Uncertain candidates stay. Optimize for
  confidence in what remains.
- **Don't change tests while the suite is running in that checkout.** Watch
  mode and parallel runners pick up half-edited files and report failures
  that don't exist.
