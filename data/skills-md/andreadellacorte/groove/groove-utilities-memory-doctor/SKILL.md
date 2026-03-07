---
name: groove-utilities-memory-doctor
description: "Check memory backend health and configuration."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-memory-doctor

## Outcome

All memory health checks pass. User knows if the memory file structure is correctly configured and accessible.

## Acceptance Criteria

- Each check is reported with ✓ or ✗
- Each failure includes a specific remediation command
- Checks cover memory path and directory structure

## Checks (run in order)

1. `.groove/index.md` exists at git root
2. `memory:` key is present and has a valid path
3. Memory base path exists (e.g. `.groove/memory/`)
4. Memory log subdirectories exist: `daily/`, `weekly/`, `monthly/`, `git/`
5. Specs directory exists: `specs/` (used by `/groove-work-spec`)

## Remediation hints

| Failure | Remediation |
|---|---|
| `.groove/index.md` missing | `/groove config` (any skill bootstraps config) |
| Memory path missing | `/groove-utilities-memory-log-daily` (will create on first run) |
| Log subdirectory missing | `/groove-utilities-memory-log-daily` |
| Specs directory missing | `/groove-utilities-memory-install` |

## Constraints

- Report all checks even if an early one fails
- Do not attempt to fix issues — report and suggest only
