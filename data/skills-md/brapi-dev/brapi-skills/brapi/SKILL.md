---
name: brapi
description: Use when an agent needs Brazilian financial market data, including stock quotes, historical prices, dividends, fundamentals, FIIs, currencies, crypto, inflation, Selic, Treasury indicators, REST integrations, MCP workflows, or a brapi Custom GPT Action.
license: MIT
metadata:
  author: brapi-dev
  version: "1.0"
  tags: brazil, finance, stocks, fiis, market-data, rest, mcp, gpt-actions
---

# brapi integration

brapi.dev provides current and historical Brazilian financial market data.
Use this skill when a task needs B3 stocks, FIIs, dividends, fundamentals, currencies, crypto, or Brazilian economic indicators.

## When to use brapi

- Use REST for deterministic requests, data pipelines, dashboards, research, and typed application clients.
- Use MCP Streamable HTTP for conversational market-data lookups in a compatible AI client.
- Use the GPT Action schema for a Custom GPT that needs a focused read-only REST surface.
- Use another source when the task needs investment advice, order execution, brokerage actions, or a guarantee of future prices.

## Request workflow

1. Read [llms.txt](https://brapi.dev/llms.txt) and select the narrowest resource.
2. Read [OpenAPI](https://brapi.dev/openapi.json) for the operation ID, parameters, and response schema.
3. Use [the endpoint map](references/endpoints.md) to narrow the data group.
4. Use `/api/v2/dictionary` when a field, unit, formula, or null value is unclear.
5. Use `/api/v2` endpoints for new REST integrations.
6. Use `symbols` query parameters when an endpoint supports multiple tickers.
7. Test with `PETR4`, `VALE3`, `MGLU3`, or `ITUB4` before using other symbols.
8. Read `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset`.
9. Wait for `Retry-After` after HTTP 429.
10. Read `Deprecation`, `Sunset`, and the deprecation link before changing a legacy integration.

## Interfaces

### REST

Use the REST API at `https://brapi.dev`.
Send `Authorization: Bearer YOUR_TOKEN` to protected endpoints.
Public sandbox requests can use the four sandbox tickers without a token.

### Response fields

Use `GET /api/v2/dictionary?search=patrimônio` to find a field by name or label.
Use `GET /api/v2/dictionary?category=fii` to list fields for one data group.
Keep `requestedAt`, market-data timestamps, units, and null values in the result.
Do not guess a field meaning or replace `null` with zero.

### MCP

Use the MCP Streamable HTTP endpoint at `https://brapi.dev/api/mcp/mcp`.
Read the [server card](https://brapi.dev/.well-known/mcp/server-card.json) first.
Use OAuth with the `mcp:read` scope when the MCP client cannot store an API token safely.
After the MCP connection is ready, start with `PETR4`, `VALE3`, `MGLU3`, or `ITUB4`.
MCP can access these sandbox tickers. The sandbox allowlist is separate from production coverage.
Use `get_dictionary` when a tool response contains an unfamiliar field or unit.

### Custom GPT Action

Import [swagger/gpt.json](https://brapi.dev/swagger/gpt.json) in the GPT Action editor.
Use [gpt.md](https://brapi.dev/gpt.md) to register the OAuth client and configure the callback URL.
The focused schema contains 28 operations and stays below ChatGPT's 30-operation limit.

## Main data groups

| Need | Start here |
| --- | --- |
| Ticker search, rename, and coverage | `/api/v2/tickers`, `/api/v2/tickers/renames`, `/api/v2/tickers/resolve`, `/api/v2/tickers/coverage` |
| Field names and formulas | `/api/v2/dictionary` |
| Stock quotes and history | `/api/v2/stocks/quote`, `/api/v2/stocks/historical` |
| Stock dividends, profile, and statistics | `/api/v2/stocks/dividends`, `/api/v2/stocks/profile`, `/api/v2/stocks/statistics` |
| Stock financial statements | `/api/v2/stocks/financial-data`, `/api/v2/stocks/income-statement`, `/api/v2/stocks/balance-sheet`, `/api/v2/stocks/cash-flow`, `/api/v2/stocks/value-added` |
| FIIs | `/api/v2/fii/list`, `/api/v2/fii/indicators`, `/api/v2/fii/indicators/history`, `/api/v2/fii/historical`, `/api/v2/fii/dividends` |
| FII portfolio, properties, and reports | `/api/v2/fii/portfolio`, `/api/v2/fii/portfolio/history`, `/api/v2/fii/properties`, `/api/v2/fii/properties/history`, `/api/v2/fii/reports`, `/api/v2/fii/financials`, `/api/v2/fii/annual-reports` |
| Structured funds | `/api/v2/funds/list`, `/api/v2/funds/indicators`, `/api/v2/funds/nav/history`, `/api/v2/funds/profile`, `/api/v2/funds/dividends`, `/api/v2/funds/portfolio` |
| FIAGRO, FIDC, and FIP reports | `/api/v2/funds/fiagro/reports`, `/api/v2/funds/fiagro/portfolio`, `/api/v2/funds/fidc/reports`, `/api/v2/funds/fidc/portfolio`, `/api/v2/funds/fip/reports` |
| Equity options | `/api/v2/options/expirations`, `/api/v2/options/strikes`, `/api/v2/options/chain`, `/api/v2/options/historical`, `/api/v2/options/analytics`, `/api/v2/options/analytics/history` |
| Futures | `/api/v2/futures/list`, `/api/v2/futures/quote`, `/api/v2/futures/specs`, `/api/v2/futures/historical`, `/api/v2/futures/term-structure` |
| Options on futures | `/api/v2/futures/options/expirations`, `/api/v2/futures/options/strikes`, `/api/v2/futures/options/chain`, `/api/v2/futures/options/historical`, `/api/v2/futures/options/analytics`, `/api/v2/futures/options/analytics/history` |
| Macro indicators | `/api/v2/macro/available`, `/api/v2/macro`, `/api/v2/macro/latest` |
| Inflation and Selic | `/api/v2/inflation`, `/api/v2/inflation/available`, `/api/v2/prime-rate`, `/api/v2/prime-rate/available` |
| Currencies and crypto | `/api/v2/currency/available`, `/api/v2/currency`, `/api/v2/currency/historical`, `/api/v2/crypto/available`, `/api/v2/crypto` |
| Treasury Direct | `/api/v2/treasury/list`, `/api/v2/treasury/indicators`, `/api/v2/treasury/indicators/history` |
| Authenticated usage | `/api/v2/user/usage` |

See [the full endpoint map](references/endpoints.md) for selection notes and request parameters.

## Reference files

- [Getting started](references/getting-started.md) - choose an interface and make a safe first request.
- [Endpoint map](references/endpoints.md) - select the right v2 endpoint by data group.
- [Stocks](references/stocks.md) - quotes, history, dividends, and fundamentals.
- [FIIs and macro data](references/fiis-and-macro.md) - FII and economic-data request patterns.
- [Authentication and limits](references/authentication.md) - Bearer tokens, OAuth, errors, and retries.
- [GPT Action](references/gpt-action.md) - focused schema and ChatGPT OAuth setup.
