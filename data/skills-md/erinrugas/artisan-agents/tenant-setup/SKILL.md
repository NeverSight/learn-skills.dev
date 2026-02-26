---
name: tenant-setup
description: >-
  Configures multi-tenant onboarding and baseline tenant data.
  Use when creating a new tenant/customer workspace and validating tenant isolation.
---

# Tenant Setup Skill

## When to Apply
- User needs new tenant/account setup.
- Multi-tenant bootstrap data or access configuration is required.

## Workflow
1. Read tenancy rules from `specs/specs.md` and `specs/security-spec.md`.
2. Create tenant record and initial admin/user roles.
3. Seed tenant-scoped baseline data.
4. Validate tenant isolation with at least one cross-tenant negative check.

## Quality Bar
- No global data leakage.
- Tenant IDs/scopes applied at write and read paths.
- Onboarding is repeatable via script/seeder where possible.
