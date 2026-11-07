---
name: loyalty-points-integration
description: |
  Implement the Access Development Loyalty Points API on your server. This skill guides you
  through building the five REST endpoints Access calls to manage loyalty point balances,
  holds, redemptions, refunds, and cancellations. Covers the OpenAPI 3.0 contract, HMAC-SHA256
  request signing verifier (Stripe-style, per program), platform recipes, idempotency,
  hold lifecycle, and testing. Use when integrating loyalty points redemption ("burn")
  into the Access Travel Platform.
trigger: |
  Use when the developer wants to implement loyalty points endpoints for the Access Travel
  Platform, implement or troubleshoot an HMAC-SHA256 request signing verifier, scaffold a
  loyalty points server from the OpenAPI spec, or understand the hold/redeem/refund lifecycle
  for loyalty point transactions.
---

# Access Development - Loyalty Points Integration Skill

You are an expert integration engineer helping a developer implement the **Access Loyalty Points API** on their server. Access calls these endpoints during the travel shopping flow to manage loyalty point balances, holds, redemptions, refunds, and cancellations. Your job is to guide them through the contract, the HMAC request signing verifier, and testing in whatever language, framework, and hosting environment they use.

## How to use this skill

When a developer asks for help implementing loyalty points integration, follow the progressive disclosure pattern below. Start with the **Quick-Start Journey** that matches their need, then drill into the relevant reference sections as questions arise. The five endpoints do not wait on the security work - implement endpoints first, verify HMAC in parallel.

---

## 1 - Architecture Overview

```
┌─────────────────────┐         ┌──────────────────────────────────────────┐
│  Access Payment API │ ── HTTPS▶│  Public hostname of your loyalty API     │
│  (the caller)       │           │  TLS 1.2 or 1.3 · HMAC headers required │
└─────────────────────┘           └──────────────────┬───────────────────────┘
        │                                            │
        │ OkHttp + signing interceptor                │
        │ 5s timeout, 3 attempts, breaker            │
                                                     │
                                                     ▼
                                          ┌─────────────────────┐
                                          │ Your application    │
                                          │ verifies HMAC over  │
                                          │ the body and path   │
                                          └─────────────────────┘
```

**Key principle**: Access is the caller. The client implements five REST endpoints. Access signs every request with an HMAC-SHA256 signature derived from a per-program secret. **The application that receives the request must verify that signature** before any business logic runs. TLS provides confidentiality in transit; HMAC is the authentication.

### What you implement

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/loyalty/balance` | GET | Return available points balance and point-to-USD valuation |
| `/v1/loyalty/holds` | POST | Reserve (hold) points for a pending transaction |
| `/v1/loyalty/holds/{hold_id}/cancel` | POST | Release a previously created hold |
| `/v1/loyalty/redemptions` | POST | Deduct points for a confirmed booking |
| `/v1/loyalty/refunds` | POST | Credit points back for a refunded transaction |

All paths are relative to your base URL (e.g., `https://your-api.example.com/api`).

### Prerequisites

1. **Access Travel SDK integrated**: the SDK handles member onboarding and produces the `member_key` used in all loyalty requests. See the [Access Travel Integration skill](../access-travel-integration/) for setup.
2. **API credentials from Access**: Access provisions an HMAC `key_id` and secret per program at onboarding, sandbox and production secrets separately, and program-specific configuration.
3. **Domain allowlisting**: your domains must be added to Access's CSP allowlist before deployment.

---

## 2 - Quick-Start Journeys

### Journey A: "I need to implement the loyalty endpoints"

1. **Review the OpenAPI spec** (see `references/openapi.yaml`): it is the source of truth for request/response schemas, headers, and error codes.
2. **Implement the five endpoints** (see `references/endpoint-contract-reference.md` for detailed schemas and examples). Do not wait on HMAC work to begin business logic.
3. **Handle idempotency and hold lifecycle** (see `references/hold-lifecycle-and-idempotency.md`).
4. **Implement the HMAC verifier** in parallel using Journey B.
5. **Test with curl** using the HMAC examples in `references/testing-and-troubleshooting.md`.
6. **Coordinate go-live** with your Access Implementation Manager.

### Journey B: "I need to implement the HMAC verifier"

1. **Read the canonical HMAC spec** at `references/hmac-signing-spec.md` (sourced from `burn-specifications/hmac-sha256-request-signing.md`, which is the source of truth). The spec defines the headers, canonical string, replay window, 401 behavior, and rotation procedure.
2. **Reproduce spec test vectors 1–3** in your verifier's unit tests, exactly. If your verifier cannot reproduce these, your canonical string is wrong.
3. **Implement the verifier** following the algorithm in `references/hmac-signing-spec.md` § "Verifier algorithm (client)". Use constant-time comparison (`MessageDigest.isEqual`, `crypto.timingSafeEqual`, `hmac.compare_digest`, or `CryptographicOperations.FixedTimeEquals`). Hash the **raw bytes on the wire**: do not parse JSON and re-serialize.
4. **Reject with 401 `AUTHENTICATION_FAILED`** for any of: missing signature header, malformed `t=...`, `|now - t| > 300`, unknown `key_id`, or signature mismatch.
5. **Run negative tests** (see `references/testing-and-troubleshooting.md`): wrong secret, stale `t`, pretty-printed body, path-prefix mismatch, reordered JSON keys.
6. **Do not persist the `Idempotency-Key`** for a 401. A later correctly-signed retry with the same key must execute, not replay a cached auth failure.
7. **Coordinate rotation** with your Access Implementation Manager. During overlap, hold current and previous secrets, try only the secret named by `X-Access-Key-Id` (never HMAC-compare against every secret - a stolen old key would otherwise stay valid past retirement).

### Journey C: "I'm troubleshooting an HMAC verification failure"

1. **Reproduce spec vectors 1–3** first. If your verifier fails these, you have a canonical-string bug - fix it before going further.
2. **Use vector reproduction as the first step** when debugging a failing live request: compute the expected v1 against the spec's known inputs and compare to the value in `X-Access-Signature`. If they differ, the difference points at the bug.
3. **Re-check the negative-prevention rules** in the spec: raw body bytes (not re-serialized JSON), exact path-and-query on the wire (RFC 3986), constant-time compare, no comparison against every secret during rotation.
4. **Check platform-specific encoding**: `URLEncoder.encode` emits `+` for space; the spec requires RFC 3986 (`%20`). Make sure your framework's query encoding matches.
5. **Test against a local unsigned-TLS (or HTTP) mock signer** to isolate verifier logic from network variability. See `references/testing-and-troubleshooting.md` for worked examples with the spec's fixture secret.

### Journey D: "I need to understand the hold/redeem/refund lifecycle"

1. **Read `references/hold-lifecycle-and-idempotency.md`** for the full lifecycle.
2. Key concepts: holds reserve points (5 min default), redemption converts a hold to a permanent deduction, refunds credit points back after a redemption, cancel releases a hold without deducting points.
3. **Idempotency is mandatory**: all POST endpoints receive an `Idempotency-Key` header. You must persist it and return the original response on duplicate requests. Do **not** persist idempotency entries for 401s (see Journey B step 6).

---

## 3 - HMAC-SHA256 Request Signing Configuration

If you previously received mTLS instructions, disregard them: V1 has no client certificate. HMAC-SHA256 request signing is the sole authentication mechanism in V1. **The application that receives a request must verify the HMAC signature** before business logic runs. TLS provides transport-layer confidentiality; HMAC authenticates Access to your endpoints.

### Headers Access sends

| Header | Required | Description |
|---|---|---|
| `X-Access-Key-Id` | Yes | Opaque per-program key identifier (e.g., `hmac_key_1`). Sent in clear - public. |
| `X-Access-Signature` | Yes | `t=<unix-seconds>,v1=<64-hex-chars>`. The timestamp `t` and the HMAC-SHA256 v1 hex of the canonical string. |
| `X-Request-Timestamp` | Yes | ISO 8601 UTC timestamp from Access. Used for logging and latency, **not** the security clock - the security clock is the integer `t` inside `X-Access-Signature`. Do not parse the ISO header and feed it into HMAC; format differences across languages break verification. |
| `X-Request-ID` | No | Optional correlation/audit ID, may change between retries. |
| `Idempotency-Key` | Yes | POST only. Stable across retries of the same logical operation. |

### Canonical string

```
{t}.{METHOD}.{path_and_query}.{body_sha256_hex}
```

- `t` - Unix epoch **seconds** (integer, no millis). UTC.
- `METHOD` - uppercase HTTP method as sent (`GET` or `POST`).
- `path_and_query` - origin-form request target: path starting with `/`, plus `?` and query string when present. **Includes the client's URL prefix** (e.g., `/api/v1/loyalty/balance` if your base URL is `https://your-api.example.com/api`, or `/v1/loyalty/balance` if it is `https://your-api.example.com/`): 
- `body_sha256_hex` - lowercase hex SHA-256 of the **raw HTTP body bytes as transmitted**.
  - GET body is empty. SHA-256 of zero bytes is always `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
  - POST: hash the exact bytes on the wire. Do not parse JSON and re-serialize: whitespace, key order, and Unicode escaping all change the hash.

### Signature

```
v1 = lowercase_hex( HMAC-SHA256( key=utf8(secret), msg=utf8(canonical_string) ) )
```

Accept the signature header in the form `t=<seconds>,v1=<64 hex chars>`. Unknown elements in this header may be ignored (forward compatible). `t` and `v1` are required.

### Query encoding

Access encodes query values as **RFC 3986**: UTF-8, space as `%20`, unreserved `A-Z a-z 0-9 - . _ ~` left unencoded. Do **not** use `application/x-www-form-urlencoded` (`+` for space). Do not reorder query parameters. The signed path-and-query must be exactly what Access sent on the wire.

### Verifier algorithm (do this before idempotency lookup and business logic)

1. Ensure the public-facing request used HTTPS (TLS 1.2 or 1.3). TLS termination on a trusted proxy/LB is fine; the application itself may see HTTP. If your environment terminates TLS at a trusted edge, configure ingress policy accordingly and, if your application checks in-band, accept only a trusted `X-Forwarded-Proto: https` (or platform-equivalent) signal set by your ingress. Never trust a client-supplied forwarded-proto header.
2. Read `X-Access-Key-Id` and `X-Access-Signature`. If either is missing or `X-Access-Signature` does not contain `t` and `v1`, return **401** `AUTHENTICATION_FAILED`.
3. Parse `t` as an integer. If `|now_utc_seconds - t| > 300`, return **401** `AUTHENTICATION_FAILED` (replay / clock skew). 300 seconds matches the 5-minute hold window.
4. Look up the secret for `X-Access-Key-Id`. During rotation you hold two secrets. If the key id is unknown, return **401**.
5. Build `path_and_query` from the **received request** (path + query as on the wire).
6. SHA-256 the raw body (empty for GET).
7. Build the canonical string. Compute `expected_v1`.
8. Compare `expected_v1` to the provided `v1` in constant time. If they differ, return **401** `AUTHENTICATION_FAILED`.
9. Only then run business logic. On POST, then apply `Idempotency-Key` rules.

Use the spec's test vectors in your default unit test suite. If your verifier produces a different v1 for vector 1, 2, or 3, your canonical string is wrong. Fix that before testing live requests.

### Constant-time comparison

Always compare the expected and provided `v1` in constant time. Use `MessageDigest.isEqual` (Java), `crypto.timingSafeEqual` (Node), `hmac.compare_digest` (Python), or `CryptographicOperations.FixedTimeEquals` (.NET). Do **not** compare with `==` on decoded byte arrays or with `String.equals`; both leak timing information.

### 401 behavior

A 401 must be returned with:

```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error_code": "AUTHENTICATION_FAILED",
  "message": "Invalid or missing request signature"
}
```

Do not distinguish "wrong secret" vs. "wrong canonical string" vs. "stale timestamp" in the message body. The error code must remain constant so a stolen old key cannot probe for the cause.

Do **not** persist an `Idempotency-Key` for a 401. A later correctly-signed retry with the same key must execute, not replay a cached auth failure. This includes not caching any business-logic response keyed on an authed request that subsequently failed verification.

### Secret storage

The HMAC secret is a credential. Store it in your secrets manager (AWS Secrets Manager, HashiCorp Vault, your platform's equivalent). Never commit it, never place it in source, never include it in logs. The skill does not provide a placeholder secret; the fixture secret in `references/testing-and-troubleshooting.md` is for offline tests only, not for production.

### Rotation

Access supports a dual-secret overlap window. During rotation you hold current and previous secrets. The key id sent in `X-Access-Key-Id` determines which secret to verify with. **Try only the secret named by `X-Access-Key-Id`**. Never HMAC-compare against every secret you hold; that turns a stolen old key into a valid signer after Access has moved on, and it hides key-id bugs. After confirmed overlap (recommended: 7 days, or until no `hmac_key_<X>` traffic), retire the previous secret.

### TLS

TLS 1.2 or 1.3. Access negotiates either. There is **no** client certificate and **no** requirement to configure mTLS on the load balancer, API gateway, or application. The Access specification does not contain a `mutualTLS` security scheme. If your environment terminates TLS at an LB, that LB does not need a trust store for Access's certificate.

---

## 4 - Endpoint Contract Summary

All endpoints are under `/v1/loyalty/`. Full schemas, examples, and error codes are in `references/endpoint-contract-reference.md` and `references/openapi.yaml`.

### Headers

| Header | Required | Method | Description |
|--------|----------|--------|-------------|
| `X-Access-Key-Id` | Yes | All | Opaque per-program HMAC key identifier. Public. |
| `X-Access-Signature` | Yes | All | `t=<unix>,v1=<64-hex>`. Canonical signing string includes `t`, METHOD, `path_and_query`, body SHA-256. |
| `X-Request-Timestamp` | Yes | All | ISO 8601 UTC timestamp from Access. Logging only, not the HMAC clock. |
| `X-Request-ID` | No | All | Optional correlation/audit ID, regenerated per attempt. |
| `Idempotency-Key` | Yes | POST only | Stable across retries; persist for dedup. |
| `program-key` | Not yet sent | GET balance, POST holds | Planned; see below. Do not require it. |
| `X-Response-Timestamp` | Yes | All responses | ISO 8601 UTC timestamp generated by your server. |

### The program-key header

**Access does not currently send `program-key`.** Shipping it is tracked by PD-7890 and PD-7891. It is documented here so multi-program clients can design for it. Until those tickets are in production:

- **Do not require it.** Rejecting a request that omits `program-key` will break every call Access makes today.
- **Read it if present, otherwise fall back** to your single configured program.

It would become relevant when a single implementation serves multiple program instances with Access, which typically happens when:

- A client has multiple subscription tiers with different product access (e.g., one program for hotels-only, another for hotels + theme parks)
- A client operates multiple brands or divisions that are billed independently by Access
- A single API server handles loyalty points for multiple Access programs

If you think you need multi-program support, raise it with your Access Implementation Manager rather than building against this header.

### Error responses

All errors use a standard JSON body:

```json
{
  "error_code": "AUTHENTICATION_FAILED",
  "message": "Invalid or missing request signature"
}
```

HTTP status code mapping is per-operation: each operation declares its own response set, and there is no global mapping. **See [the full 404 / global-mapping explainer in `endpoint-contract-reference.md`](references/endpoint-contract-reference.md#error-response-schema)** for the rules and the per-operation status table. In short, 404 means the URL-asked-for resource does not exist; collection POSTs do not return 404. Access treats any 4xx as a failed call and does not retry it.

| `error_code` | HTTP Status | Operations | When to use |
|---|---|---|---|
| `AUTHENTICATION_FAILED` | 401 | All | Missing/invalid HMAC signature; do **not** persist `Idempotency-Key` |
| `INVALID_REQUEST` | 400 | All | Validation failure (bad fields, missing required) |
| `INSUFFICIENT_POINTS` | 409 | Holds | Not enough available points for the hold |
| `HOLD_NOT_FOUND` | 404 | Cancel | Hold ID does not exist |
| `HOLD_NOT_FOUND` | 409 | Redemptions | Hold does not exist or has expired. Redemptions define no 404. |
| `MEMBER_NOT_FOUND` | 404 | Balance | `member_key` does not match any member |
| `ALREADY_PROCESSED` | 409 | Redemptions, refunds, cancel | Hold already redeemed or cancelled; refund already processed. Used for **different** operations against an already-terminal hold; identical `Idempotency-Key` retries return the cached 200/201 instead. |
| `ERROR` | 500 | All | Internal server error |

Note that `POST /v1/loyalty/holds` defines only 400, 409, and 500. If `member_key` is unknown at hold time, return 400 `INVALID_REQUEST` rather than a 404 the contract does not define.

---

## 5 - Idempotency and Hold Lifecycle

### Idempotency (critical)

All POST endpoints receive an `Idempotency-Key` header from Access. This key is stable across retries of the same logical operation. Your implementation **must**:

1. Persist the `Idempotency-Key` with the response for every successfully processed request.
2. On receiving a duplicate key (after a verified HMAC signature; see Journey B step 6), return the original response without re-executing the operation.
3. Use whatever backing store fits your stack (Redis, database table, etc.).

Do **not** turn a retry of the same logical operation into `409 ALREADY_PROCESSED`. Same `Idempotency-Key` means return the cached 200/201 and body. `ALREADY_PROCESSED` is only for a *different* operation against a hold that is already terminal (for example cancel after a successful redeem, or a second redeem with a new key). Access treats any 409 as a failed capture.

This follows the [Stripe idempotency convention](https://docs.stripe.com/api/idempotent_requests). See `references/hold-lifecycle-and-idempotency.md` for implementation patterns.

### Hold lifecycle

```
    ┌─────────┐     POST /holds      ┌─────────┐
    │ (none)  │ ──────────────────▶ │ ACTIVE  │
    └─────────┘                     └────┬────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
              POST /redemptions   POST /holds/{id}/cancel   (auto-expire
                    │                    │                  after duration)
                    ▼                    ▼                    │
              ┌─────────┐          ┌──────────┐              ▼
              │ REDEEMED│          │CANCELLED │         ┌─────────┐
              └────┬────┘          └──────────┘         │ EXPIRED │
                   │                                     └─────────┘
              POST /refunds
                   │
                   ▼
              ┌──────────┐
              │ REFUNDED │  (points credited back)
              └──────────┘
```

Key rules:

- **Hold duration**: Access standard is 5 minutes. Your system must auto-release unredeemed holds after expiry.
- **Redemption requires an active hold**: You cannot redeem without a prior hold.
- **Cancel vs refund**: Cancel releases a hold (points were never deducted). Refund credits back already-deducted points after a redemption.
- **Atomicity**: Use database transactions for hold and redemption operations to prevent double-spending under concurrent requests. Redeem unique-inserts Access's `transaction_id` in the same transaction as the hold becoming `REDEEMED`.

See `references/hold-lifecycle-and-idempotency.md` for detailed implementation guidance.

---

## 6 - Response Time Budget and Retry Behavior

Access enforces a strict timeout on every call. Your endpoints must answer well inside it, or the integration will fail in ways that are hard to diagnose from your side.

| Property | Value |
|---|---|
| Connect / read / write timeout | **5 seconds each** |
| Attempts per logical operation | **3** (1 initial + 2 retries) |
| Backoff between attempts | 500ms, then 1000ms, then 2000ms |
| Retried | 5xx responses and connection/IO failures |
| **Not** retried | **All 4xx responses** |
| Circuit breaker | Opens after 5 consecutive failed calls, stays open 30 seconds |

What this means for your implementation:

- **Answer within 5 seconds.** A hold that takes 8 seconds will never succeed, no matter how correct it is. Access sees a read timeout, retries twice, and gives up. Budget for your slowest dependency, not your median.
- **Return 4xx for real client errors only.** A 4xx stops Access immediately with no retry. Returning 400 for a transient internal problem turns a recoverable blip into a lost booking. Use 5xx for anything you want retried.
- **This is why idempotency matters.** All three attempts carry the same `Idempotency-Key`. If your server processed attempt 1 but the response was lost, attempts 2 and 3 must return the stored response rather than creating a second hold or deducting points twice. See section 5.
- **Sustained failures trip a breaker.** After 5 consecutive failures Access stops calling your endpoints for 30 seconds. During that window every transaction that would use points fails. Recovery is automatic, but a flapping endpoint produces disproportionate customer impact.
- **`X-Request-ID` changes per attempt; `Idempotency-Key` does not.** Correlate retries by `Idempotency-Key`, not by `X-Request-ID`.

---

## 7 - Data Precision Rules

- **Points are integers**: no fractions. A member has 250000 points, not 250000.5.
- **USD values are strings**: always use string representation (e.g., `"0.01"`, `"100.00"`) to avoid floating-point precision issues. This follows best practices for financial APIs.
- **Exchange rate is a string**: `loyalty_point_to_usd_exchange_rate` is a string like `"0.01"` (1 point = $0.01). The pattern is `^\d+\.\d{2}$`.
- **All monetary values are in USD** today. Additional currencies are planned.

---

## 8 - Testing

### Quick test with curl (HMAC)

The fixture secret in these examples is `test_loyalty_hmac_secret_do_not_use_in_prod` and the fixture key id is `hmac_key_1`. **Never use a real credential in source or shared test scripts.**

The `t=` value (`X-Access-Signature`'s timestamp element) must be Unix epoch seconds for the moment of the request. The `v1` value is the lowercase hex HMAC-SHA256 of `utf8(secret)` keyed against the canonical string `{t}.{METHOD}.{path_and_query}.{sha256_hex(raw_body)}`. See `references/hmac-signing-spec.md` for the full algorithm and `references/testing-and-troubleshooting.md` for worked examples including `openssl dgst` one-liners and language snippets.

```bash
# Test balance endpoint
curl -v \
  "https://loyalty.yourdomain.com/api/v1/loyalty/balance?member_key=abc123" \
  -H "X-Access-Key-Id: hmac_key_1" \
  -H "X-Access-Signature: t=1787313600,v1=<computed>" \
  -H "X-Request-Timestamp: 2026-08-21T12:00:00Z"

# Test hold creation
curl -v \
  -X POST "https://loyalty.yourdomain.com/api/v1/loyalty/holds" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key-Id: hmac_key_1" \
  -H "X-Access-Signature: t=1787313600,v1=<computed>" \
  -H "X-Request-Timestamp: 2026-08-21T12:00:00Z" \
  -H "Idempotency-Key: hold-001" \
  -d '{
    "member_key": "abc123",
    "points_requested": 10000,
    "hold_duration_minutes": 5,
    "transaction_description": "Hotel booking hold"
  }'
```

`<computed>` is `HMAC-SHA256(secret, canonical_string)` hex-encoded. The canonical string for vector 1 of the spec is:

```
1787313600.GET./api/v1/loyalty/balance?member_key=abc123.e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

which yields `v1 = d910ff46fe7cddbc1c6580148a10dc0a170e221bcc3a6e77e8a0fcfc47e048bf`. If your implementation produces a different v1 here, your canonical string is wrong.

See `references/testing-and-troubleshooting.md` for:

- Full negative scenarios (wrong secret, stale `t`, pretty-printed body, path-prefix mismatch, reordered JSON keys)
- Vector reproduction as the first troubleshooting step
- Language-specific debug commands
- Common error diagnosis
- Go-live validation checklist

---

## 9 - Go-Live Checklist

Before production launch, confirm:

- [ ] All five endpoints implemented and tested against the OpenAPI spec
- [ ] HMAC verifier reproduces spec vectors 1–3 exactly (see `references/hmac-signing-spec.md`)
- [ ] HMAC verifier uses constant-time comparison (`MessageDigest.isEqual`, `crypto.timingSafeEqual`, `hmac.compare_digest`, or `CryptographicOperations.FixedTimeEquals`)
- [ ] HMAC verifier hashes the **raw body bytes** before any JSON parse or re-serialization
- [ ] HMAC verifier uses the **exact path-and-query of the received request** (no reconstructed URL), with RFC 3986 encoding
- [ ] HMAC verifier rejects with 401 `AUTHENTICATION_FAILED` for missing `X-Access-Key-Id` / `X-Access-Signature`, malformed `t`, `|now - t| > 300`, unknown `key_id`, or signature mismatch. The body never distinguishes these cases
- [ ] `Idempotency-Key` persistence does **not** cache 401s; a later correctly-signed retry with the same key executes again
- [ ] Secret rotation: verifier holds current and previous key ids during overlap, tries only the secret named by `X-Access-Key-Id` (never HMAC-compare against every secret)
- [ ] TLS 1.2 or 1.3 verified end-to-end on the public hostname
- [ ] No client-certificate requirement anywhere on the public hostname (load balancer, reverse proxy, application)
- [ ] **p99 response time under 5 seconds** on all five endpoints, measured under production-like load
- [ ] Transient/internal failures return 5xx, not 4xx (Access never retries a 4xx)
- [ ] Server does not require `program-key` and accepts requests that omit it
- [ ] HMAC secrets stored in a vault (AWS Secrets Manager, HashiCorp Vault, or platform equivalent) - never in source, never in logs
- [ ] Secret delivery to your side is via the Implementation Manager channel, never email in the clear
- [ ] `X-Response-Timestamp` header included on all responses
- [ ] All USD values serialized as strings (not numbers)
- [ ] All points values are integers
- [ ] JSON field names use snake_case (e.g., `member_key`, `points_requested`)
- [ ] Sandbox testing completed with Access
- [ ] Domains added to Access CSP allowlist
- [ ] Access Implementation Manager has validated that signed requests from stage are accepted

---

## Instruction to the LLM

1. If the travel SDK is not already working, point at the [Access Travel Integration skill](../access-travel-integration/) first. `member_key` comes from it.
2. Whenever the developer asks about **mTLS**, **client certificate**, **TLS 1.3-only**, or **certificate rotation for the Access integration**, do **not** generate mTLS code or a network-team brief - V1 uses HMAC-SHA256 signing. , no client certificate. Point at `references/hmac-signing-spec.md` and Journey B / section 3.
3. Implement the five endpoints without waiting on the verifier. If HMAC work is partial, keep going on business logic and return to verifier implementation when ready.
4. Before claiming goto-live readiness, verify the **spec vectors 1–3** in the developer's verifier implementation. Different v1 results = canonical-string bug, fix before going further.
5. Do not require `program-key`. On redeem, the confirmatory omit/mismatch rule applies only to `member_key` and `points_to_redeem` (those live on the hold). `transaction_details` is required; persist it and echo `transaction_details.transaction_id`. If the object or the id is missing, return 400 `INVALID_REQUEST`. Never invent a `transaction_id`; Access refunds with the id it sent. Persist `transaction_id` uniquely in the same database transaction as the hold becoming `REDEEMED`.

---

## Reference Files

| File | Description |
|------|-------------|
| `references/openapi.yaml` | OpenAPI 3.0 specification (source of truth for endpoint contract and security scheme) |
| `references/hmac-signing-spec.md` | Canonical HMAC-SHA256 signing spec, copied from `burn-specifications/hmac-sha256-request-signing.md` (which is the source of truth - keep these in sync) |
| `references/endpoint-contract-reference.md` | Detailed endpoint schemas, request/response examples, error codes |
| `references/hold-lifecycle-and-idempotency.md` | Hold states, redemption flow, refund handling, idempotency patterns |
| `references/testing-and-troubleshooting.md` | Test scenarios (happy path, vector reproduction, negative cases), curl commands, common issues, debug guide |

The previous `references/mtls-configuration-guide.md` (with mTLS intake, network-team brief, and platform recipes for ALB/NLB/nginx/HAProxy) has been retired for V1. If your team is asked to use it, please escalate to the Access Implementation Manager - V1 no longer accepts mTLS as a substitute for HMAC, and mTLS recipes do not match the source of truth.

---

*For questions or support, contact your Access Implementation Manager.*
