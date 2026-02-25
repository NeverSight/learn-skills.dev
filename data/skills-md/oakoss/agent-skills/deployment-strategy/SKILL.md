---
name: deployment-strategy
description: |
  Deployment strategy patterns for zero-downtime releases. Covers blue-green, canary, rolling, and recreate strategies with rollback procedures, health checks, feature flags, progressive delivery, and environment promotion workflows.

  Use when choosing a deployment strategy, implementing rollback procedures, configuring health checks, setting up environment promotion pipelines, planning progressive delivery with feature flags, or reducing blast radius during releases.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Deployment Strategy

## Overview

Covers deployment strategy selection, rollback safety, and progressive delivery patterns. Focuses on zero-downtime release techniques, blast radius management, and environment promotion workflows from development through production.

**When to use:** Choosing between blue-green, canary, or rolling deployments, implementing rollback procedures, configuring health checks and readiness gates, planning environment promotion workflows, integrating feature flags for progressive delivery.

**When NOT to use:** CI/CD pipeline mechanics and GitHub Actions workflows (use `ci-cd-architecture` skill), infrastructure provisioning and cloud platform selection (use `ci-cd-architecture` skill), application architecture decisions (use framework-specific skills).

## Quick Reference

| Need                        | Strategy                                                        |
| --------------------------- | --------------------------------------------------------------- |
| Instant rollback            | Blue-green (swap traffic back to previous environment)          |
| Gradual risk validation     | Canary (route 1-5% traffic, monitor, then expand)               |
| Default Kubernetes updates  | Rolling (replace pods incrementally with maxSurge/maxUnavail)   |
| Full environment replace    | Recreate (stop all old, start all new; accepts brief downtime)  |
| Feature-level control       | Feature flags (decouple deploy from release)                    |
| Database schema changes     | Expand-contract migration (additive first, remove later)        |
| Multi-environment promotion | dev -> staging -> production with gates between each            |
| Blast radius reduction      | Canary + feature flags + automated rollback triggers            |
| Health verification         | Liveness, readiness, and startup probes at infrastructure level |
| Rollback without redeploy   | Feature flags to disable problematic code paths                 |

## Common Mistakes

| Mistake                                               | Correct Pattern                                                                         |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------- |
| No rollback plan before deploying                     | Define rollback procedure and verify it works before every production release           |
| Destructive database migrations alongside app deploy  | Use expand-contract: add new columns/tables first, migrate data, remove old later       |
| Canary without automated health monitoring            | Set error rate and latency thresholds that auto-halt rollout when breached              |
| Blue-green with shared mutable database               | Use backward-compatible schema changes so both versions work against the same database  |
| Feature flags without cleanup lifecycle               | Assign an owner and removal date to every flag; treat stale flags as tech debt          |
| Skipping staging and deploying directly to production | Promote through environments with automated gates between each stage                    |
| Rolling deploy without readiness probes               | Configure readiness probes so traffic routes only to healthy instances                  |
| Same environment config across all stages             | Use environment-specific configuration with secrets management per environment          |
| Manual rollback procedures in incident response       | Automate rollback triggers based on error rate, latency, and health check thresholds    |
| Testing only happy paths before release               | Include failure scenario testing: rollback drills, chaos testing, degraded mode testing |

## Delegation

- **Audit deployment safety of existing infrastructure**: Use `Explore` agent to review deployment configs, health check definitions, and rollback procedures
- **Implement a specific deployment strategy**: Use `Task` agent to configure blue-green, canary, or rolling deployment for a target platform
- **Plan migration from one deployment strategy to another**: Use `Plan` agent to evaluate current strategy, define migration steps, and identify risks

> If the `ci-cd-architecture` skill is available, delegate CI/CD pipeline setup and GitHub Actions workflow configuration to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill ci-cd-architecture`

## References

- [Blue-green, canary, rolling, and recreate deployment strategies with configuration examples](references/deployment-patterns.md)
- [Rollback procedures, health checks, feature flags, and blast radius management](references/rollback-and-safety.md)
- [Environment promotion workflows, configuration management, and secrets handling](references/environment-management.md)
