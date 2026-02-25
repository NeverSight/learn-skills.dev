---
name: sast-eslint-security
description: Run ESLint with security plugins on JavaScript/TypeScript code. Detects eval usage, non-literal RegExp, prototype pollution, and other JS/TS security anti-patterns.
---

# SAST Scan with ESLint Security (JavaScript/TypeScript)

You are a security engineer running static analysis on JavaScript/TypeScript code using **ESLint** with security-focused plugins.

## When to use

Use this skill when asked to perform a SAST scan or security review on JavaScript or TypeScript code.

## Prerequisites

- ESLint installed with security plugin:
  ```bash
  npm install --save-dev eslint eslint-plugin-security
  # For TypeScript: also install @typescript-eslint/parser
  ```
- Verify: `npx eslint --version`

## Instructions

1. **Identify the target** — Determine the JS/TS file(s) or directory to scan.
2. **Run the scan:**
   ```bash
   npx eslint --plugin security --rule 'security/detect-unsafe-regex: error' \
     --rule 'security/detect-non-literal-regexp: warn' \
     --rule 'security/detect-eval-with-expression: error' \
     --rule 'security/detect-no-csrf-before-method-override: error' \
     --rule 'security/detect-possible-timing-attacks: warn' \
     --rule 'security/detect-object-injection: warn' \
     --format json --output-file eslint-security-results.json \
     <target-path>
   ```
   - Alternatively, if the project has an `.eslintrc` with security plugin configured:
     ```bash
     npx eslint --format json --output-file eslint-security-results.json <target-path>
     ```
3. **Parse the results** — Read JSON output and present findings:

```
| # | Severity | Rule | File:Line | Finding | Remediation |
|---|----------|------|-----------|---------|-------------|
```

4. **Summarize** — Provide total issues by severity, critical findings first, and specific fixes.

## Key Security Rules

| Rule | Risk |
|------|------|
| `detect-eval-with-expression` | Remote code execution via eval() |
| `detect-non-literal-regexp` | ReDoS (Regular Expression DoS) |
| `detect-unsafe-regex` | ReDoS via exponential backtracking |
| `detect-no-csrf-before-method-override` | CSRF bypass |
| `detect-possible-timing-attacks` | Timing side-channel leaks |
| `detect-object-injection` | Prototype pollution / injection |
| `detect-child-process` | Command injection via child_process |
| `detect-non-literal-fs-filename` | Path traversal |
