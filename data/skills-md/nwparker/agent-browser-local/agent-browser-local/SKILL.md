---
name: agent-browser-local
description: Browser automation using local browser profile
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(osascript:*), Bash(/Applications/Comet.app/*), Bash(/Applications/Google Chrome.app/*), Bash(/Applications/Chromium.app/*), Bash(/Applications/Microsoft Edge.app/*), Bash(pkill:*), Bash(curl:*), Bash(pgrep:*), Bash(kill:*), Bash(sleep:*)
---

# Browser Selection

- **Default**: Use **Microsoft Edge** unless the user explicitly asks for Chrome, Chromium, or Comet.
- **User choice**: If the user says "use Chrome", "with Chromium", "in Comet", etc., use that browser instead.

# CRITICAL:

**DO NOT** kill the browser process (`pkill`) unless absolutely necessary. Killing the process will close all of the user's open windows and tabs.

Always check if CDP is already active before attempting to launch or restart the browser.

### 1. Check if Already Running (PREFERRED)

Before doing anything, check if CDP is already available on the chosen port. If it is, **USE IT** and do not restart the browser.

```bash
CDP_PORT=${CDP_PORT:-9222}
curl -s http://localhost:${CDP_PORT}/json/version >/dev/null 2>&1 && echo "ALREADY RUNNING" || echo "NEED TO LAUNCH"
```

**If "ALREADY RUNNING", skip all setup steps and go straight to your `agent-browser --cdp ...` commands.**

### 2. Setup: Launch Browser with CDP (ONLY if needed)

If the browser is already running but CDP is *not* enabled, you must ask the user before killing the process, as this will close their active windows.

#### Headed Mode (MANDATORY — visible browser window)

**CRITICAL RULE: The browser MUST be launched in headed (visible) mode.** The human user must be able to see and interact with the browser directly alongside the agent. Do not pass any `--headless` flags.

**Edge (default):**

```bash
# ONLY if user confirms or if no windows are open
pkill -9 -f "Microsoft Edge" 2>/dev/null; sleep 2

# Launch with CDP
"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --remote-debugging-port=${CDP_PORT:-9222} &disown 2>/dev/null
sleep 3

# Verify CDP is ready
curl -s http://localhost:${CDP_PORT:-9222}/json/version >/dev/null && echo "CDP ready"

# Bring window to foreground
osascript -e 'tell application "Microsoft Edge" to activate'
```

**Chrome (when user asks for it):**

```bash
pkill -9 -f "Google Chrome" 2>/dev/null; sleep 2
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=${CDP_PORT:-9222} &disown 2>/dev/null
sleep 3
curl -s http://localhost:${CDP_PORT:-9222}/json/version >/dev/null && echo "CDP ready"
osascript -e 'tell application "Google Chrome" to activate'
```

**Chromium (when user asks for it):**

```bash
pkill -9 -f Chromium 2>/dev/null; sleep 2
"/Applications/Chromium.app/Contents/MacOS/Chromium" --remote-debugging-port=${CDP_PORT:-9222} &disown 2>/dev/null
sleep 3
curl -s http://localhost:${CDP_PORT:-9222}/json/version >/dev/null && echo "CDP ready"
osascript -e 'tell application "Chromium" to activate'
```

**Comet (when user asks for it):**

```bash
pkill -9 -f Comet 2>/dev/null; sleep 2
/Applications/Comet.app/Contents/MacOS/Comet --remote-debugging-port=${CDP_PORT:-9222} &disown 2>/dev/null
sleep 3
curl -s http://localhost:${CDP_PORT:-9222}/json/version >/dev/null && echo "CDP ready"
osascript -e 'tell application "Comet" to activate'
```

## Core Rule: Always Pass `--cdp`

Every `agent-browser` command MUST include `--cdp ${CDP_PORT:-9222}`. This connects to the local browser instance instead of launching a new one.

```bash
# CORRECT — uses local browser (Edge by default)
agent-browser --cdp ${CDP_PORT:-9222} open https://example.com
agent-browser --cdp ${CDP_PORT:-9222} snapshot -i
agent-browser --cdp ${CDP_PORT:-9222} click @e1

# WRONG — would launch isolated headless browser, losing auth
agent-browser open https://example.com
```

## Workflow

Every interaction follows this pattern:

1. **Check CDP first**: `curl -s http://localhost:9222/json/version`
2. **Launch ONLY if missing**: Following the setup steps above for the chosen browser.
3. **Check for Existing Tab**: If the user specifies to continue on a tab with a given URL, you **MUST** first try to find whether there is already an active tab for that URL (e.g., by checking `curl -s http://localhost:9222/json/list`).
4. **Navigate**: `agent-browser --cdp 9222 open <url>` (or switch to/use the existing tab if found).
5. **Snapshot**: `agent-browser --cdp 9222 snapshot -i` (get element refs like `@e1`, `@e2`).
6. **Interact**: Use refs to click, fill, select — always with `--cdp 9222`.

## Session Lifecycle

- **Reuse always**: Check CDP before every interaction, never re-launch if already running.
- **Don't kill on "close"**: `agent-browser --cdp 9222 close` only disconnects agent-browser's Playwright session from the CDP endpoint. It does NOT close or kill the browser. The user's browser stays open.
- **No cleanup needed**: When the Claude Code session ends, the browser keeps running as the user's normal browser.

# Agent Browser Usage
Please load the agent-browser skill for detailed agent-browser use
