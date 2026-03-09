---
name: squash
description: Use when squash-merging a feature branch into main for linear history. Handles pre-flight checks, squash merge, commit delegation to commit, and branch cleanup.
model: sonnet
---

# Git Squash

## Pre-flight Checks

Before merging, validate the environment:

1. **Determine source branch** — use the argument if provided (`/squash feature/my-branch`), otherwise use the current branch.
2. **Verify not on main** — abort if source branch is `main`.
3. **Check for uncommitted changes** — `git status --porcelain`. If dirty, abort and suggest committing or stashing.
4. **Verify branch exists** — `git rev-parse --verify <branch>`.
5. **Verify divergence** — `git log main..<branch> --oneline`. If empty, abort — nothing to merge.

## Switch to Main

```bash
git checkout main
```

If remote `origin` exists, pull latest with `git pull --ff-only`. If ff-only fails, abort — main has diverged and needs manual resolution.

## Squash Merge

```bash
git merge --squash <branch>
```

On conflicts: `git merge --abort`, switch back to source branch, suggest `git rebase main`, stop.

## Delegate to commit

Invoke `/commit` to handle the commit. Do not write commit messages directly.

## Post-merge Verification

```bash
git log --oneline -5
git status
git diff
```

Confirm: clean working tree, squash commit at HEAD, no leftover staged changes.

## Cleanup

Try safe delete first:

```bash
git branch -d <branch>
```

If `-d` fails (expected — squash merges don't preserve ancestry), verify zero diff with `git diff main <branch>`. If empty, force-delete with `git branch -D <branch>`. If there IS a diff, stop — something was lost.

If a remote tracking branch exists (`git ls-remote --heads origin <branch>`):

```bash
git push origin --delete <branch>
```

## Rules

- **Proceed without confirmation** — pre-flight checks are the safety gate.
- Only merge into `main`.
- Always use `--squash` — never fast-forward or regular merge.
- Always delegate the commit to `/commit`.
- Abort on merge conflicts — never auto-resolve.
- Never force-push.
- Prefer `git branch -d` — use `-D` only after verifying zero diff.
- If any step fails, stop and report the error.

## Quick Reference

Pre-flight → checkout main → `git merge --squash` → `/commit` → verify → cleanup (`-d`, fall back to `-D` after zero diff check, delete remote if exists).
