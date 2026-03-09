---
name: ent-seed-sql-generator
description: Generate deterministic INSERT SQL seed data from Go Ent schemas and mixed inputs. This skill is REQUIRED whenever you need to create seed SQL for development or testing - it handles entity inference, relationship integrity, stable IDs, and dialect-specific SQL generation including JSON, arrays, and complex types. Use this skill for any task involving seed data, test fixtures, demo initialization, or database population from Ent schema definitions, even if the user doesn't explicitly mention "seed" or "SQL".
---

# Ent Seed SQL Generator

## Goal

Produce one executable seed SQL artifact from Ent schemas and mixed evidence, with deterministic IDs, valid relationships, and realistic production-like domain data with proper data coherence.

## Trigger / Non-Trigger

Use this skill when the task is to generate or revise seed SQL from Ent schema context, docs, demo behavior, or prompt requirements.

Do not use this skill for schema migration design, runtime repository/service implementation, or query performance tuning.

## Input Sources

Collect available inputs in this order:

1. Current prompt requirements
2. Ent schemas and migration/DDL files
3. Existing seed files and demo code behavior
4. Product docs and domain notes

## Reference Loading Plan

Load only what is needed for the current task:

- [references/model-extraction.md](references/model-extraction.md): entity/field/relation extraction and dependency planning
- [references/id-and-relation-rules.md](references/id-and-relation-rules.md): deterministic IDs, FK integrity, multi-tenant constraints
- [references/output-sql-pattern.md](references/output-sql-pattern.md): final SQL layout and strategy-specific patterns
- [references/password-hashing.md](references/password-hashing.md): only when credential fields are seeded

## Workflow

### Step 1: Confirm Scope and Detect Dialect

First, detect the SQL dialect from available evidence:
- Check `ent/client.go` or config for driver name (`mysql`, `postgres`, `sqlite`)
- Look at migration files in `migrations/` or `ent/migrate/`
- Check `go.mod` for dialect imports (`ent/dialect/mysql`, etc.)

If dialect cannot be determined, default to SQLite-compatible SQL and record this assumption in the header.

**Example dialect detection:**
```go
// From ent/client.go:
client, err := ent.Open("mysql", "root:pass@tcp(localhost:3306)/db")
// -> Dialect: mysql
```

### Step 2: Build Schema Map from Ent Definitions

Extract from Ent schema files (`ent/schema/*.go`):

- **Fields**: Check `field.*` options - `Optional`, `Nillable`, `Unique`, `Default`, `Immutable`, `Sensitive`
- **Enums**: Look for `/enum` values and `validate` rules
- **Relationships**: Check `edge.To`, `edge.From` with `Required`, `Unique`, `Ref` options
- **Indexes**: Note unique constraints and composite indexes

**Compute dependency order**: Tables without FK references first, then dependent tables in topological order.

**Example schema extraction:**
```go
// ent/schema/user.go
type User struct {
    ent.Schema
}
func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("email").Unique(),
        field.String("password_hash").Sensitive(),
        field.Time("created_at").Default(time.Now),
    }
}
func (User) Edges() []ent.Edge {
    return []ent.Edge{
        edge.From("organization", Organization.Type).Ref("users").Required().Unique(),
    }
}
// -> Extract: email (unique), password_hash (sensitive), created_at (default)
// -> Edge: users -> organizations (FK: organization_id)
```

### Step 3: Choose Execution Strategy

Select before writing SQL - document in header:

- `one-shot`: Plain `INSERT` statements, not rerun-safe. Use for fresh database setup.
- `idempotent`: Cleanup first or `INSERT OR IGNORE` / `ON CONFLICT DO NOTHING`. Use for repeatable runs.
- `upsert`: `ON CONFLICT DO UPDATE` when updating existing records is needed.

### Step 4: Design Deterministic Data

**ID Assignment Strategy:**
- Use non-overlapping integer ranges: users `1000-1999`, orgs `2000-2999`, etc.
- For string PKs: use semantic IDs like `usr_admin`, `org_acme`
- For UUIDs: use deterministic generation from business keys, never random

**Data Coherence Rules:**
- Timestamps: `created_at <= updated_at`
- State progressions: realistic lifecycle (`draft -> active -> archived`)
- Ownership: every `owner_id` must reference an existing user

### Step 5: Generate SQL Artifact

Follow the canonical pattern from `references/output-sql-pattern.md`:

```sql
-- Header with metadata
-- Dialect: mysql
-- Strategy: idempotent

BEGIN TRANSACTION;

-- 1) organizations (no dependencies)
INSERT INTO organizations (id, name, slug, created_at)
VALUES (2001, 'Acme', 'acme', '2026-01-01 09:00:00');

-- 2) users (depends on organizations)
INSERT INTO users (id, org_id, email, password_hash, created_at)
VALUES (1001, 2001, 'admin@acme.dev', '$2b$12$...', '2026-01-01 09:10:00');

COMMIT;
```

### Step 6: Quality Gates (Required)

Before finalizing, verify:
- [ ] No orphan FKs (every reference exists)
- [ ] No unique constraint violations
- [ ] No placeholder/TODO values
- [ ] IDs are deterministic across runs
- [ ] Timestamps are internally consistent

## Edge Cases and Common Patterns

### Soft Deletes
If entities have `deleted_at` or similar soft-delete columns:
- Set to `NULL` for active records
- Do not set future dates to simulate "deleted" unless explicitly required

### Time/Date Fields
- Use consistent epoch or realistic timestamps
- For `DEFAULT CURRENT_TIMESTAMP` columns, you may omit from INSERT (let DB handle it)
- If explicit, ensure timezone consistency

### JSON/JSONB Fields
- For PostgreSQL: use `'{"key": "value"}'::jsonb` or `'{"key": "value"}'::json`
- For MySQL: use `'{"key": "value"}'` (native JSON type)
- For SQLite: use `'{"key": "value"}'` (TEXT storage)
- Generate realistic nested structures matching production patterns
- Include varied values to demonstrate data shape diversity

### Array Fields (PostgreSQL)
- Use `ARRAY['value1', 'value2']` syntax
- Ensure elements match the column's element type
- Empty arrays: `ARRAY[]::text[]` with explicit cast

### Boolean Fields
- PostgreSQL/MySQL: `TRUE`/`FALSE` or `1`/`0`
- SQLite: `1`/`0` preferred
- Mix `TRUE` and `FALSE` values realistically

### Enum Fields
- Check Ent schema for enum values via `field.Enum` or validation rules
- Use only valid enum values in seed data
- Document enum mapping assumptions in header

### Self-Referential Relationships
- For trees (parent_id pointing to same table), insert parent first
- Use deterministic ordering: id=1 is root, children reference valid parents

### Multi-Tenant Isolation
- Seed tenant(s) first
- All dependent tables must have valid tenant FK
- Never create cross-tenant references unless isolation testing is the goal

### Complex Unique Constraints
- For composite unique constraints, ensure all columns together are unique
- Document any composite unique assumptions in header

### Realistic Data Coherence
- **User data**: Use real email patterns (`firstname.lastname@company.dev`)
- **Organization slugs**: Lowercase, hyphenated, meaningful
- **Timestamps**: Spread across reasonable time ranges, not all identical
- **Status distributions**: Mix of active/inactive/draft based on business logic
- **Numeric values**: Realistic ranges (not all 0 or max values)
- **Text content**: Meaningful short/medium strings, not Lorem Ipsum

## Output Contract

Return exactly one seed SQL artifact (inline or file, per user request) with:

1. Header comments: source inputs, dialect, assumptions
2. Strategy comment: `one-shot` or `idempotent` or `upsert`
3. Optional cleanup block (only when strategy requires it)
4. `INSERT` blocks grouped by dependency order
5. Optional verification `SELECT` queries (only when requested)

## Guardrails

- **Never invent tables or columns without evidence**: If a column isn't in the schema, don't add it. Mark inferences as assumptions in comments.
- **Never use random IDs**: Seed IDs must be stable. Use deterministic ranges, semantic strings, or deterministic UUIDs.
- **Never break FK dependency order**: Parent tables before children. Join tables after both endpoints.
- **Never bloat row counts**: 3-10 rows per core table is usually sufficient. More data doesn't mean better seeds.
- **Never expose production credentials**: Use test-only credentials. Never claim production security from seed data.
- **Never mix dialects in one file**: Use consistent syntax for the detected dialect.
- **Never omit required fields**: Check schema for Required() fields - they must be in every INSERT.
- **Never use invalid JSON syntax**: Ensure JSON columns have valid JSON strings.
- **Never use out-of-range enum values**: Validate against Ent schema enum definitions.

## Notes

This is an AI-first workflow. Dedicated scripts are optional and only needed for narrow deterministic sub-tasks (for example one-time hash generation to pin in SQL).
