---
name: groove-utilities-task-doctor
description: "Check task backend health and connectivity."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-utilities-task-doctor

## Outcome

All task backend health checks pass. User knows if the task backend is correctly configured, installed, and reachable.

## Acceptance Criteria

- Each check is reported with ✓ or ✗
- Each failure includes a specific remediation command
- Checks cover config, CLI installation, and reachability

## Checks (run in order)

1. `.groove/index.md` exists at git root
2. `tasks:` key is present and has a valid value (`beans`, `linear`, `github`, or `none`)
3. If `tasks: none` — report no-op and exit (all green)
4. Backend CLI is installed:
   - `beans`: `beans --version`
   - `linear`: `linear --version`
   - `github`: `gh --version`
5. Backend-specific config file exists:
   - `beans`: `.beans.yml` at git root
   - `linear`: auth token configured
   - `github`: `gh auth status`
6. Backend is reachable (lightweight read operation):
   - `beans`: `beans list --json` (or equivalent)
   - `linear`: list one issue
   - `github`: `gh issue list --limit 1`
7. `AGENTS.md` contains `<!-- groove:task:start -->` section (if `tasks: beans`)

## Remediation hints

| Failure | Remediation |
|---|---|
| `.groove/index.md` missing | `/groove-utilities-task-config` or `/groove config` |
| Backend not installed | `/groove-utilities-task-install` |
| `.beans.yml` missing | `/groove-utilities-task-install` (will scaffold) |
| Backend unreachable | Check auth / network, re-run `/groove-utilities-task-install` |
| `AGENTS.md` section missing | `/groove install` |

## Constraints

- Report all checks even if an early one fails — give the full picture
- Do not attempt to fix issues — report and suggest only
- If `tasks: none`, show one green line: "tasks: none — task commands disabled" and exit
