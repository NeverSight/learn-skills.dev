---
name: pgpm-cli
description: Complete reference for pgpm CLI commands. Use when asked to "deploy database", "run migrations", "manage pgpm modules", "test packages", or when working with PostgreSQL package management.
compatibility: pgpm, PostgreSQL, Node.js 18+
metadata:
  author: constructive-io
  version: "1.0.0"
---

# pgpm CLI Reference

Complete reference for the pgpm (PostgreSQL Package Manager) command-line interface. pgpm provides deterministic, plan-driven database migrations with dependency management.

## When to Apply

Use this skill when:
- Deploying database changes
- Managing database migrations
- Installing or upgrading pgpm modules
- Testing pgpm packages in CI/CD
- Setting up local PostgreSQL development

## Quick Start

```bash
# Install pgpm globally
npm install -g pgpm

# Ensure PostgreSQL is running and env vars are loaded
# See pgpm-docker and pgpm-env skills for setup

# Create workspace and module
pgpm init workspace
cd my-app
pgpm init
cd packages/your-module

# Deploy to database
pgpm deploy --createdb --database mydb
```

## Core Commands

### Database Operations

**pgpm deploy** — Deploy database changes and migrations

```bash
# Deploy to current database (from PGDATABASE)
pgpm deploy

# Create database if missing
pgpm deploy --createdb

# Deploy to specific database
pgpm deploy --database mydb

# Deploy specific package to a tag
pgpm deploy --package mypackage --to @v1.0.0

# Fast deployment (no transactions)
pgpm deploy --fast --no-tx
```

**pgpm verify** — Verify database state matches expected migrations

```bash
pgpm verify
pgpm verify --package mypackage
```

**pgpm revert** — Safely revert database changes

```bash
pgpm revert
pgpm revert --to @v1.0.0
```

### Migration Management

**pgpm migrate** — Comprehensive migration management

```bash
# Initialize migration tracking
pgpm migrate init

# Check migration status
pgpm migrate status

# List all changes
pgpm migrate list

# Show change dependencies
pgpm migrate deps
```

### Module Management

**pgpm install** — Install pgpm modules as dependencies

```bash
# Install single package
pgpm install @pgpm/faker

# Install multiple packages
pgpm install @pgpm/base32 @pgpm/faker
```

**pgpm upgrade-modules** — Upgrade installed modules to latest versions

```bash
# Interactive selection
pgpm upgrade-modules

# Upgrade all without prompting
pgpm upgrade-modules --all

# Preview without changes
pgpm upgrade-modules --dry-run

# Upgrade specific modules
pgpm upgrade-modules --modules @pgpm/base32,@pgpm/faker

# Upgrade across entire workspace
pgpm upgrade-modules --workspace --all
```

**pgpm extension** — Interactively manage module dependencies

```bash
pgpm extension
```

### Workspace Initialization

**pgpm init** — Initialize new module or workspace

```bash
# Create new workspace
pgpm init workspace

# Create new module (inside workspace)
pgpm init

# Use full template path (recommended)
pgpm init --template pnpm/module
pgpm init -t pgpm/workspace

# Create workspace + module in one command
pgpm init -w
pgpm init --template pnpm/module -w

# Use custom template repository
pgpm init --repo https://github.com/org/templates.git --template my-template
```

### Change Management

**pgpm add** — Add a new database change

```bash
pgpm add my_change
```

This creates three files in `sql/`:
- `deploy/my_change.sql` — Deploy script
- `revert/my_change.sql` — Revert script  
- `verify/my_change.sql` — Verify script

**pgpm remove** — Remove a database change

```bash
pgpm remove my_change
```

**pgpm rename** — Rename a database change

```bash
pgpm rename old_name new_name
```

### Tagging and Versioning

**pgpm tag** — Version your changes with tags

```bash
# Tag latest change
pgpm tag v1.0.0

# Tag with comment
pgpm tag v1.0.0 --comment "Initial release"

# Tag specific change
pgpm tag v1.1.0 --package mypackage --changeName my-change
```

### Packaging and Distribution

**pgpm plan** — Generate deployment plans

```bash
pgpm plan
```

**pgpm package** — Package module for distribution

```bash
pgpm package
pgpm package --no-plan
```

### Testing

**pgpm test-packages** — Run integration tests on all modules in workspace

```bash
# Deploy only
pgpm test-packages

# Full deploy/verify/revert/deploy cycle
pgpm test-packages --full-cycle

# Continue after failures
pgpm test-packages --continue-on-fail

# Exclude specific modules
pgpm test-packages --exclude legacy-module

# Combine options
pgpm test-packages --full-cycle --continue-on-fail --exclude broken-module
```

### Docker and Environment

**pgpm docker** — Manage local PostgreSQL container

```bash
pgpm docker start
pgpm docker stop
```

**pgpm env** — Print PostgreSQL environment variables

```bash
# Standard PostgreSQL
eval "$(pgpm env)"

# Supabase local development
eval "$(pgpm env --supabase)"
```

### Admin Users

**pgpm admin-users** — Manage database admin users

```bash
# Bootstrap admin users from pgpm.json roles config
pgpm admin-users bootstrap

# Add specific user
pgpm admin-users add myuser

# Remove user
pgpm admin-users remove myuser
```

### Utilities

**pgpm dump** — Dump database to SQL file

```bash
# Dump to timestamped file
pgpm dump --database mydb

# Dump to specific file
pgpm dump --database mydb --out ./backup.sql

# Dump with pruning (for test fixtures)
pgpm dump --database mydb --database-id <uuid>
```

**pgpm kill** — Clean up database connections

```bash
# Kill connections and drop databases
pgpm kill

# Only kill connections
pgpm kill --no-drop
```

**pgpm clear** — Clear database state

```bash
pgpm clear
```

**pgpm export** — Export migrations from existing databases

```bash
pgpm export
```

**pgpm analyze** — Analyze database structure

```bash
pgpm analyze
```

### Cache and Updates

**pgpm cache clean** — Clear cached template repos

```bash
pgpm cache clean
```

**pgpm update** — Install latest pgpm version

```bash
pgpm update
```

## Environment Variables

pgpm uses standard PostgreSQL environment variables:

| Variable | Description |
|----------|-------------|
| `PGHOST` | Database host |
| `PGPORT` | Database port |
| `PGDATABASE` | Database name |
| `PGUSER` | Database user |
| `PGPASSWORD` | Database password |

Quick setup with `eval "$(pgpm env)"` or manual export.

## Global Options

Most commands support:

| Option | Description |
|--------|-------------|
| `--help, -h` | Show help |
| `--version, -v` | Show version |
| `--cwd <dir>` | Set working directory |

## Common Workflows

### Starting a New Project

```bash
pgpm init workspace
cd my-app
pgpm init
cd packages/new-module
pgpm add some_change
# Edit sql/deploy/some_change.sql
pgpm deploy --createdb
```

### Installing and Using a Module

```bash
cd packages/your-module
pgpm install @pgpm/faker
pgpm deploy --createdb --database mydb
psql -d mydb -c "SELECT faker.city('MI');"
```

### CI/CD Testing

```bash
# Bootstrap admin users
pgpm admin-users bootstrap

# Test all packages
pgpm test-packages --full-cycle --continue-on-fail
```

## References

- Related skill: `pgpm-workspace` for workspace structure
- Related skill: `pgpm-changes` for authoring changes
- Related skill: `pgpm-dependencies` for module dependencies
- Related skill: `github-workflows-pgpm` for CI/CD workflows
