---
name: groove-utilities-memory-log-git
description: "Record git activity summary in memory log."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-memory-log-git

## Outcome

`<memory>/git/YYYY-MM-DD-GIT-N.md` is created with a git summary for the current session. N is auto-incremented based on existing files for that date.

## Acceptance Criteria

- File created at `<memory>/git/YYYY-MM-DD-GIT-N.md` with correct N
- Content includes commits since midnight, git status, and diff stats
- N does not collide with existing files for the same date
- File is suitable for inclusion in the same commit it describes

## Constraints

- Use `memory:` path from `.groove/index.md` frontmatter
- Always list existing files in `<memory>/git/` before writing to determine correct N
- N starts at 1 for the first file of the day, increments for subsequent
- Git data to include:
  - `git log --since=midnight --oneline` for commits
  - `git status --short` for current state
  - `git diff --stat HEAD` for changed files summary
- Use template at `skills/groove-utilities-memory-log-git/templates/git.md` for file structure
- If no git changes since midnight, still write the file noting no changes
