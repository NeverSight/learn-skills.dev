---
name: cmc-api-crypto
description: |
  API reference for CoinMarketCap cryptocurrency endpoints including quotes, listings, OHLCV, trending, and categories.
  Use this skill whenever the user mentions CMC API, asks how to get crypto data programmatically, wants to build price integrations, or needs REST endpoint documentation. This is the go-to reference for any CMC cryptocurrency API question.
  Trigger: "CMC API", "coinmarketcap api", "crypto price API", "get bitcoin price via API", "/cmc-api-crypto"
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# CoinMarketCap Cryptocurrency API

This skill covers the CoinMarketCap Cryptocurrency API endpoints for retrieving price data, market listings, historical quotes, trending coins, and token metadata.

## Authentication

All requests require an API key in the header.

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

Get your API key at: https://pro.coinmarketcap.com/login

## Base URL

```
https://pro-api.coinmarketcap.com
```

## Common Use Cases

See [use-cases.md](references/use-cases.md) for goal-based guidance on which endpoint to use:

1. Get current price of a token
2. Find a token's CMC ID from symbol or name
3. Get a token by contract address
4. Get top 100 coins by market cap
5. Find coins in a price range
6. Get historical price at a specific date
7. Build a price chart (OHLCV data)
8. Find where a coin trades
9. Get all-time high and distance from ATH
10. Find today's biggest gainers
11. Discover newly listed coins
12. Get all tokens in a category (e.g., DeFi)

## API Overview

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v1/cryptocurrency/categories | List all categories with market metrics | [categories.md](references/categories.md) |
| GET /v1/cryptocurrency/category | Single category details | [categories.md](references/categories.md) |
| GET /v1/cryptocurrency/listings/historical | Historical listings snapshot | [listings.md](references/listings.md) |
| GET /v1/cryptocurrency/listings/latest | Current listings with market data | [listings.md](references/listings.md) |
| GET /v1/cryptocurrency/listings/new | Newly added cryptocurrencies | [listings.md](references/listings.md) |
| GET /v1/cryptocurrency/map | Map names/symbols to CMC IDs | [map.md](references/map.md) |
| GET /v1/cryptocurrency/trending/gainers-losers | Top gainers and losers | [trending.md](references/trending.md) |
| GET /v1/cryptocurrency/trending/latest | Currently trending coins | [trending.md](references/trending.md) |
| GET /v1/cryptocurrency/trending/most-visited | Most visited on CMC | [trending.md](references/trending.md) |
| GET /v2/cryptocurrency/info | Static metadata (logo, description, URLs) | [info.md](references/info.md) |
| GET /v2/cryptocurrency/market-pairs/latest | Trading pairs for a coin | [market-pairs.md](references/market-pairs.md) |
| GET /v2/cryptocurrency/ohlcv/historical | Historical OHLCV candles | [ohlcv.md](references/ohlcv.md) |
| GET /v2/cryptocurrency/ohlcv/latest | Latest OHLCV data | [ohlcv.md](references/ohlcv.md) |
| GET /v2/cryptocurrency/price-performance-stats/latest | Price performance stats | [price-performance.md](references/price-performance.md) |
| GET /v2/cryptocurrency/quotes/latest | Latest price quotes | [quotes.md](references/quotes.md) |
| GET /v3/cryptocurrency/quotes/historical | Historical price quotes | [quotes.md](references/quotes.md) |

## Common Workflows

### Get Token Price by Symbol

1. First, map the symbol to a CMC ID using `/v1/cryptocurrency/map`
2. Then fetch the price using `/v2/cryptocurrency/quotes/latest`

```bash
# Step 1: Get CMC ID for ETH
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?symbol=ETH" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Step 2: Get price quote (using id=1027 for ETH)
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?id=1027" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Get Top 100 Coins by Market Cap

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=100&sort=market_cap" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Get Historical Price Data

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/cryptocurrency/quotes/historical?id=1&time_start=2024-01-01&time_end=2024-01-31&interval=daily" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Get Token Metadata

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?id=1,1027" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

## Error Handling

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (invalid API key) |
| 403 | Forbidden (endpoint not available on your plan) |
| 429 | Rate limit exceeded |
| 500 | Server error |

### Rate Limits

Rate limits depend on your subscription plan. The response headers include:

1. `X-CMC_PRO_API_KEY_CREDITS_USED` - Credits used this call
2. `X-CMC_PRO_API_KEY_CREDITS_LEFT` - Credits remaining

### Common Errors

**Invalid ID**: Ensure you use valid CMC IDs from the `/map` endpoint. Symbol lookups may return multiple matches.

**Missing Required Parameter**: Some endpoints require at least one identifier (id, slug, or symbol).

**Plan Restrictions**: Historical endpoints and some features require paid plans. Check your plan limits.

### Error Response Format

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 400,
    "error_message": "Invalid value for 'id'",
    "credit_count": 0
  }
}
```

## Response Format

All responses follow this structure:

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": { ... }
}
```

## Reference Files

See the `references/` directory for complete parameter and response documentation for each endpoint.
