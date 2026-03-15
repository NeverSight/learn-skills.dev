---
name: turbocommit
description: "Auto-commits every Claude Code agent turn with full transcript, AI-generated titles, and session continuity. Use when you want automatic save-states of all Claude work."
license: MIT
metadata:
  author: ctrlshiftbryan
  version: "0.10.2"
---

# turbocommit

Auto-commit after every Claude Code turn. Think save-states for your agent sessions.

## What it does

- **Auto-commits** every turn that modifies files (`git add -A && commit`)
- **Full transcript** in commit body (every prompt/response pair)
- **AI-generated titles** via `claude -p --model haiku`
- **Session chaining** across `/clear` — planning context survives into implementation commits
- **Workstream tracing** — `Continuation of <SHA>` links trace concurrent sessions on one branch
- **Read-only filtering** — sessions that only read (Grep/Read/Bash) are never committed
- **Co-Authored-By** trailers with auto-detected model

## Setup

After installing via `npx skills add`:

```bash
# 1. Register hooks in ~/.claude/settings.json
node <skill-path>/cli.js install

# 2. Enable per-project
cd your-repo
node <skill-path>/cli.js init

# 3. Verify
node <skill-path>/cli.js doctor
```

Where `<skill-path>` is the installed skill directory (e.g., `~/.claude/skills/turbocommit`).

## Commands

| Command | Description |
|---------|-------------|
| `install` | Add hooks to `~/.claude/settings.json` |
| `uninstall` | Remove hooks |
| `init` | Create `.claude/turbocommit.json` in current repo |
| `deinit` | Remove project config |
| `doctor` | Check hook and config health |
| `monitor` | Tail the event log |

## Configuration

`turbocommit init` creates `.claude/turbocommit.json` with `{"enabled": true}`. Optional global config at `~/.claude/turbocommit.json`.

```jsonc
{
  "enabled": true,
  "coauthor": true,        // auto-detect model, or "Name <email>", or false
  "title": {
    "type": "agent",       // "agent" or "transcript"
    "command": "claude -p --model haiku"
  },
  "body": {
    "type": "transcript",  // "transcript" or "agent"
    "maxLineLength": false  // wrap prose at N chars, or false
  }
}
```

Set `TURBOCOMMIT_DISABLED=1` to skip at runtime.

## Requirements

- Node.js >= 18
- Git
- Claude Code
