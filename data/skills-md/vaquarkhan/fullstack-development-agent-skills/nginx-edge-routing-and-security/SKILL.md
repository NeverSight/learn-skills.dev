---
name: nginx-edge-routing-and-security
description: Configure NGINX for reverse proxy routing, TLS termination, security headers, rate controls, and resilient upstream handling. Use for internet-facing edge and gateway traffic management.
disable-model-invocation: true
---

# NGINX Edge Routing And Security

## Use When

- NGINX is used as ingress, reverse proxy, or edge gateway
- Teams need stronger edge security and request control

## Workflow

1. Define route topology, upstream pools, and health checks.
2. Configure TLS, HSTS, and secure header policies.
3. Apply request limits, throttling, and abuse controls.
4. Add caching and compression with explicit invalidation policy.
5. Instrument logs and metrics for edge behavior and anomalies.

## Required Checks

- Upstream failover and timeout behavior is tested
- Security headers and TLS configuration meet policy requirements
- Rate limiting protects backend dependencies without false positives

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

- NGINX edge behavior is predictable under load and failure
- Security posture is enforceable and observable
