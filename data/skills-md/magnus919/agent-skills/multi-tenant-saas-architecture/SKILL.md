---
name: multi-tenant-saas-architecture
description: >-
  Design and review end-to-end multi-tenant SaaS architectures: tenant and
  subscription semantics, control and application planes, pooled or isolated
  tenancy, onboarding, entitlements, metering, billing handoffs, lifecycle,
  partitioning, and tenant-aware operations. Use when a subscription product
  needs a coherent tenant model and architecture decision across these seams.
  Do not use for threat modeling or isolation controls, API contract semantics,
  data-platform design, backend implementation, migration execution, privacy
  compliance artifacts, capacity evidence, financial modeling, or infrastructure
  operations; route those to the named specialist owners.
license: MIT
compatibility: Platform-agnostic methodology. No runtime dependencies.
metadata:
  tags: multi-tenant, saas, control-plane, application-plane, tenancy, entitlements, billing
---

# Multi-Tenant SaaS Architecture

Use this skill to join product tenancy semantics to system boundaries and operating decisions. It owns the cross-cutting architecture choice, not the implementation or specialist evidence behind each choice.

## Workflow

1. **Frame the service promise.** Identify customer/account shape, users and operators, subscription commitments, regions, data classes, lifecycle states, support model, scale assumptions, and unknowns. Separate contractual promises from aspirations.
2. **Define tenant semantics.** Load `references/tenant-domain-model-and-boundaries.md`. Establish tenant, account, organization, user, membership, subscription, entitlement, resource, and environment meanings, ownership, cardinality, and lifecycle authority.
3. **Separate planes.** Load `references/control-and-application-planes.md`. Draw the control-plane policy and lifecycle responsibilities apart from application-plane request and data serving, including asynchronous handoffs and failure behavior.
4. **Choose isolation per resource.** Load `references/tenancy-and-data-partitioning-models.md`. Compare pooled, bridge, silo, and hybrid choices by data, compute, cache, queue, search, and operational resource. Record why the choice meets the promise and what can trigger a change.
5. **Connect the commercial path.** Load `references/onboarding-identity-entitlements-metering-billing.md`. Trace signup, identity, provisioning, configuration, entitlement evaluation, usage capture, invoice authority, suspension, support, and reactivation without making billing or security policy implicit.
6. **Design lifecycle and operations.** Load `references/tenant-aware-operations-capacity-and-cost.md`. Cover deployment, observability, quotas, hot tenants, restore scope, export/deletion, cost attribution, and escalation. Route evidence-heavy decisions to the specialist owners.
7. **Record and challenge.** Use `templates/saas-architecture-brief.md`, `templates/tenancy-decision-record.md`, and `templates/tenant-lifecycle-checklist.md`. Test cross-tenant safety, lifecycle idempotency, entitlement lag, billing disagreement, restore scope, and noisy-neighbor behavior.

## Output Contract

Produce a SaaS architecture brief with: service promise; domain vocabulary and authorities; control/application plane boundary; resource-by-resource tenancy choices; lifecycle state transitions; entitlement, metering, and billing handoffs; data and recovery boundaries; tenant-aware operational scenarios; explicit assumptions and evidence gaps; specialist handoffs; and decisions with owners and review triggers.

## Ownership Boundaries

- Threat modeling, authorization, tenant isolation controls, secrets, and security evidence belong to [`secure-software-engineering`](../secure-software-engineering/SKILL.md).
- Capacity models, load or soak evidence, quotas as capacity controls, unit cost, and SLO-cost tradeoffs belong to [`capacity-and-cost-engineering`](../capacity-and-cost-engineering/SKILL.md).
- Pricing, ARR/MRR, churn, retention, margin, and SaaS financial outcomes belong to [`financial-modeling`](../financial-modeling/SKILL.md).
- Infrastructure, networking, deployment, observability substrate, and secret-management implementation belong to [`platform-engineering`](../platform-engineering/SKILL.md).
- API, event, webhook, schema, compatibility, and deprecation contracts belong to [`api-design-and-evolution`](../api-design-and-evolution/SKILL.md).
- Service code, data access, jobs, integrations, and application-level tests belong to [`backend-engineering`](../backend-engineering/SKILL.md).
- Storage-platform, data-model, data-product, and governance decisions belong to [`data-architect`](../data-architect/SKILL.md); lifecycle deletion requirements and verification belong to [`privacy-engineering`](../privacy-engineering/SKILL.md).
- Cross-system tenant moves, partition migrations, cutovers, reconciliation, and deprecation execution belong to [`migration-engineering`](../migration-engineering/SKILL.md).
- General system boundary and architecture-quality decisions belong to [`software-architecture`](../software-architecture/SKILL.md); this skill adds SaaS tenant and commercial lifecycle semantics to that decision.

## When Not To Use

Do not use this skill for an isolated security review, API contract, data-platform choice, service implementation, migration plan, privacy artifact, capacity study, financial model, or platform runbook. Start with the narrower owner when the SaaS context is incidental. For a general architecture decision with no tenant lifecycle or subscription boundary, use [`software-architecture`](../software-architecture/SKILL.md).

## Reference Guide

| Load when | Reference or template |
|---|---|
| Defining tenant/account/subscription terms and ownership | `references/tenant-domain-model-and-boundaries.md` |
| Splitting lifecycle policy from request serving | `references/control-and-application-planes.md` |
| Comparing pooled, bridge, silo, or hybrid isolation | `references/tenancy-and-data-partitioning-models.md` |
| Connecting signup, identity, entitlements, usage, and billing | `references/onboarding-identity-entitlements-metering-billing.md` |
| Planning tenant-aware operations, restore, fairness, and unit-cost inputs | `references/tenant-aware-operations-capacity-and-cost.md` |
| Producing the overall architecture artifact | `templates/saas-architecture-brief.md` |
| Capturing a tenancy choice and trigger to revisit it | `templates/tenancy-decision-record.md` |
| Checking tenant lifecycle completeness | `templates/tenant-lifecycle-checklist.md` |
| Reviewing public provenance and transformation limits | `references/source-index.md` |

## Completion

Stop when each material SaaS decision has an accountable owner, alternatives and consequences, a lifecycle and failure path, evidence or a named gap, and an explicit specialist handoff. Escalate unresolved tenant authority, isolation, commercial, privacy, or recovery questions rather than inventing policy.
