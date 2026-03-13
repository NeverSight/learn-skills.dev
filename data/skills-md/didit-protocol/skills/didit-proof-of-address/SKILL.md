---
name: didit-proof-of-address
description: >
  Integrate Didit Proof of Address standalone API to verify address documents.
  Use when the user wants to verify a proof of address, validate utility bills,
  bank statements, government documents, extract address from documents, verify
  residential address, implement address verification, or perform PoA checks
  using Didit. Supports OCR extraction, geocoding, name matching, and multi-page documents.
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🏠"
    homepage: https://docs.didit.me
---

# Didit Proof of Address API

## Overview

Verifies address documents by submitting images or PDFs. Extracts address information, performs authenticity checks, name matching, geocoding, and returns structured data.

**Key constraints:**
- Supported formats: **JPG, JPEG, PNG, TIFF, PDF**
- Maximum file size: **15MB**
- Document must be **within 90 days** of issue date
- Full-color, all corners visible, no digital editing
- Must be different from the ID document used for ID verification

**Capabilities:** OCR extraction, intelligent document classification, name matching with identity documents, issue date validation, geocoding with lat/lng coordinates, language detection, multi-page support.

**Accepted document types:**

| Category | Examples |
|---|---|
| Utility Bill | Electricity, water, gas, internet, phone, combined utilities |
| Bank Statement | Account statement, credit card, mortgage, loan |
| Government-Issued | Tax assessment, residency certificate, voter registration |
| Other PoA | Lease, rental agreement, insurance policy, employer letter |

**API Reference:** https://docs.didit.me/standalone-apis/proof-of-address
**Feature Guide:** https://docs.didit.me/core-technology/proof-of-address/overview

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
POST https://verification.didit.me/v3/poa/
```

### Headers

| Header | Value | Required |
|---|---|---|
| `x-api-key` | Your API key | **Yes** |
| `Content-Type` | `multipart/form-data` | **Yes** |

### Request Parameters (multipart/form-data)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `document` | file | **Yes** | — | PoA document (JPG/PNG/TIFF/PDF, max 15MB) |
| `save_api_request` | boolean | No | `true` | Save in Business Console |
| `vendor_data` | string | No | — | Your identifier for session tracking |

### Example

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/poa/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={"document": ("utility_bill.pdf", open("bill.pdf", "rb"), "application/pdf")},
    data={"vendor_data": "user-123"},
)
print(response.json())
```

```typescript
const formData = new FormData();
formData.append("document", documentFile);

const response = await fetch("https://verification.didit.me/v3/poa/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### Response (200 OK)

```json
{
  "request_id": "a1b2c3d4-...",
  "poa": {
    "status": "Approved",
    "issuing_state": "ESP",
    "document_type": "UTILITY_BILL",
    "issuer": "Endesa",
    "issue_date": "2025-01-15",
    "document_language": "es",
    "name_on_document": "Elena Martínez Sánchez",
    "poa_address": "Calle Mayor 10, 28013 Madrid",
    "poa_formatted_address": "Calle Mayor 10, 28013 Madrid, Spain",
    "poa_parsed_address": {
      "street_1": "Calle Mayor 10",
      "city": "Madrid",
      "region": "Comunidad de Madrid",
      "postal_code": "28013",
      "raw_results": {
        "geometry": {"location": {"lat": 40.4168, "lng": -3.7038}}
      }
    },
    "document_file": "https://example.com/document.pdf",
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### Status Values & Handling

| Status | Meaning | Action |
|---|---|---|
| `"Approved"` | Address verified, document valid | Proceed with your flow |
| `"Declined"` | Document invalid or expired | Check `warnings` for specific reason |
| `"In Review"` | Needs manual review | Check for name mismatch or quality issues |
| `"Not Finished"` | Processing incomplete | Wait or retry |

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
| `issuing_state` | string | ISO 3166-1 alpha-3 country code |
| `document_type` | string | `"UTILITY_BILL"`, `"BANK_STATEMENT"`, `"GOVERNMENT_ISSUED_DOCUMENT"`, `"OTHER_POA_DOCUMENT"`, `"UNKNOWN"` |
| `issuer` | string | Issuing institution name |
| `issue_date` | string | `YYYY-MM-DD` |
| `document_language` | string | Detected language code |
| `name_on_document` | string | Extracted name |
| `poa_address` | string | Raw extracted address |
| `poa_formatted_address` | string | Formatted address |
| `poa_parsed_address` | object | `{street_1, street_2, city, region, postal_code}` |
| `poa_parsed_address.raw_results.geometry.location` | object | `{lat, lng}` geocoded coordinates |
| `document_file` | string | Temporary URL (expires **60 min**) |
| `warnings` | array | `{risk, log_type, short_description, long_description}` |

---

## Warning Tags

### Auto-Decline

| Tag | Description |
|---|---|
| `POA_DOCUMENT_NOT_SUPPORTED_FOR_APPLICATION` | Document type not accepted for your app |
| `EXPIRED_DOCUMENT` | Document older than 90 days |
| `INVALID_DOCUMENT_TYPE` | Document cannot be processed |
| `MISSING_ADDRESS_INFORMATION` | No valid address could be extracted |

### Configurable (Decline / Review / Approve)

| Tag | Description |
|---|---|
| `NAME_MISMATCH_WITH_PROVIDED` | Name doesn't match verified identity |
| `NAME_MISMATCH_ID_VERIFICATION` | Name doesn't match ID document |
| `POA_NAME_MISMATCH_BETWEEN_DOCUMENTS` | Names differ between multiple PoA docs |
| `POOR_DOCUMENT_QUALITY` | Insufficient image quality |
| `DOCUMENT_METADATA_MISMATCH` | Digital signature/metadata indicates tampering |
| `SUSPECTED_DOCUMENT_MANIPULATION` | Signs of document manipulation |
| `UNSUPPORTED_DOCUMENT_LANGUAGE` | Document language not supported |
| `ADDRESS_MISMATCH_WITH_PROVIDED` | Address doesn't match provided address |
| `UNABLE_TO_EXTRACT_ISSUE_DATE` | Could not determine issue date |
| `ISSUER_NOT_IDENTIFIED` | Could not identify issuing institution |
| `UNPARSABLE_OR_INVALID_ADDRESS` | Address couldn't be parsed |
| `UNABLE_TO_VALIDATE_DOCUMENT_AGE` | Could not determine document age |
| `FUTURE_ISSUE_DATE` | Issue date is in the future |

Warning severity: `error` (→ Declined), `warning` (→ In Review), `information` (no effect).

---

## Common Workflows

### Basic Address Verification

```
1. POST /v3/poa/ → {"document": utility_bill}
2. If "Approved" → address verified
   If "Declined" → check warnings:
     EXPIRED_DOCUMENT → ask for a more recent document
     MISSING_ADDRESS_INFORMATION → ask for clearer image
     NAME_MISMATCH → verify identity matches
```

### Full KYC with Address

```
1. POST /v3/id-verification/ → verify identity document
2. POST /v3/passive-liveness/ → verify real person
3. POST /v3/poa/ → verify address
4. System auto-matches name between ID and PoA documents
5. All Approved → identity + address verified
```

---

## Utility Scripts

**verify_address.py**: Verify proof of address documents from the command line.

```bash
# Requires: pip install requests
export DIDIT_API_KEY="your_api_key"
python scripts/verify_address.py utility_bill.pdf
python scripts/verify_address.py bank_statement.jpg --vendor-data user-123
```
