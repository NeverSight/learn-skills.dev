---
name: refine-tests
description: "Critically review and refine tests generated during a coding session. Use this skill when the user asks to review tests, clean up tests, refine tests, prune tests, improve test quality, or remove useless/low-value tests. Also use when the user says 'review my tests', 'clean up tests', or mentions test quality after a coding session."
---

# Refine Tests

Review all tests generated in the current session and eliminate low-value ones while strengthening the rest. The goal is a lean, high-confidence test suite — not maximum test count.

## Step 1: Identify Tests from This Session

Look at the git diff or recent file changes to find all test files created or modified in this session. Read each one fully before making judgments.

## Step 2: Prune Low-Value Tests

Remove tests that fall into these categories:

**Trivial tests** — Tests that only verify getters, setters, or basic constructors without exercising meaningful logic. If the test would pass even with a broken implementation, it's not testing anything useful.

**Weak assertions** — Tests whose assertions only check for non-null values, basic type existence, or that "no exception was thrown" without validating actual functional outcomes. A test that asserts `$result !== null` when the interesting question is *what* `$result` contains is wasting space.

**Improbable edge cases** — Tests for scenarios that don't impact core functionality or risk areas. Testing that a method handles a 10,000-character input when the UI caps it at 255 characters adds maintenance cost without meaningful protection.

**Brittle implementation tests** — Tests that are tightly coupled to internal details (exact method call counts, specific query structures, internal state). These break on every refactor and create false failures that erode trust in the test suite.

## Step 3: Refine Remaining Tests

For each test that survives pruning, check and improve:

### Meaningful Behavior
- Focus on business logic, complex workflows, integration points, and critical production paths
- Each test should answer: "What production bug would this catch?"
- Test the *behavior* the user cares about, not the implementation steps

### Effective Assertions
- Assert on end-result outcomes: expected state changes, database records, response content, side effects
- Avoid asserting on intermediate steps or internal mechanisms
- Use the most specific assertion available (`assertEquals` over `assertTrue`, `assertDatabaseHas` over checking a return value)

### Maintainability
- Clear test names that describe the scenario and expected outcome (e.g., `it_rejects_enrollment_when_course_is_full`)
- Inline factory creation so each test is self-contained and readable without scrolling to `setUp()`
- No unnecessary dependencies between tests — each test should pass in isolation
- Fast execution: avoid hitting external services; mock only at the boundary

### Project Conventions
- Follow the testing patterns established in CLAUDE.md (PHPUnit, `TenantTestCase`, inline factories)
- Use existing factory states rather than manually building model attributes
- Use `$this->faker` or `fake()` consistently with the rest of the codebase

## Step 4: Fill Gaps

After pruning, if important behaviors are left untested, suggest or write high-value tests for:
- Happy paths through critical business workflows
- Authorization and permission checks
- Error handling for likely failure modes (payment failures, validation errors, external service timeouts)
- State transitions and side effects (events dispatched, notifications sent, records created)

## Step 5: Run the Tests

Run the refined tests to confirm they pass:

```bash
php artisan test --compact <test-file>
```

If any test fails, fix it. A refined test suite that doesn't pass is worse than the original.

## Output

Summarize what you did:
- How many tests were removed and why (grouped by reason)
- What was improved in the remaining tests
- Any new tests added to cover gaps
