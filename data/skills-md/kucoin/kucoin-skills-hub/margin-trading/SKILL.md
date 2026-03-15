---
name: margin-trading
description: KuCoin Margin trading using the KuCoin API. Cross margin and isolated margin market data, order queries, borrowing/repaying queries, lending queries, and risk limits. Authentication requires API Key, API Secret, and Passphrase.
metadata:
  version: 1.0.0
  author: KuCoin
license: MIT
---

# KuCoin Margin Trading Skill

Margin trading on KuCoin using authenticated API endpoints. Supports cross margin and isolated margin market data, HF order queries, stop order queries, OCO order queries, borrow/repay history queries, lending queries, and risk limits. Requires API Key, API Secret, and Passphrase for authenticated endpoints. Return the result in JSON format.

> **Note:** This skill only supports Classic REST API GET endpoints (read-only operations).

## Quick Reference

### Classic Margin Market Data

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v3/margin/symbols` (GET) | Get Symbols - Cross Margin (trading pair config) | None | symbol | No |
| `/api/v1/isolated/symbols` (GET) | Get Symbols - Isolated Margin (trading pair config) | None | None | No |
| `/api/v3/etf/info` (GET) | Get ETF Info (leveraged token info) | None | currency | No |
| `/api/v1/margin/config` (GET) | Get Margin Config (cross margin config, currency list) | None | None | No |
| `/api/v3/mark-price/all-symbols` (GET) | Get Mark Price List (current mark price for all margin pairs) | None | None | No |
| `/api/v3/margin/collateralRatio` (GET) | Get Margin Collateral Ratio | None | currencyList | No |
| `/api/v3/margin/available-inventory` (GET) | Get Market Available Inventory (platform borrowable amount) | None | currency | No |

### Classic Margin HF Order Queries

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v3/hf/margin/orders/{orderId}` (GET) | Get Order By OrderId | orderId (path), symbol (query) | None | Yes |
| `/api/v3/hf/margin/orders/client-order/{clientOid}` (GET) | Get Order By ClientOid | clientOid (path), symbol (query) | None | Yes |
| `/api/v3/hf/margin/order/active/symbols` (GET) | Get Symbols With Open Order | tradeType | None | Yes |
| `/api/v3/hf/margin/orders/active` (GET) | Get Open Orders | symbol, tradeType | None | Yes |
| `/api/v3/hf/margin/orders/done` (GET) | Get Closed Orders | symbol, tradeType | side, type, lastId, limit, startAt, endAt | Yes |
| `/api/v3/hf/margin/fills` (GET) | Get Trade History | symbol, tradeType | orderId, side, type, lastId, limit, startAt, endAt | Yes |

### Classic Margin Stop Order Queries

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v3/hf/margin/stop-orders` (GET) | Get Stop Orders List (paginated, untriggered) | None | symbol, side, type, tradeType, startAt, endAt, currentPage, orderIds, pageSize, stop | Yes |
| `/api/v3/hf/margin/stop-order/orderId` (GET) | Get Stop Order By OrderId | orderId | None | Yes |
| `/api/v3/hf/margin/stop-order/clientOid` (GET) | Get Stop Order By ClientOid | clientOid | None | Yes |

### Classic Margin OCO Order Queries

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v3/hf/margin/oco-order/orderId` (GET) | Get OCO Order By OrderId | orderId | None | Yes |
| `/api/v3/hf/margin/oco-order/clientOid` (GET) | Get OCO Order By ClientOid | clientOid | None | Yes |
| `/api/v3/hf/margin/oco-order/detail/orderId` (GET) | Get OCO Order Detail By OrderId (includes sub-orders) | orderId | None | Yes |
| `/api/v3/hf/margin/oco-orders` (GET) | Get OCO Order List (paginated) | pageSize, currentPage | symbol, startAt, endAt, orderIds, tradeType | Yes |

### Classic Debit Queries (Borrowing and Repaying)

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v3/margin/borrowRate` (GET) | Get Borrow Interest Rate | None | vipLevel, currency | Yes |
| `/api/v3/margin/borrow` (GET) | Get Borrow History | currency | isIsolated, symbol, orderNo, startTime, endTime, currentPage, pageSize | Yes |
| `/api/v3/margin/repay` (GET) | Get Repay History | currency | isIsolated, symbol, orderNo, startTime, endTime, currentPage, pageSize | Yes |
| `/api/v3/margin/interest` (GET) | Get Interest History | None | currency, isIsolated, symbol, startTime, endTime, currentPage, pageSize | Yes |

### Classic Credit Queries (Lending)

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v3/project/list` (GET) | Get Loan Market (currencies available for lending) | None | currency | Yes |
| `/api/v3/project/marketInterestRate` (GET) | Get Loan Market Interest Rate (past 7 days) | currency | None | Yes |
| `/api/v3/purchase/orders` (GET) | Get Purchase Orders (paginated) | status | currency, purchaseOrderNo, currentPage, pageSize | Yes |
| `/api/v3/redeem/orders` (GET) | Get Redeem Orders (paginated) | status | currency, redeemOrderNo, currentPage, pageSize | Yes |

### Classic Risk Limit

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v3/margin/currencies` (GET) | Get Margin Risk Limit (config and risk limit info per currency/symbol) | None | isIsolated, currency, symbol | Yes |

---

## Parameters

### Common Parameters

* **clientOid**: Client Order ID. Unique identifier created by the user (UUID recommended). Max length: 40 characters.
* **symbol**: Trading pair symbol (e.g., `BTC-USDT`)
* **side**: Order side filter: `buy` | `sell`
* **type**: Order type filter: `limit` | `market`
* **orderId**: Order ID for query
* **isIsolated**: `true` for isolated margin, `false` for cross margin. Default is `false`.
* **tradeType**: Transaction type: `MARGIN_TRADE` (cross margin), `MARGIN_ISOLATED_TRADE` (isolated margin)
* **stop**: Stop order trigger condition filter: `loss` | `entry`
* **lastId**: The ID of the last data set from the previous batch. Used for cursor-based pagination.
* **limit**: Number of results per page. Default: 20, Max: 100 (for order/fill queries).
* **currentPage**: Current page number for paginated queries. Default: 1.
* **pageSize**: Page size for paginated queries. Varies by endpoint (typical default: 50, max: 500).
* **startAt / startTime**: Start time filter in milliseconds.
* **endAt / endTime**: End time filter in milliseconds.
* **currency**: Currency code (e.g., `BTC`, `USDT`).
* **vipLevel**: VIP level. If empty, defaults to current user VIP level.
* **orderNo**: Order number for borrow/repay history queries.
* **purchaseOrderNo**: Purchase order ID for lending operations.
* **redeemOrderNo**: Redeem order ID for redemption queries.
* **status**: Order status filter. Values depend on endpoint (e.g., `DONE`, `PENDING`).
* **currencyList**: Comma-separated currency list for collateral ratio query.

### Enums

* **side**: `buy` | `sell`
* **type**: `limit` | `market`
* **tradeType**: `MARGIN_TRADE` (cross margin) | `MARGIN_ISOLATED_TRADE` (isolated margin)
* **stop**: `loss` | `entry`
* **purchase/redeem status**: `DONE` | `PENDING`
* **OCO order status**: `NEW` | `DONE` | `TRIGGERED` | `CANCELLED`
* **stop order status**: `NEW` | `TRIGGERED`
* **liquidity**: `taker` | `maker`

## Authentication

For endpoints that require authentication, you will need to provide KuCoin API credentials.
Required credentials:

* **API Key**: Your KuCoin API key (for header `KC-API-KEY`)
* **API Secret**: Your KuCoin API secret (for signing)
* **Passphrase**: Your KuCoin API passphrase (for header `KC-API-PASSPHRASE`)

Base URL:
* Production: `https://api.kucoin.com`

## Security

### Share Credentials

Users can provide KuCoin API credentials by sending a file where the content is in the following format:

```bash
api_key_value
api_secret_value
api_passphrase_value
```

### Never Disclose API Key and Secret

Never disclose the location of the API key, secret, or passphrase file.

Never send the API key, secret, or passphrase to any website other than the official KuCoin API endpoint.

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `abcde...wxyz`
- **API Secret:** Always mask, show only last 5: `***...s3cr3`
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
* margin-keys (Production)

### Transactions in Production

When performing transactions in production, always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## KuCoin Accounts

### main
- API Key: your_api_key
- Secret: your_api_secret
- Passphrase: your_passphrase
