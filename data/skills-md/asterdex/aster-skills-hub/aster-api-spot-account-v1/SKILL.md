---
name: aster-api-spot-account-v1
description: Account, balances, user trades, spot–futures transfer, withdraw, API key for Aster Spot API v1. Use when reading/updating spot account or transferring. Signed; see aster-api-spot-auth-v1.
---

# Aster Spot API Account (v1)

**Base:** https://sapi.asterdex.com. Endpoints signed unless noted.

## Account and trades

- **GET /api/v1/account** (W: 5): No params beyond auth. Returns balances (asset, free, locked).
- **GET /api/v1/userTrades** (W: 10): symbol (required), orderId, startTime, endTime, limit (default 500, max 1000).

## Transfer

- **POST /api/v1/asset/wallet/transfer** (W: 5): amount, asset, clientTranId (required, unique), kindType (FUTURE_SPOT | SPOT_FUTURE), timestamp. Returns tranId, status.

## Withdraw and API key

- **GET /api/v1/aster/withdraw/estimateFee** (NONE): chainId, asset. Returns tokenPrice, gasCost, gasUsdValue. chainId: 1 (ETH), 56 (BSC), 42161 (Arbi).
- **POST /api/v1/aster/user-withdraw** (USER_DATA): See reference for params; returns withdrawId, hash.
- **POST /api/v1/getNonce**, **POST /api/v1/createApiKey**: See reference for params.

Payload shapes: [reference.md](reference.md).
