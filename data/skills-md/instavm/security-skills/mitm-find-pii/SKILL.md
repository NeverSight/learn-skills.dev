---
name: mitm-find-pii
description: Find PII (Personally Identifiable Information) leakage in API responses. Use when user asks about data exposure, privacy issues, or sensitive data in traffic.
---

# Find PII Leakage

Analyze the mitmproxy dump (log.txt) for PII exposure for: $ARGUMENTS

> **Requires**: `log.txt` in the current directory. If it's missing, capture traffic first:
> ```bash
> mitmdump --set flow_detail=3 2>&1 | tee log.txt
> ```

## PII Categories to Check

### 1. Contact Information
- Email addresses in responses
- Phone numbers (full or partial)
- Physical addresses

### 2. Financial Data
- Credit card numbers (even partial)
- Bank account details
- Transaction amounts
- Payment tokens

### 3. Identity Information
- Full names
- Date of birth
- Gender
- PAN/SSN/ID numbers

### 4. Authentication Data
- Passwords (plain or hashed)
- OTPs in responses
- Session tokens
- API keys

### 5. Behavioral Data
- Purchase history
- Browsing patterns
- Location data (lat/long)

## Red Flags

- PII returned without authentication
- PII in error responses
- PII leaked to third-party domains
- PII in GET parameters (logged in server logs)
- Unmasked data where masking expected

## Output Format

For each finding:
- **Endpoint**: Where PII is exposed
- **Data Type**: What PII is leaked
- **Sample**: Redacted example
- **Context**: Authenticated/Unauthenticated
- **Severity**: Based on sensitivity
- **Fix**: Mask, remove, or restrict access
