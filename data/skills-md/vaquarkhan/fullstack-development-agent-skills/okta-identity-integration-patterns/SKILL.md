---
name: okta-identity-integration-patterns
description: Integrate Okta for enterprise identity workflows including OIDC login, group claims, and policy-based access controls. Use when implementing workforce or B2B identity scenarios.
disable-model-invocation: true
---

# Okta Identity Integration Patterns

## Use When

- Enterprise SSO is required
- Role or group-based access must map from identity provider claims

## Workflow

1. Configure Okta app integrations for frontend and backend clients.
2. Map groups, roles, and claims to application authorization model.
3. Implement OIDC login, callback, and logout flows.
4. Enforce token and session validation in API gateway and services.
5. Add break-glass and operational procedures for identity outages.

## Required Checks

- Group and role mappings are least-privilege by default
- AuthN/AuthZ behavior remains consistent across environments
- Audit logs include identity, action, and policy decision

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

- Okta integration is secure, observable, and operable
- Enterprise access scenarios work without privilege escalation gaps
