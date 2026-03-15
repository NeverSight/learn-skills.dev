---
name: broker
description: KuCoin Broker and Affiliate using the KuCoin API. Affiliate invite management, commission queries, Broker Pro user management, and ND (Exchange) Broker queries. Authentication requires API Key, API Secret, and Passphrase.
metadata:
  version: 1.0.0
  author: KuCoin
license: MIT
---

# KuCoin Broker Skill

Broker and Affiliate operations on KuCoin using authenticated API endpoints. Covers Affiliate invite/commission management, Broker Pro rebate and user queries, and ND Exchange Broker queries (KYC status, sub-account info, deposits, withdrawals, and rebates). Requires API Key, API Secret, and Passphrase for all endpoints. Return the result in JSON format.

> **Note:** This skill only supports Classic REST API GET endpoints (read-only operations).

## Quick Reference

### Affiliate

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v2/affiliate/queryInvitees` (GET) | Get Invited (list of invited users with trade stats) | None | userType, referralCode, uid, registrationStartAt, registrationEndAt, page, pageSize | Yes |
| `/api/v2/affiliate/queryMyCommission` (GET) | Get Commission (affiliate commission records) | None | siteType, rebateType, rebateStartAt, rebateEndAt, page, pageSize, userId, dataType | Yes |
| `/api/v2/affiliate/queryTransactionByUid` (GET) | Get Trade History (trade records for a specific invitee) | uid | tradeType, tradeStartAt, tradeEndAt, page, pageSize | Yes |
| `/api/v2/affiliate/queryTransactionByTime` (GET) | Get Transaction (trade records by time range) | tradeStartAt, tradeEndAt | uid, tradeType, lastId, direction, pageSize | Yes |
| `/api/v2/affiliate/queryKumining` (GET) | Get Kumining (KuMining commission records) | None | uid, startAt, endAt, lastId, direction, pageSize | Yes |

### Broker Pro

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v2/broker/api/rebate/download` (GET) | Get Broker Rebate (download rebate order file) | begin, end, tradeType | None | Yes |
| `/api/v2/broker/queryMyCommission` (GET) | Get Commission (broker commission records) | None | siteType, tradeType, rebateType, startAt, endAt, page, pageSize | Yes |
| `/api/v2/broker/queryUser` (GET) | Get User List (broker sub-users) | None | tradeType, uid, rcode, tag, startAt, endAt, page, pageSize | Yes |
| `/api/v2/broker/queryDetailByUid` (GET) | Get User Transactions (trade records per user UID) | None | tradeType, uid, startAt, endAt, lastId, direction, pageSize | Yes |

### ND Exchange Broker

> **⚠️ Note:** The ND Exchange Broker endpoints below (`/api/v1/broker/nd/*` and `/api/kyc/ndBroker/*`) may have been deprecated or migrated. These endpoints currently return 404 Not Found. They require ND Broker-level API permissions. Please consult the latest KuCoin API documentation for updated paths.

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/kyc/ndBroker/proxyClient/status/list` (GET) | Get KYC Status (by UID list) | clientUids | None | Yes |
| `/api/kyc/ndBroker/proxyClient/status/page` (GET) | Get KYC Status List (paginated) | None | pageNumber, pageSize | Yes |
| `/api/v1/broker/nd/info` (GET) | Get Broker Info (rebate download by date range) | begin, end, tradeType | None | Yes |
| `/api/v1/broker/nd/account` (GET) | Get Sub-Account (list sub-accounts) | None | uid, currentPage, pageSize | Yes |
| `/api/v1/broker/nd/account/apikey` (GET) | Get Sub-Account API Key | uid | apiKey | Yes |
| `/api/v3/broker/nd/transfer/detail` (GET) | Get Transfer History | orderId | None | Yes |
| `/api/v1/asset/ndbroker/deposit/list` (GET) | Get Deposit List (sub-account deposits) | None | currency, status, hash, startTimestamp, endTimestamp, limit | Yes |
| `/api/v3/broker/nd/deposit/detail` (GET) | Get Deposit Detail | currency, hash | None | Yes |
| `/api/v3/broker/nd/withdraw/detail` (GET) | Get Withdraw Detail | withdrawalId | None | Yes |
| `/api/v1/broker/nd/rebate/download` (GET) | Get Broker Rebate (ND broker rebate download) | begin, end, tradeType | None | Yes |

---

## Parameters

### Affiliate Parameters

* **userType**: Invited user type: `1` (Regular), `2` (KYC-verified), `3` (First-trade)
* **referralCode**: The referral code (rcode) through which the user registered
* **uid**: Invitee UID (for trade history query) or comma-separated UIDs
* **registrationStartAt / registrationEndAt**: Registration time range (13-digit timestamp)
* **siteType**: Commission source site. Default: `all`
* **rebateType**: Rebate type: `0` (all), `1` (spot), `2` (futures)
* **rebateStartAt / rebateEndAt**: Commission issuance time range (13-digit timestamp); max one-year span
* **tradeStartAt / tradeEndAt**: Trade time range (13-digit timestamp)
* **tradeType**: Trading type: `SPOT` | `FEATURE`
* **dataType**: Data type: `trade` | `kumining`
* **startAt / endAt**: Time range filter (13-digit timestamp)
* **lastId**: Cursor-based pagination: empty string for first query, then use `lastId` from last record
* **direction**: Page direction: `PRE` | `NEXT`
* **page / pageSize**: Pagination controls

### Broker Pro Parameters

* **begin / end**: Date range in `YYYYMMDD` format (e.g., `20250101`); maximum 6-month interval
* **tradeType** (Broker Pro): Transaction type: `SPOT` | `FUTURE`
* **rcode**: Referral code used when user registered with broker
* **tag**: Broker tag used by the user during trading
* **rebateType**: `1` (spot rebate), `2` (futures rebate), `0` (all; for commission query)

### ND Broker Parameters

* **clientUids**: Comma-separated client UIDs for KYC status query
* **pageNumber / pageSize**: Pagination for KYC status list
* **tradeType** (ND Broker Rebate): Transaction type: `1` (spot), `2` (futures)
* **uid**: Sub-account UID for account and API key queries
* **currentPage**: Current page number (default: 1)
* **apiKey**: Sub-account API key (filter parameter)
* **orderId**: Transfer order ID for transfer history query
* **currency**: Currency code filter for deposit list
* **status** (Deposit List): `PROCESSING` | `SUCCESS` | `FAILURE`
* **hash**: Transaction hash for deposit list/detail query
* **startTimestamp / endTimestamp**: Time range in milliseconds for deposit list
* **limit**: Maximum number of returned deposit items (default and max: 1000)
* **withdrawalId**: Withdrawal ID for withdraw detail query

### Enums

* **userType**: `1` | `2` | `3`
* **tradeType** (Affiliate): `SPOT` | `FEATURE`
* **tradeType** (Broker Pro): `all` | `SPOT` | `FUTURE`
* **tradeType** (ND Broker Rebate): `1` (spot) | `2` (futures)
* **rebateType**: `0` | `1` | `2`
* **dataType**: `trade` | `kumining`
* **direction**: `PRE` | `NEXT`
* **status** (KYC): `NONE` | `PROCESS` | `PASS` | `REJECT`
* **status** (Deposit): `PROCESSING` | `SUCCESS` | `FAILURE`

---

## Authentication

For all endpoints, you must provide KuCoin API credentials with Broker-level permissions.

Required credentials:

* **API Key** (`KC-API-KEY`): Your KuCoin Broker API key
* **API Secret**: Your KuCoin API secret (used for signing)
* **Passphrase** (`KC-API-PASSPHRASE`): Your API passphrase (HMAC-SHA256 encrypted)

Base URL:
* Production: `https://api.kucoin.com`

---

## Security

### Share Credentials

Users can provide KuCoin API credentials by sending a file where the content is in the following format:

```bash
your-api-key
your-api-secret
your-passphrase
```

### Never Disclose API Key and Secret

Never disclose the location of the API key, secret, or passphrase file.

Never send the API key, secret, or passphrase to any website other than the official KuCoin API endpoint.

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `abcde...wxyz`
- **Secret Key:** Always mask, show only last 5: `***...s3cr3`
- **Passphrase:** Always mask entirely: `***...`

Example response when asked for credentials:
Account: main
API Key: abcde...wxyz
Secret: ***...s3cr3
Passphrase: ***...

### Listing Accounts

When listing accounts, show names and environment only -- never keys:
KuCoin Accounts:
* main (Production)
* broker-keys (Production)

### Transactions in Production

When performing operations that modify data (transfers, creating sub-accounts, updating API keys), always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## KuCoin Accounts

### main
- API Key: your_api_key
- Secret: your_api_secret
- Passphrase: your_passphrase
