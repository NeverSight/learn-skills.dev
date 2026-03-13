---
name: didit-phone-verification
description: >
  Integrate Didit Phone Verification standalone API to verify phone numbers via OTP.
  Use when the user wants to verify phones, send SMS or WhatsApp or Telegram codes,
  check phone verification codes, detect disposable or VoIP numbers, or implement
  phone-based identity verification using Didit. Supports multiple delivery channels
  (SMS, WhatsApp, Telegram, voice), fraud signals, and policy-based auto-decline.
version: 1.3.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "📱"
    homepage: https://docs.didit.me
---

# Didit Phone Verification API

## Overview

Two-step phone verification via one-time code:

1. **Send** a verification code to a phone number
2. **Check** the code the user provides

**Key constraints:**
- Code expires after **5 minutes**
- Maximum **3 verification attempts** per code (then must resend)
- Maximum **2 resend requests** within 24 hours
- Rate limit: **4 sends per hour** per phone number
- Phone must be in **E.164 format** (e.g. `+14155552671`)
- You **must call Send before Check**

**Delivery channels:** SMS (default fallback), WhatsApp, Telegram, voice call. Falls back to SMS if preferred channel unavailable.

**Capabilities:** Detects disposable/temporary numbers, VoIP numbers, carrier info, and duplicate numbers. Supports fraud signals for risk scoring.

**API Reference:** [Send Code](https://docs.didit.me/standalone-apis/phone-send) | [Check Code](https://docs.didit.me/standalone-apis/phone-check)
**Feature Guide:** https://docs.didit.me/core-technology/phone-verification/overview

---

## Authentication

All requests require an API key via the `x-api-key` header.

**How to obtain:** [Didit Business Console](https://business.didit.me) → API & Webhooks → Copy API key, or via programmatic registration (see below).

```
x-api-key: your_api_key_here
```

## Getting Started (No Account Yet?)

If you don't have a Didit API key, create one in 2 API calls:

1. **Register:** `POST https://apx.didit.me/auth/v2/programmatic/register/` with `{"email": "you@gmail.com", "password": "MyStr0ng!Pass"}`
2. **Check email** for a 6-character OTP code
3. **Verify:** `POST https://apx.didit.me/auth/v2/programmatic/verify-email/` with `{"email": "you@gmail.com", "code": "A3K9F2"}` → response includes `api_key`

**To add credits:** `GET /v3/billing/balance/` to check, `POST /v3/billing/top-up/` with `{"amount_in_dollars": 50}` for a Stripe checkout link.

See the **didit-verification-management** skill for full platform management (workflows, sessions, users, billing).

---

## Step 1: Send Phone Code

### Request

```
POST https://verification.didit.me/v3/phone/send/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `application/json` | **Yes** |

### Body (JSON)

| Parameter | Type | Required | Default | Constraints | Description |
|---|---|---|---|---|---|
| `phone_number` | string | **Yes** | — | E.164 format | Phone number (e.g. `+14155552671`) |
| `options.code_size` | integer | No | `6` | Min: 4, Max: 8 | Code length |
| `options.locale` | string | No | — | Max 5 chars | Locale for message. e.g. `en-US` |
| `options.preferred_channel` | string | No | `"whatsapp"` | See channels | `"sms"`, `"whatsapp"`, `"telegram"`, `"voice"` |
| `signals.ip` | string | No | — | IPv4/IPv6 | User's IP for fraud detection |
| `signals.device_id` | string | No | — | Max 255 chars | Unique device identifier |
| `signals.device_platform` | string | No | — | Enum | `"android"`, `"ios"`, `"ipados"`, `"tvos"`, `"web"` |
| `signals.device_model` | string | No | — | Max 255 chars | e.g. `iPhone17,2` |
| `signals.os_version` | string | No | — | Max 64 chars | e.g. `18.0.1` |
| `signals.app_version` | string | No | — | Max 64 chars | e.g. `1.2.34` |
| `signals.user_agent` | string | No | — | Max 512 chars | Browser user agent |
| `vendor_data` | string | No | — | — | Your identifier for session tracking |

### Example

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/phone/send/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "phone_number": "+14155552671",
        "options": {"preferred_channel": "sms", "code_size": 6},
        "vendor_data": "session-abc-123",
    },
)
```

```typescript
const response = await fetch("https://verification.didit.me/v3/phone/send/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    phone_number: "+14155552671",
    options: { preferred_channel: "sms", code_size: 6 },
  }),
});
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Success"` | Code sent | Wait for user to provide code, then call Check |
| `"Retry"` | Temporary issue | Wait a few seconds and retry (max 2 retries) |
| `"Undeliverable"` | Number cannot receive messages | Inform user. Try a different number |
| `"Blocked"` | Number blocked (spam) | Use a different number |

### Error Responses

| Code | Meaning | Action |
|---|---|---|
| `400` | Invalid request body | Check phone format (E.164) and parameters |
| `401` | Invalid or missing API key | Verify `x-api-key` header |
| `403` | Insufficient credits/permissions | Check credits in Business Console |
| `429` | Rate limited (4/hour/number) | Wait for cooldown period |

---

## Step 2: Check Phone Code

**Must be called after a successful Send.** Optionally auto-declines risky numbers.

### Request

```
POST https://verification.didit.me/v3/phone/check/
```

### Body (JSON)

| Parameter | Type | Required | Default | Values | Description |
|---|---|---|---|---|---|
| `phone_number` | string | **Yes** | — | E.164 | Same phone used in Step 1 |
| `code` | string | **Yes** | — | 4-8 chars | The code the user received |
| `duplicated_phone_number_action` | string | No | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | Decline if already verified by another user |
| `disposable_number_action` | string | No | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | Decline disposable/temporary numbers |
| `voip_number_action` | string | No | `"NO_ACTION"` | `"NO_ACTION"` / `"DECLINE"` | Decline VoIP numbers |

### Example

```python
response = requests.post(
    "https://verification.didit.me/v3/phone/check/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "phone_number": "+14155552671",
        "code": "123456",
        "disposable_number_action": "DECLINE",
        "voip_number_action": "DECLINE",
    },
)
```

### Response (200 OK)

```json
{
  "request_id": "e39cb057-...",
  "status": "Approved",
  "message": "The verification code is correct.",
  "phone": {
    "status": "Approved",
    "phone_number_prefix": "+1",
    "phone_number": "4155552671",
    "full_number": "+14155552671",
    "country_code": "US",
    "country_name": "United States",
    "carrier": {"name": "ATT", "type": "mobile"},
    "is_disposable": false,
    "is_virtual": false,
    "verification_method": "sms",
    "verification_attempts": 1,
    "verified_at": "2025-08-24T09:12:39.662232Z",
    "warnings": [],
    "lifecycle": [...]
  }
}
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Approved"` | Code correct, no policy violations | Phone verified — proceed |
| `"Failed"` | Code incorrect | Ask user to retry (up to 3 attempts) |
| `"Declined"` | Code correct but policy violation | Check `phone.warnings` for reason |
| `"Expired or Not Found"` | No pending code | Resend via Step 1 |

---

## Response Field Reference

### `phone` Object

| Field | Type | Description |
|---|---|---|
| `status` | string | `"Approved"`, `"Failed"`, `"Declined"` |
| `phone_number_prefix` | string | Country prefix (e.g. `+1`) |
| `full_number` | string | Full E.164 number |
| `country_code` | string | ISO 3166-1 alpha-2 |
| `carrier.name` | string | Carrier name |
| `carrier.type` | string | `"mobile"`, `"landline"`, `"voip"`, `"unknown"` |
| `is_disposable` | boolean | Disposable/temporary number |
| `is_virtual` | boolean | VoIP number |
| `verification_method` | string | `"sms"`, `"whatsapp"`, `"telegram"`, `"voice"` |
| `verification_attempts` | integer | Check attempts made (max 3) |
| `warnings` | array | `{risk, log_type, short_description, long_description}` |

---

## Warning Tags

| Tag | Description | Auto-Decline |
|---|---|---|
| `VERIFICATION_CODE_ATTEMPTS_EXCEEDED` | Max code attempts exceeded | Yes |
| `PHONE_NUMBER_IN_BLOCKLIST` | Phone is in blocklist | Yes |
| `HIGH_RISK_PHONE_NUMBER` | Identified as high risk | Yes |
| `DISPOSABLE_NUMBER_DETECTED` | Temporary/disposable number | Configurable |
| `VOIP_NUMBER_DETECTED` | VoIP number detected | Configurable |
| `DUPLICATED_PHONE_NUMBER` | Already verified by another user | Configurable |

---

## Common Workflows

### Basic Phone Verification

```
1. POST /v3/phone/send/   → {"phone_number": "+14155552671"}
2. Wait for user to provide the code
3. POST /v3/phone/check/  → {"phone_number": "+14155552671", "code": "123456"}
4. If "Approved"            → phone is verified
   If "Failed"              → retry (up to 3 attempts)
   If "Expired or Not Found"→ resend (step 1)
```

### Strict Security Verification

```
1. POST /v3/phone/send/   → include signals.ip, signals.device_platform, channel: "sms"
2. POST /v3/phone/check/  → set disposable_number_action + voip_number_action to "DECLINE"
3. If "Declined" → check phone.warnings, block or warn user
```

---

## Utility Scripts

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/verify_phone.py send +14155552671 --channel sms
python scripts/verify_phone.py check +14155552671 123456 --decline-voip
```
