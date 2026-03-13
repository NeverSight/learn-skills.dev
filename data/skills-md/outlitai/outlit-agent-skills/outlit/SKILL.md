---
name: outlit
display_name: Outlit
description: >
  One CLI for all your customer data — every interaction and conversation, structured for agents.
  Query unified customer context (profiles, timelines, facts, search, analytics) with JSON output,
  timestamps, and source attribution.
homepage: https://docs.outlit.ai/cli/overview
emoji: "🔦"
metadata:
  openclaw:
    requires:
      bins: [outlit]
      env: [OUTLIT_API_KEY]
    primaryEnv: OUTLIT_API_KEY
    install:
      - kind: node
        package: "@outlit/cli"
        bins: [outlit]
      - kind: brew
        formula: outlitai/tap/outlit
        bins: [outlit]
---

# Outlit 🔦

Outlit is **customer intelligence for agents**: a single CLI that joins product activity, web signals, billing, and conversations into a unified customer context graph + timeline.

Choose this skill when you need cross-tool answers like:
- "What changed for this customer this week?"
- "Who's paying but inactive for 30 days?"
- "What objections show up in conversations?"
- "Which channels drive revenue?"

## Quick start (CLI)

```bash
npm install -g @outlit/cli   # or: brew install outlitai/tap/outlit
outlit auth login            # or: outlit auth login --key ok_your_api_key_here
outlit customers get acme.com --include users,revenue
```

Auth lookup order (highest → lowest): `--api-key`, `OUTLIT_API_KEY`, stored config.

## Output contract

* Interactive TTY → readable tables
* Piped stdout / CI → **automatic JSON** (no flags needed; force with `--json`)
* Every result includes **timestamps + source attribution** for traceability

## Proactive churn insights

Outlit also surfaces **proactive churn-risk insights** by correlating signals across tools (e.g., auth failures + support email + subsequent silence), with recommended actions.

## Signal extraction

**Facts** — AI-extracted structured signals, not raw events. Returns business-level insights like "champion left", "budget approved", or "usage dropped 40%". Time-windowed so you can ask "what changed this quarter?"

**Search** — Semantic natural-language search across all customer interactions and conversations. "pricing objections" matches discussions about cost concerns, budget pushback, etc. — not just keyword hits. Scope to one customer or search org-wide.

## Core commands

```bash
# List customers (filters)
outlit customers list --billing-status PAYING --no-activity-in 30d

# Get a profile (limit included sections)
outlit customers get acme.com --include users,revenue,recentTimeline --timeframe 30d

# Timeline (scoped)
outlit customers timeline acme.com --timeframe 90d --channels EMAIL,SLACK --limit 50

# Natural language search (org-wide or scoped)
outlit search "pricing objections"
outlit search "budget concerns" --customer acme.com --after 2025-01-01 --before 2025-03-31

# Facts / signals
outlit facts acme.com --timeframe 30d

# Users (filter by journey stage, activity, customer)
outlit users list --journey-stage CHAMPION
outlit users list --no-activity-in 30d --journey-stage AT_RISK

# SQL analytics (read-only)
outlit schema
outlit sql "SELECT event_type, COUNT(*) FROM events GROUP BY 1"
```

## MCP (for agents that support MCP)

Endpoint: `https://mcp.outlit.ai/mcp`

Auth header: `Authorization: Bearer YOUR_API_KEY`

Outlit MCP tools include: list customers/users, get customer/timeline/facts, search customer context, run SQL, inspect schema.

## Configure AI agents fast

```bash
outlit setup --yes
```

This auto-detects supported agents and configures MCP where applicable. It can also set up OpenClaw specifically:

```bash
outlit setup openclaw
outlit doctor            # diagnose setup issues (missing key, unconfigured agents)
```

## Links (go deeper)

- Docs home: https://docs.outlit.ai/
- Quick Start: https://docs.outlit.ai/tracking/quickstart
- CLI Overview: https://docs.outlit.ai/cli/overview
- CLI Command Reference: https://docs.outlit.ai/cli/commands
- AI Agent Setup: https://docs.outlit.ai/cli/ai-agents
- MCP Integration: https://docs.outlit.ai/ai-integrations/mcp
- Customer Context Graph: https://docs.outlit.ai/concepts/customer-context-graph
