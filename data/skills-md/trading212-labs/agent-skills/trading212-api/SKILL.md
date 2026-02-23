---
name: trading212-api
description: 'This skill should be used when the user asks to "connect to Trading 212", "authenticate Trading 212 API", "place a trade", "buy stock", "sell shares", "place market order",, "place pending order", "place limit order", "cancel order", "check my balance", "view account summary", "get positions", "view portfolio", "check P&L", "find ticker symbol", "search instruments", "check trading hours", "view dividends", "get order history", "export transactions", "generate CSV report", or needs guidance on Trading 212 API authentication, order placement, position monitoring, account information, instrument lookup, or historical data retrieval.'
license: MIT License
metadata:
  author: Trading 212
  version: 1.0.0
---

# Trading 212 API

> **Note:** The Trading 212 API is currently in **beta** and under active development. Some endpoints or behaviors may change.

## Quick Reference

### Environments

| Environment | Base URL                             | Purpose                                 |
| ----------- | ------------------------------------ | --------------------------------------- |
| Demo        | `https://demo.trading212.com/api/v0` | Paper trading - test without real funds |
| Live        | `https://live.trading212.com/api/v0` | Real money trading                      |

### Order Quantity Convention

- **Positive quantity = BUY** (e.g., `10` buys 10 shares)
- **Negative quantity = SELL** (e.g., `-10` sells 10 shares)

### Account Types

Only **Invest** and **Stocks ISA** accounts are supported.

### Instrument Identifiers

Trading 212 uses custom tickers as unique identifiers for instruments.
Always search for the Trading 212 ticker before making instrument requests.

---

## Authentication

HTTP Basic Auth with API Key (username) and API Secret (password).

### Check Existing Setup First

Before guiding the user through authentication setup, check if credentials are already configured:

**Semantic rule:** Credentials are configured when **at least one complete set** is present: a complete set is key + secret for the same account (e.g. `T212_API_KEY` + `T212_API_SECRET`, or `T212_API_KEY_INVEST` + `T212_API_SECRET_INVEST`, or `T212_API_KEY_STOCKS_ISA` + `T212_API_SECRET_STOCKS_ISA`). You do not need all four account-specific vars; having only the Invest pair or only the Stocks ISA pair is enough. Check for any combination that gives at least one usable key+secret pair.

```bash
# Example: configured if any complete credential set exists
if [ -n "$T212_AUTH_HEADER" ] && [ -n "$T212_BASE_URL" ]; then
  echo "Configured (derived vars)"
elif [ -n "$T212_API_KEY" ] && [ -n "$T212_API_SECRET" ]; then
  echo "Configured (single account)"
elif [ -n "$T212_API_KEY_INVEST" ] && [ -n "$T212_API_SECRET_INVEST" ]; then
  echo "Configured (Invest); Stocks ISA also if T212_API_KEY_STOCKS_ISA and T212_API_SECRET_STOCKS_ISA are set"
elif [ -n "$T212_API_KEY_STOCKS_ISA" ] && [ -n "$T212_API_SECRET_STOCKS_ISA" ]; then
  echo "Configured (Stocks ISA); Invest also if T212_API_KEY_INVEST and T212_API_SECRET_INVEST are set"
else
  echo "No complete credential set found"
fi
```

If any complete set is present, skip the full setup and proceed with API calls; when making requests, use the resolution order in "Making Requests" below (pick the pair that matches the user's account context when multiple sets exist). Do not ask the user to run derivation one-liners or merge keys into a header. Only guide users through the full setup process below when no complete credential set exists.

> **Important:** Before making any API calls, always ask the user which environment they want to use: **LIVE** (real money) or **DEMO** (paper trading). Do not assume the environment.

### API Keys Are Environment-Specific

**API keys are tied to a specific environment and cannot be used across environments.**

| API Key Created In | Works With            | Does NOT Work With    |
| ------------------ | --------------------- | --------------------- |
| LIVE account       | `live.trading212.com` | `demo.trading212.com` |
| DEMO account       | `demo.trading212.com` | `live.trading212.com` |

If you get a 401 error, verify that:

1. You're using the correct API key for the target environment
2. The API key was generated in the same environment (LIVE or DEMO) you're trying to access

### Get Credentials

1. **Decide which environment to use** - LIVE (real money) or DEMO (paper trading)
2. Open Trading 212 app (mobile or web)
3. **Switch to the correct account** - Make sure you're in LIVE or DEMO mode matching your target environment
4. Navigate to **Settings** > **API**
5. Generate a new API key pair - you'll receive:
   - **API Key (ID)** (e.g., `35839398ZFVKUxpHzPiVsxKdOtZdaDJSrvyPF`)
   - **API Secret** (e.g., `7MOzYJlVJgxoPjdZJCEH3fO9ee7A0NzLylFFD4-3tlo`)
6. **Store the credentials separately** for each environment if you use both

### Building the Auth Header

Combine your API Key (ID) and Secret with a colon, base64 encode, and prefix with `Basic ` for the Authorization header.

**Optional:** To precompute the header from key/secret, you can set:

```bash
export T212_AUTH_HEADER="Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)"
```

Otherwise, the agent builds the header from `T212_API_KEY` and `T212_API_SECRET` when making requests.

**Manual (placeholders):**

```bash
# Format: T212_AUTH_HEADER = "Basic " + base64(API_KEY_ID:API_SECRET)
export T212_AUTH_HEADER="Basic $(echo -n "<YOUR_API_KEY_ID>:<YOUR_API_SECRET>" | base64)"

# Example with sample credentials:
export T212_AUTH_HEADER="Basic $(echo -n "35839398ZFVKUxpHzPiVsxKdOtZdaDJSrvyPF:7MOzYJlVJgxoPjdZJCEH3fO9ee7A0NzLylFFD4-3tlo" | base64)"
```

### Making Requests

When making API calls, use the first option that applies (semantically: pick the credential set that matches the user's account, or the only set present):

- **If `T212_AUTH_HEADER` and `T212_BASE_URL` are set:** use them in requests.
- **Else if `T212_API_KEY` and `T212_API_SECRET` are set:** use this pair (single account). Build header as `Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)` and base URL as `https://${T212_ENV:-live}.trading212.com`. Do not guide the user to derive or merge; you do it.
- **Else if both account-specific pairs are set** (`T212_API_KEY_INVEST`/`T212_API_SECRET_INVEST` and `T212_API_KEY_STOCKS_ISA`/`T212_API_SECRET_STOCKS_ISA`): the user must clearly specify which account to target (Invest or Stocks ISA), unless they ask for information for **all accounts**. Use the Invest pair when the user refers to Invest, and the Stocks ISA pair when the user refers to ISA/Stocks ISA. **If the user wants information for all accounts, make multiple API calls—one per account** (Invest and Stocks ISA)—and present or aggregate the results for both. **If it is not clear from context which account to use (and they did not ask for all accounts), ask for confirmation before making API calls** (e.g. "Which account should I use — Invest or Stocks ISA?"). Do not assume. Build the header from the chosen key/secret and base URL as `https://${T212_ENV:-live}.trading212.com`.
- **Else if only the Invest pair is set** (`T212_API_KEY_INVEST` and `T212_API_SECRET_INVEST`): use this pair for requests; if the user asks about Stocks ISA, only the Invest account is configured.
- **Else if only the Stocks ISA pair is set** (`T212_API_KEY_STOCKS_ISA` and `T212_API_SECRET_STOCKS_ISA`): use this pair for requests; if the user asks about Invest, only the Stocks ISA account is configured.

Use the `T212_AUTH_HEADER` value in the Authorization header when it is set:

```bash
# When T212_AUTH_HEADER and T212_BASE_URL are set:
curl -H "Authorization: $T212_AUTH_HEADER" \
  "${T212_BASE_URL}/api/v0/equity/account/summary"
```

When only primary vars are set, use the inline form in the curl:

```bash
# When only T212_API_KEY, T212_API_SECRET, T212_ENV are set:
curl -H "Authorization: Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)" \
  "https://${T212_ENV:-live}.trading212.com/api/v0/equity/account/summary"
```

> **Warning:** `T212_AUTH_HEADER` must be the full header value including the `Basic ` prefix.
>
> ```bash
> # WRONG - raw base64 without "Basic " prefix
> curl -H "Authorization: <base64-only>" ...  # This will NOT work!
>
> # CORRECT - use T212_AUTH_HEADER (contains "Basic <base64>")
> curl -H "Authorization: $T212_AUTH_HEADER" ...  # This works
> ```

### Environment Variables

**Single account vs all accounts:** API keys are for a **single account**. One key/secret pair (`T212_API_KEY` + `T212_API_SECRET`) = one account (Invest or Stocks ISA). To use **all accounts** (Invest and Stocks ISA), the user must set **two sets** of key/secret: `T212_API_KEY_INVEST` / `T212_API_SECRET_INVEST` and `T212_API_KEY_STOCKS_ISA` / `T212_API_SECRET_STOCKS_ISA`. When both pairs are set, the user must clearly specify which account to target; if it is not clear from context, ask for confirmation (Invest or Stocks ISA) before making API calls.

**Primary (single account):** Set these for consistent setup with the plugin README:

```bash
export T212_API_KEY="your-api-key"       # API Key (ID) from Trading 212
export T212_API_SECRET="your-api-secret"
export T212_ENV="demo"                   # or "live" (defaults to "live" if unset)
```

**Account-specific (Invest and/or Stocks ISA):** Set only the pair(s) you use. One complete set (key + secret for the same account) is enough. For example, only Invest:

```bash
export T212_API_KEY_INVEST="your-invest-api-key"
export T212_API_SECRET_INVEST="your-invest-api-secret"
export T212_ENV="demo"                   # or "live"
```

For both accounts, set both pairs:

```bash
export T212_API_KEY_INVEST="your-invest-api-key"
export T212_API_SECRET_INVEST="your-invest-api-secret"
export T212_API_KEY_STOCKS_ISA="your-stocks-isa-api-key"
export T212_API_SECRET_STOCKS_ISA="your-stocks-isa-api-secret"
export T212_ENV="demo"                   # or "live" (applies to both)
```

**Optional – precomputed (for scripts or if the user prefers):** The user can set the auth header and base URL from the primary vars, but they do not need to; when making API calls you (the agent) must build the header and base URL from primary vars if these are not set.

```bash
# Build auth header and base URL from T212_API_KEY, T212_API_SECRET, T212_ENV
export T212_AUTH_HEADER="Basic $(echo -n "$T212_API_KEY:$T212_API_SECRET" | base64)"
export T212_BASE_URL="https://${T212_ENV:-live}.trading212.com"
```

**Alternative (manual):** If you prefer not to store key/secret in env, set derived vars directly. Remember: API keys only work with their matching environment.

```bash
# For DEMO (paper trading)
export T212_AUTH_HEADER="Basic $(echo -n "<DEMO_API_KEY_ID>:<DEMO_API_SECRET>" | base64)"
export T212_BASE_URL="https://demo.trading212.com"

# For LIVE (real money) - generate separate credentials in LIVE account
# export T212_AUTH_HEADER="Basic $(echo -n "<LIVE_API_KEY_ID>:<LIVE_API_SECRET>" | base64)"
# export T212_BASE_URL="https://live.trading212.com"
```

**Tip:** If you use both environments, use separate variable names:

```bash
# Demo credentials
export T212_DEMO_AUTH_HEADER="Basic $(echo -n "<DEMO_KEY_ID>:<DEMO_SECRET>" | base64)"

# Live credentials
export T212_LIVE_AUTH_HEADER="Basic $(echo -n "<LIVE_KEY_ID>:<LIVE_SECRET>" | base64)"
```

### Common Auth Errors

| Code | Cause                | Solution                                                                                      |
| ---- | -------------------- | --------------------------------------------------------------------------------------------- |
| 401  | Invalid credentials  | Check API key/secret, ensure no extra whitespace                                              |
| 401  | Environment mismatch | **LIVE API keys don't work with DEMO and vice versa** - verify key matches target environment |
| 403  | Missing permissions  | Check API permissions in Trading 212 settings                                                 |
| 408  | Request timed out    | Retry the request                                                                             |
| 429  | Rate limit exceeded  | Wait for `x-ratelimit-reset` timestamp                                                        |

---

## Account

### Get Account Summary

`GET /api/v0/equity/account/summary` (1 req/5s)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/account/summary"
```

**Response Schema:**

```json
{
  "id": 12345678,
  "currency": "GBP",
  "totalValue": 15250.75,
  "cash": {
    "availableToTrade": 2500.5,
    "reservedForOrders": 150.0,
    "inPies": 500.0
  },
  "investments": {
    "currentValue": 12100.25,
    "totalCost": 10500.0,
    "realizedProfitLoss": 850.5,
    "unrealizedProfitLoss": 1600.25
  }
}
```

### Account Fields

| Field                              | Type    | Description                             |
| ---------------------------------- | ------- | --------------------------------------- |
| `id`                               | integer | Primary trading account number          |
| `currency`                         | string  | Primary account currency (ISO 4217)     |
| `totalValue`                       | number  | Total account value in primary currency |
| `cash.availableToTrade`            | number  | Funds available for investing           |
| `cash.reservedForOrders`           | number  | Cash reserved for pending orders        |
| `cash.inPies`                      | number  | Uninvested cash inside pies             |
| `investments.currentValue`         | number  | Current value of all investments        |
| `investments.totalCost`            | number  | Cost basis of current investments       |
| `investments.realizedProfitLoss`   | number  | All-time realized P&L                   |
| `investments.unrealizedProfitLoss` | number  | Potential P&L if sold now               |

---

## Orders

### Order Types

| Type      | Endpoint                           | Availability | Description                          |
| --------- | ---------------------------------- | ------------ | ------------------------------------ |
| Market    | `/api/v0/equity/orders/market`     | Demo + Live  | Execute immediately at best price    |
| Limit     | `/api/v0/equity/orders/limit`      | Demo + Live  | Execute at limit price or better     |
| Stop      | `/api/v0/equity/orders/stop`       | Demo + Live  | Market order when stop price reached |
| StopLimit | `/api/v0/equity/orders/stop_limit` | Demo + Live  | Limit order when stop price reached  |

### Order Statuses

| Status             | Description                             |
| ------------------ | --------------------------------------- |
| `LOCAL`            | Order created locally, not yet sent     |
| `UNCONFIRMED`      | Sent to exchange, awaiting confirmation |
| `CONFIRMED`        | Confirmed by exchange                   |
| `NEW`              | Active and awaiting execution           |
| `CANCELLING`       | Cancel request in progress              |
| `CANCELLED`        | Successfully cancelled                  |
| `PARTIALLY_FILLED` | Some shares executed                    |
| `FILLED`           | Completely executed                     |
| `REJECTED`         | Rejected by exchange                    |
| `REPLACING`        | Modification in progress                |
| `REPLACED`         | Successfully modified                   |

### Time Validity

| Value              | Description                                |
| ------------------ | ------------------------------------------ |
| `DAY`              | Expires at midnight in exchange timezone   |
| `GOOD_TILL_CANCEL` | Active until filled or cancelled (default) |

### Order Strategy

| Value      | Description                                     |
| ---------- | ----------------------------------------------- |
| `QUANTITY` | Order by number of shares (API supported)       |
| `VALUE`    | Order by monetary value (not supported via API) |

### Initiated From

| Value        | Description         |
| ------------ | ------------------- |
| `API`        | Placed via this API |
| `IOS`        | iOS app             |
| `ANDROID`    | Android app         |
| `WEB`        | Web platform        |
| `SYSTEM`     | System-generated    |
| `AUTOINVEST` | Autoinvest feature  |

### Place Market Order

`POST /api/v0/equity/orders/market` (50 req/min)

```bash
# Buy 5 shares
curl -X POST -H "Authorization: $T212_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$T212_BASE_URL/api/v0/equity/orders/market" \
  -d '{"ticker": "AAPL_US_EQ", "quantity": 5}'

# Sell 3 shares (negative quantity)
curl -X POST -H "Authorization: $T212_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$T212_BASE_URL/api/v0/equity/orders/market" \
  -d '{"ticker": "AAPL_US_EQ", "quantity": -3}'

# Buy with extended hours enabled
curl -X POST -H "Authorization: $T212_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$T212_BASE_URL/api/v0/equity/orders/market" \
  -d '{"ticker": "AAPL_US_EQ", "quantity": 5, "extendedHours": true}'
```

**Request Fields:**

| Field           | Type    | Required | Description                                                                                                            |
| --------------- | ------- | -------- | ---------------------------------------------------------------------------------------------------------------------- |
| `ticker`        | string  | Yes      | Instrument ticker (e.g., `AAPL_US_EQ`)                                                                                 |
| `quantity`      | number  | Yes      | Positive for buy, negative for sell                                                                                    |
| `extendedHours` | boolean | No       | Set `true` to allow execution in pre-market (4:00-9:30 ET) and after-hours (16:00-20:00 ET) sessions. Default: `false` |

**Response:**

```json
{
  "id": 123456789,
  "type": "MARKET",
  "ticker": "AAPL_US_EQ",
  "instrument": {
    "ticker": "AAPL_US_EQ",
    "name": "Apple Inc",
    "isin": "US0378331005",
    "currency": "USD"
  },
  "quantity": 5,
  "filledQuantity": 0,
  "status": "NEW",
  "side": "BUY",
  "strategy": "QUANTITY",
  "initiatedFrom": "API",
  "extendedHours": false,
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Place Limit Order

`POST /api/v0/equity/orders/limit` (1 req/2s)

```bash
curl -X POST -H "Authorization: $T212_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$T212_BASE_URL/api/v0/equity/orders/limit" \
  -d '{"ticker": "AAPL_US_EQ", "quantity": 5, "limitPrice": 150.00, "timeValidity": "DAY"}'
```

**Request Fields:**

| Field          | Type   | Required | Description                             |
| -------------- | ------ | -------- | --------------------------------------- |
| `ticker`       | string | Yes      | Instrument ticker                       |
| `quantity`     | number | Yes      | Positive for buy, negative for sell     |
| `limitPrice`   | number | Yes      | Maximum price for buy, minimum for sell |
| `timeValidity` | string | No       | `DAY` (default) or `GOOD_TILL_CANCEL`   |

### Place Stop Order

`POST /api/v0/equity/orders/stop` (1 req/2s)

```bash
curl -X POST -H "Authorization: $T212_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$T212_BASE_URL/api/v0/equity/orders/stop" \
  -d '{"ticker": "AAPL_US_EQ", "quantity": -5, "stopPrice": 140.00, "timeValidity": "GOOD_TILL_CANCEL"}'
```

**Request Fields:**

| Field          | Type   | Required | Description                                |
| -------------- | ------ | -------- | ------------------------------------------ |
| `ticker`       | string | Yes      | Instrument ticker                          |
| `quantity`     | number | Yes      | Positive for buy, negative for sell        |
| `stopPrice`    | number | Yes      | Trigger price (based on Last Traded Price) |
| `timeValidity` | string | No       | `DAY` (default) or `GOOD_TILL_CANCEL`      |

### Place Stop-Limit Order

`POST /api/v0/equity/orders/stop_limit` (1 req/2s)

```bash
curl -X POST -H "Authorization: $T212_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$T212_BASE_URL/api/v0/equity/orders/stop_limit" \
  -d '{"ticker": "AAPL_US_EQ", "quantity": -5, "stopPrice": 145.00, "limitPrice": 140.00, "timeValidity": "DAY"}'
```

**Request Fields:**

| Field          | Type   | Required | Description                           |
| -------------- | ------ | -------- | ------------------------------------- |
| `ticker`       | string | Yes      | Instrument ticker                     |
| `quantity`     | number | Yes      | Positive for buy, negative for sell   |
| `stopPrice`    | number | Yes      | Trigger price to activate limit order |
| `limitPrice`   | number | Yes      | Limit price for the resulting order   |
| `timeValidity` | string | No       | `DAY` (default) or `GOOD_TILL_CANCEL` |

### Get Pending Orders

`GET /api/v0/equity/orders` (1 req/5s)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/orders"
```

Returns array of Order objects with status NEW, PARTIALLY_FILLED, etc.

### Get Order by ID

`GET /api/v0/equity/orders/{id}` (1 req/1s)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/orders/123456789"
```

### Cancel Order

`DELETE /api/v0/equity/orders/{id}` (50 req/min)

```bash
curl -X DELETE -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/orders/123456789"
```

Returns 200 OK if cancellation request accepted. Order may already be filled.

### Common Order Errors

| Error                          | Cause                   | Solution                            |
| ------------------------------ | ----------------------- | ----------------------------------- |
| `InsufficientFreeForStocksBuy` | Not enough cash         | Check `cash.availableToTrade`       |
| `SellingEquityNotOwned`        | Selling more than owned | Check `quantityAvailableForTrading` |
| `MarketClosed`                 | Outside trading hours   | Check exchange schedule             |

---

## Positions

### Get All Positions

`GET /api/v0/equity/positions` (1 req/1s)

**Query Parameters:**

| Parameter | Type   | Required | Description                                    |
| --------- | ------ | -------- | ---------------------------------------------- |
| `ticker`  | string | No       | Filter by specific ticker (e.g., `AAPL_US_EQ`) |

```bash
# All positions
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/positions"

# Filter by ticker
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/positions?ticker=AAPL_US_EQ"
```

**Response Schema:**

```json
[
  {
    "instrument": {
      "ticker": "AAPL_US_EQ",
      "name": "Apple Inc",
      "isin": "US0378331005",
      "currency": "USD"
    },
    "quantity": 15.5,
    "quantityAvailableForTrading": 12.5,
    "quantityInPies": 3,
    "currentPrice": 185.5,
    "averagePricePaid": 170.25,
    "createdAt": "2024-01-10T09:15:00Z",
    "walletImpact": {
      "currency": "GBP",
      "totalCost": 2089.45,
      "currentValue": 2275.1,
      "unrealizedProfitLoss": 185.65,
      "fxImpact": 12.3
    }
  }
]
```

### Position Fields

| Field                               | Type     | Description                         |
| ----------------------------------- | -------- | ----------------------------------- |
| `quantity`                          | number   | Total shares owned                  |
| `quantityAvailableForTrading`       | number   | Shares available to sell            |
| `quantityInPies`                    | number   | Shares allocated to pies            |
| `currentPrice`                      | number   | Current price (instrument currency) |
| `averagePricePaid`                  | number   | Average cost per share              |
| `createdAt`                         | datetime | Position open date                  |
| `walletImpact.currency`             | string   | Account currency                    |
| `walletImpact.totalCost`            | number   | Total cost in account currency      |
| `walletImpact.currentValue`         | number   | Current value in account currency   |
| `walletImpact.unrealizedProfitLoss` | number   | P&L in account currency             |
| `walletImpact.fxImpact`             | number   | Currency rate impact on value       |

### Position Quantity Scenarios

| Scenario            | quantity | quantityAvailableForTrading | quantityInPies |
| ------------------- | -------- | --------------------------- | -------------- |
| All direct holdings | 10       | 10                          | 0              |
| Some in pie         | 10       | 7                           | 3              |
| All in pie          | 10       | 0                           | 10             |

**Important:** Always check `quantityAvailableForTrading` before placing sell orders.

---

## Instruments

### Ticker Lookup Workflow

When users reference instruments by common names (e.g., "SAP", "Apple", "AAPL"), you **must** look up the exact Trading 212 ticker before making any order, position, or historical data queries. Never construct ticker formats manually.

> **CACHE FIRST:** Always check `/tmp/t212_instruments.json` before calling the API. The instruments endpoint has a 50-second rate limit and returns ~5MB. Only call the API if cache is missing or older than 1 hour.

**Generic search:** Match the user's search term in the three meaningful fields: ticker, name, or shortName. Use one variable (e.g. `SEARCH_TERM`) with `test($q; "i")` on each field so "TSLA", "Tesla", "TL0", etc. match efficiently. For regional filtering (e.g. "US stocks", "European SAP"), use the ISIN prefix (first 2 characters) for country code or `currencyCode` after the grep.

> **IMPORTANT:** Never auto-select instruments. If multiple options exist, you are required to ask the user for their preference.

```bash
# SEARCH_TERM = user query (e.g. TSLA, Tesla, AAPL, SAP)
SEARCH_TERM="TSLA"
CACHE_FILE="/tmp/t212_instruments.json"
if [ -f "$CACHE_FILE" ] && [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE"))) -lt 3600 ]; then
  # Search ticker, name, or shortName fields
  jq --arg q "$SEARCH_TERM" '[.[] | select((.ticker // "" | test($q; "i")) or (.name // "" | test($q; "i")) or (.shortName // "" | test($q; "i")))]' "$CACHE_FILE"
else
  curl -s -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL/api/v0/equity/metadata/instruments" > "$CACHE_FILE"
fi
```

### Get All Instruments

`GET /api/v0/equity/metadata/instruments` (1 req/50s)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/metadata/instruments"
```

**Response Schema:**

```json
[
  {
    "ticker": "AAPL_US_EQ",
    "name": "Apple Inc",
    "shortName": "AAPL",
    "isin": "US0378331005",
    "currencyCode": "USD",
    "type": "STOCK",
    "maxOpenQuantity": 10000,
    "extendedHours": true,
    "workingScheduleId": 123,
    "addedOn": "2020-01-15T00:00:00Z"
  }
]
```

### Instrument Fields

| Field               | Type     | Description                                 |
| ------------------- | -------- | ------------------------------------------- |
| `ticker`            | string   | Unique instrument identifier                |
| `name`              | string   | Full instrument name                        |
| `shortName`         | string   | Short symbol (e.g., AAPL)                   |
| `isin`              | string   | International Securities ID                 |
| `currencyCode`      | string   | Trading currency (ISO 4217)                 |
| `type`              | string   | Instrument type (see below)                 |
| `maxOpenQuantity`   | number   | Maximum position size allowed               |
| `extendedHours`     | boolean  | Whether extended hours trading is available |
| `workingScheduleId` | integer  | Reference to exchange schedule              |
| `addedOn`           | datetime | When added to platform                      |

### Instrument Types

| Type             | Description            |
| ---------------- | ---------------------- |
| `STOCK`          | Common stock           |
| `ETF`            | Exchange-traded fund   |
| `CRYPTOCURRENCY` | Cryptocurrency         |
| `CRYPTO`         | Crypto asset           |
| `FOREX`          | Foreign exchange       |
| `FUTURES`        | Futures contract       |
| `INDEX`          | Index                  |
| `WARRANT`        | Warrant                |
| `CVR`            | Contingent value right |
| `CORPACT`        | Corporate action       |

### Ticker Format

`{SYMBOL}_{EXCHANGE}_{TYPE}` - Examples:

- `AAPL_US_EQ` - Apple on US exchange
- `VUSA_LSE_EQ` - Vanguard S&P 500 on London
- `BTC_CRYPTO` - Bitcoin

### Get Exchange Metadata

`GET /api/v0/equity/metadata/exchanges` (1 req/30s)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/metadata/exchanges"
```

**Response Schema:**

```json
[
  {
    "id": 123,
    "name": "NASDAQ",
    "workingSchedules": [
      {
        "id": 456,
        "timeEvents": [
          { "type": "PRE_MARKET_OPEN", "date": "2024-01-15T09:00:00Z" },
          { "type": "OPEN", "date": "2024-01-15T14:30:00Z" },
          { "type": "CLOSE", "date": "2024-01-15T21:00:00Z" },
          { "type": "AFTER_HOURS_CLOSE", "date": "2024-01-15T01:00:00Z" }
        ]
      }
    ]
  }
]
```

### Time Event Types

| Type                | Description                |
| ------------------- | -------------------------- |
| `PRE_MARKET_OPEN`   | Pre-market session starts  |
| `OPEN`              | Regular trading starts     |
| `BREAK_START`       | Trading break begins       |
| `BREAK_END`         | Trading break ends         |
| `CLOSE`             | Regular trading ends       |
| `AFTER_HOURS_OPEN`  | After-hours session starts |
| `AFTER_HOURS_CLOSE` | After-hours session ends   |
| `OVERNIGHT_OPEN`    | Overnight session starts   |

---

## Historical Data

All historical endpoints use cursor-based pagination with `nextPagePath`.

### Pagination Parameters

| Parameter | Type          | Default | Max | Description                                               |
| --------- | ------------- | ------- | --- | --------------------------------------------------------- |
| `limit`   | integer       | 20      | 50  | Items per page                                            |
| `cursor`  | string/number | -       | -   | Pagination cursor (used in `nextPagePath`)                |
| `ticker`  | string        | -       | -   | Filter by ticker (orders, dividends)                      |
| `time`    | datetime      | -       | -   | Pagination time (used in `nextPagePath` for transactions) |

### Pagination Example

```bash
#!/bin/bash
# Fetch all historical orders with pagination

NEXT_PATH="/api/v0/equity/history/orders?limit=50"

while [ -n "$NEXT_PATH" ]; do
  echo "Fetching: $NEXT_PATH"

  RESPONSE=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL$NEXT_PATH")

  # Process items (e.g., save to file)
  echo "$RESPONSE" | jq '.items[]' >> orders.json

  # Get next page path (null if no more pages)
  NEXT_PATH=$(echo "$RESPONSE" | jq -r '.nextPagePath // empty')

  # Wait 1 second between requests (50 req/min limit)
  if [ -n "$NEXT_PATH" ]; then
    sleep 1
  fi
done

echo "Done fetching all orders"
```

### Historical Orders

`GET /api/v0/equity/history/orders` (50 req/min)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/orders?limit=50"

# Filter by ticker
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/orders?ticker=AAPL_US_EQ&limit=50"
```

**Response Schema:**

```json
{
  "items": [
    {
      "order": {
        "id": 123456789,
        "type": "MARKET",
        "ticker": "AAPL_US_EQ",
        "instrument": {
          "ticker": "AAPL_US_EQ",
          "name": "Apple Inc",
          "isin": "US0378331005",
          "currency": "USD"
        },
        "quantity": 5,
        "filledQuantity": 5,
        "status": "FILLED",
        "side": "BUY",
        "createdAt": "2024-01-15T10:30:00Z"
      },
      "fill": {
        "id": 987654321,
        "type": "TRADE",
        "quantity": 5,
        "price": 185.5,
        "filledAt": "2024-01-15T10:30:05Z",
        "tradingMethod": "TOTV",
        "walletImpact": {
          "currency": "GBP",
          "fxRate": 0.79,
          "netValue": 732.72,
          "realisedProfitLoss": 0,
          "taxes": [
            { "name": "STAMP_DUTY", "quantity": 3.66, "currency": "GBP" }
          ]
        }
      }
    }
  ],
  "nextPagePath": "/api/v0/equity/history/orders?limit=50&cursor=1705326600000"
}
```

### Fill Types

| Type                        | Description               |
| --------------------------- | ------------------------- |
| `TRADE`                     | Regular trade execution   |
| `STOCK_SPLIT`               | Stock split adjustment    |
| `STOCK_DISTRIBUTION`        | Stock distribution        |
| `FOP`                       | Free of payment transfer  |
| `FOP_CORRECTION`            | FOP correction            |
| `CUSTOM_STOCK_DISTRIBUTION` | Custom stock distribution |
| `EQUITY_RIGHTS`             | Equity rights issue       |

### Trading Methods

| Method | Description             |
| ------ | ----------------------- |
| `TOTV` | Traded on trading venue |
| `OTC`  | Over-the-counter        |

### Tax Types (walletImpact.taxes)

| Type                      | Description                |
| ------------------------- | -------------------------- |
| `COMMISSION_TURNOVER`     | Commission on turnover     |
| `CURRENCY_CONVERSION_FEE` | FX conversion fee          |
| `FINRA_FEE`               | FINRA trading activity fee |
| `FRENCH_TRANSACTION_TAX`  | French FTT                 |
| `PTM_LEVY`                | Panel on Takeovers levy    |
| `STAMP_DUTY`              | UK stamp duty              |
| `STAMP_DUTY_RESERVE_TAX`  | UK SDRT                    |
| `TRANSACTION_FEE`         | General transaction fee    |

### Historical Dividends

`GET /api/v0/equity/history/dividends` (50 req/min)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/dividends?limit=50"

# Filter by ticker
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/dividends?ticker=AAPL_US_EQ&limit=50"
```

**Response Schema:**

```json
{
  "items": [
    {
      "ticker": "AAPL_US_EQ",
      "instrument": {
        "ticker": "AAPL_US_EQ",
        "name": "Apple Inc",
        "isin": "US0378331005",
        "currency": "USD"
      },
      "type": "ORDINARY",
      "amount": 12.5,
      "amountInEuro": 14.7,
      "currency": "GBP",
      "tickerCurrency": "USD",
      "grossAmountPerShare": 0.24,
      "quantity": 65.5,
      "paidOn": "2024-02-15T00:00:00Z",
      "reference": "DIV-123456"
    }
  ],
  "nextPagePath": null
}
```

### Dividend Types (Common)

| Type                          | Description                |
| ----------------------------- | -------------------------- |
| `ORDINARY`                    | Regular dividend           |
| `BONUS`                       | Bonus dividend             |
| `INTEREST`                    | Interest payment           |
| `DIVIDEND`                    | Generic dividend           |
| `CAPITAL_GAINS`               | Capital gains distribution |
| `RETURN_OF_CAPITAL`           | Return of capital          |
| `PROPERTY_INCOME`             | Property income (REITs)    |
| `DEMERGER`                    | Demerger distribution      |
| `QUALIFIED_INVESTMENT_ENTITY` | QIE distribution           |
| `TRUST_DISTRIBUTION`          | Trust distribution         |

_Note: Many additional US tax-specific types exist for 1042-S reporting._

### Account Transactions

`GET /api/v0/equity/history/transactions` (50 req/min)

**Pagination:**

- **First request:** Must use only the `limit` parameter (no cursor, no timestamp)
- **Subsequent requests:** Use the `nextPagePath` from the previous response, which includes cursor and timestamp automatically
- **Time filtering:** Transactions cannot be filtered by time - pagination is the only way to navigate through historical data

```bash
# First request - use only limit
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/transactions?limit=50"
```

**Response Schema:**

```json
{
  "items": [
    {
      "type": "DEPOSIT",
      "amount": 1000.0,
      "currency": "GBP",
      "dateTime": "2024-01-10T14:30:00Z",
      "reference": "TXN-123456"
    }
  ],
  "nextPagePath": null
}
```

### Transaction Types

| Type       | Description                  |
| ---------- | ---------------------------- |
| `DEPOSIT`  | Funds deposited to account   |
| `WITHDRAW` | Funds withdrawn from account |
| `FEE`      | Fee charged                  |
| `TRANSFER` | Internal transfer            |

### CSV Reports

**Request report:** `POST /api/v0/equity/history/exports` (1 req/30s)

```bash
curl -X POST -H "Authorization: $T212_AUTH_HEADER" \
  -H "Content-Type: application/json" \
  "$T212_BASE_URL/api/v0/equity/history/exports" \
  -d '{
    "dataIncluded": {
      "includeDividends": true,
      "includeInterest": true,
      "includeOrders": true,
      "includeTransactions": true
    },
    "timeFrom": "2024-01-01T00:00:00Z",
    "timeTo": "2024-12-31T23:59:59Z"
  }'
```

**Response:**

```json
{
  "reportId": 12345
}
```

**Poll for completion:** `GET /api/v0/equity/history/exports` (1 req/min)

```bash
curl -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/exports"
```

**Response:**

```json
[
  {
    "reportId": 12345,
    "status": "Finished",
    "dataIncluded": {
      "includeDividends": true,
      "includeInterest": true,
      "includeOrders": true,
      "includeTransactions": true
    },
    "timeFrom": "2024-01-01T00:00:00Z",
    "timeTo": "2024-12-31T23:59:59Z",
    "downloadLink": "https://trading212-reports.s3.amazonaws.com/..."
  }
]
```

**Download the report:**

```bash
# Get the download link from the response
DOWNLOAD_URL=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/history/exports" | jq -r '.[0].downloadLink')

# Download the CSV file
curl -o trading212_report.csv "$DOWNLOAD_URL"
```

### Report Status Values

| Status       | Description                       |
| ------------ | --------------------------------- |
| `Queued`     | Report request received           |
| `Processing` | Report generation started         |
| `Running`    | Report actively generating        |
| `Finished`   | Complete - downloadLink available |
| `Canceled`   | Report cancelled                  |
| `Failed`     | Generation failed                 |

---

## Pre-Order Validation

### Before BUY - Check Available Funds

```bash
#!/bin/bash
# Validate funds before placing a buy order

TICKER="AAPL_US_EQ"
QUANTITY=10
ESTIMATED_PRICE=185.00
ESTIMATED_COST=$(echo "$QUANTITY * $ESTIMATED_PRICE" | bc)

# Get available funds
AVAILABLE=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/account/summary" | jq '.cash.availableToTrade')

echo "Estimated cost: $ESTIMATED_COST"
echo "Available funds: $AVAILABLE"

if (( $(echo "$ESTIMATED_COST > $AVAILABLE" | bc -l) )); then
  echo "ERROR: Insufficient funds"
  exit 1
fi

echo "OK: Funds available, proceeding with order"
```

### Before SELL - Check Available Shares

```bash
#!/bin/bash
# Validate position before placing a sell order

TICKER="AAPL_US_EQ"
SELL_QUANTITY=5

# Get position for the ticker
POSITION=$(curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/positions?ticker=$TICKER")

AVAILABLE_QTY=$(echo "$POSITION" | jq '.[0].quantityAvailableForTrading // 0')

echo "Sell quantity: $SELL_QUANTITY"
echo "Available to sell: $AVAILABLE_QTY"

if (( $(echo "$SELL_QUANTITY > $AVAILABLE_QTY" | bc -l) )); then
  echo "ERROR: Insufficient shares (some may be in pies)"
  exit 1
fi

echo "OK: Shares available, proceeding with order"
```

---

## Rate Limit Handling

### Understanding Rate Limits

Rate limits are **per-account**, not per API key or IP address. If you have multiple applications using the same Trading 212 account, they share the same rate limit pool.

### Response Headers

Every API response includes rate limit headers:

| Header                  | Description                      |
| ----------------------- | -------------------------------- |
| `x-ratelimit-limit`     | Total requests allowed in period |
| `x-ratelimit-period`    | Time period in seconds           |
| `x-ratelimit-remaining` | Requests remaining               |
| `x-ratelimit-reset`     | Unix timestamp when limit resets |
| `x-ratelimit-used`      | Requests already made            |

### Avoid Burst Requests to avoid Rate Limiting

**Do not send requests in bursts.** Even if an endpoint allows 50 requests per minute, sending them all at once can trigger rate limiting and degrade performance.
Pace your requests evenly, for example, by making one call every 1.2 seconds, ensuring you always stay within the limit.

**Bad approach (bursting):**

```bash
# DON'T DO THIS - sends all requests at once
for ticker in AAPL_US_EQ MSFT_US_EQ GOOGL_US_EQ; do
  curl -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL/api/v0/equity/positions?ticker=$ticker" &
done
wait
```

**Good approach (paced):**

```bash
# DO THIS - space requests evenly
for ticker in AAPL_US_EQ MSFT_US_EQ GOOGL_US_EQ; do
  curl -H "Authorization: $T212_AUTH_HEADER" \
    "$T212_BASE_URL/api/v0/equity/positions?ticker=$ticker"
  sleep 1.2  # 1.2 second between requests for 50 req/m limit
done
```

### Caching Strategy

For data that doesn't change frequently, cache locally to reduce API calls:

```bash
#!/bin/bash
# Cache instruments list (changes rarely)

CACHE_FILE="/tmp/t212_instruments.json"
CACHE_MAX_AGE=3600  # 1 hour

if [ -f "$CACHE_FILE" ]; then
  CACHE_AGE=$(($(date +%s) - $(stat -f %m "$CACHE_FILE")))
  if [ "$CACHE_AGE" -lt "$CACHE_MAX_AGE" ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# Cache expired or doesn't exist - fetch fresh data
curl -s -H "Authorization: $T212_AUTH_HEADER" \
  "$T212_BASE_URL/api/v0/equity/metadata/instruments" > "$CACHE_FILE"

cat "$CACHE_FILE"
```

---

## Safety Guidelines

1. **Test in demo first** - Always validate workflows before live trading
2. **Validate before ordering** - Check funds (`cash.availableToTrade`) before buy, positions (`quantityAvailableForTrading`) before sell
3. **Confirm destructive actions** - Order placement and cancellation are irreversible
4. **API is not idempotent** - Duplicate requests may create duplicate orders
5. **Never log credentials** - Use environment variables
6. **Respect rate limits** - Space requests evenly, never burst
7. **Max 50 pending orders** - Per ticker, per account
8. **Cache metadata** - Instruments and exchanges change rarely
