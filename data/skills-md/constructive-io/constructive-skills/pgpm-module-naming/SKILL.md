---
name: pgpm-module-naming
description: Understand when to use npm package names vs control file names in pgpm modules. Use when creating .control files, writing SQL requires statements, running pgpm install, or referencing dependencies between modules.
compatibility: pgpm, PostgreSQL, Node.js 18+
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PGPM Module Naming: npm Names vs Control File Names

pgpm modules have two different identifiers that serve different purposes. Understanding when to use each is critical for correct dependency management.

## When to Apply

Use this skill when:
- Creating or editing `.control` files
- Writing `-- requires:` statements in SQL deploy files
- Running `pgpm install` commands
- Referencing dependencies between modules
- Publishing modules to npm

## The Two Identifiers

Every pgpm module has two names:

### 1. npm Package Name (for distribution)

Defined in `package.json` as the `name` field. Used for npm distribution and the `pgpm install` command.

**Format:** `@scope/package-name` (scoped) or `package-name` (unscoped)

**Examples:**
- `@sf-bot/rag-core`
- `@san-francisco/sf-docs-embeddings`
- `@pgpm/base32`

### 2. Control File Name / Extension Name (for PostgreSQL)

Defined by the `.control` filename and `%project=` in `pgpm.plan`. Used in PostgreSQL extension system and SQL dependency declarations.

**Format:** `module-name` (no scope, no @ symbol)

**Examples:**
- `rag-core`
- `sf-docs-embeddings`
- `pgpm-base32`

## When to Use Each

### Use npm Package Name (`@scope/name`)

**1. pgpm install command:**
```bash
pgpm install @sf-bot/rag-core @sf-bot/rag-functions @sf-bot/rag-indexes
```

**2. package.json dependencies:**
```json
{
  "dependencies": {
    "@sf-bot/rag-core": "^0.0.3"
  }
}
```

### Use Control File Name (`name`)

**1. .control file requires line:**
```sh
# sf-docs-embeddings.control
requires = 'rag-core'
```

**2. SQL deploy file requires comments:**
```sql
-- Deploy data/seed_collection to pg
-- requires: rag-core
```

**3. pgpm.plan %project declaration:**
```sh
%project=sf-docs-embeddings
```

**4. Cross-package references in pgpm.plan:**
```sh
data/seed [rag-core:schemas/rag/schema] 2026-01-25T00:00:00Z Author <author@example.com>
```

## Real-World Example

Consider the `sf-docs-embeddings` module:

**package.json** (npm name for distribution):
```json
{
  "name": "@san-francisco/sf-docs-embeddings",
  "version": "0.0.3"
}
```

**sf-docs-embeddings.control** (control name for PostgreSQL):
```sh
# sf-docs-embeddings extension
comment = 'San Francisco documentation embeddings'
default_version = '0.0.1'
requires = 'rag-core'
```

**pgpm.plan** (control name for project):
```sh
%project=sf-docs-embeddings
```

**deploy/data/seed_collection.sql** (control name in requires):
```sql
-- Deploy data/seed_collection to pg
-- requires: rag-core
```

## The Mapping

pgpm maintains an internal mapping between control names and npm names. When you run `pgpm install`, it:

1. Reads the `.control` file's `requires` list (control names)
2. Maps those to npm package names
3. Installs the npm packages

For example, if your `.control` has `requires = 'pgpm-base32'`, pgpm knows to install `@pgpm/base32` from npm.

## Common Mistakes

### Wrong: Using npm name in .control file
```sh
# WRONG
requires = '@sf-bot/rag-core'

# CORRECT
requires = 'rag-core'
```

### Wrong: Using control name in pgpm install
```bash
# WRONG
pgpm install rag-core

# CORRECT
pgpm install @sf-bot/rag-core
```

### Wrong: Using npm name in SQL requires
```sql
-- WRONG
-- requires: @sf-bot/rag-core

-- CORRECT
-- requires: rag-core
```

## Quick Reference Table

| Context | Use | Example |
|---------|-----|---------|
| `pgpm install` | npm name | `@sf-bot/rag-core` |
| `package.json` name | npm name | `@sf-bot/rag-core` |
| `package.json` dependencies | npm name | `@sf-bot/rag-core` |
| `.control` requires | control name | `rag-core` |
| SQL `-- requires:` | control name | `rag-core` |
| `pgpm.plan` %project | control name | `rag-core` |
| Cross-package deps | control name | `rag-core:schemas/rag` |

## Summary

- **npm names** (`@scope/name`): Used for distribution and installation via npm/pgpm install
- **Control names** (`name`): Used for PostgreSQL extension system, .control files, and SQL dependency declarations

Think of it this way: npm names are for the JavaScript/npm ecosystem, control names are for the PostgreSQL ecosystem.

## References

- Related skill: `pgpm-cli` for CLI commands
- Related skill: `pgpm-workspace` for workspace structure
- Related skill: `pgpm-changes` for authoring database changes
