---
name: okx-cex-market
description: "This skill should be used when the user asks for 'price of BTC', 'ETH ticker', 'show me the orderbook', 'market depth', 'BTC candles', 'OHLCV chart data', 'funding rate', 'open interest', 'mark price', 'index price', 'recent trades', 'price limit', 'list instruments', 'what instruments are available', or any request to query public market data on OKX CEX. All commands are read-only and do NOT require API credentials. Do NOT use for account balance/positions (use okx-cex-portfolio), placing/cancelling orders (use okx-cex-trade), or grid/DCA bots (use okx-cex-bot)."
license: MIT
metadata:
  author: okx
  version: "1.0.0"
  homepage: "https://www.okx.com"
  moltbot:
    requires:
      bins: ["okx"]
    install:
      - id: npm
        kind: node
        package: "@okx_ai/okx-trade-cli"
        bins: ["okx"]
        label: "Install okx CLI (npm)"
---

# OKX CEX Market Data CLI

Public market data for OKX exchange: prices, order books, candles, funding rates, open interest, and instrument info. All commands are **read-only** and do **not require API credentials**.

## Prerequisites

1. Install `okx` CLI:
   ```bash
   npm install -g @okx_ai/okx-trade-cli
   ```
2. No credentials needed for market data — all commands are public.
3. Verify install:
   ```bash
   okx market ticker BTC-USDT
   ```

## Demo vs Live Mode

Market data commands are public and read-only — **demo mode has no effect**. The same data is returned with or without `--demo`. No confirmation needed before running any market command.

## Skill Routing

- For market data (prices, charts, depth, funding rates) → use `okx-cex-market` (this skill)
- For account balance, P&L, positions, fees, transfers → use `okx-cex-portfolio`
- For regular spot/swap/futures/algo orders → use `okx-cex-trade`
- For grid and DCA trading bots → use `okx-cex-bot`

## Quickstart

```bash
# Current BTC spot price
okx market ticker BTC-USDT

# All SWAP (perp) tickers
okx market tickers SWAP

# BTC perp order book (top 5 levels each side)
okx market orderbook BTC-USDT-SWAP

# BTC hourly candles (last 20)
okx market candles BTC-USDT --bar 1H --limit 20

# BTC perp current funding rate
okx market funding-rate BTC-USDT-SWAP

# BTC perp funding rate history
okx market funding-rate BTC-USDT-SWAP --history

# Open interest for all SWAP instruments
okx market open-interest --instType SWAP

# List all active SPOT instruments
okx market instruments --instType SPOT
```

## Command Index

| # | Command | Type | Description |
|---|---|---|---|
| 1 | `okx market ticker <instId>` | READ | Single instrument: last price, 24h high/low/vol |
| 2 | `okx market tickers <instType>` | READ | All tickers for an instrument type |
| 3 | `okx market instruments --instType <type>` | READ | List tradeable instruments |
| 4 | `okx market orderbook <instId> [--sz <n>]` | READ | Order book top asks/bids |
| 5 | `okx market candles <instId> [--bar] [--limit]` | READ | OHLCV candlestick data |
| 6 | `okx market index-candles <instId> [--bar] [--limit]` | READ | Index OHLCV candles |
| 7 | `okx market funding-rate <instId> [--history]` | READ | Current or historical funding rate |
| 8 | `okx market trades <instId> [--limit <n>]` | READ | Recent public trades |
| 9 | `okx market mark-price --instType <type> [--instId <id>]` | READ | Mark price for contracts |
| 10 | `okx market index-ticker [--instId <id>] [--quoteCcy <ccy>]` | READ | Index price (e.g., BTC-USD) |
| 11 | `okx market price-limit <instId>` | READ | Upper/lower price limits for contracts |
| 12 | `okx market open-interest --instType <type> [--instId <id>]` | READ | Open interest in contracts and coins |

## Cross-Skill Workflows

### Check price before placing an order
> User: "What's the current BTC price? I want to place a limit buy."

```
1. okx-cex-market    okx market ticker BTC-USDT              → check last price and 24h range
        ↓ user decides price
2. okx-cex-portfolio okx account balance USDT                → confirm available funds
        ↓ user approves
3. okx-cex-trade     okx spot place --instId BTC-USDT --side buy --ordType limit --px <px> --sz <sz>
```

### Check funding rate before holding a perp position
> User: "Is the BTC perp funding rate high right now?"

```
1. okx-cex-market    okx market funding-rate BTC-USDT-SWAP   → current rate + next funding time
2. okx-cex-market    okx market funding-rate BTC-USDT-SWAP --history  → trend over recent periods
        ↓ decide whether to hold position
3. okx-cex-portfolio okx account positions                   → check existing exposure
```

### Research market before creating a grid bot
> User: "I want to set up a BTC grid bot — what's the recent range?"

```
1. okx-cex-market    okx market candles BTC-USDT --bar 4H --limit 50  → recent OHLCV for range
2. okx-cex-market    okx market ticker BTC-USDT                        → current price
3. okx-cex-market    okx market orderbook BTC-USDT --sz 20             → liquidity check
        ↓ decide minPx / maxPx
4. okx-cex-bot       okx bot grid create --instId BTC-USDT ...
```

### Compare perp vs spot premium
> User: "Is there a premium between BTC spot and BTC perp?"

```
1. okx-cex-market    okx market ticker BTC-USDT              → spot last price
2. okx-cex-market    okx market ticker BTC-USDT-SWAP         → perp last price
3. okx-cex-market    okx market mark-price --instType SWAP --instId BTC-USDT-SWAP  → mark price
```

### Discover and price an option
> User: "What's the price of a BTC call option expiring this week?"

```
1. okx-cex-market    okx market open-interest --instType OPTION --instId BTC-USD  → list active option instIds
        ↓ pick target instId from the list (e.g., BTC-USD-250328-95000-C)
2. okx-cex-market    okx market ticker BTC-USD-250328-95000-C → option last price and stats
3. okx-cex-market    okx market orderbook BTC-USD-250328-95000-C → bid/ask spread
```

> **Note**: `okx market instruments --instType OPTION` requires `--uly <underlying>` (e.g., `--uly BTC-USD`). If the underlying is unknown, use `open-interest` first to discover active option instIds.

## Operation Flow

### Step 1: Identify the data needed

- Current price → `okx market ticker`
- All prices for a category → `okx market tickers`
- Order book depth → `okx market orderbook`
- Price history/chart → `okx market candles`
- Funding cost → `okx market funding-rate`
- Contract valuation → `okx market mark-price` or `okx market price-limit`
- Market volume/OI → `okx market open-interest`
- What instruments exist → `okx market instruments`

### Step 2: Run commands immediately

All market data commands are read-only — no confirmation needed.

- `--instType` values: `SPOT`, `SWAP`, `FUTURES`, `OPTION`
- `--bar` values: `1m`, `3m`, `5m`, `15m`, `30m`, `1H`, `2H`, `4H`, `6H`, `12H`, `1D`, `1W`, `1M`
- `--limit`: number of results (default varies per endpoint, typically 100)
- `--history`: for `funding-rate`, returns historical records instead of current rate

### Step 3: No writes — no verification needed

All commands in this skill are read-only. No post-execution verification required.

## CLI Command Reference

### Ticker — Single Instrument

```bash
okx market ticker <instId> [--json]
```

Returns: `last`, `24h high/low`, `24h volume`, `sodUtc8` (24h change %).

---

### Tickers — All Instruments of a Type

```bash
okx market tickers <instType> [--json]
```

| Param | Required | Values | Description |
|---|---|---|---|
| `instType` | Yes | `SPOT`, `SWAP`, `FUTURES`, `OPTION` | Instrument type |

Returns table: `instId`, `last`, `high24h`, `low24h`, `vol24h`.

---

### Instruments — List Tradeable Instruments

```bash
okx market instruments --instType <type> [--instId <id>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--instType` | Yes | - | `SPOT`, `SWAP`, `FUTURES`, `OPTION` |
| `--instId` | No | - | Filter to a single instrument |

Returns: `instId`, `ctVal`, `lotSz`, `minSz`, `tickSz`, `state`. Displays up to 50 rows.

---

### Order Book

```bash
okx market orderbook <instId> [--sz <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `instId` | Yes | - | Instrument ID (e.g., `BTC-USDT-SWAP`) |
| `--sz` | No | 5 | Depth levels per side (1–400) |

Displays top 5 asks (ascending) and bids (descending) with price and size.

---

### Candles — OHLCV

```bash
okx market candles <instId> [--bar <bar>] [--limit <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `instId` | Yes | - | Instrument ID |
| `--bar` | No | `1m` | Time granularity (`1m`, `1H`, `4H`, `1D`, etc.) |
| `--limit` | No | 100 | Number of candles to return |

Returns columns: `time`, `open`, `high`, `low`, `close`, `vol`.

---

### Index Candles

```bash
okx market index-candles <instId> [--bar <bar>] [--limit <n>] [--history] [--json]
```

Same params as `candles`. Use index instrument IDs like `BTC-USD` (not `BTC-USDT`).

---

### Funding Rate

```bash
okx market funding-rate <instId> [--history] [--limit <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `instId` | Yes | - | SWAP instrument (e.g., `BTC-USDT-SWAP`) |
| `--history` | No | false | Return historical funding rates |
| `--limit` | No | - | Number of historical records |

Current (no `--history`): returns `fundingRate`, `nextFundingRate`, `fundingTime`, `nextFundingTime`.
Historical (`--history`): table with `fundingRate`, `realizedRate`, `fundingTime`.

---

### Recent Trades

```bash
okx market trades <instId> [--limit <n>] [--json]
```

Returns: `tradeId`, `px`, `sz`, `side`, `ts`.

---

### Mark Price

```bash
okx market mark-price --instType <type> [--instId <id>] [--json]
```

Returns: `instId`, `instType`, `markPx`, `ts`. Used for liquidation price calculation and contract valuation.

---

### Index Ticker

```bash
okx market index-ticker [--instId <id>] [--quoteCcy <ccy>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--instId` | Cond. | - | Index ID (e.g., `BTC-USD`) |
| `--quoteCcy` | Cond. | - | Filter by quote currency (e.g., `USD`, `USDT`) |

Returns: `idxPx`, `high24h`, `low24h`.

---

### Price Limit

```bash
okx market price-limit <instId> [--json]
```

Returns: `buyLmt` (max buy price), `sellLmt` (min sell price). Applies to SWAP and FUTURES only.

---

### Open Interest

```bash
okx market open-interest --instType <type> [--instId <id>] [--json]
```

Returns: `oi` (contracts), `oiCcy` (base currency amount), `ts`.

---

## MCP Tool Reference

| Tool | Description |
|---|---|
| `market_get_ticker` | Single instrument ticker |
| `market_get_tickers` | All tickers for instType |
| `market_get_instruments` | List instruments |
| `market_get_orderbook` | Order book depth |
| `market_get_candles` | OHLCV candles |
| `market_get_index_candles` | Index OHLCV candles |
| `market_get_funding_rate` | Funding rate (current or history) |
| `market_get_trades` | Recent public trades |
| `market_get_mark_price` | Mark price for contracts |
| `market_get_index_ticker` | Index price ticker |
| `market_get_price_limit` | Price limits for contracts |
| `market_get_open_interest` | Open interest |

---

## Input / Output Examples

**"What's the price of BTC?"**
```bash
okx market ticker BTC-USDT
# → instId: BTC-USDT | last: 95000.5 | 24h change %: +1.2% | 24h high: 96000 | 24h low: 93000
```

**"Show me all SWAP tickers"**
```bash
okx market tickers SWAP
# → table of all perpetual contracts with last price, 24h high/low/vol
```

**"What's the BTC/USDT order book look like?"**
```bash
okx market orderbook BTC-USDT
# Asks (price / size):
#          95100.0  2.5
#          95050.0  1.2
# Bids (price / size):
#          95000.0  3.1
#          94950.0  0.8
```

**"Show me BTC 4H candles for the last 30 periods"**
```bash
okx market candles BTC-USDT --bar 4H --limit 30
# → table: time, open, high, low, close, vol
```

**"What's the current funding rate for BTC perp?"**
```bash
okx market funding-rate BTC-USDT-SWAP
# → fundingRate: 0.0001 | nextFundingRate: 0.00012 | fundingTime: ... | nextFundingTime: ...
```

**"Show historical funding rates for ETH perp"**
```bash
okx market funding-rate ETH-USDT-SWAP --history --limit 20
# → table: fundingRate, realizedRate, fundingTime
```

**"What's the open interest on BTC perp?"**
```bash
okx market open-interest --instType SWAP --instId BTC-USDT-SWAP
# → oi: 125000 | oiCcy: 125000 | ts: ...
```

**"List all available SPOT instruments"**
```bash
okx market instruments --instType SPOT
# → table: instId, ctVal, lotSz, minSz, tickSz, state (up to 50 rows)
```

## Edge Cases

- **instId format**: SPOT uses `BTC-USDT`; SWAP uses `BTC-USDT-SWAP`; FUTURES uses `BTC-USDT-250328`; OPTION uses `BTC-USD-250328-95000-C`; Index uses `BTC-USD`
- **OPTION instruments — cannot list directly**: `okx market instruments --instType OPTION` requires `--uly BTC-USD` (underlying). If the underlying is unknown, run `okx market open-interest --instType OPTION` first to discover active option instIds from the results, then use those instIds with `okx market ticker <instId>`
- **No data returned**: instrument may be delisted or instId is wrong — verify with `okx market instruments`
- **funding-rate**: only applies to SWAP instruments; returns error for SPOT/FUTURES
- **price-limit**: only applies to SWAP and FUTURES instruments
- **mark-price**: available for SWAP, FUTURES, OPTION; not applicable to SPOT
- **candles --bar**: use uppercase `H`, `D`, `W`, `M` for hour/day/week/month (e.g., `1H` not `1h`)
- **index-ticker**: use `BTC-USD` format (not `BTC-USDT`) for index IDs
- **orderbook --sz**: max depth is 400; default display shows top 5 per side regardless of `--sz`

## Global Notes

- All market data commands are public — no API key required
- `--json` returns raw OKX API v5 response for programmatic use
- `--profile <name>` has no effect on market commands (no auth needed)
- Rate limit: 20 requests per 2 seconds per IP for market data endpoints
- Candle data is sorted newest-first by default
- `vol24h` in tickers is in base currency (e.g., BTC for BTC-USDT)
