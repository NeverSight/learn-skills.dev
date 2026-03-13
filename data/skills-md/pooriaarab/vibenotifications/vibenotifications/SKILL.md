---
name: vibenotifications
description: "Customizable notifications for Claude Code -- GitHub PRs, Slack DMs, stock prices, and more while you code"
---

# vibenotifications

Bring real-world notifications into your Claude Code session. While Claude works on your code, you'll see GitHub PR reviews, Slack messages, stock prices, and more -- right in the terminal.

## When to Use This Skill

Use this skill when the user:
- Wants to receive notifications (GitHub, Slack, email, stocks, crypto) inside Claude Code
- Asks about monitoring GitHub PRs, CI failures, or mentions while coding
- Wants Slack DMs or channel messages surfaced in their terminal
- Asks about tracking stock or crypto prices during a coding session
- Wants a notification dashboard or digest in their CLI workflow
- Mentions wanting to stay updated without leaving the terminal

## Installation

```bash
npm install -g vibenotifications
vibenotifications init
```

Or run without installing:

```bash
npx vibenotifications init
```

The interactive setup wizard walks through selecting notification sources, entering API keys, testing connections, and installing Claude Code hooks automatically.

## Available Plugins

| Plugin | Source | API key needed? |
|--------|--------|----------------|
| **GitHub** | PR reviews, CI failures, mentions | Yes (PAT) |
| **Slack** | DMs, channel messages | Yes (Bot token) |
| **X/Twitter** | Mentions | Yes (Bearer token) |
| **Email** | Unread count | Yes (IMAP) |
| **Stocks/Crypto** | BTC, ETH, SOL, DOGE prices | No |
| **MCP Bridge** | Connected MCP server status | No |

## Notification Surfaces

Notifications appear across 5 Claude Code surfaces:

- **Spinner verbs**: Notification titles replace spinner text while Claude thinks
- **Status line**: Top notification shown in the status bar with clickable links
- **Context injection**: High-priority items injected into Claude's context
- **Session summary**: Notification digest shown when starting/resuming a session
- **Dashboard**: Full notification list via `vibenotifications dashboard`

## Commands

```bash
vibenotifications init            # Interactive setup wizard
vibenotifications dashboard       # View all notifications
vibenotifications add <plugin>    # Enable a new source
vibenotifications remove <plugin> # Disable a source
vibenotifications start           # Start notification daemon
vibenotifications stop            # Stop notification daemon
vibenotifications fetch           # Fetch notifications once
vibenotifications uninstall       # Remove everything
```
