---
name: earn
description: KuCoin Earn products using the KuCoin API. Query Simple Earn and Structured Earn products. Authentication requires API Key, API Secret, and Passphrase.
metadata:
  version: 1.0.0
  author: KuCoin
license: MIT
---

# KuCoin Earn Skill

Query KuCoin Earn products using authenticated API endpoints. Covers Simple Earn (savings, staking, promotions) and Structured Earn (dual investment) queries. Requires API Key, Secret Key, and Passphrase for authenticated endpoints. Return the result in JSON format.

> **Note:** This skill only supports Classic REST API GET endpoints (read-only operations).

## Quick Reference

### Simple Earn

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v1/earn/redeem-preview` (GET) | Get Redeem Preview | orderId | None | Yes |
| `/api/v1/earn/saving/products` (GET) | Get Savings Products | None | currency, currentPage, pageSize | Yes |
| `/api/v1/earn/promotion/products` (GET) | Get Promotion Products | None | currency, currentPage, pageSize | Yes |
| `/api/v1/earn/staking/products` (GET) | Get Staking Products | None | currency, currentPage, pageSize | Yes |
| `/api/v1/earn/kcs-staking/products` (GET) | Get KCS Staking Products | None | currency, currentPage, pageSize | Yes |
| `/api/v1/earn/eth-staking/products` (GET) | Get ETH Staking Products | None | currency, currentPage, pageSize | Yes |
| `/api/v1/earn/hold-assets` (GET) | Get Account Holding | None | currency, productId, productCategory, currentPage, pageSize | Yes |

### Structured Earn

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v1/struct-earn/orders` (GET) | Get Structured Product Orders. **Note: This endpoint may not be available (returns 400100).** | None | currency, status, currentPage, pageSize | Yes |
| `/api/v1/struct-earn/dual/products` (GET) | Get Dual Investment Products. **Note: This endpoint may not be available (returns 400100).** | None | currency, currentPage, pageSize | Yes |

---

## Parameters

### Common Parameters

* **orderId**: Holding ID, used for redeem preview
* **currency**: Currency code filter (e.g., `USDT`, `BTC`, `KCS`, `ETH`)
* **productId**: Earn product ID (e.g., `2611`)
* **productCategory**: Product category filter for account holdings
* **currentPage**: Current page number for paginated results (default: 1)
* **pageSize**: Number of results per page. Minimum is 10, maximum is 500 (default: 15)
* **status**: Order status filter for structured product queries

### Enums

* **productCategory**: `DEMAND` | `STAKING` | `KCS_STAKING` | `ETH_STAKING` | `PROMOTION`
* **status** (structured orders): `PENDING` | `ONGOING` | `UNSOLD` | `SETTLING` | `FINISHED`
* **productStatus**: `ONGOING` | `PENDING` | `FULL` | `INTERESTING`
* **holdingStatus**: `LOCKED` | `REDEEMING`
* **productType**: `TIME` | `DEMAND`

## Authentication

For endpoints that require authentication, you will need to provide KuCoin API credentials.
Required credentials:

* **API Key** (`KC-API-KEY`): Your KuCoin API key (for header)
* **Secret Key**: Your KuCoin API secret (for HMAC-SHA256 signing)
* **Passphrase** (`KC-API-PASSPHRASE`): Your KuCoin API passphrase (encrypted with HMAC-SHA256)

Base URL:
* Production: https://api.kucoin.com

## Security

### Share Credentials

Users can provide KuCoin API credentials by sending a file where the content is in the following format:

```bash
abc123...apikey
secret123...key
mypassphrase
```

### Never Disclose API Key, Secret, and Passphrase

Never disclose the location of the API key, secret, and passphrase file.

Never send the API key, secret, and passphrase to any website other than the production API endpoint.

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `abc12...6789`
- **Secret Key:** Always mask, show only last 5: `***...x9y8z`
- **Passphrase:** Never display

Example response when asked for credentials:
Account: main
API Key: abc12...6789
Secret: ***...x9y8z
Passphrase: ********
Environment: Production

### Listing Accounts

When listing accounts, show names and environment only -- never keys:
KuCoin Accounts:
* main (Production)
* earn-bot (Production)

### Transactions in Mainnet

When performing transactions in mainnet (purchase, redeem), always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## KuCoin Accounts

### main
- API Key: your_api_key
- Secret Key: your_secret_key
- Passphrase: your_passphrase
