---
name: aster-api-spot-auth-v1
description: HMAC SHA256 signed requests for Aster Spot API v1 (main). Base sapi.asterdex.com, /api/v1/. Use when calling TRADE, USER_DATA, or USER_STREAM. Signed; algorithm same as aster-api-auth-v1.
---

# Aster Spot API Authentication (v1)

**Base:** https://sapi.asterdex.com. Path prefix: `/api/v1/`. API key + secret **case sensitive**. Signed: send timestamp, signature; optional recvWindow (default 5000 ms, keep ≤ 5000).

| Param | Description |
|-------|--------------|
| X-MBX-APIKEY | API key (header) |
| timestamp | Current time, ms |
| recvWindow | Request valid this long after timestamp |
| signature | HMAC SHA256(totalParams, secretKey), hex |

**Signature:** Same as [aster-api-auth-v1](skills/aster-api-auth-v1/SKILL.md): totalParams = query + body; HMAC SHA256(secretKey, totalParams) → hex; add signature to query or body; header X-MBX-APIKEY.

**Timing:** Server accepts if `timestamp < serverTime+1000` and `serverTime - timestamp <= recvWindow`. Use GET /api/v1/time if clock skew.

Payload shapes: [reference.md](reference.md).
