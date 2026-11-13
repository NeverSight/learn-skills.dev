---
name: fullstack-observability-and-release-engineering
description: Operate fullstack systems with practical observability, release safety controls, incident readiness, and rollback discipline. Use when preparing production rollouts or improving service reliability.
disable-model-invocation: true
---

# Fullstack Observability And Release Engineering

## Use When

- Shipping high-risk fullstack changes
- Improving production readiness and incident recovery
- Standardizing release and rollback practices

## Workflow

1. Define service level indicators and objectives for user-critical paths.
2. Instrument frontend and backend for logs, metrics, traces, and business events.
3. Build dashboards and alerts tied to customer impact, not infrastructure noise.
4. Design rollout strategy (feature flags, canary, shadow, phased traffic shift).
5. Define rollback triggers, ownership, and communication protocol.
6. Run post-release verification and document lessons learned.

## Observability Baseline

- Correlation ID propagation from browser to backend service graph
- Error classification by user-facing severity and recoverability
- Latency percentiles per endpoint and key page interactions
- Queue depth and retry metrics for asynchronous pipelines
- Alert routes and escalation paths for on-call responders

## Required Checks

- Feature flags have default fallback and kill switch
- Database changes are backward compatible with previous app version
- Health checks and readiness probes are accurate under dependency failure
- Rollback plan includes data integrity considerations

## Decision Framework

- Define SLIs on user journeys (checkout, login, search)—not only server CPU.
- Propagate correlation IDs from browser through BFF to all downstream services.
- Choose rollout mechanism (canary, blue-green, feature flag) based on blast radius and rollback speed.
- Set rollback triggers on SLO burn, error budget, or business KPI regression before deploy starts.

## Common Rationalizations And Rebuttals

- "Monitoring infra is enough." -> Infra metrics miss user-visible failures; instrument journey SLIs.
- "Deploy Friday if tests pass." -> Release engineering includes rollback readiness and on-call coverage, not only tests.
- "Rollback is redeploy previous tag." -> Data migrations and feature flags may block naive redeploy; document full rollback path.

## Evidence Pack

- SLI/SLO definitions linked to dashboards and alert routes
- Correlation ID trace capture from UI action through backend graph
- Rollout runbook with trigger thresholds and rollback steps
- Post-release verification checklist results within defined window

## Exit Criteria

- Teams can detect, triage, and recover from regressions quickly
- Rollouts are measurable, reversible, and low-risk
- Operational ownership is explicit for runtime behavior
