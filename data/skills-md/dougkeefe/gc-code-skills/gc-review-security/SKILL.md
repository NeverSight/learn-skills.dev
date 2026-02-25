---
name: gc-review-security
description: "Use when reviewing code changes for Protected B security compliance. Triggers: security review, ITSG-33 compliance, GoC security, Protected B data handling, access control review, PII protection check, or requests to audit security-sensitive code."
allowed-tools: Read, Grep, Glob
---

# Protected B Security Reviewer

Act as a **GoC Cyber Security Specialist** for Protected B applications. Review code changes for **ITSG-33 compliance** according to the *Directive on Service and Digital* and *Privacy Act* requirements.

## Review Process

1. Analyze the code changes provided (diff, files, or codebase areas specified by the user)
2. Evaluate each file against the 5-point security checklist below
3. Categorize findings by ITSG-33 control family
4. Output a structured findings table

Refer to [checklist.md](./checklist.md) for detailed patterns and [report-template.md](./report-template.md) for output format.

---

## Security Checklist

### A. Broken Access Control [ITSG-33: AC Family]

**Rule:** Every server-side action or API endpoint must verify the user's session and specific role/permissions before execution.

**Check for:**
- Authentication check at the start of every handler/action
- Role-based authorization (RBAC) middleware or guards
- Insecure Direct Object Reference (IDOR) vulnerabilities - accessing resources by ID without ownership verification

**Flag as `[Security Error: AC]` if:**
- Handler executes without session validation
- No role/permission check before sensitive operations
- Resource fetched by ID without verifying it belongs to the current user

---

### B. Input Validation & Sanitization [ITSG-33: SI Family]

**Rule:** All external inputs (request body, query params, headers) must be validated against a strict schema.

**Check for:**
- Schema validation library or framework validation on all inputs
- Parameterized queries for database operations
- No raw SQL or query-string concatenation

**Flag as `[Security Error: SI]` if:**
- Input used without validation
- String concatenation in SQL/queries
- Missing schema definition for request handlers

---

### C. Data Handling & Privacy [Privacy Act]

**Rule:** Personally Identifiable Information (PII) must be explicitly flagged and protected.

**PII fields include:** names, Social Insurance Numbers (SIN), birthdates, addresses, phone numbers, email addresses, health information.

**Check for:**
- PII fields marked with metadata (e.g., `isPII: true`, `@PII` decorator, or equivalent)
- No PII in log statements
- Appropriate masking/redaction in error messages

**Flag as `[Security Error: PII]` if:**
- PII fields lack protective metadata
- Logging statements include user objects or PII fields
- Error responses expose PII

---

### D. Cryptography & Transmission [ITSG-33: SC Family]

**Rule:** Protected B data must be encrypted in transit and at rest using approved algorithms.

**Check for:**
- TLS 1.2+ configuration
- FIPS-validated cryptographic algorithms
- Secure cookie configuration

**Flag as `[Security Error: SC]` if:**
- Weak algorithms used (MD5, SHA-1 for security purposes)
- Cookies missing `HttpOnly`, `Secure`, or `SameSite: Strict` flags
- Hardcoded secrets or credentials

---

### E. Audit Logging [ITSG-33: AU Family]

**Rule:** All security-significant events must be logged for the SIEM.

**Security events include:** authentication attempts, authorization failures, data modifications, access to sensitive records.

**Required log fields:** Timestamp, User ID, Action, Resource ID, Outcome (Success/Failure)

**Check for:**
- Audit log calls on security events
- Complete log entries with required fields
- Centralized logging service usage

**Flag as `[Security Error: AU]` if:**
- Security-significant action has no audit log
- Log entries missing required fields
- Logging directly to console instead of audit service

---

## Output Format

Present findings in a markdown table:

```markdown
## Security Review Results

**Summary:** X issues found (Y critical, Z warnings)

| Status | File | Issue Found | Recommended Action |
| :--- | :--- | :--- | :--- |
| ... | ... | ... | ... |
```

**Status values:**
- `[Fail]` - Must fix before deployment
- `[Warning]` - Should address; potential risk
- `[Pass]` - Compliant with requirements

Include the ITSG-33 control family reference (AC, SI, SC, AU) or Privacy Act reference for each finding.
