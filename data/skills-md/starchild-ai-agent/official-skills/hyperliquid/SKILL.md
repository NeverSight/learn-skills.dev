---
name: hyperliquid
version: 1.0.0
description: Trade perpetual futures and spot on Hyperliquid DEX
tools:
  - hl_account
  - hl_balances
  - hl_open_orders
  - hl_market
  - hl_orderbook
  - hl_fills
  - hl_candles
  - hl_funding
  - hl_order
  - hl_spot_order
  - hl_tpsl_order
  - hl_cancel
  - hl_cancel_all
  - hl_modify
  - hl_leverage
  - hl_transfer_usd
  - hl_withdraw
  - hl_deposit
metadata:
  starchild:
    emoji: "📈"
    skillKey: hyperliquid
    requires:
      env: [WALLET_SERVICE_URL]
user-invocable: true
disable-model-invocation: false
---

# Hyperliquid Trading

Trade perpetual futures and spot tokens on Hyperliquid, a fully on-chain decentralized exchange. Orders are signed using this agent's EVM wallet and submitted directly to the Hyperliquid L1.

## Prerequisites

Before trading, the wallet policy must be active. Load the **wallet-policy** skill and propose the standard wildcard policy (deny key export + allow `*`). This covers all Hyperliquid operations — USDC deposits, EIP-712 order signing, and withdrawals.

## Available Tools

### Account & Market Info

| Tool | What it does |
|------|--------------|
| `hl_total_balance` | Check how much you can trade with (use this for balance checks!) |
| `hl_account` | See your open positions and PnL |
| `hl_balances` | See your token holdings (USDC, HYPE, etc.) |
| `hl_market` | Get current prices for crypto or stocks |
| `hl_orderbook` | Check order book depth and liquidity |
| `hl_fills` | See recent trade fills and execution prices |
| `hl_candles` | Get price charts (1m, 5m, 1h, 4h, 1d) |
| `hl_funding` | Check funding rates for perps |
| `hl_open_orders` | See pending orders |

### Trading

| Tool | What it does |
|------|--------------|
| `hl_order` | Buy or sell perps (crypto/stocks) |
| `hl_spot_order` | Buy or sell spot tokens |
| `hl_tpsl_order` | Place stop loss or take profit orders |
| `hl_leverage` | Set leverage (1x to asset max) |
| `hl_cancel` | Cancel a specific order |
| `hl_cancel_all` | Cancel all open orders |
| `hl_modify` | Change order price or size |

### Funds

| Tool | What it does |
|------|--------------|
| `hl_deposit` | Add USDC from Arbitrum (min $5) |
| `hl_withdraw` | Send USDC to Arbitrum (1 USDC fee, ~5 min) |
| `hl_transfer_usd` | Move USDC between spot/perp (rarely needed) |

---

## Quick Start

Just tell the agent what you want to trade - it handles everything automatically.

**Examples:**

```
User: "Buy $20 of Bitcoin with 5x leverage"
Agent: [checks balance → sets leverage → places order → reports fill]
Result: "✓ Bought 0.0002 BTC at $95,432 with 5x leverage. Position opened."

User: "Long NVIDIA with $50, 10x"
Agent: [auto-detects NVIDIA = xyz:NVDA → executes → verifies]
Result: "✓ Bought 0.25 NVDA at $198.50 with 10x leverage. Filled at $198.62."

User: "Sell my ETH position"
Agent: [checks position size → closes → reports PnL]
Result: "✓ Sold 0.5 ETH at $3,421. Realized PnL: +$12.50"
```

**You don't need to:**
- Understand account modes or fund transfers
- Check balances manually (agent does it)
- Calculate position sizes (agent does it)
- Verify fills (agent does it)

**Just say what you want, the agent handles the rest.**

---

## Agent Behavior Guidelines

**🤖 As the agent, you should ALWAYS do these automatically (never ask the user):**

1. **Check available funds** - Use `hl_total_balance` before EVERY trade to see total available margin
2. **Detect asset type** - Recognize if user wants crypto (BTC, ETH, SOL) or stocks/RWA (NVIDIA→xyz:NVDA, TESLA→xyz:TSLA)
3. **Set leverage** - Always call `hl_leverage` before placing orders (unless user specifies not to)
4. **Verify fills** - After placing ANY order, immediately call `hl_fills` to check if it filled
5. **Report results** - Tell user the outcome: filled price, size, and any PnL
6. **Suggest risk management** - For leveraged positions, remind users about stop losses or offer to set them

**🎯 User just says:** "buy X" or "sell Y" or "long Z with $N"

**🔧 You figure out:**
- Current balance (hl_total_balance)
- Asset resolution (crypto vs RWA)
- Leverage settings (hl_leverage)
- Order sizing (calculate from user's $ amount or size)
- Execution (hl_order)
- Verification (hl_fills)
- Final report to user

**📊 Balance checking hierarchy:**
- ✅ Use `hl_total_balance` - shows ACTUAL available margin regardless of account mode
- ❌ Don't use `hl_account` for balance - may show $0 even if funds available
- ❌ Don't use `hl_balances` for margin - only shows spot tokens

**🚀 Be proactive, not reactive:**
- Don't wait for user to ask "did it fill?" - check automatically
- Don't ask "should I check your balance?" - just do it
- Don't explain account modes - user doesn't care, just execute

---

## Tool Usage Examples

### Check Account State

```
hl_account()              # Default crypto perps account
hl_account(dex="xyz")     # Builder dex (RWA/stock perps) account
```

Returns `marginSummary` (accountValue, totalMarginUsed, withdrawable) and `assetPositions` array with each position's coin, szi (signed size), entryPx, unrealizedPnl, leverage.

**Important:** Builder perps (xyz:NVDA, xyz:TSLA, etc.) have separate clearinghouses. Always check the correct dex when trading RWA/stock perps.

### Check Spot Balances

```
hl_balances()
```

Returns balances array with coin, hold, total for USDC and all spot tokens.

### Check Market Prices

```
hl_market()                  # All mid prices
hl_market(coin="BTC")        # BTC price + metadata (maxLeverage, szDecimals)
```

### Place a Perp Limit Order

```
hl_order(coin="BTC", side="buy", size=0.01, price=95000)
```

Places a GTC limit buy for 0.01 BTC at $95,000.

### Place a Perp Market Order

```
hl_order(coin="ETH", side="sell", size=0.1)
```

Omitting `price` submits an IoC order at mid price +/- 3% slippage.

### Place a Post-Only Order

```
hl_order(coin="BTC", side="buy", size=0.01, price=94000, order_type="alo")
```

ALO (Add Liquidity Only) = post-only. Rejected if it would immediately fill.

### Place a Stop Loss Order

```
hl_tpsl_order(coin="BTC", side="sell", size=0.01, trigger_px=90000, tpsl="sl")
```

Automatically sells 0.01 BTC if the price drops to $90,000. Executes as market order when triggered.

For a limit order when triggered (instead of market):

```
hl_tpsl_order(coin="BTC", side="sell", size=0.01, trigger_px=90000, tpsl="sl", is_market=false, limit_px=89900)
```

### Place a Take Profit Order

```
hl_tpsl_order(coin="ETH", side="sell", size=0.5, trigger_px=3500, tpsl="tp")
```

Automatically sells 0.5 ETH if the price rises to $3,500. Executes as market order when triggered.

### Close a Perp Position

```
hl_order(coin="BTC", side="sell", size=0.01, reduce_only=true)
```

Use `reduce_only=true` to ensure it only closes, never opens a new position.

### Place a Spot Order

```
hl_spot_order(coin="HYPE", side="buy", size=10, price=25.0)
```

Spot orders use the same interface — just specify the token name.

### Cancel an Order

```
hl_cancel(coin="BTC", order_id=12345678)
```

Get `order_id` from `hl_open_orders`.

### Cancel All Orders

```
hl_cancel_all()              # Cancel everything
hl_cancel_all(coin="BTC")    # Cancel only BTC orders
```

### Modify an Order

```
hl_modify(order_id=12345678, coin="BTC", side="buy", size=0.02, price=94500)
```

### Set Leverage

```
hl_leverage(coin="BTC", leverage=10)               # 10x cross margin
hl_leverage(coin="ETH", leverage=5, cross=false)    # 5x isolated margin
```

### Transfer USDC (rarely needed)

```
hl_transfer_usd(amount=1000, to_perp=true)     # Spot → Perp
hl_transfer_usd(amount=500, to_perp=false)      # Perp → Spot
```

Note: Usually not needed - funds are automatically shared. Only use if you get an error saying you need to transfer.

### Withdraw USDC to Arbitrum

```
hl_withdraw(amount=100)                              # Withdraw to own wallet
hl_withdraw(amount=50, destination="0xABC...")        # Withdraw to specific address
```

Fee: 1 USDC deducted by Hyperliquid. Processing takes ~5 minutes.

### Deposit USDC from Arbitrum

```
hl_deposit(amount=500)
```

Sends USDC from the agent's Arbitrum wallet to the Hyperliquid bridge contract. Minimum deposit: 5 USDC. Requires USDC balance on Arbitrum.

### Get Candles

```
hl_candles(coin="BTC", interval="1h", lookback=48)
```

Intervals: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`. Lookback in hours.

### Check Funding Rates

```
hl_funding()                 # All predicted fundings
hl_funding(coin="BTC")       # BTC predicted + 24h history
```

### Get Recent Fills

```
hl_fills(limit=10)
```

---

## Coin vs RWA Resolution

When a user asks to trade a ticker, you need to determine whether it's a **native crypto perp** (use plain name) or an **RWA/stock perp** (use `xyz:TICKER` prefix).

### Decision Workflow

1. **Known crypto** → use plain name: `"BTC"`, `"ETH"`, `"SOL"`, `"DOGE"`, `"HYPE"`, etc.
2. **Known stock/commodity/forex** → use `xyz:` prefix: `"xyz:NVDA"`, `"xyz:TSLA"`, `"xyz:GOLD"`, etc.
3. **Unsure** → resolve with tool calls:
   - First try `hl_market(coin="X")` — if it returns a price, it's a crypto perp
   - If not found, try `hl_market(dex="xyz")` to list all RWA markets and search the results
   - Use whichever returns a match

### Common RWA Categories (all use `xyz:` prefix)

| Category | Examples |
|----------|----------|
| **US Stocks** | `xyz:NVDA`, `xyz:TSLA`, `xyz:AAPL`, `xyz:MSFT`, `xyz:AMZN`, `xyz:GOOG`, `xyz:META`, `xyz:TSM` |
| **Commodities** | `xyz:GOLD`, `xyz:SILVER` |
| **Indices** | `xyz:SPY` |
| **Forex** | `xyz:EUR`, `xyz:GBP`, `xyz:JPY` |

> If a user says "buy NVDA" or "trade GOLD", use `xyz:NVDA` / `xyz:GOLD`. These are real-world assets, not crypto.

### Prefixed Name — Same Tools

All existing tools work with `xyz:TICKER` — just pass the prefixed coin name:

```
hl_market(coin="xyz:NVDA")                                    # Check NVIDIA stock perp price
hl_market(dex="xyz")                                           # List ALL available RWA/stock perps
hl_orderbook(coin="xyz:NVDA")                                 # Check liquidity
hl_leverage(coin="xyz:NVDA", leverage=3)                      # Set leverage (auto-isolated)
hl_order(coin="xyz:NVDA", side="buy", size=0.5, price=188)    # Limit buy 0.5 NVDA
hl_order(coin="xyz:TSM", side="buy", size=1)                  # Market buy 1 TSM
hl_cancel(coin="xyz:NVDA", order_id=12345678)                 # Cancel order
```

### Example: User Says "Buy NVIDIA"

1. Recognize NVIDIA = stock → use `xyz:NVDA`
2. `hl_market(coin="xyz:NVDA")` — Check current price, leverage limits
3. `hl_leverage(coin="xyz:NVDA", leverage=3)` — Set leverage (builder perps use isolated margin)
4. `hl_order(coin="xyz:NVDA", side="buy", size=0.5, price=188)` — Place limit buy
5. `hl_fills()` — Check if filled

### Notes

- Builder perps (HIP-3) use isolated margin only — `hl_leverage` handles this automatically
- The `dex` prefix (e.g. `xyz`) identifies which builder deployed the perp
- All tools (candles, orderbook, funding, etc.) work the same way with prefixed names

---

## Common Workflows

### Trade Crypto Perps (BTC, ETH, SOL, etc.)

User: "Buy BTC" or "Long ETH with 5x"

Agent workflow:
1. `hl_total_balance()` → Check available funds
2. `hl_leverage(coin="BTC", leverage=5)` → Set leverage
3. `hl_order(...)` → Place order
4. `hl_fills()` → Verify fill and report result

### Trade Stocks/RWA (NVIDIA, TESLA, GOLD, etc.)

User: "Buy NVIDIA" or "Short TESLA"

Agent workflow:
1. Detect asset type → Convert "NVIDIA" to "xyz:NVDA"
2. `hl_total_balance()` → Check available funds
3. `hl_leverage(coin="xyz:NVDA", leverage=10)` → Set leverage
4. `hl_order(coin="xyz:NVDA", ...)` → Place order
5. `hl_fills()` → Verify fill and report result

### Close Positions

User: "Close my BTC position"

Agent workflow:
1. `hl_account()` → Get current position size
2. `hl_order(coin="BTC", side="sell", size=X, reduce_only=true)` → Close position
3. `hl_fills()` → Report PnL

### Spot Trading

User: "Buy 100 HYPE tokens"

Agent workflow:
1. `hl_total_balance()` → Check available USDC
2. `hl_spot_order(coin="HYPE", side="buy", size=100)` → Buy tokens
3. `hl_balances()` → Verify purchase

### Deposit/Withdraw Funds

**Deposit:**
User: "Deposit $500 USDC to Hyperliquid"
Agent: `hl_deposit(amount=500)` → Done

**Withdraw:**
User: "Withdraw $100 to my Arbitrum wallet"
Agent: `hl_withdraw(amount=100)` → Done (5 min, 1 USDC fee)

---

## Order Types

| Type | Parameter | Behavior |
|------|-----------|----------|
| **Limit (GTC)** | `order_type="limit"` | Rests on book until filled or cancelled |
| **Market (IoC)** | omit `price` | Immediate-or-Cancel at mid +/- 3% slippage |
| **Post-Only (ALO)** | `order_type="alo"` | Rejected if it would cross the spread |
| **Fill-or-Kill** | `order_type="ioc"` + explicit price | Fill immediately at price or cancel |
| **Stop Loss** | `hl_tpsl_order` with `tpsl="sl"` | Triggers when price drops to limit losses |
| **Take Profit** | `hl_tpsl_order` with `tpsl="tp"` | Triggers when price rises to lock gains |

---

## Stop Loss & Take Profit Orders

Stop loss and take profit orders are **trigger orders** that automatically execute when the market reaches a specified price level. Use these to manage risk and lock in profits without monitoring positions 24/7.

### How They Work

1. **Order Placement**: Place a dormant trigger order with a trigger price
2. **Monitoring**: Order sits inactive, watching the market price
3. **Trigger**: When market price reaches `trigger_px`, order activates
4. **Execution**: Order executes immediately (as market or limit order)

### Stop Loss (SL)

**Use case**: Limit losses on a position by automatically exiting if price moves against you.

**Example**: You're long BTC at $95,000 and want to exit if it drops below $90,000.

```
hl_tpsl_order(coin="BTC", side="sell", size=0.1, trigger_px=90000, tpsl="sl")
```

- **trigger_px=90000**: Activates when BTC drops to $90k
- **side="sell"**: Closes your long position
- **tpsl="sl"**: Marks this as a stop loss order
- **Default**: Executes as market order when triggered (instant exit)

### Take Profit (TP)

**Use case**: Lock in gains by automatically exiting when price reaches your profit target.

**Example**: You're long ETH at $3,000 and want to take profit at $3,500.

```
hl_tpsl_order(coin="ETH", side="sell", size=1.0, trigger_px=3500, tpsl="tp")
```

- **trigger_px=3500**: Activates when ETH rises to $3,500
- **side="sell"**: Closes your long position
- **tpsl="tp"**: Marks this as a take profit order
- **Default**: Executes as market order when triggered (instant exit)

### Market vs Limit Execution

By default, TP/SL orders execute as **market orders** when triggered (instant fill, possible slippage).

For more control, use a **limit order** when triggered:

```
hl_tpsl_order(
    coin="BTC",
    side="sell",
    size=0.1,
    trigger_px=90000,
    tpsl="sl",
    is_market=false,
    limit_px=89900
)
```

- **trigger_px=90000**: Activates at $90k
- **is_market=false**: Use limit order (not market)
- **limit_px=89900**: Limit price when triggered ($89,900)

**Trade-off**: Limit orders avoid slippage but may not fill in fast-moving markets.

### Short Positions

For short positions, reverse the `side` parameter:

**Stop loss on short** (exit if price rises):
```
hl_tpsl_order(coin="BTC", side="buy", size=0.1, trigger_px=98000, tpsl="sl")
```

**Take profit on short** (exit if price drops):
```
hl_tpsl_order(coin="BTC", side="buy", size=0.1, trigger_px=92000, tpsl="tp")
```

### Best Practices

1. **Always use `reduce_only=true`** (default) - ensures TP/SL only closes positions, never opens new ones
2. **Match size to position** - TP/SL size should equal or be less than your position size
3. **Set both TP and SL** - protect both upside (take profit) and downside (stop loss)
4. **Account for volatility** - don't set stops too tight or they'll trigger on normal price swings
5. **Check open orders** - use `hl_open_orders` to verify TP/SL orders are active

### Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Wrong side | SL buys instead of sells | Long position → `side="sell"` for SL/TP |
| Size too large | TP/SL opens new position | Set `size` ≤ position size, use `reduce_only=true` |
| Trigger = limit | Confusion about prices | `trigger_px` = when to activate, `limit_px` = execution price |
| No SL on leverage | Liquidation risk | Always set stop loss on leveraged positions |

---

## Perps vs Spot

| Aspect | Perps | Spot |
|--------|-------|------|
| Tool | `hl_order` | `hl_spot_order` |
| Leverage | Yes (up to asset max) | No |
| Funding | Paid/received every hour | None |
| Short selling | Yes (native) | Must own tokens to sell |
| Check positions | `hl_account` | `hl_balances` |

---

## Risk Management

- **Always check account state before trading** — know your margin usage and existing positions
- **Set leverage explicitly** before opening new positions (default may vary)
- **Use reduce_only** when closing to avoid accidentally opening the opposite direction
- **Monitor funding rates** — high positive funding means longs are expensive to hold
- **Start with small sizes** — Hyperliquid has minimum order sizes per asset (check szDecimals)
- **Post-only (ALO) orders** save on fees (maker vs taker rates)
- **Check fills after market orders** — IoC orders may partially fill or not fill at all

---

## Common Errors

| Error | Fix |
|-------|-----|
| "Unknown perp asset" | Check coin name. Crypto: "BTC", "ETH". Stocks: "xyz:NVDA", "xyz:TSLA" |
| "Insufficient margin" | Use `hl_total_balance` to check funds. Reduce size or add more USDC |
| "Order must have minimum value of $10" | Increase size. Formula: `size × price ≥ $10` |
| "Size too small" | BTC min is typically 0.001. Check asset's szDecimals |
| "Order would cross" | ALO order rejected. Use regular limit order instead |
| "User or wallet does not exist" | Deposit USDC first with `hl_deposit(amount=500)` |
| "Minimum deposit is 5 USDC" | Hyperliquid requires at least $5 per deposit |
| "Policy violation" | Load wallet-policy skill and propose wildcard policy |
| "Action disabled when unified account is active" | Transfers blocked in unified mode (default). Just place orders directly |
