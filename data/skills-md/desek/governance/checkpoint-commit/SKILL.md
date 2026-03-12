---
name: checkpoint-commit
description: Slash command that creates governance checkpoint commits. Analyzes changes, validates .gitignore, and creates formatted checkpoint commits linked to Change Requests. Trigger with /checkpoint-commit [CR-XXXX] [summary].
license: Apache-2.0
metadata:
  copyright: Copyright Daniel Grenemark 2026
  version: "1.0"
---

# /checkpoint-commit

Creates a governance checkpoint commit to preserve work-in-progress state. Analyzes all repository changes, validates `.gitignore`, and creates a properly formatted commit linked to a Change Request.

**Usage:** `/checkpoint-commit [CR-XXXX] [summary]`

Both arguments are optional. The command will auto-detect the CR ID and generate a summary if not provided.

## Workflow

Follow these steps in order.

### Step 1: Context Detection

Determine the CR identifier:

- **If CR-ID is provided in `$ARGUMENTS`:** Use the provided CR-ID.
- **If CR-ID is NOT provided:**
  1. Check the current Git branch name for a pattern like `dev/CR-XXXX` or any branch containing `CR-` followed by digits.
  2. If not found in branch name, check the most recently modified file in `docs/cr/` using `git log --diff-filter=M -1 --name-only -- docs/cr/`.
  3. If the CR-ID is ambiguous or cannot be determined, **MUST** prompt the user for confirmation. Do NOT proceed without a confirmed CR-ID.

### Step 2: Analyze Changes

Examine all changes in the repository:

```bash
# Staged changes
git diff --staged

# Unstaged changes
git diff

# Untracked files
git ls-files --others --exclude-standard
```

- **MUST** identify all staged, unstaged, and untracked files.
- If there are **no changes** (no staged, unstaged, or untracked files), report "No changes to checkpoint" and **stop**. Do NOT create a commit.

### Step 3: Update .gitignore

Before staging, review untracked files and update `.gitignore` to exclude:

- Temporary files (`.tmp`, `.bak`, `*.log`)
- Build artifacts (`dist/`, `build/`, `node_modules/`)
- Generated content (compiled files, cache directories)
- IDE-specific files not already covered

**This step is mandatory** to prevent repository bloat. If more than 50 untracked files are detected, **MUST** confirm with the user before proceeding.

### Step 4: Write Summary

- **If summary is provided in `$ARGUMENTS`:** Use the provided summary.
- **If summary is NOT provided:** Analyze the diff output and generate a "Golden Summary" — a concise one-sentence description of the changes.

Compose the full commit message:

- **Subject line:** `checkpoint(CR-xxxx): {summary}`
- **Body:** Detailed description with bullet points explaining what changed and why.

### Step 5: Stage All Changes

```bash
git add -A
```

### Step 6: Create Checkpoint Commit

```bash
git commit -m "checkpoint(CR-xxxx): {summary}

{detailed body with bullet points}"
```

### Step 7: Report

Share the result with the user:

- The commit hash (from `git log -1 --format="%H"`)
- Summary of actions performed
- List of files included in the commit

## Safety Rules

- **MUST NOT** perform destructive Git operations: `git reset`, `git rebase`, `git commit --amend`, `git push --force`
- **MUST** preserve all work without data loss
- **MUST** ensure idempotent operations safe to run multiple times
- **MUST** validate `.gitignore` before staging

