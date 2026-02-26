---
name: pest-testing
description: >-
  Writes and maintains test suites with a project-appropriate framework.
  Use when adding or fixing unit/feature/integration/e2e tests and release gates.
---

# Testing Skill

## When to Apply
- User asks to add or fix tests.
- Changes require validation coverage.

## Workflow
1. Read test strategy from `specs/qa-spec.md` and `specs/specs.md`.
2. Detect test framework from repo (Pest, PHPUnit, Jest, Vitest, Playwright, etc.).
3. Add minimal high-value tests:
   - happy path
   - validation/edge path
   - auth/permission path when applicable
4. Run the smallest relevant test subset first, then broader suite if needed.

## Quality Bar
- Tests are deterministic.
- Assertions verify behavior, not implementation detail.
- New tests fail without the fix and pass with it.
