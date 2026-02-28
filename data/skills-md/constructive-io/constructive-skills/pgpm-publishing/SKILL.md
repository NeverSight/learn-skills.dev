---
name: pgpm-publishing
description: Publish pgpm SQL modules to npm following Constructive standards. Use when asked to "publish a pgpm module", "release SQL packages", "bundle database modules", or when preparing @pgpm/* packages for distribution.
compatibility: pgpm CLI, pnpm, lerna, Node.js 20+
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Publishing PGPM Modules (Constructive Standard)

Publish pgpm SQL modules to npm using pgpm package bundling and lerna for versioning. This covers the workflow for @pgpm/* scoped packages.

## When to Apply

Use this skill when:
- Publishing SQL database modules to npm
- Bundling pgpm packages for distribution
- Managing @pgpm/* scoped packages
- Working with pgpm-modules or similar repositories

## PGPM vs PNPM Workspaces

| Aspect | PGPM Workspace | PNPM Workspace |
|--------|----------------|----------------|
| Purpose | SQL database modules | TypeScript/JS packages |
| Config | pnpm-workspace.yaml + pgpm.json | pnpm-workspace.yaml only |
| Build | `pgpm package` | `makage build` |
| Output | SQL bundles | dist/ folder |
| Versioning | Fixed (recommended) | Independent |

## Workspace Structure

```text
pgpm-modules/
├── .gitignore
├── lerna.json
├── package.json
├── packages/
│   ├── faker/
│   │   ├── deploy/
│   │   ├── revert/
│   │   ├── verify/
│   │   ├── package.json
│   │   ├── pgpm-faker.control
│   │   └── pgpm.plan
│   └── utils/
│       ├── deploy/
│       ├── revert/
│       ├── verify/
│       ├── package.json
│       ├── pgpm-utils.control
│       └── pgpm.plan
├── pgpm.json
├── pnpm-lock.yaml
└── pnpm-workspace.yaml
```

## Configuration Files

### pgpm.json

Points to packages containing SQL modules:

```json
{
  "packages": [
    "packages/*"
  ]
}
```

### pnpm-workspace.yaml

Same packages directory:

```yaml
packages:
  - packages/*
```

### lerna.json (Fixed Versioning)

For pgpm modules, use **fixed versioning** so all modules release together:

```json
{
  "$schema": "node_modules/lerna/schemas/lerna-schema.json",
  "version": "0.16.6",
  "npmClient": "pnpm"
}
```

**Note:** Unlike TypeScript packages which often use independent versioning, pgpm modules typically use fixed versioning because they're tightly coupled.

### Root package.json

```json
{
  "name": "pgpm-modules",
  "version": "0.0.1",
  "private": true,
  "repository": {
    "type": "git",
    "url": "https://github.com/constructive-io/pgpm-modules"
  },
  "license": "MIT",
  "engines": {
    "node": ">=20"
  },
  "scripts": {
    "bundle": "pnpm -r bundle",
    "lint": "pnpm -r lint",
    "test": "pnpm -r test",
    "deps": "pnpm up -r -i -L"
  },
  "devDependencies": {
    "@types/jest": "^30.0.0",
    "jest": "^30.2.0",
    "lerna": "^8.2.3",
    "pgsql-test": "^2.18.6",
    "ts-jest": "^29.4.5",
    "typescript": "^5.9.3"
  }
}
```

## Module Configuration

### Module package.json

```json
{
  "name": "@pgpm/faker",
  "version": "0.16.0",
  "description": "Fake data generation utilities for testing",
  "author": "Dan Lynch <pyramation@gmail.com>",
  "keywords": ["postgresql", "pgpm", "faker", "testing"],
  "publishConfig": {
    "access": "public"
  },
  "scripts": {
    "bundle": "pgpm package",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "dependencies": {
    "@pgpm/types": "workspace:*",
    "@pgpm/verify": "workspace:*"
  },
  "devDependencies": {
    "pgpm": "^1.3.0"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/constructive-io/pgpm-modules"
  }
}
```

**Key differences from TypeScript packages:**
- No `publishConfig.directory` — publishes from package root
- Uses `pgpm package` for bundling instead of makage
- Dependencies on other @pgpm/* modules use `workspace:*`

### Module .control File

```sh
# pgpm-faker.control
comment = 'Fake data generation utilities'
default_version = '0.16.0'
requires = 'plpgsql,uuid-ossp'
```

### Module pgpm.plan

```sh
%syntax-version=1.0.0
%project=pgpm-faker
%uri=pgpm-faker

schemas/faker 2025-01-01T00:00:00Z Author <author@example.com>
schemas/faker/functions/random_name [schemas/faker] 2025-01-01T00:00:00Z Author <author@example.com>
```

## Build Workflow

### Bundle a Module

```bash
cd packages/faker
pgpm package
```

Or bundle all modules:

```bash
pnpm -r bundle
```

### Run Tests

```bash
# All modules
pnpm -r test

# Specific module
pnpm --filter @pgpm/faker test
```

## Publishing Workflow

### 1. Prepare

```bash
pnpm install
pnpm -r bundle
pnpm -r test
```

### 2. Version

```bash
# Fixed versioning (all packages get same version)
pnpm lerna version

# Or with conventional commits
pnpm lerna version --conventional-commits
```

### 3. Publish

```bash
# Use from-package to publish versioned packages
pnpm lerna publish from-package
```

### One-Liner

```bash
pnpm install && pnpm -r bundle && pnpm -r test && pnpm lerna version && pnpm lerna publish from-package
```

## Dry Run Commands

```bash
# Test versioning (no git operations)
pnpm lerna version --no-git-tag-version --no-push

# Test publishing
pnpm lerna publish from-package --dry-run
```

## Module Dependencies

### Internal Dependencies

Use `workspace:*` for dependencies on other pgpm modules:

```json
{
  "dependencies": {
    "@pgpm/types": "workspace:*",
    "@pgpm/verify": "workspace:*"
  }
}
```

### SQL Dependencies

Declare SQL-level dependencies in the .control file:

```sh
requires = 'plpgsql,uuid-ossp,@pgpm/types'
```

And in deploy scripts:

```sql
-- Deploy: schemas/faker/functions/random_name
-- requires: schemas/faker
-- requires: @pgpm/types:schemas/types

CREATE FUNCTION faker.random_name()
RETURNS TEXT AS $$
  -- implementation
$$ LANGUAGE plpgsql;
```

## Three-File Pattern

Every SQL change has three files:

| File | Purpose |
|------|---------|
| `deploy/<path>.sql` | Creates the object |
| `revert/<path>.sql` | Removes the object |
| `verify/<path>.sql` | Confirms deployment |

**Example:**

`deploy/schemas/faker/functions/random_name.sql`:
```sql
-- Deploy: schemas/faker/functions/random_name
-- requires: schemas/faker

BEGIN;
CREATE FUNCTION faker.random_name()
RETURNS TEXT AS $$
BEGIN
  RETURN 'John Doe';
END;
$$ LANGUAGE plpgsql;
COMMIT;
```

`revert/schemas/faker/functions/random_name.sql`:
```sql
-- Revert: schemas/faker/functions/random_name

BEGIN;
DROP FUNCTION IF EXISTS faker.random_name();
COMMIT;
```

`verify/schemas/faker/functions/random_name.sql`:
```sql
-- Verify: schemas/faker/functions/random_name

SELECT verify_function('faker.random_name');
```

## Naming Conventions

- Package name: `@pgpm/<module-name>`
- Control file: `pgpm-<module-name>.control`
- SQL uses snake_case for identifiers
- Never use `CREATE OR REPLACE` — pgpm is deterministic

## Best Practices

1. **Fixed versioning**: Use for tightly coupled SQL modules
2. **Test before publish**: Run `pnpm -r test` to verify all modules
3. **Bundle before publish**: Run `pnpm -r bundle` to create packages
4. **Use verify helpers**: Leverage @pgpm/verify for consistent verification
5. **Document dependencies**: Keep .control file and SQL requires in sync

## References

- Related skill: `pgpm-workspace` for workspace setup
- Related skill: `pgpm-changes` for authoring SQL changes
- Related skill: `pgpm-dependencies` for managing dependencies
- Related skill: `pnpm-publishing` for TypeScript package publishing
