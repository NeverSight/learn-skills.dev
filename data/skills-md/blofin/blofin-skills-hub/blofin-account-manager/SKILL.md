---
name: blofin-account-manager
description: "Manage BloFin futures account — check balances, view positions, configure leverage, margin mode, and position mode. Requires authenticated BloFin API access."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "👤"
    requires:
      bins:
        - node
      env:
        - BLOFIN_API_KEY
        - BLOFIN_API_SECRET
        - BLOFIN_PASSPHRASE
    primaryEnv: BLOFIN_API_KEY
auto_activate:
  - "blofin account"
  - "blofin balance"
  - "blofin position"
  - "my positions"
  - "my balance"
  - "set leverage"
  - "margin mode"
---

# BloFin Account Manager

Manage your BloFin futures trading account — balances, positions, leverage, margin mode, and account configuration. All tools require authenticated API access.

## Available Tools (via blofin-mcp)

### get_balance — Futures Account Balance

Check your futures trading account balance.

```
Use get_balance to check account funds.
```

**Key response fields:**
- `totalEquity` — Total account equity in USD
- `isolatedEquity` — Equity in isolated margin positions
- `details` array per currency:
  - `currency`, `equity`, `balance`, `availableEquity`, `available`
  - `frozen`, `orderFrozen` — Funds locked in orders
  - `unrealizedPnl` — Current unrealized profit/loss
  - `isolatedUnrealizedPnl` — Isolated position unrealized PnL

**Example prompts:**
- "What's my BloFin account balance?"
- "How much available margin do I have?"
- "Show my unrealized PnL"

---

### get_positions — Open Positions

View all currently open positions.

```
Use get_positions to see current open positions.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | No | Filter by instrument, e.g. `BTC-USDT` |

**Key response fields:**
- `instId` — Instrument
- `positionSide` — `long`, `short`, or `net`
- `positions` — Position size (contracts)
- `availablePositions` — Closeable position size
- `averagePrice` — Average entry price
- `unrealizedPnl` — Unrealized profit/loss
- `unrealizedPnlRatio` — PnL percentage
- `leverage` — Current leverage
- `marginMode` — `cross` or `isolated`
- `liquidationPrice` — Estimated liquidation price
- `margin` — Position margin
- `markPrice` — Current mark price

**Example prompts:**
- "Show all my open positions"
- "What's my BTC position?"
- "Am I in profit or loss?"
- "How close am I to liquidation?"

---

### get_leverage_info — View Leverage

Check current leverage settings for an instrument.

```
Use get_leverage_info to see the current leverage configuration.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID, e.g. `BTC-USDT` |
| `marginMode` | String | Yes | `cross` or `isolated` |

**Example prompts:**
- "What leverage am I using for BTC-USDT?"
- "Show my leverage settings"

---

### set_leverage — Adjust Leverage

Change the leverage for a specific instrument.

```
Use set_leverage to adjust leverage. Confirm with the user before applying changes.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID, e.g. `BTC-USDT` |
| `leverage` | String | Yes | Leverage value, e.g. `10` |
| `marginMode` | String | Yes | `cross` or `isolated` |
| `positionSide` | String | No | `long` or `short` (for hedge mode) |

**Important constraints:**
- Max leverage varies by instrument (check via `get_instruments` → `maxLeverage`)
- Cannot change leverage while there are pending cross orders (error 110006)
- May need to cancel open orders and close positions first (error 110019)

**Example prompts:**
- "Set my BTC-USDT leverage to 10x"
- "Lower my ETH leverage to 5x isolated"
- "What's the maximum leverage I can use for SOL-USDT?"

---

### get_margin_mode / set_margin_mode — Margin Mode

View or change between cross and isolated margin modes.

```
Use get_margin_mode / set_margin_mode to manage margin mode.
Always confirm with the user before switching margin mode.
```

**Parameters (set):**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `instId` | String | Yes | Instrument ID |
| `marginMode` | String | Yes | `cross` or `isolated` |

**Margin mode comparison:**

| Feature | Cross | Isolated |
|---------|-------|----------|
| Margin sharing | Shared across positions | Per-position |
| Liquidation risk | All positions affected | Only the isolated position |
| Capital efficiency | Higher | Lower |
| Risk control | Less granular | More granular |

**Example prompts:**
- "Switch BTC-USDT to isolated margin"
- "What margin mode am I using for ETH?"

---

### get_position_mode / set_position_mode — Position Mode

View or change between one-way and hedge position modes.

```
Use get_position_mode / set_position_mode to manage position mode.
Always confirm with the user before switching.
```

**Parameters (set):**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `positionMode` | String | Yes | `long_short_mode` (hedge) or `net_mode` (one-way) |

**Position mode comparison:**

| Mode | Description |
|------|-------------|
| `net_mode` | One-way mode. Can only hold one direction per instrument. |
| `long_short_mode` | Hedge mode. Can hold both long and short positions simultaneously. |

---

### get_account_config — Account Configuration

Get the overall account configuration settings.

```
Use get_account_config to review account settings.
```

**Example prompts:**
- "Show my BloFin account configuration"
- "What position mode am I using?"

## Safety Rules

1. **Always confirm with the user** before changing leverage, margin mode, or position mode
2. **Warn about liquidation risk** when leverage is set above 20x
3. **Check for open positions** before changing margin mode (may fail with existing positions)
4. **Display unrealized PnL** prominently when showing positions — users need to know their current risk exposure
