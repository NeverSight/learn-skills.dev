---
name: engram-testing-coverage
description: >
  TDD and coverage standards for Engram.
  Trigger: When implementing behavior changes in any package.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

Use this skill when:
- Adding new behavior
- Fixing a bug
- Refactoring logic with branch complexity

---

## TDD Loop

1. Write a failing test for the target behavior.
2. Implement the smallest code to pass.
3. Refactor while keeping tests green.
4. Add edge/error-path tests before closing.

---

## Coverage Rules

- Cover happy path + error paths + edge cases.
- Prefer deterministic tests over flaky integration paths.
- Add seams only when branches are impossible to trigger naturally.
- Keep runtime behavior unchanged when adding seams.

---

## Validation Commands

Run:

```bash
go test ./...
go test -cover ./...
```

Report package coverage and total coverage in the PR.
