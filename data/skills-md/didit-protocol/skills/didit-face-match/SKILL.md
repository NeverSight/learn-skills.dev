---
name: didit-face-match
description: >
  Integrate Didit Face Match standalone API to compare two facial images.
  Use when the user wants to compare faces, verify face identity, implement biometric
  comparison, facial recognition, or selfie-to-document matching using Didit.
  Returns a similarity score (0-100) with configurable decline threshold.
  Supports image rotation and multi-face detection.
version: 1.3.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "👥"
    homepage: https://docs.didit.me
---

# Didit Face Match API

## Overview

Compares two facial images to determine if they belong to the same person. Returns a similarity score (0-100).

**Key constraints:**
- Supported formats: **JPEG, PNG, WebP, TIFF**
- Maximum file size: **5MB** per image
- If multiple faces in an image, the **largest face** is used for comparison
- Both `user_image` and `ref_image` are **required**

**Capabilities:** Similarity scoring, age estimation, gender detection, face bounding boxes, configurable decline threshold, optional image rotation for non-upright faces.

**API Reference:** https://docs.didit.me/standalone-apis/face-match
**Feature Guide:** https://docs.didit.me/core-technology/face-match/overview

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
POST https://verification.didit.me/v3/face-match/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `multipart/form-data` | **Yes** |

### Request Parameters (multipart/form-data)

| Parameter | Type | Required | Default | Constraints | Description |
|---|---|---|---|---|---|
| `user_image` | file | **Yes** | — | JPEG/PNG/WebP/TIFF, max 5MB | User's face image to verify |
| `ref_image` | file | **Yes** | — | Same as above | Reference image to compare against |
| `face_match_score_decline_threshold` | integer | No | `30` | 0-100 | Scores below this = Declined |
| `rotate_image` | boolean | No | `false` | — | Try 0/90/180/270 degree rotations to find upright face |
| `save_api_request` | boolean | No | `true` | — | Save in Business Console Manual Checks |
| `vendor_data` | string | No | — | — | Your identifier for session tracking |

### Example

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/face-match/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={
        "user_image": ("selfie.jpg", open("selfie.jpg", "rb"), "image/jpeg"),
        "ref_image": ("id_photo.jpg", open("id_photo.jpg", "rb"), "image/jpeg"),
    },
    data={"face_match_score_decline_threshold": "50"},
)
```

```typescript
const formData = new FormData();
formData.append("user_image", selfieFile);
formData.append("ref_image", referenceFile);
formData.append("face_match_score_decline_threshold", "50");

const response = await fetch("https://verification.didit.me/v3/face-match/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### Response (200 OK)

```json
{
  "request_id": "a1b2c3d4-...",
  "face_match": {
    "status": "Approved",
    "score": 80,
    "user_image": {
      "entities": [
        {"age": 27.63, "bbox": [40, 40, 100, 100], "confidence": 0.717, "gender": "male"}
      ],
      "best_angle": 0
    },
    "ref_image": {
      "entities": [
        {"age": 22.16, "bbox": [156, 234, 679, 898], "confidence": 0.717, "gender": "male"}
      ],
      "best_angle": 0
    },
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Approved"` | Score >= threshold | Faces match — proceed |
| `"Declined"` | Score < threshold or no face | Check `warnings` for details. May need better image |
| `"In Review"` | Needs manual review | Wait for review or retrieve via session API |

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
| `status` | string | `"Approved"`, `"Declined"`, `"In Review"` |
| `score` | integer | 0-100 similarity score (higher = more similar). `null` if no face found |
| `entities[].age` | float | Estimated age |
| `entities[].bbox` | array | Face bounding box `[x1, y1, x2, y2]` |
| `entities[].confidence` | float | Face detection confidence (0-1) |
| `entities[].gender` | string | `"male"` or `"female"` |
| `best_angle` | integer | Best rotation angle for the face |
| `warnings` | array | `{risk, log_type, short_description, long_description}` |

---

## Warning Tags

| Tag | Description | Auto-Decline |
|---|---|---|
| `NO_REFERENCE_IMAGE` | Reference or face image missing | Yes |
| `NO_FACE_DETECTED` | No face detected in one or both images | Yes |
| `LOW_FACE_MATCH_SIMILARITY` | Score below threshold — potential identity mismatch | Configurable |

> **Security best practice:** Only store the status and score. Minimize biometric image data on your servers. Image URLs (in workflow mode) expire after 60 minutes.

---

## Score Interpretation

| Score Range | Interpretation | Action |
|---|---|---|
| 90-100 | Very high confidence — same person | Auto-approve |
| 70-89 | High confidence — likely same person | Approve (default threshold 30) |
| 50-69 | Moderate — possible match | Consider manual review |
| 30-49 | Low — likely different people | Declined at default threshold |
| 0-29 | Very low — different people | Declined |

---

## Utility Scripts

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/match_faces.py selfie.jpg id_photo.jpg
python scripts/match_faces.py selfie.jpg id_photo.jpg --threshold 50 --rotate
```
