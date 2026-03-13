---
name: blofin-market-data
description: "Retrieve real-time market data from BloFin exchange — prices, orderbook depth, candlestick charts, trades, mark prices, and funding rates. No authentication required."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - node
auto_activate:
  - "btc price"
  - "eth price"
  - "crypto price"
  - "blofin price"
  - "blofin market"
  - "orderbook"
  - "order book"
  - "candlestick"
  - "funding rate"
  - "mark price"
---

# BloFin Market Data

Retrieve real-time market data from BloFin exchange. All tools in this skill are **public** and do not require API authentication.

## Available Tools (via blofin-mcp)

### get_tickers — Current Prices

Get the latest price snapshot, best bid/ask, and 24h trading volume.

```
Use get_tickers to check the current price.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | No | Instrument ID, e.g. `BTC-USDT`. Omit to get all tickers. |

**Key response fields:** `last` (last price), `askPrice` / `bidPrice`, `high24h` / `low24h`, `vol24h` (24h volume in contracts), `volCurrency24h` (24h volume in base currency).

**Example prompts:**
- "What's the current BTC price on BloFin?"
- "Show me all BloFin tickers"
- "Compare BTC and ETH prices"

---

### get_instruments — Trading Pairs & Contract Specs

Get available trading instruments and their contract specifications.

```
Use get_instruments to look up contract details.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | No | Instrument ID, e.g. `BTC-USDT` |

**Key response fields:** `contractValue` (value per contract in base currency), `minSize` (minimum order size), `lotSize` (size increment), `tickSize` (price increment), `maxLeverage`, `state` (live/suspend).

**Example prompts:**
- "What's the minimum order size for BTC-USDT on BloFin?"
- "What's the max leverage for ETH-USDT?"
- "List all available trading pairs"

---

### get_orderbook — Order Book Depth

Retrieve bid/ask depth for a specific instrument.

```
Use get_orderbook to see the order book.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID, e.g. `BTC-USDT` |
| `size` | String | No | Depth per side, max 100. Default: 1 |

**Response format:** `asks` array (sell side) and `bids` array (buy side). Each entry is `[price, quantity]`.

**Example prompts:**
- "Show me the BTC-USDT order book, top 10 levels"
- "What's the bid-ask spread for ETH-USDT?"
- "Show me the liquidity depth for SOL-USDT"

---

### get_trades — Recent Trades

Retrieve the most recent transactions for an instrument.

```
Use get_trades to see recent market activity.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID, e.g. `BTC-USDT` |
| `limit` | String | No | Number of results, max 100. Default: 100 |

**Key response fields:** `price`, `size`, `side` (buy/sell), `ts` (timestamp).

**Example prompts:**
- "Show the last 20 BTC-USDT trades"
- "What was the most recent ETH-USDT trade?"

---

### get_mark_price — Index & Mark Price

Get the mark price and index price used for liquidation calculations.

```
Use get_mark_price to check mark and index prices.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | No | Instrument ID, e.g. `BTC-USDT` |

**Key response fields:** `markPrice`, `indexPrice`, `ts`.

**Example prompts:**
- "What's the mark price for BTC-USDT?"
- "Is there a difference between mark and index price for ETH?"

---

### get_candlesticks — OHLCV Data

Get candlestick (OHLCV) chart data for technical analysis.

```
Use get_candlesticks for chart data and technical analysis.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID, e.g. `BTC-USDT` |
| `bar` | String | No | Candlestick period: `1m`, `5m`, `15m`, `30m`, `1H`, `4H`, `1D`, `1W`, `1M` |
| `before` | String | No | Pagination — return records newer than this timestamp |
| `after` | String | No | Pagination — return records older than this timestamp |
| `limit` | String | No | Number of results, max 100 |

**Example prompts:**
- "Show me the BTC-USDT 4-hour candles for the last week"
- "Get the daily candlestick data for ETH-USDT"
- "What does the 1-hour BTC chart look like?"

---

### get_funding_rate — Current Funding Rate

Get the current funding rate for perpetual swap contracts.

```
Use get_funding_rate to check current funding rates.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | No | Instrument ID, e.g. `BTC-USDT` |

**Example prompts:**
- "What's the current BTC-USDT funding rate?"
- "Which coins have the highest funding rates right now?"

---

### get_funding_rate_history — Historical Funding Rates

Get historical funding rate data for analysis.

```
Use get_funding_rate_history for historical funding data.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID, e.g. `BTC-USDT` |
| `before` | String | No | Return records newer than this timestamp |
| `after` | String | No | Return records older than this timestamp |
| `limit` | String | No | Number of results, max 100 |

**Example prompts:**
- "Show the BTC-USDT funding rate history for the past week"
- "Has ETH funding been positive or negative recently?"

## Data Notes

- All timestamps are Unix milliseconds
- Prices and sizes are returned as strings for precision
- Data is returned newest first (descending order)
- Public endpoints do not count toward authenticated rate limits
- REST API rate limit: 500 requests/minute per IP
