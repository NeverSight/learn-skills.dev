---
name: test-coverage
version: 1.1.0
description: Expand unit test coverage by targeting untested branches and edge cases. Use when users ask to "increase test coverage", "add more tests", "expand unit tests", "cover edge cases", "improve test coverage", or want to identify and fill gaps in existing test suites. Adapts to project's testing framework.
---

# Test Coverage

Expand unit test coverage by targeting untested branches and edge cases.

## Workflow

### 0. Create Feature Branch

Before making any changes:
1. Check the current branch - if already on a feature branch for this task, skip
2. Check the repo for branch naming conventions (e.g., `feat/`, `feature/`, etc.)
3. Create and switch to a new branch following the repo's convention, or fallback to: `feat/test-coverage`

### 1. Analyze Coverage

Run coverage report to identify:
- Untested branches and code paths
- Low-coverage files/functions
- Missing error handling tests

### 2. Identify Test Gaps

Review code for:
- Logical branches (if/else, switch)
- Error paths and exceptions
- Boundary values (min, max, zero, empty, null)
- Edge cases and corner cases
- State transitions and side effects

### 3. Write Tests

Use project's testing framework:
- **JavaScript/TypeScript**: Jest, Vitest, Mocha
- **Python**: pytest, unittest
- **Go**: testing, testify
- **Rust**: built-in test framework

Target scenarios:
- Error handling and exceptions
- Boundary conditions
- Null/undefined/empty inputs
- Concurrent/async edge cases

### 4. Verify Improvement

Run coverage again and confirm measurable increase.

## Guidelines

- Follow existing test patterns and naming conventions
- Present new test code blocks only
- Group related test cases logically
- Use descriptive test names that explain the scenario
