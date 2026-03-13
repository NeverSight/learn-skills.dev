---
name: stock-mcp-query
description: Query historical stock market data (A-shares, HK stocks, ETFs, indices) via MCP protocol. Use this skill when the user wants to retrieve historical daily K-line data, financial statements, market indicators, stock screening results, or any other batch data from the stock database. Requires a valid MCP query token purchased from the management platform.
---

# Stock MCP Query

Query historical stock market data including daily OHLCV, financial reports, index data, ETF data, and more through the MCP protocol.

## Prerequisites

This skill requires:

1. **STOCK_MCP_TOKEN** environment variable — a JWT token purchased from the management platform (nps_enhanced)
2. **STOCK_MCP_SERVER_URL** environment variable (optional) — the MCP server URL, defaults to the URL provided at purchase time

## Setup Check

Before using any data query tools, verify the environment is configured:

```bash
# Check if token exists
echo ${STOCK_MCP_TOKEN:+Token is set}${STOCK_MCP_TOKEN:-ERROR: STOCK_MCP_TOKEN not set}
```

If `STOCK_MCP_TOKEN` is not set:

1. Visit the management platform (nps_enhanced web panel)
2. Navigate to "MCP Data Query" subscription page
3. Purchase a query quota pack (e.g., 10k records for 10 CNY)
4. Copy the issued token
5. Set the environment variable:
   ```bash
   export STOCK_MCP_TOKEN="eyJ..."
   export STOCK_MCP_SERVER_URL="https://your-node:8001/messages"
   ```

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "stock-data": {
      "type": "streamable-http",
      "url": "${STOCK_MCP_SERVER_URL}",
      "headers": {
        "Authorization": "Bearer ${STOCK_MCP_TOKEN}"
      }
    }
  }
}
```

## Available Data Categories

| Category | Description | Example Tools |
|----------|-------------|---------------|
| Daily K-line | OHLCV + volume + turnover | `tushare_daily_*` |
| Daily Basics | PE, PB, market cap, volume ratio | `tushare_daily_basic_*` |
| Adj Factor | Forward/backward adjustment factors | `tushare_adj_factor_*` |
| Financial | Balance sheet, income, cash flow | `tushare_balancesheet_*`, etc. |
| Index | Index daily, weights, components | `tushare_index_*` |
| ETF | ETF daily prices and holdings | `tushare_fund_*` |
| HK Stock | Hong Kong stock daily data | `akshare_hk_*` |
| Market | Market overview, trading calendar | `tushare_trade_cal_*` |

## Usage Notes

- Each tool call returns data and counts against your query quota
- The response includes `_usage.record_count` showing records returned
- The response includes `_usage.quota_remaining` showing remaining quota
- When quota is exhausted, purchase additional packs from the management platform
- Data is sourced from ClickHouse and covers the full available history

## Billing

- Billed per record (data row) returned by each tool call
- Query packs are valid for 90 days from purchase
- Multiple packs stack additively (quota accumulates)
- Usage is reconciled asynchronously between the MCP server and management platform

## Troubleshooting

- **401 "API key required"**: `STOCK_MCP_TOKEN` is not set or not passed in Authorization header
- **401 "Token expired"**: Your token has expired. Purchase a new quota pack to get a fresh token
- **401 "Invalid token"**: Token is malformed or the server's public key doesn't match
- **No data returned**: Check that the requested date is a trading day, or the stock code is valid
- **Quota exhausted**: The `_usage.quota_remaining` will show 0. Purchase additional packs
