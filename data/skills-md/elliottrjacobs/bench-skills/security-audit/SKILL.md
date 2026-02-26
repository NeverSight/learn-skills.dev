---
name: security-audit
description: Deep security audit of codebase with parallel domain-focused agents. Use when the user says "security audit", "check for vulnerabilities", "security review", or before a launch/deployment. More thorough than the security reviewer in /engineer-review.
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Task", "Write"]
argument-hint: "[files or feature]"
---

# /security-audit — Deep Security Audit

Thorough security audit using 3-4 parallel agents, each focused on a specific security domain. More comprehensive than the security reviewer in `/engineer-review` — use this for pre-launch audits or when security is the primary concern.

## When to Use

- Pre-launch security review
- User says "security audit", "check for vulnerabilities"
- After significant auth/data changes
- Periodic codebase security check

## Process

### Step 1: Scope the Audit

Determine what to audit:
- If `$ARGUMENTS` specifies files or features: scope to those
- If no arguments: audit the entire codebase

Read `package.json`, config files, and directory structure to understand the tech stack. This determines which agents to launch and what they focus on.

### Step 2: Detect Tech Stack

Check for:
- `next.config.*` → server actions, middleware, API routes, CSRF
- `app.json` or `expo` in package.json → deep linking, secure storage, certificate pinning
- `supabase/` directory → RLS, auth config, storage policies
- `tsconfig.json` → type safety as security boundary
- `.env*` files → environment variable handling

### Step 3: Launch Parallel Security Agents

Spawn ALL agents IN PARALLEL using the Task tool. Send all Task calls in a single message.

#### Agent 1: Auth & Access Control
```
prompt: Perform a security audit focused on authentication and authorization.
  Examine: authentication flows, session management, token handling, password
  policies, OAuth configuration, middleware/route guards, privilege escalation
  paths, RBAC/permission checks, protected route coverage.
  For each finding: file, line, severity (P1-P4), vulnerability description,
  remediation steps.
```

#### Agent 2: Input Validation & Injection
```
prompt: Perform a security audit focused on injection vulnerabilities.
  Examine: SQL injection (especially raw queries), XSS (user content rendering,
  dangerouslySetInnerHTML), command injection, path traversal, SSRF, template
  injection, header injection, open redirects.
  Check all system boundaries: API routes, server actions, form handlers, URL
  parameters, file uploads.
  For each finding: file, line, severity (P1-P4), vulnerability description,
  proof of concept, remediation steps.
```

#### Agent 3: Data Protection & Secrets
```
prompt: Perform a security audit focused on data handling and secrets.
  Examine: hardcoded secrets/API keys, exposed environment variables,
  sensitive data in logs, PII exposure in API responses, insecure data storage,
  missing encryption, overly permissive CORS, data leak through error messages,
  client-side exposure of server-only data.
  Check: .env files, git history for leaked secrets, client bundles for
  server-only values, API response payloads for over-fetching.
  For each finding: file, line, severity (P1-P4), vulnerability description,
  remediation steps.
```

#### Agent 4: Infrastructure & Configuration (conditional)

Launch this agent if the project has API routes, middleware, or deployment configuration:

```
prompt: Perform a security audit focused on infrastructure and configuration.
  Examine: CORS configuration, CSP headers, rate limiting, dependency
  vulnerabilities (check package.json for known vulnerable packages),
  security headers (X-Frame-Options, HSTS, etc.), API rate limiting,
  file upload size limits, error handling that leaks stack traces.
  For each finding: file, line, severity (P1-P4), vulnerability description,
  remediation steps.
```

### Step 4: Synthesize Security Report

Collect all agent findings and produce a prioritized report:

```markdown
## Security Audit Report

**Scope:** [what was audited]
**Tech Stack:** [detected frameworks]
**Date:** [current date]

### Executive Summary
[1-2 sentence overall assessment]

### P1 — Critical (fix immediately)
| # | Category | File | Line | Vulnerability | Remediation |
|---|----------|------|------|---------------|-------------|

### P2 — Important (fix before merge/launch)
| # | Category | File | Line | Vulnerability | Remediation |
|---|----------|------|------|---------------|-------------|

### P3 — Moderate (fix soon)
| # | Category | File | Line | Vulnerability | Remediation |
|---|----------|------|------|---------------|-------------|

### P4 — Low (consider fixing)
| # | Category | File | Line | Vulnerability | Remediation |
|---|----------|------|------|---------------|-------------|

### Positive Security Patterns
[Good security practices found in the codebase]

### Recommendations
[General security improvements not tied to specific findings]

### Auditors Run
[List which agents were launched]
```

Deduplicate findings across agents. Escalate any finding involving user data or authentication to at minimum P2.

## Output

Security report presented inline. Save to `docs/audits/` if requested.

## Next Steps

- P1 findings? Fix immediately
- Supabase project? Ensure RLS policies and auth config are covered in findings
- Want to track fixes? Create a plan with `/engineer-plan`
- Fixed issues? Re-run `/security-audit` to verify
