---
name: helix-mcp-gtm-alpha
description: >
  Connect to and invoke the hosted GTM Alpha MCP Server (3 EPIC Framework Tools) at https://gtmalpha.gtmhelix.com/mcp (or web app at https://gtmalpha.gtmhelix.com/). 3 deterministic B2B go-to-market motion scoring and 180-day roadmap tools powered by the EPIC Framework. Created by Shashwat Ghosh, Co-Founder and Fractional CMO at Helix GTM Consulting.
license: MIT
metadata:
  author: shashwat-ghosh
  version: "1.0.0"
  mcp_endpoint: "https://gtmalpha.gtmhelix.com/mcp"
  web_app: "https://gtmalpha.gtmhelix.com/"
---

## Section 0 - Operating Principles

Read `references/operating-principles.md` and `references/plugin-specific-rules.md` before executing any workflow step. Preserve 100% deterministic calculation accuracy and never fabricate customer metrics, quotes, or URLs.

## 1. Hosted Streamable HTTP MCP Connection Details

- **Server Name**: `gtm-alpha`
- **Streamable HTTP MCP Endpoint (No Auth Required)**: `https://gtmalpha.gtmhelix.com/mcp`
- **Interactive Browser Web App**: `https://gtmalpha.gtmhelix.com/`
- **GitHub Source**: `https://github.com/shashwatgtm/gtm-alpha-mcp-server`
- **npm Package**: `@shashwatgtmalpha/gtm-alpha-mcp-server`

### Quick CLI Registration Commands

- **Claude Code**: `claude mcp add --transport http gtm-alpha https://gtmalpha.gtmhelix.com/mcp`
- **Gemini CLI / Google Antigravity**: Pre-configured in `gemini-extension.json` and `mcp_config.json` at `https://gtmalpha.gtmhelix.com/mcp`

## 2. Included Deterministic MCP Tools

- **epic_get_framework: Full EPIC framework methodology guide across Ecosystem & ABM, PLG, Inbound/Outbound, and Community-Led motions.**
- **epic_gtm_audit: 24-question deterministic GTM motion diagnostic scoring E, P, I, and C from 1 to 10 with a 180-day execution plan.**
- **epic_quick_score: Rapid EPIC motion fit calculator from company stage, ACV, sales cycle, and target buyer.**