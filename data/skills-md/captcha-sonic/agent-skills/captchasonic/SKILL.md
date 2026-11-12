---
name: captchasonic
description: Solve CAPTCHAs using the CaptchaSonic AI API. Supports reCAPTCHA, Cloudflare Turnstile, Geetest, AWS WAF, TikTok, Binance, OCR, and more. Provides MCP server tools for health checks, balance queries, and captcha solving from any AI agent.
---

# CaptchaSonic — AI CAPTCHA Solving Skill

Give your AI agent the ability to **solve any CAPTCHA** using the [CaptchaSonic](https://captchasonic.com) API.

## What This Skill Provides

This skill connects your agent to the CaptchaSonic MCP server, which exposes three tools:

| MCP Tool | What It Does | API Key Required |
|---|---|---|
| `health_check` | Verify the CaptchaSonic API is online | No |
| `get_balance` | Check your account balance in USD | Yes |
| `solve_captcha` | Submit a CAPTCHA image and get the solution | Yes |

## Supported CAPTCHA Types

- **PopularCaptcha** — image grid challenges (select all traffic lights, etc.)
- **reCAPTCHA v2** — Google grid select
- **reCAPTCHA v3** — score-based token
- **Cloudflare Turnstile** — token-based (async)
- **Cloudflare Challenge** — full page challenge
- **Geetest v3/v4** — slide, click, nine-grid
- **AWS WAF** — image classification
- **TikTok** — rotation/click
- **Binance** — slide puzzle
- **OCR** — image-to-text recognition

## Quick Setup

### 1. Get an API Key

Register at [captchasonic.com](https://captchasonic.com) and get your API key (starts with `sonic_`).

### 2. Add the MCP Server

**Claude Code CLI:**
```bash
claude mcp add sonic --env SONIC_API_KEY=sonic_xxxx -- npx -y @captchasonic/mcp-server
```

**Claude Desktop** — add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "sonic": {
      "command": "npx",
      "args": ["-y", "@captchasonic/mcp-server"],
      "env": {
        "SONIC_API_KEY": "sonic_xxxx"
      }
    }
  }
}
```

### 3. Verify It Works

Ask your agent: *"Run a health check on CaptchaSonic"*

The agent will call the `health_check` MCP tool and return the server status and version.

## Sub-Skills

For detailed workflows, see:

- **captchasonic-solve** — Solve any CAPTCHA type with step-by-step guidance
- **captchasonic-balance** — Check account balance and credit status
- **captchasonic-setup** — First-time MCP server installation and verification

## Reference Documentation

- `references/mcp-setup.md` — Detailed MCP installation for all platforms
- `references/captcha-types.md` — All supported types with required parameters
- `references/solution-types.md` — How to interpret each solution format
- `references/troubleshooting.md` — Common errors and fixes

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SONIC_API_KEY` | Your CaptchaSonic API key (`sonic_xxxx`) | — (required) |
| `SONIC_BASE_URL` | Override API server URL | `https://api.captchasonic.com` |
