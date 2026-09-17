---
name: dbml-database-docs
description: Use DBML as the standard format for database schema documentation. Apply this whenever creating, updating, reviewing, or repairing database docs, ERDs, schema diagrams, table inventories, migration summaries, Doctrine migration changes, SQL schema docs, ORM model docs, or CI schema drift failures. Prefer db/schema.dbml over Mermaid, Prisma schema, ad hoc Markdown tables, or prose-only database documentation unless the user explicitly requests another format.
license: MIT
metadata:
  author: Aircury
  version: "1.0"
---

# DBML Database Documentation

You are responsible for keeping the database structure documented in DBML.

Use DBML as the canonical, human- and AI-readable representation of the
database schema whenever the task touches database structure or database
documentation.

## Canonical File

The canonical database documentation file is:

```text
db/schema.dbml
```

If the repository has database schema documentation in another format and the
user has not explicitly asked to preserve that format, migrate or consolidate the
structural schema documentation into `db/schema.dbml`.

Use other docs only as supporting explanation. Do not let Mermaid diagrams,
Prisma schema files, Markdown tables, ORM metadata, or prose summaries become the
canonical database documentation when DBML is appropriate.

## When To Use This Skill

Use this skill when the user asks for any of these:

- Database documentation.
- DB schema documentation.
- ERD or entity relationship docs.
- Table, column, relation, foreign key, or index documentation.
- Documentation for SQL, migrations, Doctrine entities, ORM models, or database
  metadata.
- A review of whether database docs match migrations or the live schema.
- Fixing CI failures related to schema drift or DBML drift.
- Adding, changing, or reviewing structural database changes.

Structural database changes include:

- New or changed migrations.
- New, renamed, altered, or removed tables.
- New, renamed, altered, or removed columns.
- Changed column types, nullability, defaults, generated values, or comments.
- New, changed, or removed primary keys, foreign keys, unique constraints,
  checks, indexes, or enums.
- Join-table, inheritance-table, audit-table, or lookup-table changes.

## Core Rule

Whenever a structural database change is part of the work, update
`db/schema.dbml` in the same unit of work.

Do not leave a migration, ORM metadata change, or SQL schema change without the
corresponding DBML update. That creates documentation drift and makes future AI
sessions reason from stale persistence contracts.

## Workflow

1. Inspect the repository's existing database source of truth.
2. Identify the effective structural schema.
3. Create or update `db/schema.dbml` with the current schema contract.
4. Preserve behavioural requirements in `specs/features/`; keep DBML focused on
   persistence structure.
5. Run the relevant verification command when available.
6. If a drift check fails, fix the mismatch rather than bypassing the check.

Potential schema sources include:

- Doctrine migrations.
- Doctrine entity mappings or attributes.
- SQL migration files.
- ORM model definitions.
- Database dumps or schema snapshots.
- Existing DBML files.
- CI drift-check scripts.

Prefer generated or migration-backed facts over guesswork. If the schema cannot
be proven from the available files, mark the uncertainty in a DBML note or ask
the user for the missing source.

## DBML Content Requirements

Represent these details when present or inferable:

- Tables.
- Columns.
- Column types using the database's real type vocabulary where practical.
- `not null` constraints.
- Primary keys.
- Foreign keys and relationship cardinality.
- Unique constraints.
- Indexes, including composite indexes and uniqueness.
- Defaults.
- Enums or constrained value sets.
- Meaningful database comments or notes.
- Join tables and many-to-many relationships.
- Audit or timestamp columns when they are part of the schema contract.

Keep names exact. Do not modernise, rename, normalise, or reinterpret database
objects while documenting them.

## DBML Style

Use clear DBML that favours reviewable diffs:

```dbml
Table users {
  id uuid [pk]
  email varchar(255) [not null, unique]
  created_at timestamp [not null]
}

Table orders {
  id uuid [pk]
  user_id uuid [not null]
  total_amount decimal(10,2) [not null]

  Indexes {
    (user_id)
  }
}

Ref: orders.user_id > users.id
```

Use `Note:` for explanations that are part of the persistence contract, not for
general product behaviour:

```dbml
Table subscriptions {
  id uuid [pk]
  status varchar(32) [not null, note: 'Allowed by application policy: active, paused, cancelled']
}
```

If the database enforces a rule, represent it structurally where DBML supports
it. If the application enforces a persistence-relevant rule that DBML cannot
model directly, add a concise note.

## Relationship Rules

Prefer explicit `Ref:` declarations for relationships:

```dbml
Ref: order_items.order_id > orders.id
Ref: order_items.product_id > products.id
```

Keep foreign key names, referenced columns, and nullability consistent. Optional
relationships should have nullable FK columns; required relationships should use
`[not null]`.

## Index Rules

Represent indexes in each table's `Indexes` block:

```dbml
Table users {
  id uuid [pk]
  tenant_id uuid [not null]
  email varchar(255) [not null]

  Indexes {
    (tenant_id, email) [unique]
    (email)
  }
}
```

Do not omit indexes because they are not visible in entity fields. Indexes are
part of the persistence contract and often encode important lookup and
uniqueness assumptions.

## Drift Checks

If the repository contains this script, use it as the database documentation
drift gate:

```bash
./scripts/check-schema-drift.sh
```

Run it after updating `db/schema.dbml` when feasible. If it fails, inspect the
failure and make the actual database schema and `db/schema.dbml` agree.

Do not disable the check, weaken CI, skip hooks, or mark the failure as unrelated
unless the user explicitly instructs you to do so after you explain the risk.

## CI Failure Handling

When the user reports a CI schema drift failure:

1. Read the CI output and identify whether the live/generated schema, migrations,
   or `db/schema.dbml` is stale.
2. Compare the relevant migrations or schema snapshot against `db/schema.dbml`.
3. Update the stale side.
4. Re-run `./scripts/check-schema-drift.sh` if available.
5. Summarise which schema objects were brought back into sync.

## Boundary With Feature Specs

Use `db/schema.dbml` for structural persistence documentation.
Use `specs/features/` for observable system behaviour.

Examples:

- A `users.email` unique index belongs in `db/schema.dbml`.
- The business rule explaining when a user may change their email belongs in
  `specs/features/`.
- A foreign key from `orders.user_id` to `users.id` belongs in `db/schema.dbml`.
- The checkout behaviour that creates an order belongs in `specs/features/`.

When both structure and behaviour change, update both files.

## Completion Checklist

Before finishing database documentation work, verify:

- `db/schema.dbml` exists when database schema docs are required.
- Every touched table, column, FK, unique constraint, and index is represented.
- DBML names match the real database names exactly.
- Structural DB changes and DBML changes are included together.
- Relevant behaviour changes are reflected in `specs/features/` when applicable.
- `./scripts/check-schema-drift.sh` was run if present and feasible.
