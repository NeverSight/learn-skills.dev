---
name: js-skills
description: >
  Zod schema definition patterns and dayjs date/time handling conventions.
  Use when defining Zod schemas, creating domain models, integrating
  const assertion enums with Zod validation, or working with dayjs
  for date/time operations.
license: MIT
metadata:
  author: mj
  version: "2.1.0"
---

# JS Skills — Zod Schema & Dayjs Patterns

Consistent Zod schema definition rules and dayjs date/time conventions extracted from production domain modeling.

## When to Apply

Reference these guidelines when:

- Defining new domain model schemas with Zod
- Extending base schemas for entity models
- Integrating const assertion enums with Zod validation
- Composing or deriving schemas from existing ones
- Creating model instances with auto-generated base fields
- Setting up dayjs plugins and locale in a project
- Working with timestamps, time arithmetic, formatting, or durations

## Rule Categories by Priority

| Priority | Category         | Impact | Prefix    |
| -------- | ---------------- | ------ | --------- |
| 1        | Schema Patterns  | HIGH   | `schema-` |
| 2        | Dayjs Patterns   | HIGH   | `dayjs-`  |

## Quick Reference

### 1. Schema Patterns (HIGH)

- `schema-naming-convention` — Consistent naming for schemas, types, and files
- `schema-type-inference` — Derive types from schemas with z.infer
- `schema-const-enum` — Const assertion arrays + z.enum integration
- `schema-composition` — Compose schemas via nesting, pick, partial
- `schema-create-model` — Use createModel for instance creation with auto base fields

### 2. Dayjs Patterns (HIGH)

- `dayjs-usage` — Plugin setup, timestamp ops, time arithmetic, formatting, duration

## How to Use

Read individual rule files for details and examples:

```
rules/schema-naming-convention.md
rules/schema-type-inference.md
rules/schema-const-enum.md
rules/schema-composition.md
rules/schema-create-model.md
rules/dayjs-usage.md
```

Each rule file contains:

- Why the rule matters
- Incorrect implementation example
- Correct implementation example
- Reference links
