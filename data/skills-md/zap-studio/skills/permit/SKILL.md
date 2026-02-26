---
name: permit
description: Use when defining authorization policies, resource/action permissions, or role hierarchies with @zap-studio/permit.
---

# permit

## Overview

Type-safe, declarative authorization policies with Standard Schema-compatible resources.

## When to Use

- Defining permissions for resources and actions
- Modeling role hierarchies or composable access rules
- Replacing ad-hoc `if` checks with auditable policy rules

## When Not to Use

- Simple apps with a single hardcoded allow/deny check

## Quick Reference

- Policy: `createPolicy`
- Rules: `allow`, `deny`, `when`
- Conditions: `and`, `or`, `not`, `has`, `hasRole`
- Evaluate: `policy.can(ctx, action, resourceName, resource)`
- Merge: `mergePolicies` or `mergePoliciesAny`

## Inputs to Request

- Resource schemas and action lists
- Context shape (user, role, tenancy)
- Required rules and edge cases

## Resources

- https://www.zapstudio.dev/packages/permit
- https://www.zapstudio.dev/llms.txt
