---
name: pull-request-review
description: Review a pull request by branch name or URL, using a git worktree
---

# Pull Request Review

Use this skill to review a pull request given a branch name or URL.

## Input Formats

This skill accepts either:

- A branch name (e.g., `feature/add-auth`)
- A pull request URL from GitHub or GitLab (e.g., `https://github.com/owner/repo/pull/123`)

## Workflow

### Step 1: Parse Input

If given a URL, extract the pull request information:

```bash
# GitHub PR URL format: https://github.com/owner/repo/pull/123
# GitLab MR URL format: https://gitlab.com/owner/repo/-/merge_requests/123

# For GitHub, use gh CLI to get branch name
gh pr view <url-or-number> --json headRefName --jq '.headRefName'

# For GitLab, use glab CLI or parse the MR page
glab mr view <number> --output json | jq -r '.source_branch'
```

### Step 2: Determine Repository Root

Find the root of the current git repository:

```bash
git rev-parse --show-toplevel
```

### Step 3: Fetch and Verify the Branch

Fetch the branch from the remote and verify it exists:

```bash
# Fetch the specific branch
git fetch origin <branch-name>

# Verify the branch exists
if ! git rev-parse --verify "origin/<branch-name>" >/dev/null 2>&1; then
    echo "Error: Branch '<branch-name>' does not exist on the remote."
    exit 1
fi
```

If the branch does not exist, inform the user of the error and stop. Do not proceed with worktree creation or review.

### Step 4: Create Worktree

Create a worktree in a sibling directory under `worktree/`:

```bash
# From repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_PATH="${REPO_ROOT}/../worktree/<branch-name>"

# Create the worktree directory if needed
mkdir -p "${REPO_ROOT}/../worktree"

# Add the worktree
git worktree add "$WORKTREE_PATH" "origin/<branch-name>"
```

The worktree path follows the pattern `../worktree/<branch-name>` relative to the repository root.

### Step 5: Change to Worktree and Checkout Branch

Change the working directory to the new worktree and ensure the branch is checked out:

```bash
cd "$WORKTREE_PATH"

# Checkout the branch
git checkout <branch-name>

# Verify you are on the correct branch
git branch --show-current
```

Confirm the output matches the expected branch name before proceeding.

### Step 6: Set Up the Repository

Before reviewing, the repository must be properly set up. Look for developer documentation that describes how to install dependencies and prepare the codebase:

1. Search for setup instructions in these common locations:
   - `README.md`
   - `CONTRIBUTING.md`
   - `docs/` directory
   - `DEVELOPMENT.md`
   - `SETUP.md`

2. Follow the documented setup steps exactly. Common setup tasks include:
   - Installing dependencies (`npm install`, `yarn`, `pip install`, `bundle install`, etc.)
   - Setting up environment variables
   - Running database migrations
   - Building assets or compiling code

3. Do not assume the setup process. Every repository has its own conventions and requirements.

4. If no setup documentation exists, ask the user how to set up the repository before proceeding.

### Step 7: Determine Base Branch

Identify the base branch for comparison:

```bash
# For GitHub PRs
gh pr view --json baseRefName --jq '.baseRefName'

# For GitLab MRs
glab mr view --output json | jq -r '.target_branch'

# If working from branch name only, assume main or master
git branch -r | grep -E 'origin/(main|master)$' | head -1 | sed 's/.*origin\///'
```

### Step 8: Load Code Review Skill

Load and follow the `code-review` skill to perform the actual review. The code-review skill provides guidance on:

- Scope determination using git diff
- Handling pre-existing code
- Convention compliance
- Test coverage philosophy
- Review checklist

## Cleanup

After the review is complete, the worktree can be removed:

```bash
git worktree remove "$WORKTREE_PATH"
```

Inform the user that the worktree remains available for further investigation and can be removed manually when no longer needed.

## Error Handling

If any command fails during the workflow, do not retry or attempt workarounds. Stop immediately and ask the user for guidance. Common failure scenarios include:

- Branch does not exist remotely
- Worktree creation fails
- Checkout fails
- Setup commands fail
- CLI tools (gh, glab) are not available or not authenticated

Present the error output to the user and ask how they would like to proceed.
