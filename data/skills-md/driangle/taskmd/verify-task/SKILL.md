---
name: verify-task
description: Run verification checks for a task and evaluate results. Use when the user wants to verify a task's acceptance criteria.
allowed-tools: Bash, Read, Glob, Grep
---

# Verify Task

Run a task's verification checks and evaluate the results.

## Instructions

The user's query is in `$ARGUMENTS` (a task ID like `077`).

1. **Run verification**: Execute `taskmd verify $ARGUMENTS --format json`
2. **Interpret results**:
   - For `bash` steps: report pass/fail based on the JSON output (status field)
   - For `assert` steps: read each `check` assertion and evaluate whether the current codebase satisfies it by inspecting relevant files
3. **Report overall verdict**:
   - If all bash checks passed and all assert checks are satisfied: report success
   - Otherwise: list the failures and what needs to be fixed
