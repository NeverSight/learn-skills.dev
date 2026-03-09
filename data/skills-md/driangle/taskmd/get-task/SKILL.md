---
name: get-task
description: Get details of a specific task by ID or name. Use when the user wants to view or look up a task.
allowed-tools: Bash, Read
---

# Get Task

Retrieve details of a specific task using the `taskmd` CLI.

## Instructions

The user's query is in `$ARGUMENTS` (a task ID like `077` or a task name/keyword).

1. Run `taskmd get $ARGUMENTS` to look up the task
2. If the task is not found, run `taskmd list` to show available tasks so the user can identify the right one
3. Once the task file is identified, read it with the `Read` tool to show full details
4. Present the task summary including: ID, title, status, priority, tags, and full description
