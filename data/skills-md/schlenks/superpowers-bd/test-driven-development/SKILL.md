---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development (TDD)

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:** New features, bug fixes, refactoring, behavior changes.

**Exceptions (ask your human partner):** Throwaway prototypes, generated code, configuration files.

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Red-Green-Refactor (Task-Tracked)

For each TDD cycle, create three tracking tasks:

1. **RED: Write test for [feature]** -- Write one failing test. MUST run and see it fail before proceeding.
2. **GREEN: Implement [feature]** -- Write minimal code to pass the test. No extras. MUST run and see it pass. Blocked by RED.
3. **REFACTOR: Clean up [feature]** -- Remove duplication, improve names. Keep tests green. Blocked by GREEN.

**ENFORCEMENT:**
- GREEN is blocked until RED is completed (test must fail first)
- REFACTOR is blocked until GREEN is completed (code must pass first)
- Each task requires RUNNING the test command and capturing output
- Skipping the "WATCH it fail/pass" step is now visible in TaskList

## RED - Write Failing Test

Write one minimal test showing what should happen. One behavior, clear name, real code (no mocks unless unavoidable). See `references/good-vs-bad-examples.md`.

## Verify RED

**MANDATORY.** Run test, confirm it fails for expected reason (feature missing, not typos). Test passes? You're testing existing behavior — fix test.

## GREEN - Minimal Code

Write simplest code to pass the test. Don't add features, refactor other code, or "improve" beyond the test. See `references/good-vs-bad-examples.md`.

## Verify GREEN

**MANDATORY.** Run test, confirm it passes and all other tests still pass. Output pristine (no errors, warnings). Test fails? Fix code, not test.

## REFACTOR - Clean Up

After green only: remove duplication, improve names, extract helpers, reduce nesting (flatten conditionals, early returns), eliminate redundant abstractions, prefer explicit over compact.

Keep tests green. Don't add behavior.

**Conditional simplification dispatch:** If >50 lines changed OR cyclomatic complexity >10, dispatch `code-simplifier:code-simplifier` agent on changed files. Re-run tests, verify green, commit as `refactor: simplify [area]`. If tests fail, revert.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## Reference Files

- `references/tdd-cycle-diagram.dot`: Visualizing the TDD cycle
- `references/good-vs-bad-examples.md`: RED/GREEN code examples
- `references/why-order-matters.md`: Rationale for test-first and rebuttals
- `references/rationalizations-and-red-flags.md`: Common excuses and stop signals
- `references/bug-fix-workflow.md`: Bug fix example and debugging integration
- `references/when-stuck.md`: Solutions for common TDD obstacles
- `references/testing-anti-patterns.md`: Pitfalls with mocks, test-only methods

## Final Rule

```
Production code -> test exists and failed first
Otherwise -> not TDD
```

No exceptions without your human partner's permission.

<!-- compressed: 2026-02-11, original: 764 words, compressed: 594 words -->
