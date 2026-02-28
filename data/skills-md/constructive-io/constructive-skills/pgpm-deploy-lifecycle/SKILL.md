---
name: pgpm-deploy-lifecycle
description: Full lifecycle of pgpm database deployments — deploy, verify, revert, tagging, and status checking. Use when asked to "deploy a module", "revert a migration", "verify deployments", "tag a release", "check deployment status", or when running pgpm deploy/revert/verify commands.
compatibility: pgpm CLI, PostgreSQL 14+, Node.js 22+
metadata:
  author: constructive-io
---

# pgpm Deploy Lifecycle

The complete deploy → verify → revert lifecycle for pgpm database modules.

## When to Apply

Use this skill when:
- Deploying database changes with `pgpm deploy`
- Reverting deployments with `pgpm revert`
- Verifying deployed state with `pgpm verify`
- Tagging deployment points with `pgpm tag`
- Checking deployment status with `pgpm migrate status`
- Running full-cycle tests with `pgpm test-packages`

## Core Concept

pgpm deployments are **deterministic and plan-driven**. Every change is tracked in `pgpm.plan`, and each change has exactly three scripts:
- **deploy/** — applies the change
- **verify/** — confirms it was applied correctly
- **revert/** — undoes the change

pgpm handles transactions automatically — you just write the SQL.

## Deploy

### Basic Deploy

```bash
# Deploy all pending changes for the current module
pgpm deploy

# Deploy with database creation (if database doesn't exist)
pgpm deploy --createdb

# Deploy a specific module by name
pgpm deploy my-module

# Deploy all modules in the workspace
pgpm deploy --workspace --all
```

### What Happens During Deploy

1. **Dependency resolution** — reads `.control` file, resolves all required extensions and pgpm modules
2. **Extension creation** — native Postgres extensions get `CREATE EXTENSION IF NOT EXISTS`
3. **Module dependency deploy** — pgpm modules from `extensions/` are deployed first (topological order)
4. **Plan execution** — each change in `pgpm.plan` is executed in order:
   - Checks if already deployed (via tracking schema)
   - Runs the deploy script
   - Records the change in the tracking schema
5. **Automatic verification** — after deploy, verify scripts run to confirm state

### Deploy to a Tag

```bash
# Deploy only up to a specific tag
pgpm deploy --to @v1.0.0
```

### Deploy Options

| Option | Description |
|--------|-------------|
| `--createdb` | Create the target database if it doesn't exist |
| `--workspace` | Operate at workspace level |
| `--all` | Deploy all modules (with `--workspace`) |
| `--to @tag` | Deploy up to a specific tag |
| `--yes` | Skip confirmation prompts |

## Verify

Verify checks that deployed changes are actually in the expected state.

```bash
# Verify all deployed changes
pgpm verify

# Verify a specific module
pgpm verify my-module
```

### What Happens During Verify

For each deployed change, pgpm runs the corresponding `verify/` script. Verify scripts typically use `SELECT` statements that will fail if the expected objects don't exist:

```sql
-- verify/schemas/app/tables/users.sql
SELECT id, email, name, created_at
FROM app.users
WHERE FALSE;
```

If any verify script fails, pgpm reports which changes are in a bad state.

## Revert

Revert undoes deployed changes in reverse order.

```bash
# Revert the last deployed change
pgpm revert

# Revert to a specific tag
pgpm revert --to @v1.0.0

# Revert all changes
pgpm revert --all

# Revert with confirmation skip
pgpm revert --yes
```

### What Happens During Revert

1. Changes are reverted in **reverse plan order** (last deployed = first reverted)
2. Each revert script runs (e.g., `DROP TABLE`, `DROP FUNCTION`)
3. The change is removed from the tracking schema
4. Verify scripts run to confirm the revert

### Revert Options

| Option | Description |
|--------|-------------|
| `--to @tag` | Revert back to a specific tag (exclusive — the tag itself stays) |
| `--all` | Revert all deployed changes |
| `--yes` | Skip confirmation prompts |

## Tagging

Tags mark specific points in the deployment plan for targeted deploy/revert.

```bash
# Tag the current state
pgpm tag v1.0.0

# Tag with a description
pgpm tag v1.0.0 -m "Initial release"
```

Tags appear in `pgpm.plan` as:

```
@v1.0.0 2024-01-15T10:00:00Z user <user@example.com> # Initial release
```

### Using Tags

```bash
# Deploy up to a tag
pgpm deploy --to @v1.0.0

# Revert to a tag (keeps the tag, reverts everything after it)
pgpm revert --to @v1.0.0
```

## Status

Check what's deployed and what's pending.

```bash
# Show deployment status
pgpm migrate status
```

This shows:
- Which changes are deployed
- Which changes are pending (in plan but not yet deployed)
- The current tag (if any)

## Full-Cycle Testing

`pgpm test-packages` runs a full deploy → verify → revert → deploy cycle to validate that all scripts work correctly in both directions.

```bash
# Full cycle test for current module
pgpm test-packages --full-cycle

# Full cycle test for all workspace modules
pgpm test-packages --full-cycle --workspace --all
```

This is the gold standard for validating migrations — it proves:
1. Deploy scripts apply correctly
2. Verify scripts confirm the deployed state
3. Revert scripts cleanly undo everything
4. Re-deploy works (proving revert was complete)

## Common Workflows

### First-time workspace deploy

> **Prerequisite:** Ensure PostgreSQL is running and environment is loaded. See `pgpm-docker` and `pgpm-env` skills for setup.

```bash
pgpm admin-users bootstrap --yes
pgpm deploy --createdb --workspace --all --yes
```

### Deploy after adding new changes

```bash
pgpm deploy
pgpm verify
```

### Revert a bad deploy

```bash
pgpm revert --yes
# Fix the issue, then redeploy
pgpm deploy
```

### Tag a release and deploy to that point

```bash
pgpm tag v1.0.0
pgpm deploy --to @v1.0.0
```

### Validate all migrations (CI)

> **Note:** In CI, start Postgres and load env vars first. See `pgpm-docker` and `pgpm-env` skills, or `github-workflows-pgpm` for CI-specific patterns.

```bash
pgpm admin-users bootstrap --yes
pgpm test-packages --full-cycle --workspace --all
```

## Tracking Schema

pgpm tracks deployments in a PostgreSQL schema (typically `pgpm_migrate`). This contains:
- `changes` table — records each deployed change with timestamp and deployer
- `tags` table — records tagged points

This is how pgpm knows what's already deployed and what's pending.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `role "authenticated" does not exist` | Missing bootstrap | Run `pgpm admin-users bootstrap --yes` |
| `database "mydb" does not exist` | Database not created | Use `pgpm deploy --createdb` |
| Deploy fails mid-way | SQL error in a deploy script | Fix the script, `pgpm revert` the failed change, redeploy |
| Verify fails after deploy | Deploy script didn't create expected objects | Check deploy script matches verify expectations |
| Revert fails | Revert script references objects that don't exist | Check for dependencies between changes |
| `Already deployed` | Change was previously deployed | Check `pgpm migrate status` — may need `pgpm revert` first |
