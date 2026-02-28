---
name: pgpm-sql-conventions
description: SQL file format and conventions for pgpm migration scripts. Use when writing deploy/revert/verify SQL files, when asked about migration file format, SQL naming conventions, dependency declarations, or the three-file pattern in pgpm.
compatibility: pgpm CLI, PostgreSQL 14+
metadata:
  author: constructive-io
---

# pgpm SQL Conventions

Rules and format for writing SQL migration files in pgpm modules.

## When to Apply

Use this skill when:
- Writing new deploy/revert/verify SQL files
- Adding database changes to a pgpm module
- Reviewing SQL migration code for correctness
- Debugging deployment failures related to SQL format

## Critical Rules

### 1. NEVER Use CREATE OR REPLACE

pgpm is **deterministic** — each change is deployed exactly once and reverted exactly once. Use `CREATE`, not `CREATE OR REPLACE`:

```sql
-- CORRECT
CREATE FUNCTION app.my_function() ...

-- WRONG — never do this in pgpm
CREATE OR REPLACE FUNCTION app.my_function() ...
```

If you need to modify an existing function, create a **new change** that drops and recreates it, or use the revert/redeploy cycle.

### 2. NO Transaction Wrapping

**Do NOT add `BEGIN`/`COMMIT` or `BEGIN`/`ROLLBACK` to your SQL files.** pgpm handles transactions automatically. Just write the raw SQL:

```sql
-- CORRECT — just the SQL
-- Deploy schemas/app/tables/users to pg

CREATE TABLE app.users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  email text NOT NULL UNIQUE,
  name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- WRONG — do not wrap in transactions
BEGIN;
CREATE TABLE app.users ( ... );
COMMIT;
```

### 3. Use snake_case for All Identifiers

All SQL identifiers must use `snake_case`:

```sql
-- CORRECT
CREATE TABLE app.user_profiles (
  user_id uuid NOT NULL,
  display_name text,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- WRONG
CREATE TABLE app.userProfiles (
  userId uuid NOT NULL,
  displayName text,
  createdAt timestamptz NOT NULL DEFAULT now()
);
```

## File Header Format

Every SQL file starts with a header comment declaring its purpose and path.

### Deploy Files

```sql
-- Deploy schemas/app/tables/users to pg

-- requires: schemas/app/schema

CREATE TABLE app.users (
  ...
);
```

### Revert Files

```sql
-- Revert schemas/app/tables/users from pg

DROP TABLE IF EXISTS app.users;
```

### Verify Files

```sql
-- Verify schemas/app/tables/users on pg

SELECT id, email, name, created_at
FROM app.users
WHERE FALSE;
```

**Header pattern:**
- Deploy: `-- Deploy <change_path> to pg`
- Revert: `-- Revert <change_path> from pg`
- Verify: `-- Verify <change_path> on pg`

Always check existing files in the same directory for the exact format used in that module.

## Dependency Declarations

Use `-- requires:` comments after the header to declare dependencies:

```sql
-- Deploy schemas/app/tables/user_profiles to pg

-- requires: schemas/app/schema
-- requires: schemas/app/tables/users

CREATE TABLE app.user_profiles (
  user_id uuid NOT NULL REFERENCES app.users(id),
  bio text,
  avatar_url text
);
```

### Cross-Module Dependencies

When depending on a change from another module, prefix with the module name:

```sql
-- Deploy schemas/app/procedures/get_user to pg

-- requires: schemas/app/schema
-- requires: other-module:schemas/shared/tables/users

CREATE FUNCTION app.get_user(user_id uuid) ...
```

The format is `module_name:change_path`.

## Common Change Types

### Schema

```sql
-- Deploy schemas/app/schema to pg

CREATE SCHEMA app;
```

Revert: `DROP SCHEMA IF EXISTS app;`
Verify: `SELECT 1/count(*) FROM information_schema.schemata WHERE schema_name = 'app';`

### Table

```sql
-- Deploy schemas/app/tables/users to pg

-- requires: schemas/app/schema

CREATE TABLE app.users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  email text NOT NULL UNIQUE,
  name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
```

Revert: `DROP TABLE IF EXISTS app.users;`
Verify: `SELECT id, email, name, created_at FROM app.users WHERE FALSE;`

### Function / Procedure

```sql
-- Deploy schemas/app/procedures/authenticate to pg

-- requires: schemas/app/schema
-- requires: schemas/app/tables/users

CREATE FUNCTION app.authenticate(email text, password text)
RETURNS app.users AS $$
DECLARE
  result app.users;
BEGIN
  SELECT * INTO result
  FROM app.users u
  WHERE u.email = authenticate.email;

  IF result IS NULL THEN
    RAISE EXCEPTION 'Invalid credentials';
  END IF;

  RETURN result;
END;
$$ LANGUAGE plpgsql STRICT SECURITY DEFINER;
```

Revert: `DROP FUNCTION IF EXISTS app.authenticate(text, text);`
Verify: `SELECT has_function_privilege('app.authenticate(text, text)', 'execute');`

### Index

```sql
-- Deploy schemas/app/tables/users/indexes/users_email_idx to pg

-- requires: schemas/app/tables/users

CREATE INDEX users_email_idx ON app.users (email);
```

Revert: `DROP INDEX IF EXISTS app.users_email_idx;`

### Grant / RLS Policy

```sql
-- Deploy schemas/app/tables/users/policies/users_select_policy to pg

-- requires: schemas/app/tables/users

ALTER TABLE app.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY users_select_policy ON app.users
  FOR SELECT
  TO authenticated
  USING (id = current_setting('auth.user_id')::uuid);
```

Revert: `DROP POLICY IF EXISTS users_select_policy ON app.users;`

### View (PostgreSQL 17+)

```sql
-- Deploy schemas/app/views/active_users to pg

-- requires: schemas/app/tables/users

CREATE VIEW app.active_users
  WITH (security_invoker = true)
AS
  SELECT id, email, name
  FROM app.users
  WHERE active = true;
```

Note: `security_invoker` requires PostgreSQL 17+.

### Trigger

```sql
-- Deploy schemas/app/tables/users/triggers/update_timestamp to pg

-- requires: schemas/app/tables/users

CREATE FUNCTION app.tg_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_timestamp
  BEFORE UPDATE ON app.users
  FOR EACH ROW
  EXECUTE FUNCTION app.tg_update_timestamp();
```

## Nested Path Organization

Changes are organized in nested directory paths that mirror the database structure:

```
deploy/
  schemas/
    app/
      schema.sql
      tables/
        users.sql
        posts.sql
        posts/
          indexes/
            posts_author_idx.sql
          policies/
            posts_select_policy.sql
      procedures/
        authenticate.sql
      views/
        active_users.sql
```

The path in the plan file matches the directory path:
```
schemas/app/schema [deps] timestamp author <email> # comment
schemas/app/tables/users [schemas/app/schema] timestamp author <email> # comment
```

## Checklist for New Changes

1. Create all three files: `deploy/`, `revert/`, `verify/`
2. Add the correct header to each file (`-- Deploy`, `-- Revert`, `-- Verify`)
3. Add `-- requires:` declarations in the deploy file
4. Add the change to `pgpm.plan` with dependencies
5. Use `CREATE` not `CREATE OR REPLACE`
6. Do NOT wrap in `BEGIN`/`COMMIT` — pgpm handles transactions
7. Use `snake_case` for all identifiers
8. Check existing files in the module for format conventions
