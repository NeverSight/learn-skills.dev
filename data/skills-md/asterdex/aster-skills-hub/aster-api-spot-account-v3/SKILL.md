---
name: aster-api-spot-account-v3
description: Account, balances, user trades, spot–futures transfer, withdraw, API key for Aster Spot Testnet API v3. Use when reading/updating spot testnet account or transferring. Signed; see aster-api-spot-auth-v3.
---

# Aster Spot API Account (v3 — Testnet)

**Base:** https://sapi.asterdex-testnet.com. Endpoints signed unless noted.

## Account and trades

- **GET /api/v3/account** (W: 5): No params beyond auth. Returns balances (asset, free, locked).
- **GET /api/v3/userTrades** (W: 10): symbol (required), orderId, startTime, endTime, limit (default 500, max 1000).

## Transfer

- **POST /api/v3/asset/wallet/transfer** (W: 5): amount, asset, clientTranId (required, unique), kindType (FUTURE_SPOT | SPOT_FUTURE). Returns tranId, status.

## Withdraw and API key

- **GET /api/v3/aster/withdraw/estimateFee** (NONE): chainId, asset. Returns tokenPrice, gasCost, gasUsdValue.
- **POST /api/v3/aster/user-withdraw** (USER_DATA): See reference for params; returns withdrawId, hash.
- **POST /api/v3/getNonce**, **POST /api/v3/createApiKey**: See reference for params.

Payload shapes: [reference.md](reference.md).
