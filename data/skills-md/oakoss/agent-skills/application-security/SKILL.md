---
name: application-security
description: 'Comprehensive application security covering threat modeling (STRIDE), OWASP Top 10 (2025), OWASP API Security Top 10 (2023), secure coding review, authentication/authorization patterns, input validation, encryption, security headers, supply chain security, compliance (GDPR/HIPAA/SOC2/PCI-DSS), and security monitoring. Use when reviewing code for vulnerabilities, implementing auth patterns, securing APIs, configuring security headers, hardening supply chain, preventing injection attacks, or preparing for compliance audits.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Security

Security is built-in, not bolted-on. Every feature, endpoint, and data flow must consider security implications.

## OWASP Top 10 (2025)

| #   | Vulnerability                      | Prevention                                      |
| --- | ---------------------------------- | ----------------------------------------------- |
| 1   | Broken Access Control              | Verify permissions server-side, default deny    |
| 2   | Security Misconfiguration          | Secure defaults, remove unused features         |
| 3   | Software Supply Chain Failures     | SBOM, dependency scanning, signed builds        |
| 4   | Cryptographic Failures             | Use TLS, hash passwords (argon2id), encrypt PII |
| 5   | Injection                          | Parameterized queries, input validation         |
| 6   | Insecure Design                    | Threat modeling, security requirements          |
| 7   | Authentication Failures            | Strong passwords, MFA, secure session mgmt      |
| 8   | Software or Data Integrity         | Verify dependencies, sign releases              |
| 9   | Logging and Alerting Failures      | Log security events, set up alerts              |
| 10  | Mishandling Exceptional Conditions | Fail securely, generic errors to clients        |

## Security Principles

| Principle          | Rule                                                      |
| ------------------ | --------------------------------------------------------- |
| Defense in Depth   | Multiple layers: firewall, auth, authz, encryption, audit |
| Least Privilege    | Minimum permissions needed, nothing more                  |
| Zero Trust         | Never trust, always verify. Assume breach.                |
| Secure by Default  | HTTPS, strict passwords, secure cookies out of the box    |
| Fail Securely      | Access denied on error, no internal details to users      |
| Validate on Server | Client validation is UX, server validation is security    |

## Pre-Deployment Checklist

| Area          | Requirements                                                        |
| ------------- | ------------------------------------------------------------------- |
| Passwords     | Hashed with argon2id (preferred) or bcrypt (12+ rounds)             |
| Tokens        | JWT with EdDSA/ES256, 15min access / 7d refresh, httpOnly cookies   |
| Sessions      | HttpOnly, Secure, SameSite=Strict cookies                           |
| Rate Limiting | Auth endpoints: 5 attempts/15min                                    |
| Authorization | All routes check auth server-side, default deny                     |
| Input         | Validated with schema (Zod), parameterized SQL                      |
| Uploads       | Whitelist types, enforce size limits                                |
| Secrets       | No secrets in code or VCS                                           |
| Headers       | CSP (with nonces), HSTS, Permissions-Policy, X-Content-Type-Options |
| CORS          | Configured restrictively                                            |
| Encryption    | PII encrypted at rest (AES-256) and in transit (TLS 1.3)            |
| Logging       | Audit logging for security events                                   |
| Dependencies  | SBOM generated, `npm audit` clean, Dependabot enabled               |

## Threat Modeling (STRIDE)

| Threat                 | Category        | Key Mitigations                                        |
| ---------------------- | --------------- | ------------------------------------------------------ |
| Spoofing               | Authentication  | MFA, strong passwords, JWT with short expiry           |
| Tampering              | Integrity       | Input validation, HTTPS/TLS, signed tokens             |
| Repudiation            | Accountability  | Audit logging, digital signatures                      |
| Info Disclosure        | Confidentiality | Encryption, least privilege, secret management         |
| Denial of Service      | Availability    | Rate limiting, input validation, CDN/DDoS protection   |
| Elevation of Privilege | Authorization   | Authz checks on every request, ABAC, permission audits |

## Risk Levels

| Level    | Action                    |
| -------- | ------------------------- |
| Critical | Immediate action required |
| High     | Address before launch     |
| Medium   | Address post-launch       |
| Low      | Monitor, may accept risk  |

## Compliance Overview

| Framework | Scope              | Key Requirements                                                   |
| --------- | ------------------ | ------------------------------------------------------------------ |
| GDPR      | EU data subjects   | Consent, data subject rights, breach notification (72h), DPIA      |
| HIPAA     | US healthcare data | PHI encryption, RBAC, audit logs, BAA with providers               |
| SOC 2     | SaaS customer data | Security policies, MFA, encryption, incident response              |
| PCI-DSS   | Credit card data   | Use payment processor (Stripe), tokenization, network segmentation |

## Anti-Patterns

| Anti-Pattern                                  | Fix                                              |
| --------------------------------------------- | ------------------------------------------------ |
| Security as afterthought                      | Integrate from design phase                      |
| Client-side authorization                     | Always verify permissions server-side            |
| Trusting client data (e.g., userId from body) | Get user ID from authenticated session           |
| Rolling your own crypto                       | Use proven libraries (argon2, bcrypt, libsodium) |
| Compliance = security                         | Compliance is the minimum; security is ongoing   |
| Verbose error responses                       | Generic messages to clients, details server-side |

## Common Mistakes

| Mistake                                                       | Correct Pattern                                                     |
| ------------------------------------------------------------- | ------------------------------------------------------------------- |
| Performing authorization checks only on the client side       | Always verify permissions server-side; client checks are UX only    |
| Trusting user-supplied IDs from request body (e.g., userId)   | Derive user identity from the authenticated session or token        |
| Rolling custom cryptography instead of using proven libraries | Use argon2id, bcrypt, or libsodium for all cryptographic operations |
| Treating compliance certification as equivalent to security   | Compliance is the minimum bar; security requires ongoing review     |
| Returning verbose error messages with stack traces to clients | Show generic messages to clients; log details server-side only      |

## Delegation

- **Scan codebase for OWASP Top 10 vulnerabilities and insecure patterns**: Use `Explore` agent to search for SQL injection, XSS, and hardcoded secrets
- **Implement authentication, authorization, and security headers end-to-end**: Use `Task` agent to configure JWT, RBAC, CSP, HSTS, and rate limiting
- **Design a threat model and security architecture for new features**: Use `Plan` agent to apply STRIDE methodology and map trust boundaries

> For database-layer security (RLS policies, Postgres/Supabase hardening, audit trails), use the `database-security` skill. For AI/LLM security (prompt injection defense, agentic zero-trust, MCP tool hardening), use the `secure-ai` skill.

## References

- [Threat Modeling](references/threat-modeling.md) — STRIDE methodology, risk assessment process, trust boundaries
- [Authentication and Authorization](references/auth.md) — JWT, session-based, OAuth, RBAC, ABAC, IDOR protection
- [API Security](references/api-security.md) — OWASP API Security Top 10, object-level authorization, rate limiting, SSRF prevention, security testing
- [Input Validation](references/input-validation.md) — SQL injection, XSS, command injection, path traversal, Zod validation, file upload security
- [Data Protection](references/data-protection.md) — Password hashing (argon2id/bcrypt), AES-256-GCM encryption, secrets management
- [Secure Configuration](references/secure-config.md) — Security headers, CORS, Express hardening, rate limiting
- [Supply Chain Security](references/supply-chain.md) — SBOM generation, dependency scanning, CI/CD hardening, artifact signing
- [Monitoring and Compliance](references/monitoring-compliance.md) — Audit logging, error handling, GDPR/HIPAA/SOC2/PCI-DSS, troubleshooting
