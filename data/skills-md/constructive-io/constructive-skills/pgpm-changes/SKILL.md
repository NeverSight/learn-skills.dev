---
name: pgpm-changes
description: Author database changes with pgpm using the three-file pattern (deploy/revert/verify). Use when asked to "add a table", "create a function", "add a migration", "write database changes", or when modifying database schema.
compatibility: pgpm CLI, PostgreSQL
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Authoring Database Changes with PGPM

Create safe, reversible database changes using pgpm's three-file pattern. Every change has deploy, revert, and verify scripts.

## When to Apply

Use this skill when:
- Adding tables, functions, triggers, or indexes
- Creating database migrations
- Modifying existing schema
- Organizing database changes in a pgpm module

## The Three-File Pattern

Every database change consists of three files:

| File | Purpose |
|------|---------|
| `deploy/<change>.sql` | Creates the object |
| `revert/<change>.sql` | Removes the object |
| `verify/<change>.sql` | Confirms deployment |

## Adding a Change

```bash
pgpm add schemas/pets/tables/pets --requires schemas/pets
```

This creates:
```text
deploy/schemas/pets/tables/pets.sql
revert/schemas/pets/tables/pets.sql
verify/schemas/pets/tables/pets.sql
```

And updates `pgpm.plan`:
```sh
schemas/pets/tables/pets [schemas/pets] 2025-11-14T00:00:00Z Author <author@example.com>
```

## Writing Deploy Scripts

Deploy scripts create database objects. Use `CREATE`, not `CREATE OR REPLACE` (pgpm is deterministic).

**deploy/schemas/pets/tables/pets.sql:**
```sql
-- Deploy: schemas/pets/tables/pets
-- requires: schemas/pets

CREATE TABLE pets.pets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  breed TEXT,
  owner_id UUID,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Important:** Never use `CREATE OR REPLACE` unless absolutely necessary. pgpm tracks what's deployed and ensures idempotency through its migration system.

## Writing Revert Scripts

Revert scripts undo the deploy. Must leave database in pre-deploy state.

**revert/schemas/pets/tables/pets.sql:**
```sql
-- Revert: schemas/pets/tables/pets

DROP TABLE IF EXISTS pets.pets;
```

## Writing Verify Scripts

Verify scripts confirm deployment succeeded. Use `DO` blocks that raise exceptions on failure.

**verify/schemas/pets/tables/pets.sql:**
```sql
-- Verify: schemas/pets/tables/pets

DO $$
BEGIN
  PERFORM 1 FROM pg_tables
  WHERE schemaname = 'pets' AND tablename = 'pets';
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Table pets.pets does not exist';
  END IF;
END $$;
```

## Nested Paths

Organize changes hierarchically using nested paths:

```text
schemas/
└── app/
    ├── schema.sql
    ├── tables/
    │   └── users/
    │       ├── table.sql
    │       └── indexes/
    │           └── email.sql
    ├── functions/
    │   └── create_user.sql
    └── triggers/
        └── updated_at.sql
```

Add changes with full paths:
```bash
pgpm add schemas/app/schema
pgpm add schemas/app/tables/users/table --requires schemas/app/schema
pgpm add schemas/app/tables/users/indexes/email --requires schemas/app/tables/users/table
pgpm add schemas/app/functions/create_user --requires schemas/app/tables/users/table
```

**Key insight:** Deployment order follows the plan file, not directory structure. Nested paths are for organization only.

## Plan File Format

The `pgpm.plan` file tracks all changes:

```sh
%syntax-version=1.0.0
%project=pets
%uri=pets

schemas/pets 2025-11-14T00:00:00Z Author <author@example.com>
schemas/pets/tables/pets [schemas/pets] 2025-11-14T00:00:00Z Author <author@example.com>
schemas/pets/tables/pets/indexes/name [schemas/pets/tables/pets] 2025-11-14T00:00:00Z Author <author@example.com>
```

Format: `change_name [dependencies] timestamp author <email> # optional note`

## Two Workflows

### Incremental (Development)

Add changes one at a time:
```bash
pgpm add schemas/pets --requires uuid-ossp
pgpm add schemas/pets/tables/pets --requires schemas/pets
```

Plan file updates automatically with each `pgpm add`.

### Pre-Production (Batch)

Write all SQL files first, then generate plan:
```bash
# Write deploy/revert/verify files manually
# Then generate plan from requires comments:
pgpm plan
```

`pgpm plan` reads `-- requires:` comments from deploy files and generates the plan.

## Common Change Types

### Schema
```bash
pgpm add schemas/app
```

```sql
-- deploy/schemas/app.sql
CREATE SCHEMA app;

-- revert/schemas/app.sql
DROP SCHEMA IF EXISTS app CASCADE;

-- verify/schemas/app.sql
DO $$ BEGIN
  PERFORM 1 FROM information_schema.schemata WHERE schema_name = 'app';
  IF NOT FOUND THEN RAISE EXCEPTION 'Schema app does not exist'; END IF;
END $$;
```

### Table
```bash
pgpm add schemas/app/tables/users --requires schemas/app
```

```sql
-- deploy/schemas/app/tables/users.sql
CREATE TABLE app.users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- revert/schemas/app/tables/users.sql
DROP TABLE IF EXISTS app.users;

-- verify/schemas/app/tables/users.sql
DO $$ BEGIN
  PERFORM 1 FROM pg_tables WHERE schemaname = 'app' AND tablename = 'users';
  IF NOT FOUND THEN RAISE EXCEPTION 'Table app.users does not exist'; END IF;
END $$;
```

### Function
```bash
pgpm add schemas/app/functions/get_user --requires schemas/app/tables/users
```

```sql
-- deploy/schemas/app/functions/get_user.sql
CREATE FUNCTION app.get_user(user_id UUID)
RETURNS app.users AS $$
  SELECT * FROM app.users WHERE id = user_id;
$$ LANGUAGE sql STABLE;

-- revert/schemas/app/functions/get_user.sql
DROP FUNCTION IF EXISTS app.get_user(UUID);

-- verify/schemas/app/functions/get_user.sql
DO $$ BEGIN
  PERFORM 1 FROM pg_proc WHERE proname = 'get_user';
  IF NOT FOUND THEN RAISE EXCEPTION 'Function get_user does not exist'; END IF;
END $$;
```

### Index
```bash
pgpm add schemas/app/tables/users/indexes/email --requires schemas/app/tables/users
```

```sql
-- deploy/schemas/app/tables/users/indexes/email.sql
CREATE INDEX idx_users_email ON app.users(email);

-- revert/schemas/app/tables/users/indexes/email.sql
DROP INDEX IF EXISTS app.idx_users_email;

-- verify/schemas/app/tables/users/indexes/email.sql
DO $$ BEGIN
  PERFORM 1 FROM pg_indexes WHERE indexname = 'idx_users_email';
  IF NOT FOUND THEN RAISE EXCEPTION 'Index idx_users_email does not exist'; END IF;
END $$;
```

## Deploy and Verify

```bash
# Deploy to database
pgpm deploy --database myapp_dev --createdb --yes

# Verify deployment
pgpm verify --database myapp_dev
```

## References

- Related skill: `pgpm-workspace` for workspace setup
- Related skill: `pgpm-dependencies` for cross-module dependencies
- Related skill: `pgpm-testing` for testing database changes
