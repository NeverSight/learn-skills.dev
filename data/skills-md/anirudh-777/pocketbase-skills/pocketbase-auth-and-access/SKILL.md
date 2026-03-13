---
name: pocketbase-auth-and-access
description: Use when you specifically need detailed PocketBase auth and authorization rule design beyond the orchestrator quick actions
---

# PocketBase Auth and Access (Advanced)

## Overview
Use this only for deeper auth/rule design. Default to `pocketbase-agent-orchestrator` for standard operations.

## Focus
- Auth flows (email/password, OAuth)
- Collection access rules (`list/view/create/update/delete`)
- Ownership and tenant membership checks

## Minimal Workflow
1. Define actor types and trust boundaries.
2. Set least-privilege rules per collection operation.
3. Verify unauthorized and cross-tenant failures.
4. Align with API integration and incident checks.

## References
- [rule-patterns.md](references/rule-patterns.md)
- [auth-flow-checklist.md](references/auth-flow-checklist.md)
- [multitenancy-pattern.md](references/multitenancy-pattern.md)
