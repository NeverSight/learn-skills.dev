---
name: complete-task
description: Mark a task as completed. Use when the user wants to mark a task as done or complete.
allowed-tools: Bash, Read, Edit
---

# Complete Task

Mark a task as completed using the `taskmd` CLI.

## Instructions

The user's query is in `$ARGUMENTS` (a task ID like `077`).

1. **Add a final worklog entry** (if worklogs are enabled):
   - Check `.taskmd.yaml` for `worklogs: true` -- only create worklogs if explicitly enabled; skip this step otherwise
   - Otherwise, find the worklog file at `tasks/<group>/.worklogs/<ID>.md` (or `tasks/.worklogs/<ID>.md`)
   - If a worklog exists, append a timestamped completion summary
2. **Check the workflow mode** in `.taskmd.yaml`:
   - If `workflow: pr-review` is set, use `taskmd set $ARGUMENTS --status in-review` instead of `completed` (note: in pr-review mode, tasks are completed by merging the PR, not by setting status directly)
   - Otherwise (default `solo` mode), run `taskmd set $ARGUMENTS --status completed --verify`
   - The `--verify` flag runs any verification checks defined in the task before applying the status change
   - If verification fails, report the failures to the user
3. Confirm the status change to the user
