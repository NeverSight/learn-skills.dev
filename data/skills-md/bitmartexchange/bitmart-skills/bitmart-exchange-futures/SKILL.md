---
name: bitmart-exchange-futures
description: "Use when the user asks about BitMart futures or contract trading, including opening/closing positions, setting leverage, placing plan (conditional) orders, take-profit/stop-loss, trailing orders, checking futures positions, managing futures account, sub-account transfers, affiliate/rebate queries, or simulated trading. Do NOT use for spot trading (use bitmart-exchange-spot)."
homepage: "https://www.bitmart.com"
metadata: {"author":"bitmart","version":"2026.3.10","sdk_version":"1.4.0","updated":"2026-03-10"}
---

# BitMart Futures Trading

## Overview

53 endpoints total. Table:

| # | Category | API Endpoint | Type | Description |
|---|----------|-------------|------|-------------|
| 1 | Market Data | `GET /contract/public/details` | READ | Contract specifications |
| 2 | Market Data | `GET /contract/public/depth` | READ | Order book |
| 3 | Market Data | `GET /contract/public/market-trade` | READ | Recent trades (max 100) |
| 4 | Market Data | `GET /contract/public/funding-rate` | READ | Current funding rate |
| 5 | Market Data | `GET /contract/public/funding-rate-history` | READ | Historical funding rates |
| 6 | Market Data | `GET /contract/public/kline` | READ | K-line (steps: 1,3,5,15,30,60,120,240,360,720,1440,4320,10080) |
| 7 | Market Data | `GET /contract/public/markprice-kline` | READ | Mark price K-line |
| 8 | Market Data | `GET /contract/public/open-interest` | READ | Open interest |
| 9 | Market Data | `GET /contract/public/leverage-bracket` | READ | Leverage tiers / risk limits |
| 10 | Account | `GET /contract/private/assets-detail` | READ | Futures account balance |
| 11 | Account | `GET /contract/private/trade-fee-rate` | READ | Trade fee rate |
| 12 | Account | `GET /contract/private/position` | READ | Current positions |
| 13 | Account | `GET /contract/private/position-v2` | READ | Positions (extended info) |
| 14 | Account | `GET /contract/private/position-risk` | READ | Position risk / liquidation |
| 15 | Account | `GET /contract/private/get-position-mode` | READ | Current position mode |
| 16 | Account | `GET /contract/private/transaction-history` | READ | PnL / funding / fees history |
| 17 | Trading | `POST /contract/private/submit-order` | WRITE | Place order |
| 18 | Trading | `POST /contract/private/cancel-order` | WRITE | Cancel order |
| 19 | Trading | `POST /contract/private/cancel-orders` | WRITE | Batch cancel |
| 20 | Trading | `POST /contract/private/modify-limit-order` | WRITE | Amend limit order |
| 21 | Trading | `POST /contract/private/cancel-all-after` | WRITE | Timed cancel all |
| 22 | Trading | `POST /contract/private/submit-leverage` | WRITE | Set leverage |
| 23 | Trading | `POST /contract/private/set-position-mode` | WRITE | Set hedge/one-way mode |
| 24 | Trading | `POST /account/v1/transfer-contract` | WRITE | Spot-Futures transfer |
| 25 | Plan Order | `POST /contract/private/submit-plan-order` | WRITE | Conditional/trigger order |
| 26 | Plan Order | `POST /contract/private/cancel-plan-order` | WRITE | Cancel plan order |
| 27 | Plan Order | `POST /contract/private/modify-plan-order` | WRITE | Amend plan order |
| 28 | TP/SL | `POST /contract/private/submit-tp-sl-order` | WRITE | Set take-profit/stop-loss |
| 29 | TP/SL | `POST /contract/private/modify-tp-sl-order` | WRITE | Modify TP/SL |
| 30 | TP/SL | `POST /contract/private/modify-preset-plan-order` | WRITE | Modify preset TP/SL on order |
| 31 | Trailing | `POST /contract/private/submit-trail-order` | WRITE | Trailing stop order |
| 32 | Trailing | `POST /contract/private/cancel-trail-order` | WRITE | Cancel trailing |
| 33 | Order Query | `GET /contract/private/order` | READ | Order by ID |
| 34 | Order Query | `GET /contract/private/order-history` | READ | Historical orders |
| 35 | Order Query | `GET /contract/private/get-open-orders` | READ | All open orders |
| 36 | Order Query | `GET /contract/private/current-plan-order` | READ | Active plan orders |
| 37 | Order Query | `GET /contract/private/trades` | READ | Trade / fill history |
| 38 | Order Query | `POST /account/v1/transfer-contract-list` | READ | Transfer records |
| 39 | Sub-Account | `POST /account/contract/sub-account/main/v1/sub-to-main` | WRITE | Sub → Main transfer (main account) |
| 40 | Sub-Account | `POST /account/contract/sub-account/main/v1/main-to-sub` | WRITE | Main → Sub transfer (main account) |
| 41 | Sub-Account | `POST /account/contract/sub-account/sub/v1/sub-to-main` | WRITE | Sub → Main transfer (sub account) |
| 42 | Sub-Account | `GET /account/contract/sub-account/main/v1/wallet` | READ | Sub-account futures balance |
| 43 | Sub-Account | `GET /account/contract/sub-account/main/v1/transfer-list` | READ | Sub-account transfer history |
| 44 | Sub-Account | `GET /account/contract/sub-account/v1/transfer-history` | READ | Account transfer history |
| 45 | Affiliate | `GET /contract/private/affiliate/rebate-list` | READ | Rebate overview |
| 46 | Affiliate | `GET /contract/private/affiliate/trade-list` | READ | Affiliate trade records |
| 47 | Affiliate | `GET /contract/private/affiliate/rebate-user` | READ | Single user rebate data |
| 48 | Affiliate | `GET /contract/private/affiliate/rebate-api` | READ | Single API user rebate data |
| 49 | Affiliate | `GET /contract/private/affiliate/invite-check` | READ | Check if invited user |
| 50 | Affiliate | `GET /contract/private/affiliate/rebate-inviteUser` | READ | Invited customer list |
| 51 | Simulated | `POST /contract/private/claim` | WRITE | Demo account top-up (demo only) |
| 52 | System | `GET /system/time` | READ | Get server time (milliseconds) |
| 53 | System | `GET /system/service` | READ | Get system service status / maintenance |

---

## Skill Routing

| User Intent | Correct Skill |
|------------|---------------|
| Futures/contract trading, leverage, TP/SL, plan orders, trailing stops, sub-account transfers, affiliate/rebate queries, simulated trading | **bitmart-exchange-futures** (this skill) |
| Spot buy/sell, order management, spot balance, fee rates | bitmart-exchange-spot |

---

## Authentication

### Credential Check (Before Any Private API Call)

Before calling any authenticated endpoint, verify credentials are available:

1. Check for environment variables:
   - `BITMART_API_KEY` — API key
   - `BITMART_API_SECRET` — Secret key
   - `BITMART_API_MEMO` — Memo string
2. Or check for config file: `~/.bitmart/config.toml`
   ```toml
   [default]
   api_key = "your-api-key"
   api_secret = "your-secret-key"
   memo = "your-memo"
   ```
3. If missing: **STOP**. Guide user to set up credentials. Do NOT proceed with any authenticated call.

**Key display rules:** When displaying credentials back to the user, show only the first 5 and last 4 characters (e.g., `bmk12...9xyz`). NEVER display full secret or memo values.

### Auth Levels

| Level | When | Headers Required |
|-------|------|-----------------|
| **NONE** | Public market data (endpoints 1-9) | None |
| **KEYED** | Read-only private data — balances, positions, orders, affiliate (endpoints 10-16, 33-37, 42-50) | `X-BM-KEY` |
| **SIGNED** | Write operations — trading, leverage, transfers, sub-account transfers, demo claim (endpoints 17-32, 38-41, 51) | `X-BM-KEY` + `X-BM-SIGN` + `X-BM-TIMESTAMP` |

### Signature Generation

```
timestamp = current UTC time in milliseconds
message   = "{timestamp}#{memo}#{request_body_json}"
signature = HMAC-SHA256(secret_key, message) → hex string
```

- For **POST** requests: `request_body_json` is the JSON body string.
- For **GET** requests: `request_body_json` is an empty string `""`.

### Required Headers (SIGNED)

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `X-BM-KEY` | API key |
| `X-BM-SIGN` | Hex-encoded HMAC-SHA256 signature |
| `X-BM-TIMESTAMP` | Current UTC timestamp in milliseconds |

---

## API Base

- **Base URL**: `https://api-cloud-v2.bitmart.com`
- **Symbol Format**: `BTCUSDT` (no separator — unlike spot which uses `BTC_USDT`)

## Key Differences from Spot

| Aspect | Spot | Futures |
|--------|------|---------|
| Base URL | `api-cloud.bitmart.com` | `api-cloud-v2.bitmart.com` |
| Symbol Format | `BTC_USDT` (underscore) | `BTCUSDT` (no separator) |
| Order Side | `"buy"` / `"sell"` (string) | `1` / `2` / `3` / `4` (integer) |
| Leverage | N/A | Configurable per symbol |
| Position Mode | N/A | `hedge_mode` / `one_way_mode` |
| Margin Mode | N/A | `cross` / `isolated` |

**IMPORTANT:** Always use the futures base URL (`api-cloud-v2`) for contract endpoints. Using the spot base URL will fail.

## Standard Response Format

**Success:**
```json
{
  "code": 1000,
  "message": "OK",
  "trace": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "data": { ... }
}
```

**Error:**
```json
{
  "code": 40035,
  "message": "Order not exist",
  "trace": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "data": null
}
```

**Important:** `code == 1000` means success. Any other code is an error.

**GET requests:** Parameters go in the query string.
**POST requests:** Parameters go in the JSON body.

---

## Order Side Reference

| Value | Hedge Mode | One-Way Mode |
|-------|------------|--------------|
| 1 | Open Long (buy_open_long) | Buy |
| 2 | Close Short (buy_close_short) | Buy (Reduce Only) |
| 3 | Close Long (sell_close_long) | Sell (Reduce Only) |
| 4 | Open Short (sell_open_short) | Sell |

**Hedge mode mapping:**
- To **open long**: side = 1
- To **close long**: side = 3
- To **open short**: side = 4
- To **close short**: side = 2

**One-way mode:** Use side 1 (buy) or 4 (sell). The system infers whether to open or close.

## Order Mode Reference

| Value | Name | Description |
|-------|------|-------------|
| 1 | GTC | Good Till Cancel — order stays open until filled or canceled |
| 2 | FOK | Fill or Kill — must fill entirely or cancel immediately |
| 3 | IOC | Immediate or Cancel — fill what's available, cancel the rest |
| 4 | Maker Only | Post Only — rejected if it would immediately match |

---

## Rate Limits

| Endpoint | Rate | Target |
|----------|------|--------|
| Public Market Data (most) | 12/2sec | IP |
| Open Interest | 2/2sec | IP |
| Assets Detail | 12/2sec | KEY |
| Trade Fee Rate | 2/2sec | KEY |
| Position / Position V2 | 6/2sec | KEY |
| Position Risk | 24/2sec | KEY |
| Get Position Mode | 2/2sec | KEY |
| Transaction History | 6/2sec | KEY |
| Order Detail | 50/2sec | KEY |
| Order History / Trades | 6/2sec | KEY |
| Open Orders / Plan Orders | 50/2sec | KEY |
| Submit Order | 24/2sec | KEY |
| Cancel Order | 40/2sec | KEY |
| Cancel Orders (batch) | 2/2sec | KEY |
| Modify Order | 24/2sec | UID |
| Plan / TP-SL / Trail Orders | 24/2sec | UID |
| Cancel Plan Order | 40/2sec | UID |
| Cancel All After | 4/2sec | UID |
| Set Leverage | 24/2sec | KEY |
| Set Position Mode | 2/2sec | KEY |
| Transfer | 1/2sec | KEY |
| Transfer List | 1/2sec | KEY |
| Sub-Account Transfers (39-41) | 8/2sec | KEY |
| Sub-Account Wallet (42) | 12/2sec | KEY |
| Sub-Account History (43-44) | 8/2sec | KEY |
| Affiliate Endpoints (45-50) | 24/2sec | KEY |
| `GET /system/time` | 10/sec | IP |
| `GET /system/service` | 10/sec | IP |

**Rate limit response headers:**
- `X-BM-RateLimit-Remaining` — Requests remaining in window
- `X-BM-RateLimit-Limit` — Total allowed requests in window
- `X-BM-RateLimit-Reset` — Seconds until window resets

If rate limited (HTTP 429), wait for the reset period before retrying.

---

## Quickstart

### Example 1: Get BTC contract details (no auth)

```bash
curl -s 'https://api-cloud-v2.bitmart.com/contract/public/details?symbol=BTCUSDT'
```

### Example 2: Get futures positions (KEYED)

```bash
curl -s -H "X-BM-KEY: $BITMART_API_KEY" \
  'https://api-cloud-v2.bitmart.com/contract/private/position?symbol=BTCUSDT'
```

### Example 3: Open long BTC position (SIGNED)

```bash
TIMESTAMP=$(date +%s000)
BODY='{"symbol":"BTCUSDT","side":1,"type":"market","size":1,"leverage":"10","open_type":"cross"}'
SIGN=$(echo -n "${TIMESTAMP}#${BITMART_API_MEMO}#${BODY}" | openssl dgst -sha256 -hmac "$BITMART_API_SECRET" | awk '{print $2}')
curl -s -X POST 'https://api-cloud-v2.bitmart.com/contract/private/submit-order' \
  -H "Content-Type: application/json" \
  -H "X-BM-KEY: $BITMART_API_KEY" \
  -H "X-BM-SIGN: $SIGN" \
  -H "X-BM-TIMESTAMP: $TIMESTAMP" \
  -d "$BODY"
```

---

## Operation Flow

### Step 0: Credential Check

Verify `BITMART_API_KEY`, `BITMART_API_SECRET`, and `BITMART_API_MEMO` are available via environment variables or `~/.bitmart/config.toml`. If missing, STOP and guide the user to set up credentials.

### Step 1: Identify User Intent

Parse user request and map to a READ or WRITE operation:

- **READ** operations: market data, positions, balance, order queries, funding rates
- **WRITE** operations: open/close position, set leverage, place plan order, set TP/SL, trailing stop, transfer

### Step 1.5: Pre-Trade Position Check (MANDATORY for open/leverage operations)

Before executing ANY of: open position (`POST /contract/private/submit-order` with side 1 or 4), set leverage (`POST /contract/private/submit-leverage`), or change margin mode:

1. Call `GET /contract/private/position-v2?symbol=<SYMBOL>` to check for existing positions and current margin mode (`open_type`)
2. **If an existing position is found (`current_amount != 0`):**
   - **You MUST inherit** the existing `leverage` value — do NOT send a different leverage in the order
   - **You MUST inherit** the existing `open_type` (margin mode: `cross` or `isolated`) — do NOT send a different margin mode
   - If the user explicitly requested different leverage or margin mode: **STOP** and warn:
     > "You have an existing [X]x [cross/isolated] [LONG/SHORT] position of [size] contracts. Changing leverage or margin mode while a position is open is commonly rejected by the API (for example, code 40012/40040). Please close the existing position first if you want to change these settings."
   - Wait for user decision before proceeding
3. **If no existing position:** proceed with user-specified leverage and margin mode

### Step 1.6: TP/SL Order Parameter Rules (MANDATORY when setting TP/SL on a position)

When the user asks to set take-profit or stop-loss on an **existing futures position**, use `POST /contract/private/submit-tp-sl-order`.

**CRITICAL — Do NOT confuse these two mechanisms:**
- `preset_take_profit_price` / `preset_stop_loss_price`: optional fields on `submit-order` to attach TP/SL at position-open time
- `submit-tp-sl-order`: standalone endpoint to set TP/SL on an **already-open position** — uses `trigger_price` + `executive_price`, NOT `take_profit_price`/`stop_loss_price`

**Required parameters:**

| Parameter | Type | Value | Notes |
|-----------|------|-------|-------|
| `symbol` | String | e.g. `BTCUSDT` | |
| `type` | String | `"take_profit"` or `"stop_loss"` | NEVER `"market"` or `"limit"` |
| `side` | Int | `3` (close long) or `2` (close short) | Must match position direction |
| `trigger_price` | String | Activation price | Long TP: > entry; Long SL: < entry |
| `executive_price` | String | `"0"` for market fill; or a limit price | |
| `price_type` | Int | `1` last price / `2` mark price | Default: `1` |
| `plan_category` | Int | `1` TP/SL order (default) / `2` Position TP/SL order | For existing-position TP/SL, use `2` |

**Always submit TP and SL as two separate API calls.** One call for take-profit, one for stop-loss.

Long BTC TP example: `{"symbol":"BTCUSDT","type":"take_profit","side":3,"trigger_price":"72000","executive_price":"0","price_type":1,"plan_category":2}`
Long BTC SL example: `{"symbol":"BTCUSDT","type":"stop_loss","side":3,"trigger_price":"64000","executive_price":"0","price_type":1,"plan_category":2}`

### Timestamp Display Rules

API responses contain Unix timestamps in different units. When displaying any timestamp to the user, **always convert to human-readable local time**.

| Field | Unit | Conversion |
|-------|------|------------|
| `create_time`, `update_time` (order responses) | Milliseconds | `÷ 1000` → Unix seconds → local time |
| `server_time` (system time) | Milliseconds | `÷ 1000` → Unix seconds → local time |
| `timestamp` (K-line candle open time) | Seconds | Direct → Unix seconds → local time |
| `open_timestamp`, `funding_time` (contract details) | Milliseconds | `÷ 1000` → Unix seconds → local time |

**Query parameter timestamps** for futures endpoints (`start_time`, `end_time`) are **endpoint-specific**:

- **Seconds**: `/contract/public/kline`, `/contract/public/markprice-kline`, `/contract/private/order-history`, `/contract/private/trades`, and affiliate rebate endpoints (`/contract/private/affiliate/...`)
- **Milliseconds**: `/contract/private/transaction-history`

Do NOT assume all futures `start_time` / `end_time` are seconds — always follow the target endpoint definition.

**Display format:** `YYYY-MM-DD HH:MM:SS` in the user's local timezone. Example: timestamp `1709971200000` (ms) → `2024-03-09 16:00:00` (UTC+8).

**Common mistakes to avoid:**
- Do NOT treat millisecond timestamps as seconds (produces dates in year 55000+)
- Do NOT display raw numeric timestamps — always convert to readable format
- Do NOT assume UTC — convert to the user's local timezone

### Step 2: Execute

- **READ**: Call the API endpoint, parse response, format data for user display.
- **WRITE**: Follow sub-steps below, then ask for **"CONFIRM"**:

  **2a. submit-order conditional param selection:**

  | Scenario | Send | Do NOT send |
  |----------|------|-------------|
  | Open position, `type=limit` (side=1 or 4) | `symbol`, `side`, `type:"limit"`, `price`, `size`, `leverage`, `open_type` | — |
  | Open position, `type=market` (side=1 or 4) | `symbol`, `side`, `type:"market"`, `size`, `leverage`, `open_type` | `price` (ignored, causes confusion) |
  | Close position, `type=limit` (side=2 or 3) | `symbol`, `side`, `type:"limit"`, `price`, `size` | `leverage`, `open_type` (not needed for close) |
  | Close position, `type=market` (side=2 or 3) | `symbol`, `side`, `type:"market"`, `size` | `price`, `leverage`, `open_type` |

  Additional constraints:
  - **`leverage` / `open_type` for open orders**: if an existing position is found (Step 1.5), use the existing position's values — do NOT send different ones.
  - **`mode=4` (Maker Only)**: only valid with `type=limit`. Never combine with `type=market`.
  - **`preset_take_profit_price` / `preset_stop_loss_price`**: only valid for opening orders (side=1 or 4). For TP/SL on an **already-open** position, use `submit-tp-sl-order` (see Step 1.6).
  - **`size` is always an integer** (number of contracts). Check the minimum contract size via `GET /contract/public/details`.

  **2b. Confirm and execute:**
  Present a summary (symbol, side, type, price if limit, size, leverage, open_type) and ask for explicit **"CONFIRM"** before executing.

### Step 3: Verify (WRITE only)

- After **opening a position**: Call `GET /contract/private/position-v2` to confirm position was opened. Report entry price, size, leverage, liquidation price, margin used.
- After **closing a position**: Call `GET /contract/private/position-v2` to confirm position was closed or reduced. Report realized PnL.
- After **placing an order**: Call `GET /contract/private/order` to confirm order status.
- After **canceling an order**: Call `GET /contract/private/get-open-orders` to verify the order is no longer open.
- Report the verified result to the user.

See `references/open-position.md`, `references/close-position.md`, `references/plan-order.md`, and `references/tp-sl.md` for detailed step-by-step workflows.

---

## References

- **[API Reference](references/api-reference.md)** — All 53 endpoints with full parameters, examples, and response fields
- **[Open Position](references/open-position.md)** — Step-by-step open position workflow
- **[Close Position](references/close-position.md)** — Step-by-step close position workflow
- **[Plan Orders](references/plan-order.md)** — Conditional/trigger order workflow
- **[TP/SL](references/tp-sl.md)** — Take-profit/stop-loss workflow

---

## Cross-Skill Workflows

### Workflow 1: Transfer Funds → Open Position → Monitor

1. **bitmart-exchange-futures** → `POST /account/v1/transfer-contract` — Transfer USDT from spot to futures
2. **bitmart-exchange-futures** → `POST /contract/private/submit-leverage` — Set leverage
3. **bitmart-exchange-futures** → `POST /contract/private/submit-order` — Open position (after user CONFIRM)
4. **bitmart-exchange-futures** → `GET /contract/private/position-v2` — Monitor position

### Workflow 2: Check Spot Balance → Transfer → Open Futures

1. **bitmart-exchange-spot** → `GET /account/v1/wallet` — Check spot balance
2. **bitmart-exchange-futures** → `POST /account/v1/transfer-contract` — Transfer to futures
3. **bitmart-exchange-futures** → `POST /contract/private/submit-order` — Open position

---

## Error Handling

| Code | Description | Action |
|------|-------------|--------|
| 1000 | Success | Process response normally |
| 30002 | X-BM-KEY not found | Check that API key is set correctly |
| 30005 | X-BM-SIGN is wrong | Verify signature generation (timestamp, memo, body format) |
| 30007 | Timestamp/recvWindow validation failed | Sync system clock (NTP), send X-BM-TIMESTAMP as Unix milliseconds, and ensure (serverTime - timestamp) <= recvWindow; recvWindow must be Long in (0,60000], default 5000 (max 60000) |
| 30010 | IP forbidden | Check API key IP whitelist settings |
| 30013 | Rate limit exceeded | Wait for rate limit window to reset, then retry |
| 40035 | Order not exist | Verify the order ID is correct and belongs to this account |
| 40044 | Invalid order size | Check min/max limits via `GET /contract/public/details` |
| 40027 | Insufficient balance | Check futures balance; may need to transfer from spot |
| 42000 | Insufficient balance (margin) | Reduce order size or add margin |
| 40021 | Position does not exist | Verify position is still open before trying to close |
| 40040 | Invalid leverage / mode constraint | Check leverage bracket and current position state; if position exists, keep current leverage + `open_type` |
| 40012 | Parameter/state conflict | Commonly appears when leverage/mode conflicts with current position/order state; query `GET /contract/private/position-v2` and inherit existing leverage + `open_type` |
| 429 | HTTP rate limit | Back off exponentially, check `X-BM-RateLimit-Reset` header |
| 418 | IP banned | Stop all requests immediately; wait before retrying |

---

## Security Notes

- **Never display full API keys or secrets.** Show first 5 + last 4 characters only (e.g., `bmk12...9xyz`).
- **All WRITE operations require explicit user confirmation** before execution. Present a clear summary of the action and wait for "CONFIRM".
- **Recommend IP whitelist** on API keys for additional security.
- **Recommend minimum permissions:** Read-Only + Futures-Trade only (no Withdraw permission).
- **Leverage warning:** Higher leverage amplifies both gains and losses. Always inform the user of the liquidation price before opening leveraged positions.
- **All trading outputs include disclaimer:** "Not financial advice. You are solely responsible for your investment decisions. Futures trading carries significant risk of loss."

---

## Reference: Order Types

| Type | Description |
|------|-------------|
| `limit` | Execute at specified price or better |
| `market` | Execute immediately at best available price |

## Reference: Order Sides

| Value | Hedge Mode | One-Way Mode |
|-------|------------|--------------|
| 1 | Open Long | Buy |
| 2 | Close Short | Buy (Reduce Only) |
| 3 | Close Long | Sell (Reduce Only) |
| 4 | Open Short | Sell |

## Reference: Order Modes

| Value | Name | Description |
|-------|------|-------------|
| 1 | GTC | Good Till Cancel |
| 2 | FOK | Fill or Kill |
| 3 | IOC | Immediate or Cancel |
| 4 | Maker Only | Post Only — rejected if it would immediately match |

## Reference: Order States

| State | Code | Description |
|-------|------|-------------|
| Approving | 1 | Order being validated |
| Pending | 2 | Order accepted, awaiting fill |
| Closed | 4 | Order completed (filled or canceled) |

## Reference: Open Types (Margin Mode)

| Value | Description |
|-------|-------------|
| `cross` | Cross margin — all available balance used as margin |
| `isolated` | Isolated margin — only allocated margin is at risk |

## Reference: Position Modes

| Value | Description |
|-------|-------------|
| `hedge_mode` | Can hold simultaneous long and short positions |
| `one_way_mode` | Can hold only one direction at a time |

## Reference: Plan Categories

| Value | Description |
|-------|-------------|
| 1 | TP/SL order — applies to a specific order quantity |
| 2 | Position TP/SL — applies to the entire position (default) |

## Reference: Price Types

| Value | Description |
|-------|-------------|
| 1 | Last price (default) — triggers based on last trade price |
| 2 | Fair price (mark price) — triggers based on mark price |

## Reference: Price Way (Plan Orders)

| Value | Description |
|-------|-------------|
| 1 | Bullish — trigger when price rises above trigger_price |
| 2 | Bearish — trigger when price drops below trigger_price |

## Reference: Transfer Types

| Value | Description |
|-------|-------------|
| `spot_to_contract` | Spot wallet to futures wallet |
| `contract_to_spot` | Futures wallet to spot wallet |

## Reference: Flow Types (Transaction History)

| Value | Description |
|-------|-------------|
| 0 | All types |
| 1 | Transfer |
| 2 | Realized PNL |
| 3 | Funding Fee |
| 4 | Commission |
| 5 | Liquidation |

## Reference: STP Modes (Self-Trade Prevention)

| Value | Description |
|-------|-------------|
| 1 | Cancel Maker (default) |
| 2 | Cancel Taker |
| 3 | Cancel Both |

## Reference: K-Line Steps

| Step (minutes) | Description |
|----------------|-------------|
| 1 | 1-minute candles |
| 3 | 3-minute candles |
| 5 | 5-minute candles |
| 15 | 15-minute candles |
| 30 | 30-minute candles |
| 60 | 1-hour candles |
| 120 | 2-hour candles |
| 240 | 4-hour candles |
| 360 | 6-hour candles |
| 720 | 12-hour candles |
| 1440 | 1-day candles |
| 4320 | 3-day candles |
| 10080 | 1-week candles |
