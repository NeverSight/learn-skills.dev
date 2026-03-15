---
name: didit-kyc-onboarding
description: >
  End-to-end KYC (Know Your Customer) identity verification for onboarding real users.
  Use when someone needs to perform KYC, onboard users with identity verification, verify
  a person's identity with ID scan and selfie, run a full KYC flow, create a verification
  session for a user, set up ID + liveness + face match verification, or implement user
  onboarding with document and biometric checks. Creates a KYC workflow, generates a
  verification URL, and retrieves the decision.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "✅"
    homepage: https://docs.didit.me
---

# Running KYC with Didit

End-to-end Know Your Customer (KYC) verification. This skill creates a KYC workflow, generates a session URL where a real user completes ID scan + selfie + face match, and retrieves the verification decision.

**What the user experiences:**
1. Receives a verification link
2. Scans their ID document (passport, ID card, driver's license)
3. Takes a live selfie
4. System auto-matches selfie to document photo
5. Gets approved, declined, or flagged for review

**API Reference:**
- Workflows: https://docs.didit.me/management-api/workflows/create
- Sessions: https://docs.didit.me/sessions-api/create-session
- Decisions: https://docs.didit.me/sessions-api/retrieve-session
- Programmatic Registration: https://docs.didit.me/integration/programmatic-registration
- Full API Overview: https://docs.didit.me/sessions-api/management-api

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

## Quick Start — KYC in 3 API Calls

```python
import requests, time

API_KEY = "your_api_key"
headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
BASE = "https://verification.didit.me/v3"

# 1. Create a KYC workflow (one-time setup — reuse the workflow_id for all users)
workflow = requests.post(f"{BASE}/workflows/", headers=headers, json={
    "workflow_label": "KYC Onboarding",
    "workflow_type": "kyc",
    "is_liveness_enabled": True,
    "is_face_match_enabled": True,
    "face_match_score_decline_threshold": 50,
    "max_retry_attempts": 3,
}).json()
workflow_id = workflow["uuid"]

# 2. Create a session for a specific user
session = requests.post(f"{BASE}/session/", headers=headers, json={
    "workflow_id": workflow_id,
    "vendor_data": "user-abc-123",
    "callback": "https://yourapp.com/verification-done",
    "language": "en",
}).json()

print(f"Send user to: {session['url']}")
# User opens this URL → scans ID → takes selfie → done

# 3. Poll for the decision (or use webhooks)
while True:
    decision = requests.get(
        f"{BASE}/session/{session['session_id']}/decision/",
        headers={"x-api-key": API_KEY},
    ).json()
    status = decision["status"]
    if status in ("Approved", "Declined", "In Review"):
        break
    time.sleep(10)

print(f"Result: {status}")
if status == "Approved":
    id_data = decision["id_verifications"][0]
    print(f"Name: {id_data['first_name']} {id_data['last_name']}")
    print(f"DOB: {id_data['date_of_birth']}")
    print(f"Document: {id_data['document_type']} ({id_data['issuing_country']})")
```

---

## Step 1: Create a KYC Workflow

A workflow defines what checks run. Create one per use case and reuse it for all users.

```
POST https://verification.didit.me/v3/workflows/
```

**API Reference:** https://docs.didit.me/management-api/workflows/create

### Recommended KYC Configuration

| Parameter | Value | Why |
|---|---|---|
| `workflow_type` | `"kyc"` | Full KYC template with ID + selfie |
| `is_liveness_enabled` | `true` | Prevents spoofing (printed photos, screens) |
| `is_face_match_enabled` | `true` | Compares selfie to document photo |
| `face_match_score_decline_threshold` | `50` | Match below 50% → auto-decline |
| `is_aml_enabled` | `false` | Set `true` for sanctions/PEP screening (+cost) |
| `max_retry_attempts` | `3` | User can retry 3 times on failure |

### Response

```json
{
  "uuid": "d8d2fa2d-c69c-471c-b7bc-bc71512b43ef",
  "workflow_label": "KYC Onboarding",
  "workflow_type": "kyc",
  "features": ["ocr", "liveness", "face_match"],
  "total_price": "0.10",
  "workflow_url": "https://verify.didit.me/..."
}
```

Save `uuid` as your `workflow_id`.

---

## Step 2: Create a Session for Each User

Each user gets their own session. The session generates a unique URL where they complete verification.

```
POST https://verification.didit.me/v3/session/
```

**API Reference:** https://docs.didit.me/sessions-api/create-session

### Key Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `workflow_id` | uuid | **Yes** | From Step 1 |
| `vendor_data` | string | Recommended | Your user ID — links the session to your system |
| `callback` | url | Recommended | Redirect URL after verification. Didit appends `?verificationSessionId=...&status=...` |
| `language` | string | No | UI language (ISO 639-1). Auto-detected if omitted |
| `contact_details.email` | string | No | Pre-fill email for notification |
| `expected_details.first_name` | string | No | Triggers mismatch warning if document name differs |
| `expected_details.date_of_birth` | string | No | `YYYY-MM-DD` format |
| `metadata` | JSON string | No | Custom data stored with session |

### Response

```json
{
  "session_id": "11111111-2222-3333-4444-555555555555",
  "session_token": "abcdef123456",
  "url": "https://verify.didit.me/session/abcdef123456",
  "status": "Not Started",
  "workflow_id": "d8d2fa2d-..."
}
```

**Send the user to `url`** — this is where they complete verification (web or mobile).

---

## Step 3: Get the Decision

After the user completes verification, retrieve the results.

```
GET https://verification.didit.me/v3/session/{sessionId}/decision/
```

**API Reference:** https://docs.didit.me/sessions-api/retrieve-session

### Two Ways to Know When It's Ready

**Option A: Webhooks (recommended for production)**
Configure a webhook URL in [Business Console](https://business.didit.me) → API & Webhooks. Didit sends a POST with `session_id` and `status` when the decision is ready.

**Option B: Polling**
Poll `GET /v3/session/{id}/decision/` every 10–30 seconds. Check `status` — stop when it's `Approved`, `Declined`, or `In Review`.

### Decision Response Fields

```json
{
  "session_id": "...",
  "status": "Approved",
  "features": ["ID_VERIFICATION", "LIVENESS", "FACE_MATCH"],
  "id_verifications": [{
    "status": "Approved",
    "document_type": "PASSPORT",
    "issuing_country": "USA",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "document_number": "ABC123456",
    "expiry_date": "2030-06-01",
    "gender": "M",
    "nationality": "USA",
    "mrz": "P<USADOE<<JOHN<<<<<<<<<..."
  }],
  "liveness_checks": [{
    "status": "Approved",
    "method": "PASSIVE",
    "score": 92.5
  }],
  "face_matches": [{
    "status": "Approved",
    "score": 97.3
  }],
  "aml_screenings": [],
  "warnings": []
}
```

### Key Decision Statuses

| Status | Meaning | Action |
|---|---|---|
| `Approved` | All checks passed | User is verified |
| `Declined` | One or more checks failed | Check `warnings` for details |
| `In Review` | Borderline result | Manual review needed, or auto-decide via API |
| `Not Started` | User hasn't opened the link yet | Wait or remind user |
| `In Progress` | User is completing verification | Wait |
| `Expired` | Session expired (default: 7 days) | Create a new session |

---

## Optional: Post-Decision Actions

### Approve or Decline Manually

```
PATCH https://verification.didit.me/v3/session/{sessionId}/update-status/
```

**API Reference:** https://docs.didit.me/sessions-api/update-status

```python
requests.patch(f"{BASE}/session/{session_id}/update-status/",
    headers=headers,
    json={"new_status": "Approved", "comment": "Manual review passed"})
```

### Request Resubmission

If the ID photo was blurry, ask the user to redo just that step:

```python
requests.patch(f"{BASE}/session/{session_id}/update-status/",
    headers=headers,
    json={
        "new_status": "Resubmitted",
        "nodes_to_resubmit": [{"node_id": "feature_ocr", "feature": "OCR"}],
        "send_email": True,
        "email_address": "user@example.com",
    })
```

### Block Fraudulent Users

```python
requests.post(f"{BASE}/blocklist/add/",
    headers=headers,
    json={"session_id": session_id, "blocklist_face": True, "blocklist_document": True})
```

**API Reference:** https://docs.didit.me/sessions-api/blocklist/add

### Generate PDF Report

```python
response = requests.get(f"{BASE}/session/{session_id}/generate-pdf",
    headers={"x-api-key": API_KEY})
```

**API Reference:** https://docs.didit.me/sessions-api/generate-pdf

---

## KYC Workflow Variants

### KYC + AML Screening

Add sanctions/PEP screening to catch high-risk individuals:

```python
requests.post(f"{BASE}/workflows/", headers=headers, json={
    "workflow_type": "kyc",
    "is_liveness_enabled": True,
    "is_face_match_enabled": True,
    "is_aml_enabled": True,
    "aml_decline_threshold": 80,
})
```

### KYC + Phone + Email

Add contact verification to the flow:

```python
requests.post(f"{BASE}/workflows/", headers=headers, json={
    "workflow_type": "kyc",
    "is_liveness_enabled": True,
    "is_face_match_enabled": True,
    "is_phone_verification_enabled": True,
    "is_email_verification_enabled": True,
})
```

### KYC + NFC (Chip Reading)

For passports with NFC chips — highest assurance:

```python
requests.post(f"{BASE}/workflows/", headers=headers, json={
    "workflow_type": "kyc",
    "is_liveness_enabled": True,
    "is_face_match_enabled": True,
    "is_nfc_enabled": True,
})
```

---

## Utility Scripts

### run_kyc.py — Full KYC setup from the command line

```bash
# Requires: pip install requests
export DIDIT_API_KEY="your_api_key"

# Create a KYC workflow (one-time)
python scripts/run_kyc.py setup --label "My KYC" --liveness --face-match

# Create a session for a user
python scripts/run_kyc.py session --workflow-id <uuid> --vendor-data user-123

# Get the decision
python scripts/run_kyc.py decision <session_id>

# Full flow: create workflow + session in one command
python scripts/run_kyc.py full --vendor-data user-123 --callback https://myapp.com/done
```

Can also be imported:

```python
from scripts.run_kyc import setup_kyc_workflow, create_kyc_session, get_decision
```
