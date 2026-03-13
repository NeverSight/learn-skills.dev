---
name: commit-work
description: "Review, organize, and commit pending changes. Split into logical commits, stage carefully, and write clear Conventional Commit messages. Use when the user asks to commit, stage changes, or organize work into commits."
---

# Commit work

## Goal
Make commits that are easy to review and safe to ship:
- only intended changes are included
- commits are logically scoped (split when needed)
- commit messages describe what changed and why

## Inputs to ask for (if missing)
- Single commit or multiple commits? Default to multiple small commits when there are unrelated changes.
- Any extra rules: max subject length, required scopes.

## Workflow

1) **Inspect** the working tree
   - `git status` and `git diff` (unstaged)
   - If many changes: `git diff --stat`
2) **Decide** commit boundaries (split if needed)
   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes
   - If you cannot describe the commit cleanly in one sentence, it's too big — split further
3) **Stage** only what belongs in the next commit
   - Use `git add -p` for mixed changes in one file
   - To unstage: `git restore --staged -p` or `git restore --staged <path>`
4) **Review** what will be committed
   - `git diff --cached`
   - Verify: no secrets/tokens, no debug logging, no unrelated formatting churn
5) **Describe** the staged change in 1-2 sentences before writing the message
   - "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed — go back to step 2
6) **Write** the commit message (see format below)
   - Prefer `git commit -v` for multi-line messages
7) **Verify** — run the repo's fastest relevant check (lint, unit tests, or build)
8) **Repeat** for the next commit until the working tree is clean

## Organization Rules

- Changes with their tests go in the same commit
- If 2 unrelated changes are in one file, use patch staging to organize commits
- Documentation files (README.md, Schemas.yaml, etc.) go in separate commit
- Translation files go in separate commit
- Separate dependency installation from usage (two commits)
- One commit = one responsibility

## Commit Format

Format: `type(context): description`

### Types
- **feat**: new feature
- **fix**: bug fix
- **docs**: documentation changes
- **style**: formatting, no code change
- **refactor**: code change without new feature or fix
- **perf**: performance improvement
- **test**: adding or fixing tests
- **chore**: build process or auxiliary tools

### Rules
- Context in `kebab-case` (e.g., `user-signup`)
- Optional component after context with `/` (e.g., `api/LoginService`)
- Imperative verb: "add" not "added" or "adds"
- No capital letter at start
- No period at end
- Max 100 characters
- Body (optional): what changed and why, not implementation diary
- Footer: `BREAKING CHANGE:` if applicable

## Deliverable
- The final commit message(s)
- A short summary per commit (what/why)
- The commands used to stage/review (at minimum: `git diff --cached`, plus any tests run)

## Important
- Keep messages concise and direct
