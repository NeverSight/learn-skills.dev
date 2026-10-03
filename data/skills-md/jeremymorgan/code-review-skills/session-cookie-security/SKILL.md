---
name: session-cookie-security
description: Analyzes session and cookie security, including flags, expiration, fixation, and storage. Use when auditing session management and cookie configuration.
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

# Session and Cookie Security
Analyze this project's source code. 
Focus on session management and cookie security.

Verify:
1. Session configuration
   - Secure flag (HTTPS only)
   - HttpOnly flag (no JS access)
   - SameSite attribute
   - Session timeout
   - Session regeneration after login

2. Cookie security
   - All cookies have appropriate flags
   - No sensitive data in cookies
   - Proper domain/path scoping
   - Encryption for sensitive cookies

3. CSRF Protection
   - Token implementation
   - Double submit cookie pattern
   - Origin header validation

4. Session storage
   - Not using default in-memory storage in production
   - Redis/database backed sessions
   - Session cleanup/expiration

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
