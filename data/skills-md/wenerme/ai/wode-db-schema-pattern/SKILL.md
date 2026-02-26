---
name: wode-db-schema-pattern
description: 'Use when designing, creating, or modifying PostgreSQL table schemas in the Wode project, including ID strategy, multi-tenant isolation, or naming conventions'
---

# Wode DB Schema Pattern

You are strictly required to follow this PostgreSQL schema design pattern. When creating or modifying table structures, you MUST adhere to every rule below.

## 1. Core Rules (MUST FOLLOW)

### Table Naming
- MUST use PostgreSQL schema for isolation, NEVER use table name prefixes
- MUST prefer singular form: `user`, `order`
- System tables MAY use plural: `users`, `groups`

### Data Types
- MUST use: `text`, `bigint`, `jsonb`, `bool`, `timestamptz`
- MUST use `text[]` for tag-like arrays
- NEVER use `varchar(n)` — validate at business layer + check constraints

### ID Strategy
- MUST use K-Sortable random primary keys (ULID or UUIDv7)
- MUST add type prefix for readability: `user_`, `order_`
- NEVER use auto-increment IDs

### Field Naming
- Timestamps: MUST use `_at` suffix (`created_at`, `updated_at`, `deleted_at`)
- Foreign keys: MUST use `_id` suffix (`user_id`, `customer_id`)
- Discriminators: MUST use `_type` suffix (`owner_type`, `entity_type`)
- Enum values: MUST use PascalCase (`Active`, `Draft`, `User`)

## 2. Standard Field Template

```sql
create table example (
    -- Identifiers
    id           text        not null default 'prefix_' || uuidv7(),
    tid          bigint      not null default current_tenant_id(),
    uid          uuid        not null default gen_random_uuid(),
    sid          bigint      not null default (next_entity_sid('Type')),

    -- Timestamps
    created_at   timestamptz not null default current_timestamp,
    updated_at   timestamptz not null default current_timestamp,
    deleted_at   timestamptz,

    -- State Machine
    state        text,        -- Active, Inactive, Suspended
    status       text,        -- Draft, Pending, Approved

    -- Extension Data
    attributes   jsonb       not null default '{}',  -- Client read/write
    properties   jsonb       not null default '{}',  -- Server managed, client read-only
    extensions   jsonb       not null default '{}',  -- Internal use, hidden from client
    metadata     jsonb       not null default '{}',

    -- Polymorphic Association
    owner_id     text,
    owner_type   text,        -- User, Team, Department

    -- Constraints
    primary key (tid, id),
    unique (tid, uid)
);
```

## 3. Extension Data Strategy

When adding flexible data fields, you MUST follow this separation:

| Field | Access | Purpose |
|-------|--------|---------|
| `attributes` | Client read/write | User-defined custom fields |
| `properties` | Server write, client read | Server-managed configuration |
| `extensions` | Internal only | Hidden from client API |
| `metadata` | Supplementary | Descriptive content |

## 4. Multi-Tenant Isolation

- Every business table MUST include `tid bigint not null default current_tenant_id()`
- Primary key MUST be composite: `primary key (tid, id)`
- Unique constraints MUST include `tid`: `unique (tid, uid)`

## 5. Detailed Reference

For complete field catalog (external IDs, audit trail, ownership pattern, generated columns, index naming, schema organization), read: [references/db-schema-design.md](references/db-schema-design.md)
