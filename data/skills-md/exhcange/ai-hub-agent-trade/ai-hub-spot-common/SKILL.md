---
name: ai-hub-spot-common
version: "0.1.31"
description: Use this Skill when a user asks for AI Hub public spot market data, including connection status, server time, symbols, ticker data, order-book depth, recent trades, or candlesticks. Use the local ai-hub CLI, require no credentials for these commands, and route account or state-changing requests to the focused Skill.
---

# AI Hub Spot Common

## Unified merchant connections

A single MCP server may support both Spot and Futures. Select the configured merchant by `system_get_capabilities`, including `products` and `productAccess`; never infer its product from the server name. Use product-specific tools on that same server. For CLI fallback, use the selected unified merchant profile for either product, replacing legacy `--profile spot` / `--profile futures` examples below. Never switch merchant profiles to recover from a failed request. Existing separate product profiles remain supported.


Use this Skill for public spot market information. All commands in this Skill are read-only and may run without API credentials.

## MCP First

If AI Hub MCP Tools are available, call the matching `market_*` Tool directly. Do not read CLI references, run CLI help, or inspect configuration first. Use CLI Fast Path only when MCP is unavailable.

For normal market questions, follow [references/mcp-routing.md](references/mcp-routing.md): use summary Tools unless raw fields are explicitly requested.

## Prerequisites

Run public commands directly with the configured default profile. Read [references/preflight.md](references/preflight.md) only if the request expands to authenticated work and the CLI reports a profile or credential error.

## Fast Path

For a complete public-market request, run the exact CLI command immediately. Do not read [references/market-commands.md](references/market-commands.md) unless a required parameter is missing, the request is ambiguous, or the CLI returns an error.

## Command Index

| Command | Description |
| --- | --- |
| `ai-hub market ping` | Test the configured OpenAPI connection. |
| `ai-hub market time` | Get server time. |
| `ai-hub market symbols` | List supported spot symbols. |
| `ai-hub market symbols-overview` | Get a small generic overview: counts and sample symbols. |
| `ai-hub market symbols-list` | Browse a bounded page, optionally by quote asset. |
| `ai-hub market symbols-search` | Search by a required keyword without trading-rule metadata. |
| `ai-hub market symbol-info` | Get precision and limit/market minimum rules for one exact symbol. |
| `ai-hub market price` | Get only the current price for one exact symbol. |
| `ai-hub market ticker` | Get exact ticker data for an explicitly requested symbol or symbol list. |
| `ai-hub market ticker-summary` | Get a bounded market overview, movers, and volume leaders. |
| `ai-hub market depth-summary` | Get best bid/ask, spread, and bounded book levels. |
| `ai-hub market trades-summary` | Get bounded recent-trade statistics and samples. |
| `ai-hub market klines-summary` | Get bounded candle analysis and samples. |
| `ai-hub market klines-1min-history` | Get bounded historical one-minute candles from the dedicated historical endpoint. |
| `ai-hub market depth` | Get order-book depth for one symbol. |
| `ai-hub market trades` | Get recent trades for one symbol. |
| `ai-hub market klines` | Get candlesticks for one symbol and interval. |

## Operating Flow

1. For a generic symbol-list request, use `symbols-overview`; for quote-asset browsing, use `symbols-list`; for a keyword, use `symbols-search`; and use `symbol-info` only for an exact symbol's trading rules. Do not request a large raw payload.
2. Identify the symbol and interval or limit when the command needs them.
3. Execute the read-only command immediately.
4. State whether the result is a bounded summary or raw market data and avoid presenting it as investment advice.
5. Route balance, asset movement, sub-account, or order requests to the focused Skill.

`symbol-info` exposes the OpenAPI-advertised `marketBuyMin` (minimum quote-asset amount for MARKET or STOP_MARKET BUY) and `marketSellMin` (minimum base-asset quantity for MARKET or STOP_MARKET SELL). A missing or zero value means the client defers that minimum check to OpenAPI.

If a public endpoint returns `AI_HUB_OPENAPI_BUSINESS_ERROR`, read [references/openapi-error-diagnosis.md](references/openapi-error-diagnosis.md). Use its `reason` and `suggestedAction`; do not infer a cause from the code alone.

Only read [references/market-commands.md](references/market-commands.md) when Fast Path does not apply.
