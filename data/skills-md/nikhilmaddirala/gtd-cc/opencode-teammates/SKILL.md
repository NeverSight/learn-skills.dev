---
name: opencode-teammates
description: Team-based OpenCode orchestration via local skill scripts. Create teams, spawn teammates, assign tasks, exchange inbox messages, and run shutdown plus health checks.
---

# opencode-teammates

## Overview

Local skill-based alternative to Claude Teams MCP. It preserves the operational model using script-driven state in `~/.claude/teams` and `~/.claude/tasks`.

Current scope is intentionally simple: teammates are opencode-only and are driven through `opencode serve` HTTP APIs.

## Sub-skills

Load the matching sub-skill from `sub-skills/` based on user intent.

- `create-team.md`: initialize or delete team state
- `spawn-teammate.md`: create teammate records, seed inbox instructions, and start runtime (headless default, optional tmux TUI)
- `assign-task.md`: create and update tasks with dependency-safe transitions
- `message.md`: direct and broadcast inbox messaging
- `shutdown.md`: graceful shutdown request and teammate cleanup
- `status.md`: team health, orphan detection, and repair guidance

## Process

- determine user intent
- load the matching sub-skill
- execute script commands from `scripts/`
- validate state changes with `scripts/doctor.py`
- always report a visibility snapshot to the user after each operation:
  - `./scripts/team.py show --team <team>`
  - `./scripts/tasks.py list --team <team>`
  - `./scripts/inbox.py read --team <team> --agent team-lead --unread-only --no-mark-read`
  - `./scripts/doctor.py check --team <team>`

## State model

- team config: `~/.claude/teams/<team>/config.json`
- inboxes: `~/.claude/teams/<team>/inboxes/*.json`
- tasks: `~/.claude/tasks/<team>/*.json`

## Guardrails

- never mutate JSON by hand when scripts can do it
- keep one source of truth on disk
- run atomic writes through scripts
- prefer graceful shutdown before force kill

## Quick command map

- `./scripts/team.py create --team demo --description "..."`
- `./scripts/team.py set-anchor --team demo --window-id @6`
- `./scripts/spawn.sh --team demo --name worker-1 --prompt "..."`
- `./scripts/tasks.py create --team demo --subject "..." --description "..."`
- `./scripts/inbox.py read --team demo --agent team-lead --unread-only`
- `./scripts/lead.py sync-done --team demo --from-agent worker-1 --summary worker_done --task-id 1`
- `./scripts/lead.py status-report --team demo --max-messages 10`
- `./scripts/doctor.py check --team demo`

## Runtime requirements

- run `opencode serve` before spawning teammates
- set `OPENCODE_SERVER_URL` if your serve instance is not `http://127.0.0.1:4098`
- teammate spawn defaults to headless runtime; use `--runtime tui` for interactive panes
