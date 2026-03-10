---
name: web-security-hardening
description: Security audit checklist for web applications. Use when reviewing, auditing, or hardening a web app's security posture. Covers rate limiting, auth headers, IP blocking, CORS, security middleware, input validation, file upload limits, ORM usage, and password hashing. Triggers on requests like "review security", "harden this app", "security audit", "check for vulnerabilities", or when building/reviewing API endpoints.
---

# Web Security Hardening

Security audit checklist for web applications. Run through each item when reviewing or building web apps.

## Audit Workflow

1. Identify the framework (Node.js/Express, Python/Django/Flask, etc.)
2. Review each checklist item below
3. For implementation details, see framework-specific references:
   - **Node.js/Express**: See [references/nodejs.md](references/nodejs.md)
   - **Python/Django/Flask**: See [references/python.md](references/python.md)
4. For production deployments, see [references/production-gcp.md](references/production-gcp.md) for extended checklist covering:
   - GCP infrastructure (IAM, networking, secrets)
   - CI/CD pipeline security
   - Monitoring & incident response
5. Report findings with severity and remediation steps

## Security Checklist

### 1. Rate Limiting
**Risk**: DoS attacks, brute force attempts, API abuse

Check for:
- Per-endpoint rate limits (stricter on auth endpoints)
- Rate limit headers in responses (`X-RateLimit-*`)
- Appropriate limits for different user tiers

### 2. Security & Authorization Headers
**Risk**: XSS, clickjacking, MIME sniffing, info leakage

Required headers:
- `Strict-Transport-Security` (HSTS)
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- `Content-Security-Policy`
- `Authorization` header validation on protected routes

### 3. IP Block List (Public APIs)
**Risk**: Abuse from known bad actors, bot traffic

Check for:
- IP-based blocking mechanism
- Integration with threat intelligence feeds (optional)
- Logging of blocked requests

### 4. CORS Configuration
**Risk**: Unauthorized cross-origin requests, data theft

Check for:
- Explicit origin whitelist (not `*` in production)
- Appropriate methods and headers allowed
- Credentials handling if needed

### 5. Security Middleware
**Risk**: Common web vulnerabilities

Check for framework-appropriate middleware:
- Node.js: `helmet`
- Python: `django-secure`, `flask-talisman`
- Sets multiple security headers automatically

### 6. Input Validation
**Risk**: Injection attacks, data corruption, XSS

Check for:
- Frontend validation (UX, not security)
- Backend validation (required for security)
- Schema validation libraries (Zod, Joi, Pydantic, etc.)
- Sanitization of user input before storage/display

### 7. File Upload Limits
**Risk**: Storage exhaustion, malicious file uploads

Check for:
- Max file size limits
- Allowed file type restrictions (MIME + extension)
- File content validation (magic bytes)
- Secure storage location (outside webroot)

### 8. ORM for Database Access
**Risk**: SQL injection

Check for:
- Parameterized queries (never string concatenation)
- ORM usage (Prisma, Sequelize, SQLAlchemy, Django ORM)
- If raw SQL needed: prepared statements only

### 9. Password Hashing
**Risk**: Credential theft, rainbow table attacks

Check for:
- Strong algorithm: bcrypt, Argon2, or scrypt
- Appropriate cost factor (bcrypt rounds ≥10)
- No MD5, SHA1, or plain SHA256 for passwords
- No plaintext password storage or logging

## Audit Report Format

```markdown
## Security Audit: [App Name]

### Summary
- **Items Passing**: X/9
- **Critical Issues**: X
- **Recommendations**: X

### Findings

#### [Item Name] - [PASS/FAIL/PARTIAL]
**Severity**: Critical/High/Medium/Low
**Finding**: [Description]
**Location**: [File/endpoint]
**Remediation**: [Steps to fix]
```
