---
name: authentication-and-authorization-fullstack
description: Implement end-to-end authentication and authorization across frontend and backend with secure session design, token lifecycle controls, and role or permission enforcement. Use for login, access control, and identity-related changes.
disable-model-invocation: true
---

# Authentication And Authorization Fullstack

## Use When

- Adding login, signup, SSO, or session refresh flows
- Enforcing role-based or permission-based access across UI and API
- Reviewing security controls for identity-sensitive features

## Workflow

1. Define identity model (users, tenants, roles, permissions, claims).
2. Choose session strategy (cookie session, JWT, or hybrid) with threat model.
3. Implement backend middleware or guards for coarse and fine-grained authorization.
4. Implement frontend route and component guards without exposing privileged actions.
5. Add audit logs for sensitive operations and failed access attempts.
6. Validate token expiry, refresh flow, revocation, and logout semantics.

## Security Guardrails

- Avoid storing long-lived sensitive tokens in unsafe browser storage
- Enforce CSRF protection for cookie-based sessions
- Validate issuer, audience, and signature for all tokens
- Use least-privilege defaults for service-to-service permissions
- Ensure authorization checks are server-side source of truth

## Required Checks

- Privileged endpoints reject unauthorized or malformed claims
- UI does not reveal restricted controls for unauthorized identities
- Session invalidation works across browser tabs and devices where required
- Audit events contain actor, action, scope, and timestamp

## Decision Framework

- Enforce server-side authorization as the source of truth for access decisions.
- Use least-privilege scopes and role mappings by default.
- If tokens are used, define validation, rotation, and revocation behavior explicitly.
- If external identity providers are involved, define outage and fallback behavior.

## Common Rationalizations And Rebuttals

- "Client checks are enough." -> Client logic is bypassable; enforce checks on backend boundaries.
- "Broad scopes are easier to manage." -> Broad scopes increase blast radius and compliance risk.
- "We can add audit logs later." -> Missing audit evidence blocks incident and compliance response.

## Evidence Pack

- Negative test cases for unauthorized and malformed access attempts
- Scope-to-permission mapping with owner approval
- Token/session lifecycle flow and revocation behavior proof
- Audit and security monitoring evidence for sensitive operations

## Exit Criteria

- Auth flows are secure, reliable, and user-comprehensible
- Authorization behavior is consistent between UI and API
- Security review checklist is completed with evidence
