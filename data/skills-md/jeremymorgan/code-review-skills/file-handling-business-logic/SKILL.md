---
name: file-handling-business-logic
description: Reviews file upload and handling for path traversal, type validation, storage, and related logic flaws. Use when auditing file upload or processing security.
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

Review all file upload functionality:

Check for:
1. File type validation (whitelist, not blacklist)
2. File size limits
3. Filename sanitization
4. Anti-virus scanning integration
5. Storage location (outside webroot)
6. Direct execution prevention
7. MIME type validation
8. Magic number verification
9. Image manipulation library vulnerabilities
10. ZIP bomb protection

Provide recommendations for secure file handling.

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
