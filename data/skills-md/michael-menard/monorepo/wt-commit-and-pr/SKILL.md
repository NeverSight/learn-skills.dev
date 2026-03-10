---
name: wt-commit-and-pr
description: Commit all changes, push to remote, and create or update a GitHub PR for a story branch. With the draft-PR-first workflow, this is primarily used for incremental pushes to existing draft PRs. Also handles legacy cases where no PR exists yet.
---

# /wt:commit-and-pr - Commit, Push, and Create/Update PR

## Description
Commits all staged changes in the current worktree, pushes to the remote, and creates a GitHub PR (or detects an existing one). Designed for automated use from workflow orchestrators.

> **Note:** With the draft-PR-first workflow (`/wt:new` creates a draft PR upfront), this skill is primarily used for incremental commit+push operations to existing draft PRs. It gracefully handles both cases: existing PRs (reports "updated") and new PRs (creates one).

## Usage
```
/wt:commit-and-pr {STORY_ID} "{STORY_TITLE}"
/wt:commit-and-pr {STORY_ID} "{STORY_TITLE}" {EVIDENCE_PATH}
```

### Examples
```
/wt:commit-and-pr WINT-1012 "Add worktree management"
/wt:commit-and-pr WINT-1012 "Add worktree management" _implementation/EVIDENCE.yaml
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `STORY_ID` | Yes | — | Story identifier (e.g., `WINT-1012`) |
| `STORY_TITLE` | Yes | — | Human-readable story title for commit message and PR |
| `EVIDENCE_PATH` | No | — | Path to EVIDENCE.yaml for AC checklist in PR body |

## What It Does

This slash command:
1. Verifies the current directory is inside the story worktree
2. Stages all changes in the worktree
3. Creates a conventional commit
4. Pushes the branch to the remote
5. Creates a new GitHub PR or detects an existing one
6. Reports the result with PR number and URL

## Workflow

1. **Verify worktree context** - Confirm current directory is inside `tree/story/{STORY_ID}` worktree. If not, attempt to locate and cd into it.

2. **Stage all changes** - Run `git add -A`. This is safe because worktrees are isolated per-story; there is no risk of staging unrelated work.

3. **Check for changes to commit** - Run `git status --porcelain`. If no staged changes exist, skip commit and push steps, proceed directly to PR check (step 5).

4. **Commit changes** - Create a conventional commit:
   ```bash
   git commit -m "feat({STORY_ID}): {STORY_TITLE}"
   ```

5. **Push to remote** - Push the branch and set upstream:
   ```bash
   git push -u origin story/{STORY_ID}
   ```

6. **Check for existing PR** - Query GitHub for an open PR on this branch:
   ```bash
   gh pr list --head story/{STORY_ID} --state open --json number,url
   ```

7. **Create or report PR**:

   **If no PR exists**: Create one:
   ```bash
   gh pr create --title "{STORY_ID}: {STORY_TITLE}" --body "..." --base main
   ```

   The PR body is built from:
   - AC checklist extracted from EVIDENCE.yaml (if `EVIDENCE_PATH` provided)
   - Default body if artifact is not available

   **If PR already exists**: Report "updated with new commits" and capture the existing PR number/URL.

## Output

After completion, always report:
```
COMMIT AND PR COMPLETE
  story_id: {STORY_ID}
  branch: story/{STORY_ID}
  commit: {short_sha}
  pr_number: {number}
  pr_url: {url}
  pr_action: created | updated
```

If no changes were committed (step 3 skip):
```
COMMIT AND PR COMPLETE
  story_id: {STORY_ID}
  branch: story/{STORY_ID}
  commit: skipped (no changes)
  pr_number: {number}
  pr_url: {url}
  pr_action: created | updated | unchanged
```

This structured output allows the calling orchestrator to parse `pr_number` and `pr_url` for CHECKPOINT.yaml.

## Error Handling

| Error | Action |
|-------|--------|
| Not in a worktree | ERROR: "Not inside story worktree. Run from tree/story/{STORY_ID}." |
| `gh` CLI not found | ERROR: "GitHub CLI (gh) is required. Install: https://cli.github.com" |
| No changes to commit | WARNING: Skip commit/push, still check/create PR |
| Push fails (no remote) | ERROR: "Push failed. Check remote configuration." |
| Push fails (rejected) | WARNING: "Push rejected. Try pulling first: git pull --rebase origin story/{STORY_ID}" |
| PR creation fails | ERROR: Report `gh` error message verbatim |
| Not authenticated | ERROR: "gh auth required. Run: gh auth login" |

## Notes

- Worktrees are isolated per-story, so `git add -A` is safe
- The commit message follows conventional commit format: `feat({STORY_ID}): {STORY_TITLE}`
- PR base branch is always `main`
- If called multiple times (e.g., after fixes), new commits are pushed and the existing PR updates automatically
- The `gh` CLI must be installed and authenticated
