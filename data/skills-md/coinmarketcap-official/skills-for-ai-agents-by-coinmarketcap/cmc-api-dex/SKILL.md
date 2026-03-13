---
name: cmc-api-dex
description: |
  API reference for CoinMarketCap DEX endpoints including token lookup, pools, transactions, trending, and security analysis.
  Use this skill whenever the user mentions DEX API, asks about on-chain token data, wants to look up tokens by contract address, needs security/rug risk checks, or is building DEX integrations. This is the definitive reference for CMC DEX API questions.
  Trigger: "DEX API", "token by contract address", "CMC security API", "liquidity pool API", "/cmc-api-dex"
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# CoinMarketCap DEX API

This skill covers CoinMarketCap's DEX (Decentralized Exchange) APIs for on-chain token data. Unlike CEX endpoints, these APIs fetch data directly from blockchain DEXs like Uniswap, PancakeSwap, and Raydium.

## Authentication

All requests require an API key in the header:

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/platform/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

Get your API key at: https://pro.coinmarketcap.com/login

## Base URL

```
https://pro-api.coinmarketcap.com
```

## POST vs GET Endpoints

Many DEX endpoints use POST for complex queries with body parameters. Always check the method:

1. GET endpoints pass parameters as query strings
2. POST endpoints pass parameters in JSON body with `Content-Type: application/json`

## Common Use Cases

See [use-cases.md](references/use-cases.md) for goal-based guidance on which endpoint to use:

1. Get DEX token price by contract address
2. Find a token's contract address by name
3. Get prices for multiple tokens at once
4. Check token security before trading
5. Find liquidity pools for a token
6. Find trending DEX tokens
7. Find today's biggest DEX gainers
8. Find newly launched tokens
9. Detect potential rug pulls (liquidity removal)
10. Get recent trades for a token
11. Get supported networks and DEXs
12. Get meme coins

## API Overview

| Endpoint | Method | Description | Reference |
|----------|--------|-------------|-----------|
| /v1/dex/token | GET | Token details by platform/address | [tokens.md](references/tokens.md) |
| /v1/dex/token/price | GET | Latest DEX price for a token | [tokens.md](references/tokens.md) |
| /v1/dex/token/price/batch | POST | Batch token prices | [tokens.md](references/tokens.md) |
| /v1/dex/token/pools | GET | Liquidity pools for a token | [tokens.md](references/tokens.md) |
| /v1/dex/token-liquidity/query | GET | Token liquidity over time | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/batch-query | POST | Batch token metadata | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/transactions | GET | Recent DEX transactions | [tokens.md](references/tokens.md) |
| /v1/dex/tokens/trending/list | POST | Trending DEX tokens | [tokens.md](references/tokens.md) |
| /v4/dex/pairs/quotes/latest | GET | Latest DEX pair quotes | [pairs.md](references/pairs.md) |
| /v4/dex/spot-pairs/latest | GET | DEX spot pairs listing | [pairs.md](references/pairs.md) |
| /v1/dex/platform/list | GET | List supported DEX platforms | [platforms.md](references/platforms.md) |
| /v1/dex/platform/detail | GET | Platform details | [platforms.md](references/platforms.md) |
| /v1/dex/search | GET | Search DEX tokens/pairs | [platforms.md](references/platforms.md) |
| /v1/dex/gainer-loser/list | POST | Top DEX gainers/losers | [discovery.md](references/discovery.md) |
| /v1/dex/liquidity-change/list | GET | Tokens with liquidity changes | [discovery.md](references/discovery.md) |
| /v1/dex/meme/list | POST | Meme tokens on DEX | [discovery.md](references/discovery.md) |
| /v1/dex/new/list | POST | Newly discovered DEX tokens | [discovery.md](references/discovery.md) |
| /v1/dex/security/detail | GET | Token security/risk signals | [security.md](references/security.md) |

## Common Workflows

### Get DEX Token Information

1. Search for token: `/v1/dex/search?keyword=PEPE`
2. Get token details: `/v1/dex/token?network_slug=ethereum&contract_address=0x...`
3. Check security risks: `/v1/dex/security/detail?network_slug=ethereum&contract_address=0x...`

### Analyze Token Liquidity

1. Get token pools: `/v1/dex/token/pools?network_slug=ethereum&contract_address=0x...`
2. Get liquidity history: `/v1/dex/token-liquidity/query?network_slug=ethereum&contract_address=0x...`

### Find Trending Tokens

1. Get trending tokens: POST `/v1/dex/tokens/trending/list` with filters
2. Get gainers/losers: POST `/v1/dex/gainer-loser/list`
3. Find new tokens: POST `/v1/dex/new/list`

### Monitor DEX Activity

1. Get recent transactions: `/v1/dex/tokens/transactions?network_slug=ethereum&contract_address=0x...`
2. Get pair quotes: `/v4/dex/pairs/quotes/latest?network_slug=ethereum&contract_address=0x...`

## Key Parameters

Most DEX endpoints require:

1. `network_slug` or `platform_crypto_id`: Identifies the blockchain (ethereum, solana, bsc)
2. `contract_address`: The token's on-chain contract address

Use `/v1/dex/platform/list` to get valid network slugs and platform IDs.

## Error Handling

| Code | Meaning |
|------|---------|
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (invalid or missing API key) |
| 403 | Forbidden (endpoint not in your plan) |
| 429 | Rate limit exceeded |
| 500 | Server error |

Example error response:

```json
{
  "status": {
    "error_code": 400,
    "error_message": "Invalid value for 'contract_address'"
  }
}
```

## Rate Limits

Rate limits depend on your API plan. Check response headers:

1. `X-CMC_PRO_API_KEY_CREDITS_REMAINING`: Credits left
2. `X-CMC_PRO_API_KEY_CREDITS_RESET`: Reset timestamp

## Response Format

All responses follow this structure:

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null
  },
  "data": { ... }
}
```
