---
name: groove-utilities-memory-log-daily
description: "Write the daily memory log entry. Use at end of day to record what happened."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-memory-log-daily

## Outcome

`<memory>/daily/YYYY-MM-DD.md` is created or updated with a structured end entry. The file may already exist from daily start (start-of-day structure); if so, append the closeout sections. The file is written so that the next daily start can verify yesterday had an end.

## Acceptance Criteria

- File exists at `<memory>/daily/YYYY-MM-DD.md` after command completes
- "Done today" section contains granular multi-level bullets sourced from completed tasks and git diff
- Git section summarises commits and changed files for the day
- Tasks section shows task summary by status
- Learnings section is populated (not blank)
- Open/Next section captures carry-forward items
- If file already exists, content is updated/appended rather than overwritten

## Constraints

- Use `memory:` path from `.groove/index.md` frontmatter for base directory
- Write at daily end only — never called at daily start. File may already exist from daily start; append closeout sections rather than overwriting.
- "Done today" must be sourced from: completed tasks (date-matched) and `git diff` output — not from incomplete work
- If a completed task has no resolution in its body, ask user for a summary before writing the bullet
- Use template at `skills/groove-utilities-memory-log-daily/templates/daily.md` for file structure
- If the directory `<memory>/daily/` does not exist, create it before writing
- Vague entries ("worked on stuff") should trigger a clarification ask before writing
