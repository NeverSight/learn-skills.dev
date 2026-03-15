---
name: assets
description: KuCoin Assets management using the KuCoin API. Account information, balances, deposits, withdrawals, sub-accounts, and fee rates. Authentication requires API Key, API Secret, and Passphrase.
metadata:
  version: 1.0.0
  author: KuCoin
license: MIT
---

# KuCoin Assets Skill

Assets management on KuCoin using authenticated API endpoints. Requires API Key, API Secret, and Passphrase for all endpoints. Return the result in JSON format.

> **Note:** This skill only supports Classic REST API GET endpoints (read-only operations).

## Quick Reference

### Classic API -- Account & Funding

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `GET /api/v2/user-info` | Get Account Summary Info | None | None | Yes |
| `GET /api/v1/user/api-key` | Get Apikey Info | None | None | Yes |
| `GET /api/v1/hf/accounts/opened` | Get Account Type - Spot | None | None | Yes |
| `GET /api/v1/accounts` | Get Account List - Spot | None | currency, type | Yes |
| `GET /api/v1/accounts/{accountId}` | Get Account Detail - Spot | accountId (path) | None | Yes |
| `GET /api/v3/margin/accounts` | Get Account - Cross Margin. **Note: Requires margin trading to be enabled on the account.** | None | quoteCurrency, queryType | Yes |
| `GET /api/v3/isolated/accounts` | Get Account - Isolated Margin. **Note: Requires margin trading to be enabled on the account.** | None | symbol, quoteCurrency, queryType | Yes |
| `GET /api/v1/account-overview` | Get Account - Futures. **Note: Must use Futures base URL (`https://api-futures.kucoin.com`).** | None | currency | Yes |
| `GET /api/v1/accounts/ledgers` | Get Account Ledgers - Spot/Margin | None | currency, direction, bizType, startAt, endAt, currentPage, pageSize | Yes |
| `GET /api/v1/hf/accounts/ledgers` | Get Account Ledgers - Trade_hf | None | currency, direction, bizType, lastId, limit, startAt, endAt | Yes |
| `GET /api/v3/hf/margin/account/ledgers` | Get Account Ledgers - Margin_hf | None | currency, direction, bizType, lastId, limit, startAt, endAt | Yes |
| `GET /api/v1/transaction-history` | Get Account Ledgers - Futures. **Note: Must use Futures base URL (`https://api-futures.kucoin.com`).** | None | currency, type, offset, forward, maxCount, startAt, endAt | Yes |

### Classic API -- Sub Account

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `GET /api/v2/sub/user` | Get Sub-Account List - Summary Info | None | currentPage, pageSize | Yes |
| `GET /api/v1/sub-accounts/{subUserId}` | Get Sub-Account Detail - Balance | subUserId (path) | includeBaseAmount, baseCurrency, baseAmount | Yes |
| `GET /api/v2/sub-accounts` | Get Sub-Account List - Spot Balance (V2) | None | currentPage, pageSize | Yes |
| `GET /api/v1/account-overview-all` | Get Sub-Account List - Futures Balance (V2). **Note: Must use Futures base URL (`https://api-futures.kucoin.com`).** | None | currency | Yes |

### Classic API -- Sub Account API

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `GET /api/v1/sub/api-key` | Get Sub-Account API List | subName | apiKey | Yes |

### Classic API -- Deposit

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `GET /api/v3/deposit-addresses` | Get Deposit Address (V3) | currency | chain | Yes |
| `GET /api/v1/deposits` | Get Deposit History | currency | status, startAt, endAt, currentPage, pageSize | Yes |

### Classic API -- Withdrawals

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `GET /api/v1/withdrawals/quotas` | Get Withdrawal Quotas | currency | chain | Yes |
| `GET /api/v1/withdrawals/{withdrawalId}` | Get Withdrawal History By ID | withdrawalId (path) | None | Yes |
| `GET /api/v1/withdrawals` | Get Withdrawal History | currency | status, startAt, endAt, currentPage, pageSize | Yes |

### Classic API -- Transfer

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `GET /api/v1/accounts/transferable` | Get Transfer Quotas | currency, type | tag | Yes |

### Classic API -- Trade Fee

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `GET /api/v1/base-fee` | Get Basic Fee - Spot/Margin | None | currencyType | Yes |
| `GET /api/v1/trade-fees` | Get Actual Fee - Futures | symbols | None | Yes |

---

## Parameters

### Common Parameters

* **currency**: Currency code (e.g., `BTC`, `USDT`, `ETH`). Some endpoints support querying multiple currencies separated by commas.
* **chain**: The chain ID of a currency (e.g., `eth`, `trx`, `bsc`, `ton2`, `arbitrum`). Recommended for multi-chain currencies.
* **startAt / endAt**: Start and end time in milliseconds since Unix epoch.
* **currentPage**: Current request page, default 1.
* **pageSize**: Number of results per page. Varies by endpoint (typical min 10, max 100-500).
* **lastId**: The ID of the last set of data from the previous batch. Used for cursor-based pagination.
* **direction**: Direction of transfer: `in` or `out`.

### Classic API Account Parameters

* **type** (Spot Account List): Account type: `main` (funding), `trade` (spot).
* **accountId**: Account ID (path parameter for account detail).
* **quoteCurrency**: Quote currency for margin accounts: `USDT`, `KCS`, `BTC`.
* **queryType** (Cross Margin): `MARGIN`, `MARGIN_V2`, `ALL`.
* **queryType** (Isolated Margin): `ISOLATED`, `ISOLATED_V2`, `ALL`.
* **bizType** (Spot/Margin Ledger): `DEPOSIT`, `WITHDRAW`, `TRANSFER`, `SUB_TRANSFER`, `TRADE_EXCHANGE`, `MARGIN_EXCHANGE`, `KUCOIN_BONUS`, `BROKER_TRANSFER`.
* **bizType** (Trade_hf Ledger): `TRADE_EXCHANGE`, `TRANSFER`, `SUB_TRANSFER`, `RETURNED_FEES`, `DEDUCTION_FEES`, `OTHER`.
* **bizType** (Margin_hf Ledger): `TRANSFER`, `MARGIN_EXCHANGE`, `ISOLATED_EXCHANGE`, `LIQUIDATION`, `ASSERT_RETURN`.
* **type** (Futures Ledger): `RealisedPNL`, `Deposit`, `Withdrawal`, `TransferIn`, `TransferOut`.
* **offset**: Start offset for futures ledger pagination.
* **forward**: Boolean. `true` for forward lookup (default), `false` for backward.
* **maxCount**: Displayed size per page for futures ledger. Default 50.
* **limit**: Number of results per page for HF ledger queries.

### Sub Account Parameters

* **subUserId**: The user ID of a sub-account (path parameter).
* **subName**: Sub-account name (for API key queries).
* **apiKey**: API key of the sub-account (filter parameter).
* **includeBaseAmount**: Boolean. `true` to display all currencies including zero-balance ones.
* **baseCurrency**: Currency used to convert and display asset values.
* **baseAmount**: Filter: currency balance must be >= this amount.

### Deposit & Withdrawal Parameters

* **status** (Deposit History): `PROCESSING`, `SUCCESS`, `FAILURE`, `WAIT_TRM_MGT`, `TRM_MGT_REJECTED`.
* **status** (Withdrawal History): `PROCESSING`, `REVIEW`, `WALLET_PROCESSING`, `SUCCESS`, `FAILURE`.
* **withdrawalId**: Withdrawal ID (path parameter).

### Transfer Parameters

* **type** (Transfer Quotas): Account type: `MAIN`, `TRADE`, `MARGIN`, `ISOLATED`, `MARGIN_V2`, `ISOLATED_V2`.
* **tag**: Trading pair required when account type is `ISOLATED` (e.g., `BTC-USDT`).

### Trade Fee Parameters

* **currencyType**: Currency type: `0` (crypto currency), `1` (fiat currency). Default `0`.
* **symbols**: Trading pair symbols for futures fee query (e.g., `XBTUSDTM`).

---

## Enums

### Account Types (Classic API)

| Value | Description |
|-------|-------------|
| `main` | Funding account |
| `trade` | Spot trading account |
| `MAIN` | Funding account (transfer context) |
| `TRADE` | Spot trading account (transfer context) |
| `CONTRACT` | Futures account (transfer context) |
| `MARGIN` | Cross margin account (HF) |
| `ISOLATED` | Isolated margin account (HF) |
| `MARGIN_V2` | Cross margin account (legacy, phasing out) |
| `ISOLATED_V2` | Isolated margin account (legacy, phasing out) |

### Deposit Status

| Value | Description |
|-------|-------------|
| `PROCESSING` | Deposit is being processed |
| `SUCCESS` | Deposit completed successfully |
| `FAILURE` | Deposit failed |
| `WAIT_TRM_MGT` | Waiting for travel rule management |
| `TRM_MGT_REJECTED` | Rejected by travel rule management |

### Withdrawal Status

| Value | Description |
|-------|-------------|
| `REVIEW` | Under review |
| `PROCESSING` | Processing |
| `WALLET_PROCESSING` | Wallet processing |
| `SUCCESS` | Withdrawal completed successfully |
| `FAILURE` | Withdrawal failed |

---

## Authentication

For all endpoints, you must provide KuCoin API credentials.

Required credentials:

* **API Key**: Your KuCoin API key (sent as `KC-API-KEY` header)
* **API Secret**: Your KuCoin API secret (used for HMAC-SHA256 signing)
* **Passphrase**: The passphrase you set when creating the API key (sent as `KC-API-PASSPHRASE` header, encrypted for API Key Version 2)

Base URLs:

| Environment | URL |
|-------------|-----|
| Production | `https://api.kucoin.com` |

---

## Security

### Share Credentials

Users can provide KuCoin API credentials by sending a file where the content is in the following format:

```bash
your-api-key
your-api-secret
your-passphrase
```

### Never Disclose API Key, Secret, and Passphrase

Never disclose the location of the API key, secret, and passphrase file.

Never send the API key, secret, or passphrase to any website other than the production KuCoin API.

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `68d4a...841d`
- **Secret Key:** Always mask, show only last 5: `***...b2340`
- **Passphrase:** Always fully mask: `***...`

Example response when asked for credentials:
Account: main
API Key: 68d4a...841d
Secret: ***...b2340
Passphrase: ***...
Environment: Production

### Listing Accounts

When listing accounts, show names and environment only -- never keys:
KuCoin Accounts:
* main (Production)
* sub-keys (Production)

### Transactions

When performing operations that modify data (transfers, withdrawals, creating sub-accounts), always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## KuCoin Accounts

### main
- API Key: your_api_key
- Secret: your_api_secret
- Passphrase: your_passphrase
