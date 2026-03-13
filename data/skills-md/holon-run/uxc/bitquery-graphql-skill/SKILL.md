---
name: bitquery-graphql-skill
description: Use Bitquery GraphQL through UXC for onchain trades, transfers, token holder analysis, balances, and market structure queries across supported networks, with OAuth client_credentials authentication and query-first execution.
---

# Bitquery GraphQL Skill

Use this skill to run Bitquery GraphQL API operations through `uxc`.

Reuse the `uxc` skill for discovery, GraphQL execution, OAuth lifecycle, and generic error handling.

## Prerequisites

- `uxc` is installed and available in `PATH`.
- Network access to `https://streaming.bitquery.io/graphql`.
- A Bitquery application `client_id` and `client_secret` are available.

## Authentication

Bitquery uses bearer access tokens. The most stable agent path is OAuth `client_credentials`, not a copied temporary token.

1. Create a Bitquery application and note:
   - application `client_id`
   - application `client_secret`
   - token scope `api`
2. Login once with OAuth client credentials:
   - `uxc auth oauth login bitquery-graphql --endpoint https://streaming.bitquery.io/graphql --flow client_credentials --client-id <client_id> --client-secret <client_secret> --scope api --token-endpoint https://oauth2.bitquery.io/oauth2/token`
   - This flow completes in one command. No browser approval page is required.
3. Bind the GraphQL endpoint:
   - `uxc auth binding add --id bitquery-graphql --host streaming.bitquery.io --path-prefix /graphql --scheme https --credential bitquery-graphql --priority 100`
4. Verify auth mapping:
   - `uxc auth binding match https://streaming.bitquery.io/graphql`
   - `uxc auth oauth info bitquery-graphql`

## Core Workflow

1. Use fixed link command by default:
   - `command -v bitquery-graphql-cli`
   - If missing, create it: `uxc link bitquery-graphql-cli https://streaming.bitquery.io/graphql`
   - `bitquery-graphql-cli -h`
   - If command conflict is detected and cannot be safely reused, stop and ask skill maintainers to pick another fixed command name.
2. Discover available root operations:
   - `bitquery-graphql-cli -h`
   - Verified roots currently include `query/EVM`, `query/Solana`, `query/Trading`, `query/Tron`, and matching `subscription/*` roots.
3. Inspect a specific operation:
   - `bitquery-graphql-cli query/EVM -h`
   - `bitquery-graphql-cli query/Trading -h`
4. Execute with positional JSON and explicit GraphQL selection sets:
   - `bitquery-graphql-cli query/EVM '{"network":"base","dataset":"combined","_select":"DEXTrades(limit: {count: 1}) { Transaction { Hash } }"}'`
5. Prefer `query/*` operations first.
   - Use `subscription/*` only after runtime validation in the current environment.

## Capability Map

- EVM onchain queries:
  - `query/EVM`
  - `subscription/EVM`
- Solana onchain queries:
  - `query/Solana`
  - `subscription/Solana`
- Cross-market / trading queries:
  - `query/Trading`
  - `subscription/Trading`
- Tron onchain queries:
  - `query/Tron`
  - `subscription/Tron`

Within those roots, Bitquery exposes entities for tasks such as:

- DEX trades
- token balances and holder analysis
- transfers
- blocks and transactions
- mempool and realtime activity
- market or trading views depending on the root

Always inspect the current schema with `-h` and use the narrowest `_select` needed.

## Recommended Usage Pattern

1. Inspect root arguments first:
   - `bitquery-graphql-cli query/EVM -h`
2. Start with a minimal query on one network:
   - `bitquery-graphql-cli query/EVM '{"network":"eth","dataset":"combined","_select":"DEXTrades(limit: {count: 1}) { Transaction { Hash } }"}'`
3. Add only the fields needed for the task:
   - buyers / sellers
   - token addresses
   - symbols
   - amounts
   - timestamps
4. Narrow with GraphQL arguments inside `_select`:
   - `limit`
   - `orderBy`
   - `where`
5. Treat large or realtime queries carefully:
   - avoid wide selections
   - prefer one chain / token / wallet at a time on first pass

## Tested Real Scenario

The following authenticated Bitquery flow was verified successfully through `uxc`:

- OAuth login with `client_credentials`
- auth binding on `https://streaming.bitquery.io/graphql`
- GraphQL host help
- `query/EVM -h`
- authenticated `query/EVM` call on `base`

The verified query shape was:

```json
{
  "network": "base",
  "dataset": "combined",
  "_select": "DEXTrades(limit: {count: 1}) { Block { Time } Transaction { Hash } Trade { Buy { Amount Buyer Currency { Symbol SmartContract } } Sell { Amount Seller Currency { Symbol SmartContract } } } }"
}
```

## Guardrails

- Keep automation on JSON output envelope; do not rely on `--text`.
- Parse stable fields first: `ok`, `kind`, `protocol`, `data`, `error`.
- Use `bitquery-graphql-cli` as the default command path.
- `bitquery-graphql-cli <operation> ...` is equivalent to `uxc https://streaming.bitquery.io/graphql <operation> ...`.
- Prefer positional JSON for GraphQL calls because `_select` is usually required.
- Keep `_select` small on first pass and add explicit filters before expanding scope.
- Prefer `query/*` for stable agent workflows. Treat `subscription/*` as advanced and validate runtime behavior before depending on it.
- If auth fails:
  - confirm `uxc auth binding match https://streaming.bitquery.io/graphql` resolves to `bitquery-graphql`
  - inspect token state with `uxc auth oauth info bitquery-graphql`
  - manually refresh with `uxc auth oauth refresh bitquery-graphql`
  - if needed, rerun `uxc auth oauth login ... --flow client_credentials ...`
- Do not paste temporary IDE tokens into long-lived skill docs. Prefer application-based `client_credentials`.

## References

- Invocation patterns:
  - `references/usage-patterns.md`
