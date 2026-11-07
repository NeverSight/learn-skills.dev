---
name: helix-mcp-revenue-enablement
description: >
  Connect to and invoke the hosted Revenue Enablement MCP Server (12 B2B Deal Strategy & Sales Tools) at https://revenue-enablement.gtmhelix.com/mcp (or web app at https://revenue-enablement.gtmhelix.com/). 12 B2B deal execution, MEDDPICC discovery, CFO ROI business case, and seller enablement tools. Created by Shashwat Ghosh, Co-Founder and Fractional CMO at Helix GTM Consulting.
license: MIT
metadata:
  author: shashwat-ghosh
  version: "1.0.0"
  mcp_endpoint: "https://revenue-enablement.gtmhelix.com/mcp"
  web_app: "https://revenue-enablement.gtmhelix.com/"
---

## Section 0 - Operating Principles

Read `references/operating-principles.md` and `references/plugin-specific-rules.md` before executing any workflow step. Preserve 100% deterministic calculation accuracy and never fabricate customer metrics, quotes, or URLs.

## 1. Hosted Streamable HTTP MCP Connection Details

- **Server Name**: `revenue-enablement`
- **Streamable HTTP MCP Endpoint (No Auth Required)**: `https://revenue-enablement.gtmhelix.com/mcp`
- **Interactive Browser Web App**: `https://revenue-enablement.gtmhelix.com/`
- **GitHub Source**: `https://github.com/shashwatgtm/revenue-enablement-mcp`
- **npm Package**: `@shashwatgtmalpha/revenue-enablement-mcp`

### Quick CLI Registration Commands

- **Claude Code**: `claude mcp add --transport http revenue-enablement https://revenue-enablement.gtmhelix.com/mcp`
- **Gemini CLI / Google Antigravity**: Pre-configured in `gemini-extension.json` and `mcp_config.json` at `https://revenue-enablement.gtmhelix.com/mcp`

## 2. Included Deterministic MCP Tools

- **deal_qualification: Score live opportunities across MEDDPICC / SPICED qualification dimensions.**
- **discovery_question_generator: Build persona-specific discovery questions and trap-setting prompts.**
- **roi_business_case_builder: Calculate CFO-ready ROI percentage, payback period in months, and 3-year net value.**
- **competitive_battlecard: Build head-to-head seller battlecards with landmines and proof points.**
- **mutual_action_plan: Generate backward-scheduled close plans co-owned with the buyer champion.**
- **executive_briefing_generator: Draft 1-page executive sponsor briefings for complex B2B deals.**
- **objection_handler: Generate evidence-backed responses to pricing, timing, and status-quo objections.**
- **proposal_structurer: Structure commercial proposals tied directly to buyer pain and ROI.**
- **champion_enablement_kit: Build internal selling decks and forwarding emails for your buyer champion.**
- **pricing_negotiation_planner: Plan give-get trade matrices and multi-year packaging options.**
- **win_loss_analyzer: Synthesize deal post-mortems across product, pricing, and sales execution.**
- **account_expansion_planner: Identify land-and-expand whitespace and cross-sell triggers.**