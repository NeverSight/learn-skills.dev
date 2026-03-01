---
name: check-ci
description: Check the current CI status for the active branch or PR. Shows GitHub Actions workflow results, merge conflict state, and CodeRabbit review status. Optionally triggers /fix-ci, /fix-conflict, or /fix-review for automatic repair. Use when you want to manually check CI state.
---

# Check CI Status

This skill checks the current CI status for the active branch or PR, reports GitHub Actions workflow results, merge conflict state, CodeRabbit review status, and optionally suggests automatic repair via /fix-ci, /fix-conflict, or /fix-review.

## Usage

```
/check-ci          # Show current CI status + conflict + review state
/check-ci --fix    # Show status and suggest fix commands for any issues found
/check-ci --wait   # Report if CI is still running
```

## Workflow

### Step 1: Determine Context

Get the current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

Check if a PR exists for the current branch:

```bash
gh pr view --json number,url,statusCheckRollup 2>/dev/null
```

If the command succeeds, a PR exists. Record the PR number and URL for use in subsequent steps.

### Step 2: Fetch CI Status

**If a PR exists:**

```bash
gh pr checks
```

This returns all checks associated with the PR along with their statuses.

**If no PR exists:**

```bash
gh run list --branch <branch> --limit 3 --json databaseId,status,conclusion,name,updatedAt
```

This returns the most recent workflow runs for the branch.

### Step 2b: Check Merge Conflict State

If a PR exists, check the mergeable status:

```bash
gh pr view --json mergeable,mergeStateStatus
```

Report the merge state:
- **MERGEABLE**: No conflicts
- **CONFLICTING** or mergeStateStatus=**DIRTY**: Merge conflicts exist
- **UNKNOWN**: GitHub is still computing (note this in the report)

### Step 2c: Check CodeRabbit Review Status

If a PR exists, check for CodeRabbit reviews:

```bash
gh api "repos/$(gh repo view --json nameWithOwner -q '.nameWithOwner')/pulls/$(gh pr view --json number -q '.number')/reviews" \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]")] | length'
```

If CodeRabbit reviews exist, fetch inline comment count:

```bash
gh api "repos/$(gh repo view --json nameWithOwner -q '.nameWithOwner')/pulls/$(gh pr view --json number -q '.number')/comments" \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]")] | length'
```

### Step 3: Report Status

List each check or workflow with its status:

- **pass**: The check completed successfully
- **fail**: The check failed
- **pending**: The check has not started yet
- **running**: The check is currently in progress

For **failed checks**: show the failure summary. Fetch details if needed:

```bash
gh run view <run_id> --log-failed
```

For **running checks**: show the elapsed time since the run started.

**Merge conflict state** (from Step 2b):
- If CONFLICTING/DIRTY: show "Merge Conflicts: YES — conflicts with base branch"
- If MERGEABLE: show "Merge Conflicts: None"
- If UNKNOWN: show "Merge Conflicts: Computing..."

**CodeRabbit review** (from Step 2c):
- If reviews exist: show "CodeRabbit Review: <N> inline comments"
- If no reviews: show "CodeRabbit Review: No review yet"

### Step 4: Handle `--fix` Flag

If the `--fix` flag is provided, check for issues in this priority order:

1. **Merge conflicts** (highest priority): If conflicts exist, inform: "Merge conflicts detected. Run `/fix-conflict` to attempt automatic resolution. Resolve conflicts before addressing other issues."
2. **CI failures**: If failures exist, inform: "CI failures detected. Run `/fix-ci` to attempt automatic repair."
3. **CodeRabbit comments**: If actionable review comments exist, inform: "CodeRabbit review has actionable comments. Run `/fix-review` to address them."

If multiple issues exist, list all of them with their suggested fix commands.

If the `--fix` flag is provided but no issues exist:

- Report that all checks are passing, no conflicts, and no review issues

### Step 5: Handle `--wait` Flag

If the `--wait` flag is provided and checks are still running:

1. Report that CI is still in progress
2. List which checks are running and their elapsed time
3. Suggest: "Run `/check-ci` again later to see final results, or wait for the PostToolUse hook to notify on completion."

If the `--wait` flag is provided and all checks have completed:

- Report the final status of all checks

## Error Handling

1. **gh CLI not found**: Report "The `gh` CLI is not installed. Install it from https://cli.github.com/ to use this skill."
2. **gh CLI not authenticated**: Report "The `gh` CLI is not authenticated. Run `gh auth login` to authenticate."
3. **No CI runs found**: Report "No CI runs found for branch `<branch>`. This may mean no workflows are configured, or no commits have been pushed to this branch yet."
4. **Network errors**: Report the error message from `gh` and suggest retrying.

## Examples

### Basic CI status check
```
/check-ci
```

Example output:
```
CI Status for branch: feature/my-feature
PR: #42 (https://github.com/owner/repo/pull/42)

  CI Checks:
    tests       pass     2m 30s
    lint        pass     45s
    typecheck   fail     1m 12s
    build       running  3m 10s (in progress)

  1 failed, 1 running, 2 passed out of 4 checks.

  Failed: typecheck
    error: synapse/server.py:42 - Argument of type "str" is not assignable to parameter "port" of type "int"

  Merge Conflicts: None
  CodeRabbit Review: 3 inline comments (1 bug, 2 suggestions)
```

### Check and suggest fix
```
/check-ci --fix
```

### Check if CI is still running
```
/check-ci --wait
```
