---
name: tdd
description: >-
  Test-driven development workflow. Write failing tests first, implement to
  pass, then refactor. Enforces red-green-refactor cycles and mandatory test
  runs after every change. Always run full test suite, lints, and evals after
  implementation is complete.
  Activates on: test, tdd, spec, testing, test-driven, red-green, write tests,
  add tests, test first, failing test, test suite, coverage, assert, expect.
metadata:
  version: 0.1.0
---

# Test-Driven Development

Write the test first. Make it pass. Clean up. Run the tests. Every time.

## The Cycle

Every code change follows red-green-refactor:

1. **Red** — Write a test for the next behavior. Run it. Watch it fail.
2. **Green** — Write the minimum code to make the test pass. Nothing more.
3. **Refactor** — Clean up duplication and improve clarity. Tests stay green.
4. **Repeat** — Pick the next behavior. Start another cycle.

Run tests after every step. Not just at the end — after *every* step.

## 1. Start With a Failing Test

Before writing any implementation, write a test that:
- Describes one specific behavior or requirement
- Fails for the right reason (missing function, wrong return value — not a syntax error)
- Uses clear, descriptive names that read as specifications

Do not write multiple tests at once. One test, one behavior, one cycle.

## 2. Write the Minimum to Pass

Make the failing test pass with the simplest code that works. Do not:
- Handle edge cases you haven't tested yet
- Build abstractions before you have three examples
- Add error handling for scenarios not covered by a test
- Optimize before the behavior is correct

If you're writing code that no test exercises, stop. Write the test first.

## 3. Refactor Under Green Tests

After the test passes, improve the code while keeping tests green:
- Extract common patterns only when you see real duplication
- Rename for clarity
- Simplify complex conditionals
- Remove dead code

Run tests after each refactoring move. If any test turns red, undo and try a
smaller change.

## 4. Run Tests After Every Change

This is not optional. Run the relevant test suite:
- After writing a new test (confirm it fails)
- After writing implementation (confirm it passes)
- After every refactoring move
- Before considering any task done

If you cannot run tests (no test runner configured, unfamiliar project), tell
the user and ask how to run them. Do not skip testing and move on silently.

## 5. Discover the Test Runner

Before writing the first test, find out how this project runs tests:
- Look for test configuration files (`jest.config`, `pytest.ini`, `Cargo.toml`, etc.)
- Check `package.json` scripts, `Makefile` targets, or CI config
- Look at existing test files for import patterns and conventions
- Ask the user if nothing is obvious

Match the project's existing test style — framework, file naming, directory
structure, assertion library. Do not introduce a new test framework.

## 6. Test Naming and Organization

Tests are documentation. Follow these conventions:
- Name tests by the behavior they verify, not the function they call
- Group related tests logically (by feature, by scenario)
- Keep each test independent — no shared mutable state between tests
- Follow the Arrange-Act-Assert pattern within each test

For detailed naming and organization patterns, read `references/examples.md`.

## 7. What to Test

Focus tests on behavior at public interfaces:
- Function inputs and outputs
- State changes caused by operations
- Error conditions and edge cases
- Integration points between modules

Do not test:
- Private implementation details
- Framework internals or library code
- Trivial getters/setters with no logic
- The same behavior from multiple angles

## 8. Closing Audit — Mandatory

After all implementation cycles are complete, run a full verification pass.
This is a hard gate — do not consider the task done until all checks pass.

**Run these in order:**

1. **Full test suite** — run the complete test suite, not just the tests you wrote
2. **Linter / formatter** — run the project's lint and format checks if configured
3. **Type checker** — run type checking if the project uses one (tsc, mypy, etc.)
4. **Build** — confirm the project builds if applicable
5. **Review** — verify every test you wrote has a clear name and tests one behavior

If any step fails, fix it before declaring the work complete. Do not leave
failing tests, lint errors, or type errors for the user to clean up.

For the full workflow with decision points, read `references/workflow.md`.

## Per-Cycle Checklist

Before moving to the next cycle, verify:

- [ ] A failing test was written before any implementation
- [ ] The test fails for the right reason
- [ ] Implementation is the minimum needed to pass
- [ ] Tests pass after implementation
- [ ] Any refactoring was done under green tests
- [ ] Tests pass after refactoring

## Post-Implementation Checklist

Before declaring the task complete:

- [ ] Full test suite passes (not just new tests)
- [ ] Linter / formatter passes (if configured)
- [ ] Type checker passes (if configured)
- [ ] Project builds (if applicable)
- [ ] Every new test has a clear, behavior-describing name
- [ ] No test depends on execution order or shared state
