---
name: worktree-manager
description: Create alpha-forge git worktrees with auto branch naming. TRIGGERS - create worktree, new worktree, alpha-forge worktree.
allowed-tools: Bash, Read, AskUserQuestion
---

# Alpha-Forge Worktree Manager

<!-- ADR: /docs/adr/2025-12-14-alpha-forge-worktree-management.md -->

Create and manage git worktrees for the alpha-forge repository with automatic branch naming, consistent conventions, and lifecycle management.

## When to Use This Skill

Use this skill when:

- Creating a new worktree for alpha-forge development
- Setting up a worktree from a remote branch
- Using an existing local branch in a new worktree
- Managing multiple parallel feature branches

## Operational Modes

This skill supports three distinct modes based on user input:

| Mode             | User Input Example                            | Action                                |
| ---------------- | --------------------------------------------- | ------------------------------------- |
| **New Branch**   | "create worktree for sharpe validation"       | Derive slug, create branch + worktree |
| **Remote Track** | "create worktree from origin/feat/existing"   | Track remote branch in new worktree   |
| **Local Branch** | "create worktree for feat/2025-12-15-my-feat" | Use existing branch in new worktree   |

---

## Mode 1: New Branch from Description (Primary)

This is the most common workflow. User provides a natural language description, Claude derives the slug.

### Step 1: Parse Description and Derive Slug

**Claude derives kebab-case slugs following these rules:**

**Word Economy Rule**:

- Each word in slug MUST convey unique meaning
- Remove filler words: the, a, an, for, with, and, to, from, in, on, of, by
- Avoid redundancy (e.g., "database" after "ClickHouse")
- Limit to 3-5 words maximum

**Conversion Steps**:

1. Parse description from user input
2. Convert to lowercase
3. Apply word economy (remove filler words)
4. Replace spaces with hyphens

**Examples**:

| User Description                        | Derived Slug                    |
| --------------------------------------- | ------------------------------- |
| "sharpe statistical validation"         | `sharpe-statistical-validation` |
| "fix the memory leak in metrics"        | `memory-leak-metrics`           |
| "implement user authentication for API" | `user-authentication-api`       |
| "add BigQuery data source support"      | `bigquery-data-source`          |

### Step 2: Verify Main Worktree Status

**CRITICAL**: Before proceeding, check that main worktree is on `main` branch.

```bash
/usr/bin/env bash << 'GIT_EOF'
cd ~/eon/alpha-forge
CURRENT=$(git branch --show-current)
GIT_EOF
```

**If NOT on main/master**:

Use AskUserQuestion to warn user:

```yaml
question: "Main worktree is on '$CURRENT', not main. Best practice is to keep main worktree clean. Continue anyway?"
header: "Warning"
options:
  - label: "Continue anyway"
    description: "Proceed with worktree creation"
  - label: "Switch main to 'main' first"
    description: "I'll switch the main worktree to main branch before creating"
multiSelect: false
```

If user selects "Switch main to 'main' first":

```bash
cd ~/eon/alpha-forge
git checkout main
```

### Step 3: Fetch Remote and Display Branches

```bash
cd ~/eon/alpha-forge
git fetch --all --prune

# Display available branches for user reference
echo "Available remote branches:"
git branch -r | grep -v HEAD | head -20
```

### Step 4: Prompt for Branch Type

Use AskUserQuestion:

```yaml
question: "What type of branch is this?"
header: "Branch type"
options:
  - label: "feat"
    description: "New feature or capability"
  - label: "fix"
    description: "Bug fix or correction"
  - label: "refactor"
    description: "Code restructuring (no behavior change)"
  - label: "chore"
    description: "Maintenance, tooling, dependencies"
multiSelect: false
```

### Step 5: Prompt for Base Branch

Use AskUserQuestion:

```yaml
question: "Which branch should this be based on?"
header: "Base branch"
options:
  - label: "main (Recommended)"
    description: "Base from main branch"
  - label: "develop"
    description: "Base from develop branch"
multiSelect: false
```

If user needs a different branch, they can select "Other" and provide the branch name.

### Step 6: Construct Branch Name

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
TYPE="feat"           # From Step 4
DATE=$(date +%Y-%m-%d)
SLUG="sharpe-statistical-validation"  # From Step 1
BASE="main"           # From Step 5

BRANCH="${TYPE}/${DATE}-${SLUG}"
# Result: feat/2025-12-15-sharpe-statistical-validation
SKILL_SCRIPT_EOF
```

### Step 7: Create Worktree (Atomic)

```bash
/usr/bin/env bash << 'GIT_EOF_2'
cd ~/eon/alpha-forge

WORKTREE_PATH="$HOME/eon/alpha-forge.worktree-${DATE}-${SLUG}"

# Atomic branch + worktree creation
git worktree add -b "${BRANCH}" "${WORKTREE_PATH}" "origin/${BASE}"
GIT_EOF_2
```

### Step 8: Generate Tab Name and Report

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF_2'
# Generate acronym from slug
ACRONYM=$(echo "$SLUG" | tr '-' '\n' | cut -c1 | tr -d '\n')
TAB_NAME="AF-${ACRONYM}"
SKILL_SCRIPT_EOF_2
```

Report success:

```
✓ Worktree created successfully

  Path:    ~/eon/alpha-forge.worktree-2025-12-15-sharpe-statistical-validation
  Branch:  feat/2025-12-15-sharpe-statistical-validation
  Tab:     AF-ssv
  Env:     .envrc created (loads shared secrets)

  iTerm2: Restart iTerm2 to see the new tab
```

---

## Mode 2: Remote Branch Tracking

When user specifies `origin/branch-name`, create a local tracking branch.

**Detection**: User input contains `origin/` prefix.

**Example**: "create worktree from origin/feat/2025-12-10-existing-feature"

### Workflow

```bash
/usr/bin/env bash << 'GIT_EOF_3'
cd ~/eon/alpha-forge
git fetch --all --prune

REMOTE_BRANCH="origin/feat/2025-12-10-existing-feature"
LOCAL_BRANCH="feat/2025-12-10-existing-feature"

# Extract date and slug for worktree naming
# Pattern: type/YYYY-MM-DD-slug
if [[ "$LOCAL_BRANCH" =~ ^(feat|fix|refactor|chore)/([0-9]{4}-[0-9]{2}-[0-9]{2})-(.+)$ ]]; then
    DATE="${BASH_REMATCH[2]}"
    SLUG="${BASH_REMATCH[3]}"
else
    DATE=$(date +%Y-%m-%d)
    SLUG="${LOCAL_BRANCH##*/}"
fi

WORKTREE_PATH="$HOME/eon/alpha-forge.worktree-${DATE}-${SLUG}"

# Create tracking branch + worktree
git worktree add -b "${LOCAL_BRANCH}" "${WORKTREE_PATH}" "${REMOTE_BRANCH}"
GIT_EOF_3
```

---

## Mode 3: Existing Local Branch

When user specifies a local branch name (without `origin/`), use it directly.

**Detection**: User input is a valid branch name format (e.g., `feat/2025-12-15-slug`).

**Example**: "create worktree for feat/2025-12-15-my-feature"

### Workflow

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
cd ~/eon/alpha-forge

BRANCH="feat/2025-12-15-my-feature"

# Verify branch exists
if ! git show-ref --verify "refs/heads/${BRANCH}" 2>/dev/null; then
    echo "ERROR: Local branch '${BRANCH}' not found"
    echo "Available local branches:"
    git branch | head -20
    exit 1
fi

# Extract date and slug
if [[ "$BRANCH" =~ ^(feat|fix|refactor|chore)/([0-9]{4}-[0-9]{2}-[0-9]{2})-(.+)$ ]]; then
    DATE="${BASH_REMATCH[2]}"
    SLUG="${BASH_REMATCH[3]}"
else
    DATE=$(date +%Y-%m-%d)
    SLUG="${BRANCH##*/}"
fi

WORKTREE_PATH="$HOME/eon/alpha-forge.worktree-${DATE}-${SLUG}"

# Create worktree for existing branch (no -b flag)
git worktree add "${WORKTREE_PATH}" "${BRANCH}"
VALIDATE_EOF
```

---

## Naming Conventions

### Worktree Folder Naming (ADR-Style)

**Format**: `alpha-forge.worktree-YYYY-MM-DD-slug`

**Location**: `~/eon/`

| Branch                                          | Worktree Folder                                                 |
| ----------------------------------------------- | --------------------------------------------------------------- |
| `feat/2025-12-14-sharpe-statistical-validation` | `alpha-forge.worktree-2025-12-14-sharpe-statistical-validation` |
| `feat/2025-12-13-feature-genesis-skills`        | `alpha-forge.worktree-2025-12-13-feature-genesis-skills`        |
| `fix/quick-patch`                               | `alpha-forge.worktree-{TODAY}-quick-patch`                      |

### iTerm2 Tab Naming (Acronym-Based)

**Format**: `AF-{acronym}` where acronym = first character of each word in slug

| Worktree Slug                   | Tab Name   |
| ------------------------------- | ---------- |
| `sharpe-statistical-validation` | `AF-ssv`   |
| `feature-genesis-skills`        | `AF-fgs`   |
| `eth-block-metrics-data-plugin` | `AF-ebmdp` |

---

## Stale Worktree Detection

Check for worktrees whose branches are already merged to main:

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
cd ~/eon/alpha-forge

# Get branches merged to main
MERGED=$(git branch --merged main | grep -v '^\*' | grep -v 'main' | tr -d ' ')

# Check each worktree
git worktree list --porcelain | grep '^branch' | cut -d' ' -f2 | while read branch; do
    branch_name="${branch##refs/heads/}"
    if echo "$MERGED" | grep -q "^${branch_name}$"; then
        path=$(git worktree list | grep "\[${branch_name}\]" | awk '{print $1}')
        echo "STALE: $branch_name at $path"
    fi
done
PREFLIGHT_EOF
```

If stale worktrees found, prompt user to cleanup using AskUserQuestion.

---

## Cleanup Workflow

### Remove Stale Worktree

```bash
# Remove worktree (keeps branch)
git worktree remove ~/eon/alpha-forge.worktree-{DATE}-{SLUG}

# Optionally delete merged branch
git branch -d {BRANCH}
```

### Prune Orphaned Entries

```bash
git worktree prune
```

---

## Error Handling

| Scenario                 | Action                                           |
| ------------------------ | ------------------------------------------------ |
| Branch already exists    | Suggest using Mode 3 (existing branch) or rename |
| Remote branch not found  | List available remote branches                   |
| Main worktree on feature | Warn via AskUserQuestion, offer to switch        |
| Empty description        | Show usage examples                              |
| Network error on fetch   | Allow offline mode with local branches only      |
| Worktree path exists     | Suggest cleanup or different slug                |

### Branch Not Found

```
✗ Branch 'feat/nonexistent' not found

  Available branches:
  - feat/2025-12-14-sharpe-statistical-validation
  - main

  To create from remote:
  Specify: "create worktree from origin/branch-name"
```

### Worktree Already Exists

```
✗ Worktree already exists for this branch

  Existing path: ~/eon/alpha-forge.worktree-2025-12-14-sharpe-statistical-validation

  To use existing worktree:
  cd ~/eon/alpha-forge.worktree-2025-12-14-sharpe-statistical-validation
```

---

## Integration

### direnv Environment Setup

Worktrees automatically get a `.envrc` file that loads shared credentials from `~/eon/.env.alpha-forge`.

**What happens on worktree creation**:

1. Script checks if `~/eon/.env.alpha-forge` exists
2. Creates `.envrc` in the new worktree with `dotenv` directive
3. Runs `direnv allow` to approve the new `.envrc`

**Shared secrets file** (`~/eon/.env.alpha-forge`):

```bash
# ClickHouse credentials, API keys, etc.
CLICKHOUSE_HOST_READONLY="..."
CLICKHOUSE_USER_READONLY="..."
CLICKHOUSE_PASSWORD_READONLY="..."
```

**Generated `.envrc`** (in each worktree):

```bash
# alpha-forge worktree direnv config
# Auto-generated by create-worktree.sh

# Load shared alpha-forge secrets
dotenv $HOME/eon/.env.alpha-forge

# Worktree-specific overrides can be added below
```

**Prerequisites**:

- direnv installed via mise (`mise use -g direnv@latest`)
- Shell hook configured (`eval "$(direnv hook zsh)"` in `~/.zshrc`)
- Shared secrets file at `~/eon/.env.alpha-forge`

### iTerm2 Dynamic Detection

The `default-layout.py` script auto-discovers worktrees:

1. Globs `~/eon/alpha-forge.worktree-*`
2. Validates each against `git worktree list`
3. Generates `AF-{acronym}` tab names
4. Inserts tabs after main AF tab

---

## References

- [Naming Conventions](./references/naming-conventions.md)
- [ADR: Alpha-Forge Git Worktree Management](/docs/adr/2025-12-14-alpha-forge-worktree-management.md)
- [Design Spec](/docs/design/2025-12-14-alpha-forge-worktree-management/spec.md)

---

## Troubleshooting

| Issue                     | Cause                          | Solution                                        |
| ------------------------- | ------------------------------ | ----------------------------------------------- |
| Branch already exists     | Local branch with same name    | Use Mode 3 (existing branch) or rename slug     |
| Remote branch not found   | Typo or not pushed yet         | Run `git fetch --all --prune` and list branches |
| Worktree path exists      | Previous worktree not cleaned  | Remove old worktree or use different slug       |
| direnv not loading        | Shell hook not configured      | Add `eval "$(direnv hook zsh)"` to ~/.zshrc     |
| Shared secrets not found  | ~/eon/.env.alpha-forge missing | Create shared secrets file with required vars   |
| iTerm2 tab not appearing  | Dynamic layout not refreshed   | Restart iTerm2 to trigger layout regeneration   |
| Main worktree not on main | Previous work not switched     | Run `git checkout main` in main worktree first  |
| Stale worktree detected   | Branch merged but not cleaned  | Run `git worktree remove <path>` to cleanup     |
