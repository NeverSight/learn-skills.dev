---
name: get-task-status
description: Get only the metadata/status of a task without full details. Use when the user wants to quickly check a task's status, priority, or other metadata.
allowed-tools: Bash
---

# Get Task Status

Retrieve lightweight metadata for a specific task using the `taskmd` CLI.

## Instructions

The user's query is in `$ARGUMENTS` (a task ID like `077` or a task name/keyword).

1. Run `taskmd status $ARGUMENTS` to get the task metadata
2. Present the result to the user (includes ID, title, status, priority, effort, tags, owner, dependencies, and file path)
3. If the task is not found, suggest using `taskmd list` to find available tasks
