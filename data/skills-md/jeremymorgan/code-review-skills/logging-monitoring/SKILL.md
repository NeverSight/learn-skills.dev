---
name: logging-monitoring
description: Reviews logging and monitoring for security visibility, sensitive-data leakage, and audit coverage. Use when auditing observability and security logging.
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

# Logging and Monitoring

Review logging and monitoring implementation in this application.

Verify:
1. Sensitive data not logged
   - Passwords, tokens, PII
   - Credit card numbers
   - API keys

2. Security event logging
   - Failed login attempts
   - Authorization failures
   - Input validation failures
   - System errors

3. Log injection prevention
   - Input sanitization in logs
   - Structured logging

4. Log storage and retention
   - Secure storage
   - Rotation policy
   - Backup strategy

5. Monitoring alerts
   - Unusual activity detection
   - Error rate monitoring
   - Performance anomalies

Provide a logging compliance checklist.

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
