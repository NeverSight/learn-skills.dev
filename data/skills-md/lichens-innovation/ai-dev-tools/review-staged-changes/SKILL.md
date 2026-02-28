---
name: review-staged-changes
description: Reviews staged git changes for code quality, maintainability, readability, and potential regressions. Verifies changes make sense in context, improve maintainability, enhance readability, and don't introduce side effects. Use when reviewing staged changes, examining git diffs, or when the user asks to review modifications before committing.
---

# Review Staged Changes

Reviews staged git changes to ensure they improve code quality, maintainability, and readability without introducing regressions.

## Workflow

When reviewing staged changes:

1. **Get the staged diff**: `git diff --cached` or `git diff --staged`
2. **Analyze each change** against the four criteria below
3. **Provide structured feedback** using the template in this skill: [templates/review-summary.md](templates/review-summary.md) (relative to the skill directory)

## Review Criteria

### 1. Contextual Sense

Verify changes align with the stated purpose:

- Do the modifications address the intended goal?
- Are related changes grouped logically?
- Is the scope appropriate (not too broad, not too narrow)?
- Are any unrelated changes included that should be in a separate commit?

### 2. Regression Prevention

Identify potential breaking changes:

- **Behavior changes**: Does the code behave differently than before?
- **API changes**: Are function signatures, props, or interfaces modified?
- **Side effects**: Could changes affect other parts of the codebase?
- **Dependencies**: Are imports, dependencies, or external integrations affected?
- **Edge cases**: Are existing edge cases still handled correctly?

**Red flags:**

- Removing error handling without replacement
- Changing return types or function signatures
- Modifying shared utilities without checking usages
- Removing validation or checks
- Changing default values that other code might depend on

### 3. Maintainability & Evolvability

Assess long-term code health:

- **Structure**: Is code better organized (extracted functions, clearer modules)?
- **Complexity**: Is cyclomatic complexity reduced?
- **Coupling**: Are dependencies reduced or better managed?
- **Testability**: Is code easier to test (pure functions, dependency injection)?
- **Documentation**: Are complex parts documented?
- **Patterns**: Are established patterns followed consistently?

**Signs of improvement:**

- Extracting reusable utilities
- Reducing nested conditionals
- Breaking large functions into smaller ones
- Using consistent naming conventions
- Following project architecture patterns

### 4. Readability

Evaluate code clarity:

- **Naming**: Are variables, functions, and types clearly named?
- **Structure**: Is code flow easy to follow?
- **Comments**: Are comments helpful (explain "why", not "what")?
- **Formatting**: Is code consistently formatted?
- **Magic numbers**: Are constants extracted and named?

**Signs of improvement:**

- More descriptive variable names
- Reduced nesting levels
- Clearer control flow
- Better type annotations
- Consistent code style

## Common Patterns to Check

### Refactoring Patterns

**Good refactoring:**

- Extract function → Verify all call sites updated
- Rename variable → Verify all references updated
- Move code → Verify imports and dependencies updated

**Risky refactoring:**

- Changing shared utilities without checking all usages
- Modifying type definitions without updating consumers
- Removing "unused" code that might be used dynamically

### Code Quality Improvements

**Verify improvements are real:**

- Not just moving code around
- Actually reducing complexity
- Actually improving readability
- Making code more testable, not just prettier

### Readability Improvements

**Ensure clarity gains:**

- Names are actually more descriptive
- Structure is genuinely easier to follow
- Comments add value, not noise

## When to Flag Issues

Flag changes if:

- **Critical**: Changes break existing functionality or introduce bugs
- **Warning**: Changes might cause issues or reduce maintainability
- **Suggestion**: Changes could be improved but aren't problematic

Provide specific examples from the diff when flagging issues.
