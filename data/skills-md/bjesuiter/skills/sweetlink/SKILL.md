---
name: sweetlink
description: Use SweetLink to connect your AI agent to a real browser tab. Like Playwright, but works in your current tab. Enables authentication, screenshots, smoke tests, and DevTools telemetry without headless automation.
homepage: https://github.com/steipete/sweetlink
metadata: {"clawdbot":{"emoji":"🍭","requires":{"bins":["sweetlink"]},"install":[{"id":"node","kind":"node","package":"sweetlink","bins":["sweetlink"],"label":"Install SweetLink (pnpm)"}]}}
---

# SweetLink 🍭

Connect your AI agent to a real browser tab. Like Playwright, but works in your current tab.

## Why SweetLink?

- **Real browser** — Automate your actual browser session (Chrome with DevTools)
- **Auth preserved** — Cookies/sessions from your profile carry over
- **Loop closed** — Agent can see what you see, interact with your tab
- **Smoke tests** — Verify web apps in real browser context

## Install

```bash
# From source (requires pnpm)
cd ~/Develop/bjesuiter/sweetlink
pnpm install
pnpm build

# Or globally
pnpm add -g sweetlink

# Trust CA for TLS
sweetlink trust-ca
```

## Start Daemon

```bash
# Start the SweetLink daemon (runs on https://localhost:4455)
sweetlink daemon start

# Check status
sweetlink daemon status

# Stop daemon
sweetlink daemon stop
```

## Core Commands

### Session Management
```bash
# List active sessions
sweetlink session list

# Reconnect after hot reload
sweetlink session reconnect <session-id>
```

### Browser Control
```bash
# Open browser with DevTools (from main profile)
sweetlink browser open --profile default

# Open incognito profile
sweetlink browser open --profile incognito

# Get browser status
sweetlink browser status
```

### Console & Network
```bash
# Tail console logs (last 50 entries)
sweetlink devtools console --tail 50

# Tail network requests
sweetlink devtools network --tail 50

# Clear buffers
sweetlink devtools clear
```

### Screenshot & DOM
```bash
# Capture screenshot
sweetlink screenshot --output screenshot.png

# Get DOM snapshot
sweetlink dom snapshot --output dom.json

# Query element (CSS selector)
sweetlink dom query ".submit-button" --property textContent
```

### Automation Prompts

Use with Codex, Claude, or Cursor once a session is live:

```bash
# Example: Check if element exists
sweetlink dom query "#login-form" --exists

# Example: Click button
sweetlink dom click ".submit-btn"

# Example: Type in input
sweetlink dom type "#email" "user@example.com"

# Example: Get page title
sweetlink browser title
```

## Workflow with AI Agents

### 1. Start SweetLink Daemon
```bash
sweetlink daemon start
sweetlink trust-ca  # First time only
```

### 2. Open Browser Tab
```bash
sweetlink browser open --profile default
```

### 3. Navigate to target site
- Do this manually in the opened browser
- Authenticate if needed (cookies persist)

### 4. Agent can now automate
```bash
# Agent uses these commands:
sweetlink dom query ".product-card" --property outerHTML
sweetlink screenshot --output products.png
sweetlink devtools console --tail 100
```

### 5. Reattach sessions
```bash
sweetlink session list
sweetlink session reconnect <session-id>
```

## Example Use Cases

### Smoke Test Web App
```bash
# Navigate to app
sweetlink browser open --profile default
# (manually navigate to http://localhost:3000)

# Check for console errors
sweetlink devtools console --tail 0
```

### Screenshot Testing
```bash
# Capture full page
sweetlink screenshot --full-page --output test.png

# Capture specific element
sweetlink dom query ".hero" --screenshot hero.png
```

### Form Automation
```bash
sweetlink dom type "#name" "Test User"
sweetlink dom type "#email" "test@example.com"
sweetlink dom click "#submit"
sweetlink dom query "#success" --exists
```

## API Reference

### Daemon API (internal)
- `GET /api/sweetlink/status` — Check daemon health + TLS trust
- `POST /api/sweetlink/session` — Create new session
- `GET /api/sweetlink/sessions` — List sessions

### CLI Commands
| Command | Description |
|---------|-------------|
| `sweetlink daemon start\|stop\|status` | Manage daemon |
| `sweetlink browser open\|close` | Control browser |
| `sweetlink session list\|reconnect` | Manage sessions |
| `sweetlink devtools console\|network` | DevTools access |
| `sweetlink dom query\|click\|type\|screenshot` | DOM operations |
| `sweetlink screenshot` | Capture screenshots |

## Troubleshooting

### Daemon won't start
```bash
# Check if port is in use
lsof -i :4455

# Kill existing process
sweetlink daemon stop
sweetlink daemon start
```

### TLS certificate not trusted
```bash
# Re-run trust
sweetlink trust-ca

# Open browser to accept
open https://localhost:4455
```

### Session disconnected
```bash
# List sessions
sweetlink session list

# Reconnect
sweetlink session reconnect <session-id>
```

## Related Skills

- **oracle** — Prompt bundler for multi-model runs (pairs well with SweetLink)
- **browser** — Clawdbot's built-in browser control

## Notes

- SweetLink uses real Chrome/Chromium with DevTools Protocol
- Cookies/auth persist from your browser profile
- Works on macOS with Chrome or Chromium-based browsers
- TLS certificate required for daemon communication
