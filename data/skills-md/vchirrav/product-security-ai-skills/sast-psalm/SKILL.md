---
name: sast-psalm
description: Run Psalm with taint analysis on PHP code. Detects SQL injection, XSS, command injection, path traversal, and other taint-flow vulnerabilities in PHP applications.
---

# SAST Scan with Psalm Taint Analysis (PHP)

You are a security engineer running static analysis on PHP code using **Psalm** with taint analysis.

## When to use

Use this skill when asked to perform a SAST scan or security review on PHP code.

## Prerequisites

- Psalm installed (`composer require --dev vimeo/psalm`)
- Initialize: `./vendor/bin/psalm --init`
- Verify: `./vendor/bin/psalm --version`

## Instructions

1. **Identify the target** — Determine the PHP project directory.
2. **Run the scan:**
   ```bash
   ./vendor/bin/psalm --taint-analysis --output-format=json > psalm-results.json
   ```
   - Specific directory: `./vendor/bin/psalm --taint-analysis src/ --output-format=json`
   - Higher analysis level: `./vendor/bin/psalm --taint-analysis --level=1 --output-format=json`
   - Show info: `./vendor/bin/psalm --taint-analysis --show-info=true --output-format=json`
3. **Parse the results** — Read JSON output and present findings:

```
| # | Severity | Type | File:Line | Finding | Taint Flow | Remediation |
|---|----------|------|-----------|---------|------------|-------------|
```

4. **Summarize** — Provide total issues, critical taint flows first, and specific sanitization fixes.

## Key Psalm Taint Types

| Taint Type | Risk |
|-----------|------|
| TaintedSql | SQL injection via unsanitized input |
| TaintedHtml | XSS via unescaped output |
| TaintedShell | Command injection |
| TaintedFile | Path traversal |
| TaintedHeader | HTTP header injection |
| TaintedSSRF | Server-side request forgery |
| TaintedUnserialize | Insecure deserialization |
| TaintedInclude | Remote/local file inclusion |
| TaintedEval | Code injection via eval |
| TaintedLdap | LDAP injection |
