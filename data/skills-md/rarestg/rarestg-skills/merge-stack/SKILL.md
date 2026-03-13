---
name: merge-stack
description: Merge a linear stack of GitHub PRs into main one by one. Use when the user has multiple PRs that form a chain (each targeting the previous branch, with the bottom one targeting main) and wants to merge them all into main sequentially. Triggers on phrases like "merge the stack", "merge my PRs", "merge stacked PRs", or when the user has a numbered branch series (e.g. feature-1, feature-2, feature-3) they want merged.
disable-model-invocation: true
allowed-tools: Bash(gh *), Read, Glob, Grep
argument-hint: "[branch-prefix]"
---

# Merge Stacked PRs

Merge a linear chain of stacked PRs into `main` one at a time, re-targeting each subsequent PR to `main` before merging.

## Workflow

### 1. Discover the stack

```bash
gh pr list --state open --json number,title,headRefName,baseRefName,additions,deletions \
  --jq '.[] | "#\(.number) \(.headRefName) → \(.baseRefName) (+\(.additions) -\(.deletions))"'
```

If a branch prefix argument is provided, filter to only PRs whose branch names match it. Confirm the PRs form a single linear chain ending at `main`. Show the user the full stack (bottom to top) and get confirmation before proceeding.

### 2. Merge bottom-up

Starting with the PR that targets `main`:

1. Merge it: `gh pr merge <number> --merge`
2. For each next PR in the chain:
   a. Re-target to main: `gh pr edit <number> --base main`
   b. Merge it: `gh pr merge <number> --merge`
3. Repeat until all PRs are merged.

Use `--merge` (not `--squash` or `--rebase`) to preserve commit history, unless the user requests otherwise.

### 3. Verify

```bash
gh pr list --state open
```

Confirm zero open PRs remain (or only unrelated PRs remain) and report the result.

## Notes

- Always show the user the discovered stack and get confirmation before merging anything.
- If a merge fails (e.g. conflicts), stop and report the issue rather than continuing.
- If a merge fails because required CI checks haven't passed (common after re-targeting to `main`), suggest `gh pr merge <number> --merge --auto` to auto-merge once checks pass.
- The branch naming pattern is typically incremental (e.g. `feature-1`, `feature-2`), but detect the actual chain by following base branch references, not by name pattern.
