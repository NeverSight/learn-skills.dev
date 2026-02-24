---
name: owasp-security-review
description: "Review code and architectures against the OWASP Top 10:2025 — the ten most critical web application security risks. Use when: (1) reviewing code for security vulnerabilities, (2) auditing a feature or codebase against OWASP categories, (3) providing remediation guidance for identified vulnerabilities, (4) writing new code and needing secure coding patterns. Triggers: 'review for security', 'OWASP audit', 'check for vulnerabilities','security checklist', 'is this code secure', 'security review', 'fix vulnerability'."
---

# OWASP Top 10:2025 Security Review

## Quick reference

| #   | Category                              | Key risk                                                               | Avg incidence |
| --- | ------------------------------------- | ---------------------------------------------------------------------- | ------------- |
| A01 | Broken Access Control                 | Unauthorized data access, privilege escalation, SSRF, CSRF             | 3.74%         |
| A02 | Security Misconfiguration             | Default creds, verbose errors, missing hardening, XXE                  | 3.00%         |
| A03 | Software Supply Chain Failures        | Vulnerable/malicious dependencies, compromised build pipelines         | 5.72%         |
| A04 | Cryptographic Failures                | Weak algorithms, hardcoded keys, missing encryption, weak hashing      | 3.80%         |
| A05 | Injection                             | SQLi, XSS, command injection, LDAP/XPath/EL injection                  | 3.08%         |
| A06 | Insecure Design                       | Missing threat modeling, business logic flaws, insufficient controls   | 1.86%         |
| A07 | Authentication Failures               | Credential stuffing, weak passwords, session fixation, missing MFA     | 2.92%         |
| A08 | Software/Data Integrity Failures      | Unsigned updates, insecure deserialization, untrusted CDN code         | 2.75%         |
| A09 | Security Logging & Alerting Failures  | Missing audit logs, no alerting, log injection, sensitive data in logs | 3.91%         |
| A10 | Mishandling of Exceptional Conditions | Failing open, info leakage via errors, unchecked return values         | 2.95%         |

## Workflows

### 1. Code review for security

Systematically check the code against each relevant category:

1. **Identify the code's surface area** — Does it handle auth? User input? File uploads? External data? Crypto? Error responses?
2. **Select relevant categories** from the table above based on the surface area.
3. **Load the reference file** for each relevant category and check the code against the "What to look for" section.
4. **Report findings** grouped by category with severity (Critical/High/Medium/Low), the specific code location, and a concrete fix.

Priority order for review (highest impact first):

- `[CRITICAL]` Input handling code → A05 (Injection), A01 (Access Control)
- `[CRITICAL]` Auth/session code → A07 (Authentication), A01 (Access Control)
- `[HIGH]` Data storage/transmission → A04 (Cryptographic Failures)
- `[HIGH]` Configuration/deployment → A02 (Security Misconfiguration)
- `[HIGH]` Dependencies → A03 (Supply Chain)
- `[MEDIUM]` Error handling → A10 (Exceptional Conditions), A09 (Logging)
- `[MEDIUM]` Architecture/design → A06 (Insecure Design)
- `[MEDIUM]` Data integrity → A08 (Integrity Failures)

### 2. Security audit checklist

Generate a checklist for a feature or codebase:

1. Read the feature/codebase to understand its scope.
2. For each of the 10 categories, determine if it applies.
3. For applicable categories, load the reference file and produce a checklist of items to verify.
4. Output a markdown checklist grouped by category.

### 3. Remediation guidance

When a vulnerability is identified:

1. Classify it into the correct OWASP category.
2. Load the corresponding reference file.
3. Apply the prevention checklist to produce a specific, actionable fix.
4. Provide a code example of the fix when possible.

## Reference files

Load the relevant file when you need detailed guidance for a specific category:

- **A01 Broken Access Control** — authorization checks, IDOR, CORS, CSRF, path traversal: [references/a01-broken-access-control.md](references/a01-broken-access-control.md)
- **A02 Security Misconfiguration** — hardening, default creds, error messages, headers, XXE: [references/a02-security-misconfiguration.md](references/a02-security-misconfiguration.md)
- **A03 Supply Chain Failures** — dependency management, SBOM, build pipeline security: [references/a03-supply-chain-failures.md](references/a03-supply-chain-failures.md)
- **A04 Cryptographic Failures** — encryption, hashing, key management, TLS, PRNG: [references/a04-cryptographic-failures.md](references/a04-cryptographic-failures.md)
- **A05 Injection** — SQL, XSS, command, ORM, LDAP, template injection: [references/a05-injection.md](references/a05-injection.md)
- **A06 Insecure Design** — threat modeling, business logic, secure SDLC: [references/a06-insecure-design.md](references/a06-insecure-design.md)
- **A07 Authentication Failures** — credential stuffing, MFA, session management, password policy: [references/a07-authentication-failures.md](references/a07-authentication-failures.md)
- **A08 Integrity Failures** — deserialization, code signing, untrusted sources, CDN trust: [references/a08-integrity-failures.md](references/a08-integrity-failures.md)
- **A09 Logging & Alerting** — audit trails, log injection, alerting, sensitive data in logs: [references/a09-logging-alerting-failures.md](references/a09-logging-alerting-failures.md)
- **A10 Exceptional Conditions** — error handling, fail-closed, resource cleanup, info leakage: [references/a10-exceptional-conditions.md](references/a10-exceptional-conditions.md)

## Severity classification

Use these severity levels when reporting findings:

- **Critical**: Directly exploitable, leads to full system compromise or mass data breach (e.g., SQLi with no parameterization, hardcoded admin credentials, missing auth on admin endpoints).
- **High**: Exploitable with moderate effort, significant data exposure or privilege escalation (e.g., IDOR, weak password hashing, SSRF, deserialization of untrusted data).
- **Medium**: Exploitable under specific conditions, limited impact (e.g., missing CSRF protection, verbose error messages, missing security headers).
- **Low**: Defense-in-depth issue, minimal direct impact (e.g., missing rate limiting, incomplete logging, suboptimal crypto configuration).

## Output format

When reporting security findings, use this structure:

```
### [SEVERITY] A0X: Category Name — Brief title

**Location**: `file:line`
**Risk**: What can go wrong and the impact.
**Finding**: What the code does wrong.
**Fix**: Specific remediation with code example.
```
