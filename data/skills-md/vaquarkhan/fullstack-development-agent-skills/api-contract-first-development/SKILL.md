---
name: api-contract-first-development
description: Define API contracts before implementation to reduce integration errors and preserve backward compatibility. Use when designing or updating REST, GraphQL, or event-driven interfaces between UI and backend services.
disable-model-invocation: true
---

# API Contract-First Development

## Use When

- Designing or changing REST, GraphQL, or event contracts between UI and services
- Backward compatibility or versioning decisions are required

## Workflow

1. Capture consumer needs and edge cases.
2. Draft contract schema and examples.
3. Define versioning and compatibility guarantees.
4. Implement provider and consumer validation.
5. Release with deprecation timeline when needed.

## Required Checks

- Include required and optional fields explicitly
- Define error envelope and status mapping
- Publish examples for happy and failure paths
- Avoid breaking changes without a migration path
- Contract tests run in CI
- Existing consumers remain compatible
- Deprecations are documented and announced

## Decision Framework

- Draft OpenAPI, GraphQL, or event schema before provider or consumer code merges.
- Classify every field change as safe additive, breaking, or deprecated-with-timeline.
- Consumer-driven contract tests must run in CI for every published schema revision.
- Version endpoints or use compatibility headers when multiple consumer generations coexist.

## Common Rationalizations And Rebuttals

- "We can document the API after shipping." -> Undocumented contracts drift; consumers embed assumptions that break silently.
- "Breaking changes are fine if we own all clients." -> Mobile, partner, and async consumers lag deploys; assume external consumers exist.
- "Examples in code comments are enough." -> CI cannot validate comments; publish machine-readable schemas and examples.

## Evidence Pack

- Published schema artifact with diff against previous version
- Consumer contract test results (provider and consumer suites)
- Deprecation timeline and migration guide for breaking changes
- Error envelope examples for validation, auth, and not-found paths

## Exit Criteria

- Workflow decisions are documented and implementation-ready
- Validation evidence exists for quality, reliability, and compatibility
- Operational readiness and rollback expectations are explicit

