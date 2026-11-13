---
name: verification-and-testing
description: >-
  Enforce evidence-based verification and meaningful test coverage before
  claiming any task is complete. Use this skill when writing tests, validating
  `workflow/SPEC.md` acceptance criteria, or verifying builds, linters, and
  runtime behavior after code changes.
---

# Verification & Testing

Never claim a change works, passes, or is complete without **fresh, direct verification evidence** collected after the final edit.

## Core Rule

**Evidence before completion claims.** If you did not run a check after your last change and observe its output, do not report it as passing.

## 1. Align Verification with `workflow/SPEC.md`

- Map every acceptance criterion in `workflow/SPEC.md` and the verification strategy in `workflow/PLAN.md` to a concrete check (automated test, build, lint, typecheck, or explicit runtime check).
- Treat untested acceptance criteria as incomplete work.

## 2. Write Meaningful Tests

- **Test behavior, not implementation details**: Assert observable outputs, state transitions, and side effects so tests survive safe refactoring (`code-simplification`).
- **Cover the edges**: Include boundary values, empty/null inputs, invalid states, and error paths—not just the happy path.
- **Keep tests isolated and deterministic**: Avoid shared mutable state, real network calls, or time-dependent flakiness unless explicitly testing integration boundaries.
- **Never weaken assertions**: Do not relax, skip, or mock away the core behavior under test just to make a suite green.

## 3. Execution Gate After Final Edit

Before handing off work or moving to `workflow/REVIEW.md`:

1. Run the relevant unit/integration tests, linter, typechecker, and build commands.
2. Confirm **all** executed checks pass with zero skipped or relaxed assertions.
3. Report the exact scope of what was run (e.g., full suite vs. targeted subset, any environment limitations).
