---
name: fullstack-testing-and-quality-gates
description: Define and enforce layered test strategy and quality gates for fullstack systems, including UI behavior, API contracts, integration paths, and release readiness criteria.
disable-model-invocation: true
---

# Fullstack Testing And Quality Gates

## Use When

- New fullstack features are being delivered
- Teams need predictable pre-merge and pre-release gates
- Regressions occur between frontend and backend integration points

## Workflow

1. Map risk by feature area, user path, and service dependency.
2. Define layered tests: unit, component, contract, integration, and end-to-end.
3. Prioritize deterministic tests for core flows and flaky-test elimination.
4. Build CI gates for linting, type checks, tests, coverage thresholds, and security checks.
5. Add release smoke tests for production-like environments.
6. Capture evidence and failure triage guidance in pull request templates.

## Test Coverage Model

- Unit tests for domain rules and utility logic
- Component tests for UI state transitions and accessibility behavior
- Contract tests for request and response compatibility
- Integration tests for API, database, and queue boundaries
- End-to-end tests for critical business journeys only

## Required Checks

- Contract changes include backward compatibility or migration note
- Coverage thresholds exist for changed modules
- Flaky tests are quarantined with an owner and remediation date
- CI failures include actionable logs and reproduction steps

## Decision Framework

- Map tests to risk: unit for rules, contract for APIs, integration for boundaries, E2E only for revenue-critical journeys.
- Block merge on lint, typecheck, unit, and contract suites; gate release on smoke and migration compatibility tests.
- Quarantine flaky tests with owner and SLA; never silently retry without tracking flake rate.
- Require backward-compatibility proof when contracts or schemas change.

## Common Rationalizations And Rebuttals

- "E2E covers everything." -> E2E is slow and brittle; lean on contracts and integration for breadth.
- "Coverage percentage is the goal." -> Covered nonsense tests provide false confidence; assert behavior and contracts.
- "We can skip gates for hotfixes." -> Hotfixes cause most regressions; expedite with scoped gates, don't remove them.

## Evidence Pack

- Test pyramid plan mapped to changed modules and user journeys
- CI gate configuration diff showing required jobs for merge vs release
- Contract test output for changed API surfaces
- Flake quarantine register or explicit zero-flake attestation for touched suites

## Exit Criteria

- Critical fullstack flows are covered with maintainable tests
- CI and release gates block unsafe changes
- Teams have clear evidence for merge and release decisions
