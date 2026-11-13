---
name: angular-enterprise-frontend
description: Build and review Angular frontend applications with strong module boundaries, accessibility, performance, and maintainability. Use when the user asks for Angular UI features, component architecture, or enterprise frontend refactors.
disable-model-invocation: true
---

# Angular Enterprise Frontend

## Use When

- Building or refactoring Angular enterprise UIs
- Module boundaries, accessibility, or bundle performance need review

## Workflow

1. Define page and component responsibilities.
2. Prefer shared modules and reusable UI primitives.
3. Keep state flow explicit and predictable.
4. Enforce accessibility and responsive behavior.
5. Validate bundle impact and test coverage.

## Required Checks

- Lazy loading strategy for large routes
- Strict typing for component and API models
- Accessibility for keyboard and screen readers
- Unit and integration tests for key journeys

## Decision Framework

- Prefer the simplest architecture that preserves maintainability under team growth.
- Make rendering, state, and API boundary decisions explicit before implementation.
- If a feature affects critical user journeys, require performance and accessibility checks.
- If introducing dependencies, justify bundle and long-term maintenance cost.

## Common Rationalizations And Rebuttals

- "We can optimize later." -> Performance debt compounds quickly; set budgets now.
- "Accessibility is polish." -> Accessibility is core behavior and should ship with the feature.
- "One global state store is easiest." -> Over-centralization increases coupling and slows iteration.

## Evidence Pack

- UX state coverage (loading, empty, error, success) for changed flows
- Accessibility checks for keyboard, focus, and semantics
- Performance snapshot for key routes or interactions
- Test evidence for critical user paths

## Exit Criteria

- Workflow decisions are documented and implementation-ready
- Validation evidence exists for quality, reliability, and compatibility
- Operational readiness and rollback expectations are explicit

