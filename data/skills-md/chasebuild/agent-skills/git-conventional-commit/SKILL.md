---
name: git-conventional-commit
description: Create Conventional Commit messages with consistent type, scope, and body. Use when asked to write commit messages, enforce commit conventions, or improve commit history clarity.
---

# Git Conventional Commit

Write commit messages in Conventional Commits format and ensure checks passed before commit.

## Required Format

`type(scope)!: short imperative summary`

Optional body explains why and impact. Optional footer includes ticket links and breaking changes.

## Type Selection

Use this default mapping:

- `feat`: user-visible behavior or capability
- `fix`: bug fix
- `refactor`: internal change with no behavior change
- `perf`: measurable performance improvement
- `test`: test-only updates
- `docs`: documentation-only updates
- `build`: dependency/build pipeline changes
- `ci`: CI configuration changes
- `chore`: maintenance that does not fit above

See `./references/conventional-types.md` for examples.

## Process

1. Confirm `git-run-checks` passed for the staged slice.
2. Read staged diff: `git diff --cached`.
3. Pick the narrowest type and accurate scope.
4. Keep subject line under 72 chars and in imperative mood.
5. Add body only when it adds decision context.
6. Use `!` + `BREAKING CHANGE:` footer for incompatible changes.

## Optional Helper Script

Use `./scripts/compose-conventional-commit.sh` to draft a message skeleton.

## Boris-Inspired Operating Rules

- Prefer precision over verbosity.
- Explicitly state assumptions when scope is ambiguous.
- Keep semantic history clean so reviews and bisects stay fast.

## Claude Mapping (Optional)

- If project uses slash commands, expose `/commit-msg` to call the helper script.
