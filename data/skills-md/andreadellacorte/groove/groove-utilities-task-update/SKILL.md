---
name: groove-utilities-task-update
description: "Update an existing task in the configured backend."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-task-update

## Outcome

A task's status, body, or metadata is updated in the configured backend. Progress notes are appended without overwriting existing content. When completing a task, a resolution (Summary of Changes or Reasons for Scrapping) is written to the task body before marking done.

## Acceptance Criteria

- Specified fields are updated in backend
- Existing body content is preserved; new content is appended
- Completed tasks have a "Summary of Changes" or "Reasons for Scrapping" section in body
- User confirms before task is marked as completed or scrapped

## Constraints

- Read `tasks:` from `.groove/index.md` to determine backend
- If `tasks: none`, no-op with friendly message
- Never mark a task completed without a resolution section in the body
- Ask user to provide resolution if task body has none
- User must explicitly confirm completion — do not auto-complete
- Progress notes should be appended as dated bullets under a "Progress" section
- Backend mappings:
  - `beans`: `beans update <id> -s <status>` and `beans update <id> -d "<body>"`
  - `linear`: update issue via linear CLI or MCP
  - `github`: `gh issue edit <number> --body "<body>"` and label/close commands
