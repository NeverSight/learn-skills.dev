---
name: groove-utilities-task-config
description: "Configure task backend settings interactively."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-task-config

## Outcome

The current task backend configuration is shown to the user, or updated based on provided arguments. After update, user is prompted to run `/groove-utilities-task-install` if the backend changed.

## Acceptance Criteria

- Current `tasks:` value is displayed with no arguments
- Backend is updated in `.groove/index.md` frontmatter when new value provided
- User is reminded to run `/groove-utilities-task-install` if backend changed

## Constraints

- Read and write `.groove/index.md` frontmatter `tasks:` key only
- Valid values: `beans`, `linear`, `github`, `none`
- Reject unknown backend values with a helpful error listing valid options
- If `.groove/index.md` does not exist, create from `skills/groove/templates/index.md` with defaults
- Do not modify any other keys in `.groove/index.md`
