---
name: repo-kanban-pm
description: "Install and enforce a lightweight product-management workflow inside a code repo: feature-as-kanban boards, ROADMAP status tracking, branch/PR conventions, and an optional daily OpenClaw cron PM review. Use this skill when (1) starting work in a NEW repository/project that does not yet have a ROADMAP+feature-KANBAN system, (2) you are delegated to spin up a new project and want multi-agent coordination from day one, or (3) you are asked to fix/restructure an existing repo and introduce an organized backlog/feature tracking system. Also use when adding a daily PM audit loop (cron) to keep code + docs + PRs in sync." 
---

# Repo Kanban PM System

## What this skill does

Sets up a **multi-agent-safe** product workflow in a repo:
- `docs/roadmap/ROADMAP.md` as the portfolio status
- `docs/features/<feature>/KANBAN.md` as execution boards
- `docs/pm/bugs/` as the **bug intake + triage inbox** (linkable into KANBAN)
- Updates `AGENTS.md` to enforce the workflow
- (Optional) creates a daily OpenClaw cron job to run a PM review (includes bug triage)

## When to use this skill (decision rule)

Use `repo-kanban-pm` when you are tasked with either:

1) **Creating/spinning up a new project/repo** and multiple agents will work on it (or you want to avoid chaos later).
   - Goal: install ROADMAP + per-feature KANBAN boards immediately.

2) **Entering an existing repo to fix, refactor, or restructure it** and it *does not* have a clear feature/backlog tracking system.
   - Goal: introduce the kanban workflow so subsequent work is trackable and PRs stay aligned.

Do **not** use this skill if the repo already has an equivalent system that the team actively uses (avoid duplicating governance).

---

## Quick start

### 1) Initialize the repo workflow

Run:

```bash
bash scripts/init_repo_pm.sh /absolute/path/to/repo
```

This will:
- create `docs/pm/` with the workflow doc + template
- create `docs/pm/bugs/` with bug README + template
- add `KANBAN.md` to any existing `docs/features/*/` folders
- patch `AGENTS.md` to include the kanban rules (idempotent)

### 2) Add a daily PM cron (optional)

Run:

```bash
bash scripts/add_daily_pm_cron.sh /absolute/path/to/repo --agent persey --tz Europe/Minsk --time 10:00
```

## Operating rules (agents)

1. Pick a feature from `docs/roadmap/ROADMAP.md`
2. Create/update `docs/features/<feature>/KANBAN.md` and set status to `in-progress`
3. Create a branch: `feat/<feature-slug>-<short>`
4. PR must link the feature’s `KANBAN.md`
5. On merge: mark `KANBAN.md` as done and tick the ROADMAP checkbox

## Templates

- Workflow spec: `docs/pm/KANBAN-SYSTEM.md`
- Feature template: `docs/pm/FEATURE-KANBAN-TEMPLATE.md`

## Notes

- Keep KANBAN boards short.
- ROADMAP contains status only; do not duplicate per-task detail there.
