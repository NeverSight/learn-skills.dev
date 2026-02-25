---
name: claude-chrome
description: Use Claude Code with Chrome browser extension for web browsing and automation tasks. Alternative to OpenClaw's built-in browser tools.
metadata: {"clawdbot":{"emoji":"🌐","requires":{"anyBins":["claude"]}}}
---

# Claude Chrome — Browser Automation via Claude Code

Use Claude Code's Chrome integration to browse the web, interact with pages, and automate browser tasks. This is an alternative to OpenClaw's built-in browser tools (Chrome Relay, OpenClaw profile).

## Prerequisites

1. **Claude Code** installed on the node (e.g. `/opt/homebrew/bin/claude`)
2. **Claude Code Chrome extension** installed and enabled in Chrome
3. **Chrome** running on the node

## How It Works

Claude Code can connect to Chrome via its built-in browser extension (MCP server). When enabled, Claude Code gains browser tools — it can navigate pages, click elements, fill forms, read content, and more.

## Step 1: Check if Chrome Extension is Active

Look for the native host process to confirm the Chrome extension is running:

```bash
nodes.run node=<your-node-id> command='["bash", "-lc", "pgrep -f \"claude --chrome-native-host\""]'
```

If this returns a PID, the Chrome extension bridge is active and ready.

## Step 2: Run Claude Code with Chrome

Use `nodes.run` with your node to execute browser tasks:

```bash
nodes.run node=<your-node-id> commandTimeoutMs=120000 command='["bash", "-lc", "claude --dangerously-skip-permissions --chrome -p \"Go to example.com and read the headline\""]'
```

**Flags:**
- `--dangerously-skip-permissions` — auto-approve all actions (required for automation)
- `--chrome` — enable Chrome browser integration
- `-p` / `--print` — non-interactive print mode (required for automated use)
- `bash -lc` — login shell to ensure PATH is loaded

**Timeout:** See benchmarks below for guidance. Recommended defaults:
- Simple tasks (single page read): `commandTimeoutMs=30000` (30 seconds)
- Medium complexity (multi-step navigation): `commandTimeoutMs=120000` (2 minutes)
- Complex workflows (multiple pages + summarization): `commandTimeoutMs=180000` (3 minutes)

## Performance Benchmarks

| Task Type | Example | Duration | Recommended Timeout |
|-----------|---------|----------|---------------------|
| **Simple** | Read button text on Google | 13s | 30s (30000ms) |
| **Medium** | Wikipedia search + navigate + summarize | 76s | 2min (120000ms) |
| **Complex** | Multi-page navigation + external links | ~90s+ | 3min (180000ms) |

**Gateway timeout note:** OpenClaw's gateway has a hardcoded 10-second connection timeout. Commands will error immediately but continue running in the background. Results arrive via system messages when complete.

## Limitations

- **Domain permissions:** Claude Code's Chrome extension may require user approval for new domains (cannot be automated)
- **Gateway timeout:** Initial connection times out at 10s, but commands continue running
- **Desktop required:** Only works on nodes with a desktop environment, Chrome, and the extension active

## Tips

- Always use `--dangerously-skip-permissions` for automated runs
- Always use `-p` / `--print` for non-interactive output
- Always use `bash -lc` for login shell (PATH loading)
- Be aggressive with timeouts - commands complete in background even after gateway timeout
- Claude Code can combine coding and browsing in a single session
- Check the native host process before attempting browser tasks
- For simple data scraping, consider `web_fetch` instead (faster, no domain permissions needed)
