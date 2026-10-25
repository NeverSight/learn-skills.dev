---
name: helix-mcp-icp-intelligence
description: >
  Connect to and invoke the hosted ICP Intelligence MCP Server (9 B2B Targeting & TAM/SAM/SOM Tools) at https://icp-intelligence.gtmhelix.com/mcp (or web app at https://icp-intelligence.gtmhelix.com/). 9 deep ICP pattern detection, market sizing, buying group, and account prioritization tools. Created by Shashwat Ghosh, Co-Founder and Fractional CMO at Helix GTM Consulting.
license: MIT
metadata:
  author: shashwat-ghosh
  version: "1.2.25"
  mcp_endpoint: "https://icp-intelligence.gtmhelix.com/mcp"
  web_app: "https://icp-intelligence.gtmhelix.com/"
---

## Section 0 - Operating Principles

Read `references/operating-principles.md` and `references/plugin-specific-rules.md` before executing any workflow step. Preserve 100% deterministic calculation accuracy and never fabricate customer metrics, quotes, or URLs.

## 1. Hosted Streamable HTTP MCP Connection Details

- **Server Name**: `icp-intelligence`
- **Streamable HTTP MCP Endpoint (No Auth Required)**: `https://icp-intelligence.gtmhelix.com/mcp`
- **Interactive Browser Web App**: `https://icp-intelligence.gtmhelix.com/`
- **GitHub Source**: `https://github.com/shashwatgtm/icp-intelligence-mcp`
- **npm Package**: `@shashwatgtmalpha/icp-intelligence-mcp`

### Quick CLI Registration Commands

- **Claude Code**: `claude mcp add --transport http icp-intelligence https://icp-intelligence.gtmhelix.com/mcp`
- **Gemini CLI / Google Antigravity**: Pre-configured in `gemini-extension.json` and `mcp_config.json` at `https://icp-intelligence.gtmhelix.com/mcp`

## 2. Included Deterministic MCP Tools

- **icp_deep_dive: Extract firmographic, technographic, and behavioral ICP patterns from customer lists.**
- **icp_scoring_model: Build weighted 100-point account fit and intent scoring rubrics.**
- **buyer_group_analyzer: Map Economic Buyers, Champions, Technical Evaluators, and Blockers.**
- **tam_sam_som_calculator: Deterministic bottom-up TAM, SAM, and SOM arithmetic calculator.**
- **lookalike_signal_generator: Identify observable buying triggers and lookalike account signals.**
- **account_prioritization: Tier target accounts into Tier 1 ABM, Tier 2 Scale, and Tier 3 Nurture.**
- **icp_gap_analysis: Compare current customer base against target upmarket or new-vertical ICP.**
- **icp_evolution_tracker: Track ICP drift across cohorts as ACV and product maturity grow.**
- **icp_interview_synthesizer: Extract structured ICP patterns from raw customer interview notes.**