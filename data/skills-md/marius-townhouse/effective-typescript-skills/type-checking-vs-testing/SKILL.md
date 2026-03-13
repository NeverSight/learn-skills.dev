---
name: type-checking-vs-testing
description: Use when deciding between types and tests. Use when catching logic errors. Use when testing edge cases. Use when building test suites. Use when validating assumptions.
---

# Understand the Relationship Between Type Checking and Unit Testing

## Overview

Type checking and unit testing catch different kinds of errors. Type checking catches type mismatches at compile time. Unit testing catches logic errors and edge cases at runtime. They complement each other - types reduce the need for some tests, but can't replace tests for logic.

## When to Use This Skill

- Deciding between types and tests
- Catching logic errors
- Testing edge cases
- Building test suites
- Validating assumptions

## The Iron Rule

**Use types to catch type errors at compile time. Use tests to catch logic errors and edge cases at runtime. They complement each other.**

## Example

```typescript
// Type checking catches:
function add(a: number, b: number): number {
  return a + b;
}

add(1, '2'); // Compile error - types don't match

// Tests catch:
function divide(a: number, b: number): number {
  return a / b; // Logic error: no check for division by zero
}

// Type system can't catch this - need tests:
test('divide by zero', () => {
  expect(() => divide(1, 0)).toThrow();
});
```

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 77: Understand the Relationship Between Type Checking and Unit Testing
