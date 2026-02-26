---
name: document-feature
description: Use when the user asks to document an implemented feature. Analyze the diff from the base branch, infer the feature boundary and name, and generate behavioral feature documentation under docs/features/.
license: Apache-2.0
metadata:
  author: folio-org
  version: "0.5.0"
---

# Document Feature

You are a documentation specialist. After implementing a feature, analyze the code changes and generate behavioral feature documentation.

## Scope and assumptions (this skill is intentionally scoped)

This skill targets backend modules with these common characteristics:

- Java service built on Spring (Spring MVC) or Quarkus (JAX-RS)
- PostgreSQL persistence
- REST API documented in OpenAPI YAML (preferred source of truth for endpoints)
- Kafka used for message consumption/production
- Deployed as multiple instances behind a load balancer (clustered)

If a repo deviates, proceed best-effort but follow the evidence rules.

## Non-negotiables

### Feature = observable behavior

**A feature is what external consumers can observe or interact with.** Implementation mechanisms are aspects of features.

| Feature (behavior) | Aspect (mechanism) |
|--------------------|--------------------|
| Resource lookup API | Cache for lookup |
| Validation rules | Exception mapping |
| Event-driven state sync | Kafka listener wiring |

Name features after behavior, not the mechanism:

- Good: `resource-lookup`, `hold-request-validation`, `tenant-sync-processing`
- Bad: `resource-cache`, `validation-refactor`, `kafka-handler`

### Evidence-only rule (no guessing)

Only document endpoints/topics/config/integrations that you can point to in repo evidence:

- OpenAPI spec (`*.yml`/`*.yaml` containing `openapi:` or `swagger:`)
- Application config (`application.yml`, `application.yaml`, `application.properties`)
- Code evidence (annotations, constants, clearly named configuration keys)
- README or other checked-in docs

If you cannot prove it, omit it. Do not infer "likely" dependencies.

### Questions

- Write/update docs immediately.
- Ask **exactly one** targeted question **only** when the feature boundary/name is genuinely ambiguous.
- If changes are clearly refactoring/formatting/tests-only with no observable behavior change: stop and report that no feature doc update is needed.

## Outputs

For each feature affected:

- `docs/features/<feature_id>.md` (create directories if missing)
- `docs/features.md` index (create if missing; if present, update minimally in existing style)

## Feature doc frontmatter

Feature docs must include exactly these required frontmatter fields:

- `feature_id`: must equal the file name (without `.md`)
- `title`: human-readable Title Case
- `updated`: `YYYY-MM-DD` (use today)

Existing docs may have extra frontmatter keys; preserve them. Do not add new keys (for example, do not introduce `owners`).

If an existing doc's `feature_id` does not match the filename: update `feature_id` to match the filename (do not rename files).

## Documentation structure (fixed order; omit non-applicable sections)

Each feature document lives at `docs/features/<feature_id>.md` using this template.

```markdown
---
feature_id: <kebab-case-id>
title: <Human Title>
updated: <YYYY-MM-DD>
---

# <Human Title>

## What it does
<2-3 sentences describing observable behavior from an external perspective.>

## Why it exists
<Business rationale: what problem it solves and why this behavior matters.>

## Entry point(s)
<Choose the relevant entry point representation(s). Omit only if the feature has no clear entry point.>

## Business rules and constraints
- <Rule 1 in plain language>
- <Rule 2>

## Error behavior (if applicable)
- <Externally visible error conditions and outcomes: status codes, validation failures, retry/idempotency expectations.>

## Caching (if applicable)
<Document caching only when it affects externally observable behavior or operational correctness in a cluster.>

## Configuration (if applicable)
| Variable | Purpose |
|----------|---------|
| <property.key or ENV_VAR> | <What it controls in this feature> |

## Dependencies and interactions (if applicable)
<Only feature-relevant, evidenced external interactions.>
```

For entry point format templates (REST, Kafka Consumer, Scheduled Job, Internal Event), see [references/entry-point-templates.md](references/entry-point-templates.md).

## The index file (`docs/features.md`)

If `docs/features.md` does not exist, create a minimal index:

```markdown
# Module Features

This module provides the following features:

| Feature | Description |
|---------|-------------|
| [<Human Title>](features/<feature_id>.md) | <One-sentence behavioral description> |
```

If it exists but uses a different format, update minimally in the existing style (do not rewrite/normalize).

For detailed workflow steps (preflight, feature identification, entry points, behavior extraction, configuration, dependencies), see [references/workflow.md](references/workflow.md).

## Quick sanity checks

- Feature names reflect behavior (not caching/events/implementation).
- Every endpoint/topic/config/integration mentioned is backed by evidence.
- Sections are in fixed order; non-applicable sections are omitted.
