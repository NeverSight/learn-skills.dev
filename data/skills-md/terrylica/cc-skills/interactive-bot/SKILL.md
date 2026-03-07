---
name: interactive-bot
description: Gmail Commander Telegram bot with slash commands, inline keyboards, and AI routing. TRIGGERS - telegram bot, bot commands, inbox bot, email bot, start bot, stop bot, compose email via telegram.
allowed-tools: Read, Bash, Grep, Glob
---

# Interactive Bot

Gmail Commander Telegram bot — slash commands for email access + AI-powered free-text routing.

## Mandatory Preflight

### Step 1: Check Bot Script Exists

```bash
ls -la "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/bot.ts" 2>/dev/null || echo "SCRIPT_NOT_FOUND"
```

### Step 2: Verify Environment

```bash
echo "TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:+SET}"
echo "TELEGRAM_CHAT_ID: ${TELEGRAM_CHAT_ID:-NOT_SET}"
echo "GMAIL_OP_UUID: ${GMAIL_OP_UUID:-NOT_SET}"
echo "HAIKU_MODEL: ${HAIKU_MODEL:-NOT_SET}"
```

## Bot Commands (Sidebar Menu)

| Command  | Description                        |
| -------- | ---------------------------------- |
| /inbox   | Show recent inbox emails           |
| /search  | Search emails (Gmail query syntax) |
| /read    | Read email by ID                   |
| /compose | Compose a new email                |
| /reply   | Reply to an email                  |
| /drafts  | List draft emails                  |
| /digest  | Run email digest now               |
| /status  | Bot status and stats               |
| /help    | Show all commands                  |

## Two-Tier Command System

**Tier 1 — Deterministic**: Slash commands call Gmail CLI directly.

**Tier 2 — Intelligent**: Free-text messages route through Agent SDK (Haiku) with 4 Gmail MCP tools (list, search, read, draft).

## Safety Controls

- **Mutex**: 1 agent query at a time
- **Timeout**: 2-minute maximum per query
- **Circuit Breaker**: 3 failures in a row disables agent for 10 minutes
- **Anti-contamination**: Skill contamination detection on all agent responses
- **Auth Guard**: Only responds to authorized TELEGRAM_CHAT_ID

## Running Manually

```bash
cd ~/own/amonic && bun run "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/gmail-commander/scripts/bot.ts"
```

## References

- [command-reference.md](./references/command-reference.md) — All commands with examples
- [compose-flow.md](./references/compose-flow.md) — Multi-step compose/reply state machine
- [display-patterns.md](./references/display-patterns.md) — Email rendering rules

## Post-Change Checklist

- [ ] YAML frontmatter valid (no colons in description)
- [ ] Trigger keywords current
- [ ] Path patterns use $HOME not hardcoded paths
