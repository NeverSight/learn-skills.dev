---
name: jb-tdd
description: Use red-green-refactor to implement features and bug fixes with tests first.
---

# TDD (Red-Green-Refactor)

Use this skill whenever you need reliable, incremental implementation with test-first development.

## When to use

- Building new behavior where correctness matters
- Fixing bugs with a reproducible failing test
- Refactoring safely with behavior locked by tests
- Working in codebases where regression risk is high

## Workflow

1. **Red**
   - Write or update a test that describes the intended behavior.
   - Run tests and verify the new/changed test fails for the right reason.

2. **Green**
   - Implement the smallest possible code change to make the failing test pass.
   - Run the smallest relevant test scope first, then broader tests.

3. **Refactor**
   - Improve naming, remove duplication, simplify logic.
   - Keep behavior unchanged and run tests again.

4. **Repeat**
   - Continue in small cycles until acceptance criteria are complete.

## Guardrails

- Never skip the failing test step.
- Keep each cycle small and reviewable.
- Prefer deterministic tests over timing/network fragile tests.
- If behavior is unclear, stop and ask for clarification before coding.

## Deliverables

- Final passing tests for all new/changed behavior
- Minimal implementation changes
- Brief summary of what each red-green-refactor cycle achieved
