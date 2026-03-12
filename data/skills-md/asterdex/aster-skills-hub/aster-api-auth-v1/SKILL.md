---
name: aster-api-auth-v1
description: HMAC SHA256 signed requests for Aster Futures API v1. X-MBX-APIKEY, timestamp, recvWindow, signature. Use when calling TRADE, USER_DATA, or USER_STREAM (/fapi/v1/ or v2/v4).
---

# Aster API Authentication (v1)

**Base:** https://fapi.asterdex.com. API key + secret **case sensitive**. Signed: send timestamp, signature; optional recvWindow (default 5000 ms, keep ≤ 5000).

| Param | Description |
|-------|--------------|
| X-MBX-APIKEY | API key (header) |
| timestamp | Current time, ms |
| recvWindow | Request valid this long after timestamp |
| signature | HMAC SHA256(totalParams, secretKey), hex |

**Signature:** (1) totalParams = query + body (no `&` between; GET = query only; POST/PUT/DELETE = query + body as sent). (2) HMAC SHA256(secretKey, totalParams) → hex. (3) Add signature to query or body (last param); header X-MBX-APIKEY. Signature not case sensitive.

**Timing:** Server accepts if `timestamp < serverTime+1000` and `serverTime - timestamp <= recvWindow`. Use GET /fapi/v1/time if clock skew. **Security:** Env vars for key/secret; keys can be restricted (TRADE-only etc.).

Payload shapes: [reference.md](reference.md).
