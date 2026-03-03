---
name: crypto-agent-trading
description: "Execute crypto trades (buy, sell, swap, exchange) and query account balances, market prices, and transaction history via the Crypto.com API. View weekly trading limits and portfolio positions. Use when the user wants to trade, purchase, sell, or swap cryptocurrency, check token prices or portfolio balances, view recent trades, discover coins, or activate the kill switch. Supports BTC, ETH, CRO, and 200+ tokens across fiat and crypto wallets."
user-invocable: true
metadata:
---

# Skill: crypto-agent-trading

## Agent Capability Requirements

This skill requires your agent platform to support the following capabilities. If your platform lacks any **required** capability, the skill will not function.

| Capability | Required | Details |
|---|---|---|
| **Shell command execution** | Yes | Must be able to run `npx tsx ./scripts/...` and capture stdout |
| **Environment variables** | Yes | Must read `CDC_API_KEY` and `CDC_API_SECRET` from the shell environment |
| **JSON parsing** | Yes | Must parse structured JSON from script stdout to extract fields |
| **Multi-turn conversation** | Yes | Trading uses a quote → confirm flow that spans multiple user turns |
| **Persistent memory** | No | Used for `confirmation_required` preference. If unsupported, default to always confirming trades |
| **Elapsed-time awareness** | No | Used to check quote expiry (`countdown` field). If unsupported, always attempt confirmation and handle `invalid_quotation` errors gracefully |

## CRITICAL: How This Skill Works

**You MUST use the TypeScript scripts for ALL API interactions. NEVER call the API directly with `curl`, `fetch`, or any other HTTP method.**

The scripts handle request signing, error handling, and response formatting. If you bypass them:
- The request will fail (missing HMAC signature)
- The response won't be filtered or structured

**For every user request, find the matching command below and run it via `npx tsx`. Read the JSON output. Act on it.**

## Configurations
- BASE_URL: `https://wapi.crypto.com`
- CDC_API_KEY: `{{env.CDC_API_KEY}}`
- CDC_API_SECRET: `{{env.CDC_API_SECRET}}`
- CONFIRMATION_REQUIRED: `{{memory.confirmation_required}}` (Default: true)
- SKILL_DIR: The directory containing this `SKILL.md` file. Resolve it from the path you loaded this file from (e.g. if you read `/home/user/skills/crypto-agent-trading/SKILL.md`, then `SKILL_DIR` is `/home/user/skills/crypto-agent-trading`).

## Environment Setup
- Both `CDC_API_KEY` and `CDC_API_SECRET` must be set as environment variables before use.
- **Before running any script**, check whether both variables are set by running:
  ```bash
  echo "CDC_API_KEY=${CDC_API_KEY:+set}" "CDC_API_SECRET=${CDC_API_SECRET:+set}"
  ```
  If either prints empty instead of `set`, prompt the user:
  > "Your API credentials are not configured. Please set them in your terminal before I can proceed:
  > ```
  > export CDC_API_KEY="your-api-key"
  > export CDC_API_SECRET="your-api-secret"
  > ```
  > You can generate an API key at https://help.crypto.com/en/articles/13843786-api-key-management.
  > Let me know once you've set them."
  
  Then **stop and wait** for the user to confirm before retrying.
- If a script returns a `MISSING_ENV` error, treat it the same way: prompt the user to set the variables and wait.

## Script Commands

**ALL API interactions MUST go through these scripts.** They handle signing, execution, filtering, and error formatting. Run the appropriate command below via shell, then parse the JSON output.

**Prerequisite:** `npx tsx` (Node.js 18+ required; `tsx` is fetched automatically by `npx`).

**Important:** All script paths below use `$SKILL_DIR` as a placeholder for this skill's root directory. Resolve it from the path you loaded this SKILL.md from, or `cd` into the skill directory and use `./scripts/...` as the path. Either approach works.

### Account Commands

```bash
# Filtered non-zero balances (scope: fiat | crypto | all)
npx tsx $SKILL_DIR/scripts/account.ts balances [fiat|crypto|all]

# Single token balance lookup
npx tsx $SKILL_DIR/scripts/account.ts balance <SYMBOL>

# Weekly trading limit
npx tsx $SKILL_DIR/scripts/account.ts trading-limit

# Find funded source wallets for a trade type
npx tsx $SKILL_DIR/scripts/account.ts resolve-source <purchase|sale|exchange>

# Kill switch — revoke API key
npx tsx $SKILL_DIR/scripts/account.ts revoke-key
```

### Trade Commands

Trading follows a **two-step flow**: get a quotation first, then confirm the order.

```bash
# Step 1 — Get quotation (type: purchase | sale | exchange)
npx tsx $SKILL_DIR/scripts/trade.ts quote <type> '<json-params>'
# Returns: {"ok": true, "data": {"id": "<quotation-id>", "from_amount": {...}, "to_amount": {...}, "countdown": 15, ...}}

# Step 2 — Confirm order: pass the data.id from Step 1 as <quotation-id>
npx tsx $SKILL_DIR/scripts/trade.ts confirm <type> <quotation-id>

# View recent transactions
npx tsx $SKILL_DIR/scripts/trade.ts history
```

**How to map user intent to trade type:**

| User says | Trade type | From | To |
|-----------|-----------|------|-----|
| "Buy CRO with 100 USD" | `purchase` | USD (fiat) | CRO (crypto) |
| "Sell 0.1 BTC" | `sale` | BTC (crypto) | USD (fiat) |
| "Swap 0.1 BTC to ETH" | `exchange` | BTC (crypto) | ETH (crypto) |

**Quotation JSON params by trade type:**

| Type | JSON fields |
|------|------------|
| purchase | `{"from_currency":"USD","to_currency":"CRO","from_amount":"100"}` or use `to_amount` instead |
| sale | `{"from_currency":"BTC","to_currency":"USD","from_amount":"0.1","fixed_side":"from"}` |
| exchange | `{"from_currency":"BTC","to_currency":"ETH","from_amount":"0.1","side":"buy"}` |

**Example — "Buy CRO with 100 USD":**

1. Run: `npx tsx $SKILL_DIR/scripts/trade.ts quote purchase '{"from_currency":"USD","to_currency":"CRO","from_amount":"100"}'`
2. Read `data.id`, `data.from_amount`, `data.to_amount`, `data.countdown` from the response.
3. **If confirmation required** (default): Ask user "Confirm: 100 USD for X CRO? Valid for {countdown}s. Reply 'YES' to proceed."
   - If user says YES (within countdown): `npx tsx $SKILL_DIR/scripts/trade.ts confirm purchase <data.id>`
4. **If confirmation opted out** (`memory.confirmation_required` is `false`): Skip asking and immediately run `npx tsx $SKILL_DIR/scripts/trade.ts confirm purchase <data.id>`

**Opt-in / Opt-out:** Users can say "stop asking for confirmation" to auto-execute trades, or "require confirmation" to re-enable the prompt. See Section 3 below.

### Coin Discovery Commands

```bash
# Search coins
npx tsx $SKILL_DIR/scripts/coins.ts search '{"keyword":"BTC","sort_by":"rank","sort_direction":"asc","native_currency":"USD","page_size":10}'
```

**Required JSON parameters:**

| Parameter | Type | Allowed values |
|-----------|------|----------------|
| `sort_by` | string | `rank`, `market_cap`, `alphabetical`, `volume`, `performance` |
| `sort_direction` | string | `asc`, `desc` |
| `native_currency` | string | Uppercase currency code (e.g. `USD`) |
| `keyword` | string | Search string, 1–100 chars; matches coin name and symbol only |
| `page_size` | integer | Number of results per page |

**Optional:** `page_token` — opaque token for fetching the next page (see pagination below).

**Pagination:** The response includes a `pagination` object with `has_more` (boolean) and `next_page_token` (string). When `has_more` is `true`, pass `next_page_token` as `page_token` in the next request to fetch the next page.

**Key response fields per coin:** `rails_id` (identical to `currency_id` / `currency` in trade and account APIs — use this to cross-reference), `price_native`, `price_usd`, `percent_change_*_native` (price performance over past timeframes, e.g. `percent_change_24h_native`).

### Output Format

Every script prints structured JSON to stdout:

**Success:**
```json
{"ok": true, "data": { ... }}
```

**Error:**
```json
{"ok": false, "error": "ERROR_CODE", "error_message": "Human-readable message"}
```

## Constraints
- **Validation:** Success requires `ok: true` in the script output.
- **Confirmation Window:** Quote validity is defined by the `countdown` field in the quotation data.
- **Execution Warning:** If order confirmation takes > 5s, notify: "Order submitted but taking longer than expected. Check order status with 'Show recent trades'".
- **Rate Limits:**
  - Max **10 trades per minute**.
  - Max **100 API calls per minute**.
  - On HTTP 429 (`RATE_LIMITED` error): wait **60 seconds** before retrying the same request. Inform the user: "Rate limit reached — please wait 60 seconds before trying again."

## Error Handling

All scripts return structured errors. Parse the `error` field to determine the appropriate response.

### Script Error Codes

These are the `error` values in the script's JSON output. They tell you *what category* of failure occurred.

| Error Code | Meaning | Agent Response |
|------------|---------|----------------|
| `MISSING_ENV` | `CDC_API_KEY` or `CDC_API_SECRET` not set | Tell user to set env vars via terminal |
| `API_ERROR` | API returned non-200 or `ok !== true` | Report: "Transaction failed: {error_message}" |
| `INVALID_ARGS` | Bad command-line arguments | Show correct usage from the `error_message` |
| `QUOTATION_FAILED` | Quotation request rejected by API | Report the `error_message` to user (see API errors below) |
| `EXECUTION_FAILED` | Order confirmation failed | Report and suggest: "Check order status with 'Show recent trades'" |
| `API_KEY_NOT_FOUND` | Key already revoked or does not exist | "API key not found — it may have already been revoked." |
| `RATE_LIMITED` | Too many requests (HTTP 429) | "Rate limit reached — please wait 60 seconds before trying again." |
| `UNKNOWN` | Unexpected error | Report the raw `error_message` |

**Rule:** When `ok` is `false` in the output, stop the current operation and report the error to the user using the guidance above. Never proceed to the next step after a failure.

### Common API Errors (Quick Reference)

These are the *specific* API error codes that appear inside the `error_message` of `QUOTATION_FAILED`, `EXECUTION_FAILED`, or `API_ERROR` responses. They tell you *why* the API rejected the request.

| `error` | Meaning | Recovery |
|---------|---------|----------|
| `not_enough_balance` | Insufficient funds | Check balances, reduce trade amount |
| `invalid_currency` | Currency code not recognized | Verify via coin search |
| `invalid_quotation` | Quote expired or already used | Request a new quotation |
| `failed_to_create_quotation` | Quotation engine error | Retry shortly |
| `not_eligible_for_prime` | Not eligible for Prime benefits | Proceed without Prime |
| `unauthorized` | Account not approved for trading | Contact support |
| `restricted_feature` | Feature restricted on account | Report `error_message` to user |
| `existing_currency_order_error` | An existing order is in progress | Wait or cancel existing order |
| `viban_purchase_not_enabled` | Fiat-to-crypto not enabled | Account feature not available |
| `crypto_viban_not_enabled` | Crypto-to-fiat not enabled | Account feature not available |
| `bank_transfer_not_enabled` | Bank transfer not enabled | Account feature not available |
| `missing_parameter` | Required parameter missing | Script bug — report it |
| `failed_to_create_transaction` | Transaction creation failed | Retry or contact support |
| `key_not_active` | API key revoked or expired | Generate a new API key, update env vars |
| `api_key_not_found` | Key doesn't exist or belongs to another user | Verify correct key is set in `CDC_API_KEY` |

For dynamic errors (limit exceeded, currency disabled, cooling-off, etc.), report the `error` and `error_message` directly to the user. For full details, see [references/errors.md](references/errors.md).

---

## Logic & Rules

### 1. Asset & Source Disambiguation

Determine the trade type first:
- **Purchase** — fiat → crypto
- **Sale** — crypto → fiat
- **Exchange** — crypto → crypto

Then resolve the source wallet:
- For **purchase**: run `npx tsx $SKILL_DIR/scripts/account.ts resolve-source purchase`. The script returns only funded fiat entries.
- For **sale** or **exchange**: run `npx tsx $SKILL_DIR/scripts/account.ts resolve-source sale` (or `exchange`). The script returns only funded crypto entries.

**Result (from `data.status`):**
- **`SELECTED`** → auto-select `data.currency`.
- **`AMBIGUOUS`** → prompt user to choose from `data.options`.
- **`EMPTY`** → inform user "No funded wallets found" and stop.

**"Sell All" Scenario:** If user says "Sell all [TOKEN]", run `npx tsx $SKILL_DIR/scripts/account.ts balance [TOKEN]`. Use the `data.available` amount (or `data.balance`) as `from_amount` for the quotation.

### 2. Trading Process (Quotation → Confirmation → Execution)

When the user asks to buy, sell, or swap crypto, **always** follow this three-step flow:

- **Step A — Get Quotation:** Build the JSON params from the user's request (see the "Quotation JSON params" table in Trade Commands) and run:
  `npx tsx $SKILL_DIR/scripts/trade.ts quote <type> '<json-params>'`
  Read `data.id`, `data.from_amount`, `data.to_amount`, and `data.countdown` from the response.

- **Step B — Ask User to Confirm:**
    - **IF** `memory.confirmation_required` is `true` (or unset):
        - Prompt: "Confirm: {from_amount} for {to_amount}? Valid for {countdown}s. Reply 'YES' to proceed."
        - **Expiration Logic:** If the user replies "YES" after `countdown` seconds have elapsed, reject: "Transaction rejected: The quotation rate has expired. Please request a new quote."
        - Execute Step C ONLY if user replies "YES" within the valid window.
    - **ELSE (Opted Out):**
        - Notify: "Quotation received. Proceeding to execution automatically..."
        - Immediately proceed to Step C.

- **Step C — Execute Order:** Run: `npx tsx $SKILL_DIR/scripts/trade.ts confirm <type> <data.id>` using the `id` from Step A.

### 3. Memory Management (Opt-in/Out)
- **To Opt-out:** If user says "stop asking for confirmation" or "enable auto-trade", update `memory.confirmation_required` to `false`.
- **To Opt-in:** If user says "require confirmation" or "enable manual trade", update `memory.confirmation_required` to `true`.
- **Platforms without persistent memory:** If your platform does not support `{{memory.*}}`, treat `confirmation_required` as always `true` (safest default).

### 4. Error Handling
- All script outputs include an `ok` field. Success is defined ONLY as `ok: true`.
- If `ok` is `false`, read `error` and respond per the Error Handling table above.
- Never proceed to the next step after a failed command.

### 5. Account & History
- **History:** Run `npx tsx $SKILL_DIR/scripts/trade.ts history` — display the entries from `data`.
- **Weekly Trading Limit:** Run `npx tsx $SKILL_DIR/scripts/account.ts trading-limit` — display as: "📊 Weekly Trading Limit: {data.used} / {data.limit} USD (Remaining: {data.remaining} USD)".
- **Balances (Categorized):**
    - If "List Fiat": run `npx tsx $SKILL_DIR/scripts/account.ts balances fiat`.
    - If "List Crypto": run `npx tsx $SKILL_DIR/scripts/account.ts balances crypto`.
    - If "List All": run `npx tsx $SKILL_DIR/scripts/account.ts balances all`. **Crucial:** Display Fiat category first, followed by Crypto balances below.
    - The scripts automatically filter out zero-balance entries. If a category has no entries in the output, display "No holdings" under that header.

### 6. Kill Switch
- **Trigger:** User says "STOP ALL TRADING", "kill switch", or similar emergency stop command.
- **ALWAYS require explicit confirmation** regardless of `memory.confirmation_required`:
    - Prompt: "⚠️ WARNING: This will immediately revoke your API key and disable all trading. A new API key must be generated to resume. Type 'CONFIRM KILL SWITCH' to proceed."
    - Execute ONLY if user replies with the exact phrase.
- **Execution:** Run `npx tsx $SKILL_DIR/scripts/account.ts revoke-key`.
- **On success (`ok: true`):** Notify: "🛑 Kill switch activated. API key has been revoked. All trading is disabled. Generate a new API key and update your environment variables to resume."
- **On `API_KEY_NOT_FOUND` error:** Notify: "API key not found — it may have already been revoked or does not exist."
- **Idempotency:** Revoking an already-revoked key is not an error; treat it the same as a successful revocation.

### 7. Balance Display Format
- **Fiat Header:** "🏦 Fiat Balances"
- **Crypto Header:** "🪙 Crypto Balances"
- Always list Fiat section before Crypto section when both are requested.
- **Never display zero-balance assets.** Only show assets with a balance greater than 0. If all assets in a category are zero, show "No holdings" under that header.
