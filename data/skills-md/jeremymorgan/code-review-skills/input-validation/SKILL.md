---
name: input-validation
description: Reviews input validation and sanitization across the application for injection and malformed-input risks. Use when auditing how untrusted input is handled.
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

## Input Validation

Review all input validation across the application.

Check for:
1. SQL Injection vulnerabilities
   - Raw SQL queries without parameterization
   - Dynamic query building
   - Stored procedure calls

2. NoSQL Injection (if using MongoDB)
   - Unvalidated query operators ($where, $ne, $gt)
   - JavaScript execution in queries

3. Command Injection
   - Child process spawning
   - System command execution

4. XSS Prevention
   - Input sanitization
   - Output encoding
   - Content-Type headers

5. XXE (XML External Entity) attacks
   - XML parsing configuration
   - File upload handling

6. Path Traversal
   - File system operations
   - Directory listing prevention

7. Request validation
   - Body size limits
   - Parameter pollution
   - Type checking
   - Required field validation

Create a validation matrix showing each endpoint and its validation status.

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
