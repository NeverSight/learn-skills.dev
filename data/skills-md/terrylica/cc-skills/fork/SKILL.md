---
name: fork
allowed-tools: Read, Write, Edit, Bash(git town:*), Bash(git remote:*), Bash(git config:*), Bash(git status:*), Bash(git log:*), Bash(git branch:*), Bash(gh repo:*), Bash(gh api:*), Bash(gh auth:*), Bash(which:*), Bash(brew:*), Grep, Glob, AskUserQuestion, TodoWrite
argument-hint: "[upstream-url] | --check | --fix"
description: "Create or configure a fork workflow with git-town. Preflight checks at every step. TRIGGERS - fork repo, setup fork, git-town fork, create fork, fork workflow, upstream setup."
---

<!-- ⛔⛔⛔ MANDATORY: READ THIS ENTIRE FILE BEFORE ANY ACTION ⛔⛔⛔ -->

# Git-Town Fork Workflow — STOP AND READ

**DO NOT ACT ON ASSUMPTIONS. Read this file first.**

This is a **prescriptive, gated workflow**. Every step requires:

1. **Preflight check** - Verify preconditions
2. **User confirmation** - AskUserQuestion before action
3. **Validation** - Verify action succeeded

## ⛔ WORKFLOW PHILOSOPHY

**GIT-TOWN IS CANONICAL. RAW GIT IS FORBIDDEN FOR BRANCH OPERATIONS.**

| Operation     | ✅ Use             | ❌ Never Use            |
| ------------- | ------------------ | ----------------------- |
| Create branch | `git town hack`    | `git checkout -b`       |
| Update branch | `git town sync`    | `git pull`, `git merge` |
| Create PR     | `git town propose` | Manual web UI           |
| Merge PR      | `git town ship`    | `git merge` + push      |
| Switch branch | `git town switch`  | `git checkout`          |

**Exception**: Raw git for commits, staging, log viewing, diff (git-town doesn't replace these).

---

## Phase 0: Preflight — MANDATORY FIRST

**Execute this BEFORE any other action.**

### Step 0.1: Create TodoWrite

```
TodoWrite with todos:
- "[Fork] Phase 0: Check git-town installation" | in_progress
- "[Fork] Phase 0: Check GitHub CLI installation" | pending
- "[Fork] Phase 0: Detect current repository context" | pending
- "[Fork] Phase 0: Detect existing remotes" | pending
- "[Fork] Phase 0: Detect GitHub account(s)" | pending
- "[Fork] Phase 1: GATE - Present findings and get user confirmation" | pending
- "[Fork] Phase 2: Create fork (if needed)" | pending
- "[Fork] Phase 2: Configure remotes" | pending
- "[Fork] Phase 2: Initialize git-town" | pending
- "[Fork] Phase 3: Validate setup" | pending
- "[Fork] Phase 3: Display workflow cheatsheet" | pending
```

### Step 0.2: Check git-town Installation

```bash
/usr/bin/env bash -c 'which git-town && git-town --version'
```

**If NOT installed:**

```
AskUserQuestion with questions:
- question: "git-town is not installed. Would you like to install it now?"
  header: "Install"
  options:
    - label: "Yes, install via Homebrew (Recommended)"
      description: "Run: brew install git-town"
    - label: "No, abort workflow"
      description: "Cannot proceed without git-town"
  multiSelect: false
```

If "Yes": Run `brew install git-town`, then re-check.
If "No": **STOP. Do not proceed.**

### Step 0.3: Check GitHub CLI Installation

```bash
/usr/bin/env bash -c 'which gh && gh --version && gh auth status'
```

**If NOT installed or NOT authenticated:**

```
AskUserQuestion with questions:
- question: "GitHub CLI is required for fork operations. How to proceed?"
  header: "GitHub CLI"
  options:
    - label: "Install and authenticate (Recommended)"
      description: "Run: brew install gh && gh auth login"
    - label: "I'll handle this manually"
      description: "Provide instructions and exit"
  multiSelect: false
```

### Step 0.4: Detect Repository Context

**Run detection script BEFORE any AskUserQuestion:**

```bash
/usr/bin/env bash << 'DETECT_REPO_EOF'
echo "=== REPOSITORY DETECTION ==="

# Check if in git repo
if ! git rev-parse --git-dir &>/dev/null; then
    echo "ERROR: Not in a git repository"
    exit 1
fi

# Detect remotes
echo "--- Existing Remotes ---"
git remote -v

# Detect current branch
echo "--- Current Branch ---"
git branch --show-current

# Detect repo URL patterns
echo "--- Remote URLs ---"
ORIGIN_URL=$(git remote get-url origin 2>/dev/null || echo "NONE")
UPSTREAM_URL=$(git remote get-url upstream 2>/dev/null || echo "NONE")

echo "origin: $ORIGIN_URL"
echo "upstream: $UPSTREAM_URL"

# Parse GitHub owner/repo from URLs
if [[ "$ORIGIN_URL" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
    echo "ORIGIN_OWNER=${BASH_REMATCH[1]}"
    echo "ORIGIN_REPO=${BASH_REMATCH[2]%.git}"
fi

if [[ "$UPSTREAM_URL" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
    echo "UPSTREAM_OWNER=${BASH_REMATCH[1]}"
    echo "UPSTREAM_REPO=${BASH_REMATCH[2]%.git}"
fi

# Check git-town config
echo "--- Git-Town Config ---"
git town config 2>/dev/null || echo "git-town not configured"

DETECT_REPO_EOF
```

### Step 0.5: Detect GitHub Account(s)

```bash
/usr/bin/env bash << 'DETECT_ACCOUNT_EOF'
echo "=== GITHUB ACCOUNT DETECTION ==="

# Method 1: gh CLI auth status
echo "--- gh CLI Account ---"
GH_USER=$(gh api user --jq '.login' 2>/dev/null || echo "NONE")
echo "gh auth user: $GH_USER"

# Method 2: SSH config
echo "--- SSH Config Hosts ---"
grep -E "^Host github" ~/.ssh/config 2>/dev/null | head -5 || echo "No GitHub SSH hosts"

# Method 3: Git global config
echo "--- Git Global Config ---"
git config --global user.name 2>/dev/null || echo "No global user.name"
git config --global user.email 2>/dev/null || echo "No global user.email"

# Method 4: mise env (if available)
echo "--- mise env ---"
mise env 2>/dev/null | grep -i github || echo "No GitHub vars in mise"

DETECT_ACCOUNT_EOF
```

---

## Phase 1: GATE — Present Findings

**MANDATORY: Present ALL detection results and get explicit user confirmation.**

### Step 1.1: Synthesize Findings

Create a summary table of detected state:

| Aspect              | Detected Value | Status        |
| ------------------- | -------------- | ------------- |
| Repository          | {owner}/{repo} | ✅/❌         |
| Origin remote       | {url}          | ✅/❌         |
| Upstream remote     | {url}          | ✅/❌/MISSING |
| GitHub account      | {username}     | ✅/❌         |
| git-town configured | yes/no         | ✅/❌         |

### Step 1.2: Determine Workflow Type

```
AskUserQuestion with questions:
- question: "What fork workflow do you need?"
  header: "Workflow"
  options:
    - label: "Fresh fork - Create new fork from upstream"
      description: "You want to fork someone else's repo to contribute"
    - label: "Fix existing - Reconfigure existing fork's remotes"
      description: "Origin/upstream are misconfigured, need to fix"
    - label: "Verify only - Check current setup is correct"
      description: "Just validate, don't change anything"
  multiSelect: false
```

### Step 1.3: Confirm Remote URLs (if Fresh Fork)

```
AskUserQuestion with questions:
- question: "Confirm the upstream repository (the original you're forking FROM):"
  header: "Upstream"
  options:
    - label: "{detected_upstream_owner}/{detected_upstream_repo} (Detected)"
      description: "Detected from current remotes"
    - label: "Enter different URL"
      description: "I want to fork a different repository"
  multiSelect: false
```

### Step 1.4: Confirm Fork Destination

```
AskUserQuestion with questions:
- question: "Where should the fork be created?"
  header: "Fork Owner"
  options:
    - label: "{gh_auth_user} (Your account - Recommended)"
      description: "Fork to your personal GitHub account"
    - label: "Organization account"
      description: "Fork to a GitHub organization you have access to"
  multiSelect: false
```

### Step 1.5: Final Confirmation Gate

```
AskUserQuestion with questions:
- question: "Ready to proceed with fork setup?"
  header: "Confirm"
  options:
    - label: "Yes, create/configure fork"
      description: "Proceed with: upstream={upstream_url}, fork_owner={fork_owner}"
    - label: "No, abort"
      description: "Cancel and make no changes"
  multiSelect: false
```

**If "No, abort": STOP. Do not proceed.**

---

## Phase 2: Execute Fork Setup

### Step 2.1: Create Fork (if needed)

**Only if fork doesn't exist:**

```bash
/usr/bin/env bash -c 'gh repo fork {upstream_owner}/{upstream_repo} --clone=false --remote=false'
```

**Validate:**

```bash
/usr/bin/env bash -c 'gh repo view {fork_owner}/{repo} --json url'
```

### Step 2.2: Configure Remotes

**Set origin to fork (SSH preferred):**

```bash
git remote set-url origin git@github.com:{fork_owner}/{repo}.git
```

**Add upstream (if missing):**

```bash
git remote add upstream git@github.com:{upstream_owner}/{repo}.git
```

**Or fix upstream (if wrong):**

```bash
git remote set-url upstream git@github.com:{upstream_owner}/{repo}.git
```

### Step 2.3: Initialize git-town

```bash
/usr/bin/env bash << 'INIT_GITTOWN_EOF'
# Initialize git-town with fork settings
git town config setup

# Ensure sync-upstream is enabled
git config git-town.sync-upstream true

# Set dev-remote to origin (your fork)
git config git-town.dev-remote origin

INIT_GITTOWN_EOF
```

---

## Phase 3: Validation

### Step 3.1: Verify Remote Configuration

```bash
/usr/bin/env bash << 'VALIDATE_REMOTES_EOF'
echo "=== REMOTE VALIDATION ==="

ORIGIN=$(git remote get-url origin)
UPSTREAM=$(git remote get-url upstream)

echo "origin: $ORIGIN"
echo "upstream: $UPSTREAM"

# Validate origin points to fork owner
if [[ "$ORIGIN" =~ {fork_owner} ]]; then
    echo "✅ origin correctly points to your fork"
else
    echo "❌ origin does NOT point to your fork"
    exit 1
fi

# Validate upstream points to original
if [[ "$UPSTREAM" =~ {upstream_owner} ]]; then
    echo "✅ upstream correctly points to original repo"
else
    echo "❌ upstream does NOT point to original repo"
    exit 1
fi

VALIDATE_REMOTES_EOF
```

### Step 3.2: Verify git-town Configuration

```bash
/usr/bin/env bash -c 'git town config'
```

**Expected output should show:**

- `sync-upstream: true`
- `dev-remote: origin`

### Step 3.3: Test git-town Sync

```
AskUserQuestion with questions:
- question: "Run a test sync to verify everything works?"
  header: "Test"
  options:
    - label: "Yes, run git town sync --dry-run"
      description: "Preview what sync would do (safe)"
    - label: "Yes, run git town sync for real"
      description: "Actually sync branches"
    - label: "Skip test"
      description: "I'll test manually later"
  multiSelect: false
```

If test selected:

```bash
git town sync --dry-run  # or without --dry-run
```

### Step 3.4: Display Workflow Cheatsheet

**Always display at end:**

```markdown
## ✅ Fork Workflow Configured Successfully

### Daily Commands (USE THESE, NOT RAW GIT)

| Task                  | Command                      |
| --------------------- | ---------------------------- |
| Create feature branch | `git town hack feature-name` |
| Update all branches   | `git town sync`              |
| Create PR to upstream | `git town propose`           |
| Merge approved PR     | `git town ship`              |
| Switch branches       | `git town switch`            |

### ⚠️ FORBIDDEN (Will Break Workflow)

| ❌ Never Use           | ✅ Use Instead                     |
| ---------------------- | ---------------------------------- |
| `git checkout -b`      | `git town hack`                    |
| `git pull`             | `git town sync`                    |
| `git merge`            | `git town sync` or `git town ship` |
| `git push origin main` | `git town sync`                    |

### Quick Reference

- **Sync with upstream**: `git town sync` (automatic)
- **Create stacked branches**: `git town append child-feature`
- **Undo last git-town command**: `git town undo`
- **See branch hierarchy**: `git town branch`
```

---

## Error Handling

### If Fork Creation Fails

```
AskUserQuestion with questions:
- question: "Fork creation failed. How to proceed?"
  header: "Error"
  options:
    - label: "Retry"
      description: "Try creating the fork again"
    - label: "Fork exists - configure existing"
      description: "Fork already exists, just configure remotes"
    - label: "Abort"
      description: "Cancel and investigate manually"
  multiSelect: false
```

### If Remote Configuration Fails

Display the error and provide manual commands:

```bash
# Manual fix commands:
git remote set-url origin git@github.com:{fork_owner}/{repo}.git
git remote add upstream git@github.com:{upstream_owner}/{repo}.git
```

---

## Arguments

- `[upstream-url]` - Optional: URL of repository to fork
- `--check` - Only run validation, don't make changes
- `--fix` - Auto-fix detected issues without prompting

## Examples

```bash
# Fork a new repository
/git-town-workflow:fork https://github.com/EonLabs-Spartan/alpha-forge

# Check existing fork setup
/git-town-workflow:fork --check

# Auto-fix misconfigured remotes
/git-town-workflow:fork --fix
```

## Troubleshooting

| Issue                 | Cause                       | Solution                              |
| --------------------- | --------------------------- | ------------------------------------- |
| gh fork failed        | Already forked or no access | Use `--check` to verify existing fork |
| Permission denied     | SSH key not added to GitHub | Add SSH key or use HTTPS URL          |
| Remote already exists | Origin/upstream already set | Use `git remote set-url` to update    |
| Fork not detected     | Origin URL doesn't match    | Check `git remote -v` for mismatch    |
| Upstream sync fails   | Diverged histories          | `git town sync` to reconcile          |
| "Not a fork" error    | Repo is origin, not a fork  | Fork first via `gh repo fork`         |
