---
name: security-by-design
description: How to make security an architectural PROPERTY. Use for auth, authorization, secrets, encryption, injection/XSS/CSRF/SSRF, rate limiting, multi-tenancy isolation, AI/prompt-injection security, compliance, audit logs, security review.
when_to_use: |
  - authentication, authorization, secrets, encryption
  - SQL injection, XSS, CSRF, SSRF, rate limiting
  - multi-tenancy isolation, AI prompt-injection, compliance
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Security by Design

Security is not a feature — it is an **architectural property**. Every component protects itself.
Design security from the start; never bolt it on after implementation.

## Golden rule & zero trust

Everything is hostile until proven otherwise — users, browsers, requests, headers, files, cookies,
3rd-party APIs, AI outputs, internal services. Every input is validated. Never assume *internal =
safe*: every service authenticates, every request authorizes, every resource verifies permissions.

**Least privilege:** every user, service, key, token, worker gets only the permissions required.

## AuthN & AuthZ

- **Authentication** (*who are you?*): prefer managed (WorkOS, Auth0, Clerk, Better Auth, Cognito,
  Supabase, Firebase). Build custom only when necessary.
- **Authorization** (*what may you do?*): backend domain logic — never trust frontend checks.
- **RBAC** (Admin/Manager/User/Viewer) for simple systems; **ABAC** for enterprise/compliance.
- **Resource ownership:** who owns it, who can read/update/delete/share — explicit.
- **MFA** for admins, finance, infra, production, sensitive ops.

## Secrets & encryption

- **Secrets:** never hardcode / commit / log / expose to frontend. Use Vault / cloud secret store /
  env vars (config, not security). Rotate regularly.
- **API keys:** store hash + identifier + scopes + expiration + owner. **Passwords:** salted,
  adaptive, hashed (Argon2id / bcrypt / scrypt) — never SHA256/MD5.
- **Sessions:** secure, HTTP-only, SameSite, short-lived + refresh. **JWT:** identity token, not a
  DB — never embed permissions/profiles/business data.
- **Encryption:** passwords, tokens, PII, financial data, backups via proven libraries. **OAuth**
  for Google/Microsoft/GitHub/Apple/SSO.

## Threat defenses

| Threat | Defense |
|---|---|
| Injection | Parameterized queries / ORM / prepared statements — never string concat |
| XSS | Escape output, sanitize HTML, CSP — never trust user content |
| CSRF | Tokens, SameSite cookies, origin validation |
| SSRF | No arbitrary URLs; whitelist domains, restrict metadata |
| Command injection | No user input in shell/SQL/system commands |
| File uploads | Validate size/type/MIME, virus-scan, never execute |
| AI output | Validate tool calls / SQL / code / URLs; treat as untrusted |

## Protection & ops

- **Rate limiting** on login/reset/register/AI/payments/search/uploads — different limits per endpoint.
- **DDoS:** CDN, WAF, caching, queue, autoscaling, graceful degradation. Never expose infra directly.
- **AI security:** prompt injection — treat retrieved docs as hostile, never let them override system
  instructions; separate instructions from knowledge; scoped tool permissions; sandbox generated code.
- **Logging:** never log passwords/tokens/cookies/secrets/PII; mask. **Audit logs:** auth, authZ,
  permission/billing/admin/prod changes — immutable.
- **Compliance:** GDPR/HIPAA/SOC2/ISO27001/PCI influence architecture. **Multi-tenancy:** enforce
  tenant isolation on every query; never trust frontend tenant IDs.
- **Backups:** encrypted, versioned, tested, recoverable, separate. **Dependencies:** update/scan/
  remove unused. **Headers:** HSTS, CSP, X-Frame-Options, etc. — secure by default.

## Security review checklist

- [ ] AuthN · AuthZ · Validation · Encryption · Secret mgmt · Rate limiting · Audit logs
- [ ] Tenant isolation · Input sanitization · File validation · Dependency scan · Security headers
- [ ] Backup strategy · Recovery plan · Monitoring · Alerting

## Security mindset

Continuously ask: what if this request is malicious? key leaks? server compromised? dependency
malicious? model hallucinates? user is an attacker? Design the answers before coding.

## Architecture decision tree

```
Need to protect the system?
  ↓
Consumer / SaaS? → Build auth? NO → Clerk / Better Auth / Supabase / WorkOS
Enterprise / SSO? → WorkOS / Keycloak / Cognito
Sensitive role? → Require MFA
Every request → authenticate + authorize + validate
AI feature? → model output untrusted → sandbox + verify
Store secret? → Vault / secret manager (never repo, never logs)
Multi-tenant? → enforce isolation on every query
```

## Anti-patterns

- ❌ Adding security after implementation
- ❌ Trusting frontend authorization checks
- ❌ Hardcoding / committing / logging secrets · SHA256/MD5 for passwords
- ❌ String-concatenated SQL · trusting LLM output without verification
- ❌ Executing generated code on production · storing secrets/files in frontend
- ❌ Assuming internal = safe · multi-tenant queries without isolation

## Architecture prompts

- What if this request is malicious?
- What if this API key / token leaks?
- What if this dependency is compromised?
- What if the model hallucinates or is injected?
- Is authorization enforced server-side, not just in the UI?
- Does every query enforce tenant isolation? Can this secret rotate without downtime?
