---
name: coingecko-api
description: This skill should be used when the user asks to "get crypto price", "check Bitcoin price", "query token price", "get market data", "check crypto market cap", "find trending coins", "get historical price data", "get OHLC data", "get candlestick data", "lookup token by contract address", "search for a coin", "get coin info", "get token logo", "find token icon", "get global crypto stats", "check Bitcoin dominance", or mentions CoinGecko API, cryptocurrency price queries, or crypto market data.
---

# CoinGecko API

## Overview

Query cryptocurrency market data using the CoinGecko API V3. This skill covers:

- Price lookups by coin ID, symbol, or contract address
- Market data with rankings, volume, and price changes
- Historical price charts and OHLC data
- Search and trending coins
- Global market statistics

**Scope:** Covers the Demo (free), Analyst, Lite, and Pro tiers. For on-chain DEX data (GeckoTerminal endpoints), consult the fallback documentation.

## Prerequisites

### API Key Detection

Before making any API call, determine the available API key:

```bash
if [ -n "$COINGECKO_PRO_API_KEY" ]; then
  CG_BASE="https://pro-api.coingecko.com/api/v3"
  CG_AUTH=(-H "x-cg-pro-api-key: $COINGECKO_PRO_API_KEY")
elif [ -n "$COINGECKO_API_KEY" ]; then
  CG_BASE="https://api.coingecko.com/api/v3"
  CG_AUTH=(-H "x-cg-demo-api-key: $COINGECKO_API_KEY")
else
  CG_BASE="https://api.coingecko.com/api/v3"
  CG_AUTH=()
  echo "Warning: No CoinGecko API key found. Using keyless access (stricter rate limits)."
  echo "For higher limits, set COINGECKO_API_KEY or COINGECKO_PRO_API_KEY."
fi
```

### API Tiers

| Tier | Base URL | Auth Header | Rate Limit |
| ---- | -------- | ---------- | ---------- |
| Demo | `https://api.coingecko.com/api/v3` | `x-cg-demo-api-key` | ~30 calls/min, ~10k/month |
| Analyst / Lite / Pro | `https://pro-api.coingecko.com/api/v3` | `x-cg-pro-api-key` | Plan-dependent |

Authentication via HTTP header (recommended). Query parameters (`x_cg_demo_api_key` / `x_cg_pro_api_key`) also work.

## Coin ID Resolution

CoinGecko uses string IDs (e.g., `bitcoin`, `ethereum`, `uniswap`) rather than symbols. Before querying, resolve the correct coin ID.

### Resolution Strategy

1. **Common coins** — Use well-known IDs directly: `bitcoin`, `ethereum`, `solana`, `cardano`, `chainlink`, `uniswap`, `aave`, `maker`. Note that some IDs diverge from the coin name: `binancecoin` (BNB), `avalanche-2` (AVAX), `polygon-ecosystem-token` (POL) — see the table below.
2. **Symbol lookup** — Use `/simple/price` with the `symbols` parameter for quick lookups: `symbols=btc,eth`. Symbols are not unique — multiple coins can share the same symbol. By default, only the top-market-cap coin per symbol is returned; pass `include_tokens=all` to get all matches.
3. **Ambiguous symbols** — If a symbol maps to multiple coins (e.g., "UNI" could be Uniswap or Universe), use `/search?query=<name>` to disambiguate. Always verify the result matches the user's intent.
4. **Contract address** — Use `/simple/token_price/{platform_id}` when a contract address is provided.
5. **Unknown coins** — Use `/search?query=<term>` to find the correct ID before querying.

### Common Coin IDs

| Coin | ID | Symbol |
| ---- | -- | ------ |
| Bitcoin | `bitcoin` | BTC |
| Ethereum | `ethereum` | ETH |
| Solana | `solana` | SOL |
| BNB | `binancecoin` | BNB |
| XRP | `ripple` | XRP |
| Cardano | `cardano` | ADA |
| Dogecoin | `dogecoin` | DOGE |
| Chainlink | `chainlink` | LINK |
| Avalanche | `avalanche-2` | AVAX |
| Polygon | `polygon-ecosystem-token` | POL |
| Uniswap | `uniswap` | UNI |
| Aave | `aave` | AAVE |
| Maker | `maker` | MKR |
| USDC | `usd-coin` | USDC |
| USDT | `tether` | USDT |
| DAI | `dai` | DAI |
| Wrapped BTC | `wrapped-bitcoin` | WBTC |

## Platform Resolution

Do not default to Ethereum. Always infer the platform from the user's prompt before making contract-based API calls.

### Inference Rules

1. **Explicit platform mention** — If the user mentions a chain name (e.g., "on Polygon", "Arbitrum token", "Base chain"), map it to the corresponding platform ID (see `./references/platforms.md`).
2. **Platform-specific tokens** — Some tokens exist primarily on specific platforms:
   - SOL, BONK, JUP → Solana (`solana`)
   - POL → Polygon (`polygon-pos`)
   - ARB → Arbitrum One (`arbitrum-one`)
   - OP → Optimism (`optimistic-ethereum`)
3. **Address format hints** — Base58 addresses (no `0x` prefix) may be Solana or Tron — ask the user to clarify. `0x`-prefixed addresses are EVM but exist on multiple chains.
4. **Testnet keywords** — Words like "testnet", "Sepolia", "Goerli", "devnet" indicate testnets. CoinGecko does not index testnet tokens — inform the user immediately.
5. **Ambiguous cases** — If the platform cannot be inferred, **ask the user** before proceeding. Do not assume Ethereum.

### Unsupported Platforms

If the user references a chain not indexed by CoinGecko, respond with:

```
The chain "[chain name]" is not supported by the CoinGecko API.

For the current list of supported platforms, query:
https://api.coingecko.com/api/v3/asset_platforms
```

For a curated list of common platforms, see `./references/platforms.md`. For the full live index, query the endpoint above.

## Core Workflows

### Quick Price Check

Fetch current price for one or more coins:

```bash
curl -s "$CG_BASE/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_market_cap=true" "${CG_AUTH[@]}"
```

For symbol-based lookups:

```bash
curl -s "$CG_BASE/simple/price?symbols=btc,eth&vs_currencies=usd" "${CG_AUTH[@]}"
```

### Token Price by Contract Address

Fetch price using a contract address on a specific chain:

```bash
curl -s "$CG_BASE/simple/token_price/ethereum?contract_addresses=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&vs_currencies=usd&include_market_cap=true" "${CG_AUTH[@]}"
```

Common platform IDs: `ethereum`, `polygon-pos`, `arbitrum-one`, `optimistic-ethereum`, `base`, `avalanche`, `binance-smart-chain`. For the full list, see `./references/platforms.md`.

### Token Logo

The `/coins/{id}` response includes logo URLs in the `image` object:

| Field | Typical Size |
| ----- | ------------ |
| `image.thumb` | 25x25 px |
| `image.small` | 50x50 px |
| `image.large` | 200x200 px |

Fetch via `/coins/{id}` or `/coins/{platform}/contract/{address}` — the `image` field is present in both responses.

### Market Rankings

Fetch top coins by market cap with detailed data:

```bash
curl -s "$CG_BASE/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&price_change_percentage=24h,7d" "${CG_AUTH[@]}"
```

### Historical Price Data

Fetch price history for charts:

```bash
# Last 7 days (hourly granularity)
curl -s "$CG_BASE/coins/bitcoin/market_chart?vs_currency=usd&days=7" "${CG_AUTH[@]}"

# Last 365 days (daily granularity)
curl -s "$CG_BASE/coins/bitcoin/market_chart?vs_currency=usd&days=365" "${CG_AUTH[@]}"
```

Auto-granularity: 1 day → 5-min intervals, 2-90 days → hourly, >90 days → daily.

Response contains `prices`, `market_caps`, and `total_volumes` arrays of `[timestamp_ms, value]` pairs.

### OHLC / Candlestick Data

Fetch OHLC data for charting:

```bash
curl -s "$CG_BASE/coins/bitcoin/ohlc?vs_currency=usd&days=7" "${CG_AUTH[@]}"
```

Returns `[[timestamp, open, high, low, close], ...]`. Valid `days` values: `1`, `7`, `14`, `30`, `90`, `180`, `365`, `max`.

### Global Market Stats

```bash
curl -s "$CG_BASE/global" "${CG_AUTH[@]}"
```

Returns total market cap, 24h volume, BTC/ETH dominance percentages, and active cryptocurrencies count.

### Search for a Coin

```bash
curl -s "$CG_BASE/search?query=sablier" "${CG_AUTH[@]}"
```

Returns matching coins, exchanges, categories, and NFTs sorted by market cap.

### Trending Coins

```bash
curl -s "$CG_BASE/search/trending" "${CG_AUTH[@]}"
```

Returns top trending coins based on CoinGecko search activity.

## Output Formatting

**Default behavior:** Present results in a Markdown table:

```markdown
| Coin | Price (USD) | 24h Change | Market Cap |
| ---- | ----------- | ---------- | ---------- |
| Bitcoin | $67,187.34 | +3.64% | $1.32T |
| Ethereum | $3,456.78 | +2.15% | $415.2B |
```

**User preference:** If the user requests a specific format (JSON, CSV, plain text), use that format instead.

### Number Formatting

- Prices > $1: 2 decimal places (e.g., `$67,187.34`)
- Prices $0.01–$1: 4 decimal places (e.g., `$0.4523`)
- Prices < $0.01: 6+ decimal places (e.g., `$0.000001234`)
- Market caps: abbreviated (e.g., `$1.32T`, `$415.2B`, `$8.5M`)
- Percentages: 2 decimal places with sign (e.g., `+3.64%`, `-1.23%`)

## Rate Limits

For Pro/Analyst/Lite plans, query the `/key` endpoint for live quotas (Pro base URL only — returns 401 on Demo):

```bash
curl -s "https://pro-api.coingecko.com/api/v3/key" -H "x-cg-pro-api-key: $COINGECKO_PRO_API_KEY"
```

Returns `plan`, `rate_limit_request_per_minute`, `monthly_call_credit`, and `current_remaining_monthly_calls`. Demo users should refer to the [pricing page](https://www.coingecko.com/en/api/pricing) for current limits.

**Approximate defaults** (may vary):

| Tier | Requests/Min | Monthly Cap |
| ---- | ------------ | ----------- |
| Demo (free) | ~30 | ~10,000 |
| Analyst | ~500 | ~500,000 |
| Lite | ~500 | ~1,000,000 |
| Pro | ~1,000 | ~3,000,000 |

If rate limited (HTTP 429), wait briefly and retry. Batch multiple coin queries into single calls using comma-separated IDs where possible.

## Error Handling

| HTTP Code | Error Code | Cause | Action |
| --------- | ---------- | ----- | ------ |
| 401 | 10002 | Invalid or missing API key | Verify the key value and base URL match the tier |
| 401 | 10005 | Endpoint not included in current plan | Use the tier-restricted fallback below |
| 429 | — | Rate limit exceeded | Wait and retry; reduce request frequency |
| 200 `{}` | — | Unknown coin ID or contract address | `/simple/*` endpoints return empty `{}` instead of 404 for unrecognized IDs/addresses. Treat an empty response as "not found" and use `/search` to resolve the correct ID |
| 404 | — | Invalid endpoint path | Verify the endpoint URL is correct |

### Tier-Restricted Endpoints

Some endpoints return 401 (error code 10005) on the Pro base URL for lower-tier plans (e.g., Analyst) but work on the Demo base URL.

**Known Analyst-tier restrictions** (401/10005 on Pro base URL):
- `/search/trending`
- `/global`
- `/global/decentralized_finance_defi`

**Fallback strategy:** On a 401 with error code 10005, retry on the Demo base URL. If `COINGECKO_API_KEY` is available, use it for better rate limits; otherwise fall back to keyless:

```bash
if [ -n "$COINGECKO_API_KEY" ]; then
  curl -s "https://api.coingecko.com/api/v3/search/trending" \
    -H "x-cg-demo-api-key: $COINGECKO_API_KEY"
else
  curl -s "https://api.coingecko.com/api/v3/search/trending"
fi
```

Do not use this fallback for error code 10002 (invalid key) — that indicates a misconfigured API key, not a tier restriction.

## Reference Files

- **`./references/endpoints.md`** — Curated endpoint reference with parameters, response formats, and asset platform IDs
- **`./references/platforms.md`** — Curated list of common asset platform IDs with chain mappings (query `/asset_platforms` for the full live index)

## Fallback Documentation

For endpoints not covered by this skill (on-chain DEX data, NFT details, exchange-specific queries), fetch the AI-friendly documentation:

```
https://docs.coingecko.com/llms.txt
```

Use `WebFetch` to retrieve this documentation for extended API capabilities.
