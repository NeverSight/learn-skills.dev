---
name: notfound-security-audit
description: Read-only security audit of a web project — stack detection, vulnerable dependencies and runtimes (PHP, Node.js, Next.js…), leaked secrets, injection patterns (SQLi, XSS, SSRF, command execution), auth/session/cookie/CORS/header misconfiguration, Docker, CI and external services (Supabase, Firebase). Use when the user asks to audit, security-review or "check for vulnerabilities" in a codebase, asks whether their site is affected by a CVE, or before deploying an AI-generated app. Reports confirmed issues, findings that need review and preventive advice separately, and never modifies code without explicit approval.
---

# NotFound Security Audit

A read-only audit you run **with** the user, not on them. The bundled scanner (`scripts/nfaudit.py`, Python 3.9+,
standard library only) does the mechanical part; your job is to triage what it finds, review what it cannot
see (authentication, authorisation, business logic) and explain the result in plain language.

## Ground rules (always)

1. **Read-only by default.** Do not edit, delete, install, upgrade or commit anything until the user approves a
   specific fix. Proposing a patch is fine; applying it needs a yes.
2. **No attacks.** Never send exploit payloads, fuzz, brute-force or scan systems. The only network actions are
   the two opt-ins below, and only after the user agrees.
3. **Never print secrets.** Reports redact them; when you quote code, redact keys/tokens/passwords the same way
   (first 4 characters + `…******`).
4. **Be honest about certainty.** A pattern match is not a vulnerability, and a vulnerability is not an attack.
   Never say a project "was hacked" or "is exploitable" without evidence.
5. **Runtime CVEs are fixed by upgrading the runtime.** Changing application code or plugins does not fix a
   vulnerable PHP/Node.js binary; a WAF rule is defence in depth, not a fix.

## Workflow

### 1. Scope
Confirm the project path. Ask whether this is the user's own code. Reports go to the system temp directory by
default (outside the project); pass `--out` only if the user wants them elsewhere.

### 2. Automated scan (read-only, offline)
```bash
python "<this skill's directory>/scripts/nfaudit.py" scan <project-path>
```
It prints a summary and the report paths (`nfaudit-report.md` / `.json`; add `--format md,json,sarif` for SARIF).
Read the JSON report: it has the stack, every finding with `status`, `severity`, `file`, `line`, `evidence`,
`fingerprint`, plus `entry_points` (attack surface) and `notes` (coverage gaps).

### 3. Ask before going online (optional)
- **Dependencies against OSV.dev** — full CVE coverage for npm, PyPI, Packagist, Go, crates.io, RubyGems, Maven.
  Sends only package names and versions, never code. Ask: *"¿Consulto tus dependencias en OSV.dev? Solo se envían
  nombres y versiones de paquetes."* Then add `--osv`.
- **Live headers** — one GET request to a URL **the user owns**: `nfaudit.py headers https://their-site`.
  Checks HSTS, CSP, cookies, CORS and version banners. No crawling, no payloads.
- If `osv-scanner`, `gitleaks`, `trivy` or `semgrep` are already installed, you may offer to run them as a second
  opinion; do not install anything without approval.

### 4. Triage (the important part)
Work through findings in this order: `confirmed` → `suspected` high/critical → the rest.
- **confirmed** — vulnerable version pinned in a lockfile/Dockerfile, open Firebase rules, committed `.env`, etc.
  Verify the evidence is real (e.g. the lockfile is the one deployed), then report.
- **suspected** — open the file and trace the data flow **source → sink**: does user input actually reach it?
  Is there validation, an allow-list, a parameterised query or framework escaping on the way? Try to disprove it.
  Downgrade or drop it if it is safe, and say why. Keep it if you cannot rule it out.
- **preventive** — hardening. Group them; do not inflate them into vulnerabilities.
- Runtime findings: if only `php:8.4` / `node:24` is declared, the patch level is unknown. Ask the user to run
  `php -v` / `node -v` where it is deployed (or check the hosting panel) instead of guessing.
- Ignore what is out of scope unless clearly exploitable: generic DoS, missing rate limiting, open redirects
  without impact, test fixtures, docs examples.

### 5. Manual review (what the scanner cannot do)
Use `entry_points` from the report and the checklists in `references/`:
- `references/methodology.md` — triage method, severity and status rules, false-positive list.
- `references/checklists.md` — per-stack review: auth & sessions, authorisation (IDOR), uploads, SSRF, secrets,
  Next.js, Laravel/PHP, Django/Flask, Express, Supabase/Firebase, Docker, CI.
For each route handler, server action or API endpoint: who can call it, what it checks, whose data it touches.

### 6. Report
Use `references/report-template.md`. Keep three separate sections: **Confirmed**, **Needs review**,
**Preventive**. For each finding: severity, what it is (one sentence a non-expert understands), file:line,
redacted evidence, why it matters, and the fix. End with what was *not* covered.
Answer in the user's language.

### 7. Fixes — only with approval
Offer fixes ordered by risk. For each one show the exact change (diff or command) and wait for approval.
After applying, re-run the scan to confirm. Never rotate keys, push, deploy or touch production for the user;
tell them what to do (e.g. "rotate this key in the Stripe dashboard first").

## Configuration
A `.nfaudit.json` in the project root (optional):
```json
{ "exclude": ["legacy/**"], "disable_rules": ["js-weak-hash"], "ignore": ["<fingerprint>"], "include_tests": true }
```
Inline `nfaudit-ignore` on (or above) a line silences that line. `--fail-on high` makes CI fail on
non-preventive findings of that severity or above.

## Limits (say them when relevant)
Pattern rules are line-based, not full data-flow analysis: expect false positives and misses. The built-in
advisory list is small and dated (see `data/known-advisories.json` → `updated`); use `--osv` for real coverage.
It cannot see the server's real runtime version, WAF, network or cloud settings.
