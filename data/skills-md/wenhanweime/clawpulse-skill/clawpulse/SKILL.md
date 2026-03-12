---
name: clawpulse
description: Open the ClawPulse local monitoring dashboard in the default browser (and optionally restart the local gateway proxy). Use when the user says "open clawpulse", "show the monitor", "open the dashboard", or asks to view OpenClaw monitoring UI.
---

# ClawPulse

This skill opens the locally running ClawPulse dashboard.

## What it does

- Opens the dashboard URL (default: `http://127.0.0.1:18790/`).
- If the dashboard is not reachable, it can try to restart the proxy server script.

## Files / assumptions

- Proxy script (optional restart): `~/.openclaw/monitors/gateway-proxy-enhanced.js`
- Dashboard HTML served by the proxy: `~/.openclaw/monitors/clawpulse.html`

## How to use (agent procedure)

1. Try to open the dashboard URL.
2. If it fails to connect:
   - Restart the proxy script (background).
   - Wait ~1s.
   - Open the dashboard URL again.

## Script

Prefer running the bundled script:

```bash
node ~/.agents/skills/clawpulse/scripts/open.js
```

### Environment overrides

- `CLAWPULSE_URL` (default `http://127.0.0.1:18790/`)
- `CLAWPULSE_PROXY_SCRIPT` (default `~/.openclaw/monitors/gateway-proxy-enhanced.js`)
