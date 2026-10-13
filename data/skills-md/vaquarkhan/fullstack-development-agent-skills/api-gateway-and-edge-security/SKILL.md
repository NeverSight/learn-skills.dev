---
name: api-gateway-and-edge-security
description: Design API gateway policies for auth, rate limits, WAF controls, request validation, and zero-trust edge posture. Use for internet-facing APIs and multi-client access management.
disable-model-invocation: true
---

# API Gateway And Edge Security

## Use When

- Exposing APIs to public clients or partners
- Centralized edge policy is required for governance

## Workflow

1. Define route-level authn and authz requirements.
2. Configure request validation and schema enforcement at edge.
3. Apply IP, token, and tenant-aware rate limiting.
4. Add WAF, bot mitigation, and abuse detection rules.
5. Emit security audit logs and anomaly alerts.

## Required Checks

- Unauthorized traffic is blocked before backend invocation
- Sensitive headers and payload fields are sanitized
- Rate limits protect downstream services under burst traffic

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

- Edge security posture is enforceable and monitored
- API consumers receive consistent error and quota semantics
