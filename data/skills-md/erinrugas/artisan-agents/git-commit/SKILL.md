---
name: git-commit
description: >-
  Creates clean commits using a consistent message convention.
  Use when staging changes, composing commit messages, and preparing reviewable history.
---

# Git Commit Skill

## When to Apply
- User asks to commit current changes.
- Commit message quality/history cleanup is needed.

## Workflow
1. Review changed files and group by intent.
2. Stage only relevant files (avoid accidental unrelated changes).
3. Write commit message using project convention (or Conventional Commits by default).
4. Verify commit contains only intended changes.

## Default Message Format
- `<type>(<scope>): <summary>`
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`
