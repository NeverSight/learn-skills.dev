---
name: branch-cleanup
description: Clean up local branches after PR merges. Syncs main with origin, identifies branches with merged PRs, and proposes safe deletion. Use when the user asks to 'clean up branches', 'delete merged branches', 'sync branches', or mentions branch cleanup.
---

# Branch Cleanup

Automated workflow to sync main with origin and clean up local branches that have merged PRs.

## Quick Start

When user asks to "clean up branches" or "delete merged branches":

1. **Pre-flight checks:**
   - `git fetch origin` (update remote refs)
   - `git branch --show-current` (verify current branch)
   - If not on main: **Ask user:** "Should I switch to main? (Current: {branch})"

2. **Sync main:**
   - `git checkout main`
   - `git pull origin main --ff-only`
   - **If conflicts:** ⚠️ Stop and report "Main has conflicts. Resolve manually."

3. **List local branches:**
   - `git branch --format='%(refname:short)'`
   - Filter out: `main`, `master`, `develop`, `staging`, `production`, `archive*`
   - **If no branches:** Report "No local branches to clean up" and STOP.

4. **Check PR status for each branch:**
   - Get PR for branch: `gh pr list --head {branch} --state merged --json number,title,url`
   - **If merged PR found:** Add to cleanup list
   - **If no PR or not merged:** Skip

5. **Present cleanup list:**
   - Show table with: branch name, PR number, PR title, PR URL
   - **Ask user:** "Delete these {count} branches? (y/n)"
   - **If user declines:** STOP.

6. **Delete branches:**
   - For each approved branch:
     - `git branch -d {branch}` (safe delete)
     - **If fails with unmerged warning:** Show warning and skip
     - **If succeeds:** Report "✅ Deleted {branch}"
   - **Final summary:** "Deleted {count} branches, skipped {count} unmerged branches"

## Workflow Details

### Step 1: Pre-flight Checks

```bash
# Fetch latest remote refs
git fetch origin

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
```

**If not on main:**
- Show: "Currently on `{CURRENT_BRANCH}`. Switch to main?"
- Wait for user confirmation

**Safety:**
- Never switch branches with uncommitted changes
- Check: `git status --porcelain` (must be empty)

### Step 2: Sync Main

```bash
# Switch to main
git checkout main

# Fast-forward merge only (no conflicts)
git pull origin main --ff-only
```

**If fast-forward fails:**
- ⚠️ Stop with error: "Main branch has diverged from origin. Manual resolution required."
- Do NOT attempt merge or rebase

### Step 3: Identify Merged Branches

For each local branch:

```bash
# Get merged PR for branch
gh pr list --head {branch} --state merged --json number,title,url --limit 1
```

**Branch categories:**

| Status | Action |
|--------|--------|
| Merged PR found | Add to cleanup list |
| Open PR found | Skip (not merged) |
| No PR found | Skip (might be local work) |
| Protected branch | Skip (main, master, etc.) |

**Protected branches:**
- `main`, `master`, `develop`, `staging`, `production`
- Any branch starting with `archive` (e.g., `archive-2024`, `archive/old`)
- Any branch matching `origin/*`

### Step 4: Present Cleanup List

Format as markdown table:

```markdown
## Branches with merged PRs

| Branch | PR | Title |
|--------|-----|-------|
| fxstein/AIT-12-feature | [#45](url) | Feature implementation |
| oliver/ait-8-bugfix | [#38](url) | Fix login bug |

Total: 2 branches
```

**User prompt:**
"Delete these branches? They have merged PRs and are safe to remove. (y/n)"

### Step 5: Safe Deletion

```bash
# Safe delete (only if fully merged)
git branch -d {branch}
```

**If `git branch -d` fails:**
- Shows: "The branch '{branch}' is not fully merged."
- **Action:** Skip and report to user
- **Reason:** Prevents data loss

**Force delete (`-D`) is NEVER used automatically.**

## Edge Cases

### No Merged Branches

If no branches qualify for cleanup:
```
✅ All local branches are up to date.
No merged branches found for cleanup.
```

### Partially Merged Branches

If branch has commits not in main but PR is merged:
- `git branch -d` will fail (expected)
- Report: "⚠️ Skipped {branch}: has unmerged commits (possible rebase)"
- User can manually verify with: `git log main..{branch}`

### Archive Branches

Branches starting with `archive` are preserved:
- ❌ Skip: `archive-2024`, `archive/backup`, `archive-old-features`
- **Reason:** Archive branches contain historical work that should be manually managed

### Remote Tracking Branches

Only delete **local** branches, never remote refs:
- ✅ Delete: `fxstein/AIT-12-feature`
- ❌ Skip: `origin/fxstein/AIT-12-feature`

Use `git push origin --delete {branch}` only if user explicitly requests remote deletion.

## Error Handling

**If ANY error occurs:**
1. STOP IMMEDIATELY
2. Report the specific error
3. Show current state: branch name, operation attempted
4. WAIT for user input

**Common errors:**

| Error | Cause | Action |
|-------|-------|--------|
| "Not on main" | Current branch not main | Ask to switch |
| "Fast-forward failed" | Main diverged from origin | Stop, manual resolution |
| "gh command not found" | GitHub CLI not installed | Stop, ask user to install |
| "Branch not fully merged" | Branch has unmerged commits | Skip branch |

## Safety Guarantees

- ✅ Never force-delete (`-D`) branches
- ✅ Never delete without user confirmation
- ✅ Never modify remote branches
- ✅ Never switch branches with uncommitted changes
- ✅ Always use `--ff-only` for main sync

## Output Format

### Success

```
🔄 Syncing main with origin...
✅ Main is up to date

📋 Found 3 branches with merged PRs:
- fxstein/AIT-12-feature (PR #45)
- oliver/ait-8-bugfix (PR #38)
- fxstein/AIT-10-docs (PR #42)

🗑️  Deleting branches...
✅ Deleted fxstein/AIT-12-feature
✅ Deleted oliver/ait-8-bugfix
✅ Deleted fxstein/AIT-10-docs

✨ Cleanup complete: 3 branches deleted
```

### With Skipped Branches

```
🗑️  Deleting branches...
✅ Deleted fxstein/AIT-12-feature
⚠️  Skipped fxstein/AIT-15-wip: not fully merged
✅ Deleted oliver/ait-8-bugfix

✨ Cleanup complete: 2 deleted, 1 skipped
```

## Additional Features

### Dry Run Mode

If user asks for "preview" or "dry run":
- Execute steps 1-4 only
- Show cleanup list
- STOP before deletion

### Delete Remote Branches

If user explicitly asks to "delete remote branches too":
- After local deletion succeeds
- For each deleted branch:
  ```bash
  git push origin --delete {branch}
  ```
- Report: "✅ Deleted {branch} (local + remote)"

## Requirements

- **Git:** Version 2.0+
- **GitHub CLI (gh):** Required for PR status checks
- **Repository:** Must be a git repository with GitHub remote

## Forbidden Actions

- ❌ Never use `git branch -D` (force delete)
- ❌ Never delete branches without user confirmation
- ❌ Never modify `main`, `master`, or protected branches
- ❌ Never attempt merge/rebase to resolve conflicts
