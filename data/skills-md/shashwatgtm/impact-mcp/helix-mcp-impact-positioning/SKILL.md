---
name: helix-mcp-impact-positioning
description: >
  Connect to and invoke the hosted IMPACT Positioning MCP Server (8 B2B Positioning & Messaging Tools) at https://impact.gtmhelix.com/mcp (or web app at https://impact.gtmhelix.com/). 8 hypothesis-driven B2B positioning and messaging tools covering all 6 steps of the IMPACT Framework. Created by Shashwat Ghosh, Co-Founder and Fractional CMO at Helix GTM Consulting.
license: MIT
metadata:
  author: shashwat-ghosh
  version: "2.2.18"
  mcp_endpoint: "https://impact.gtmhelix.com/mcp"
  web_app: "https://impact.gtmhelix.com/"
---

## Section 0 - Operating Principles

Read `references/operating-principles.md` and `references/plugin-specific-rules.md` before executing any workflow step. Preserve 100% deterministic calculation accuracy and never fabricate customer metrics, quotes, or URLs.

## 1. Hosted Streamable HTTP MCP Connection Details

- **Server Name**: `impact`
- **Streamable HTTP MCP Endpoint (No Auth Required)**: `https://impact.gtmhelix.com/mcp`
- **Interactive Browser Web App**: `https://impact.gtmhelix.com/`
- **GitHub Source**: `https://github.com/shashwatgtm/impact-mcp`
- **npm Package**: `@shashwatgtmalpha/impact-mcp`

### Quick CLI Registration Commands

- **Claude Code**: `claude mcp add --transport http impact https://impact.gtmhelix.com/mcp`
- **Gemini CLI / Google Antigravity**: Pre-configured in `gemini-extension.json` and `mcp_config.json` at `https://impact.gtmhelix.com/mcp`

## 2. Included Deterministic MCP Tools

- **impact_get_framework: Complete guide to the 6-phase IMPACT positioning methodology.**
- **impact_identify_champions: Phase 1 tool to pinpoint acute pain champions and trigger events.**
- **impact_map_alternatives: Phase 2 tool to map status quo, DIY, and direct competitors.**
- **impact_pinpoint_value: Phase 3 tool to isolate differentiated capabilities and measurable outcomes.**
- **impact_anchor_market: Phase 4 tool to select the winnable beachhead market category.**
- **impact_craft_message: Phase 5 tool to build the core positioning statement, tagline, and 3 value pillars.**
- **impact_translate_execution: Phase 6 tool to translate positioning into homepage copy, sales pitch, and launch assets.**
- **impact_full_audit: End-to-end 6-phase IMPACT positioning score and weakest-link diagnostic.**