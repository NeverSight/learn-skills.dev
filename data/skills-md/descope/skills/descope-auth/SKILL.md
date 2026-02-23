---
name: descope-auth
description: Integrate Descope authentication into applications. Use when implementing login, signup, passwordless auth (OTP, Magic Link, Passkeys), OAuth, SSO, or MFA. Detects framework and provides targeted guidance.
---

# Descope Authentication

Integrate secure, passwordless authentication using Descope Flows and SDKs.

## Framework Detection

Detect the user's framework and use the appropriate reference:

| If project has... | Use reference |
|-------------------|---------------|
| `next` in package.json | `references/nextjs.md` |
| `react` (no Next.js) | `references/react.md` |
| Python/Node.js backend only | `references/backend.md` |

## Quick Start (all frameworks)

1. Get Project ID from https://app.descope.com/settings/project
2. Set environment variable: `NEXT_PUBLIC_DESCOPE_PROJECT_ID=<your-id>`
3. Follow framework-specific reference

## Valid Flow IDs (CRITICAL - do not invent others)

| Flow ID | Purpose |
|---------|---------|
| `sign-up-or-in` | Combined signup/login (RECOMMENDED) |
| `sign-up` | Registration only |
| `sign-in` | Login only |
| `step-up` | MFA step-up authentication |
| `update-user` | Profile updates, add auth methods |

## Authentication Methods

| Method | When to use |
|--------|-------------|
| OTP (Email/SMS) | Quick verification codes |
| Magic Link | Passwordless email links |
| Passkeys | Biometric/WebAuthn (most secure) |
| OAuth | Social login (Google, GitHub, etc.) |
| SSO | Enterprise SAML/OIDC |
| Passwords | Traditional auth (not recommended) |

## DO NOT (Security Guardrails)

- DO NOT parse JWTs manually - always use SDK's `validateSession()`
- DO NOT store tokens in localStorage - SDK handles this securely
- DO NOT invent flow IDs - only use IDs from the table above
- DO NOT skip server-side validation - always validate on backend
- DO NOT expose DESCOPE_MANAGEMENT_KEY in client code

## References

- `references/nextjs.md` - Next.js App Router integration
- `references/react.md` - React SPA integration  
- `references/backend.md` - Backend session validation
