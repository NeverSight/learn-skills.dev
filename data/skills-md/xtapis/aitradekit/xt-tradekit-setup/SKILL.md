---
name: xt-tradekit-setup
description: XT TradeKit installer. Use when the user asks to install/initialize/configure/update XT TradeKit, XT MCP, or xt-tradekit, or when another xt-* skill finds the xt-tradekit MCP tools unavailable. One-click deployment of the local MCP server.
---

# XT TradeKit Installer

The other `xt-*` skills depend on a local MCP server named `xt-tradekit` (39 tools). This skill installs/updates it.

## When to Trigger

- The user explicitly requests: install / initialize / update XT TradeKit (or XT MCP)
- Another `xt-*` skill finds during execution that the `xt-tradekit` MCP tools do not exist

## Installation Flow

1. Run the installation script bundled with this skill:

```bash
bash "$(dirname "$SKILL_PATH")/scripts/install.sh"
```

If `$SKILL_PATH` is unavailable, locate `scripts/install.sh` based on the actual skill installation path (the scripts directory alongside this file).

2. What the script does: clone/update the TradeKit repository to `~/.xt-tradekit/app` → create a Python venv and install dependencies → `claude mcp add --scope user` to register the stdio server (if the claude CLI is not detected, it prints the manual configuration JSON for each client).

3. After installation, tell the user: the `xt-tradekit` tools take effect after **restarting the Claude Code session**; market data/analysis/news require no API Key, while trading requires configuring credentials by running `~/.xt-tradekit/app/setup-credentials.sh` in their own terminal (see the security rules in the `xt-spot-trade` skill: never collect keys within the conversation).

## Prerequisites

- `git`, `python3` (>=3.10)
- Registering with Claude Code requires the `claude` CLI; for other MCP clients, configure manually using the JSON output by the script

## Updating

Simply run the same script again (git pull + dependency update + re-registration).
