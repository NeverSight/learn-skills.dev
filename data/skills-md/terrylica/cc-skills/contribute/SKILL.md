---
name: contribute
allowed-tools: Read, Write, Edit, Bash(git town:*), Bash(git remote:*), Bash(git config:*), Bash(git status:*), Bash(git log:*), Bash(git branch:*), Bash(git add:*), Bash(git commit:*), Bash(git diff:*), Bash(gh pr:*), Bash(gh api:*), Grep, Glob, AskUserQuestion, TodoWrite
argument-hint: "[feature-name] | --pr | --ship"
description: "Complete contribution workflow using git-town. Create branch → commit → PR → ship. Preflight at every step. TRIGGERS - contribute, feature branch, create PR, submit PR, git-town contribute."
---

<!-- ⛔⛔⛔ MANDATORY: READ THIS ENTIRE FILE BEFORE ANY ACTION ⛔⛔⛔ -->

# Git-Town Contribution Workflow — STOP AND READ

**This workflow guides you through a complete contribution cycle using git-town.**

## ⛔ WORKFLOW ENFORCEMENT

**YOU MUST USE GIT-TOWN COMMANDS. RAW GIT BRANCH COMMANDS ARE FORBIDDEN.**

| Step          | ✅ Correct         | ❌ Forbidden                         |
| ------------- | ------------------ | ------------------------------------ |
| Create branch | `git town hack`    | `git checkout -b`                    |
| Update branch | `git town sync`    | `git pull`, `git fetch`, `git merge` |
| Create PR     | `git town propose` | Manual GitHub UI                     |
| Merge PR      | `git town ship`    | `git merge` + `git push`             |

---

## Phase 0: Preflight — MANDATORY

### Step 0.1: Create TodoWrite

```
TodoWrite with todos:
- "[Contribute] Phase 0: Verify fork workflow is configured" | in_progress
- "[Contribute] Phase 0: Check workspace is clean" | pending
- "[Contribute] Phase 0: Sync with upstream" | pending
- "[Contribute] Phase 1: GATE - Confirm feature branch creation" | pending
- "[Contribute] Phase 1: Create feature branch with git town hack" | pending
- "[Contribute] Phase 2: Implement changes" | pending
- "[Contribute] Phase 2: Commit changes (raw git allowed here)" | pending
- "[Contribute] Phase 2: Sync branch before PR" | pending
- "[Contribute] Phase 3: GATE - Confirm PR creation" | pending
- "[Contribute] Phase 3: Create PR with git town propose" | pending
- "[Contribute] Phase 4: (Optional) Ship PR with git town ship" | pending
```

### Step 0.2: Verify Fork Workflow Configured

```bash
/usr/bin/env bash << 'VERIFY_FORK_EOF'
echo "=== FORK WORKFLOW VERIFICATION ==="

# Check remotes
ORIGIN=$(git remote get-url origin 2>/dev/null)
UPSTREAM=$(git remote get-url upstream 2>/dev/null)

if [[ -z "$UPSTREAM" ]]; then
    echo "❌ FATAL: upstream remote not configured"
    echo "Run: /git-town-workflow:fork to configure"
    exit 1
fi

echo "✅ origin: $ORIGIN"
echo "✅ upstream: $UPSTREAM"

# Check git-town config
SYNC_UPSTREAM=$(git config git-town.sync-upstream 2>/dev/null)
if [[ "$SYNC_UPSTREAM" != "true" ]]; then
    echo "⚠️ WARNING: git-town.sync-upstream is not true"
    echo "Run: git config git-town.sync-upstream true"
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

VERIFY_FORK_EOF
```

**If verification fails:**

```
AskUserQuestion with questions:
- question: "Fork workflow is not configured. Run fork setup first?"
  header: "Setup Required"
  options:
    - label: "Yes, run /git-town-workflow:fork now"
      description: "Configure fork workflow first"
    - label: "No, abort"
      description: "Cannot proceed without fork setup"
  multiSelect: false
```

### Step 0.3: Check Workspace Clean

```bash
/usr/bin/env bash -c 'git status --porcelain'
```

**If workspace has changes:**

```
AskUserQuestion with questions:
- question: "Workspace has uncommitted changes. How to proceed?"
  header: "Dirty Workspace"
  options:
    - label: "Stash changes (Recommended)"
      description: "git stash, create branch, git stash pop"
    - label: "Commit changes first"
      description: "Create commit before new branch"
    - label: "Discard changes"
      description: "WARNING: Loses uncommitted work"
    - label: "Abort"
      description: "Handle manually"
  multiSelect: false
```

### Step 0.4: Sync with Upstream

**ALWAYS sync before creating feature branch:**

```bash
git town sync
```

**If conflicts occur:**

1. Display conflict files
2. Wait for user to resolve
3. Run `git town continue`

---

## Phase 1: Create Feature Branch

### Step 1.1: GATE — Confirm Branch Creation

```
AskUserQuestion with questions:
- question: "What is the feature branch name?"
  header: "Branch Name"
  options:
    - label: "feat/{feature-name}"
      description: "Standard feature branch"
    - label: "fix/{bug-name}"
      description: "Bug fix branch"
    - label: "docs/{doc-name}"
      description: "Documentation branch"
    - label: "Enter custom name"
      description: "I'll provide the full branch name"
  multiSelect: false
```

### Step 1.2: Create Branch with git-town

**⛔ NEVER use `git checkout -b`. ALWAYS use:**

```bash
git town hack {branch-name}
```

**This command:**

1. Fetches from origin and upstream
2. Creates branch from updated main
3. Sets up tracking correctly
4. Updates parent chain

### Step 1.3: Verify Branch Created

```bash
/usr/bin/env bash << 'VERIFY_BRANCH_EOF'
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"

# Verify parent is main
git town branch
VERIFY_BRANCH_EOF
```

---

## Phase 2: Implement & Commit

### Step 2.1: Implement Changes

**User implements their changes here.**

(This phase is handled by the user or other skills)

### Step 2.2: Stage and Commit (Raw git allowed)

**Raw git IS allowed for commits:**

```bash
git add .
git commit -m "feat: description of change"
```

**Commit message format:**

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

### Step 2.3: Sync Before PR

**⛔ NEVER use `git pull` or `git push`. ALWAYS use:**

```bash
git town sync
```

**This:**

1. Pulls changes from upstream/main
2. Rebases/merges feature branch
3. Pushes to origin (your fork)

**If conflicts:**

```
AskUserQuestion with questions:
- question: "Sync encountered conflicts. What next?"
  header: "Conflicts"
  options:
    - label: "I'll resolve conflicts manually"
      description: "Fix conflicts, then run: git town continue"
    - label: "Skip conflicting changes"
      description: "Run: git town skip (may lose changes)"
    - label: "Abort sync"
      description: "Run: git town undo"
  multiSelect: false
```

---

## Phase 3: Create Pull Request

### Step 3.1: GATE — Confirm PR Creation

```
AskUserQuestion with questions:
- question: "Ready to create a pull request to upstream?"
  header: "Create PR"
  options:
    - label: "Yes, create PR to upstream"
      description: "Run: git town propose"
    - label: "No, keep working"
      description: "Continue development, create PR later"
    - label: "Create draft PR"
      description: "Create PR but mark as draft"
  multiSelect: false
```

### Step 3.2: Create PR with git-town

**⛔ NEVER create PR manually. ALWAYS use:**

```bash
git town propose
```

**This:**

1. Pushes latest changes to origin
2. Opens browser to create PR
3. Targets correct upstream repository
4. Fills in branch info

**For draft PR:**

```bash
git town propose --draft
```

### Step 3.3: Verify PR Created

```bash
/usr/bin/env bash -c 'gh pr view --json url,state,title'
```

---

## Phase 4: Ship (After PR Approved)

### Step 4.1: GATE — Confirm Ship

```
AskUserQuestion with questions:
- question: "Has your PR been approved and ready to merge?"
  header: "Ship PR"
  options:
    - label: "Yes, ship it (merge to main)"
      description: "Run: git town ship"
    - label: "Not yet, PR is pending review"
      description: "Wait for approval"
    - label: "PR was merged via GitHub UI"
      description: "Just cleanup local branches"
  multiSelect: false
```

### Step 4.2: Ship with git-town

**⛔ NEVER merge manually. ALWAYS use:**

```bash
git town ship
```

**This:**

1. Verifies PR is approved
2. Merges to main
3. Deletes feature branch (local + remote)
4. Updates local main

### Step 4.3: Post-Ship Cleanup

```bash
/usr/bin/env bash << 'CLEANUP_EOF'
echo "=== POST-SHIP STATUS ==="

# Show current branch
git branch --show-current

# Show recent commits on main
git log --oneline -5

# Verify feature branch deleted
git branch -a | grep -v "^*" | head -10

echo "✅ Ship complete"
CLEANUP_EOF
```

---

## Stacked Branches (Advanced)

### Creating Child Branches

If your feature needs to be split into smaller PRs:

```bash
# On feature branch, create child
git town append child-feature

# Creates stack:
# main
#   └── feature
#         └── child-feature
```

### Navigating Stacks

```bash
git town up      # Go to parent branch
git town down    # Go to child branch
git town branch  # Show full stack hierarchy
```

### Shipping Stacks

**Ship from bottom up:**

```bash
git town ship feature        # Ships feature first
git town ship child-feature  # Then ship child
```

---

## Error Recovery

### Undo Last git-town Command

```bash
git town undo
```

### Continue After Resolving Conflicts

```bash
git town continue
```

### Skip Conflicting Branch in Sync

```bash
git town skip
```

### Check git-town Status

```bash
git town status
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                GIT-TOWN CONTRIBUTION FLOW               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. SYNC         git town sync                          │
│                  ↓                                      │
│  2. BRANCH       git town hack feature-name             │
│                  ↓                                      │
│  3. COMMIT       git add . && git commit -m "..."       │
│                  ↓                                      │
│  4. SYNC         git town sync                          │
│                  ↓                                      │
│  5. PR           git town propose                       │
│                  ↓                                      │
│  6. SHIP         git town ship (after approval)         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  ⚠️  FORBIDDEN: git checkout -b, git pull, git merge    │
│  ✅ ALLOWED: git add, git commit, git log, git diff     │
└─────────────────────────────────────────────────────────┘
```

---

## Arguments

- `[feature-name]` - Optional: Branch name for new feature
- `--pr` - Skip to PR creation (branch already exists)
- `--ship` - Skip to ship (PR already approved)

## Examples

```bash
# Start new contribution
/git-town-workflow:contribute feat/add-dark-mode

# Create PR for existing branch
/git-town-workflow:contribute --pr

# Ship after PR approved
/git-town-workflow:contribute --ship
```

## Troubleshooting

| Issue               | Cause                     | Solution                                 |
| ------------------- | ------------------------- | ---------------------------------------- |
| Sync failed         | Merge conflicts           | Resolve conflicts, then `git town sync`  |
| Branch parent wrong | git-town config mismatch  | `git town branch` to view/fix hierarchy  |
| Propose failed      | No remote tracking branch | `git town sync` first to push            |
| Ship blocked        | Branch not on main        | Merge PR first, or use `--ignore-parent` |
| "Cannot ship"       | Uncommitted changes       | Commit or stash changes first            |
| PR already exists   | Re-running propose        | Use `--pr` flag to view existing PR      |
