---
name: tdd
description: WHEN working in TDD Red-Green-Refactor; NOT ad-hoc coding; write tests first, add minimal code to green, then assess refactoring.
---

# TDD Best Practices

Test-Driven Development with behavior-focused testing, factory patterns, and the Red-Green-Refactor cycle.

## Core Principle

**Every single line of production code must be written in response to a failing test.**

This is non-negotiable. If you're typing production code without a failing test demanding it, you're not doing TDD.

## The Sacred Cycle: Red → Green → Refactor

### 1. RED - Write a Failing Test

Write a test that describes the desired behavior. The test must fail because the behavior doesn't exist yet.

**Rules:**

- Start with the simplest behavior
- Test ONE thing at a time
- Focus on business behavior, not implementation
- Use descriptive test names that document intent
- Use factory functions for test data

### 2. GREEN - Minimal Implementation

Write the **minimum** code to make the test pass. Nothing more.

**Rules:**

- Only enough code to pass the current test
- Resist "just in case" logic
- No speculative features
- If writing more than needed, STOP and question why

### 3. REFACTOR - Assess and Improve

With tests green, assess whether refactoring would add value.

**Rules:**

- Commit working code FIRST
- External APIs stay unchanged
- All tests must still pass
- Commit refactoring separately
- Not all code needs refactoring - if clean, move on

## Quick Reference

| Topic                                                            | Guide                                                   |
| ---------------------------------------------------------------- | ------------------------------------------------------- |
| Red-Green-Refactor examples with step-by-step workflows          | [workflow-examples.md](references/workflow-examples.md) |
| Factory functions, composition, test organization, 100% coverage | [test-factories.md](references/test-factories.md)       |
| Critical violations, high priority issues, style improvements    | [violations.md](references/violations.md)               |
| Behavior testing patterns, test naming, and organization         | [patterns.md](references/patterns.md)                   |

## When to Use Each Guide

### Workflow Examples

Use [workflow-examples.md](references/workflow-examples.md) when you need:

- Complete TDD workflow examples (free shipping, payment validation)
- Step-by-step RED-GREEN-REFACTOR cycles
- When to refactor vs when to move on
- Refactoring assessment criteria
- Refactoring rules (commit first, preserve API, etc.)

### Test Factories

Use [test-factories.md](references/test-factories.md) when you need:

- Factory function patterns with overrides
- Why factories beat let/beforeEach
- Composing factories for complex data
- Test organization by behavior
- No 1:1 mapping between tests and implementation
- Achieving 100% coverage through behavior testing

### Violations

Use [violations.md](references/violations.md) when you need:

- Critical violations reference (production code without test, etc.)
- High priority issues (let/beforeEach, testing privates, etc.)
- Style issues (large files, duplication, magic values)
- Behavior vs implementation examples
- Quality gates checklist

### Patterns

Use [patterns.md](references/patterns.md) when you need:

- Behavior-focused testing examples
- Testing through public APIs only
- Factory patterns with schema validation
- Composing factories for complex data
- Descriptive test naming patterns
- Test organization by business behavior

## Quick Reference: Decision Trees

### Should I write this code?

```
Is there a failing test demanding this code?
├── Yes → Write minimal code to pass
└── No → Write the failing test first
```

### Is my test good?

```
Does the test verify a business outcome?
├── Yes → Does it use the public API only?
│   ├── Yes → Does it use factory functions?
│   │   ├── Yes → Good test ✓
│   │   └── No → Refactor to use factories
│   └── No → Rewrite to avoid internals
└── No → Rewrite to focus on behavior
```

### Should I refactor?

```
Are all tests green?
├── Yes → Is the code already clean?
│   ├── Yes → Commit and move on
│   └── No → Commit first, then refactor
└── No → Make tests pass first
```

### How much code should I write?

```
Does this code make the current failing test pass?
├── Yes → Is there any code that could be removed
│         and tests still pass?
│   ├── Yes → Remove it
│   └── No → Done, commit
└── No → Keep writing minimal code
```

## Summary Checklist

Before committing, verify:

- [ ] All production code has a test that demanded it
- [ ] Tests verify behavior, not implementation
- [ ] Implementation is minimal (only what's needed)
- [ ] Refactoring assessment completed
- [ ] All tests pass
- [ ] Factory functions used (no `let`/`beforeEach`)
- [ ] Test names describe business behavior
- [ ] Edge cases covered
- [ ] Tests use public API only
- [ ] No testing of implementation details
- [ ] Test organization reflects business features
- [ ] 100% coverage achieved through behavior testing
