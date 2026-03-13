---
name: testing-patterns
description: >
  Universal testing principles including TDD workflow, role-based test matrices,
  and seed data factory patterns. Use this skill when writing or reviewing tests
  to ensure consistent structure, meaningful coverage, and maintainable test
  suites regardless of language or framework.
license: MIT
metadata:
  author: loomcrafthq
  version: "1.0.0"
---

# Testing Patterns

## TDD Workflow

Follow the Red-Green-Refactor cycle for every unit of behavior.

```
Red → Green → Refactor
```

1. **Red** — Write a failing test that describes the expected behavior.
2. **Green** — Write the minimum code to make the test pass.
3. **Refactor** — Clean up the implementation without changing behavior. Tests stay green.

Never skip the Red step. If you write code before the test, you don't know if the test actually verifies anything.

## Test Structure — Arrange, Act, Assert

Every test should have three clearly separated sections.

```
// Arrange — set up the preconditions
[create test data, configure mocks, initialize state]

// Act — execute the behavior under test
[call the function, trigger the action]

// Assert — verify the outcome
[check return values, verify side effects, assert state changes]
```

### Rules

- One **Act** per test. If you have multiple acts, you have multiple tests.
- Keep **Arrange** minimal. Only set up what this specific test needs.
- **Assert** outcomes, not implementation. Test *what* happened, not *how* it happened internally.

## Role-Based Test Matrix

For any feature with access control, test every role explicitly.

| Scenario | PUBLIC (unauthenticated) | USER (authenticated) | ADMIN |
|----------|-------------------------|---------------------|-------|
| Read own data | 401 Unauthorized | 200 OK | 200 OK |
| Read other's data | 401 Unauthorized | 403 Forbidden | 200 OK |
| Create resource | 401 Unauthorized | 201 Created | 201 Created |
| Update own resource | 401 Unauthorized | 200 OK | 200 OK |
| Update other's resource | 401 Unauthorized | 403 Forbidden | 200 OK |
| Delete resource | 401 Unauthorized | 403 Forbidden | 200 OK |

Adapt the matrix to your application's roles. The key principle is: **every role-action combination is an explicit test case**, not an assumption.

## What to Test

### Do Test

- **Business logic and services** — the core of your application
- **Edge cases** — empty inputs, boundary values, nulls, maximum lengths
- **Error paths** — what happens when things fail (invalid input, missing data, downstream errors)
- **Authorization rules** — every role-action combination (see matrix above)
- **State transitions** — valid transitions succeed, invalid ones are rejected
- **Data transformations** — input-to-output mapping for pure functions

### Don't Test

- Framework internals (routing plumbing, ORM query building)
- Third-party library behavior
- Trivial getters/setters with no logic
- Implementation details that could change without affecting behavior

> **Rule of thumb:** Test the *contract* (inputs → outputs), not the *wiring* (which internal function called which).

## Seed Data Factory Pattern

Create reusable factory functions that produce valid test entities with sensible defaults. Override only what matters for each test.

### Principles

- A factory returns a **valid, complete** entity by default
- Each test overrides **only the fields relevant to its assertion**
- Factories compose: a factory for an Order can use a factory for a User
- Factories do NOT touch the database — they produce plain objects. Persistence is a separate concern.

### Conceptual Example

```
createUser(overrides)
  → merge(defaultUser, overrides)
  → return complete User object

// Test: email validation
user = createUser({ email: "invalid" })
result = validateUser(user)
assert result has error on "email"

// Test: admin permissions
admin = createUser({ role: "ADMIN" })
result = canDeleteResource(admin, someResource)
assert result is true
```

This pattern eliminates brittle test setup, makes tests self-documenting, and prevents coupling between unrelated tests.

## Test Naming

Use a consistent naming pattern that describes the scenario and expected outcome.

```
[unit under test] — [scenario] — [expected result]
```

Examples:

- `validateEmail — empty string — returns validation error`
- `calculateDiscount — order over threshold — applies percentage discount`
- `deleteUser — non-admin caller — returns forbidden`

Good test names serve as living documentation. If a test fails, the name should tell you what broke without reading the test body.

## Test Isolation

- Each test must be independent. No test should depend on another test's execution or side effects.
- Reset shared state between tests (database, in-memory stores, global variables).
- Avoid shared mutable variables across tests — prefer fresh setup in each test.
- Tests must pass when run individually, in any order, and in parallel.

## Do / Don't

| Do | Don't |
|----|-------|
| Write the test first (Red step) | Write tests after the fact to hit a coverage number |
| Test one behavior per test | Cram multiple assertions for different behaviors into one test |
| Assert on outcomes and outputs | Assert on internal method calls or execution order |
| Use factory functions for test data | Copy-paste setup blocks across tests |
| Name tests as scenario → expected outcome | Name tests `test1`, `test2`, or `should work` |
| Test edge cases and error paths explicitly | Only test the happy path |
| Keep tests fast (milliseconds, not seconds) | Let slow I/O or network calls into unit tests |
| Use mocks/stubs for external dependencies | Mock the unit under test itself |
| Clean up state between tests | Let tests depend on execution order |

## Anti-Patterns

| Anti-Pattern | Why It Hurts | Fix |
|--------------|-------------|-----|
| **Ice cream cone** (lots of E2E, few unit tests) | Slow feedback, flaky suite, hard to diagnose failures | Invert the pyramid: many unit tests, fewer integration, minimal E2E |
| **Test the mock** | Test passes but verifies nothing real | Assert on outputs and observable side effects, not mock internals |
| **Invisible arrangement** | Shared setup in a distant beforeAll makes tests unreadable | Inline setup or use factories; each test should be readable on its own |
| **Flaky by design** | Tests depend on timing, network, or random data | Eliminate non-determinism; use fixed seeds, stubs, and controlled clocks |
| **Coverage theater** | 100% line coverage with no meaningful assertions | Focus on behavioral coverage; every test should be able to fail meaningfully |
| **Copy-paste tests** | Maintenance nightmare when the contract changes | Extract shared setup into factories; parameterize similar tests |
