---
name: aster-api-errors-v3
description: Error codes, rate limits, 429/418 handling, retry/backoff for Aster Futures API v3. Use when handling API errors or building rate-aware clients.
---

# Aster API Errors

**Payload:** `{ "code": -1121, "msg": "..." }`. Handle by **code** (stable); messages may vary.

**Rate limits:** From GET /fapi/v3/exchangeInfo → rateLimits. **REQUEST_WEIGHT:** per IP (e.g. 2400/min); header `X-MBX-USED-WEIGHT-*`. **ORDERS:** per account (e.g. 1200/min); header `X-MBX-ORDER-COUNT-*`. **429:** back off. **418:** IP banned (2 min–3 days). Prefer WebSocket to reduce REST load.

**Security:** -1021 INVALID_TIMESTAMP → recvWindow or clock; use GET /fapi/v3/time. -1022 INVALID_SIGNATURE → check signing/API wallet key.

| Range | Category | Examples |
|-------|----------|----------|
| 10xx | Server/network | -1000, -1001, -1003, -1007, -1015, -1021, -1022 |
| 11xx | Request/params | -1102, -1121, -1130 |
| 20xx | Processing | -2010, -2011, -2013, -2018, -2019, -2021, -2025 |
| 40xx | Filters | -4004, -4014, -4023, -4047, -4048, -4164 |

**HTTP:** 4XX = client (403 WAF, 429, 418); 5XX = server. 503 = may have been processed—do not assume failure.

Payload shapes: [reference.md](reference.md).
