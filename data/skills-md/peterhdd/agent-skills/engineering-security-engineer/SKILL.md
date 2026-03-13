---
name: engineering-security-engineer
description: "Secure applications, infrastructure, and pipelines through threat modeling, vulnerability assessment, and security architecture. Use when you need OWASP Top 10 remediation, threat modeling (STRIDE/DREAD), penetration testing methodology, secrets management, dependency vulnerability scanning, authentication/authorization architecture, CSP and security headers, API security, supply chain security, compliance frameworks (SOC 2, GDPR, HIPAA), incident response, or security-focused code review."
metadata:
  version: "1.1.1"
---

# Security Engineering Guide

## Overview
This guide covers application security, infrastructure hardening, threat modeling, vulnerability management, and security operations. Use it when designing auth systems, reviewing code for security issues, setting up security scanning in CI/CD, responding to incidents, managing secrets, or ensuring compliance with security frameworks.

## First 10 Minutes

- Map the attack surface before suggesting fixes: public routes, auth entrypoints, admin paths, file upload/download flows, third-party callbacks, and secrets-loading paths.
- Run the bundled scripts from the skill directory first, not the repo under review: `engineering-security-engineer/scripts/scan_secrets.sh` and `engineering-security-engineer/scripts/audit_auth_surface.py`.
- For large mobile/web repos, start with high-signal trees such as `src`, `app`, `server`, `api`, `config`, and `scripts`; only scan the full repo if needed.
- Use `scripts/scan_secrets.sh` first. Secret exposure changes priority immediately.
- Use `scripts/audit_auth_surface.py` next to inventory auth-related files and session/token patterns before reviewing login or authorization changes.
- Identify the highest-risk trust boundary in the task: browser to API, API to service, service to database, or CI to cloud.

## Refuse or Escalate

- Refuse to approve security-sensitive changes that skip authorization checks, input validation, or audit logging "for later."
- Escalate immediately when the task involves credential exposure, insecure direct object access in production, or suspected compromise.
- Do not recommend weakening CSP, CORS, or cookie settings without documenting the exact breakage and the narrowest safe exception.
- Escalate if the requested solution conflicts with legal or compliance obligations already named in the system.

## Threat Modeling

### When to Threat Model
- Before building any new feature that handles user data, authentication, authorization, payments, or file uploads.
- When adding a new external dependency, third-party integration, or API endpoint.
- When changing data flow (new database, new cache, new queue) or access patterns.
- Quarterly review of existing threat models for systems handling PII, financial data, or health data.

### STRIDE Framework
For every component in the system, evaluate:
- **Spoofing**: Can an attacker impersonate a legitimate user or service? Mitigation: strong authentication (MFA, mutual TLS, API keys with rotation).
- **Tampering**: Can data be modified in transit or at rest? Mitigation: TLS 1.2+ for transit, AES-256/KMS for rest, HMAC signatures for integrity verification.
- **Repudiation**: Can a user deny performing an action? Mitigation: immutable audit logs with timestamp, user ID, action, and IP. Ship to a separate log store that the application cannot modify.
- **Information Disclosure**: Can sensitive data leak through logs, error messages, API responses, or side channels? Mitigation: scrub PII from logs, return generic error messages to clients, use constant-time comparison for secrets.
- **Denial of Service**: Can the system be overwhelmed? Mitigation: rate limiting, request size limits, timeout enforcement, auto-scaling with cost caps.
- **Elevation of Privilege**: Can a user gain unauthorized access? Mitigation: RBAC/ABAC at every layer, principle of least privilege, input validation on all trust boundaries.

### DREAD Risk Scoring
For each identified threat, score 1-10 on:
- **Damage**: How severe if exploited? (10 = full data breach, 1 = cosmetic issue)
- **Reproducibility**: How easy to reproduce? (10 = every time, 1 = requires rare conditions)
- **Exploitability**: How much skill/tooling needed? (10 = script kiddie, 1 = nation-state)
- **Affected users**: How many users impacted? (10 = all users, 1 = single user)
- **Discoverability**: How easy to find? (10 = publicly visible, 1 = requires insider access)

Average score determines priority: >7 = Critical (fix before release), 5-7 = High (fix within sprint), 3-5 = Medium (fix within quarter), <3 = Low (backlog).

## OWASP Top 10 Decision Rules

### A01: Broken Access Control
- Every API endpoint must check authentication AND authorization. Auth at the gateway is not sufficient — check again in the service.
- Use deny-by-default: if no explicit permission grants access, the request is rejected.
- Test for BOLA (Broken Object-Level Authorization): request resources with IDs belonging to other users. Must return 403 or 404, never the other user's data.
- Test for BFLA (Broken Function-Level Authorization): call admin endpoints with regular user tokens. Must return 403.
- Implement rate limiting on all endpoints: 100 req/min default, 10 req/min for auth endpoints, 5 req/min for password reset.

### A02: Cryptographic Failures
- Use bcrypt (cost factor 12+) or Argon2id for password hashing. Never use MD5, SHA-1, or SHA-256 for passwords.
- Encrypt all PII at rest with AES-256-GCM or use provider-managed KMS (AWS KMS, GCP KMS). Never store encryption keys alongside encrypted data.
- Enforce TLS 1.2+ for all connections. Reject TLS 1.0/1.1. Use HSTS header with `max-age=31536000; includeSubDomains; preload`.
- Never log or return secrets, tokens, passwords, or full credit card numbers in API responses or error messages. Mask to last 4 digits.

### A03: Injection
- Use parameterized queries exclusively for all database operations. Never construct SQL/NoSQL queries via string concatenation with user input.
- Validate and sanitize all user input at the API boundary. Use schema validators (Zod, Joi, Pydantic) with strict types, not just string parsing.
- For HTML output, use a templating engine with auto-escaping enabled by default (React JSX, Jinja2 with autoescape, Go html/template).
- For OS command execution, use language-native libraries (not `exec`/`system`). If shell execution is unavoidable, use allowlists, not blocklists, for permitted characters.

### A04: Insecure Design
- Apply defense in depth: authentication + authorization + input validation + output encoding + encryption + logging. No single layer is sufficient.
- Limit resource consumption per user: max file upload size (10MB default), max request body size (1MB default), max query results (100 default, 1000 max).
- Implement account lockout after 5 failed login attempts within 15 minutes. Use progressive delays (1s, 2s, 4s, 8s, 16s) instead of hard lockout for better UX.

### A05: Security Misconfiguration
- Disable directory listing, debug endpoints, and stack traces in production. Check with: `curl -v https://yourapp.com/debug`, `curl https://yourapp.com/.env`.
- Set security headers on all responses:
  ```
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.yourapp.com; frame-ancestors 'none'
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  ```
- Remove default credentials, sample data, and unused endpoints before deploying. Scan with `scripts/check_security_headers.sh`.

### A06: Vulnerable and Outdated Components
- Run `npm audit` / `pip audit` / `bundle audit` in CI. Fail the build on critical or high severity findings.
- Update dependencies monthly. For security patches, update within 48 hours of advisory publication.
- Before adding a new dependency, check: last commit date (<12 months), download count (>1k/week for JS, >500/week for Python), open CVEs (zero critical), and maintenance status (>1 active maintainer).
- Pin exact dependency versions in lock files. Use Renovate or Dependabot for automated upgrade PRs with test runs.

### A07: Identification and Authentication Failures
- Require MFA for all admin accounts and for any account with access to PII or financial data.
- Issue short-lived access tokens (15 min JWT) with opaque refresh tokens stored server-side. Refresh tokens must be rotatable and revocable.
- Implement password requirements: minimum 8 characters, check against breached password lists (Have I Been Pwned API or local k-anonymity check), no maximum length less than 128 characters.
- Session management: regenerate session ID after login, set `Secure`, `HttpOnly`, `SameSite=Strict` on all cookies. Expire idle sessions after 30 minutes for sensitive applications.

### A08: Software and Data Integrity Failures
- Verify integrity of all CI/CD artifacts: sign Docker images (cosign/Notary), verify checksums on downloaded binaries, use lock files for dependency integrity.
- Pin CI/CD action versions to SHA, not tags: `uses: actions/checkout@a81bbbf` not `uses: actions/checkout@v4`. Tags can be moved; SHAs cannot.
- Implement Subresource Integrity (SRI) for any third-party scripts loaded from CDNs.

### A09: Security Logging and Monitoring Failures
- Log all: authentication events (login, logout, failed attempts, MFA challenges), authorization failures (403s), input validation failures (400s), admin actions, and data access to PII.
- Never log: passwords, tokens, session IDs, full credit card numbers, or other secrets. Mask sensitive fields.
- Ship logs to a centralized, append-only system (CloudWatch, Datadog, Splunk) separate from the application. Retention: 90 days hot, 1 year cold for compliance.
- Alert on: >10 failed login attempts from same IP in 5 minutes, any admin action outside business hours, any access to bulk PII export, and 5xx error rate >1%.

### A10: Server-Side Request Forgery (SSRF)
- Validate and allowlist all URLs provided by users. Block requests to internal IP ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.169.254` (cloud metadata).
- If the application needs to fetch external URLs, use a dedicated HTTP client with: DNS resolution restricted to public IPs, request timeout (5s), and response size limit (10MB).
- For cloud environments, disable IMDS v1 and require IMDSv2 (AWS) or equivalent. The metadata endpoint is the most common SSRF escalation vector.

## Secrets Management

### Rules
- Never commit secrets to source control. Use `.gitignore` for `.env` files and run `git-secrets` or `trufflehog` in CI to catch accidental commits.
- Store secrets in: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, or Azure Key Vault. Inject at runtime via environment variables or sidecar.
- Rotate secrets on a schedule: API keys every 90 days, database passwords every 90 days, encryption keys every 365 days. Automate rotation — manual rotation gets skipped.
- If a secret is exposed (committed to git, logged, or sent to an unauthorized party): revoke immediately, rotate, audit access logs for the exposure window, and notify affected users if PII was accessible.

### Secret Detection in CI
- Run `trufflehog` or `gitleaks` on every PR. Block merge on any finding.
- Scan Docker images for embedded secrets: `docker history --no-trunc <image>` and check for ENV/ARG with secrets.
- Check Terraform state files for secrets: use `sensitive = true` for all secret variables. Store state encrypted in S3 with restricted access.

## Supply Chain Security

- Use lock files (package-lock.json, poetry.lock, go.sum) and verify integrity hashes.
- Pin GitHub Actions to commit SHAs, not tags. Review action source code before using.
- Run SCA (Software Composition Analysis) in CI: Snyk, Grype, or `npm audit --audit-level=high`. Block merges on critical/high findings.
- For Docker base images, use specific version tags (not `latest`), verify digests, and rebuild images monthly to pick up security patches.
- Maintain a Software Bill of Materials (SBOM) for production applications. Generate with `syft` or `trivy sbom`.

## API Security Decision Rules

- Authenticate every API call. Public endpoints must still have rate limiting and abuse detection.
- Use OAuth 2.0 + PKCE for user-facing APIs. Use API keys with HMAC signatures for service-to-service. Use mutual TLS for internal high-security services.
- Validate request bodies with strict schemas. Reject unknown fields (no mass assignment). Enforce maximum payload sizes.
- Return consistent error responses that do not leak implementation details. `{"error": "invalid_request", "message": "Validation failed"}` — never stack traces or SQL errors.
- Implement request signing for webhooks: HMAC-SHA256 with a shared secret. Include a timestamp in the signature to prevent replay attacks (reject if >5 minutes old).

## Self-Verification Protocol
After implementing security controls, verify:
- **Auth**: Test with: no token (expect 401), expired token (expect 401), valid token wrong role (expect 403), valid token correct role (expect 200). Test every endpoint, not just the ones you changed.
- **Input validation**: Send OWASP test payloads to every input field: `' OR '1'='1`, `<script>alert(1)</script>`, `../../../etc/passwd`, `; ls -la`, `{{7*7}}`. All must be rejected or safely escaped.
- **Headers**: Run `curl -I https://yourapp.com` and verify all security headers are present with correct values.
- **Secrets**: Search the entire repo: `git log --all -p | grep -iE '(password|secret|api.key|token).*=.*[A-Za-z0-9]{8,}'`. Zero matches on real secrets.
- **Dependencies**: Run `npm audit` / `pip audit` / `trivy image`. Zero critical or high vulnerabilities.
- **Logging**: Perform a login, a failed login, an authorization failure, and a data access. Verify all four events appear in the log system with correct fields.
- **Rate limiting**: Send 200 requests to a rate-limited endpoint within 1 minute. Verify 429 responses appear at the configured threshold.

## Failure Recovery
- **Security vulnerability reported**: Assess severity with DREAD within 1 hour. Critical (>7): patch within 24 hours, notify affected users. High (5-7): patch within 7 days. Medium (3-5): patch within 30 days. Low (<3): add to backlog.
- **Secret exposed in git**: Immediately: (1) rotate the secret, (2) revoke the old secret, (3) search logs for unauthorized usage during exposure window, (4) use `git filter-branch` or BFG to remove from history, (5) force-push. Notify affected users if data access is possible.
- **DDoS detected**: Enable CDN-level DDoS protection (Cloudflare Under Attack Mode, AWS Shield). Increase rate limiting thresholds. Enable geo-blocking if attack originates from a specific region. Scale up infrastructure only as a last resort — it is expensive and the attacker can scale too.
- **Compromised credentials**: Immediately: (1) disable the compromised account, (2) rotate all secrets the account had access to, (3) review audit logs for the account's actions during the compromise window, (4) notify the user and require password reset with MFA re-enrollment. If the compromised account is a service account, additionally check all systems it had access to for signs of lateral movement.
- **Failed security scan blocking deploy**: Never bypass the scan. Read the findings. If it is a true positive, fix it. If it is a false positive, add an explicit suppression with a comment explaining why and a review date (max 90 days). If the scan tool is broken, fix the tool — do not disable it.

## Existing System Security Audit
When assessing the security of an existing system:
1. **Map the attack surface** (30 min) — List all: public endpoints, authentication mechanisms, data stores, external integrations, file upload/download capabilities, and admin interfaces.
2. **Check auth** (15 min) — How are tokens issued, validated, and revoked? Is MFA available? Are sessions properly managed? Test BOLA on 5 endpoints.
3. **Check secrets** (15 min) — Run `trufflehog` on the repo. Check environment variable management. Verify secrets are not in Docker images, logs, or Terraform state.
4. **Check dependencies** (10 min) — Run `npm audit` / `pip audit` / `trivy`. Count critical and high findings.
5. **Check headers** (5 min) — Run `scripts/check_security_headers.sh` on the production URL. Flag missing headers.
6. **Check logging** (10 min) — Are auth events logged? Are logs shipped to a centralized system? Can the application modify its own logs?
7. **Check data handling** (10 min) — Is PII encrypted at rest? Is all traffic over TLS? Are backups encrypted? Who has access to production data?
8. **Prioritize findings** — Score each finding with DREAD. Present the top 5 by risk score with specific remediation steps and effort estimates.

## Deliverables

- Threat summary listing trust boundaries, likely abuse paths, and top risks by DREAD score.
- Remediation plan with priority, exploit preconditions, and owner.
- Verification checklist covering authz, secrets, headers, dependencies, and audit logs.
- If the task is incident response: timeline, containment action, rotation status, and follow-up validation steps.

## Compliance Quick Reference

### SOC 2
- Access control: RBAC with quarterly access reviews. Document who has access to what and why.
- Change management: All changes through version-controlled PRs with reviews. No direct production access.
- Monitoring: Centralized logging with 1-year retention. Alert on unauthorized access attempts.
- Incident response: Documented procedure, tested annually. Post-mortems for all security incidents.

### GDPR
- Data inventory: Document all PII collected, where it is stored, why it is collected, and retention period.
- Consent: Collect explicit consent before processing. Make opt-out as easy as opt-in.
- Right to erasure: Implement a data deletion pipeline that removes user data from all stores (including backups within retention period).
- Data breach notification: Notify supervisory authority within 72 hours. Notify affected users "without undue delay."

### HIPAA
- Encrypt all PHI at rest (AES-256) and in transit (TLS 1.2+). No exceptions.
- Access controls: minimum necessary principle. Log all access to PHI with user, timestamp, and purpose.
- Business Associate Agreements (BAAs) with all vendors that process PHI.
- Annual risk assessment and security training for all personnel with PHI access.

## Scripts

### `scripts/check_security_headers.sh`
Check HTTP security headers for a given URL. Tests for: Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security, Referrer-Policy, and Permissions-Policy. Reports missing, misconfigured, and present headers with grades.

```bash
scripts/check_security_headers.sh https://yourapp.com
scripts/check_security_headers.sh --json https://api.yourapp.com
```

### `scripts/scan_secrets.sh`
Scan a directory or git repository for accidentally committed secrets. Checks for: API keys, AWS credentials, private keys, database connection strings, JWT secrets, generic token assignments, and common credential patterns. By default it skips generated/vendor trees such as `www/`, `platforms/`, `Pods/`, `dist/`, and `build/` to reduce noise.

```bash
scripts/scan_secrets.sh .
scripts/scan_secrets.sh --git-history /path/to/repo
scripts/scan_secrets.sh --format json /path/to/project
```

### `scripts/audit_auth_surface.py`
Scan a repository for auth, session, token, cookie, and middleware hotspots. By default it skips generated/vendor trees such as `www/`, `platforms/`, `Pods/`, `dist/`, and `build/`. Use this before reviewing login flows, RBAC changes, or session security.

```bash
scripts/audit_auth_surface.py .
scripts/audit_auth_surface.py /path/to/repo --top 20
```

## References

- [Auth Patterns](references/auth-patterns.md) -- JWT + refresh token flow, OAuth 2.0 PKCE, session management, MFA implementation, RBAC/ABAC models, and API key management.
- [Security Headers](references/security-headers.md) -- CSP configuration for common frameworks (React, Next.js, Express), HSTS setup, and security header testing.
- [Vulnerability Patterns](references/vulnerability-patterns.md) -- OWASP Top 10 code examples (vulnerable and fixed versions) for Node.js, Python, and Go with automated test patterns.
- [Incident Response](references/incident-response.md) -- Incident response runbook, severity classification, communication templates, post-mortem template, and root cause analysis framework.
- [Compliance Checklists](references/compliance-checklists.md) -- SOC 2, GDPR, HIPAA, and PCI-DSS implementation checklists with evidence collection guides.
