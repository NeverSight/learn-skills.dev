---
name: mitm-find-secrets
description: Find leaked secrets, API keys, and credentials in traffic. Use when user asks about exposed keys, hardcoded secrets, or credential leakage.
---

# Find Leaked Secrets

Analyze the mitmproxy dump (log.txt) for exposed secrets for: $ARGUMENTS

> **Requires**: `log.txt` in the current directory. If it's missing, capture traffic first:
> ```bash
> mitmdump --set flow_detail=3 2>&1 | tee log.txt
> ```

## Secret Types to Find

### 1. API Keys & Tokens
- `api_key`, `apiKey`, `access_key`
- `secret_key`, `secretKey`, `client_secret`
- `token`, `auth_token`, `bearer`
- Patterns: Long alphanumeric strings (32+ chars)

### 2. Cloud Credentials
- AWS: `AKIA...` (access key ID)
- GCP: `AIza...` (API key)
- Azure: Connection strings
- Firebase: Config objects

### 3. Payment Secrets
- Merchant salts
- HMAC keys
- Encryption keys
- PCI-sensitive data

### 4. Third-Party Services
- SMS gateway credentials
- Email service keys
- Analytics tokens
- CDN secrets

### 5. Internal Secrets
- Database credentials
- Internal API keys
- JWT secrets
- Encryption salts

## Common Leak Locations

- JavaScript files
- Mobile app API calls
- Error responses with stack traces
- Debug endpoints
- Configuration endpoints

## Output Format

For each finding:
- **Secret Type**: Category of secret
- **Location**: Where found (endpoint/file)
- **Value**: Partially masked secret
- **Service**: What it's used for
- **Risk**: Potential impact
- **Verification**: How to test if active
