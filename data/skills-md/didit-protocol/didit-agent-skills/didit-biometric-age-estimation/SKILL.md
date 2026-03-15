---
name: didit-biometric-age-estimation
description: >
  Estimates a person's age from a facial image via the Didit standalone API. Use when
  implementing age gating, checking if someone is over 18 or 21, performing age verification
  for compliance, or detecting underage users. Includes passive liveness check. Supports
  configurable thresholds, adaptive fallback to ID verification, and per-country restrictions.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🎂"
    homepage: https://docs.didit.me
---

# Didit Age Estimation API

## Overview

Estimates a person's age from a facial image using deep learning. Also performs a passive liveness check to prevent spoofing.

**Key constraints:**
- Supported formats: **JPEG, PNG, WebP, TIFF**
- Maximum file size: **5MB**
- Image must contain **one clearly visible face**
- Accuracy: MAE ±3.5 years overall; ±1.5 years for under-18

**Capabilities:** Age estimation with confidence scoring, gender estimation, passive liveness detection, configurable age thresholds, per-country age restrictions, adaptive mode with ID verification fallback for borderline cases.

**Liveness methods (workflow mode):**

| Method | Security | Best For |
|---|---|---|
| `ACTIVE_3D` (Action + Flash) | Highest | Banking, government, healthcare |
| `FLASHING` (3D Flash) | High | Financial services, identity verification |
| `PASSIVE` (single-frame CNN) | Standard | Low-friction consumer apps |

**API Reference:** https://docs.didit.me/standalone-apis/age-estimation
**Feature Guide:** https://docs.didit.me/core-technology/age-estimation/overview

---

## Authentication

All requests require `x-api-key` header. Get your key from [Didit Business Console](https://business.didit.me) → API & Webhooks, or via programmatic registration (see below).

## Getting Started (No Account Yet?)

If you don't have a Didit API key, create one in 2 API calls:

1. **Register:** `POST https://apx.didit.me/auth/v2/programmatic/register/` with `{"email": "you@gmail.com", "password": "MyStr0ng!Pass"}`
2. **Check email** for a 6-character OTP code
3. **Verify:** `POST https://apx.didit.me/auth/v2/programmatic/verify-email/` with `{"email": "you@gmail.com", "code": "A3K9F2"}` → response includes `api_key`

**To add credits:** `GET /v3/billing/balance/` to check, `POST /v3/billing/top-up/` with `{"amount_in_dollars": 50}` for a Stripe checkout link.

See the **didit-verification-management** skill for full platform management (workflows, sessions, users, billing).

---

## Endpoint

```
POST https://verification.didit.me/v3/age-estimation/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `multipart/form-data` | **Yes** |

### Request Parameters (multipart/form-data)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `user_image` | file | **Yes** | — | Facial image (JPEG/PNG/WebP/TIFF, max 5MB) |
| `rotate_image` | boolean | No | `false` | Try 0/90/180/270 rotations for non-upright faces |
| `save_api_request` | boolean | No | `true` | Save in Business Console Manual Checks |
| `vendor_data` | string | No | — | Your identifier for session tracking |

### Example

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/age-estimation/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={"user_image": ("selfie.jpg", open("selfie.jpg", "rb"), "image/jpeg")},
    data={"vendor_data": "user-123"},
)
print(response.json())
```

```typescript
const formData = new FormData();
formData.append("user_image", selfieFile);

const response = await fetch("https://verification.didit.me/v3/age-estimation/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### Response (200 OK)

```json
{
  "request_id": "a1b2c3d4-...",
  "liveness": {
    "status": "Approved",
    "method": "PASSIVE",
    "score": 89.92,
    "age_estimation": 24.3,
    "reference_image": "https://example.com/reference.jpg",
    "video_url": null,
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Approved"` | Age verified above threshold, liveness passed | Proceed with your flow |
| `"Declined"` | Age below minimum or liveness failed | Check `warnings` for specifics |
| `"In Review"` | Borderline case, needs review | Trigger ID verification fallback or manual review |

### Error Responses

| Code | Meaning | Action |
|---|---|---|
| `400` | Invalid request | Check file format, size, parameters |
| `401` | Invalid API key | Verify `x-api-key` header |
| `403` | Insufficient credits | Top up at business.didit.me |

---

## Response Field Reference

| Field | Type | Description |
|---|---|---|
| `status` | string | `"Approved"`, `"Declined"`, `"In Review"`, `"Not Finished"` |
| `method` | string | `"ACTIVE_3D"`, `"FLASHING"`, or `"PASSIVE"` |
| `score` | float | 0-100 liveness confidence score |
| `age_estimation` | float | Estimated age in years (e.g. `24.3`). `null` if no face |
| `reference_image` | string | Temporary URL (expires 60 min) |
| `video_url` | string | Temporary URL for active liveness video. `null` for passive |
| `warnings` | array | `{risk, log_type, short_description, long_description}` |

### Accuracy by Age Range

| Age Range | MAE (years) | Confidence |
|---|---|---|
| Under 18 | 1.5 | High |
| 18-25 | 2.8 | High |
| 26-40 | 3.2 | High |
| 41-60 | 3.9 | Medium-High |
| 60+ | 4.5 | Medium |

---

## Warning Tags

### Auto-Decline

| Tag | Description |
|---|---|
| `NO_FACE_DETECTED` | No face found in image |
| `LIVENESS_FACE_ATTACK` | Spoofing attempt detected |
| `FACE_IN_BLOCKLIST` | Face matches a blocklist entry |

### Configurable (Decline / Review / Approve)

| Tag | Description |
|---|---|
| `AGE_BELOW_MINIMUM` | Estimated age below configured minimum |
| `AGE_NOT_DETECTED` | Unable to estimate age (image quality, lighting) |
| `LOW_LIVENESS_SCORE` | Liveness score below threshold |
| `POSSIBLE_DUPLICATED_FACE` | Significant similarity with previously verified face |

Warning severity: `error` (→ Declined), `warning` (→ In Review), `information` (no effect).

---

## Common Workflows

### Basic Age Gate

```
1. Capture user selfie
2. POST /v3/age-estimation/ → {"user_image": selfie}
3. Check liveness.age_estimation >= your_minimum_age
4. If "Approved" → user meets age requirement
   If "Declined" → check warnings for AGE_BELOW_MINIMUM or liveness failure
```

### Adaptive Age Estimation (Workflow Mode)

Uses `workflow_type: "adaptive_age_verification"` — creates a session where borderline ages trigger automatic ID verification fallback.

```
1. POST /v3/workflows/ → {"workflow_type": "adaptive_age_verification", "is_liveness_enabled": true, "is_age_restrictions_enabled": true}
2. POST /v3/session/ → create session with the workflow_id from step 1
3. User takes selfie → system estimates age
4. Clear pass (well above threshold) → Approved instantly
   Clear fail (well below threshold) → Declined
   Borderline case → automatic ID verification fallback
5. If ID fallback triggered: per-country age restrictions apply
```

### Per-Country Age Restrictions

Configure in Console per issuing country:

| Country | Min Age | Overrides |
|---|---|---|
| USA | 18 | Mississippi: 21, Alabama: 19 |
| KOR | 19 | — |
| GBR | 18 | — |
| ARE | 21 | — |

> Use "Apply age of majority" button in Console to auto-populate defaults.

---

## Utility Scripts

**estimate_age.py**: Estimate age from a facial image via the command line.

```bash
# Requires: pip install requests
export DIDIT_API_KEY="your_api_key"
python scripts/estimate_age.py selfie.jpg
python scripts/estimate_age.py photo.png --threshold 21 --vendor-data user-123
```
