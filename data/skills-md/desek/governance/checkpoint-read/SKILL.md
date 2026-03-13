---
name: checkpoint-read
description: Slash command that reads checkpoint commit history to recover context for new sessions. Queries Git history for checkpoint commits and summarizes what was implemented, what remains, and decisions captured.
license: Apache-2.0
metadata:
  copyright: Copyright Daniel Grenemark 2026
  version: "1.0"
---

# /checkpoint-read

Reads checkpoint commit history to recover project context when starting a new session. Queries Git history for checkpoint commits created by `/checkpoint-commit`, displays the most recent relevant checkpoint details, and summarizes what was implemented, what remains, and any decisions captured — enabling seamless session continuity.

**Usage:** `/checkpoint-read`

No arguments required. The command automatically reads the most recent checkpoint commits from local Git history.

## Workflow

Follow these steps in order.

### Step 1: List Recent Checkpoints

Query Git history for checkpoint commits:

```bash
git log --oneline --decorate --grep '^checkpoint.*:' -n 25
```

- **If no results:** Report "No checkpoint commits found in this repository." and **STOP**. Proceed with the session without checkpoint context.
- **If results exist:** Display the list of recent checkpoint commits to provide an overview of checkpoint history.

### Step 2: Read Most Recent Checkpoint

Extract the SHA from the most recent (first) checkpoint in the list, then read its full details:

```bash
# Show commit stats (files changed)
git show --stat {SHA}

# Show full commit message and diff
git show {SHA}
```

Parse the commit message subject line and body for context recovery.

### Step 3: Summarize Context

Analyze the checkpoint commit message and produce a structured summary with three sections:

1. **What was implemented:** Extract completed work from the commit body bullet points and diff content.
2. **What remains:** Identify pending items, TODOs, or incomplete work mentioned in the commit message.
3. **Decisions captured:** Note any architectural or design decisions recorded in the commit message.

### Step 4: Report

Present the structured summary to the user, including:

- The checkpoint commit SHA and date for reference
- The CR identifier from the commit subject (e.g., `CR-XXXX`)
- The three-section context summary (implemented, remaining, decisions)

## Safety Rules

- **MUST NOT** perform destructive Git operations: `git reset`, `git rebase`, `git commit --amend`, `git push --force`
- **MUST NOT** create commits, modify files, or alter Git state in any way
- **MUST** be entirely read-only — only Git query commands are permitted
- **MUST** rely only on local Git operations (no network calls)
