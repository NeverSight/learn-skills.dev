---
name: browser-wsl
description: Install and configure a headless Chrome browser for OpenClaw on WSL/Linux. Gives the agent autonomous browsing without the Chrome extension relay — no human needed.
---

# Browser WSL — Autonomous Headless Browsing for OpenClaw

Give your OpenClaw agent its own browser on WSL/Linux. No relay extension, no human clicking toolbar icons, no "tab not found" errors. Just a headless Chrome instance the agent controls directly via CDP.

## When to Use

- Agent is running on WSL or headless Linux
- `browser` tool returns "No supported browser found"
- Chrome relay extension is unreliable (cross-origin navigation breaks tabs)
- You want 24/7 autonomous browsing without a human at the keyboard

## Quick Setup

### 1. Install Chrome

Run the install script (requires sudo):

```bash
bash scripts/install-chrome.sh
```

This installs Google Chrome + all required dependencies (`libnspr4`, `libnss3`, `libgbm1`, etc.) and verifies headless CDP works.

### 2. Configure OpenClaw

Patch the gateway config to add a managed `openclaw` browser profile:

```
gateway config.patch with:
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true,
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      }
    }
  }
}
```

**Keep `defaultProfile: "chrome"`** if you also use the relay extension. The agent can switch between profiles:
- `profile=chrome` — relay to your real browser (has logins/cookies)
- `profile=openclaw` — headless Chrome (always available, no human needed)

### 3. Use It

```
browser action:start profile:openclaw
browser action:open profile:openclaw targetUrl:"https://example.com"
browser action:snapshot profile:openclaw targetId:<id>
browser action:navigate profile:openclaw targetId:<id> targetUrl:"https://other-site.com"
```

Cross-origin navigation works. No tab tracking issues. No extension required.

## What This Solves

### The Relay Problem

OpenClaw's default `chrome` profile uses a Chrome extension relay. It has known issues:

1. **Cross-origin navigation breaks tabs** — Chrome reassigns target IDs on cross-origin navigation, but the extension doesn't re-attach the debugger. Result: "tab not found" after any `navigate` call.
2. **Requires human interaction** — Someone must click the toolbar icon to attach each tab.
3. **Only works when the PC is active** — No browsing while you're away.

### The Fix

A managed headless Chrome instance (`openclaw` profile) bypasses the relay entirely. The gateway controls Chrome directly via CDP — no extension middleman, no target ID tracking bugs.

## Limitations

- **No cookies/logins** from your real browser — this is a fresh Chrome profile
- **Cloudflare challenges** still block headless Chrome (use the relay for those when you're home)
- **No GUI** — headless only on WSL (no display server)
- **Requires sudo** for initial Chrome installation

## Recommended Setup

Run both profiles:

| Profile | Use Case | Human Needed |
|---------|----------|-------------|
| `chrome` (relay) | Sites needing your logins, Cloudflare-protected sites | Yes |
| `openclaw` (headless) | Research, scraping, price checks, any public site | No |

The agent should default to `openclaw` for autonomous work and fall back to `chrome` relay when authentication or Cloudflare bypass is needed.

## Troubleshooting

**"error while loading shared libraries"** — Run the install script again. It installs all required system libraries.

**CDP not responding** — Make sure port 18800 isn't in use: `lsof -i :18800`

**"No supported browser found"** — The `executablePath` in config must point to the actual Chrome binary: `/usr/bin/google-chrome-stable`

**libasound2 not found** — Ubuntu 24.04+ renamed it to `libasound2t64`. The install script handles both.
