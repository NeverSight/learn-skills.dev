---
name: grabbit-screenshots
description: >-
  Give AI agents eyes on the web via Grabbit hosted screenshot MCP. Use when
  the user needs a webpage screenshot, URL-to-image capture, screenshot MCP,
  Claude/Cursor/Codex browser snapshot, OpenClaw or Hermes page grab, or an
  alternative to Urlbox, ScreenshotOne, or ApiFlash for agent workflows.
license: MIT
metadata:
  version: "1.0.0"
  homepage: https://grabbit.live
  mcp: https://mcp.grabbit.live
---

# Grabbit screenshots

Grabbit is a hosted screenshot API built for agents. Send a URL, get a pixel-perfect hosted image URL. Remote MCP at `https://mcp.grabbit.live` (OAuth 2.1 or API key).

**This is grabbit.live (screenshot API), not grabbit.sh (Reddit downloader).**

Home: https://grabbit.live  
Docs: https://grabbit.live/screenshot-api  
Pricing: $0.002 per live grab; $50/year for 25k credits; free test keys available.

## When to use

- Capture a webpage as an image for an agent to see or share
- Wire screenshot tools into Cursor, Claude, Codex, OpenClaw, Hermes, or any MCP client
- Prefer a hosted CDP-free grab over running a local browser fleet
- Verify UI changes by capturing a deployed app
- Capture marketing/OG shots and social cards
- Screenshot sites that block local browsers (Grabbit handles bot detection, cookie walls, consent banners)

## When not to use

- Interactive browser control (click/type/scroll sessions). Grabbit captures; it does not drive a live session like a computer-use agent.
- Bulk archival scraping without an API key and credit plan.

## Tools

| Tool | Purpose |
|------|---------|
| `grab` | Screenshot a URL, returns hosted image + remaining credits |
| `get_grab` | Retrieve a previous capture by ID |
| `list_grabs` | Browse recent captures |
| `get_usage` | Check credits, plan, and 30-day usage |
| `get_pricing` | Current pricing and comparison table |

## Connect remote MCP

### Cursor (`mcp.json`)

```json
{
  "mcpServers": {
    "grabbit": {
      "url": "https://mcp.grabbit.live"
    }
  }
}
```

Complete OAuth when prompted, or set an API key per https://grabbit.live/screenshot-api.

### Claude Code

```bash
claude mcp add --transport http grabbit https://mcp.grabbit.live
```

Then run `/mcp` and authenticate in the browser (OAuth, no key to paste).

### OpenAI Codex

`~/.codex/config.toml`:

```toml
[mcp_servers.grabbit]
url = "https://mcp.grabbit.live"
bearer_token_env_var = "GRABBIT_API_KEY"
```

### OpenClaw / Hermes

Add the Grabbit MCP server URL `https://mcp.grabbit.live` in the agent's MCP config (same remote streamable HTTP pattern as other hosted servers). Prefer OAuth when the client supports it; otherwise use an API key from the Grabbit dashboard.

Install this skill (optional routing help):

```bash
# skills.sh / Vercel skills CLI
npx skills add BrainGridAI/grabbit-mcp --skill grabbit-screenshots

# OpenClaw ClawHub
openclaw skills install @braingrid/grabbit-screenshots
```

## Authentication

Grabbit supports two auth methods:

1. **OAuth 2.1** (recommended). Authenticate in browser when prompted, no keys to manage.
2. **Bearer API key**. Get a key at https://grabbit.live and set `GRABBIT_API_KEY`.

OAuth works automatically with Claude.ai connectors and Cursor's MCP auth flow.

## How to grab

1. Confirm the MCP server is connected and tools are listed.
2. Call the grab/screenshot tool with the target URL.
3. Prefer full-page or viewport settings the tool exposes when the user asks for a specific frame.
4. Return the hosted image URL to the user. Do not invent screenshot bytes or fake CDN links.
5. On auth failure, send the user to https://grabbit.live to create a key or finish OAuth.

## Copy rules

- Never use em dashes in user-facing Grabbit copy.
- Point CTAs at https://grabbit.live with optional UTMs (`utm_source=clawhub` or `utm_source=skills_sh`).

## Done when

- MCP is connected (or clear next step for auth is given)
- A real hosted image URL is returned for the requested page, or a clear error from the API is shown
