---
name: git-rebase-main
description: Safely rebase the current feature branch on top of the latest origin/main. Use when preparing a branch for PR, UAT, or release.
---

# Git Rebase Main

## Purpose
Ensure the current feature branch includes all the latest changes from `main` before proceeding with code review, UAT, or release. This prevents merge conflicts and ensures tests run against the latest codebase.

## Hard Rules
### Must
- Fetch from origin before rebasing.
- Handle rebase conflicts by stopping and reporting to the user.
- Verify the branch is not `main` before rebasing.

### Must Not
- Force-push without user confirmation.
- Rebase if there are uncommitted changes.

## Actions

### 1. Pre-flight Checks
```bash
# Ensure we're not on main
current_branch=$(git branch --show-current)
if [[ "$current_branch" == "main" ]]; then
  echo "ERROR: Cannot rebase main onto itself. Switch to a feature branch first."
  exit 1
fi

# Ensure working directory is clean
if [[ -n "$(scripts/git-status.sh --porcelain)" ]]; then
  echo "ERROR: Working directory has uncommitted changes. Commit or stash them first."
  exit 1
fi
```

### 2. Fetch and Rebase
```bash
git fetch origin
git rebase origin/main
```

### 3. Handle Conflicts
If the rebase fails due to conflicts:
1. Report the conflicting files to the user.
2. Do NOT attempt to auto-resolve.
3. Wait for user to resolve and run `git rebase --continue`.

### 4. Force Push (with confirmation)
After a successful rebase, the branch history has changed. Ask the user before force-pushing:
```bash
git push --force-with-lease origin HEAD
```

## Golden Example
```bash
$ git fetch origin && git rebase origin/main
First, rewinding head to replay your work on top of it...
Applying: feat: add new formatting option
$ git push --force-with-lease origin HEAD
```
