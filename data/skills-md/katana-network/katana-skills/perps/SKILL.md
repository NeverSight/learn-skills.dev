---
name: perps
description: Activate when the user asks about perpetual futures, perps, leveraged trading, order placement, funding rates, or position management on Katana Perps.
license: MIT
metadata:
  author: katana
  version: '1.1.0'
---

# Perps Trader — Katana Perps

Trade perpetual futures on Katana Perps — a non-custodial, cross-margined perpetual futures DEX with a central limit order book. This skill covers market data, position management, order placement, and withdrawals.

## When to Activate
- User asks about perpetual futures, perps, or leveraged trading on Katana
- User wants to check perps market data, prices, funding rates, or liquidations
- User wants to view their perps positions, orders, or fills
- User wants to place or cancel perps orders
- User wants to withdraw from the perps exchange

## Contract Addresses

| Item | Mainnet | Testnet |
|------|---------|---------|
| Exchange Contract | `0x835Ba5b1B202773A94Daaa07168b26B22584637a` | `0xcE3765616b9e354E64530875f492dc4DfddF2118` |

### EIP-712 Domain

| Field | Mainnet | Testnet |
|-------|---------|---------|
| name | `KatanaPerps` | `KatanaPerps` |
| version | `1.0.0` | `1.0.0-sandbox` |
| chainId | `747474` | `737373` |
| verifyingContract | `0x835Ba5b1B202773A94Daaa07168b26B22584637a` | `0xcE3765616b9e354E64530875f492dc4DfddF2118` |

## REST API

Base URLs:
- **Mainnet:** `https://api-perps.katana.network`
- **Testnet:** `https://api-perps-sandbox.katana.network`

### Public Endpoints (no auth needed)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v4/exchange` | GET | Exchange info — fees, volume, open interest, contract addresses, quote token (vbUSDC) |
| `/v4/markets` | GET | Market info — leverage limits, margin requirements, fees, index prices, funding |
| `/v4/tickers` | GET | 24h stats — OHLCV, bid/ask, mark/index prices |
| `/v4/orderbook?market={market}&level={1\|2}&limit={n}` | GET | Order book (L1 = best bid/ask, L2 = full depth) |
| `/v4/candles?market={market}&interval={interval}&limit={n}` | GET | OHLCV candles (intervals: 1m, 5m, 15m, 1h, 4h, 1d) |
| `/v4/trades?market={market}&limit={n}` | GET | Recent public trades |
| `/v4/liquidations?market={market}&limit={n}` | GET | Recent liquidation records |
| `/v4/fundingRates?market={market}&limit={n}` | GET | Historical funding rates (8h payment schedule) |
| `/v4/gasFees` | GET | Withdrawal gas fee estimates per destination chain |

### Authenticated Endpoints (require HMAC signature)

**Authentication:** Requires `PERPS_API_KEY` and `PERPS_API_SECRET`. Sign requests using HMAC-SHA256 of the request payload with the API secret.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v4/wallets?wallet={address}` | GET | Wallet state — equity, collateral, leverage, margin ratio |
| `/v4/positions?wallet={address}` | GET | Open positions — PnL, liquidation price, ADL risk |
| `/v4/orders?wallet={address}&closed={bool}` | GET | Open or historical orders with fills |
| `/v4/fills?wallet={address}&market={market}` | GET | Trade fill history — fees, PnL, maker/taker side |

### Trade Endpoints (require API key + EIP-712 wallet signature)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v4/orders` | POST | Create order — returns EIP-712 typed data for signing |
| `/v4/orders/cancel` | DELETE | Cancel by order IDs, market, or all |
| `/v4/withdrawals` | POST | Withdraw to Katana or cross-chain via Stargate |
| `/v4/wallets/associate` | POST | Associate wallet with API account (first-time setup) |

## On-Chain Interactions

### Depositing to Perps Exchange

The exchange collateral is **vbUSDC** (`0x203A662b0BD271A6ed5a60EdFbd04bFce608FD36`). To fund a trading account:

1. Call `approve(exchangeAddress, amount)` on the vbUSDC contract for the exchange contract
2. Call the exchange deposit function with the approved amount

Get the exact `exchangeContractAddress` and `quoteTokenAddress` from the `/v4/exchange` endpoint.

### Order Signing (EIP-712)

Orders use a **two-step flow:**

1. **Build:** POST to `/v4/orders` with order parameters → returns EIP-712 typed data
2. **Sign:** User signs the typed data with their wallet using the EIP-712 domain above
3. **Submit:** Re-POST with the `walletSignature` field to submit the signed order

The agent **never signs** — it constructs the request and returns the EIP-712 data for the user's wallet to sign.

## Key Concepts

### Collateral & Margin
- **Collateral:** vbUSDC only, cross-margined across all positions
- **Initial Margin Fraction (IMF):** Margin to open a position (determines max leverage)
- **Maintenance Margin Fraction (MMF):** Margin to avoid liquidation
- **Margin Ratio:** totalMaintenanceMarginReq / equity — liquidation when > 1
- Larger positions require higher IMF (incremental margin)

### Order Types
| Type | Description |
|------|-------------|
| `market` | Execute immediately at best price |
| `limit` | Execute at specified price or better |
| `stopLossMarket` | Market order triggered at stop price |
| `stopLossLimit` | Limit order triggered at stop price |
| `takeProfitMarket` | Market order triggered at take profit price |
| `takeProfitLimit` | Limit order triggered at take profit price |

### Time In Force
| Value | Description |
|-------|-------------|
| `gtc` | Good-til-canceled (default, rests on book) |
| `gtx` | Post-only / maker only (canceled if crosses spread) |
| `ioc` | Immediate-or-cancel (fill what you can, cancel rest) |
| `fok` | Fill-or-kill (entire quantity or nothing) |

### Funding Payments
- Every 8 hours: 00:00, 08:00, 16:00 UTC
- Positive rate → longs pay shorts; negative → shorts pay longs
- Incentivizes order book price to converge with index price

### Precision
- All prices and quantities: 8 decimal zero-padded strings (e.g., `"2500.05000000"`)

## Key Workflows

### 1. Check Market Overview
1. GET `/v4/markets` — see all markets, leverage, fees
2. GET `/v4/tickers` — 24h stats, current bid/ask, funding
3. GET `/v4/orderbook?market=ETH-USD&level=2&limit=10` — order book depth

### 2. Analyze a Market
1. GET `/v4/candles?market=ETH-USD&interval=1h&limit=24` — price history
2. GET `/v4/trades?market=ETH-USD&limit=20` — recent trades
3. GET `/v4/fundingRates?market=ETH-USD&limit=10` — funding history
4. GET `/v4/liquidations?market=ETH-USD&limit=10` — recent liquidations

### 3. Monitor Positions
1. GET `/v4/wallets?wallet=0x...` — equity, margin, leverage
2. GET `/v4/positions?wallet=0x...` — all positions with PnL
3. GET `/v4/orders?wallet=0x...&closed=false` — open orders
4. GET `/v4/fills?wallet=0x...&market=ETH-USD` — fill history

### 4. Place an Order
1. POST `/v4/orders` with: wallet, market (`"ETH-USD"`), type (`"limit"`), side (`"buy"`), quantity (`"1.00000000"`), price (`"2400.00000000"`), timeInForce (`"gtc"`)
2. Returns EIP-712 typed data → user signs with wallet
3. Re-POST with `walletSignature` to submit

To earn a fee share on the orders your product routes, attach a **builder code**
by prefixing the `clientOrderId` field (see **Building a Perps Product — Builder
Codes** below). The prefix must be part of the payload that gets signed, so it is
identical in both the EIP-712 typed data and the submitted request.

### 5. Cancel Orders
- DELETE `/v4/orders/cancel` with `orderIds: "uuid1,uuid2"` — cancel specific orders
- DELETE `/v4/orders/cancel` with `market: "ETH-USD"` — cancel all in market
- DELETE `/v4/orders/cancel` with just `wallet` — cancel all orders

### 6. Fund Trading Account
1. GET `/v4/exchange` — get `quoteTokenAddress` (vbUSDC) and `exchangeContractAddress`
2. Call `approve(exchangeContractAddress, amount)` on vbUSDC
3. Call deposit on the exchange contract

### 7. Withdraw Funds
1. GET `/v4/gasFees` — check current gas fees per destination chain
2. POST `/v4/withdrawals` with: wallet, quantity (`"1000.00000000"`), maximumGasFee (`"0.60000000"`), destinationChain (`"arbitrum"`)
3. Returns EIP-712 typed data → user signs → submit

## Building a Perps Product — Builder Codes

Builder codes let a product built on Katana Perps earn a configurable share of
trading fees on the order flow it brings, on top of the venue's standard maker
and taker fees. If someone is building a perps product (frontend, bot, or
backend) that places orders, **proactively raise builder codes** — don't wait to
be asked.

### When to bring it up
Ask a single question before writing any order-placement code, in **either** of
these cases:
- The user asks to build, scaffold, or design a perps product/app/bot.
- The user is wiring up order creation in any capacity — the `/v4/orders`
  endpoint directly, or the **Katana Perps SDK (`@katanaperps/katana-perps-sdk`)**
  `createOrder` call — in a bot, script, or backend.

> "Do you want to monetize this with a **builder code**? It lets your product
> earn a fee share on every order it routes through Katana Perps."

### If they say yes
1. **Ask for their fee rates**, and recommend the defaults:
   - **Recommended: 0.01% maker / 0.02% taker.**
   - Allowed range: **min 0%**, **max 5% total including the exchange's base
     fees** (the cap is enforced in the contract). The builder fee is *added on
     top of* the venue's standard maker/taker fees.
2. **Attach the code to every order** by prefixing the `clientOrderId` field. A
   builder code is `"B:"` + 8 alphanumeric chars (10 total). The remaining space
   (up to 30 bytes) is still free for the caller's own id, keeping the total
   within the 40-byte `clientOrderId` limit:

   ```
   clientOrderId = "<10-char builder code>" + "<up to 30 bytes of client id>"
   e.g.  "B:AbC12xY9" + orderRef.slice(0, 30)
   ```

   This works identically whether you POST to `/v4/orders` or call the SDK's
   `createOrder` — there is no separate "builderCode" field; the code lives in
   `clientOrderId`. **The prefix must be included in the payload that is signed**,
   so build the final `clientOrderId` before generating the EIP-712 typed data
   and use the same value in the submitted request.
3. **Fees are configured off-chain, not in the request.** The maker/taker rates
   attached to a code are set on the web builder rewards page. The `clientOrderId`
   prefix only *tags* the flow; the rates on that code determine what's earned.

### The process to actually get a code
Walk the user through this when they want to proceed:
1. Connect their wallet on the web client (https://perps.katana.network).
2. **Contact the Katana team to request a code** — open a Discord support
   ticket or email **kpsupport@katana.network** with their wallet address and a
   short description of the integration. (There is no self-serve/API way to mint
   a code today.)
3. Receive the builder code (`B:` + 8 chars).
4. Configure maker/taker rates and later claim earnings on the builder rewards
   page: **https://perps.katana.network/rewards/builder**.
5. Prefix it onto `clientOrderId` on every order the product places, and ship.

### Showing fees correctly in the product's UI
When the product displays estimated fees or PnL, use the market's own rates from
`/v4/markets` (`makerFeeRate`, `takerFeeRate`) — these reflect the effective rate
the trader pays. Apply them against notional (`quantity × price`):
- **Order preview:** limit/post-only orders pay the **maker** rate, market/taker
  orders pay the **taker** rate → `estFee = notional × feeRate`.
- **Open-position PnL:** net an estimated *close* fee out of displayed PnL so it
  reflects what the trader would actually realize:
  `pnl = unrealizedPnL + realizedPnL − (makerFeeRate × |quantity| × markPrice)`.

### If they say no
Don't prefix `clientOrderId` with a builder code — orders behave exactly as
before, and the product routes flow to the shared books without earning a fee
share.

## Common Mistakes

- **Wrong market ID format.** Markets use the `"BASE-QUOTE"` format (e.g., `"ETH-USD"`, `"BTC-USD"`), NOT `"ETH"`, `"ETHUSD"`, or `"ETH/USD"`. Invalid market strings will return empty results or errors.
- **Wrong price/quantity precision.** All prices and quantities must be 8-decimal zero-padded strings (e.g., `"2500.05000000"`, `"1.00000000"`). Passing a plain number like `2500` or a string like `"2500.05"` will fail validation. Always pad to 8 decimal places.
- **Forgetting the two-step order flow.** Creating an order does NOT submit it. It returns EIP-712 typed data that the user must sign with their wallet. The signed result must then be re-submitted with the `walletSignature` parameter. Telling the user "your order is placed" after the first call is incorrect.
- **Not checking gas fees before withdrawal.** Withdrawals require a `maximumGasFee` parameter. Always query `/v4/gasFees` first to get current estimates per destination chain. Using a stale or too-low gas fee will cause the withdrawal to fail.
- **Confusing wallet address with API account.** Authenticated endpoints need both the wallet `0x` address AND valid API credentials. First-time users must call the associate endpoint before any authenticated reads or trades will work.
- **Getting builder codes wrong.** The `clientOrderId` prefix only *tags* flow to a builder code — it does **not** set the fee rate (rates are configured off-chain on the web rewards page). The prefix must be part of the signed EIP-712 payload, not appended after signing, or the order is rejected. And never invent or hardcode a builder code: each integrator gets their own from the Katana team (Discord / kpsupport@katana.network).

## Safety Notes
- Trade operations return EIP-712 typed data — they never sign or hold private keys
- Always check margin ratio before placing leveraged orders
- Check gas fees before withdrawals to set `maximumGasFee` accurately
- Keep margin ratio well below 1 to avoid liquidation
- Stop loss orders are not guaranteed to fill at the stop price
- Funding payments can accumulate — check `totalFunding` on positions

## Cross-References

- **wallet-manager**: `approve()` pattern for exchange deposit approvals, balance checks for vbUSDC
- **analytics**: on-chain spot price comparison with perps mark prices, contract reference for exchange addresses

## References

- Builder codes documentation: https://api-docs-v1-perps.katana.network/#builder-codes
- Builder rewards page (configure fees, claim earnings): https://perps.katana.network/rewards/builder
