---
name: dotnet-aspnet-core-microservices
description: Design and implement .NET ASP.NET Core microservices with explicit contracts, resilience, observability, and safe release patterns. Use when users request .NET backend services, C# APIs, distributed service design, or production hardening.
disable-model-invocation: true
---

# .NET ASP.NET Core Microservices

## Use When

- Implementing .NET ASP.NET Core APIs or microservices
- Resilience, observability, or safe release patterns are required

## Workflow

1. Define service boundary and ownership.
2. Define API contract and versioning approach.
3. Implement resilience and fault-handling strategy.
4. Add metrics, logs, and distributed tracing.
5. Validate with contract tests and failure-mode checks.

## Required Checks

- Explicit dependency lifetimes and clean DI setup
- Idempotency and concurrency safeguards
- Health probes and readiness endpoints
- Rollout plan with rollback criteria

## Decision Framework

- Prefer explicit contracts and compatibility rules before implementation.
- If dependency risk is high, require timeout, retry, and fallback strategy per call path.
- If async messaging is used, require idempotency, replay, and dead-letter handling.
- If traffic patterns are volatile, require load, failover, and scaling validation before ship.

## Common Rationalizations And Rebuttals

- "Retries will handle failures automatically." -> Unbounded retries can amplify outages; use budgets.
- "We can skip runbooks for now." -> Operational ambiguity delays incident recovery.
- "Contract changes are minor." -> Small breaking changes cause broad downstream regressions.

## Evidence Pack

- Contract compatibility note and migration strategy (if applicable)
- Failure-mode test evidence for dependency degradation and recovery
- Observability snapshot (latency, error, saturation, or queue health)
- Rollout and rollback steps with clear trigger thresholds

## Exit Criteria

- Workflow decisions are documented and implementation-ready
- Validation evidence exists for quality, reliability, and compatibility
- Operational readiness and rollback expectations are explicit

