---
name: generate-docs
description: Generate or update documentation for DaaS application code changes including API references, component docs, hook docs, schema files, and changelogs. Use when the user says generate-docs, update docs, document this, or needs documentation.
argument-hint: "[file or feature to document]"
---

# Generate Documentation

Every code change MUST have corresponding documentation updates.

## Documentation by Change Type

| What Changed   | Documentation Required                                   |
| -------------- | -------------------------------------------------------- |
| API endpoint   | `docs/API_REFERENCE.md`, `docs/api/[collection].md`      |
| Component      | `docs/COMPONENTS.md`, `docs/components/[name].md`        |
| Hook           | `docs/HOOKS.md`                                          |
| Collection     | `docs/COLLECTIONS.md`, `docs/schemas/[name].schema.json` |
| Feature        | `docs/features/[name].md`                                |
| Workflow       | `docs/WORKFLOWS.md`                                      |
| **Any change** | `docs/CHANGELOG.md` (always!)                            |

## Process

1. **Read the code** that was changed or created
2. **Identify doc type** from the table above
3. **Generate docs** following the templates below
4. **Update CHANGELOG.md** with a dated entry

## API Route Documentation Template

```markdown
## [Method] /api/[endpoint]

**Description:** Brief description

**Authentication:** Required / Public

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|

**Response:**
| Status | Body | Description |
|--------|------|-------------|

**Example:**
```

## Component Documentation Template

```markdown
## ComponentName

**Import:** `import { ComponentName } from '@/components/ui/component-name'`

**Props:**
| Prop | Type | Default | Description |
|------|------|---------|-------------|

**Usage:**
[Working code example]
```

## Standards

- JSDoc comments on all exported functions/types
- Usage examples for every public API
- Complete prop tables for components
- Working code examples that can be copy-pasted

## References

- [Documentation guidelines](references/documentation.instructions.md)
