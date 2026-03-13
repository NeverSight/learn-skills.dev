---
name: blofin-trader
description: "Execute trades on BloFin exchange — place orders (market, limit, post_only, fok, ioc), cancel orders, batch operations, close positions, and manage TP/SL and algo/trigger orders. Requires authenticated API access with TRADE permission."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "💹"
    requires:
      bins:
        - node
      env:
        - BLOFIN_API_KEY
        - BLOFIN_API_SECRET
        - BLOFIN_PASSPHRASE
    primaryEnv: BLOFIN_API_KEY
auto_activate:
  - "buy btc"
  - "sell btc"
  - "place order"
  - "open long"
  - "open short"
  - "close position"
  - "stop loss"
  - "take profit"
  - "blofin trade"
  - "blofin order"
  - "limit order"
  - "market order"
---

# BloFin Trader

Execute trades on BloFin exchange. Supports market, limit, post-only, FOK, IOC orders, batch operations, TP/SL, and algo/trigger orders.

**CRITICAL: Always confirm order details with the user before placing any trade. Display the instrument, side, size, price, and estimated cost/margin before execution.**

## Order Basics

### Order Types

| Type | Description |
|------|-------------|
| `market` | Execute immediately at best available price |
| `limit` | Execute at specified price or better |
| `post_only` | Limit order that only adds liquidity (maker only); cancelled if it would match immediately |
| `fok` | Fill or Kill — must fill entirely immediately or cancel |
| `ioc` | Immediate or Cancel — fill what's possible immediately, cancel the rest |

### Position Sides

| Side | Position Side | Action |
|------|--------------|--------|
| `buy` | `long` | Open long / close short |
| `sell` | `short` | Open short / close long |
| `buy` | `short` | Close short (in hedge mode) |
| `sell` | `long` | Close long (in hedge mode) |

### Size & Contract Value

- Order `size` is in **contracts**, not in base currency
- Each contract has a `contractValue` (check via `get_instruments`)
- Example: BTC-USDT contract value is 0.001 BTC, so 100 contracts = 0.1 BTC
- Minimum order size is defined by `minSize` (e.g., 0.1 contracts for BTC-USDT)
- Size must be a multiple of `lotSize`

## Available Tools (via blofin-mcp)

### place_order — Place a Single Order

```
Use place_order to submit a new trade. ALWAYS confirm with the user first.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID, e.g. `BTC-USDT` |
| `marginMode` | String | Yes | `cross` or `isolated` |
| `positionSide` | String | Yes | `long`, `short`, or `net` |
| `side` | String | Yes | `buy` or `sell` |
| `orderType` | String | Yes | `market`, `limit`, `post_only`, `fok`, `ioc` |
| `size` | String | Yes | Order size in contracts |
| `price` | String | Conditional | Required for limit/post_only/fok/ioc orders |
| `reduceOnly` | Boolean | No | If true, only reduces existing position |
| `clientOrderId` | String | No | Custom order ID (max 32 chars) |
| `tpTriggerPrice` | String | No | Take-profit trigger price |
| `tpOrderPrice` | String | No | TP order price (-1 for market) |
| `slTriggerPrice` | String | No | Stop-loss trigger price |
| `slOrderPrice` | String | No | SL order price (-1 for market) |
| `brokerId` | String | No | Broker ID if applicable |

**Example prompts:**
- "Buy 1 BTC-USDT contract at market price"
- "Place a limit buy for 10 ETH-USDT at $3,000"
- "Open a 5x long BTC position with 100 contracts"
- "Short ETH-USDT with a stop loss at $4,000"

**Pre-order checklist (always do this before placing):**
1. Confirm instrument exists and is live (`get_instruments`)
2. Verify user has sufficient balance (`get_balance`)
3. Check current leverage setting (`get_leverage_info`)
4. For limit orders, compare price to current market (`get_tickers`)
5. Calculate estimated cost: `size * contractValue * price / leverage`
6. Display order summary and get explicit user confirmation

---

### cancel_order — Cancel an Order

```
Use cancel_order to cancel a pending order.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID |
| `orderId` | String | Conditional | Order ID (either orderId or clientOrderId required) |
| `clientOrderId` | String | Conditional | Client order ID |

---

### batch_orders — Place Multiple Orders

```
Use batch_orders for placing multiple orders at once. Max 20 orders per batch.
```

All orders in a batch must share the same `instId` and `marginMode`.

**Example prompts:**
- "Place a grid of limit orders for BTC-USDT from $60,000 to $65,000"
- "Open both a long and short position on ETH"

---

### cancel_batch_orders — Cancel Multiple Orders

```
Use cancel_batch_orders to cancel multiple orders at once.
```

All cancellations should use the same identifier type (prefer `orderId`).

---

### close_position — Close an Entire Position

```
Use close_position to close a full position on an instrument. Confirm with the user first.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID |
| `marginMode` | String | Yes | `cross` or `isolated` |
| `positionSide` | String | No | `long`, `short`, or `net` |
| `clientOrderId` | String | No | Custom order ID |

**Example prompts:**
- "Close my BTC-USDT long position"
- "Close all my ETH positions"

---

### get_open_orders — View Pending Orders

```
Use get_open_orders to see unfilled or partially filled orders.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | No | Filter by instrument |
| `orderType` | String | No | Filter by order type |
| `state` | String | No | `live` or `partially_filled` |
| `before` / `after` | String | No | Pagination by orderId |
| `limit` | String | No | Max 100, default 100 |

---

### get_order_detail — Single Order Details

```
Use get_order_detail to check the status of a specific order.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID |
| `orderId` | String | Conditional | Order ID |
| `clientOrderId` | String | Conditional | Client order ID |

---

### get_order_history — Past Orders

```
Use get_order_history to review filled, cancelled, or expired orders.
```

---

## Take-Profit / Stop-Loss (TP/SL)

### place_tpsl — Attach TP/SL to a Position

```
Use place_tpsl to set take-profit and/or stop-loss on an existing position.
Always confirm trigger prices with the user.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID |
| `marginMode` | String | Yes | `cross` or `isolated` |
| `positionSide` | String | Yes | `long`, `short`, or `net` |
| `tpTriggerPrice` | String | Conditional | Take-profit trigger price |
| `tpOrderPrice` | String | No | TP execution price (-1 for market) |
| `slTriggerPrice` | String | Conditional | Stop-loss trigger price |
| `slOrderPrice` | String | No | SL execution price (-1 for market) |
| `size` | String | No | Size to close (default: full position) |

**TP/SL validation rules:**
- Long position: TP trigger > current price, SL trigger < current price
- Short position: TP trigger < current price, SL trigger > current price
- Always verify against current market price before placing

**Example prompts:**
- "Set a take profit at $70,000 and stop loss at $60,000 for my BTC long"
- "Add a stop loss at $3,200 for my ETH short"

### cancel_tpsl — Cancel TP/SL Orders

```
Use cancel_tpsl to remove existing TP/SL orders.
```

### get_pending_tpsl / get_tpsl_history — View TP/SL Orders

```
Use get_pending_tpsl to see active TP/SL orders.
Use get_tpsl_history to review past TP/SL orders.
```

---

## Algo / Trigger Orders

### place_algo_order — Conditional/Trigger Orders

```
Use place_algo_order for trigger-based orders that execute when a condition is met.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID |
| `marginMode` | String | Yes | `cross` or `isolated` |
| `positionSide` | String | Yes | `long`, `short`, or `net` |
| `side` | String | Yes | `buy` or `sell` |
| `orderType` | String | Yes | Order type for execution |
| `size` | String | Yes | Size in contracts |
| `triggerPrice` | String | Yes | Price that triggers the order |
| `orderPrice` | String | Conditional | Execution price (required for limit) |
| `reduceOnly` | Boolean | No | Only reduces position |

### cancel_algo_order / get_pending_algo_orders / get_algo_order_history

Manage and review algo/trigger orders.

---

## Safety Rules

1. **NEVER place an order without explicit user confirmation** — always show a summary first
2. **Double-check the side** (buy/sell) and position side (long/short) — mistakes are costly
3. **Verify sufficient balance** before placing orders
4. **Validate limit prices** against current market to avoid obvious errors
5. **Warn about high-leverage orders** — clearly state the liquidation risk
6. **For large orders**, check order book depth to estimate slippage
7. **Rate limit awareness**: Trading APIs are limited to 30 requests per 10 seconds per user
