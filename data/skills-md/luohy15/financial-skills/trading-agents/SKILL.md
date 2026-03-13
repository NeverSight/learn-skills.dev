---
name: trading-agents
description: Multi-agent stock analysis workflow
author: roy
---

# Trading Agents

Multi-agent stock analysis workflow with 4 phases: Analysis → Research Debate → Trading → Risk.

**Usage:** `/trading-agents NVDA` or `/trading-agents AAPL analysis`

**Phases:**
- Analysis: news, market, fundamentals, social analysts (parallel)
- Research: bull/bear researchers + manager
- Trading: trader proposal
- Risk: risk debate + manager → final decision

**Sub-skills:** `news-analyst`, `market-analyst`, `fundamentals-analyst`, `social-analyst`, `bull-researcher`, `bear-researcher`, `research-manager`, `trader`, `risk-debate`, `risk-manager`

**Output:** `report/<TICKER>/<DATE>/<RANK>/*.md`
