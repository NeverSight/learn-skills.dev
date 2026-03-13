---
name: tdd
description: >
  Use when implementing any feature or fix outside code-forge workflow — enforces
  Red-Green-Refactor cycle with mandatory test-first discipline. For ad-hoc development,
  quick fixes, or any code change that is not tracked by code-forge:impl.
---

# Code Forge — TDD

Standalone Test-Driven Development enforcement for any code change.

## When to Use

- Writing code outside of code-forge:impl workflow (ad-hoc changes, quick fixes)
- Any new feature, bug fix, or behavior change that needs test discipline
- When you catch yourself about to write production code without a test

**Note:** code-forge:impl already enforces TDD internally. This skill is for work outside that workflow.

## Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

No exceptions. Not for "simple" changes. Not for "obvious" fixes. Not when under time pressure.

## Workflow

```
RED (write failing test) → VERIFY RED → GREEN (minimal code) → VERIFY GREEN → REFACTOR → REPEAT
```

## The Cycle

Complete each phase fully before moving to the next.

### 1. RED — Write a Failing Test

- One minimal test showing the desired behavior
- Clear, descriptive test name
- Use real code, not mocks (unless unavoidable: external APIs, time-dependent behavior)
- One behavior per test

### 2. VERIFY RED — Watch It Fail (MANDATORY)

Run the test. Confirm:
- It **fails** (not errors)
- The failure message describes the missing behavior
- It fails because the feature is missing, not because of typos or setup issues

If the test **passes**: you're testing existing behavior. Rewrite the test.
If the test **errors**: fix the error, re-run until it fails correctly.

### 3. GREEN — Write Minimal Code

- Simplest code that makes the test pass
- No extra features, no "while I'm here" improvements
- No premature abstractions — three similar lines beats a premature helper

### 4. VERIFY GREEN — Watch It Pass (MANDATORY)

Run the test. Confirm:
- The new test **passes**
- All other tests **still pass**
- Output is clean (no warnings, no errors)

If the new test **fails**: fix the code, not the test.
If other tests **fail**: fix them now, before proceeding.

### 5. REFACTOR — Clean Up (After Green Only)

- Remove duplication, improve names, extract helpers
- Keep all tests green throughout
- Do NOT add new behavior during refactor

### 6. REPEAT

Go back to Step 1 for the next behavior.

## Anti-Rationalization Table

| Thought | Reality |
|---------|---------|
| "This is too simple to test" | Simple code has the sneakiest bugs. Test it. |
| "I'll write tests after" | Tests written after implementation pass immediately — they prove nothing. |
| "I already tested manually" | Manual testing is ad-hoc and not reproducible. Write the test. |
| "Just this one quick fix" | Quick fixes without tests become permanent regressions. |
| "TDD is too slow" | TDD is faster than debugging untested code later. |
| "Deleting my code and starting over is wasteful" | Sunk cost fallacy. If code isn't test-driven, rewrite. |

## Verification Checklist

Before claiming work is complete:

- [ ] Every new function/method has at least one test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason (not errors)
- [ ] Wrote minimal code per test (no gold-plating)
- [ ] All tests pass with clean output
- [ ] Edge cases and error paths covered
- [ ] Mocks used only when unavoidable

## When Stuck

- Test too complicated to write → design is too complicated, simplify first
- Must mock everything → code is too coupled, extract interfaces
- Test setup is huge → extract test helpers or fixtures
