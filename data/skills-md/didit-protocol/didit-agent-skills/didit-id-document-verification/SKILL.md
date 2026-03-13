---
name: didit-id-document-verification
description: >
  Verifies identity documents via the Didit standalone API. Use when verifying a passport,
  ID card, driver's license, or residence permit, performing OCR extraction, MRZ parsing,
  document authenticity checks, or KYC document validation. Supports 4000+ document types
  across 220+ countries.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "📋"
    homepage: https://docs.didit.me
---

# Didit ID Verification API

## Overview

Verifies identity documents by submitting images of the front and back sides. Performs OCR extraction, MRZ parsing, authenticity checks, and document liveness detection.

**Key constraints:**
- Supported formats: **JPEG, PNG, WebP, TIFF**
- Maximum file size: **5MB** per image
- All document corners must be visible, full-color, no glare/shadows
- Original real-time photos only (no screenshots, scans, or digital copies)

**Coverage:** 4,000+ document types, 220+ countries, 130+ languages. Supports passports, national ID cards, driver's licenses, and residence permits.

**Processing pipeline:**
1. Intelligent capture & document type detection
2. OCR text extraction + MRZ/barcode parsing
3. Template matching, security feature validation, tamper detection
4. Document liveness (detects screen captures, printed copies, portrait manipulation)

**API Reference:** https://docs.didit.me/standalone-apis/id-verification
**Feature Guide:** https://docs.didit.me/core-technology/id-verification/overview
**Supported Documents:** https://docs.didit.me/core-technology/id-verification/supported-documents-id-verification

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
POST https://verification.didit.me/v3/id-verification/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `multipart/form-data` | **Yes** |

### Request Parameters (multipart/form-data)

| Parameter | Type | Required | Default | Constraints | Description |
|---|---|---|---|---|---|
| `front_image` | file | **Yes** | — | JPEG/PNG/WebP/TIFF, max 5MB | Front image of ID document |
| `back_image` | file | No | — | Same as above | Back image (when applicable) |
| `save_api_request` | boolean | No | `true` | — | Save in Business Console Manual Checks |
| `vendor_data` | string | No | — | — | Your identifier for session tracking |

### Example

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/id-verification/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={
        "front_image": ("front.jpg", open("front.jpg", "rb"), "image/jpeg"),
        "back_image": ("back.jpg", open("back.jpg", "rb"), "image/jpeg"),
    },
    data={"vendor_data": "user-123"},
)
```

```typescript
const formData = new FormData();
formData.append("front_image", frontImageFile);
formData.append("back_image", backImageFile);
formData.append("vendor_data", "user-123");

const response = await fetch("https://verification.didit.me/v3/id-verification/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### Response (200 OK)

```json
{
  "request_id": "a1b2c3d4-...",
  "id_verification": {
    "status": "Approved",
    "document_type": "Identity Card",
    "document_number": "YZA123456",
    "personal_number": "X9876543L",
    "first_name": "Elena",
    "last_name": "Martínez Sánchez",
    "full_name": "Elena Martínez Sánchez",
    "date_of_birth": "1985-03-15",
    "age": 40,
    "gender": "F",
    "nationality": "ESP",
    "issuing_state": "ESP",
    "issuing_state_name": "Spain",
    "expiration_date": "2030-08-21",
    "date_of_issue": "2020-08-21",
    "address": "Calle Mayor 10, Madrid",
    "formatted_address": "Calle Mayor 10, 28013 Madrid, Spain",
    "place_of_birth": "Valencia",
    "portrait_image": "<base64>",
    "front_document_image": "<base64>",
    "back_document_image": "<base64>",
    "mrz": {
      "surname": "MARTINEZ SANCHEZ",
      "given_name": "ELENA",
      "document_type": "I",
      "document_number": "YZA123456",
      "country": "ESP",
      "nationality": "ESP",
      "birth_date": "850315",
      "expiry_date": "300821",
      "sex": "F"
    },
    "parsed_address": {"city": "Madrid", "region": "...", "postal_code": "28013", "country": "ES"},
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### Status Values

| Status | Meaning |
|---|---|
| `"Approved"` | Document verified successfully |
| `"Declined"` | Verification failed (see `warnings`) |
| `"In Review"` | Requires manual review |

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
| `document_type` | string | `"Passport"`, `"Identity Card"`, `"Driver's License"`, `"Residence Permit"` |
| `document_number` | string | Document ID number |
| `personal_number` | string | Personal/national ID number |
| `first_name`, `last_name`, `full_name` | string | Extracted name fields |
| `date_of_birth` | string | `YYYY-MM-DD` |
| `age` | integer | Calculated age |
| `gender` | string | `"M"`, `"F"`, `"U"` |
| `nationality`, `issuing_state` | string | ISO 3166-1 alpha-3 |
| `expiration_date`, `date_of_issue` | string | `YYYY-MM-DD` |
| `portrait_image` | string | Base64-encoded portrait from document |
| `mrz` | object | Machine Readable Zone data |
| `parsed_address` | object | Geocoded address: `{city, region, postal_code, country, street_1}` |
| `warnings` | array | `{risk, log_type, short_description, long_description}` |

---

## Warning Tags

### Auto-Decline (always)

| Tag | Description |
|---|---|
| `ID_DOCUMENT_IN_BLOCKLIST` | Document in blocklist (previously flagged) |
| `PORTRAIT_IMAGE_NOT_DETECTED` | No portrait found on document |
| `DOCUMENT_EXPIRED` | Document expiration date has passed |
| `DOCUMENT_NOT_SUPPORTED_FOR_APPLICATION` | Document type not accepted |

### Configurable (Decline / Review / Approve)

| Category | Tags |
|---|---|
| **Document liveness** | `SCREEN_CAPTURE_DETECTED`, `PRINTED_COPY_DETECTED`, `PORTRAIT_MANIPULATION_DETECTED` |
| **MRZ issues** | `MRZ_NOT_DETECTED`, `MRZ_VALIDATION_FAILED`, `MRZ_AND_DATA_EXTRACTED_FROM_OCR_NOT_SAME` |
| **Data issues** | `NAME_NOT_DETECTED`, `DATE_OF_BIRTH_NOT_DETECTED`, `DOCUMENT_NUMBER_NOT_DETECTED`, `DATA_INCONSISTENT` |
| **Duplicates** | `POSSIBLE_DUPLICATED_USER` |
| **Expected mismatch** | `FULL_NAME_MISMATCH_WITH_PROVIDED`, `DOB_MISMATCH_WITH_PROVIDED`, `GENDER_MISMATCH_WITH_PROVIDED` |
| **Geolocation** | `DOCUMENT_COUNTRY_MISMATCH` |

---

## Common Workflows

### Basic ID Verification

```
1. POST /v3/id-verification/ → front_image (+ back_image if applicable)
2. If "Approved" → extract first_name, last_name, date_of_birth, document_number
   If "Declined" → check warnings:
     DOCUMENT_EXPIRED → ask for valid document
     SCREEN_CAPTURE_DETECTED → ask for real photo of physical document
     MRZ_VALIDATION_FAILED → ask for clearer image
```

### Full Identity Verification Pipeline

```
1. POST /v3/id-verification/ → verify document
2. POST /v3/passive-liveness/ → verify real person
3. POST /v3/face-match/ → compare selfie to document portrait
4. POST /v3/aml/ → screen extracted name/DOB/nationality
5. All Approved → fully verified identity
```

---

## Utility Scripts

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/verify_id.py front.jpg
python scripts/verify_id.py front.jpg back.jpg --vendor-data user-123
```
