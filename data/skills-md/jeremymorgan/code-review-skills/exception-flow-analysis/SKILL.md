---
name: exception-flow-analysis
description: Traces how errors and exceptions flow through critical code paths to find swallowed errors and broken propagation. Use when analyzing exception handling on important paths.
license: CC0-1.0
metadata:
  category: code-quality
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

Trace error flow through the application:

Critical paths to analyze:
1. Database connection failure
2. Third-party API timeout
3. Invalid user input
4. Authentication failure
5. File system errors

For each path, verify:
- Where is the error caught?
- How is it transformed?
- What gets logged?
- What does the user see?
- Is the system state consistent?

In the audit report, document the error flow as a text diagram or structured list showing:
- Error origin points
- Transformation layers
- Final handling points
- Recovery mechanisms

Anti-patterns to identify:
- Swallowed exceptions (empty catch blocks)
- Generic catch-all handlers hiding specific errors
- Errors used for flow control
- Missing error boundaries
- Inconsistent error formats

Provide a standardized error handling template.

## Provide:

A structured finding report

A scale of 1/10 on how important each finding is

Remediation: precise code-level fix or config change (snippets welcome) if possible

## Constraints & style:

Be concrete and cite exact code locations and identifiers.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
