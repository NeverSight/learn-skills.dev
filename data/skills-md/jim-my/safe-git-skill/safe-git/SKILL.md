---
name: safe-git
description: Use before starting any task, staging files, committing (including after pre-commit failures), or creating a PR — enforces safe git operations to prevent working on stale branches, amending pushed commits, working on main, and staging irrelevant files
---

# safe-git

**Announce at start:** "I'm using the safe-git skill to verify safe git operations."

## Gate 0 — Ensure workspace isolation before starting

Goal: prevent multiple agents from working in the same repository folder.

1. Detect whether you are in the main worktree or an already-isolated linked worktree:
   ```bash
   git_dir=$(git rev-parse --git-dir)
   common_dir=$(git rev-parse --git-common-dir)
   ```
2. If `git_dir` equals `common_dir` (main worktree) → create and switch to a dedicated linked worktree before any task work:
   - Ensure `.worktrees/` is in `.gitignore` before creating project-local worktrees.
   ```bash
   # Example naming convention:
   # <agent-or-ticket>-<short-task>, e.g. codex-safegit-gate0
   git worktree add .worktrees/<agent-or-ticket>-<short-task> -b <feature-branch-name>
   ```
   - Switch your active session/tool working directory to the new worktree path.
   After switching, continue to Gate 1 in that new worktree.
3. If already in a linked worktree (`git_dir` differs from `common_dir`) → continue to Gate 1.
4. After task completion and merge, clean up the linked worktree:
   ```bash
   git worktree remove .worktrees/<agent-or-ticket>-<short-task>
   ```

> **Note:** This gate is structural isolation. It does not replace branch safety checks; it enforces one active agent workspace per folder.

## Gate 1 — Before starting any work on a task

### 1a — Confirm you're on a feature branch

1. Run `git branch --show-current`
2. If result is `main` or `master` → **STOP**

   Do not proceed. Create a feature branch first:
   ```bash
   git checkout -b <descriptive-branch-name>
   ```
   Then begin work on the feature branch.

### 1b — Confirm your branch is up-to-date

1. Run `git fetch` to update remote tracking info
2. Check if an upstream is configured:
   ```bash
   git rev-parse @{u} 2>/dev/null
   ```
   If this fails (no upstream set) → branch is local-only. Skip to Gate 2.
3. Run:
   ```bash
   git log HEAD..@{u} --oneline
   ```
   - **Returns nothing** → branch is up-to-date. Proceed.
   - **Returns commits** → **WARN the user:**

     > Your local branch is behind the remote by N commit(s). Starting work now risks merge conflicts and duplicated effort.
     >
     > Recommended: pull before starting.
     > ```bash
     > git pull
     > ```
     > If you choose to proceed without pulling, inform the user of the risk.

   > **Note:** If `git log @{u}..HEAD --oneline` also returns commits, the branches have **diverged**. This requires manual resolution — do not blindly `git pull`. Warn the user explicitly and stop until they decide how to proceed.

## Gate 2 — Before staging files

1. Run `git status` and review ALL listed changes
2. Identify which files are relevant to the current task
3. Stage specific files only:
   ```bash
   git add path/to/file1 path/to/file2
   ```
   > **WARNING:** `git add .` and `git add -A` are **FORBIDDEN** — they silently include unrelated changes. Stop immediately. Do not run these commands. Explain the situation to the user.
4. Verify staged files:
   ```bash
   git diff --staged --stat
   ```
   Confirm only intended files appear. If unintended files are staged, unstage them:
   ```bash
   git restore --staged <file>
   ```

## Gate 3 — Before any commit

### If recovering from a pre-commit hook failure:

The pre-commit hook rejected the commit — **no commit was created**.
After fixing the issue, use a fresh commit:

```bash
git commit -m "your message"
```

`git commit --amend` is **FORBIDDEN** in this case. Stop immediately. Do not run this command. Explain the situation to the user. The commit you would be amending is the last *pushed* commit, not a new one.

### Before any other use of `git commit --amend`:

Run:
```bash
git log @{u}..HEAD --oneline
```

> **Note:** If this command fails with "no upstream configured" or similar error, the branch is local-only (never pushed). Amend is safe.

- **Returns commits** → amend is safe (those commits are unpushed)
- **Returns nothing** → amend is **FORBIDDEN**, all commits are already pushed. Stop immediately. Do not run this command. Explain the situation to the user.

  Use a fresh commit instead:
  ```bash
  git commit -m "your message"
  ```

## Gate 4 — Before creating a PR

1. Run `git branch --show-current`
2. If result is `main` or `master` → **STOP immediately. Do not proceed.**

   You cannot create a PR from main/master. Create a feature branch first:
   ```bash
   git checkout -b <descriptive-branch-name>
   # move your changes to the feature branch if needed
   ```

## Recommended Hook Setup

Install these hooks in each repo to add mechanical protection independent of this skill.

### pre-commit — blocks direct commits to main/master

Save to `.git/hooks/pre-commit` and run `chmod +x .git/hooks/pre-commit`:

```bash
#!/bin/bash
branch=$(git branch --show-current)
if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
  echo "ERROR: Direct commit to $branch is not allowed. Create a feature branch first."
  exit 1
fi
```

### pre-push — blocks pushing to main/master

Save to `.git/hooks/pre-push` and run `chmod +x .git/hooks/pre-push`:

```bash
#!/bin/bash
while read local_ref local_sha remote_ref remote_sha; do
  if [[ "$remote_ref" =~ refs/heads/main ]] || [[ "$remote_ref" =~ refs/heads/master ]]; then
    echo "ERROR: Pushing to main/master is blocked. Use a feature branch and PR."
    exit 1
  fi
done
exit 0
```
