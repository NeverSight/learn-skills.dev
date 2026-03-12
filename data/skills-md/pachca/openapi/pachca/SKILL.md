---
name: pachca
description: >
  Pachca — corporate messenger with REST API and CLI. Router skill: determines the
  right skill for the user's task. Use when user mentions Pachca, messenger,
  channels, messages, bots, tasks. Do NOT make API calls from this skill — route
  to the appropriate specialized skill.
allowed-tools: Bash(npx:*), Bash(pachca:*), Bash(which:*), Bash(npm:*)
---

# pachca

Pachca — corporate messenger with REST API and CLI.

## Quick start (zero-install)

```bash
npx @pachca/cli <command> --token <TOKEN>
```

## For regular use

```bash
npm install -g @pachca/cli && pachca auth login
```

## Routing

Match the user's task to the right skill below, then activate it.

| User task | Skill |
|-----------|-------|
| User profile, status management, custom fields, token verification | Use `pachca-profile` |
| Employee and tag (group) management | Use `pachca-users` |
| Channel and conversation management, chat members | Use `pachca-chats` |
| Send messages to channels, conversations, and DMs | Use `pachca-messages` |
| Bot management, incoming/outgoing webhooks, link unfurling | Use `pachca-bots` |
| Interactive forms with input fields and buttons for bots | Use `pachca-forms` |
| Create, get, update, and delete tasks (reminders) | Use `pachca-tasks` |
| Full-text search across employees, chats, and messages | Use `pachca-search` |
| Security audit event log | Use `pachca-security` |

## CLI commands

Full list: `pachca commands`
Complex scenarios: see references/ in each skill
Help: `pachca <command> --help`
