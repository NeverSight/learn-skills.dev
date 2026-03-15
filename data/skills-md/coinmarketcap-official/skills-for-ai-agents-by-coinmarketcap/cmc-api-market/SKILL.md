---
name: cmc-api-market
description: |
  API reference for CoinMarketCap market-wide endpoints including global metrics, fear/greed, indices, trending topics, and charts.
  Use this skill whenever the user mentions market API, asks about fear/greed index, wants global metrics or BTC dominance data, needs k-line charts, or is working with market sentiment. This is the complete reference for CMC market-wide API questions.
  Trigger: "market API", "fear greed API", "global metrics API", "CMC charts API", "/cmc-api-market"
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# CoinMarketCap Market API Skill

This skill covers market-wide cryptocurrency data including global metrics, sentiment indicators, market indices, community activity, news content, charting data, and utility endpoints.

## Authentication

All requests require the `X-CMC_PRO_API_KEY` header.

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

Get your API key at: https://pro.coinmarketcap.com/login

## Base URL

```
https://pro-api.coinmarketcap.com
```

## Common Use Cases

See [use-cases.md](references/use-cases.md) for goal-based guidance on which endpoint to use:

1. Get current market sentiment (Fear & Greed)
2. Get total crypto market cap
3. Get BTC dominance
4. Track market cap history
5. Track Fear & Greed history
6. Get CMC100 index performance
7. Compare CMC100 vs CMC20
8. Get OHLCV candlestick data for charts
9. Get simple price time series
10. Get community trending tokens
11. Get trending discussion topics
12. Get latest crypto news
13. Convert currency amounts
14. Check API usage and limits
15. Get fiat currency IDs

## API Overview

### Global Metrics

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v1/global-metrics/quotes/historical | Historical global market metrics | [global-metrics.md](references/global-metrics.md) |
| GET /v1/global-metrics/quotes/latest | Latest total market cap, BTC dominance | [global-metrics.md](references/global-metrics.md) |

### Fear and Greed Index

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v3/fear-and-greed/historical | Historical fear/greed values | [fear-greed.md](references/fear-greed.md) |
| GET /v3/fear-and-greed/latest | Current market sentiment score | [fear-greed.md](references/fear-greed.md) |

### Market Indices

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v3/index/cmc100-historical | CMC100 index history | [indices.md](references/indices.md) |
| GET /v3/index/cmc100-latest | CMC100 current value | [indices.md](references/indices.md) |
| GET /v3/index/cmc20-historical | CMC20 index history | [indices.md](references/indices.md) |
| GET /v3/index/cmc20-latest | CMC20 current value | [indices.md](references/indices.md) |

### Community

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v1/community/trending/token | Trending tokens by community activity | [community.md](references/community.md) |
| GET /v1/community/trending/topic | Trending discussion topics | [community.md](references/community.md) |

### Content

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v1/content/latest | Latest news and Alexandria articles | [content.md](references/content.md) |
| GET /v1/content/posts/comments | Comments on a specific post | [content.md](references/content.md) |
| GET /v1/content/posts/latest | Latest community posts | [content.md](references/content.md) |
| GET /v1/content/posts/top | Top ranked community posts | [content.md](references/content.md) |

### K-Line Charts

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v1/k-line/candles | OHLCV candlestick data | [kline.md](references/kline.md) |
| GET /v1/k-line/points | Time series price/market cap points | [kline.md](references/kline.md) |

### Tools

| Endpoint | Description | Reference |
|----------|-------------|-----------|
| GET /v1/fiat/map | Map fiat currencies to CMC IDs | [tools.md](references/tools.md) |
| GET /v1/key/info | API key usage and plan details | [tools.md](references/tools.md) |
| GET /v2/tools/price-conversion | Convert between currencies | [tools.md](references/tools.md) |

## Common Workflows

### Get Market Sentiment Overview

1. Fetch fear/greed index: `/v3/fear-and-greed/latest`
2. Get global metrics: `/v1/global-metrics/quotes/latest`
3. Combine for sentiment analysis with market cap context

### Track Market Index Performance

1. Get current CMC100 value: `/v3/index/cmc100-latest`
2. Fetch historical data: `/v3/index/cmc100-historical`
3. Compare performance over time

### Monitor Community Activity

1. Check trending tokens: `/v1/community/trending/token`
2. Review trending topics: `/v1/community/trending/topic`
3. Read latest posts: `/v1/content/posts/top`

### Build Price Charts

1. Fetch OHLCV candles: `/v1/k-line/candles`
2. Use interval parameter for timeframe (1h, 4h, 1d)
3. Plot candlestick chart with returned data

### Currency Conversion

1. Get fiat currency IDs: `/v1/fiat/map`
2. Convert amounts: `/v2/tools/price-conversion`

## Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 400 | Bad Request | Check parameter values and format |
| 401 | Unauthorized | Verify API key is valid |
| 403 | Forbidden | Endpoint not available on your plan |
| 429 | Rate Limited | Wait and retry with backoff |
| 500 | Server Error | Retry after delay |

### Error Response Format

```json
{
  "status": {
    "error_code": 400,
    "error_message": "Invalid value for 'id'"
  }
}
```

### Rate Limit Headers

Check these response headers to monitor usage:

1. `X-CMC_PRO_API_KEY_CREDITS_USED` - Credits consumed
2. `X-CMC_PRO_API_KEY_CREDITS_REMAINING` - Credits left
3. `X-CMC_PRO_API_KEY_RATE_LIMIT` - Requests per minute limit

## Response Format

All endpoints return JSON with this structure:

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": { }
}
```

## Tips

1. Use the `/v1/key/info` endpoint to check your plan limits before heavy usage
2. Cache global metrics data as it updates every few minutes
3. Fear/greed index updates daily, no need for frequent polling
4. K-line data supports multiple intervals for different chart timeframes
5. Community trending data refreshes periodically throughout the day
