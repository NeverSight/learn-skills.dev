---
name: manage-git-branches
description: >
  Create, track, switch, sync, and clean up Git branches. Covers
  naming conventions, safe branch switching with stash, upstream
  synchronization, and pruning merged branches. Use when starting work
  on a new feature or bug fix, switching between tasks on different
  branches, keeping a feature branch up to date with main, or cleaning
  up branches after merging pull requests.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: git
  complexity: intermediate
  language: multi
  tags: git, branches, branching-strategy, stash, remote-tracking
---

# Manage Git Branches

Create, switch, sync, and clean up branches following consistent naming conventions.

## When to Use

- Starting work on a new feature or bug fix
- Switching between tasks on different branches
- Keeping a feature branch up to date with main
- Cleaning up branches after merging pull requests
- Listing and inspecting branches

## Inputs

- **Required**: Repository with at least one commit
- **Optional**: Branch naming convention (default: `type/description`)
- **Optional**: Base branch for new branches (default: `main`)
- **Optional**: Remote name (default: `origin`)

## Procedure

### Step 1: Create a Feature Branch

Use a consistent naming convention:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New functionality | `feature/add-weighted-mean` |
| `fix/` | Bug fix | `fix/null-pointer-in-parser` |
| `docs/` | Documentation | `docs/update-api-reference` |
| `refactor/` | Code restructuring | `refactor/extract-validation` |
| `chore/` | Maintenance | `chore/update-dependencies` |
| `test/` | Test additions | `test/add-edge-case-coverage` |

```bash
# Create and switch to a new branch from main
git checkout -b feature/add-weighted-mean main

# Or using the newer switch command
git switch -c feature/add-weighted-mean main
```

**Expected:** New branch created and checked out. `git branch` shows the new branch with an asterisk.

**On failure:** If the base branch doesn't exist locally, fetch first: `git fetch origin main && git checkout -b feature/name origin/main`.

### Step 2: Track Remote Branches

Set up tracking when pushing a new branch for the first time:

```bash
# Push and set upstream tracking
git push -u origin feature/add-weighted-mean

# Check tracking relationship
git branch -vv
```

To check out a remote branch that someone else created:

```bash
git fetch origin
git checkout feature/their-branch
# Git auto-creates a local tracking branch
```

**Expected:** Local branch tracks the corresponding remote branch. `git branch -vv` shows the upstream.

**On failure:** If auto-tracking fails, set it manually: `git branch --set-upstream-to=origin/feature/name feature/name`.

### Step 3: Switch Branches Safely

Before switching, ensure the working tree is clean:

```bash
# Check for uncommitted changes
git status
```

**If changes exist**, either commit or stash them:

```bash
# Option 1: Commit work in progress
git add <files>
git commit -m "wip: save progress on validation logic"

# Option 2: Stash changes temporarily
git stash push -m "validation work in progress"

# Switch branches
git checkout main

# Later, restore stashed changes
git checkout feature/add-weighted-mean
git stash pop
```

List and manage stashes:

```bash
# List all stashes
git stash list

# Apply a specific stash (without removing it)
git stash apply stash@{1}

# Drop a stash
git stash drop stash@{0}
```

**Expected:** Branch switch succeeds. Working tree reflects the target branch's state. Stashed changes are recoverable.

**On failure:** If switch is blocked by uncommitted changes that would be overwritten, stash or commit first. `git stash` cannot stash untracked files unless you use `git stash push -u`.

### Step 4: Sync with Upstream

Keep your feature branch up to date with the base branch:

```bash
# Fetch latest changes
git fetch origin

# Rebase onto latest main (preferred — keeps linear history)
git rebase origin/main

# Or merge main into your branch (creates merge commit)
git merge origin/main
```

**Expected:** Branch now includes the latest changes from main. No conflicts, or conflicts resolved (see `resolve-git-conflicts`).

**On failure:** If rebase causes conflicts, resolve each one and `git rebase --continue`. If the conflicts are too complex, abort with `git rebase --abort` and try `git merge origin/main` instead.

### Step 5: Clean Up Merged Branches

After pull requests are merged, remove stale branches:

```bash
# Delete a local branch that has been merged
git branch -d feature/add-weighted-mean

# Delete a local branch (force, even if not merged)
git branch -D feature/abandoned-experiment

# Delete a remote branch
git push origin --delete feature/add-weighted-mean

# Prune remote-tracking references for deleted remote branches
git fetch --prune
```

**Expected:** Merged branches are removed locally and remotely. `git branch` shows only active branches.

**On failure:** `git branch -d` refuses to delete unmerged branches. If the branch was merged via squash merge on GitHub, Git may not recognize it as merged. Use `git branch -D` if you are certain the work is preserved.

### Step 6: List and Inspect Branches

```bash
# List local branches
git branch

# List all branches (local and remote)
git branch -a

# List branches with last commit info
git branch -v

# List branches merged into main
git branch --merged main

# List branches NOT yet merged
git branch --no-merged main

# See which remote branch each local branch tracks
git branch -vv
```

**Expected:** Clear view of all branches, their status, and tracking relationships.

**On failure:** If remote branches appear stale, run `git fetch --prune` to clean up references to deleted remote branches.

## Validation

- [ ] Branch names follow the agreed naming convention
- [ ] Feature branches are created from the correct base branch
- [ ] Local branches track their remote counterparts
- [ ] Merged branches are cleaned up (local and remote)
- [ ] Working tree is clean before branch switches
- [ ] Stashed changes are not left orphaned

## Common Pitfalls

- **Working on main directly**: Always create a feature branch. Committing directly to main makes it difficult to create PRs and collaborate.
- **Forgetting to fetch before branching**: Creating a branch from a stale local main means you start behind. Always `git fetch origin` first.
- **Long-lived branches**: Feature branches that live for weeks accumulate merge conflicts. Sync frequently and keep branches short-lived.
- **Orphaned stashes**: `git stash` is temporary storage. Don't rely on it for long-term work. Commit or branch instead.
- **Deleting unmerged work**: `git branch -D` is destructive. Double-check with `git log branch-name` before force-deleting.
- **Not pruning**: Remote branches deleted on GitHub still appear locally until you `git fetch --prune`.

## Related Skills

- `commit-changes` - committing work on branches
- `create-pull-request` - opening PRs from feature branches
- `resolve-git-conflicts` - handling conflicts during sync
- `configure-git-repository` - repository setup and branch strategy
