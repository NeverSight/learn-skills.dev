---
name: mitm-find-otp
description: Find OTP implementation vulnerabilities. Use when user asks about OTP security, verification bypass, SMS security, or two-factor authentication issues.
---

# Find OTP Vulnerabilities

Analyze the mitmproxy dump (log.txt) for OTP issues for: $ARGUMENTS

> **Requires**: `log.txt` in the current directory. If it's missing, capture traffic first:
> ```bash
> mitmdump --set flow_detail=3 2>&1 | tee log.txt
> ```

## Vulnerability Types

### 1. OTP in Response
- OTP returned in API response body
- OTP in page source/JavaScript
- OTP in error messages
- Should only be sent via SMS/email, never in API response

### 2. No Rate Limiting
- Unlimited OTP generation requests
- Unlimited verification attempts
- Can brute force 4-6 digit OTP

### 3. OTP Bypass
- Response manipulation bypasses OTP
- Changing `verified: false` to `verified: true`
- Empty OTP accepted
- Old OTP still valid

### 4. Predictable OTP
- Sequential OTPs
- Timestamp-based OTPs
- Same OTP for multiple requests

### 5. OTP Leakage
- OTP in URL parameters (logged)
- OTP visible in function names in source
- OTP sent in GET request

## Testing Approach

```bash
# Check for OTP in response
curl -X POST "https://target.com/api/send-otp" \
  -d "phone=1234567890" | grep -i otp

# Test rate limiting
for i in {1..20}; do
  curl -X POST "https://target.com/api/verify-otp" \
    -d "phone=1234567890&otp=$i"
done

# Test with empty/invalid OTP
curl -X POST "https://target.com/api/verify-otp" \
  -d "phone=1234567890&otp="
```

## Output Format

For each finding:
- **Endpoint**: OTP send/verify URL
- **Issue**: Type of vulnerability
- **Evidence**: What was observed
- **Exploit**: Steps to reproduce
- **Impact**: Account takeover risk
- **Fix**: Server-side validation, rate limiting
