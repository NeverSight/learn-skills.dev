---
name: owasp-top-10
description: "OWASP Top 10 web application security risks - prevention, detection, and remediation. Use when implementing or reviewing access control, authentication, crypto/sensitive data, input validation and injection, secure design, security configuration, dependency management, session/identity, deserialization or CI/CD integrity, logging and monitoring, or server-side requests (SSRF)."
---

# OWASP Web Application Top 10

This skill encodes the OWASP Top 10 web application security risks for secure design, code review, and vulnerability prevention. References are loaded per risk (progressive disclosure).

Based on OWASP Top 10:2021 with 2025 RC callouts where applicable.

## When to Read Which Reference

| Risk | Read |
|------|------|
| A01 Broken Access Control | [references/a01-broken-access-control.md](references/a01-broken-access-control.md) |
| A02 Cryptographic Failures | [references/a02-cryptographic-failures.md](references/a02-cryptographic-failures.md) |
| A03 Injection | [references/a03-injection.md](references/a03-injection.md) |
| A04 Insecure Design | [references/a04-insecure-design.md](references/a04-insecure-design.md) |
| A05 Security Misconfiguration | [references/a05-security-misconfiguration.md](references/a05-security-misconfiguration.md) |
| A06 Vulnerable and Outdated Components | [references/a06-vulnerable-components.md](references/a06-vulnerable-components.md) |
| A07 Identification and Authentication Failures | [references/a07-authentication-failures.md](references/a07-authentication-failures.md) |
| A08 Software and Data Integrity Failures | [references/a08-integrity-failures.md](references/a08-integrity-failures.md) |
| A09 Security Logging and Monitoring Failures | [references/a09-logging-monitoring-failures.md](references/a09-logging-monitoring-failures.md) |
| A10 Server-Side Request Forgery (SSRF) | [references/a10-ssrf.md](references/a10-ssrf.md) |

Supply chain / dependencies → A06 (2025 A03 Software Supply Chain expands this).

## Quick Patterns

- Validate and sanitize at boundaries; use parameterized queries and allowlists.
- Apply least privilege and deny-by-default for access control.
- Use safe defaults in configuration; disable unnecessary features and change default credentials.
- Track and update dependencies; verify integrity of artifacts and pipelines.

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Prevent SQL injection | Use parameterized queries; never concatenate user input. See [A03](references/a03-injection.md). |
| Enforce access control | Check "can this user access this resource?" server-side before returning data. See [A01](references/a01-broken-access-control.md). |
| Protect sensitive data | Use strong encryption (AES-256, RSA-2048+), secure key storage, TLS everywhere. See [A02](references/a02-cryptographic-failures.md). |
| Harden configuration | Disable defaults, set security headers (CSP, HSTS), use generic error pages. See [A05](references/a05-security-misconfiguration.md). |
| Manage dependencies | Track versions, run `npm audit` / `pip audit`, update promptly. See [A06](references/a06-vulnerable-components.md). |

**Safe - parameterized query:**
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Unsafe - SQL injection risk:**
```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # NEVER do this
```

**Safe - authorization check:**
```python
def get_document(doc_id, current_user):
    doc = Document.query.get(doc_id)
    if doc.owner_id != current_user.id:
        raise PermissionError("Access denied")
    return doc
```

## Workflow

1. **Reviewing access control** → Read [references/a01-broken-access-control.md](references/a01-broken-access-control.md).
2. **Adding or changing authentication** → Read [references/a07-authentication-failures.md](references/a07-authentication-failures.md).
3. **Handling user input or queries** → Read [references/a03-injection.md](references/a03-injection.md).
4. **Designing a new feature** → Read [references/a04-insecure-design.md](references/a04-insecure-design.md), then the relevant A0x for the feature.
5. **Aligning with OWASP 2025** → See notes in A01 (SSRF), A06 (supply chain), and A10 (exceptional conditions below).

**2025 A10 – Mishandling of Exceptional Conditions:** Handle exceptions and errors safely; avoid leaking sensitive information in stack traces or messages; fail secure. See [OWASP Top 10:2025](https://owasp.org/Top10/2025/) for the full category.

Load reference files only when relevant to the task.
