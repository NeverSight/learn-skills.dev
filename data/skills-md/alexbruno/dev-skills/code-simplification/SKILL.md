---
name: code-simplification
description: >-
  Simplify code for human readability, clarity, and directness without
  changing behavior. Use this skill after implementing a feature, during
  refactoring, or when addressing code review feedback—especially when code feels
  over-engineered, deeply nested, or takes unnecessary detours to do simple
  things.
---

# Code Simplification

Make code **clean, direct, and easy for humans to read** while preserving exact runtime behavior. Prefer straightforward, objective implementations over clever tricks or premature abstractions.

## Core Principles

1. **Preserve Behavior Exactly**: Inputs, outputs, side effects, error semantics, and edge-case guards must remain identical. Existing tests must pass without modification.
2. **Clarity Over Cleverness (and Over Brevity)**: The goal is human comprehension, not fewer lines. Never replace readable code with cryptic one-liners, nested ternaries, or dense chains.
3. **Direct Over Indirection**: Do not take three hops to do something simple. Inline trivial single-use wrappers, pass-through helpers, and speculative abstractions that add ceremony without clarity.
4. **Chesterton's Fence**: Before deleting or rewriting code that looks redundant or defensive, understand *why* it was written (check callers, tests, comments, or `workflow/SPEC.md`).

## When to Apply

- Right after a feature or bug fix works and tests pass, to clean up rough or over-complicated implementation details.
- When functions have deep `if/else` nesting, long monolithic blocks, or unclear variable/method names.
- When `workflow/REVIEW.md` flags readability, maintainability, or over-engineering issues.

## What to Simplify

- **Flatten control flow**: Replace deep `if/else` nesting with guard clauses and early returns.
- **Remove unnecessary indirection**: Collapse pass-through functions, single-use factories, or redundant layers that hide simple operations.
- **Make logic linear and objective**: Replace convoluted state flags or roundabout transformations with direct, step-by-step code.
- **Right-size functions**: Break up overly long functions into cohesive, well-named units—only when each unit represents a clear step, not to fragment trivial code.
- **Use clear names, trim obvious noise**: Rename vague identifiers so code is self-explanatory. Remove comments that merely restate the code, while preserving non-obvious *why* comments and existing docstrings.
- **Unify genuine duplication**: When two blocks repeat the same logic, extract a single parameterized helper rather than maintaining parallel copies.

## Guardrails (What NOT to Do)

- Do **not** alter public APIs, return shapes, or error handling unless explicitly requested.
- Do **not** refactor unrelated files outside the scope of the current change.
- Do **not** remove edge-case checks (`null`, empty, boundary conditions) unless proven unreachable.

## Verification

1. Review the diff to confirm every change is simpler, cleaner, and strictly behavior-preserving.
2. Run the relevant test suite, linter, and typechecker to verify all checks pass unchanged.
