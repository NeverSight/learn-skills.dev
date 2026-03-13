---
name: git-atomic-commit
description: Split a large diff into atomic, review-friendly commits. Use when asked to "split commits", "create atomic commits", "chunk this diff", or prepare clean commit history.
---

# Git Atomic Commit

Always produce small commits where each commit has one logical purpose and passes checks.

## Required Guardrails

1. Run `git-run-checks` before the first commit and after each meaningful commit group.
2. Never mix refactor + behavior change + formatting in one commit unless unavoidable.
3. Keep commit ordering dependency-safe (prerequisites first).

## Atomic Slicing Process

1. Inspect changes with `git status --short` and `git diff`.
2. Draft commit slices by concern:
   - mechanical move/rename
   - API or schema changes
   - behavior changes
   - tests
   - docs/chore
3. Stage only one slice (`git add -p` or path-based staging).
4. Verify staged diff with `git diff --cached`.
5. Commit with a Conventional Commit message (delegate to `git-conventional-commit`).
6. Repeat until working tree is clean.

## Quality Checks per Slice

- Commit compiles and tests at least at smoke level.
- Message explains intent, not implementation trivia.
- Follow-up commits do not silently depend on unstaged files.

## Optional Helper Script

Use `./scripts/suggest-slices.sh` to get candidate commit groupings from file paths.

## Boris-Inspired Operating Rules

- Read first, code less, and edit only what is necessary.
- Keep context tight and decisions explicit.
- Prefer deterministic command sequences over ad-hoc experimentation.
- Surface assumptions and risks before finalizing each commit.

## Claude Mapping (Optional)

- Use parallel agents only for independent subproblems; merge results into one coherent commit plan.
- Keep each subagent assigned to one commit slice to avoid overlap.
