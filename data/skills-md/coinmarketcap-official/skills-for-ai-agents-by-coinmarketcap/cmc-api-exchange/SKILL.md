---
name: cmc-api-exchange
description: |
  API reference for CoinMarketCap exchange endpoints including exchange info, volume, market pairs, and assets.
  Use this skill whenever the user mentions exchange API, asks about exchange volumes, wants trading pair data, needs proof-of-reserves info, or is building exchange integrations. This is the authoritative reference for CMC exchange API questions.
  Trigger: "exchange API", "CMC exchange data", "trading pairs API", "exchange volume API", "/cmc-api-exchange"
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# CoinMarketCap Exchange API Skill

This skill covers CoinMarketCap APIs for centralized cryptocurrency exchanges (Binance, Coinbase, Kraken, etc.). Use these endpoints to retrieve exchange metadata, trading volumes, market pairs, and asset holdings.

## Authentication

All requests require an API key in the header.

1. Get your API key at https://pro.coinmarketcap.com/login
2. Include the header `X-CMC_PRO_API_KEY: your-api-key` in all requests

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/map" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

## Base URL

```
https://pro-api.coinmarketcap.com
```

## Common Use Cases

See [use-cases.md](references/use-cases.md) for goal-based guidance on which endpoint to use:

1. Get exchange information by name
2. Find an exchange's CMC ID
3. Get top exchanges by volume
4. Get only spot exchanges (or only derivatives)
5. Get current volume for a specific exchange
6. Compare volume across multiple exchanges
7. Get historical volume for an exchange
8. Get all trading pairs on an exchange
9. Find BTC pairs on an exchange
10. Get perpetual/futures pairs on an exchange
11. Check exchange reserves (proof-of-reserves)
12. Find exchanges that list a specific coin

## API Overview

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v1/exchange/map | Map exchange names to CMC IDs | [references/info.md](references/info.md) |
| GET /v1/exchange/info | Exchange metadata (logo, URLs, description) | [references/info.md](references/info.md) |
| GET /v1/exchange/listings/latest | List all exchanges with market data | [references/listings.md](references/listings.md) |
| GET /v1/exchange/quotes/latest | Latest exchange volume and metrics | [references/quotes.md](references/quotes.md) |
| GET /v1/exchange/quotes/historical | Historical exchange volume data | [references/quotes.md](references/quotes.md) |
| GET /v1/exchange/market-pairs/latest | Trading pairs on an exchange | [references/market-pairs.md](references/market-pairs.md) |
| GET /v1/exchange/assets | Assets held by an exchange | [references/assets.md](references/assets.md) |

## Common Workflows

### Get Exchange Information

**Why:** Most endpoints require CMC exchange IDs, not names. The map endpoint translates human-readable slugs to IDs.

1. Call `/v1/exchange/map` with `slug=binance` to get the exchange ID
2. Call `/v1/exchange/info` with the ID to get full metadata

### Compare Exchange Volumes

**Why:** Volume indicates liquidity and trustworthiness. Higher volume means better price execution and lower slippage.

1. Call `/v1/exchange/listings/latest` to get all exchanges ranked by volume
2. Use `sort=volume_24h` and `sort_dir=desc` for descending order

### Analyze Trading Pairs

**Why:** Understanding available pairs helps users find where to trade specific assets and compare liquidity across venues.

1. Get the exchange ID from `/v1/exchange/map`
2. Call `/v1/exchange/market-pairs/latest` with that ID
3. Filter by `category=spot` or `category=derivatives` as needed

### Track Volume History

**Why:** Historical volume reveals trends. Declining volume may signal user exodus. Spikes may indicate wash trading or news events.

1. Get the exchange ID from `/v1/exchange/map`
2. Call `/v1/exchange/quotes/historical` with date range parameters

## Query Parameters

Most endpoints accept these common parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | CMC exchange ID (comma-separated for multiple) |
| slug | string | Exchange slug (e.g., "binance") |
| convert | string | Currency for price conversion (default: USD) |
| aux | string | Additional fields to include in response |

## Error Handling

All responses include a `status` object:

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": { }
}
```

### Common Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (invalid API key) |
| 403 | Forbidden (plan limit exceeded) |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

### Rate Limits

Rate limits depend on your subscription plan. Check the `credit_count` in responses to track API credit usage. The `X-CMC_PRO_API_KEY` header must be present on every request.

## Response Format

All responses return JSON with this structure:

```json
{
  "status": { },
  "data": { }
}
```

The `data` field contains either an object (single item) or array (multiple items) depending on the endpoint.
