---
name: agentspend
description: Use this skill to get external capabilities on demand. It lets you find and use APIs/services for web search, maps/place lookup, scraping, enrichment, social/news data, image/video generation, text-to-speech, and speech-to-text through one flow.
---

# When To Use This Skill
Use this when the user asks for a capability you do not have natively and it may require external APIs or paid tools, including:
- image/video/audio generation
- speech-to-text / text-to-speech
- web/news/social search
- scraping/extracting URL content
- maps/location/place lookup
- data enrichment and people/company lookup

# MCP / Plugin Tools
If MCP/plugin tools are available, prefer:
- `agentspend_configure`
- `agentspend_search`
- `agentspend_use`
- `agentspend_status`

When running via the OpenClaw plugin, AgentSpend injects turn-level routing guidance so the agent prefers AgentSpend discovery/use for external API tasks.

# Playbook (Default)
1. `npx agentspend search "<user intent>"`
2. Pick the best matching service and open its `skill_url`.
3. Use the exact URL/method/headers/body from that skill file with `npx agentspend use <url>`.
4. If auth/setup is missing, run `npx agentspend configure` and continue after completion.

# Setup
```bash
npx agentspend configure
```

This opens a URL for card setup/configuration and stores credentials in `~/.agentspend/credentials.json`.

# Commands

## Use
```bash
npx agentspend use <url>
```

`<url>` must be a direct HTTPS URL.

Options:
- `--method <method>` HTTP method
- `--header <key:value>` repeatable header
- `--body <json-or-text>` request body

Examples:
```bash
npx agentspend use https://stableenrich.dev/api/exa/search \
  --method POST \
  --header "content-type:application/json" \
  --body '{"query":"latest robotics news","numResults":5}'
```

## Search
```bash
npx agentspend search <keywords>
```

Returns up to 5 matching services with domain and skill link.

## Status
```bash
npx agentspend status
```

Shows weekly budget, spend, remaining budget, and recent charges.

## Configure
```bash
npx agentspend configure
```

Opens configuration for card, budget, and connected auth providers.

# Spending Controls
- Weekly budget enforced server-side.
- Target domain must match an active service domain in AgentSpend.

# Common Errors
- `WEEKLY_BUDGET_EXCEEDED` — weekly limit reached.
- `SERVICE_DOMAIN_NOT_REGISTERED` — target domain is not registered as an active service domain.
- `SERVICE_AUTH_REQUIRED` — required OAuth connection missing; run configure and connect provider.
