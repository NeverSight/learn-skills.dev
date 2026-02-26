---
name: buildover-setup
description: >
  Set up and integrate BuildOver into any existing web project. BuildOver is an AI-powered dev tool
  that wraps a running web app with a floating chat widget via a reverse proxy — letting you ask
  Claude to modify source files in real-time with HMR.

  Use this skill when the user says /buildover-setup, asks to "add BuildOver to my project",
  "integrate BuildOver", "set up AI coding assistant on my dev server", or wants to connect
  BuildOver to their existing running application.
---

# BuildOver Setup

BuildOver wraps your existing dev server with a reverse proxy + AI chat widget. You visit
`localhost:<buildover-port>` instead of your original port, and a floating panel lets you ask
Claude to edit your source files live with HMR.

**Packages** (all pulled in by the `buildover` CLI):
- `buildover` — CLI (`buildover dev`)
- `buildover-server` — auto-installed dependency
- `buildover-widget` — auto-installed dependency

## Workflow

### 1. Check Existing Installation

```bash
buildover --version 2>/dev/null || npx buildover --version 2>/dev/null
```

### 2. Install BuildOver

**Global (recommended):**
```bash
npm install -g buildover
```

**Local dev dependency:**
```bash
npm install --save-dev buildover
# pnpm add -D buildover / yarn add -D buildover
```

### 3. Detect Target Port

Read `package.json` to find the dev port:
```bash
cat package.json | grep -E '"dev"|"start"'
```

Common defaults if not specified:
- `3000` — React CRA, Next.js
- `5173` — Vite
- `4200` — Angular
- `8080` / `8000` — generic / Django / Flask

Ask the user to confirm if unclear.

### 4. Configure API Key

```bash
grep "ANTHROPIC_API_KEY" .env 2>/dev/null || echo "not set"
```

If missing, add to `.env` (create if needed):
```
ANTHROPIC_API_KEY=sk-ant-...
```

Get a key at https://console.anthropic.com/settings/keys.
> The proxy and widget work without a key — only AI chat requires it.

### 5. Start BuildOver

```bash
# Global install:
buildover dev --target <target-port> --port <buildover-port>

# Local install:
npx buildover dev --target <target-port> --port <buildover-port>
```

Default `--port` is `4100`. Use `10001` to avoid common conflicts.

**Example** (Next.js on 3000, BuildOver on 10001):
```bash
buildover dev --target 3000 --port 10001
# → Open http://localhost:10001
```

### 6. (Optional) Cloudflare Tunnel for Remote Access

If the user wants a public HTTPS URL:

```bash
# Install (macOS)
brew install cloudflared

# Authenticate & create tunnel
cloudflared tunnel login
cloudflared tunnel create <tunnel-name>
```

Create `~/.cloudflared/config.yml`:
```yaml
tunnel: <tunnel-id>
credentials-file: /Users/<username>/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: your-subdomain.yourdomain.com
    service: http://localhost:<buildover-port>
  - service: http_status:404
```

```bash
cloudflared tunnel run <tunnel-name>
```

## Verification Checklist

- No `⚠ No authentication configured` at startup → API key loaded ✓
- Banner shows correct target and BuildOver URLs ✓
- Opening `http://localhost:<buildover-port>` shows original site + floating chat button ✓
- Sending a chat message triggers `[Agent]` logs in the server output ✓

## Common Issues

| Issue | Fix |
|-------|-----|
| `EADDRINUSE` on BuildOver port | `lsof -i :<port>` → kill the process |
| `⚠ No authentication configured` | Add `ANTHROPIC_API_KEY` to `.env` and restart server |
| Chat sends but no code changes | Check server logs for `[Agent] Error` — usually auth failure |
| Widget not visible | Hard-refresh; check `/buildover/widget.js` returns 200 |
| HMR not working | Start the original dev server before BuildOver |
