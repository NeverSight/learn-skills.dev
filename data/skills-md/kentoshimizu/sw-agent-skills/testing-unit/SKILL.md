---
name: testing-unit
description: "Deterministic unit-test strategy for isolated logic and fast feedback. Use when core logic branches, error paths, and edge conditions need low-latency regression evidence with controlled dependencies; do not use for browser-flow or cross-service compatibility validation."
---

# Testing Unit

## Overview
Use this skill to validate small-scope logic quickly and deterministically with strong failure localization.

## Scope Boundaries
- Use when correctness can be validated within isolated units.
- Typical requests:
  - `Harden branch and edge-case logic with fast deterministic tests.`
  - `Verify exception paths and guard-rail behavior.`
  - `Isolate dependencies to pinpoint failure causes.`
- Do not use when:
  - Cross-service compatibility is the core risk (`testing-contract`/`testing-integration`).
  - Full UI journey behavior is needed (`testing-e2e`/`playwright`).

## Inputs
- Unit boundaries and behavior expectations
- Mock/stub strategy and dependency seams
- Runtime constraints for fast feedback loops

## Outputs
- Unit suite with fixture and isolation strategy
- Decision record for scope and assertion depth
- Verification checklist for edge/failure coverage

## Workflow
1. Identify unit boundaries and observable contracts.
2. Define edge and failure conditions before implementation.
3. Compare isolation strategies and choose one with rationale.
4. Implement deterministic tests with explicit assertions.
5. Publish residual risks and uncovered dependency behaviors.

## Quality Gates
- Unit scope is explicit and dependency control is intentional.
- Edge and failure cases are covered for critical logic.
- Tests are deterministic and fast enough for frequent execution.
- Evidence is reproducible and actionable.

## Failure Handling
- Stop when critical units lack edge/failure coverage.
- Escalate when isolation requires architectural refactoring.

## Bundled Resources
- `references/trigger-and-examples.md`: trigger patterns, anti-patterns, and deliverable expectations.
