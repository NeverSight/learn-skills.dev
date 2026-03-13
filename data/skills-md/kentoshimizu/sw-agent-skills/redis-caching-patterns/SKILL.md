---
name: redis-caching-patterns
description: "Redis caching workflow for latency improvement with explicit key strategy, TTL/invalidation policy, and correctness bounds. Use when Redis-backed caching decisions are required for application performance; do not use for repository-wide architecture governance or release management policy."
---

# Redis Caching Patterns

## Overview
Use this skill to design cache behavior that improves performance without silently violating correctness expectations.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Cache invalidation rules:
  - `references/cache-invalidation-rules.md`

## Templates And Assets
- Redis cache policy template:
  - `assets/redis-cache-policy-template.md`
- Cache observability checklist:
  - `assets/cache-observability-checklist.md`

## Inputs To Gather
- Read/write hotspots and latency objectives.
- Freshness and consistency constraints.
- Redis memory/eviction limits.
- Failure/degradation expectations.

## Deliverables
- Key namespace and TTL/invalidation policy.
- Stampede/hot-key mitigation plan.
- Cache observability and operational guardrails.

## Workflow
1. Define cache policy in `assets/redis-cache-policy-template.md`.
2. Apply freshness/invalidation rules from `references/cache-invalidation-rules.md`.
3. Validate stampede and hot-key behavior.
4. Define failure behavior for cache misses/outages.
5. Finalize with `assets/cache-observability-checklist.md`.

## Quality Standard
- Key strategy is consistent and ownership is explicit.
- Invalidation policy matches correctness requirements.
- Failure paths preserve system correctness.
- Observability supports rapid cache regression diagnosis.

## Failure Conditions
- Stop when invalidation policy cannot satisfy correctness bounds.
- Stop when cache behavior is unobservable in production.
- Escalate when caching introduces tail-latency or error regressions.
