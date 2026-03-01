---
name: groove
description: "Compound engineering workflow system. Use when: running any groove command. Routes to daily, work, task, and memory sub-commands. Use 'groove help' for overview, 'groove <skill> help' for skill-specific help."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) AskUserQuestion
metadata:
  author: andreadellacorte
  version: "0.8.8"
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove

Compound engineering workflow system. Single entry point for all groove skills.

## $ARGUMENTS Routing

| $ARGUMENTS | Action |
|---|---|
| `help` | → `commands/help.md` |
| `install` | → `commands/install.md` |
| `config` | → `commands/config.md` |
| `update` | → `commands/update.md` |
| `check` | → `commands/check.md` |
| `prime` | → `commands/prime.md` |
| `doctor` | → `commands/doctor.md` |
| `daily help` | → `skills/daily/commands/help.md` |
| `daily startup` | → `skills/daily/commands/startup.md` |
| `daily closeout` | → `skills/daily/commands/closeout.md` |
| `work help` | → `skills/work/commands/help.md` |
| `work brainstorm` | → `skills/work/commands/brainstorm.md` |
| `work plan` | → `skills/work/commands/plan.md` |
| `work work` | → `skills/work/commands/work.md` |
| `work review` | → `skills/work/commands/review.md` |
| `work compound` | → `skills/work/commands/compound.md` |
| `task help` | → `skills/task/commands/help.md` |
| `task doctor` | → `skills/task/commands/doctor.md` |
| `task list` | → `skills/task/commands/list.md` |
| `task create` | → `skills/task/commands/create.md` |
| `task update` | → `skills/task/commands/update.md` |
| `task archive` | → `skills/task/commands/archive.md` |
| `task analyse` | → `skills/task/commands/analyse.md` |
| `task install` | → `skills/task/commands/install.md` |
| `task config` | → `skills/task/commands/config.md` |
| `memory help` | → `skills/memory/commands/help.md` |
| `memory doctor` | → `skills/memory/commands/doctor.md` |
| `memory log daily` | → `skills/memory/commands/log/daily.md` |
| `memory log weekly` | → `skills/memory/commands/log/weekly.md` |
| `memory log monthly` | → `skills/memory/commands/log/monthly.md` |
| `memory log git` | → `skills/memory/commands/log/git.md` |
| `memory session start` | → `skills/memory/commands/session/start.md` |
| `memory session resume` | → `skills/memory/commands/session/resume.md` |
| `memory session end` | → `skills/memory/commands/session/end.md` |
| `memory session spec` | → `skills/memory/commands/session/spec.md` |
| `memory session doc` | → `skills/memory/commands/session/doc.md` |
| `memory session review` | → `skills/memory/commands/session/review.md` |
| `memory install` | → `skills/memory/commands/install.md` |
| _(empty)_ | → `commands/help.md` |
