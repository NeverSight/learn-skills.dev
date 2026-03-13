---
name: strict-tdd
description: Enforces strict Test-Driven Development — one test at a time, red-green-refactor cycle with phase-by-phase discipline
---

# Strict TDD

You follow strict Test-Driven Development. Every behavior is implemented through a red-green-refactor cycle, one test at a time.

## The Cycle

```
  RED ──────> GREEN ──────> REFACTOR ──┐
  (1 test)   (minimal code) (clean up) │
  ^                                    │
  └────────────────────────────────────┘
```

## Phase Rules

### RED — Write ONE Failing Test
- Write exactly one `it()` / `test()` block for a single behavior
- Run tests to confirm it fails
- Do NOT write any implementation code
- Do NOT write multiple tests at once

### GREEN — Make It Pass
- Write the MINIMUM code to make the failing test pass
- Do NOT add extra functionality beyond what the test requires
- Do NOT refactor or clean up yet
- Do NOT write additional tests
- Run tests to confirm ALL tests pass
- **Run quality gates** (linter, formatter, typecheck) and fix any issues

### REFACTOR — Clean Up
- Improve code quality, remove duplication, improve naming
- Do NOT add new functionality
- Do NOT write new tests
- Run tests after each change to confirm they still pass
- If no refactoring is needed, confirm tests pass and move on

## Process

1. Start in RED. Write one failing test for the next behavior.
2. Run tests. Confirm the new test fails and all other tests still pass.
3. Switch to GREEN. Write the minimal code to make it pass.
4. Run tests. Confirm ALL tests pass.
5. Run quality gates (linter, formatter, typecheck). Fix any issues.
6. Switch to REFACTOR. Clean up if needed.
7. Run tests. Confirm all tests still pass.
8. Go back to RED for the next behavior.

## Quality Gates (After GREEN)

After every GREEN phase, run these checks before moving to REFACTOR:

1. **Linter + Formatter** — `bunx biome check --write <files>`
   - Fixes formatting and linting issues automatically
   - Commit fixes if any

2. **Typecheck** — `bun run typecheck` (or project equivalent)
   - Verify no type errors in changed packages
   - Fix any type issues before proceeding

3. **All Tests Pass** — Confirm quality gate fixes didn't break tests

These gates ensure code quality is maintained throughout the TDD cycle, not just at the end.

## Rules

- Never write implementation code without a failing test first
- Never write multiple tests before implementing
- Each cycle handles exactly ONE behavior
- Run tests after every change to confirm red/green state
- **Run quality gates after every GREEN** before moving to REFACTOR
- If tests are not tested, the behavior does not exist
- Keep the green phase minimal — resist the urge to add "just one more thing"
- Refactoring means changing structure without changing behavior

## Type-Level TDD

Type-only changes (generics, constraints, narrowing) follow the same red-green-refactor cycle. The RED test for a type change is a `@ts-expect-error` directive on code the compiler should reject but doesn't yet.

1. **Red** — Write a `@ts-expect-error` on a wrong-shaped call. The directive is "unused" (the compiler doesn't error) → test fails.
2. **Green** — Tighten the type signature so the compiler rejects the call. The directive is now needed → test passes.
3. **Refactor** — Clean up types while tests stay green.

Positive type tests ("correct shape compiles") are NOT valid RED tests — loose signatures like `unknown` already accept them. Write negative tests first to drive the type constraints.

**Important:** `@ts-expect-error` tests only verify **interface signatures** (the public API). They do NOT catch type errors in the **implementation body**. After GREEN, run the project's typecheck command to ensure the implementation types are also correct. Type tests + typecheck together cover the full picture.
