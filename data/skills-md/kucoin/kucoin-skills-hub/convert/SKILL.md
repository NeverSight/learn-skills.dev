---
name: convert
description: KuCoin Convert using the KuCoin API. Get conversion quotes, query convert order details and history. Authentication requires API Key, API Secret, and Passphrase.
metadata:
  version: 1.0.0
  author: KuCoin
license: MIT
---

# KuCoin Convert Skill

Query convert currencies, quotes, and order details on KuCoin. Return results in JSON format.

> **Note:** This skill only supports Classic REST API GET endpoints (read-only operations).

## Quick Reference

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v1/convert/symbol` (GET) | Get Convert Symbol | fromCurrency, toCurrency | orderType | No |
| `/api/v1/convert/currencies` (GET) | Get Convert Currencies | None | None | No |
| `/api/v1/convert/quote` (GET) | Get Convert Quote | fromCurrency, toCurrency | fromCurrencySize, toCurrencySize | Yes |
| `/api/v1/convert/order/detail` (GET) | Get Convert Order Detail | orderId or clientOrderId (at least one) | None | Yes |
| `/api/v1/convert/order/history` (GET) | Get Convert Order History | None | status, startAt, endAt, page, pageSize | Yes |
| `/api/v1/convert/limit/quote` (GET) | Get Convert Limit Quote | fromCurrency, toCurrency | fromCurrencySize, toCurrencySize | Yes |
| `/api/v1/convert/limit/order/detail` (GET) | Get Convert Limit Order Detail | None | orderId, clientOrderId | Yes |
| `/api/v1/convert/limit/orders` (GET) | Get Convert Limit Orders | None | status, startAt, endAt, page, pageSize | Yes |

---

## Parameters

### Common Parameters

* **fromCurrency**: The source currency for the trading pair (e.g., BTC)
* **toCurrency**: The target currency for the trading pair (e.g., USDT)
* **fromCurrencySize**: The amount of the source currency to convert. Either fromCurrencySize or toCurrencySize must be provided, but not both simultaneously.
* **toCurrencySize**: The amount of the target currency to convert. Either fromCurrencySize or toCurrencySize must be provided, but not both simultaneously.
* **orderType**: Order type filter when querying convert symbols (e.g., MARKET)
* **orderId**: Convert order ID. Either orderId or clientOrderId must be provided for detail endpoints.
* **clientOrderId**: A unique order identifier defined by the user. Maximum 40 characters.
* **status**: Order status filter for history queries.
* **startAt**: Order start time filter, in Unix milliseconds.
* **endAt**: Order end time filter, in Unix milliseconds.
* **page**: Current page number for paginated results.
* **pageSize**: The number of results per page (20-100).

### Enums

* **orderType**: MARKET | LIMIT
* **status** (market orders): OPEN | SUCCESS | FAIL
* **status** (limit orders): OPEN | SUCCESS | FAIL | CANCELLED

## Authentication

For endpoints that require authentication, you will need to provide KuCoin API credentials.
Required credentials:

* **API Key** (`KC-API-KEY`): Your KuCoin API key (sent as header)
* **API Secret**: Your KuCoin API secret (used for HMAC-SHA256 signing)
* **Passphrase** (`KC-API-PASSPHRASE`): Your KuCoin API passphrase (sent as header, encrypted with HMAC-SHA256 using the API Secret)

Base URL:
* Production: https://api.kucoin.com

## Security

### Share Credentials

Users can provide KuCoin API credentials by sending a file where the content is in the following format:

```bash
abc123...apikey
secret123...key
passphrase123
```

### Never Disclose API Key, Secret, and Passphrase

Never disclose the location of the API key, secret, and passphrase file.

Never send the API key, secret, and passphrase to any website other than the KuCoin production API.

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `su1Qc...8akf`
- **Secret Key:** Always mask, show only last 5: `***...aws1`
- **Passphrase:** Always mask entirely: `***...`

Example response when asked for credentials:
Account: main
API Key: su1Qc...8akf
Secret: ***...aws1
Passphrase: ***...
Environment: Production

### Listing Accounts

When listing accounts, show names and environment only -- never keys:
KuCoin Accounts:
* main (Production)
* trading-bot (Production)

### Transactions

When performing convert transactions, always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## KuCoin Accounts

### main
- API Key: your_api_key
- Secret: your_api_secret
