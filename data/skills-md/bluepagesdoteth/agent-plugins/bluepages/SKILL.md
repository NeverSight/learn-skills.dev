---
name: bluepages
description: >
  Look up wallet address <> Twitter/Farcaster identity mappings via Bluepages.fyi.
  Use when asked who owns a wallet, finding addresses for a Twitter/Farcaster handle,
  looking up 0x addresses, or any wallet identity and address attribution queries.
compatibility: >
  Requires MCP server (npx github:bluepagesdoteth/bluepages-mcp) and one of:
  BLUEPAGES_API_KEY or PRIVATE_KEY (Ethereum, for x402 payments).
metadata:
  author: bluepages
  version: "1.0.2"
  openclaw:
    emoji: 📘
    install:
      - kind: node
        package: "github:bluepagesdoteth/bluepages-mcp"
    homepage: https://bluepages.fyi/docs.html
    requires:
      env:
        - BLUEPAGES_API_KEY
        - PRIVATE_KEY
---

# Bluepages

800K+ verified Ethereum address <> Twitter/X mappings, plus Farcaster.

## Setup

Requires the Bluepages MCP server: `npx -y github:bluepagesdoteth/bluepages-mcp`
or direct API calls (see below). The MCP server is the recommended way to use Bluepages.

## Authentication

Requires one of these env vars:

- **`BLUEPAGES_API_KEY`** (recommended) — 20% cheaper, 2x rate limits.
- **`PRIVATE_KEY`** — Ethereum private key for x402 pay-per-request (USDC on Base).

> **Security note**: Never use a main wallet key. Use a dedicated, funded-only-as-needed agent wallet if providing `PRIVATE_KEY`.

**With a private key**, you can either pay per request via x402 or purchase a `BLUEPAGES_API_KEY` using the `get_api_key` and `purchase_credits` MCP tools.

**Without a private key**, the user must get an API key at [bluepages.fyi/api-keys](https://bluepages.fyi/api-keys.html) and set `BLUEPAGES_API_KEY`.

## Tools (quick reference)

| Tool                       | Cost                   | Description                                        |
| -------------------------- | ---------------------- | -------------------------------------------------- |
| `check_address`            | 1 credit ($0.001)      | Check if address has data                          |
| `check_twitter`            | 1 credit ($0.001)      | Check if Twitter handle has data                   |
| `get_data_for_address`     | 50 credits ($0.05)     | Full identity data for address (free if not found) |
| `get_data_for_twitter`     | 50 credits ($0.05)     | Full identity data for handle (free if not found)  |
| `batch_check`              | 40 credits ($0.04)     | Check up to 50 items at once                       |
| `batch_get_data`           | 40 credits/found item  | Data for up to 50 items (x402: $2.00 flat/batch)   |
| `batch_check_streaming`    | same as batch_check    | For large lists (100+), shows progress             |
| `batch_get_data_streaming` | same as batch_get_data | For large lists (100+), shows progress             |
| `check_credits`            | free                   | Check remaining credits (API key only)             |
| `set_credit_alert`         | free                   | Set low-credit warning threshold (API key only)    |
| `get_api_key`              | free                   | Get/create API key via wallet signature            |
| `purchase_credits`         | $5–$600 USDC           | Buy credits via x402 (PRIVATE_KEY only)            |

## Input format

- **Addresses**: 0x-prefixed, 42-char hex. Case-insensitive.
- **Twitter handles**: With or without `@`.

## Cost-saving workflow

- **Single lookups**: `check_address`/`check_twitter` first (1 credit), then `get_data_*` only if found (50 credits). Skipping the check wastes credits on misses.
- **Batch lookups**: Always two-phase — `batch_check` then `batch_get_data` on found items only. This saves ~90% vs fetching everything blind.
- **Large lists (100+)**: Use `_streaming` variants for progress updates.

## Rate limits

- API Key: 60 req/min
- x402: 30 req/min
- Batch: max 50 items per request

## Alternative: Direct HTTP API

If MCP is unavailable, call the API directly. Auth depends on your setup:

- **API key**: pass `X-API-KEY` header
- **Private key (x402)**: endpoints return a 402 with payment details; sign and resend with `X-PAYMENT` header

```bash
# With API key
curl "https://bluepages.fyi/check?address=0x..." -H "X-API-KEY: your-key"
curl "https://bluepages.fyi/data?address=0x..." -H "X-API-KEY: your-key"

# Batch check
curl -X POST "https://bluepages.fyi/batch/check" \
  -H "X-API-KEY: your-key" -H "Content-Type: application/json" \
  -d '{"addresses": ["0x...", "0x..."]}'
```

Full API docs: [bluepages.fyi/docs](https://bluepages.fyi/docs.html)
