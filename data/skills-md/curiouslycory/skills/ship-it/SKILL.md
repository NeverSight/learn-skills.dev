---
name: ship-it
description: "Automate PR creation and merging. Commits uncommitted changes, creates a PR targeting main, waits for CI/CD checks, and squash merges on success. Triggers on: ship it, ship this, create and merge pr, ship pr, merge to main."
user-invokable: true
compatibility: "Requires gh CLI authenticated with repo permissions, and git"
---

# Ship It

Automate the full PR lifecycle: commit changes, create a PR, wait for CI/CD, and squash merge into main.

## Workflow

Follow each step sequentially. Stop and report to the user if any step fails.

### Step 1: Pre-flight Checks

Run these checks before anything else. If any fail, stop and tell the user why.

1. **Branch check**: Run `git branch --show-current`. If in detached HEAD state, stop — tell the user to check out a named branch.
2. **Remote check**: Run `git remote -v`. If no remote is configured, stop — tell the user to add a remote.
3. **GitHub CLI check**: Run `gh auth status`. If not authenticated, stop — tell the user to run `gh auth login`.

Save the current branch name for later use.

### Step 2: Handle Uncommitted Changes

1. Run `git status --porcelain` to check for uncommitted changes (staged, unstaged, and untracked).
2. If the working tree is clean (no output) **and** not on `main`, skip to Step 3. If the working tree is clean **and** on `main`, stop — there is nothing to ship.
3. If there are changes, display the list of changed files and ask the user:
   - **A) Include all changes** — stage everything shown
   - **B) Select individual files** — present a numbered list and let the user pick which files to include (e.g., "1, 3, 5")
   - **C) Cancel** — abort the entire workflow
4. Stage the selected files using `git add <file1> <file2> ...` with explicit file paths. **Never use `git add -A` or `git add .`**.
5. Run `git diff --cached --stat` and `git diff --cached` to understand the changes.
6. Generate a clear, descriptive commit message based on the diff.
7. Create the commit.

### Step 2b: Create Feature Branch (if on main)

If the current branch is `main`, create a feature branch before proceeding:

1. Generate a descriptive branch name from the staged changes (e.g., `feat/add-user-validation`, `fix/null-pointer-in-parser`). Use kebab-case with a conventional prefix (`feat/`, `fix/`, `chore/`, `refactor/`, etc.).
2. Run `git checkout -b <branch-name>` to create and switch to the new branch. The commit made in Step 2 comes along automatically.
3. Save this branch name for cleanup in Step 6.

### Step 3: Push and Create PR

1. Run `git push -u origin HEAD` to push the branch to the remote.
2. Check if a PR already exists: `gh pr view --json number,url 2>/dev/null`.
   - If a PR exists, display its URL and skip to Step 4.
3. If no PR exists:
   - Review the commits with `git log main..HEAD --oneline`.
   - Generate a concise PR title (under 70 characters) and a body summarizing the changes.
   - Create the PR: `gh pr create --base main --title "<title>" --body "<body>"`.
4. Display the PR URL to the user.

### Step 4: Poll CI/CD Checks

1. Wait 10 seconds before the first check to give CI time to start.
2. Run `gh pr checks` to get check status.
3. Parse the results:
   - **All checks pass** → proceed to Step 5.
   - **Any check fails** → stop and report the failure to the user. Include the check name, status, and link. Do not proceed.
   - **Checks still pending** → wait 30 seconds, then poll again.
   - **No checks configured** (empty output) → ask the user whether to proceed with merge anyway or stop.
4. If checks are still pending after 15 minutes of polling, stop and tell the user. Provide the PR URL so they can monitor manually.

### Step 5: Squash Merge

1. Run `gh pr merge --squash --delete-branch` to squash merge and delete the remote branch.
2. If the merge fails (merge conflicts, branch protection rules, etc.), report the specific error to the user and stop.

### Step 6: Clean Up

1. Run `git checkout main`.
2. Run `git pull origin main` to get the merged changes.
3. Delete the local feature branch: `git branch -d <branch-name>` (using the branch name saved in Step 1).
4. Report success with a summary:
   - PR URL
   - Merge status
   - Branches cleaned up

## Edge Cases

- **On main with changes**: Create a feature branch automatically (Step 2b) after committing.
- **On main with no changes**: Stop — nothing to ship.
- **Detached HEAD**: Stop immediately with a message to check out a named branch.
- **PR already exists**: Use the existing PR. Skip PR creation, proceed to CI polling.
- **No CI checks configured**: Ask the user whether to merge without checks.
- **CI timeout (15 min)**: Report PR URL for manual monitoring. Do not merge.
- **Merge conflicts**: Report the error. Do not attempt to resolve automatically.
- **Branch protection rules block merge**: Report the specific error from `gh`.
- **User cancels during file selection**: Abort the entire workflow gracefully.
