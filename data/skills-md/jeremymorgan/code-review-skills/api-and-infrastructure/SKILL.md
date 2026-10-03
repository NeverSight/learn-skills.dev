---
name: api-and-infrastructure
description: Reviews API and infrastructure security configuration, including endpoints, headers, transport, and deployment settings. Use when auditing API or infrastructure hardening.
license: CC0-1.0
metadata:
  category: security
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

## API & Infrastructure Security

Review API-specific security configurations.


Check for:
1. CORS configuration
   - Not using wildcard (*) in production
   - Proper origin validation
   - Credentials handling

2. Rate Limiting
   - Implemented on all endpoints
   - Different limits for different operations
   - Distributed rate limiting for scaled apps

3. API Versioning security
   - Deprecated version handling
   - Breaking change management

4. Request size limits
   - Body parser limits
   - File upload restrictions
   - JSON depth limits

5. HTTP Security Headers
   - Helmet.js configuration
   - CSP headers
   - X-Frame-Options
   - X-Content-Type-Options
   - Strict-Transport-Security

6. API key/token management
   - Secure storage
   - Rotation policy
   - Scope limitations

7. Error handling
   - No stack traces in production
   - Generic error messages
   - Proper status codes

## Provide:

A structured finding report with the following for each issue:

Title, Severity (Critical/High/Medium/Low), CWE (if applicable), Evidence (file, function, line ranges), and a short Why it matters.

Exploitability notes and, where safe, a minimal PoC or reproduction steps (no real secrets).

Remediation: precise code-level fix or config change (snippets welcome), plus defense-in-depth guidance.

A summary risk score (0–10) and top 3–5 prioritized fixes that reduce risk fastest.

A checklist diff: which items from the “Check for” list are Pass/Fail/Not Applicable.

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
