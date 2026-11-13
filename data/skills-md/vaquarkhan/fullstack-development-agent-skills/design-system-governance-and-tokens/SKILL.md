---
name: design-system-governance-and-tokens
description: Govern design systems with tokens, component APIs, versioning, and cross-team adoption controls for consistent UI delivery.
disable-model-invocation: true
---

# Design System Governance And Tokens

## Use When

- Multiple teams consume shared UI primitives
- Brand or accessibility updates must roll out safely

## Workflow

1. Define token taxonomy for color, spacing, typography, and motion
2. Establish component API contracts and deprecation policy
3. Add visual regression and accessibility checks in CI
4. Plan migration paths for breaking component changes
5. Document contribution and review workflow

## Required Checks

- Tokens are single source of truth
- Breaking changes include migration guide
- Accessibility checks run on shared components
- Bundle impact tracked for design system releases

## Decision Framework

- Prefer composable primitives over one-off variants
- Version design system packages independently when needed
- Use codemods or adapters for large migrations
- Align tokens with platform themes (light/dark/high-contrast)

## Common Rationalizations And Rebuttals

- "Teams can fork components when blocked." -> Fragmentation and inconsistency grow quickly.
- "Visual polish can come after launch." -> Rework cost is higher than early consistency.
- "Design tokens are optional." -> Inconsistent UI scales poorly across products.

## Evidence Pack

- Token changelog and migration notes
- Visual regression report
- Accessibility audit for shared components
- Adoption metrics across product areas

## Exit Criteria

- Design system changes are safe and predictable
- Teams ship consistent UI faster
