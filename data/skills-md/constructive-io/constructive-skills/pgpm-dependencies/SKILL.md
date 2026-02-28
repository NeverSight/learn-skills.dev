---
name: pgpm-dependencies
description: Manage module dependencies in pgpm workspaces. Use when asked to "add a dependency", "reference another module", "manage cross-module dependencies", or when working with multi-module database projects.
compatibility: pgpm CLI, PostgreSQL
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Managing PGPM Dependencies

Handle dependencies between database changes and across modules in pgpm workspaces.

## When to Apply

Use this skill when:
- Adding dependencies between database changes
- Referencing objects from other modules
- Managing cross-module dependencies
- Resolving dependency order issues

## Dependency Types

### Within-Module Dependencies

Changes within the same module reference each other by path:

```sql
-- deploy/schemas/pets/tables/pets.sql
-- requires: schemas/pets

CREATE TABLE pets.pets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL
);
```

Add with `--requires`:
```bash
pgpm add schemas/pets/tables/pets --requires schemas/pets
```

### Cross-Module Dependencies

Reference changes from other modules using `module:path` syntax:

```sql
-- deploy/schemas/app/tables/user_pets.sql
-- requires: schemas/app/tables/users
-- requires: pets:schemas/pets/tables/pets

CREATE TABLE app.user_pets (
  user_id UUID REFERENCES app.users(id),
  pet_id UUID REFERENCES pets.pets(id),
  PRIMARY KEY (user_id, pet_id)
);
```

The `pets:schemas/pets/tables/pets` syntax means:
- `pets` = module name (from .control file)
- `schemas/pets/tables/pets` = change path within that module

## The .control File

Module metadata and extension dependencies live in the `.control` file:

```sh
# pets.control
comment = 'Pet management module'
default_version = '0.0.1'
requires = 'uuid-ossp,plpgsql'
```

| Field | Purpose |
|-------|---------|
| `comment` | Module description |
| `default_version` | Semantic version |
| `requires` | PostgreSQL extensions needed |

## Adding Extension Dependencies

When your module needs PostgreSQL extensions:

```bash
# Interactive mode
pgpm extension

# Or edit .control directly
requires = 'uuid-ossp,plpgsql,pgcrypto'
```

## Dependency Resolution

pgpm resolves dependencies recursively:

1. Reads `pgpm.plan` for change order
2. Parses `-- requires:` comments
3. Resolves cross-module references
4. Deploys in correct topological order

Example deployment order:
```text
1. uuid-ossp (extension)
2. plpgsql (extension)
3. schemas/pets (schema)
4. schemas/pets/tables/pets (table)
5. schemas/app (schema)
6. schemas/app/tables/users (table)
7. schemas/app/tables/user_pets (references both)
```

## Common Patterns

### Schema Before Tables

```bash
pgpm add schemas/app
pgpm add schemas/app/tables/users --requires schemas/app
pgpm add schemas/app/tables/posts --requires schemas/app/tables/users
```

### Functions After Tables

```bash
pgpm add schemas/app/functions/create_user --requires schemas/app/tables/users
```

### Triggers After Functions

```bash
pgpm add schemas/app/triggers/user_updated --requires schemas/app/functions/update_timestamp
```

### Cross-Module Reference

Module A (users):
```bash
pgpm add schemas/users/tables/users
```

Module B (posts):
```bash
pgpm add schemas/posts/tables/posts --requires users:schemas/users/tables/users
```

## Viewing Dependencies

Check what a change depends on:
```bash
# View plan file
cat pgpm.plan
```

Plan shows dependencies in brackets:
```sh
schemas/app/tables/user_pets [schemas/app/tables/users pets:schemas/pets/tables/pets] 2025-11-14T00:00:00Z Author <author@example.com>
```

## Circular Dependencies

pgpm prevents circular dependencies. If you see:
```text
Error: Circular dependency detected
```

Refactor to break the cycle:
1. Extract shared objects to a base module
2. Have both modules depend on the base
3. Remove direct cross-references

**Before (circular):**
```text
module-a depends on module-b
module-b depends on module-a
```

**After (resolved):**
```text
module-base (shared objects)
module-a depends on module-base
module-b depends on module-base
```

## Deploying with Dependencies

Deploy resolves all dependencies automatically:

```bash
# Deploy single module (pulls in dependencies)
pgpm deploy --database myapp_dev --createdb --yes

# Deploy specific module in workspace
cd packages/posts
pgpm deploy --database myapp_dev --yes
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Ensure module is in workspace `packages/` |
| "Change not found" | Check path matches exactly in plan file |
| "Circular dependency" | Refactor to use base module pattern |
| Wrong deploy order | Check `-- requires:` comments in deploy files |

## Best Practices

1. **Explicit dependencies**: Always declare what you need
2. **Minimal dependencies**: Only require what's directly used
3. **Consistent naming**: Use same paths in requires and plan
4. **Test deployments**: Verify order with fresh database

## References

- Related skill: `pgpm-workspace` for workspace setup
- Related skill: `pgpm-changes` for authoring changes
- Related skill: `pgpm-testing` for testing modules
