---
name: task
description: "Backend-agnostic task management. Use when: (1) creating, listing, updating, or archiving tasks; (2) analysing task status; (3) setting up task backend. NOT for: memory population (use memory); session management (use memory session)."
license: MIT
allowed-tools: Bash(beans:*) Bash(gh:*) Bash(linear:*) Read Write Edit AskUserQuestion
metadata:
  author: andreadellacorte
  version: "0.1.0"
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# task

Backend-agnostic task management skill for groove. Reads backend config from `.groove/index.md` and routes all commands to the appropriate CLI or API.

## Git Root Detection

Before running any command, detect the git root:

```bash
git rev-parse --show-toplevel
```

All file paths (`.groove/index.md`, `.beans.yml`) are relative to git root.

## Commands

| Command | Description |
|---|---|
| `list` | Show active, ready tasks from configured backend |
| `create` | Create task with title, type, parent, status |
| `update` | Update task status, body, or metadata |
| `archive` | Archive all completed/scrapped tasks (user confirms) |
| `analyse` | Summarise tasks by status for closeout/daily memory |
| `install` | Install configured task backend |
| `config` | Show or update task backend configuration |

## $ARGUMENTS Routing

| $ARGUMENTS | Action |
|---|---|
| `help` | → `commands/help.md` |
| `doctor` | → `commands/doctor.md` |
| `list` | → `commands/list.md` |
| `create` | → `commands/create.md` |
| `update` | → `commands/update.md` |
| `archive` | → `commands/archive.md` |
| `analyse` | → `commands/analyse.md` |
| `install` | → `commands/install.md` |
| `config` | → `commands/config.md` |
| _(empty)_ | → `commands/help.md` |

## Bootstrap

If `.groove/index.md` does not exist at git root, create it from `skills/groove/templates/index.md` before proceeding. Ask user to confirm the defaults or provide overrides.

## File Structure

```
.groove/
└── index.md          # shared groove config (frontmatter: tasks, memory, git.*)
.beans.yml            # beans CLI config (at git root, owned by beans)
skills/task/
├── SKILL.md
├── commands/
│   ├── list.md
│   ├── create.md
│   ├── update.md
│   ├── archive.md
│   ├── analyse.md
│   ├── install.md
│   └── config.md
├── references/
│   └── backends.md
└── templates/
    └── beans-config.md
```
