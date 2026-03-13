---
name: blofin-asset-manager
description: "Manage BloFin assets — check balances across account types, transfer funds between accounts (funding, futures, copy trading, earn, spot), and track deposit/withdrawal history. Requires authenticated API access with TRANSFER permission."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "🏦"
    requires:
      bins:
        - node
      env:
        - BLOFIN_API_KEY
        - BLOFIN_API_SECRET
        - BLOFIN_PASSPHRASE
    primaryEnv: BLOFIN_API_KEY
auto_activate:
  - "transfer funds"
  - "move funds"
  - "deposit"
  - "withdrawal"
  - "asset balance"
  - "fund transfer"
  - "blofin assets"
---

# BloFin Asset Manager

Manage assets across BloFin accounts — check balances, transfer funds between account types, and track deposit/withdrawal history.

## Account Types

BloFin has multiple account types for different purposes:

| Account | Code | Description |
|---------|------|-------------|
| **Funding** | `funding` | Main wallet for deposits and withdrawals |
| **Futures** | `futures` | Futures/perpetual swap trading (also used for unified accounts) |
| **Copy Trading** | `copy_trading` | Copy trading account |
| **Earn** | `earn` | Earn/staking products |
| **Spot** | `spot` | Spot trading |
| **Inverse Contract** | `inverse_contract` | Inverse contract trading |

**Typical flow:** Deposit to Funding → Transfer to Futures → Trade → Transfer back to Funding → Withdraw

---

## Available Tools (via blofin-mcp)

### get_asset_balances — Balances Across Accounts

Check balances for any account type.

```
Use get_asset_balances to see funds in a specific account.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `accountType` | String | Yes | `funding`, `futures`, `copy_trading`, `earn`, `spot` |
| `currency` | String | No | Filter by currency, e.g. `USDT` |

**Key response fields:** `currency`, `balance` (total), `available` (can be used/transferred), `frozen` (locked).

**Example prompts:**
- "How much USDT do I have in my funding account?"
- "Show all my balances across all accounts"
- "What's available in my futures account?"

To show all accounts, query each account type and present a combined view:

```
Asset Overview
==============
| Account       | USDT     | BTC      | ETH     |
|---------------|----------|----------|---------|
| Funding       | X,XXX.XX | X.XXXX   | X.XXXX  |
| Futures       | X,XXX.XX | -        | -       |
| Copy Trading  | XXX.XX   | -        | -       |
| Spot          | XXX.XX   | X.XXXX   | X.XXXX  |
| Total         | X,XXX.XX | X.XXXX   | X.XXXX  |
```

---

### fund_transfer — Transfer Between Accounts

Move funds between account types.

```
Use fund_transfer to move funds. ALWAYS confirm the transfer details with the user first.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `currency` | String | Yes | Currency, e.g. `USDT` |
| `amount` | String | Yes | Amount to transfer |
| `fromAccount` | String | Yes | Source: `funding`, `futures`, `copy_trading`, `earn`, `spot`, `inverse_contract` |
| `toAccount` | String | Yes | Destination: same options as above |
| `clientId` | String | No | Custom transfer ID (max 32 chars, alphanumeric/underscore) |

**Important notes:**
- Transfers are instant and free within BloFin
- The `available` balance in the source account must be >= the transfer amount
- For unified accounts, use `futures` as the account type
- `clientId` must be unique (error 150003 if duplicate)

**Example prompts:**
- "Transfer 100 USDT from funding to futures"
- "Move all my USDT from futures back to funding"
- "Send 500 USDT to my copy trading account"

**Pre-transfer checklist:**
1. Verify source account has sufficient available balance
2. Confirm transfer details: currency, amount, from, to
3. Execute transfer
4. Verify destination account balance increased

---

### get_fund_transfer_history — Transfer Records

View past fund transfers.

```
Use get_fund_transfer_history to see transfer records.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `currency` | String | No | Filter by currency |
| `fromAccount` | String | No | Filter by source account |
| `toAccount` | String | No | Filter by destination account |
| `before` / `after` | String | No | Pagination by timestamp (ms) |
| `limit` | String | No | Max 100, default 100 |

**Key response fields:** `transferId`, `currency`, `fromAccount`, `toAccount`, `amount`, `ts`, `clientId`.

**Example prompts:**
- "Show my recent fund transfers"
- "When did I last transfer USDT to futures?"

---

### get_deposit_history — Deposit Records

View blockchain deposit history.

```
Use get_deposit_history to check deposit status and records.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `currency` | String | No | Filter by currency, e.g. `USDT` |
| `depositId` | String | No | Specific deposit ID |
| `txId` | String | No | Blockchain transaction hash |
| `state` | String | No | `0` pending, `1` done, `2` failed, `3` KYT review |
| `before` / `after` | String | No | Pagination by timestamp |
| `limit` | String | No | Max 100, default 20 |

**Key response fields:** `currency`, `chain` (e.g. `TRC20`, `ERC20`), `address`, `amount`, `state`, `confirm` (confirmations), `txId`, `ts`.

**Deposit states:**

| State | Meaning |
|-------|---------|
| `0` | Pending — waiting for confirmations |
| `1` | Done — successfully credited |
| `2` | Failed |
| `3` | KYT — under compliance review |

**Example prompts:**
- "Has my USDT deposit arrived?"
- "Show all my deposit history"
- "Check the status of my latest deposit"

---

### get_withdrawal_history — Withdrawal Records

View withdrawal history.

```
Use get_withdrawal_history to check withdrawal status and records.
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `currency` | String | No | Filter by currency |
| `withdrawId` | String | No | Specific withdrawal ID |
| `txId` | String | No | Blockchain transaction hash |
| `type` | String | No | `0` blockchain, `1` internal transfer |
| `state` | String | No | See states below |
| `before` / `after` | String | No | Pagination by timestamp |
| `limit` | String | No | Max 100, default 20 |

**Withdrawal states:**

| State | Meaning |
|-------|---------|
| `0` | Waiting for manual review |
| `2` | Failed |
| `3` | Success |
| `4` | Cancelled |
| `6` | KYT — under compliance review |
| `7` | Processing |

**Key response fields:** `currency`, `chain`, `address`, `amount`, `fee`, `feeCurrency`, `state`, `txId`, `ts`, `withdrawId`.

**Example prompts:**
- "Has my withdrawal been processed?"
- "Show my withdrawal history"
- "How much did I pay in withdrawal fees?"

---

### get_apikey_info — API Key Information

Check API key permissions and details.

```
Use get_apikey_info to verify API key status and permissions.
```

**Response fields:** `uid`, `apiName`, `apiKey`, `readOnly` (0=read+write, 1=read only), `ips`, `type`, `expireTime`, `createTime`.

## Safety Rules

1. **Always confirm transfer details** before executing — wrong direction transfers are instant
2. **Verify available balance** in source account before transferring
3. **Never expose API keys or withdrawal addresses** in conversation logs
4. **Warn about withdrawal delays** — blockchain withdrawals require manual review and may take time
5. **Inform about withdrawal fees** before the user initiates a withdrawal
