---
name: commit-jira
description: Create and execute Git commits with a required JIRA-style subject and required body. Use when the user asks to commit changes, write commit messages, or prepare a clean commit and expects a ticket-prefixed subject. Always run a pre-commit safety guard first, abort on log files or untracked high-risk binary extensions, then stage with `git add . -A`.
---

# Commit Jira

## Overview

Create safe, structured commits with deterministic checks and consistent message quality.
Run a guard before staging, then commit using a required JIRA-style subject and required body bullets.

## Path Resolution (Mandatory)

- Resolve any relative path in this skill from this skill directory, not from the caller's current working directory.
- For this skill, set `skill_dir` to the directory that contains this file (`commit-jira/SKILL.md`), then use `skill_dir/scripts/precommit_guard.py`.
- Do not search for `scripts/precommit_guard.py` at repo root.

## Workflow

1. Run safety guard:
   - `python3 <skill_dir>/scripts/precommit_guard.py`
2. Abort immediately if the guard exits non-zero.
   - Do not run `git add` or `git commit` when blocked.
3. Stage all changes only after guard passes:
   - `git add . -A`
4. Review staged changes:
   - `git diff --cached --name-only`
   - `git diff --cached --stat`
5. Ensure the user provided a ticket number (example: `JIRA-123`).
   - If missing, stop and ask the user for the ticket number.
6. Compose commit subject and body using the format rules below.
7. Execute commit:
   - `git commit -m "<subject>" -m "<body>"`

## Safety Guard Rules

Abort when any path matches one of these conditions:

1. Log-like files:
- `*.log`, `*.out`, `*.err`
- `npm-debug.log*`, `yarn-debug.log*`, `yarn-error.log*`, `pnpm-debug.log*`
- any file under a `logs/` directory

2. Untracked high-risk binary extensions:
- `.exe`, `.dll`, `.so`, `.dylib`, `.bin`, `.class`
- `.zip`, `.tar`, `.gz`, `.bz2`, `.xz`, `.7z`, `.rar`, `.jar`
- `.iso`, `.dmg`, `.db`, `.sqlite`, `.sqlite3`

If blocked, list offending files grouped by reason and request user action.
Do not auto-delete files.

## Commit Message Format

Use JIRA subject format:
- `<ticket>: <description>`
- Ticket must be provided by the user (example: `JIRA-123`).
- If no ticket is provided, return an error and ask the user for the ticket number before committing.
- Subject must describe what changed (not only intent), be imperative, and avoid trailing period.
- Keep subject concise (prefer <= 72 chars).

Require commit body:
- Provide bullet lines summarizing key changes and impact.
- Mention migration/risk notes when relevant.
- Use concise, factual bullets.

Example:

Subject:
- `JIRA-123: my important changes`

Body:
- `- Serialize refresh attempts per user session to prevent duplicate refresh calls.`
- `- Add timeout handling so failed refresh does not block subsequent requests.`
- `- Update session middleware tests for concurrent request scenarios.`

## Execution Notes

- Prefer one logical commit for the current request.
- If changes are unrelated, split into separate commits and repeat the guard + staging flow for each.
- If message quality is uncertain, summarize staged diff first, then derive subject/body.
