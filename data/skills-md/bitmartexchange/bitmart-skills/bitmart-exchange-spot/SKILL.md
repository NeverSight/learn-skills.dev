---
name: bitmart-exchange-spot
description: "Use when the user asks about BitMart spot trading, including buying or selling crypto, placing limit or market orders, checking spot balance, querying open orders, viewing trade history, or managing margin positions. Do NOT use for futures/contract trading (use bitmart-exchange-futures)."
homepage: "https://www.bitmart.com"
metadata: {"author":"bitmart","version":"2026.3.10","sdk_version":"1.4.0","updated":"2026-03-10"}
---

# BitMart Spot Trading

## Overview

| # | Category | API Endpoint | Type | Description |
|---|----------|-------------|------|-------------|
| 1 | Market Data | `GET /spot/quotation/v3/ticker` | READ | Get single pair ticker |
| 2 | Market Data | `GET /spot/quotation/v3/tickers` | READ | Get all pair tickers |
| 3 | Market Data | `GET /spot/quotation/v3/books` | READ | Order book depth (max 50) |
| 4 | Market Data | `GET /spot/quotation/v3/trades` | READ | Recent public trades (max 50) |
| 5 | Market Data | `GET /spot/quotation/v3/klines` | READ | Historical K-line/candlestick |
| 6 | Market Data | `GET /spot/quotation/v3/lite-klines` | READ | Latest K-line data |
| 7 | Market Data | `GET /spot/v1/symbols/details` | READ | Trading pair details |
| 8 | Market Data | `GET /spot/v1/symbols` | READ | Trading pair list |
| 9 | Market Data | `GET /spot/v1/currencies` | READ | All supported currencies |
| 10 | Account | `GET /account/v1/wallet` | READ | Account balance (all wallets) |
| 11 | Account | `GET /spot/v1/wallet` | READ | Spot wallet balance |
| 12 | Account | `GET /spot/v1/trade_fee` | READ | Actual trade fee rate |
| 13 | Account | `GET /spot/v1/user_fee` | READ | Base fee rate (account tier) |
| 14 | Margin Account | `GET /spot/v1/margin/isolated/account` | READ | Isolated margin account details |
| 15 | Margin Account | `GET /spot/v1/margin/isolated/pairs` | READ | Borrowing rate & amount |
| 16 | Margin Account | `GET /spot/v1/margin/isolated/borrow_record` | READ | Borrow record |
| 17 | Margin Account | `GET /spot/v1/margin/isolated/repay_record` | READ | Repayment record |
| 18 | Trading | `POST /spot/v2/submit_order` | WRITE | Place single order |
| 19 | Trading | `POST /spot/v1/margin/submit_order` | WRITE | Place margin order |
| 20 | Trading | `POST /spot/v4/batch_orders` | WRITE | Batch orders (max 10) |
| 21 | Trading | `POST /spot/v3/cancel_order` | WRITE | Cancel single order |
| 22 | Trading | `POST /spot/v4/cancel_orders` | WRITE | Cancel multiple orders |
| 23 | Trading | `POST /spot/v4/cancel_all` | WRITE | Cancel all open orders |
| 24 | Order Query | `POST /spot/v4/query/order` | READ | Query order by order ID |
| 25 | Order Query | `POST /spot/v4/query/client-order` | READ | Query by client order ID |
| 26 | Order Query | `POST /spot/v4/query/open-orders` | READ | All open orders |
| 27 | Order Query | `POST /spot/v4/query/history-orders` | READ | Historical orders |
| 28 | Order Query | `POST /spot/v4/query/trades` | READ | Account trade history |
| 29 | Order Query | `POST /spot/v4/query/order-trades` | READ | Trades for specific order |
| 30 | Margin Loan | `POST /spot/v1/margin/isolated/borrow` | WRITE | Margin borrow (isolated) |
| 31 | Margin Loan | `POST /spot/v1/margin/isolated/repay` | WRITE | Margin repay (isolated) |
| 32 | Margin Loan | `POST /spot/v1/margin/isolated/transfer` | WRITE | Margin asset transfer |
| 33 | System | `GET /system/time` | READ | Get server time (milliseconds) |
| 34 | System | `GET /system/service` | READ | Get system service status / maintenance |

---

## Skill Routing

| User Intent | Correct Skill |
|------------|---------------|
| Spot buy/sell, order management, balance, fee rates | **bitmart-exchange-spot** (this skill) |
| Futures/contract trading, leverage, TP/SL, plan orders | bitmart-exchange-futures |

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
| **KEYED** | Read-only private data — balances, fees, margin account, borrow/repay records (endpoints 10-17) | `X-BM-KEY` |
| **SIGNED** | Write operations and order queries (endpoints 18-32) | `X-BM-KEY` + `X-BM-SIGN` + `X-BM-TIMESTAMP` |

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

See `references/authentication.md` for full setup guide and troubleshooting.

---

## API Base

- **Base URL**: `https://api-cloud.bitmart.com`
- **Symbol Format**: `BTC_USDT` (base_quote, underscore separated)

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
  "code": 51003,
  "message": "Account Limit",
  "trace": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "data": null
}
```

**Important:** `code == 1000` means success. Any other code is an error.

**GET requests:** Parameters go in the query string.
**POST requests:** Parameters go in the JSON body.

---

## Rate Limits

| Endpoint | Rate | Target |
|----------|------|--------|
| `GET /spot/quotation/v3/ticker` | 15 req/2sec | IP |
| `GET /spot/quotation/v3/tickers` | 10 req/2sec | IP |
| `GET /spot/quotation/v3/lite-klines` | 15 req/2sec | IP |
| `GET /spot/quotation/v3/klines` | 10 req/2sec | IP |
| `GET /spot/quotation/v3/books` | 15 req/2sec | IP |
| `GET /spot/quotation/v3/trades` | 15 req/2sec | IP |
| `GET /spot/v1/currencies` | 8 req/2sec | IP |
| `GET /spot/v1/symbols` | 8 req/2sec | IP |
| `GET /spot/v1/symbols/details` | 12 req/2sec | IP |
| Balance | 12 req/2sec | KEY |
| Trade Fee / User Fee | 2 req/2sec | KEY |
| Margin Account | 12 req/2sec | KEY |
| Margin Pairs | 2 req/2sec | KEY |
| Borrow / Repay Records | 150 req/2sec | KEY |
| Place Order (spot) | 40 req/2sec | UID |
| Batch Place Orders (`/spot/v4/batch_orders`) | 40 req/2sec | UID |
| Place Order (margin) | 20 req/1sec | UID |
| Cancel Order | 40 req/2sec | UID |
| Cancel Multiple (`/spot/v4/cancel_orders`) | 40 req/2sec | UID |
| Cancel All | 1 req/3sec | UID |
| Query Order by ID | 50 req/2sec | KEY |
| Query by Client Order ID (`/spot/v4/query/client-order`) | 50 req/2sec | KEY |
| Open / History / Trades | 12 req/2sec | KEY |
| Order-Trades | 12 req/2sec | KEY |
| Margin Borrow / Repay / Transfer | 2 req/2sec | KEY |
| `GET /system/time` | 10 req/sec | IP |
| `GET /system/service` | 10 req/sec | IP |

**Rate limit response headers:**
- `X-BM-RateLimit-Remaining` — Number of requests already used in the current window
- `X-BM-RateLimit-Limit` — Maximum allowed requests in the current window
- `X-BM-RateLimit-Reset` — Current time window length (seconds)

**Warning:** If `X-BM-RateLimit-Remaining > X-BM-RateLimit-Limit`, stop calling immediately to avoid ban.

If rate limited (HTTP 429), wait for the reset period before retrying.

---

## Quickstart

### Example 1: Get BTC price (no auth)

```bash
curl -s 'https://api-cloud.bitmart.com/spot/quotation/v3/ticker?symbol=BTC_USDT'
```

### Example 2: Get account balance (KEYED)

```bash
curl -s -H "X-BM-KEY: $BITMART_API_KEY" \
  'https://api-cloud.bitmart.com/account/v1/wallet'
```

### Example 3: Place limit buy order (SIGNED)

```bash
TIMESTAMP=$(date +%s000)
BODY='{"symbol":"BTC_USDT","side":"buy","type":"limit","size":"0.001","price":"60000"}'
SIGN=$(echo -n "${TIMESTAMP}#${BITMART_API_MEMO}#${BODY}" | openssl dgst -sha256 -hmac "$BITMART_API_SECRET" | awk '{print $2}')
curl -s -X POST 'https://api-cloud.bitmart.com/spot/v2/submit_order' \
  -H "Content-Type: application/json" \
  -H "X-BM-KEY: $BITMART_API_KEY" \
  -H "X-BM-SIGN: $SIGN" \
  -H "X-BM-TIMESTAMP: $TIMESTAMP" \
  -d "$BODY"
```

---

## API Reference

See `references/api-reference.md` for full endpoint documentation with parameters, examples, and response formats.

---

## Reference: Order Types

| Type | Description |
|------|-------------|
| `limit` | Execute at specified price or better |
| `market` | Execute immediately at best available price |
| `limit_maker` | Post-only; rejected if it would immediately match (ensures maker fee) |
| `ioc` | Immediate-or-cancel; unfilled portion is canceled immediately |

## Reference: Order Sides

| Side | Description |
|------|-------------|
| `buy` | Buy base currency with quote currency |
| `sell` | Sell base currency for quote currency |

## Reference: Order States

| State | Description |
|-------|-------------|
| `new` | Order accepted, not yet filled |
| `partially_filled` | Partially executed, still open |
| `filled` | Fully executed |
| `canceled` | Canceled by user |
| `partially_canceled` | Partially filled, then canceled |

## Reference: Cancel Sources

| Source | Description |
|--------|-------------|
| `""` (empty) | Not canceled |
| `user` | Canceled by user |
| `system` | Canceled by system (e.g., insufficient balance) |
| `stp` | Canceled by self-trade prevention |

## Reference: STP Modes

| Mode | Description |
|------|-------------|
| `none` | No self-trade prevention |
| `cancel_maker` | Cancel the resting (maker) order if self-trade detected |
| `cancel_taker` | Cancel the incoming (taker) order if self-trade detected |
| `cancel_both` | Cancel both orders if self-trade detected |

## Reference: Trade Roles

| Role | Description |
|------|-------------|
| `taker` | Order matched immediately against resting order |
| `maker` | Order rested on book and was matched later |

## Reference: Parameter Naming Convention

> **CRITICAL — Wrong case = silently ignored field.** The API does NOT return an error for misnamed params; it simply ignores them, causing unexpected behavior or wrong results. Always verify the endpoint version before constructing any request body.

| API Version | Convention | Examples |
|-------------|-----------|----------|
| v1-v3 | snake_case | `client_order_id`, `order_id`, `start_time` |
| v4 | camelCase | `clientOrderId`, `orderId`, `orderMode`, `startTime` |

**Mixed-case exceptions (must be memorized):**
- `POST /spot/v2/submit_order`: `stpMode` (camelCase) alongside `client_order_id` (snake_case)
- `POST /spot/v1/margin/submit_order`: `clientOrderId` (camelCase in a v1 endpoint)

## Reference: K-Line Steps

| Step (minutes) | Description |
|----------------|-------------|
| 1 | 1-minute candles |
| 5 | 5-minute candles |
| 15 | 15-minute candles |
| 30 | 30-minute candles |
| 60 | 1-hour candles |
| 120 | 2-hour candles |
| 240 | 4-hour candles |
| 1440 | 1-day candles |
| 10080 | 1-week candles |
| 43200 | 1-month candles |

---

## Operation Flow

### Step 0: Credential Check

Verify `BITMART_API_KEY`, `BITMART_API_SECRET`, and `BITMART_API_MEMO` are available via environment variables or `~/.bitmart/config.toml`. If missing, STOP and guide the user to set up credentials.

### Step 1: Identify User Intent

Parse user request and map to a READ or WRITE operation:

- **READ** operations: market data, balance queries, order queries, fee rates
- **WRITE** operations: place order, cancel order, batch orders

### Timestamp Display Rules

API responses contain Unix timestamps in different units. When displaying any timestamp to the user, **always convert to human-readable local time**.

| Field | Unit | Conversion |
|-------|------|------------|
| `createTime`, `updateTime` (order responses) | Milliseconds | `÷ 1000` → Unix seconds → local time |
| `server_time` (system time) | Milliseconds | `÷ 1000` → Unix seconds → local time |
| `t` (K-line candle open time) | Seconds | Direct → Unix seconds → local time |
| `create_time` (borrow records) | Seconds | Direct → Unix seconds → local time |
| `repay_time` (repay records) | Seconds | Direct → Unix seconds → local time |

**Display format:** `YYYY-MM-DD HH:MM:SS` in the user's local timezone. Example: timestamp `1700000000000` (ms) → `2023-11-15 06:13:20` (UTC+8).

**Common mistakes to avoid:**
- Do NOT treat millisecond timestamps as seconds (produces dates in year 55000+)
- Do NOT display raw numeric timestamps — always convert to readable format
- Do NOT assume UTC — convert to the user's local timezone

### Step 2: Execute

- **READ**: Call the API endpoint, parse response, format data for user display.
- **WRITE**: Follow these sub-steps strictly in order:

  **2a. Parameter naming check (prevents silent failures):**
  - Identify the API version of the target endpoint
  - v4 endpoints (`/spot/v4/...`): ALL params must be **camelCase** (`clientOrderId`, `orderId`, `orderMode`, `startTime`)
  - v1–v3 endpoints: ALL params must be **snake_case** (`client_order_id`, `order_id`, `start_time`)
  - Special exception: `POST /spot/v2/submit_order` uses **mixed** — `client_order_id` (snake_case) + `stpMode` (camelCase)
  - The API does NOT return an error for wrong-case params — it silently ignores them, causing wrong orders or failed queries

  **2b. Order type rules — params, precision, minimum validation:**

  First call `GET /spot/v1/symbols/details`, locate the symbol in `data.symbols[]`, extract: `price_max_precision`, `quote_increment`, `min_buy_amount`, `min_sell_amount`.

  Then branch:

  **`type=market`, `side=buy` — Market buy:**
  - Send only `notional` (USDT/quote amount). Do NOT send `size` or `price` — silently ignored and causes error 50021.
  - Validate: `float(notional) >= min_buy_amount`. If not, STOP — suggest `"notional":"<min_buy_amount>"`. API returns 51012 otherwise.
  - Body: `{"symbol":"XRP_USDT","side":"buy","type":"market","notional":"5"}`

  **`type=market`, `side=sell` — Market sell:**
  - Send only `size` (base currency quantity, e.g. XRP amount). Do NOT send `price` or `notional`.
  - Truncate `size` to `quote_increment` precision.
  - Estimate value: `size * current_last_price`. If estimated value `< min_sell_amount`, STOP and warn user.
  - Body: `{"symbol":"XRP_USDT","side":"sell","type":"market","size":"10"}`

  **`type=limit` — Limit order:**
  - Send `size` + `price`. Truncate `price` to `price_max_precision`, `size` to `quote_increment`.
  - **Note:** If price exceeds `price_max_precision`, the API silently truncates the extra decimals instead of returning an error. Always truncate client-side to ensure the submitted price matches the intended price.
  - Calculate `order_value = size * price`. If `order_value < min_buy_amount` (buy) or `< min_sell_amount` (sell), STOP.
  - If user requested "buy all" / "use full balance": `size = floor(balance / price)` at precision, re-verify minimum.
  - **No hidden risk** — order sits on the book until filled or canceled.

  **`type=limit_maker` — Post-only (maker-only):**
  - Same params as `limit` (`size` + `price`). Same precision/minimum rules.
  - **CRITICAL behavioral note:** The server **auto-cancels** the order (no error) if the price would immediately match:
    - Buy `limit_maker`: if `price >= best_ask`, order is silently canceled. Price must be **below** best ask.
    - Sell `limit_maker`: if `price <= best_bid`, order is silently canceled. Price must be **above** best bid.
  - Inform user of this risk when setting an aggressive `limit_maker` price.

  **`type=ioc` — Immediate-or-Cancel:**
  - Same params as `limit` (`size` + `price`). Same precision/minimum rules.
  - **Behavioral note:** Fills whatever quantity is available immediately at the given price; the unfilled remainder is **immediately canceled**. User may receive a partial fill or no fill at all.

  **2c. Confirm and execute:**
  - Present order summary based on type:
    - market buy: symbol, side=buy, type=market, notional amount
    - market sell: symbol, side=sell, type=market, size (quantity)
    - limit/limit_maker/ioc: symbol, side, type, size, price, estimated order value
  - For `limit_maker`: include a reminder that the order will be auto-canceled if the price crosses the spread.
  - Ask for explicit **"CONFIRM"** before executing. Only proceed after user confirms.

### Step 3: Verify (WRITE only)

- After **placing an order**: Call `POST /spot/v4/query/order` with `{"orderId":"..."}` to confirm order status.
- After **canceling an order**: Call `POST /spot/v4/query/open-orders` to verify the order is no longer open.
- Report the verified result to the user.

---

## Cross-Skill Workflows

### Workflow 1: Check Price → Check Balance → Buy

1. **bitmart-exchange-spot** → `GET /spot/quotation/v3/ticker?symbol=BTC_USDT` — Get current price
2. **bitmart-exchange-spot** → `GET /account/v1/wallet` — Check available balance
3. **bitmart-exchange-spot** → `POST /spot/v2/submit_order` — Place buy order (after user CONFIRM)
4. **bitmart-exchange-spot** → `POST /spot/v4/query/order` — Verify order execution

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
| 51003 | Account Limit | Reduce borrow/repay/transfer scope or verify account restrictions |
| 51006 | Exceeds the amount to be repaid | Ensure repay amount is not greater than outstanding principal + interest |
| 51007 | order_mode not found | Use a valid `orderMode` value (`spot` or `iso_margin`) on v4 query endpoints |
| 50021 | param error | For `market` buy, use `notional` (USDT amount) — do NOT use `size`; `size` is silently ignored and causes this error |
| 51011 | param not match : size * price >= X | Read symbol constraints from `GET /spot/v1/symbols/details`; enforce side-specific minimum notional (`min_buy_amount`/`min_sell_amount`) |
| 51012 | below minimum order amount | `notional` (for market buy) or `size * price` (for limit) is below `min_buy_amount`; increase order value to at least the symbol minimum |
| 40044 | Invalid order size | Call `GET /spot/v1/symbols/details`; use symbol precision/increment fields and truncate (not round) `size` and `price` |
| 50023 | Operation is limited | Pair may not support API trading; use a different pair |
| 429 | HTTP rate limit | Back off exponentially, check `X-BM-RateLimit-Reset` header |
| 418 | IP banned | Stop all requests immediately; wait before retrying |

---

## Security Notes

- **Never display full API keys or secrets.** Show first 5 + last 4 characters only (e.g., `bmk12...9xyz`).
- **All WRITE operations require explicit user confirmation** before execution. Present a clear summary of the action and wait for "CONFIRM".
- **Recommend IP whitelist** on API keys for additional security.
- **Recommend minimum permissions:** Read-Only + Spot-Trade only (no Withdraw permission).
- **All trading outputs include disclaimer:** "Not financial advice. You are solely responsible for your investment decisions."
