---
name: memory
description: "Daily/weekly/monthly/git log population and session context management. Use when: (1) writing daily closeout log; (2) rolling up weekly/monthly memory; (3) recording git summary; (4) starting/ending sessions; (5) creating specs or docs. NOT for: task management (use task); compound loop (use work)."
license: MIT
allowed-tools: Bash(git:*) Bash(mkdir:*) Bash(npx:*) Read Write Edit Glob AskUserQuestion
metadata:
  author: andreadellacorte
  version: "0.1.0"
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# memory

Two responsibilities in one skill: **log** (structured markdown memory files) and **session** (named, parallel session tracking with start/resume/end lifecycle).

## Git Root Detection

Before running any command, detect the git root:

```bash
git rev-parse --show-toplevel
```

All paths (`memory:` config value, log files) are relative to git root.

## Commands

### Log Commands

| Command | Description |
|---|---|
| `log daily` | Write daily closeout log to `<memory>/daily/YYYY-MM-DD.md` |
| `log weekly` | Roll up weekly memory from daily files |
| `log monthly` | Roll up monthly memory from daily files |
| `log git` | Write git summary to `<memory>/git/YYYY-MM-DD-GIT-N.md` |

### Session Commands

| Command | Description |
|---|---|
| `session start [name]` | Start a new named session |
| `session resume [name]` | Resume an existing active session |
| `session end [name]` | End a session and capture work done |
| `session spec <topic>` | Create an outcome spec |
| `session doc <topic>` | Create documentation |
| `session review` | Review current work |

### Other

| Command | Description |
|---|---|
| `install` | Install configured sessions backend |

## $ARGUMENTS Routing

| $ARGUMENTS | Action |
|---|---|
| `help` | → `commands/help.md` |
| `doctor` | → `commands/doctor.md` |
| `log daily` | → `commands/log/daily.md` |
| `log weekly` | → `commands/log/weekly.md` |
| `log monthly` | → `commands/log/monthly.md` |
| `log git` | → `commands/log/git.md` |
| `session start` | → `commands/session/start.md` |
| `session resume` | → `commands/session/resume.md` |
| `session end` | → `commands/session/end.md` |
| `session spec` | → `commands/session/spec.md` |
| `session doc` | → `commands/session/doc.md` |
| `session review` | → `commands/session/review.md` |
| `install` | → `commands/install.md` |
| _(empty)_ | → `commands/help.md` |

## Bootstrap

If `.groove/index.md` does not exist, create from `skills/groove/templates/index.md` before proceeding.

If the `memory:` path does not exist, create the full directory structure:

```bash
mkdir -p <memory>/daily <memory>/weekly <memory>/monthly <memory>/git
```

## File Structure

```
<memory>/              # default: .groove/memory/
├── daily/
│   └── YYYY-MM-DD.md
├── weekly/
│   └── YYYY-Www.md
├── monthly/
│   └── YYYY-MM.md
└── git/
    └── YYYY-MM-DD-GIT-N.md

skills/memory/
├── SKILL.md
├── commands/
│   ├── log/
│   │   ├── daily.md
│   │   ├── weekly.md
│   │   ├── monthly.md
│   │   └── git.md
│   ├── session/
│   │   ├── start.md
│   │   ├── resume.md
│   │   ├── end.md
│   │   ├── spec.md
│   │   ├── doc.md
│   │   └── review.md
│   └── install.md
└── templates/
    └── log/
        ├── daily.md
        ├── weekly.md
        ├── monthly.md
        └── git.md
```
