---
name: protobuf
description: >-
  Use when working with Protocol Buffer (.proto) files, buf.yaml, buf.gen.yaml,
  or buf.lock. Covers proto design, buf CLI, gRPC/Connect services, protovalidate
  constraints, schema evolution, and troubleshooting lint/breaking errors.
filePatterns:
  - "**/*.proto"
  - "**/buf.yaml"
  - "**/buf.*.yaml"
  - "**/buf.gen.yaml"
  - "**/buf.gen.*.yaml"
  - "**/buf.lock"
---

# Protocol Buffers

## When You Need This Skill

- Creating or editing `.proto` files
- Setting up `buf.yaml` or `buf.gen.yaml`
- Designing gRPC or Connect services
- Adding protovalidate constraints
- Troubleshooting buf lint or breaking change errors

## Core Workflow

### 1. Match Project Style

Before writing proto code, review existing `.proto` files in the project.
Match conventions for naming, field ordering, structural patterns, validation, and documentation style.
If none exists, ask the user what style should be used or an existing library to emulate.

### 2. Write Proto Code

- Apply universal best practices from [best_practices.md](references/best_practices.md)
- Add [protovalidate](references/protovalidate.md) constraints to every field—this is not optional for production APIs
- For service templates, see [assets/](assets/)

### 3. Verify Changes

**Always run after making changes:**

```bash
buf format -w && buf lint
```

Check for a Makefile first—many projects use `make lint` or `make format`.

Fix all errors before considering the change complete.

## Quick Reference

| Task | Reference |
|------|-----------|
| Field types, enums, oneofs, maps | [quick_reference.md](references/quick_reference.md) |
| Schema evolution, breaking changes | [best_practices.md](references/best_practices.md) |
| Validation constraints | [protovalidate.md](references/protovalidate.md) |
| Complete service examples | [examples.md](references/examples.md), [assets/](assets/) |
| buf CLI, buf.yaml, buf.gen.yaml | [buf_toolchain.md](references/buf_toolchain.md) |
| Migrating from protoc | [migration.md](references/migration.md) |
| Lint errors, common issues | [troubleshooting.md](references/troubleshooting.md) |
| Proto API review checklist | [review_checklist.md](references/review_checklist.md) |

## Project Setup

### New Project

1. Create directory structure:
   ```
   proto/
   ├── buf.yaml
   ├── buf.gen.yaml
   └── company/
       └── domain/
           └── v1/
               └── service.proto
   ```

2. Use `assets/buf.yaml` as starting point
3. Add `buf.build/bufbuild/protovalidate` as a dependency in `buf.yaml` and run `buf dep update`
4. Use `assets/buf.gen.*.yaml` for code generation config

### Code Generation Templates

| Template | Use For |
|----------|---------|
| `buf.gen.go.yaml` | Go with gRPC |
| `buf.gen.go-connect.yaml` | Go with Connect |
| `buf.gen.ts.yaml` | TypeScript with Connect |
| `buf.gen.python.yaml` | Python with gRPC |
| `buf.gen.java.yaml` | Java with gRPC |

### Proto File Templates

Located in `assets/proto/example/v1/`:

| Template | Description |
|----------|-------------|
| `book.proto` | Entity message, BookRef oneof, enum |
| `book_service.proto` | Full CRUD with batch ops, pagination, ordering |

## Common Tasks

### Add a new field

1. Use next sequential field number
2. Add [protovalidate](references/protovalidate.md) constraints: every field should have validation appropriate to its type (format validators, length bounds, numeric ranges, enum constraints, etc.)
3. Document the field
4. Run `buf format -w && buf lint`

### Remove a field

1. Reserve the field number AND name:
   ```protobuf
   reserved 4;
   reserved "old_field_name";
   ```
2. Run `buf breaking --against '.git#branch=main'` to verify

### Add protovalidate constraints

Every field in a production API should have appropriate validation.
See [protovalidate.md](references/protovalidate.md) for the full reference.

Common constraints:
- String formats: `.string.uuid`, `.string.email`, `.string.uri`, `.string.pattern`
- String bounds: `.string.min_len`, `.string.max_len`
- Numeric bounds: `.int32.gte`, `.uint32.lte`
- Enum validation: `.enum.defined_only`, `.enum.not_in = 0`
- Repeated bounds: `.repeated.min_items`, `.repeated.max_items`
- Required fields: `(buf.validate.field).required = true`
- Oneof required: `(buf.validate.oneof).required = true`

## Verification Checklist

After making changes:
- [ ] Every field has appropriate protovalidate constraints
- [ ] `buf format -w` (apply formatting)
- [ ] `buf lint` (check style rules)
- [ ] `buf breaking --against '.git#branch=main'` (if modifying existing schemas)
