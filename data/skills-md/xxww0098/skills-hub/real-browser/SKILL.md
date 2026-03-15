---
name: real-browser
description: >
  Launch a real Chrome with the user's login state (cloned profile), exposing CDP
  on a port (default 9851). Supports headless (default) or headed mode, incremental
  profile updates, customizable logging, machine-readable output, and additional
  Chrome arguments via environment variables. Requires the `agent-browser` skill for
  all browser commands.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Real Browser — Login-State CDP Bridge

> **This skill = launch Chrome with login state + CDP port.**
> **`agent-browser` skill = ALL browser commands (click, fill, type, scroll, eval, etc.).**
> You MUST load BOTH skills to operate a browser.

## Step 0: Load the `agent-browser` Skill

Before running ANY browser command, you **MUST** read and load the `agent-browser`
skill. It contains the full command reference with 50+ commands you will need:
click, fill, type, press, scroll, select, hover, check, eval, snapshot, diff,
screenshot, download, upload, auth, sessions, and more.

**Without loading the `agent-browser` skill, you will not know how to interact
with the browser.** This skill only teaches you how to LAUNCH and CONNECT.

## Step 1: Launch Chrome

```bash
# Default: headless on port 9851 (recommended for automation)
scripts/real_browser.sh

# Visible window (only if user explicitly asks to see the browser)
scripts/real_browser.sh --headed

# Custom port (headless)
scripts/real_browser.sh 9888

# Visible window on custom port
scripts/real_browser.sh --headed 9888

# Incremental updates: preserve login state between runs (faster startup)
scripts/real_browser.sh --keep-profile

# Custom logging level (debug, info, warn, error)
scripts/real_browser.sh --log-level debug

# Machine-readable output (for scripting): outputs CDP_URL=<url>
scripts/real_browser.sh --machine-readable

# Combine options as needed
scripts/real_browser.sh --keep-profile --log-level info --headed 9852
```

### Environment Variables for Advanced Customization

| Variable | Purpose | Example |
|----------|---------|---------|
| `REAL_BROWSER_BIN` | Override the Chrome binary path (e.g., for Brave, Edge, or custom Chrome builds) | `REAL_BROWSER_BIN=/usr/bin/brave-browser` |
| `REAL_BROWSER_EXTRA_ARGS` | Additional arguments passed to Chrome (space-separated) | `REAL_BROWSER_EXTRA_ARGS="--no-sandbox --disable-gpu --disable-dev-shm-usage"` |
| `REAL_BROWSER_LOG_LEVEL` | Set the logging level (debug, info, warn, error) | `REAL_BROWSER_LOG_LEVEL=warn` |
| `REAL_BROWSER_CDP_TIMEOUT` | Set the CDP readiness timeout in units of 0.25 seconds (default 160 = 40s) | `REAL_BROWSER_CDP_TIMEOUT=200` (50s) |

**Example with environment variables:**
```bash
REAL_BROWSER_BIN=/opt/google/chrome/chrome \
REAL_BROWSER_EXTRA_ARGS="--no-sandbox --disable-web-security" \
REAL_BROWSER_LOG_LEVEL=debug \
scripts/real_browser.sh --machine-readable 9851
```

## Step 2: Interact via `agent-browser --cdp <port>`

After launch, prepend `--cdp <port>` to every `agent-browser` command.
This is the **ONLY** difference from standard `agent-browser` usage.
All commands, patterns, and workflows from the `agent-browser` skill apply as-is.

```bash
agent-browser --cdp 9851 open https://x.com
agent-browser --cdp 9851 snapshot -i
agent-browser --cdp 9851 click @e3
```

> 💡 **Note**: If you used a custom port when launching (e.g., `scripts/real_browser.sh 9888`),
> then use `--cdp 9888` in all `agent-browser` commands.

## Visibility Guard

If commands fail or return unexpected results, the CDP target may be on a
`chrome://` internal page. Diagnose and fix:

```bash
agent-browser --cdp 9851 get url       # what page am I on?
agent-browser --cdp 9851 tab list      # list all tabs
agent-browser --cdp 9851 tab <index>   # switch to the correct tab
```

## Login State Notes

| Site type | Examples | Login state |
|-----------|----------|-------------|
| Normal sites | X, Reddit, GitHub, 知乎, V2EX | ✅ Preserved |
| High-security (DBSC/Keychain) | Google, Claude, ChatGPT | ⚠️ May log out |

> ⚠️ **Note**: When using `--keep-profile`, the login state is preserved between runs.
> Over time, the profile directory (`~/.chrome-cdp-profile`) may grow in size.
> Periodically remove it to reset the state if needed.

## Rules

1. `--cdp <port>` on **EVERY** `agent-browser` command. No exceptions.
2. Load the **`agent-browser` skill** for all available commands.
3. `open` → always `wait --load networkidle` immediately after.
4. `snapshot -i` before any interaction to get fresh refs.
5. Re-snapshot after any page navigation or DOM change.
6. Never mix `chrome-devtools` tool with `agent-browser`.
7. Port is `9851` unless user passed a custom port to the launch script.

## Troubleshooting

```bash
lsof -iTCP:9851 -sTCP:LISTEN    # find process on port
kill <pid>                       # free the port
rm -f /tmp/.real_browser.lock    # remove stale lock
scripts/real_browser.sh          # re-launch fresh
```

> 🔍 **Additional checks**:
> - If using environment variables, verify they are set correctly (e.g., `echo $REAL_BROWSER_EXTRA_ARGS`).
> - If Chrome fails to launch, check the binary path and extra arguments.
> - For machine-readable output, ensure no other logging interferes (use `--log-level error` to minimize noise).