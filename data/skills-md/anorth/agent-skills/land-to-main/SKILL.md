---
name: land-to-main
description: >-
  Lands a finished work branch onto the local main branch. 
  Use when the user asks to land, land to main, merge to main.
disable-model-invocation: false
---

# Land to Main

Land the current work branch onto **local `main`**. Remotes are out of scope — do not push or pull.

## Preconditions (fail fast)

1. **Not on `main`**: if `HEAD` is `main`, refuse and stop.
2. **Clean tree**: if there are uncommitted changes (staged or unstaged), stop. Do not commit as part of landing.
3. **Already landed**: if work branch and `main` point at the same commit, report that and stop (nothing to do).

## Workflow

Run these steps in order. Stop and wait for the user on any unexpected failure.

### 1. Inspect history

Review commits on the work branch that are not on `main` (`git log main..HEAD`).

- Normally land as-is.
- If any look like WIP / temporary / "fixup later" commits, **ask before continuing**. Do not squash or rewrite unless the user asks.

### 2. Rebase onto local `main`

```bash
git rebase main
```

- **Simple conflicts** (obvious one-sided or mechanical): resolve, `git add`, continue.
- **Complex or semantic conflicts**: stop, explain the conflict, wait for direction.
- Never use `git rebase -i`.

### 3. Lint and test

- Prefer the project's documented lint and test entrypoints.
- Run lint, then tests. Fail-stop on either — do not fast-forward if either fails.
- Do not run a full production build unless the project documents that as the check to use.

### 4. Fast-forward `main`

`main` is typically checked out in another worktree, so do not `git checkout main` here.

Only after lint and tests succeed:

1. Find the worktree that has `main`: `git worktree list`
2. Fast-forward that checkout to this branch tip (stay in the work-branch worktree):

```bash
git -C <main-worktree-path> merge --ff-only <work-branch-tip>
```

Use the work branch name or its SHA for `<work-branch-tip>`.

- `--ff-only` only — if FF is not possible, stop and ask (do not create a merge commit).
- If the main worktree has local changes, the merge should fail; abort and report — do not dirty-merge or stash there.
- If no worktree has `main`, you can directly `git push . HEAD:main`. Do not force push.
- Stay on the **work branch**. Do **not** delete any branches.

### 5. Verify

Confirm work branch and `main` are the same commit
(e.g. `git rev-parse HEAD` vs `git -C <main-worktree-path> rev-parse HEAD`).

### 6. Close tickets

Find the tickets the landed commits resolve (from commit messages, or the ticket this work started from).
Close each in the project's tracker; skip any that are already closed.
Leave open any ticket the work only partly addresses.

### 7. Report

Report briefly: branch name, new `main` tip (short SHA + subject), that checks passed,
and the tickets closed and left open.

## Hard rules

- Local `main` only — no remote fetch/pull/push.
- Do not commit, amend, squash, or otherwise rewrite history unless the user explicitly asks.
- Do not delete branches.
- End on the work branch, with `main` fast-forwarded to match.
- If unsure how to proceed: stop and wait for the user.
