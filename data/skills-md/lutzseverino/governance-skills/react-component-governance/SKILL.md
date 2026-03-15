---
name: react-component-governance
description: Opinionated React component architecture guidance for React projects. Use when reviewing or designing component boundaries, deciding whether UI should stay inline, become a local helper, become a component boundary, or become another boundary kind, classifying components as presentational, interactive, or container, applying compound, headless, or polymorphic patterns, setting packaging and ownership rules, or reasoning about providers, pages, forms, loading, and error shells.
---

# React Component Governance

Make consistent React component architecture decisions without drifting into ad hoc local conventions.

Use [$implementation-governance](../implementation-governance/SKILL.md) alongside this skill when the task also needs change-kind, scope, validation, contract-change, or escalation decisions beyond React boundary structure.

## Workflow

1. Decide whether a meaningful boundary should exist at all.
Read [references/workflow.md](references/workflow.md) and [references/extraction.md](references/extraction.md) first when the question is whether UI should stay `inline`, become a `local helper`, become a `component boundary`, or become another boundary kind.

2. Decide what kind of boundary the extraction creates.
If the result is a `component boundary`, read [references/classification.md](references/classification.md) to classify it as `presentational`, `interactive`, or `container`.
If the result is a `headless behavior boundary`, `provider/infrastructure boundary`, or `support boundary`, keep that boundary kind explicit and do not force a component role onto it.

3. Check boundary cases when the structure is not an ordinary reusable UI component.
Read [references/boundary-cases.md](references/boundary-cases.md) for providers, pages, form coordinators, and loading or error shells before finalizing classification, packaging, or ownership for those cases.

4. Add optional patterns only when they strengthen the chosen role.
Use [references/patterns.md](references/patterns.md) for `compound`, `headless hook plus UI shell`, and `slot-based or polymorphic` patterns.

5. Decide packaging and ownership.
Read [references/packaging.md](references/packaging.md) and [references/ownership.md](references/ownership.md) to determine folder shape, public API boundaries, local-first placement, and promotion rules for the chosen boundary.

## Working Rules

- Choose exactly one primary role only when the extracted boundary is a `component boundary`.
- Use the canonical outcome terms consistently: `inline`, `local helper`, `component boundary`, `headless behavior boundary`, `provider/infrastructure boundary`, and `support boundary`.
- Treat patterns as optional modifiers, not as replacements for responsibility.
- Prefer local scope first. Shared abstractions must be earned by reuse or broader ownership.
- Prefer the smallest boundary that improves clarity.
- Do not treat same-owner support files on their own as evidence that a new `component boundary` is required.
- Treat flat reusable packaging as an area-level convention, not as a per-component choice inside one local owner.
- Prefer boundary-prefixed filenames for extracted support files so IDE and search discovery remain obvious.
- Adapt filesystem examples to the repo you are in. Do not assume every project uses the same folder names.

## Output Expectations

For a review, refactor plan, or implementation proposal:

- state the boundary outcome:
  `inline`, `local helper`, `component boundary`, `headless behavior boundary`, `provider/infrastructure boundary`, or `support boundary`
- state the classification: a primary role for a `component boundary`, or the explicit boundary kind for a non-component boundary
- name any optional pattern only if it genuinely strengthens the chosen role or boundary
- explain the intended packaging and ownership boundary
- call out any relevant boundary-case reasoning

Use this response shape:

```text
Boundary outcome: ...
Classification: ...
Optional pattern: ...
Packaging: ...
Ownership: ...
Boundary-case note: ...
```

## Reference Map

Use these references directly as needed:

- [references/overview.md](references/overview.md)
- [references/workflow.md](references/workflow.md)
- [references/classification.md](references/classification.md)
- [references/extraction.md](references/extraction.md)
- [references/packaging.md](references/packaging.md)
- [references/ownership.md](references/ownership.md)
- [references/boundary-cases.md](references/boundary-cases.md)
- [references/roles.md](references/roles.md)
- [references/patterns.md](references/patterns.md)

## Not For

- generic React setup, Vite config, routing, or build tooling
- broad code-quality guidance outside UI boundary and component architecture decisions
- domain modeling outside UI boundary and component architecture decisions
