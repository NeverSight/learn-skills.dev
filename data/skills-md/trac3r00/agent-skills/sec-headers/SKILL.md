---
name: sec-headers
description: Grades the HTTP security headers of a URL — HSTS, Content-Security-Policy, framing protection (X-Frame-Options/frame-ancestors), X-Content-Type-Options, Referrer-Policy, and cookie Secure/HttpOnly flags — with an A-F letter grade and per-header pass/warn/fail. Stdlib-only fetch, no browser.
when_to_use: After deploying a web app, before go-live, or in CI as a header gate (--min-grade). NOT a vulnerability scanner or a pentest; it checks the headers browsers enforce, nothing else.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [security, http, headers, web, ci-gate]
---

# Sec Headers

The security headers browsers enforce, graded in one request.

## Commands

```bash
python3 scripts/sec_headers.py https://your-app.com
python3 scripts/sec_headers.py https://your-app.com --json --min-grade B
```

## Checks

| Header | Missing = |
|---|---|
| Strict-Transport-Security | FAIL (-25): downgrade attacks possible |
| Content-Security-Policy | FAIL (-25): no XSS second line of defense |
| X-Frame-Options or CSP frame-ancestors | WARN (-10): clickjacking possible |
| X-Content-Type-Options | WARN (-10): MIME confusion |
| Referrer-Policy | WARN (-10): URL leakage |
| Cookie Secure/HttpOnly | WARN (-10): session theft surface |

Grade: A ≥90, B ≥75, C ≥60, D ≥40, F below. `--min-grade` makes it a CI gate.

## Pairs with

`api-tester` (endpoint behavior), `secret-gate` (credential leaks in the
code behind those headers), `net-probe` (TLS validity of the connection).
