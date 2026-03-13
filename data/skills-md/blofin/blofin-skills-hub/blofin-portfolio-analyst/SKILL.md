---
name: blofin-portfolio-analyst
description: "Analyze your BloFin trading portfolio — PnL breakdown, trade history, fill analysis, performance metrics, and generate reports. Requires authenticated API access."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins:
        - node
      env:
        - BLOFIN_API_KEY
        - BLOFIN_API_SECRET
        - BLOFIN_PASSPHRASE
    primaryEnv: BLOFIN_API_KEY
auto_activate:
  - "portfolio"
  - "pnl"
  - "profit"
  - "loss"
  - "trade history"
  - "performance"
  - "fill history"
  - "trading report"
---

# BloFin Portfolio Analyst

Analyze trading performance, review trade history, compute PnL metrics, and generate portfolio reports.

## Core Analysis Workflows

### 1. Portfolio Snapshot

Build a comprehensive overview of the user's current portfolio state:

1. **Get account balance** via `get_balance` — total equity, available margin, unrealized PnL
2. **Get all positions** via `get_positions` — open positions with entry price, size, PnL
3. **Get current prices** via `get_tickers` for each held instrument
4. **Calculate and present:**
   - Total portfolio value (equity)
   - Unrealized PnL (absolute and percentage)
   - Per-position breakdown: instrument, side, size, entry price, current price, PnL, PnL%
   - Available margin and margin usage ratio
   - Largest winning and losing positions

**Example prompts:**
- "Give me a portfolio overview"
- "How is my portfolio doing?"
- "What's my total PnL?"

---

### 2. Trade History Analysis

Review past trades and compute performance metrics:

1. **Get trade fills** via `get_fills_history` — recent executed trades with fill prices
2. **Get order history** via `get_order_history` — all past orders including cancelled ones
3. **Analyze and present:**
   - Total trades in period
   - Win rate (trades with positive `fillPnl` vs total closing trades)
   - Average win size vs average loss size (profit factor)
   - Most traded instruments
   - Trading frequency patterns

**Parameters for get_fills_history:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | No | Filter by instrument |
| `orderId` | String | No | Filter by order |
| `before` / `after` | String | No | Pagination by tradeId |
| `begin` / `end` | String | No | Filter by timestamp (ms) |
| `limit` | String | No | Max 100, default 20 |

**Key fill response fields:** `instId`, `fillPrice`, `fillSize`, `fillPnl`, `positionSide`, `side`, `fee`, `ts`.

**Example prompts:**
- "Show my trade history for the last 7 days"
- "What's my win rate on BTC-USDT?"
- "Analyze my trading performance this month"

---

### 3. PnL Breakdown

Detailed profit and loss analysis:

1. **Realized PnL** — from `get_fills_history`, sum `fillPnl` for all closing trades
2. **Unrealized PnL** — from `get_positions`, current `unrealizedPnl`
3. **Fees paid** — from `get_fills_history`, sum `fee` fields
4. **Net PnL** = Realized PnL + Unrealized PnL - Total Fees
5. **Present per-instrument PnL table**

**Example prompts:**
- "Break down my PnL by instrument"
- "How much have I paid in fees?"
- "What's my net profit after fees?"

---

### 4. Spot Trade History (if applicable)

For users who also trade spot markets:

Use `get_fills_history` with spot-specific endpoints:
- Endpoint: `GET /api/v1/spot/trade/fills-history`
- Requires `instType: "SPOT"`

**Example prompts:**
- "Show my spot trading history"
- "Compare my spot and futures performance"

---

### 5. Performance Report Generation

Generate a structured trading performance report:

```
When asked for a report, compile data from multiple sources and present
a well-formatted summary with tables and key metrics.
```

**Report template:**

```
📈 BloFin Trading Report
========================
Period: [start_date] to [end_date]

## Account Summary
- Total Equity: $XXX
- Available Balance: $XXX
- Margin Usage: XX%

## Open Positions
| Instrument | Side | Size | Entry | Current | PnL | PnL% |
|------------|------|------|-------|---------|-----|------|

## Performance Metrics
- Total Trades: XX
- Win Rate: XX%
- Average Win: $XX
- Average Loss: $XX
- Profit Factor: X.XX
- Total Fees: $XX
- Net Realized PnL: $XX

## Top Performers
- Best trade: [instrument] +$XX
- Worst trade: [instrument] -$XX
```

**Example prompts:**
- "Generate a trading report for this week"
- "Give me a detailed performance analysis"
- "Create a summary of my trading activity"

## Analysis Guidelines

1. **Always include fees** in PnL calculations — they significantly impact real returns
2. **Use timestamps** to filter data to the user's requested time period
3. **Handle pagination** — if more than 100 records exist, make multiple requests with `before`/`after` parameters
4. **Present numbers clearly** — use currency formatting, percentages, and color-coding context (profit vs loss)
5. **Compare to entry** — always show PnL relative to entry price, not just absolute values
6. **Note data limitations** — fill history may be limited to recent data; inform the user if the requested period exceeds available data
