---
name: didit-liveness-detection
description: >
  Detects liveness from a single selfie image via the Didit standalone API. Use when
  checking if a person is physically present, detecting spoofing or presentation attacks,
  implementing anti-spoofing measures, or performing passive liveness verification.
  Returns liveness score, face quality, and luminance metrics. 99.9% accuracy.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🧑"
    homepage: https://docs.didit.me
---

# Didit Passive Liveness API

## Overview

Verifies that a user is physically present by analyzing a single captured image — no explicit movement or interaction required.

**Key constraints:**
- Supported formats: **JPEG, PNG, WebP, TIFF**
- Maximum file size: **5MB**
- Image must contain **exactly one clearly visible face**
- Original real-time photo only (no screenshots or printed photos)

**Accuracy:** 99.9% liveness detection accuracy, <0.1% false acceptance rate (FAR).

**Capabilities:** Liveness scoring, face quality assessment, luminance analysis, age/gender estimation, spoof detection (screen captures, printed copies, masks, deepfakes), duplicate face detection across sessions, blocklist matching.

**Liveness methods:** This standalone endpoint uses `PASSIVE` method (single-frame CNN). Workflow mode also supports `ACTIVE_3D` (action + flash, highest security) and `FLASHING` (3D flash, high security).

**API Reference:** https://docs.didit.me/standalone-apis/passive-liveness
**Feature Guide:** https://docs.didit.me/core-technology/liveness/overview

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
POST https://verification.didit.me/v3/passive-liveness/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `multipart/form-data` | **Yes** |

### Request Parameters (multipart/form-data)

| Parameter | Type | Required | Default | Constraints | Description |
|---|---|---|---|---|---|
| `user_image` | file | **Yes** | — | JPEG/PNG/WebP/TIFF, max 5MB | User's face image |
| `face_liveness_score_decline_threshold` | integer | No | — | 0-100 | Scores below this = Declined |
| `rotate_image` | boolean | No | — | — | Try rotations to find upright face |
| `save_api_request` | boolean | No | `true` | — | Save in Business Console |
| `vendor_data` | string | No | — | — | Your identifier for session tracking |

### Example

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/passive-liveness/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={"user_image": ("selfie.jpg", open("selfie.jpg", "rb"), "image/jpeg")},
    data={"face_liveness_score_decline_threshold": "80"},
)
```

```typescript
const formData = new FormData();
formData.append("user_image", selfieFile);
formData.append("face_liveness_score_decline_threshold", "80");

const response = await fetch("https://verification.didit.me/v3/passive-liveness/", {
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
    "score": 95,
    "user_image": {
      "entities": [
        {"age": 22.16, "bbox": [156, 234, 679, 898], "confidence": 0.717, "gender": "male"}
      ],
      "best_angle": 0
    },
    "warnings": [],
    "face_quality": 85.0,
    "face_luminance": 50.0
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Approved"` | User is physically present | Proceed with your flow |
| `"Declined"` | Liveness check failed | Check `warnings`. May be a spoof or poor image quality |

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
| `status` | string | `"Approved"` or `"Declined"` |
| `method` | string | Always `"PASSIVE"` for this endpoint |
| `score` | integer | 0-100 liveness confidence (higher = more likely real). `null` if no face |
| `face_quality` | float | 0-100 face image quality score. `null` if no face |
| `face_luminance` | float | Face luminance value. `null` if no face |
| `entities[].age` | float | Estimated age |
| `entities[].bbox` | array | Face bounding box `[x1, y1, x2, y2]` |
| `entities[].confidence` | float | Face detection confidence (0-1) |
| `entities[].gender` | string | `"male"` or `"female"` |
| `warnings` | array | `{risk, log_type, short_description, long_description}` |

---

## Warning Tags

### Auto-Decline (always)

| Tag | Description |
|---|---|
| `NO_FACE_DETECTED` | No face detected in image |
| `LIVENESS_FACE_ATTACK` | Potential spoofing attempt (printed photo, screen, mask) |
| `FACE_IN_BLOCKLIST` | Face matches a blocklisted entry |
| `POSSIBLE_FACE_IN_BLOCKLIST` | Possible blocklist match detected |

### Configurable (Decline / Review / Approve)

| Tag | Description | Notes |
|---|---|---|
| `LOW_LIVENESS_SCORE` | Score below threshold | Configurable review + decline thresholds |
| `DUPLICATED_FACE` | Matches another approved session | — |
| `POSSIBLE_DUPLICATED_FACE` | May match another user | Configurable similarity threshold |
| `MULTIPLE_FACES_DETECTED` | Multiple faces (largest used for scoring) | Passive only |
| `LOW_FACE_QUALITY` | Image quality below threshold | Passive only |
| `LOW_FACE_LUMINANCE` | Image too dark | Passive only |
| `HIGH_FACE_LUMINANCE` | Image too bright/overexposed | Passive only |

---

## Common Workflows

### Basic Liveness Check

```
1. Capture user selfie
2. POST /v3/passive-liveness/ → {"user_image": selfie}
3. If "Approved" → user is real, proceed
   If "Declined" → check warnings:
     - NO_FACE_DETECTED → ask user to retake with face clearly visible
     - LOW_FACE_QUALITY → ask for better lighting/positioning
     - LIVENESS_FACE_ATTACK → flag as potential fraud
```

### Liveness + Face Match (combined)

```
1. POST /v3/passive-liveness/ → verify user is real
2. If Approved → POST /v3/face-match/ → compare selfie to ID photo
3. Both Approved → identity verified
```

---

## Utility Scripts

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/check_liveness.py selfie.jpg
python scripts/check_liveness.py selfie.jpg --threshold 80
```
