---
name: spec-creator
description: Generate comprehensive technical specifications for usage with Ralph.
---

# Spec Authoring

## Purpose

Produce detailed, engineering-grade specifications similar in depth and structure to a full platform spec. The output must be explicit, testable, and implementation-ready without needing back-and-forth clarification.

## Core Principles

1. State intent clearly and early.
2. Define scope and non-scope to avoid ambiguity.
3. Make every requirement verifiable.
4. Prefer concrete examples over vague descriptions.
5. Use consistent naming and types across the document.
6. Include failure modes and edge cases.
7. Avoid assumptions; write them down.
8. Define canonical data models in a single spec and reference them elsewhere to prevent duplication.

## Required Structure

See the [SPEC_TEMPLATE.md](./SPEC_TEMPLATE.md) for a template with detailed section descriptions and writing guidelines.

Follow this structure exactly, but customize content to the project.

## Writing Rules

- Use precise, plain english language.
- Prefer tables for enums, options, or matrices.
- Include code blocks with correct syntax highlighting.
- Keep naming consistent across entities, APIs, and SDKs.
- If a behavior depends on policy, state it explicitly.
- If a data model is shared across domains, treat one spec as the source of truth and reference it rather than re-defining it.

## Output Quality Checklist

Before finalizing, confirm:

- Scope is explicit and non-goals are listed.
- All core entities and relationships are defined.
- Every endpoint has auth and payloads.
- All critical workflows are described step-by-step.
- Security and permissions are not implicit.
- At least one example is given for each major section.

## Related docs

When the new spec is complete, update specs/README.md to include it in the list of available specs.
