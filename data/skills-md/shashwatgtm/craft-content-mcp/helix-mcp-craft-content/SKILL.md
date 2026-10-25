---
name: helix-mcp-craft-content
description: >
  Connect to and invoke the hosted CRAFT Content MCP Server (8 B2B Content Creation Tools) at https://craft-content.gtmhelix.com/mcp (or web app at https://craft-content.gtmhelix.com/). 8 B2B content creation and repurposing tools powered by the CRAFT Framework. Created by Shashwat Ghosh, Co-Founder and Fractional CMO at Helix GTM Consulting.
license: MIT
metadata:
  author: shashwat-ghosh
  version: "2.2.22"
  mcp_endpoint: "https://craft-content.gtmhelix.com/mcp"
  web_app: "https://craft-content.gtmhelix.com/"
---

## Section 0 - Operating Principles

Read `references/operating-principles.md` and `references/plugin-specific-rules.md` before executing any workflow step. Preserve 100% deterministic calculation accuracy and never fabricate customer metrics, quotes, or URLs.

## 1. Hosted Streamable HTTP MCP Connection Details

- **Server Name**: `craft-content`
- **Streamable HTTP MCP Endpoint (No Auth Required)**: `https://craft-content.gtmhelix.com/mcp`
- **Interactive Browser Web App**: `https://craft-content.gtmhelix.com/`
- **GitHub Source**: `https://github.com/shashwatgtm/craft-content-mcp`
- **npm Package**: `@shashwatgtmalpha/craft-content-mcp`

### Quick CLI Registration Commands

- **Claude Code**: `claude mcp add --transport http craft-content https://craft-content.gtmhelix.com/mcp`
- **Gemini CLI / Google Antigravity**: Pre-configured in `gemini-extension.json` and `mcp_config.json` at `https://craft-content.gtmhelix.com/mcp`

## 2. Included Deterministic MCP Tools

- **case_study_generator: Turn verified customer win metrics into full case studies plus 1-line, social, and email versions.**
- **newsletter_builder: Structure high-signal B2B operator newsletters with curated takeaways.**
- **webinar_script: Build end-to-end webinar outlines, talk tracks, and follow-up hooks.**
- **content_repurposer: Transform a core asset into multi-channel LinkedIn, email, and brief formats.**
- **thought_leadership_series: Plan multi-part executive thought leadership arcs anchored on operator POV.**
- **testimonial_capture: Generate low-friction customer quote request templates and interview prompts.**
- **sales_enablement_content: Produce one-pagers, follow-up sequences, and stage-specific buyer collateral.**
- **craft_content_improver: Audit and sharpen existing B2B drafts using CRAFT constraints.**