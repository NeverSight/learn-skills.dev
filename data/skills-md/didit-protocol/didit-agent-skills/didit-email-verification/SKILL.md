---
name: didit-email-verification
description: >
  Integrate Didit Email Verification standalone API to verify email addresses via OTP.
  Use when the user wants to verify emails, send email OTP codes, check email verification codes,
  detect breached or disposable emails, check if an email is undeliverable, or implement
  email-based identity verification using Didit. Supports fraud signals (IP, device, user agent),
  configurable code length, alphanumeric codes, and policy-based auto-decline for risky emails.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "✉️"
    homepage: https://docs.didit.me
---

# Didit Email Verification API

## Overview

Two-step email verification via one-time code:

1. **Send** a verification code to an email address
2. **Check** the code the user provides

**Key constraints:**
- Code expires after **5 minutes**
- Maximum **3 verification attempts** per code (then must resend)
- Maximum **2 resend requests** within 24 hours
- You **must call Send before Check** — Check returns `"Expired or Not Found"` otherwise

**Capabilities:** Detects breached emails (via known data breaches), disposable/temporary email providers, and undeliverable addresses. Supports fraud signals for risk scoring.

**API Reference:** [Send Code](https://docs.didit.me/standalone-apis/email-send) | [Check Code](https://docs.didit.me/standalone-apis/email-check)
**Feature Guide:** https://docs.didit.me/core-technology/email-verification/overview

---

## Authentication

All requests require an API key via the `x-api-key` header.

**How to obtain:** [Didit Business Console](https://business.didit.me) → API & Webhooks → Copy API key, or via programmatic registration (see below).

```
x-api-key: your_api_key_here
```

> `401` = API key missing or invalid. `403` = key lacks permissions or insufficient credits.

## Getting Started (No Account Yet?)

If you don't have a Didit API key, create one in 2 API calls:

1. **Register:** `POST https://apx.didit.me/auth/v2/programmatic/register/` with `{"email": "you@gmail.com", "password": "MyStr0ng!Pass"}`
2. **Check email** for a 6-character OTP code
3. **Verify:** `POST https://apx.didit.me/auth/v2/programmatic/verify-email/` with `{"email": "you@gmail.com", "code": "A3K9F2"}` → response includes `api_key`

**To add credits:** `GET /v3/billing/balance/` to check, `POST /v3/billing/top-up/` with `{"amount_in_dollars": 50}` for a Stripe checkout link.

See the **didit-verification-management** skill for full platform management (workflows, sessions, users, billing).

---

## Step 1: Send Email Code

Sends a one-time verification code to the specified email address.

### Request

```
POST https://verification.didit.me/v3/email/send/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `application/json` | **Yes** |

### Body (JSON)

| Parameter | Type | Required | Default | Constraints | Description |
|---|---|---|---|---|---|
| `email` | string | **Yes** | — | Valid email | Email address to send code to |
| `options.code_size` | integer | No | `6` | Min: 4, Max: 8 | Length of the verification code |
| `options.alphanumeric_code` | boolean | No | `false` | — | `true` = A-Z + 0-9 (case-insensitive) |
| `options.locale` | string | No | — | Max 5 chars | Locale for email template. e.g. `en-US` |
| `signals.ip` | string | No | — | IPv4 or IPv6 | User's IP for fraud detection |
| `signals.device_id` | string | No | — | Max 255 chars | Unique device identifier |
| `signals.user_agent` | string | No | — | Max 512 chars | Browser/client user agent |
| `vendor_data` | string | No | — | — | Your identifier for session tracking |

### Example

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/email/send/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "email": "user@example.com",
        "options": {"code_size": 6},
        "signals": {"ip": "203.0.113.42"},
        "vendor_data": "session-abc-123",
    },
)
print(response.status_code, response.json())
```

```typescript
const response = await fetch("https://verification.didit.me/v3/email/send/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "user@example.com",
    options: { code_size: 6 },
    signals: { ip: "203.0.113.42" },
  }),
});
```

### Response (200 OK)

```json
{
  "request_id": "e39cb057-92fc-4b59-b84e-02fec29a0f24",
  "status": "Success",
  "reason": null
}
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Success"` | Code sent | Proceed — wait for user to provide code, then call Check |
| `"Retry"` | Temporary delivery issue | Wait a few seconds and retry Send (max 2 retries) |
| `"Undeliverable"` | Email cannot receive mail | Inform user the email is invalid or cannot receive messages |

### Error Responses

| Code | Meaning | Action |
|---|---|---|
| `400` | Invalid request body or email | Check email format and parameter constraints |
| `401` | Invalid or missing API key | Verify `x-api-key` header |
| `403` | Insufficient credits/permissions | Check credits in Business Console |
| `429` | Rate limited | Back off and retry after indicated period |

---

## Step 2: Check Email Code

Verifies the code the user received. **Must be called after a successful Send.** Optionally auto-declines risky emails.

### Request

```
POST https://verification.didit.me/v3/email/check/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `application/json` | **Yes** |

### Body (JSON)

| Parameter | Type | Required | Default | Values | Description |
|---|---|---|---|---|---|
| `email` | string | **Yes** | — | Valid email | Same email used in Step 1 |
| `code` | string | **Yes** | — | 4-8 chars | The code the user received |
| `duplicated_email_action` | string | No | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | Decline if email already verified by another user |
| `breached_email_action` | string | No | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | Decline if email found in data breaches |
| `disposable_email_action` | string | No | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | Decline if email is disposable/temporary |
| `undeliverable_email_action` | string | No | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | Decline if email is undeliverable |

> **Policy note:** When an action is `"DECLINE"`, verification is rejected even if the code is correct. The `email.*` fields are still populated so you can inspect why.

### Example

```python
response = requests.post(
    "https://verification.didit.me/v3/email/check/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "email": "user@example.com",
        "code": "123456",
        "breached_email_action": "DECLINE",
        "disposable_email_action": "DECLINE",
    },
)
```

```typescript
const response = await fetch("https://verification.didit.me/v3/email/check/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "user@example.com",
    code: "123456",
    breached_email_action: "DECLINE",
    disposable_email_action: "DECLINE",
  }),
});
```

### Response (200 OK)

```json
{
  "request_id": "e39cb057-92fc-4b59-b84e-02fec29a0f24",
  "status": "Approved",
  "message": "The verification code is correct.",
  "email": {
    "status": "Approved",
    "email": "user@example.com",
    "is_breached": false,
    "breaches": [],
    "is_disposable": false,
    "is_undeliverable": false,
    "verification_attempts": 1,
    "verified_at": "2025-09-15T17:36:19.963451Z",
    "warnings": [],
    "lifecycle": [
      {"type": "EMAIL_VERIFICATION_MESSAGE_SENT", "timestamp": "...", "fee": 0.03},
      {"type": "VALID_CODE_ENTERED", "timestamp": "...", "fee": 0}
    ]
  },
  "created_at": "2025-09-15T17:36:19.703719+00:00"
}
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Approved"` | Code correct, no policy violations | Email verified — proceed with your flow |
| `"Failed"` | Code incorrect | Ask user to re-enter. After 3 failures, resend a new code |
| `"Declined"` | Code correct but policy violation | Inform user. Check `email.warnings` for reason |
| `"Expired or Not Found"` | No pending code | Code expired (>5 min) or Send was never called. Resend |

### Error Responses

| Code | Meaning | Action |
|---|---|---|
| `400` | Invalid request body | Check email and code format |
| `401` | Invalid or missing API key | Verify `x-api-key` header |
| `403` | Insufficient credits/permissions | Check credits in Business Console |
| `404` | Code expired or not found | Resend a new code via Step 1 |

---

## Response Field Reference

### `email` Object

| Field | Type | Description |
|---|---|---|
| `status` | string | `"Approved"`, `"Failed"`, `"Declined"` |
| `email` | string | The email address verified |
| `is_breached` | boolean | Found in known data breaches |
| `breaches` | array | Breach details: `{name, domain, breach_date, data_classes, breach_emails_count}` |
| `is_disposable` | boolean | From a disposable/temporary provider |
| `is_undeliverable` | boolean | Cannot receive email |
| `verification_attempts` | integer | Number of check attempts (max 3) |
| `verified_at` | string | ISO 8601 timestamp when verified (`null` if not) |
| `warnings` | array | Risk warnings: `{risk, log_type, short_description, long_description}` |
| `lifecycle` | array | Event log: `{type, timestamp, fee}` |

---

## Warning Tags

| Tag | Description | Auto-Decline |
|---|---|---|
| `EMAIL_CODE_ATTEMPTS_EXCEEDED` | Max code entry attempts exceeded | Yes |
| `EMAIL_IN_BLOCKLIST` | Email is in blocklist | Yes |
| `UNDELIVERABLE_EMAIL_DETECTED` | Email cannot be delivered | Yes |
| `BREACHED_EMAIL_DETECTED` | Found in known data breaches | Configurable |
| `DISPOSABLE_EMAIL_DETECTED` | Disposable/temporary provider | Configurable |
| `DUPLICATED_EMAIL` | Already verified by another user | Configurable |

Warning severity levels: `error` (critical), `warning` (requires attention), `information` (informational).

---

## Common Workflows

### Basic Email Verification

```
1. POST /v3/email/send/   → {"email": "user@example.com"}
2. Wait for user to provide the code
3. POST /v3/email/check/  → {"email": "user@example.com", "code": "123456"}
4. If "Approved"            → email is verified
   If "Failed"              → ask user to retry (up to 3 attempts)
   If "Expired or Not Found"→ go back to step 1
```

### Strict Security Verification

```
1. POST /v3/email/send/   → include signals.ip, signals.device_id, signals.user_agent
2. Wait for user to provide the code
3. POST /v3/email/check/  → set all *_action fields to "DECLINE"
4. If "Approved"  → safe to proceed
   If "Declined" → check email.warnings for reason, block or warn user
```

---

## Utility Scripts

**verify_email.py**: Send and check email verification codes from the command line.

```bash
# Requires: pip install requests
export DIDIT_API_KEY="your_api_key"

python scripts/verify_email.py send user@example.com
python scripts/verify_email.py check user@example.com 123456 --decline-breached --decline-disposable
```

Can also be imported as a library:

```python
from scripts.verify_email import send_code, check_code

send_result = send_code("user@example.com")
check_result = check_code("user@example.com", "123456", decline_breached=True)
```
