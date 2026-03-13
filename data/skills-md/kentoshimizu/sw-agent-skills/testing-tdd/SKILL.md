---
name: testing-tdd
description: "Red-green-refactor workflow for test-first implementation feedback loops. Use when behavior and design must evolve safely through small increments backed by failing-then-passing tests; do not use for post-hoc test backfilling only."
---

# Testing TDD

## Overview
Use this skill to drive implementation through fast red-green-refactor cycles with explicit design feedback.

## Scope Boundaries
- Use when implementation should be guided by failing tests first.
- Typical requests:
  - `Develop a new feature with strict red-green-refactor discipline.`
  - `Reduce refactor risk with micro-cycle verification.`
  - `Use tests to shape API and domain design incrementally.`
- Do not use when:
  - Tests are added only after full implementation.
  - The primary goal is performance/load experimentation.

## Inputs
- Target behavior and constraints
- Existing test harness and coding standards
- Cycle-time and commit-granularity expectations

## Outputs
- Red-green-refactor evidence at incremental steps
- Decision record for cycle design and test scope
- Verification checklist for regression safety

## Workflow
1. Write a failing test for the smallest next behavior.
2. Implement the minimal change to pass.
3. Refactor while keeping tests green.
4. Repeat in small increments with explicit intent.
5. Publish residual risks and uncovered behaviors.

## Quality Gates
- Every implementation step is preceded by a failing test.
- Steps remain small enough for quick diagnosis and rollback.
- Refactoring preserves behavior with green evidence.
- Assumptions and unresolved risks are explicit.

## Failure Handling
- Stop when implementation proceeds without prior failing tests.
- Escalate when cycle size becomes too large for reliable feedback.

## Bundled Resources
- `references/trigger-and-examples.md`: trigger patterns, anti-patterns, and deliverable expectations.
