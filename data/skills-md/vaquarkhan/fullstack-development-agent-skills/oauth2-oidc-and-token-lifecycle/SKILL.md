---
name: oauth2-oidc-and-token-lifecycle
description: Implement OAuth 2.0 and OpenID Connect flows with secure token lifecycle handling across frontend and backend. Use for SSO, delegated access, and standards-based identity architecture.
disable-model-invocation: true
---

# OAuth2 OIDC And Token Lifecycle

## Use When

- Building SSO or federated login
- Implementing delegated API access with standards-based tokens

## Workflow

1. Select grant types per client (PKCE for public clients, client credentials for machine clients).
2. Define token claims, scopes, and audience boundaries.
3. Implement secure token validation on backend services.
4. Design refresh, rotation, revocation, and session expiry behavior.
5. Add observability for auth failures and suspicious token usage.

## Provider And Flow Guidance

- Prefer authorization code with PKCE for browser and mobile clients.
- Keep access tokens short-lived; use refresh tokens with rotation for longer sessions.
- Validate tokens at every trust boundary; never trust client-side checks alone.
- Map scopes to business actions, not broad technical group names.

## Required Checks

- Token signature, issuer, audience, and expiry are validated server-side
- Scope and claim checks are enforced per protected endpoint
- Token refresh and revocation paths are deterministic

## Decision Framework

- Prefer authorization code with PKCE for browser and mobile clients.
- Keep access tokens short-lived; use refresh tokens with rotation for longer sessions.
- Validate tokens at every trust boundary; never trust client-side checks alone.
- Map scopes to business actions, not broad technical group names.

## Common Rationalizations And Rebuttals

- "Client already checked auth." -> Client checks are bypassable; enforce authorization server-side.
- "Long-lived access tokens reduce complexity." -> They increase blast radius after compromise.
- "Any valid token should work across APIs." -> Enforce audience restrictions to avoid token confusion.

## Evidence Pack

- Flow diagram covering login, refresh, logout, and revocation
- Negative test evidence for invalid issuer, expired token, wrong audience, and missing scope
- Key rotation or JWKS failure handling notes
- Security alert dashboard for auth anomalies

## Exit Criteria

- Identity flows are standards-compliant and secure
- Token misuse and failure modes are detectable and recoverable
