---
name: security-authorization
description: "Security workflow for authorization boundaries, least-privilege policy, and enforcement design. Use when permission models, access decisions, or privileged action controls are required; do not use for authentication factor selection or non-security quality tuning."
---

# Security Authorization

## Overview
Use this skill to build authorization systems that enforce least privilege across APIs, UI actions, and background jobs.

## Scope Boundaries
- Role/permission models are being introduced or revised.
- Resource-scoped access control must be consistent across services.
- Privileged workflows require explicit separation-of-duty controls.

## Templates And Assets
- Authorization policy matrix:
  - `assets/authorization-policy-matrix-template.md`

## Inputs To Gather
- Actor categories, resources, and sensitive actions.
- Data classification and tenant or domain boundaries.
- Existing policy model and enforcement points (API gateway, service layer, DB layer).
- Abuse scenarios (horizontal/vertical privilege escalation, confused deputy, missing object-level checks).

## Deliverables
- Authorization model (RBAC, ABAC, ReBAC, or hybrid) with policy decision rules.
- Enforcement map (where decisions are made and where they are enforced).
- Default-deny and exception policy with break-glass controls.
- Verification plan for privilege escalation and cross-tenant isolation tests.

## Workflow
1. Enumerate subject-action-resource tuples and fill `assets/authorization-policy-matrix-template.md`.
2. Select model based on change frequency, policy complexity, and auditability requirements.
3. Define canonical policy evaluation order and conflict resolution rules.
4. Ensure object-level authorization is checked server-side for every mutable/read-sensitive path.
5. Specify admin and break-glass flows with time limits, approval, and audit logging.
6. Validate policy propagation consistency across UI hints and backend enforcement.
7. Run abuse-case tests for IDOR, privilege creep, and stale privilege revocation.

## Quality Standard
- Authorization decisions are default-deny and centrally explainable.
- Every privileged operation has a single source of policy truth.
- Policy updates are auditable and revocation latency is acceptable.
- Cross-tenant and cross-domain boundaries are explicitly tested.

## Failure Conditions
- Stop when enforcement relies on client-side checks.
- Stop when policy conflicts are unresolved or implicit.
- Escalate when least-privilege requirements cannot be implemented without structural change.
