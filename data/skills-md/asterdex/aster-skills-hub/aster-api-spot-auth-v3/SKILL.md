---
name: aster-api-spot-auth-v3
description: EIP-712 signed requests for Aster Spot Testnet API v3. Base sapi.asterdex-testnet.com, /api/v3/. Use when calling TRADE, USER_DATA, USER_STREAM, or MARKET_DATA on spot testnet. Algorithm same as aster-api-auth-v3.
---

# Aster Spot API Authentication (v3 — Testnet)

**Base:** https://sapi.asterdex-testnet.com. Path prefix: `/api/v3/`. Signed: send user, signer, nonce, signature in body.

| Param | Description |
|-------|--------------|
| user | Main account wallet |
| signer | API wallet |
| nonce | Current time, microseconds |
| signature | EIP-712 (hex) |

**Signing:** Same as [aster-api-auth-v3](skills/aster-api-auth-v3/SKILL.md): param string (key=value, sort ASCII); EIP-712 domain (testnet may use chainId 714—check api-docs); sign with API wallet private key; add signature to body. POST/DELETE: application/x-www-form-urlencoded.

**Noop:** **POST /api/v3/noop** (TRADE): Cancel in-flight requests that have not completed on-chain; nonce can be reset. Weight: 1.

Payload shapes: [reference.md](reference.md).
