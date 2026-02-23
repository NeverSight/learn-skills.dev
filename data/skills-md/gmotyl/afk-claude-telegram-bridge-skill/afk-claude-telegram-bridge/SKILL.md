---
name: afk-claude-telegram-bridge
description: Remote-control Claude Code from Telegram when AFK. Telegram Topics for session routing, message buffer, approve tool calls, no prefix needed.
---

# AFK Claude Telegram Bridge

Remote-control Claude Code sessions from your phone via Telegram when AFK (away from keyboard).

## When to Use

- "set up telegram bridge" / "configure telegram AFK"
- "enable remote control" / "activate AFK mode"
- "I want to control Claude from my phone"
- Installing this skill on a new machine

## What This Skill Does

Installs a complete Telegram ↔ Claude Code bridge that allows you to:

1. **Approve/deny tool calls** from Telegram inline keyboards
2. **Continue tasks** by sending new instructions when Claude finishes
3. **Auto-approve** read-only tools (Read, Glob, Grep, WebSearch, WebFetch)
4. **Multi-session support** — up to 4 concurrent sessions (S1-S4)
5. **Zero dependencies** — Python stdlib only

## Installation

Run the installer — it copies files, registers hooks, installs `/afk` and `/back` commands, and walks you through Telegram bot setup:

```bash
bash ~/.claude/skills/afk-claude-telegram-bridge/install.sh
```

The installer handles everything:
- Copies hook.py, hook.sh, bridge.py to `~/.claude/hooks/telegram-bridge/`
- Installs `/afk` and `/back` commands to `~/.claude/commands/`
- Registers Stop, Notification, and PermissionRequest hooks in `~/.claude/settings.json`
- Prompts for your bot token and auto-detects your Telegram group

**Restart Claude Code after installation** to load the new `/afk` and `/back` commands.

### Prerequisites

Before running the installer, create a Telegram bot:

1. Open Telegram → search **@BotFather** → send `/newbot`
2. Name it "Claude Bridge" (or your preferred name)
3. Copy the bot token
4. Create a **Telegram Group** with **Topics enabled**
5. Add the bot to the group as **Administrator**
6. Send a message in the group (so the bot can detect it)

## Usage

### Activate AFK Mode

In any Claude Code session:
```
/afk
```

You'll see a confirmation on Telegram: "📡 S1 — AFK Activated"

### Deactivate AFK Mode

```
/back
```

### From Telegram

When Claude needs approval for a tool call, you'll see:
```
🔐 S1 — Permission Request
Tool: Bash
`npm install express`
[✅ Approve] [❌ Deny]
```

When Claude finishes a task:
```
✅ S1 — Task Complete
I've implemented the login form...
[🛑 Let it stop]
```

Reply with text to send Claude a new instruction!

### Multi-Session

With multiple sessions, prefix instructions:
```
S1: now add unit tests
S2: push to remote
```

## File Structure

After installation:
```
~/.claude/hooks/telegram-bridge/
  hook.sh        — Bash entry point
  hook.py        — Hook logic
  bridge.py      — Telegram daemon
  config.json    — Bot token, chat_id, settings
  state.json     — Runtime state
  daemon.log     — Daemon log
  ipc/           — Per-session IPC

~/.claude/commands/
  afk.md         — /afk command
  back.md        — /back command
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `hook.sh --activate <session_id> [project]` | Activate AFK mode |
| `hook.sh --deactivate <session_id>` | Deactivate AFK mode |
| `hook.sh --status` | Show active sessions |
| `hook.sh --setup` | Configure bot token/chat_id |
| `hook.sh --help` | Show help |

## Troubleshooting

- **Daemon log**: `cat ~/.claude/hooks/telegram-bridge/daemon.log`
- **Status**: `~/.claude/hooks/telegram-bridge/hook.sh --status`
- **Manual start**: `python3 ~/.claude/hooks/telegram-bridge/bridge.py`
- **Kill daemon**: Check PID in `state.json`, then `kill <pid>`

## Dependencies

- Python 3 (stdlib only — no pip packages needed)
- bash
- Telegram bot token

## Credits

Originally built by Greg Motyl (@gmotyl).
