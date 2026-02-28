---
name: pgpm-extensions
description: Manage PostgreSQL extensions and pgpm modules in a pgpm workspace. Use when asked to "add an extension", "install a module", "add a dependency", "use pgcrypto/uuid-ossp", or when working with .control files and the extensions/ directory. CRITICAL — never run CREATE EXTENSION directly; pgpm handles extension creation during deploy.
compatibility: pgpm CLI, PostgreSQL 14+, Node.js 22+
metadata:
  author: constructive-io
---

# pgpm Extensions

How extensions and modules work in pgpm — adding dependencies, installing packages, and understanding the .control file.

## When to Apply

Use this skill when:
- Adding a PostgreSQL extension (uuid-ossp, pgcrypto, plpgsql, etc.) to a module
- Installing a pgpm-published module (@pgpm/faker, @pgpm/base32, etc.)
- Editing a `.control` file's `requires` list
- Running `pgpm extension` or `pgpm install`
- Debugging missing extension errors during deploy

## Critical Rule

**NEVER run `CREATE EXTENSION` directly in SQL migration files.** pgpm is deterministic — it reads the `.control` file and handles extension creation automatically during `pgpm deploy`. Writing `CREATE EXTENSION` in a deploy script will cause errors or duplicate operations.

## Two Kinds of Extensions

### 1. Native PostgreSQL Extensions

Built into Postgres or installed via OS packages. Examples:

| Extension | Purpose |
|-----------|---------|
| `uuid-ossp` | UUID generation (`uuid_generate_v4()`) |
| `pgcrypto` | Cryptographic functions (`gen_random_bytes()`) |
| `plpgsql` | PL/pgSQL procedural language |
| `pg_trgm` | Trigram text similarity |
| `citext` | Case-insensitive text |
| `hstore` | Key-value store |

These are resolved by Postgres itself during deploy. pgpm issues `CREATE EXTENSION IF NOT EXISTS` for them automatically.

### 2. pgpm Modules

Published to npm under scoped names (e.g., `@pgpm/faker`, `@pgpm/base32`, `@pgpm/uuid`). These contain their own deploy/revert/verify scripts and are installed into the workspace's `extensions/` directory.

| npm Name | Control Name | Purpose |
|----------|-------------|---------|
| `@pgpm/base32` | `pgpm-base32` | Base32 encoding |
| `@pgpm/types` | `pgpm-types` | Common types |
| `@pgpm/verify` | `pgpm-verify` | Verification helpers |
| `@pgpm/uuid` | `pgpm-uuid` | UUID utilities |
| `@pgpm/faker` | `pgpm-faker` | Test data generation |

During deploy, pgpm resolves these from the `extensions/` directory and deploys them before your module (topological dependency order).

## The .control File

Every pgpm module has a `.control` file at its root. This declares metadata and dependencies.

### Anatomy

```
# my-module extension
comment = 'My module description'
default_version = '0.0.1'
requires = 'plpgsql, uuid-ossp, pgpm-base32, pgpm-types'
```

**Key fields:**
- `comment` — Human-readable description
- `default_version` — Version string (typically `0.0.1`)
- `requires` — Comma-separated list of dependency **control names** (not npm names)

### Control Names vs npm Names

The `requires` field uses **control file names**, not npm package names:

| npm Name (for install) | Control Name (for requires) |
|------------------------|-----------------------------|
| `@pgpm/base32` | `pgpm-base32` |
| `@pgpm/types` | `pgpm-types` |
| `uuid-ossp` | `uuid-ossp` |
| `pgcrypto` | `pgcrypto` |

See the `pgpm-module-naming` skill for the full naming convention.

## Adding Dependencies

### Interactive: `pgpm extension`

Run inside a module directory to interactively select dependencies:

```bash
cd packages/my-module
pgpm extension
```

This shows a checkbox picker of all available modules in the workspace. Selected items are written to the `.control` file's `requires` list. You can also type custom extension names for native Postgres extensions.

### Installing npm-published pgpm modules: `pgpm install`

To add an npm-published pgpm module to your workspace:

```bash
# Install a single module
pgpm install @pgpm/base32

# Install multiple modules
pgpm install @pgpm/base32 @pgpm/types @pgpm/uuid

# Install all missing modules declared in .control requires
pgpm install
```

`pgpm install` downloads the module from npm and places it in the workspace's `extensions/` directory (e.g., `extensions/@pgpm/base32/`).

After installing, use `pgpm extension` to add the installed module to your `.control` file's `requires`.

### Manual Editing

You can also edit the `.control` file directly:

```
requires = 'plpgsql, uuid-ossp, pgpm-base32'
```

Then run `pgpm install` (no arguments) to install any missing modules.

## The extensions/ Directory

When you run `pgpm install @pgpm/foo`, it creates:

```
extensions/
  @pgpm/
    foo/
      pgpm-foo.control     # Module's control file
      pgpm.plan             # Module's deployment plan
      deploy/               # Deploy scripts
      revert/               # Revert scripts
      verify/               # Verify scripts
      package.json          # npm metadata
```

This directory is typically committed to version control so that `pgpm deploy` can resolve all dependencies without needing npm access.

## Upgrading Modules

```bash
# Upgrade a specific module
pgpm upgrade-modules @pgpm/base32

# Upgrade all modules in the workspace
pgpm upgrade-modules --workspace --all

# Preview what would be upgraded
pgpm upgrade-modules --workspace --all --dry-run
```

## Dependency Resolution During Deploy

When you run `pgpm deploy`, pgpm:

1. Reads the target module's `.control` file for `requires`
2. Resolves native Postgres extensions → queues `CREATE EXTENSION IF NOT EXISTS`
3. Resolves pgpm modules from `extensions/` → deploys them first (recursively resolving their dependencies)
4. Deploys your module's changes in plan order

This is fully automatic — you never need to manually order extension creation.

## Common Workflows

### Add a native Postgres extension to your module

1. Edit `.control`:
   ```
   requires = 'plpgsql, uuid-ossp, pgcrypto'
   ```
2. Deploy — pgpm creates the extensions automatically

### Add a pgpm module dependency

1. Install: `pgpm install @pgpm/base32`
2. Add to requires: `pgpm extension` (interactive) or edit `.control`
3. Deploy — pgpm deploys `@pgpm/base32` before your module

### Check what's installed

```bash
# List installed modules in the workspace extensions/ dir
ls extensions/

# Check a module's dependencies
cat packages/my-module/my-module.control
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `extension "pgpm-foo" is not available` | Module not installed in `extensions/` | Run `pgpm install @pgpm/foo` |
| `extension "uuid-ossp" is not available` | Postgres image missing the extension | Use `pyramation/postgres:17` or `postgres-plus:17` image |
| Deploy creates extension twice | You wrote `CREATE EXTENSION` in a deploy script | Remove it — pgpm handles this automatically |
| Wrong name in requires | Used npm name instead of control name | Use control name (e.g., `pgpm-base32` not `@pgpm/base32`) |
