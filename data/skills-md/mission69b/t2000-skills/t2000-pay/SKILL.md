---
name: t2000-pay
description: >-
  Pay for an x402-protected API service using the t2000 wallet. Use when an
  API returns a 402 Payment Required response, when asked to "call that paid
  API", "pay for data from", "access the x402 service at", or when fetching
  a resource that requires micropayment. Handles the full x402 handshake
  automatically.
license: MIT
status: active
metadata:
  author: t2000
  version: "1.2"
  requires: t2000 CLI (npx @t2000/cli init)
  available: true
---

# t2000: Pay for x402 API Service

## Status
✅ Active — requires `t2000` CLI with `@t2000/x402` installed.

## Purpose
Make a paid HTTP request to any x402-protected endpoint. Handles the 402
handshake, signs the USDC payment from the available balance, and returns
the API response.

## Command
```bash
t2000 pay <url> [options]

# Examples:
t2000 pay https://api.example.com/data
t2000 pay https://api.example.com/analyze --method POST --data '{"text":"hello"}'
t2000 pay https://api.example.com/premium --max-price 0.10
t2000 pay https://api.example.com/data --dry-run
t2000 pay https://api.example.com/data --header 'X-Custom=value' --timeout 60
```

## Options
| Option | Description | Default |
|--------|-------------|---------|
| `--method <method>` | HTTP method (GET, POST, PUT) | GET |
| `--data <json>` | Request body for POST/PUT | — |
| `--max-price <amount>` | Max USDC per request | $1.00 |
| `--header <key=value>` | Additional HTTP header (repeatable) | — |
| `--timeout <seconds>` | Request timeout in seconds | 30 |
| `--dry-run` | Show what would be paid without paying | — |

## Flow (automatic)
1. Makes initial HTTP request to the URL
2. If 402: reads PAYMENT-REQUIRED header for amount and terms
3. If price ≤ --max-price: signs and broadcasts USDC payment on Sui
4. Retries with X-PAYMENT proof header
5. Returns the API response body

## Safety
- If requested price exceeds --max-price, payment is refused (no funds spent)
- Default max-price: $1.00 USDC per request
- Payment only broadcast after 402 terms are validated

## Errors
- `PRICE_EXCEEDS_LIMIT`: API asking more than --max-price
- `INSUFFICIENT_BALANCE`: not enough available USDC
- `UNSUPPORTED_NETWORK`: 402 requires a network other than Sui
- `PAYMENT_EXPIRED`: payment challenge has expired
- `DUPLICATE_PAYMENT`: nonce already used on-chain
