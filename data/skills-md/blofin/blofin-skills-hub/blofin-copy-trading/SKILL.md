---
name: blofin-copy-trading
description: "Manage BloFin copy trading — view copy trading account, positions, orders, and lead trader operations. Supports both follower and lead trader workflows. Requires authenticated API access."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "👥"
    requires:
      bins:
        - node
      env:
        - BLOFIN_API_KEY
        - BLOFIN_API_SECRET
        - BLOFIN_PASSPHRASE
    primaryEnv: BLOFIN_API_KEY
auto_activate:
  - "copy trading"
  - "copy trade"
  - "lead trader"
  - "follow trader"
  - "blofin copy"
---

# BloFin Copy Trading

Manage copy trading operations on BloFin — both as a follower and as a lead trader. Copy trading allows users to automatically replicate the trades of experienced traders.

## Overview

BloFin copy trading has two roles:

| Role | Description |
|------|-------------|
| **Follower** | Automatically copies trades from lead traders |
| **Lead Trader** | Trades are copied by followers; earns profit sharing |

Copy trading uses a dedicated account (`copy_trading`), separate from the main futures account.

**WebSocket:** `wss://openapi.blofin.com/ws/copytrading/private`

---

## Follower Workflows

### 1. Copy Trading Account Overview

Check copy trading account status:

1. **Get copy trading balance** — check funds in copy trading account
2. **Get copy trading positions** — view positions opened via copy trading
3. **Present account summary:**

```
Copy Trading Account
====================
Total Equity: $X,XXX
Available: $X,XXX

Active Positions:
| Instrument | Side | Size | Entry | PnL | Lead Trader |
|------------|------|------|-------|-----|-------------|
```

**Example prompts:**
- "Show my copy trading account"
- "What positions do I have from copy trading?"
- "How much is in my copy trading account?"

---

### 2. Fund Copy Trading Account

Transfer funds to start copy trading:

1. Use `get_asset_balances` with `accountType: "funding"` to check available funds
2. Use `fund_transfer` with `toAccount: "copy_trading"` to move funds

```
To start copy trading:
1. Transfer USDT from funding to copy_trading account
2. Select lead traders to follow on the BloFin platform
3. Set your copy parameters (amount per trade, max positions, etc.)
```

**Example prompts:**
- "Transfer 500 USDT to my copy trading account"
- "How much do I need to start copy trading?"

---

### 3. Monitor Copy Trading Performance

Track how your copy trades are performing:

1. Get copy trading positions and PnL
2. Review copy trading order history
3. Compare performance across different lead traders

**Example prompts:**
- "How are my copy trades performing?"
- "Show my copy trading profit and loss"
- "Which lead trader is making me the most money?"

---

## Lead Trader Workflows

### 4. Lead Trader Account Management

For users operating as lead traders:

**Copy Trading REST API endpoints (Lead Trader):**

- **Get Account** — View lead trader account balance and equity
- **Get Positions** — View positions that are being copied by followers
- **Place Order** — Place trades (with `brokerId` if applicable)
- **Close Position** — Close positions (followers' positions close proportionally)
- **Get Open Orders / Order History** — View and manage orders
- **Set Leverage** — Adjust leverage (affects followers' positions)
- **TP/SL Management** — Set take-profit and stop-loss on positions

**Example prompts:**
- "Show my lead trader account"
- "What positions are my followers copying?"
- "Place a BTC long for my copy trading followers"

---

### 5. Lead Trader Order Management

Place and manage orders as a lead trader:

**Place Order Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID |
| `marginMode` | String | Yes | `cross` or `isolated` |
| `positionSide` | String | Yes | `long`, `short`, or `net` |
| `side` | String | Yes | `buy` or `sell` |
| `orderType` | String | Yes | `market`, `limit`, `post_only`, `fok`, `ioc` |
| `size` | String | Yes | Size in contracts |
| `price` | String | Conditional | Required for limit orders |
| `brokerId` | String | No | Broker ID if applicable |

**Example prompts:**
- "Open a BTC long position for copy trading"
- "Close my ETH short in copy trading"
- "Set stop loss at $60,000 for my copy trading BTC position"

---

### 6. Lead Trader Risk Management

Manage risk for both yourself and your followers:

1. **Set appropriate leverage** — affects all followers
2. **Use TP/SL** — protects followers' capital too
3. **Monitor position sizes** — be aware of total follower exposure

**Example prompts:**
- "Set 5x leverage for BTC in copy trading"
- "Add stop loss to all my copy trading positions"

---

## Copy Trading WebSocket Channels

For real-time updates, subscribe to copy trading private channels:

| Channel | Description |
|---------|-------------|
| `copytrading-positions` | Real-time position updates |
| `copytrading-orders` | Order fills and status changes |
| `copytrading-account` | Account balance and equity updates |

**Account channel push data includes:**
- `totalEquity`, `isolatedEquity`
- Per-currency details: `equity`, `balance`, `available`, `frozen`, `unrealizedPnl`

---

## Best Practices

1. **Start small** — begin with a small allocation to test lead traders before committing more
2. **Diversify** — follow multiple lead traders to spread risk
3. **Monitor regularly** — copy trading is not fully passive; check performance and adjust
4. **Set risk limits** — configure maximum loss per lead trader and per trade
5. **Understand fees** — lead traders may take a percentage of profits
6. **As a lead trader** — always use TP/SL to protect followers' capital; maintain consistent strategy
7. **Transfer back** — when stopping copy trading, transfer funds back to funding account via `fund_transfer`
