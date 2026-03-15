---
name: codex-supergraph
description: >-
  Query Codex Supergraph GraphQL data (prices, tokens, pairs, events, holders,
  and live subscriptions). Use when users ask for Codex on-chain analytics or
  need runnable GraphQL calls to https://graph.codex.io/graphql with an API key.
metadata:
  author: codex-data
  version: "1.0"
---

# Codex Supergraph Data

## API Key Guard

This skill requires a valid `CODEX_API_KEY`. When the key is missing or empty, fall back to the codex-mpp skill instead — do not attempt keyless requests or public endpoints unless the user explicitly asks for one. Check for the key before making any network calls.

Switching back: If a user later provides a key and asks to use this skill, re-check at that point. A key simply appearing in the environment does not auto-activate this skill.

If both a local and global copy of this skill exist, the local copy takes precedence.

## Summary

Use this skill to produce valid Codex GraphQL requests using API key authentication.

|                       |                                                                 |
| --------------------- | --------------------------------------------------------------- |
| HTTP endpoint         | `https://graph.codex.io/graphql`                                |
| WebSocket endpoint    | `wss://graph.codex.io/graphql`                                  |
| Schema (SDL)          | `https://graph.codex.io/schema/latest.graphql`                  |
| Introspection JSON    | `https://graph.codex.io/schema/latest.json`                     |
| API-key auth          | `Authorization: <key>` or `Authorization: Bearer <token>`       |

## Authentication

- Use `Authorization: <key>` or `Authorization: Bearer <token>` for all queries, mutations, and subscriptions.
- If the user already has a valid key, use this path.

## Session preflight (required)

Run once and cache:

```bash
curl -sS https://graph.codex.io/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $CODEX_API_KEY" \
  --data-binary '{"query":"query GetNetworks { getNetworks { id name } }"}'
```

Use network IDs from this result before expensive requests.

## Operation selection

| Need | Operation |
| ---- | --------- |
| Networks | `getNetworks` |
| Token discovery/search | `filterTokens` |
| Token prices | `getTokenPrices` |
| Pair metadata | `pairMetadata` |
| Pair OHLCV | `getBars` |
| Token OHLCV | `getTokenBars` |
| Maker events | `getTokenEventsForMaker` |
| Holders | `holders` |
| Top-10 concentration | `top10HoldersPercent` |
| Live single price | `onPriceUpdated` |
| Live multi-price | `onPricesUpdated` |
| Live bars/pairs | `onBarsUpdated`, `onPairMetadataUpdated`, `onTokenBarsUpdated` |
| Short-lived keys | `createApiTokens`, `apiTokens`, `apiToken`, `deleteApiToken` |

Default discovery path: start with `filterTokens`.

## Rules

- Never print raw API keys.
- Validate `networkId` first.
- Keep selection sets minimal until shape is confirmed.
- Use `onPricesUpdated` instead of many single-token subscriptions.

## References

| File | Purpose |
| ---- | ------- |
| [references/apis.md](references/apis.md) | Endpoint/auth matrix, constraints, errors |
| [references/query-templates.md](references/query-templates.md) | Query + websocket templates |
| [references/endpoint-playbook.md](references/endpoint-playbook.md) | Operation selection heuristics by intent |
| [references/tooling-and-mcp.md](references/tooling-and-mcp.md) | Codex Docs MCP setup for coding tools |
