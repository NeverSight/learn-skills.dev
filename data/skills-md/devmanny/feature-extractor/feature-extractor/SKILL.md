---
name: feature-extractor
description: Analyzes a complete software project and extracts all its functionalities, documenting them in individual .md files for product management, commercial, or technical use. Use this skill when the user wants to document project features, generate a feature catalog, understand what a system does without reading code, prepare documentation for stakeholders or AIs, or when they mention "extract features", "document features", "feature catalog", "what does this project do", "feature extraction", "extraer funcionalidades", "documentar features", "catalogo de funcionalidades", or wants to map codebase capabilities. Also use it when someone wants to audit what's built vs what's planned.
---

# Feature Extractor

Analyzes a software project and generates structured documentation of all its functionalities, organized into individual Markdown files. The output is readable by both humans (product managers, founders, sales teams, engineers) and AIs.

## Principles

- **No code**: Never include code snippets in generated documentation. Describe behaviors, flows, and business rules in natural yet technical language.
- **Stack-agnostic**: Works with any project type (frontend, backend, mobile, monorepo, microservices, etc.). Adapt your exploration to whatever stack you find.
- **Automatic**: Detect features by traversing the code — don't wait for the user to enumerate them.
- **Hierarchical**: Each main feature gets its own file, with sub-features detailed inside.

## Language

Write all generated documentation in the same language the user is using to communicate with you. If the user writes in Spanish, output in Spanish. If in English, output in English. If in French, output in French. Match their language exactly — including file names, section headers, and all prose content.

## Analysis Process

### Phase 1: Project Reconnaissance

Before documenting, understand the project:

1. Read root configuration files (package.json, Cargo.toml, pyproject.toml, go.mod, etc.) to identify the stack, dependencies, and structure.
2. Read README.md, CLAUDE.md, and any existing documentation in `docs/`.
3. Identify the high-level directory structure.
4. Detect whether it's a monorepo, microservices, single app, etc.

The goal is to build a mental map of the project before going deep.

### Phase 2: Feature Discovery

Traverse the project systematically looking for features in these sources:

**Source code** (primary source):
- Routes/endpoints (API routes, page routes, controllers)
- Models/entities and their relationships
- Use cases / services / business logic layers
- Significant UI components (complex forms, dashboards, wizards)
- External service integrations
- Jobs/workers/crons/scheduled tasks
- Middleware with business logic (auth, permissions, validation)

**Existing documentation**:
- .md files anywhere in the project
- High-level comments in key files
- Specs, PRDs, or design documents

**Indicators of planned or incomplete features**:
- TODOs and FIXMEs in code
- Features mentioned in docs but not implemented
- Commented-out code suggesting future functionality
- Branches or files prefixed with `wip-`, `draft-`, `experimental-`

### Phase 3: Classification and Grouping

Group discovered features into logical categories. A main feature is a system capability that a user or stakeholder would recognize as "a thing the system does." Sub-features are the pieces that compose it.

**Grouping example**:
- Feature: "Certificate Management"
  - Sub: PDF certificate generation
  - Sub: Bulk email delivery
  - Sub: Certificate number validation
  - Sub: Delivery history

Use your judgment to determine the right level of granularity. If a sub-feature is complex enough (has its own flow, multiple steps, its own integrations), it may deserve to be a main feature.

### Phase 4: Documentation

Generate files in `docs/features/` relative to the project root.

#### Feature file structure

Use this template as a guide, adapting sections as needed. Not every feature will have every section — omit those that don't apply rather than leaving them empty.

```markdown
# [Feature Name]

> [One-line description of what this feature does and why it exists]

## Status

[Implemented | Partially implemented | Planned]

## Description

[2-4 paragraphs describing the feature in business/product terms.
What problem it solves, who uses it, and what the general flow is.
No code, but be technical when describing behaviors.]

## Sub-features

### [Sub-feature name 1]
- **Status**: [Implemented | Partial | Planned]
- **Description**: [What it does and how it behaves]
- **Flow**: [User or system flow steps, if applicable]
- **Business rules**: [Constraints, validations, conditions]

### [Sub-feature name 2]
...

## Entities Involved

[List of data models/entities that participate and their role in this feature]

## Integrations

[External services, APIs, providers this feature uses]

## Permissions and Access

[Who can use this feature, roles, access restrictions]

## Internal Dependencies

[Other system features this one depends on or interacts with]

## Notes and Observations

[Any relevant detail: known limitations, technical debt,
important design decisions, planned items found in TODOs or docs]
```

File naming: use kebab-case based on the feature name.
Example: `docs/features/certificate-management.md`

#### General Index

Generate `docs/features/README.md` as the central catalog:

```markdown
# Feature Catalog

> Automatically generated by feature-extractor
> Project: [project name]
> Date: [generation date]

## Summary

[2-3 lines describing the project and its main purpose]

**Total features**: [N]
**Implemented**: [N] | **Partial**: [N] | **Planned**: [N]

## Features

| Feature | Status | Description |
|---|---|---|
| [Name](./file.md) | Implemented | Brief description |
| [Name](./file.md) | Partial | Brief description |
| [Name](./file.md) | Planned | Brief description |

## Dependency Map

[Briefly describe how the main features relate to each other]
```

## Important Considerations

**Parallelism**: Use subagents to explore multiple project areas simultaneously when the project is large. Assign different areas or modules to each subagent and then consolidate findings.

**Large projects**: If the project has more than 5 apps or major modules, present a feature outline to the user first for confirmation before generating all files. This avoids wasted work.

**Don't overwrite**: If `docs/features/` already exists with prior content, inform the user and ask whether they want to regenerate, update, or create in a different location.

**Planned features**: Document features found in TODOs, READMEs, spec docs, or commented-out code with "Planned" status. Include the source where the reference was found (e.g., "Mentioned in docs/roadmap.md", "TODO in src/services/payments.ts").

**Precision over exhaustiveness**: It's better to document 15 well-described features than 40 superficial ones. If you don't have enough context about a feature, explicitly indicate the description is partial rather than making up details.
