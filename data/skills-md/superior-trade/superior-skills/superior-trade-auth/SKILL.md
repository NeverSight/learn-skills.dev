---
name: superior-trade-auth
description: Use when an agent needs to register a Superior Trade account, verify an email OTP, configure x-api-key authentication, or recover from missing or invalid credentials before using the Unified API.
license: see LICENSE
metadata:
  openclaw:
    requires:
      env:
        - SUPERIOR_TRADE_API_KEY
    primaryEnv: SUPERIOR_TRADE_API_KEY
    envVars:
      - name: SUPERIOR_TRADE_API_KEY
        required: true
        description: Superior Trade API key, sent as the x-api-key header.
  version: "1.0.0"
---

# Superior Trade Authentication

Use this skill to get a Superior Trade API key and make authenticated requests to `https://api.superior.trade`.

## API Key Onboarding

If a user does not already have a Superior Trade API key, ask for the email address that should receive the key. Do not ask for wallet keys, seed phrases, private keys, passwords, or other secrets.

Request a verification OTP with:

```bash
curl -sS https://api.superior.trade/account/register \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com"}'
```

Ask the user for the OTP sent to that inbox, then exchange it for an API key:

```bash
curl -sS https://api.superior.trade/account/verify \
  -X POST \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","otp":"123456"}'
```

Tell the user to configure the returned key in their normal credential store or environment, usually as `SUPERIOR_TRADE_API_KEY`.

Do not paste the received key into chat, source files, logs, or examples. If the user provides a key in chat, treat it as a secret and avoid repeating it.

## Authenticated Requests

Use the key in the `x-api-key` header:

```bash
curl -sS https://api.superior.trade/account \
  -H "x-api-key: $SUPERIOR_TRADE_API_KEY"
```

The email is verified once the API key is used successfully in an authenticated request such as the status check above. If the first authenticated request fails with `401` or `403`, ask the user to confirm they copied the full key from the latest email and that the credential is being passed as the `x-api-key` header.

## Operating Rules

- Prefer `SUPERIOR_TRADE_API_KEY` from the environment or credential manager when it is available.
- Use `https://api.superior.trade` as the production API base URL.
- Use only the unversioned Unified API contract from `GET /openapi.json`.
- Use `Content-Type: application/json` for JSON request bodies.
- Never fabricate authentication status. Verify by making a real API call when credentials are available.
- Never request or handle private keys, seed phrases, or wallet credentials.
- Never start live trading, deposits, or other fund-moving actions without the explicit confirmations required by the relevant Superior Trade trading skill.

## Next: the rest of the library

This page covers authentication only. Everything past the API key — funding, strategy selection, backtesting, deployment — lives in the installable skill library.

Install it:

```bash
npx skills add Superior-Trade/superior-skills
```

Then load `skills/superior-trade`, which owns the full path from an empty account to a running strategy and hands off to the venue skills.

- `skills/superior-trade` — start here; the access → funding → backtest → deploy path
- `skills/hyperliquid` — Hyperliquid perps and spot, including HIP-3 stocks and commodities
- `skills/polymarket` — Polymarket discovery, backtests, and deployments
- `skills/lighter` — Lighter market context, wallet checks, backtests, and contract-supported Nautilus deployments
- `skills/aerodrome` — Aerodrome/Base spot-AMM workflows
- `skills/deposit-qr` — QR code or payment URI to fund a Superior-managed wallet
- `skills/external-deposit` — external bridge links, Relay quotes, MetaMask Mobile QR
