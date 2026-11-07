---
name: owasp-top10-analysis
description: Systematically review a web application against the OWASP Top 10 vulnerability classes with concrete test cases per category. Use for web app assessments and security gate reviews.
---

# OWASP Top 10 Analysis

Work a web application category-by-category so nothing is skipped.

## Checklist by Category (2021)

### A01 Broken Access Control
- Test IDOR: swap identifiers (user IDs, UUIDs, filenames) between two test accounts
- Verify server-side enforcement on every endpoint, not just UI hiding
- Try HTTP method overrides, path traversal in IDs, mass assignment on profile updates
- Check forced browsing to admin routes after logout/role downgrade

### A02 Cryptographic Failures
- Confirm TLS 1.2+ only, HSTS present
- Find plaintext protocols, hardcoded keys, weak hashes (MD5/SHA1) for passwords
- Passwords hashed with bcrypt/argon2 + per-user salt; secrets not in client bundles

### A03 Injection
- SQL/NoSQL/ORM injection: parameterized queries verified; test in sort/filter/order params, not just search
- OS command injection in file upload/filename handling, image processing, PDF generators
- Header injection, template injection (SSTI) in email/render features

### A04 Insecure Design
- Business logic abuse: negative quantities, currency confusion, race conditions on credits/coupons
- Trust-boundary violations: client-computed prices, unsigned discount tokens

### A05 Security Misconfiguration
- Debug modes, default credentials, verbose errors, directory listing
- Unnecessary features enabled (PUT, TRACE), permissive CORS (`*` with credentials)

### A06 Vulnerable Components
- SBOM against known CVEs; flag unmanaged/EOL dependencies
- Check client-side libs too (npm audit / Retire.js signals)

### A07 Authentication Failures
- Credential stuffing resistance (rate limiting, MFA), session fixation, weak password policy
- Session tokens: rotated on login, invalidated on logout, secure/httpOnly flags
- MFA bypass flows: reset, backup codes, OAuth account linking

### A08 Integrity Failures
- Unsigned updates/deserialization of untrusted data (pick your targets: memcached, JWT, file parsers)
- CI/CD pipeline: pinned dependencies, verified provenance

### A09 Logging & Monitoring
- Auth events, access-control denials, and input-validation failures are logged with context
- Logs don't contain passwords/tokens; alerting exists for brute force

### A10 SSRF
- Any URL-fetch feature (webhooks, importers, preview generators): test localhost, link-local (169.254.169.254), IPv6 equivalents, DNS rebinding
- Scheme and redirect handling enforced server-side

## Output

Per finding: category, evidence, reproduction, severity, fix. Note verified-negatives per category for coverage evidence.
