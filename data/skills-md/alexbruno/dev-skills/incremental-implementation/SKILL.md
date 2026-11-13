---
name: incremental-implementation
description: >-
  Build features and refactorings in small, verified vertical slices instead of
  large unverified code dumps. Use this skill when executing `workflow/PLAN.md`
  or `workflow/TASKS.md`, modifying multiple files, or implementing changes
  expected to exceed ~100 lines.
---

# Incremental Implementation

Deliver changes in **thin, verifiable increments**—one working slice at a time. Never write an entire multi-file feature in a single unverified pass.

## Core Rule

**One slice, one verification cycle.** Do not start the next slice while the current slice has failing tests, type errors, or a broken build.

## When to Apply

- Executing steps from `workflow/PLAN.md` or tasks from `workflow/TASKS.md`.
- Any change touching two or more files or exceeding ~100 lines of code.
- Refactoring existing modules where behavior must remain intact at every step.

## The Increment Loop

For each step in `workflow/PLAN.md` (or task in `workflow/TASKS.md`):

1. **Scope the Slice**: Pick the smallest cohesive unit that delivers testable progress toward `workflow/SPEC.md`.
2. **Implement Minimally**: Write only the code required for this slice—avoid speculative scaffolding for future slices.
3. **Test & Verify Immediately**: Run targeted unit/integration tests, typecheck, and linter to confirm the slice works and introduces no regressions.
4. **Checkpoint**: Update status in `workflow/PLAN.md` or `workflow/TASKS.md` (e.g., mark `done`), and create a clean commit/checkpoint when appropriate so rollback is effortless.
5. **Repeat**: Advance to the next slice only after the current one is green.

## Slicing Strategies

Choose the slicing strategy that best fits the work:

- **Vertical Slices (Default)**: Implement one thin end-to-end capability across layers (e.g., schema -> service -> endpoint -> test) rather than building all backend files first and all frontend/test files last.
- **Risk-First Slicing**: Tackle the highest-uncertainty assumption, integration, or performance bottleneck in the earliest slice so surprises surface immediately.
- **Contract-First Slicing**: Define types, interfaces, and test assertions first, verify they compile/fail as expected, then implement the concrete behavior.

## Guardrails

- **No stacked brokenness**: Fix failing checks in the current slice before moving on.
- **Keep diffs reviewable**: If a slice grows too large, split it into smaller sub-slices before continuing.
- **Stay aligned with `SPEC.md`**: Do not add unrequested features while implementing a slice.
