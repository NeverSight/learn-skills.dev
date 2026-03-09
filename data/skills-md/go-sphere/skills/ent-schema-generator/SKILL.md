---
name: ent-schema-generator
description: Design and generate Go + Ent database schemas for sphere-layout projects from requirements. Use when users describe data models, entity relationships, database tables, or schema changes — including prompts, Markdown docs, existing proto/service files, or demo behavior. Produces implementation-ready schema plans with field definitions, ID strategies, relation designs, indexes, entproto annotations, and bind/render/service integration guidance.
---

# Ent Schema Generator

## Overview

Transform requirement inputs into implementation-ready database schema plans for `sphere-layout` Go projects using Ent ORM. This skill focuses on decisions directly actionable in Ent schema code and downstream integration layers.

**This skill is repository-specific** — always prefer local scaffold conventions over generic patterns unless explicitly requested.

## When to Use

Use this skill when the user mentions:
- Database schema, Ent schema, entity design, or table structure
- Adding new data models, fields, or relationships
- Database migration, schema evolution, or index planning
- Proto bindings, entpb generation, or bind/render integration
- Any prompt describing business data requirements that need database persistence

## Required Reading

Always read these files in order before generating schema plans:

1. [references/best-practices.md](references/best-practices.md) — Decision rules for schema design
2. [references/output-template.md](references/output-template.md) — Required output format

Reference these when needed:

- [references/ent-schema-examples.md](references/ent-schema-examples.md) — Code patterns with entproto annotations
- [references/go-ent-service-patterns.md](references/go-ent-service-patterns.md) — DAO/service patterns

## Workflow

Follow this sequence for each schema task:

### Phase 1: Analysis
1. Gather evidence from prompt/docs/proto/schema/service/dao/render
2. Extract candidate entities and lifecycle states
3. Identify key business requirements and constraints

### Phase 2: Design Decisions
4. Design field-level policies (Optional/Nillable/Unique/Immutable/Default)
5. Decide ID strategy — generator-managed by default
6. Decide relation strategy: relation-entity > array > join table > JSON fallback
7. Build query-driven index plan from list/filter/sort paths
8. Plan Go implementation (weak relation IDs, batch IDIn, chunking)

### Phase 3: EntProto Compliance (REQUIRED)
9. Add entproto annotations to ALL schemas:
   - Schema: `entproto.Message()` in `Annotations()` method
   - Fields: `entproto.Field(n)` with sequential numbers (ID=1)
   - Enums: `entproto.Field(n)` + `entproto.Enum(map[string]int32{...})` with values starting from 1
10. Verify enum values always start from 1 (0 is reserved)

### Phase 4: Integration
11. Map to bind registration, WithIgnoreFields, render/dao/service
12. Document post-change commands and validation steps

### Phase 5: Output
13. Produce final brief using [references/output-template.md](references/output-template.md)

## Critical Requirements

### EntProto Annotation Rules

**ALL schemas MUST include entproto annotations** — this is not optional:

| Component | Required Annotation |
|-----------|---------------------|
| Schema | `entproto.Message()` in `Annotations()` |
| Primary Key Field | `entproto.Field(1)` |
| Regular Fields | `entproto.Field(n)` (sequential) |
| Enum Fields | `entproto.Field(n)` + `entproto.Enum(map[string]int32{...})` |
| Enum Values | Must start from 1 (0 reserved) |

Import: `"entgo.io/contrib/entproto"`

### Integration Completeness

Task is incomplete without addressing:

1. **Bind registration** — New entities must be added to `cmd/tools/bind/main.go#createFilesConf`
2. **WithIgnoreFields** — Review for timestamps and sensitive fields
3. **Post-generation commands** — Always include:
   ```bash
   make gen/proto
   go test ./...
   ```
4. **Generation diff checklist** — Verify entpb/proto/bind/map changes are consumed

## Output Requirements

Use [references/output-template.md](references/output-template.md) as the exact output format:
- Keep all 11 sections in order
- Mark assumptions explicitly as "Assumption:"
- Add "Blocking Notes:" under any section with incomplete validation

## Common Pitfalls

- **Don't** stop at schema-only output when integration is affected
- **Don't** skip `WithIgnoreFields` review for sensitive fields
- **Don't** use Optional/Nillable for entproto — prefer zero-value defaults
- **Don't** start enum values from 0
- **Don't** forget to register new entities in bind config
