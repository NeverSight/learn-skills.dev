---
name: test-driven-development
description: TDD guidelines for Agent. Triggers when planning new features, implementing functionality, or making changes to existing code. Ensures tests are written as an integral part of development, not an afterthought.
---

# Test Driven Development

## Core Principle

**Tests are code, not an add-on.** Every feature, bug fix, or refactoring should include tests that verify the behavior. Writing tests is part of implementing functionality, not a separate activity done after.

## When to Use This Skill

- Planning new features or functionality
- Implementing any code change
- Fixing bugs
- Refactoring existing code

## Trigger Conditions

This skill should be active when:
1. Adding new functionality to the codebase
2. Modifying existing behavior
3. Fixing a bug
4. Changing or improving existing code

## How to Apply TDD in Agent Workflow

### Feature Implementation

1. **Understand the feature** - Read requirements or specifications
2. **Plan test cases** - Identify all behaviors to verify
3. **Write tests first** - Create tests that describe desired behavior
4. **Watch tests fail** - Verify tests fail because behavior does not exist
5. **Write minimal code** - Implement only what tests require
6. **Refactor** - Clean up while keeping tests green

### Bug Fixing

1. **Write a test that reproduces the bug**
2. **Verify the test fails**
3. **Fix the bug**
4. **Verify the test passes**

### Refactoring

1. **Ensure tests exist** for code being refactored
2. **Run tests** to establish baseline
3. **Refactor in small steps**
4. **Run tests** after each step
5. **All tests must pass** before considering refactoring complete

## Key Principles

### Tests Before Code

Write tests before writing production code. This drives cleaner design and ensures testability from the start.

### Tests as Documentation

Test names and structure should clearly describe the expected behavior. Tests serve as executable documentation.

### Minimal Test Scope

Each test should verify one behavior. This makes tests easier to understand, maintain, and debug when they fail.

## References

For detailed guidance, see:

- [TDD Principles](references/tdd-principles.md) - Three laws, Red-Green-Refactor cycle, test structure
- [Test Planning](references/test-planning.md) - How to plan tests during feature development
- [Anti-Patterns](references/anti-patterns.md) - Common mistakes to avoid
