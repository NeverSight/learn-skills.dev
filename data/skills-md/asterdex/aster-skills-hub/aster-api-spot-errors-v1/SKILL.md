---
name: aster-api-spot-errors-v1
description: Error codes, rate limits, 429/418 handling for Aster Spot API v1. Use when handling spot API errors or building rate-aware clients.
---

# Aster Spot API Errors (v1)

**Payload:** `{ "code": -1121, "msg": "..." }`. Handle by **code** (stable); messages may vary.

**Rate limits:** From GET /api/v1/exchangeInfo → rateLimits. **REQUEST_WEIGHT:** per IP (e.g. 1200/min); header `X-MBX-USED-WEIGHT-*`. **ORDERS:** per account (e.g. 100/min); header `X-MBX-ORDER-COUNT-*`. **429:** back off. **418:** IP banned (2 min–3 days). Prefer WebSocket to reduce REST load.

**Security:** -1021 INVALID_TIMESTAMP → recvWindow or clock; use GET /api/v1/time. -1022 INVALID_SIGNATURE → check HMAC/secret.

| Range | Category | Examples |
|-------|----------|----------|
| 10xx | Server/network | -1000, -1001, -1003, -1021, -1022 |
| 11xx | Request/params | -1102, -1121, -1130 |
| 20xx | Processing | -2010, -2011, -2013, -2018, -2019, -2021 |

**HTTP:** 4XX = client (403 WAF, 429, 418); 5XX = server. 503 = may have been processed—do not assume failure.

Payload shapes: [reference.md](reference.md).
