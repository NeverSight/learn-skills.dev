---
name: wt-merge-pr
description: Squash-merge a GitHub PR, delete the remote and local branches, and remove the local worktree. Use after QA verification passes to land code on main and clean up.
---

# /wt:merge-pr - Merge PR and Clean Up Worktree

## Description
Squash-merges an open GitHub PR for a story branch, deletes branches, and removes the local worktree. Designed for automated use from QA completion workflows.

## Usage
```
/wt:merge-pr {STORY_ID}
/wt:merge-pr {STORY_ID} {PR_NUMBER}
```

### Examples
```
/wt:merge-pr WINT-1012
/wt:merge-pr WINT-1012 42
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `STORY_ID` | Yes | — | Story identifier (e.g., `WINT-1012`) |
| `PR_NUMBER` | No | _(discovered via gh)_ | PR number to merge. If absent, discovered from branch name. |

## What It Does

This slash command:
1. Finds the open PR for the story branch (or uses provided PR number)
2. Squash-merges the PR via GitHub
3. Deletes the remote branch (handled by `--delete-branch`)
4. Removes the local worktree
5. Cleans up the local branch reference

## Workflow

1. **Discover PR** (if `PR_NUMBER` not provided):
   ```bash
   gh pr list --head story/{STORY_ID} --state open --json number
   ```
   - If no open PR found: WARNING "No open PR for story/{STORY_ID}. Skipping merge." Continue to step 4 (worktree cleanup).

2. **Verify PR is mergeable** - Check PR status:
   ```bash
   gh pr view {PR_NUMBER} --json mergeable,state
   ```
   - If not mergeable: WARNING, attempt merge anyway (GitHub will reject if truly unmergeable).

3. **Squash-merge PR** - Merge and delete remote branch:
   ```bash
   gh pr merge {PR_NUMBER} --squash --delete-branch
   ```
   - On success: record merge result.
   - On failure: WARNING, continue to worktree cleanup.

4. **Remove local worktree** - Clean up the worktree directory:
   ```bash
   git worktree remove tree/story/{STORY_ID}
   ```
   - If fails (dirty tree): retry with `--force`
   - If still fails: WARNING, continue.

5. **Delete local branch** - Remove the local branch reference:
   ```bash
   git branch -D story/{STORY_ID}
   ```
   - May already be gone from `--delete-branch`. Ignore errors.

6. **Prune worktree metadata** - Clean up stale references:
   ```bash
   git worktree prune
   ```

## Output

After completion, always report:
```
PR MERGED AND CLEANED UP
  story_id: {STORY_ID}
  pr_number: {number}
  merge_strategy: squash
  branch_deleted: true | false
  worktree_removed: true | false
```

If no PR was found:
```
WORKTREE CLEANED UP (NO PR)
  story_id: {STORY_ID}
  pr_number: none
  merge_strategy: skipped
  branch_deleted: true | false
  worktree_removed: true | false
```

This structured output allows the calling orchestrator to parse results for CHECKPOINT.yaml and status updates.

## Error Handling

All failures are **non-blocking** — each step is independent and continues regardless of prior step outcomes.

| Error | Action |
|-------|--------|
| `gh` CLI not found | WARNING: "GitHub CLI (gh) not found. Skipping PR merge. Worktree cleanup only." |
| No open PR found | WARNING: Skip merge, proceed to worktree cleanup |
| PR merge fails | WARNING: Log error, continue to worktree cleanup |
| Worktree remove fails | WARNING: Retry with `--force`, log if still fails |
| Local branch delete fails | WARNING: Branch may already be gone, ignore |
| Not authenticated | WARNING: "gh auth required for PR merge. Skipping merge." |

## Notes

- All steps are non-blocking: a failure in any step does not prevent subsequent steps from executing
- Mirrors the fault-tolerance pattern from `/wt:finish`
- Squash merge produces a single clean commit on main
- `--delete-branch` handles remote branch deletion as part of the merge
- The worktree cleanup runs even if no PR exists (handles edge cases where PR was manually closed)
- The `gh` CLI must be installed and authenticated for PR operations
