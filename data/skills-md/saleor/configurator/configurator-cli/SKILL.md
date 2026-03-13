---
name: configurator-cli
description: "CLI commands for deploying, diffing, and introspecting Saleor stores. Use this skill whenever running ANY configurator CLI command or debugging CLI output. Covers deploy, introspect, diff, validate, --plan, CI/CD setup, and CLI flags."
license: MIT
metadata:
  author: saleor
  version: 3.0.0
  requires: "@saleor/configurator CLI"
---

# Configurator CLI

## Overview

The Saleor Configurator CLI syncs your YAML configuration with a live Saleor instance. You define your store in `config.yml`, then use CLI commands to preview and apply changes.

In non-TTY mode (pipes, CI, subprocesses), all commands automatically output a JSON envelope. Use `--json` to force JSON in a terminal, or `--text` to force human-readable in non-TTY.

## When to Use

- "How do I deploy my config?"
- "How do I pull the current store configuration?"
- "How do I preview changes before deploying?"
- "What flags does deploy support?"
- "How do I set up CI/CD for my store?"
- "What do the exit codes mean?"
- "How do I validate my config without network?"
- When NOT modeling products or writing YAML -- use `product-modeling` or `configurator-schema` instead

## Core Commands

### validate

Validates `config.yml` against the schema locally (no network required).

```bash
pnpm dlx @saleor/configurator validate
pnpm dlx @saleor/configurator validate --config custom-config.yml
pnpm dlx @saleor/configurator validate --json
```

### introspect

Pulls the current configuration from a Saleor instance into `config.yml`.

```bash
pnpm dlx @saleor/configurator introspect --url=$SALEOR_URL --token=$SALEOR_TOKEN
```

**Use cases:** initial setup, backup before changes, restore from known-good state.

### deploy

Pushes local `config.yml` changes to a Saleor instance.

```bash
pnpm dlx @saleor/configurator deploy --url=$SALEOR_URL --token=$SALEOR_TOKEN
```

**Important flags:**
- `--plan` -- preview changes without applying (replaces `--dry-run`)
- `--plan --json` -- machine-readable deployment plan
- `--fail-on-delete` -- abort if any deletions would occur (exit code 6)
- `--fail-on-breaking` -- abort if breaking changes detected (exit code 7)
- `--include <types>` -- only deploy specific entity types
- `--exclude <types>` -- skip specific entity types
- `--report-path <file>` -- custom path for deployment report (default: auto-generated in CWD)
- `--skip-media` -- skip media file uploads

### diff

Compares local `config.yml` with the remote Saleor instance.

```bash
pnpm dlx @saleor/configurator diff --url=$SALEOR_URL --token=$SALEOR_TOKEN
```

**Output markers:** `+ CREATE` (new), `~ UPDATE` (modified), `- DELETE` (removed).

**Entity scoping:**
- `--entity-type "Categories"` -- filter to one entity type
- `--entity "Categories/electronics"` -- filter to one specific entity

## Quick Reference

| Flag | Commands | Description |
|------|----------|-------------|
| `--url` | deploy, diff, introspect | Saleor GraphQL endpoint URL |
| `--token` | deploy, diff, introspect | Saleor API authentication token |
| `--json` | All | Force JSON envelope output |
| `--text` | All | Force human-readable output |
| `--drift-check` | introspect | Exit code 1 if remote differs from local |
| `--include` | deploy, diff, introspect | Comma-separated entity types to include |
| `--exclude` | deploy, diff, introspect | Comma-separated entity types to exclude |
| `--fail-on-delete` | deploy | Exit code 6 if deletions detected |
| `--fail-on-breaking` | deploy | Exit code 7 if breaking changes detected |
| `--plan` | deploy | Show plan without executing changes |
| `--report-path` | deploy | Custom path for deployment report |
| `--skip-media` | deploy, diff | Skip media file comparison/upload |
| `--entity-type` | diff | Filter to one entity type |
| `--entity` | diff | Filter to one specific entity (Type/name) |

## Environment Variables

Set credentials via `.env.local` (auto-loaded) or environment variables:

```bash
export SALEOR_URL="https://your-store.saleor.cloud/graphql/"
export SALEOR_TOKEN="your-api-token"

pnpm dlx @saleor/configurator deploy  # No flags needed
```

## JSON Envelope

In non-TTY mode, all commands output:

```json
{
  "command": "deploy",
  "version": "1.3.0",
  "exitCode": 0,
  "result": { },
  "logs": [{ "level": "info", "ts": "...", "message": "..." }],
  "errors": []
}
```

Parse with `jq`:
```bash
OUTPUT=$(pnpm dlx @saleor/configurator validate --json 2>/dev/null)
echo "$OUTPUT" | jq '.result.valid'
echo "$OUTPUT" | jq '.result.errors[]'
```

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Operation completed |
| 1 | Unexpected error | Check error message and logs |
| 2 | Authentication error | Verify URL and token |
| 3 | Network error | Check connectivity |
| 4 | Validation error | Fix config.yml syntax/schema |
| 5 | Partial failure | Some operations failed, check errors array |
| 6 | Deletion blocked | `--fail-on-delete` triggered |
| 7 | Breaking blocked | `--fail-on-breaking` triggered |

## Common Workflows

### Optimal Agent Workflow

```bash
# 1. Validate locally first
pnpm dlx @saleor/configurator validate --json

# 2. Compare with remote
pnpm dlx @saleor/configurator diff --json

# 3. Preview deployment
pnpm dlx @saleor/configurator deploy --plan --json

# 4. Execute deployment
pnpm dlx @saleor/configurator deploy --json
```

### Safe CI/CD Deployment

```bash
pnpm dlx @saleor/configurator deploy --fail-on-delete
```

### Entity-Scoped Debugging

```bash
# Drill into a specific entity type
pnpm dlx @saleor/configurator diff --entity-type "Categories" --json

# Drill into a specific entity
pnpm dlx @saleor/configurator diff --entity "Categories/electronics" --json
```

### Selective Deployment

```bash
# Deploy only channels and products
pnpm dlx @saleor/configurator deploy --include channels,products

# Deploy everything except products
pnpm dlx @saleor/configurator deploy --exclude products
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Deploying without previewing first | Always run `diff` or `deploy --plan` before `deploy` |
| Wrong URL format | URL must end with `/graphql/` (e.g., `https://store.saleor.cloud/graphql/`) |
| Expired or invalid token | Regenerate your API token in Saleor Dashboard |
| Not using `--drift-check` for CI drift detection | Use `introspect --drift-check` to fail CI if remote config has drifted |
| Forgetting `--fail-on-delete` in CI | Prevents accidental deletions |
| Using `SALEOR_API_URL` | Correct env var is `SALEOR_URL` |

## `diff` vs `deploy --plan`

| | `diff` | `deploy --plan` |
|---|--------|-----------------|
| **Purpose** | Show field-level differences between local and remote | Show what operations deploy would execute |
| **Output** | Per-field changes (old -> new values) | Operation summary (creates, updates, deletes) |
| **Scoping** | `--entity-type`, `--entity` for drill-down | No entity-level scoping |
| **Use when** | Debugging what changed, reviewing individual fields | Pre-deploy safety check, CI gates |

**Recommended workflow**: Use `diff` to understand changes, then `deploy --plan` to confirm the execution plan.

## Rollback & Recovery

Configurator doesn't have a built-in rollback command, but you can recover using these patterns:

**Before deploying** (recommended):
```bash
# Save current remote state as backup
pnpm dlx @saleor/configurator introspect --config=backup-config.yml
```

**After a bad deploy**:
```bash
# Restore from backup
pnpm dlx @saleor/configurator deploy --config=backup-config.yml
```

**Using git**:
```bash
# Revert config.yml to last known good state
git checkout HEAD~1 -- config.yml
pnpm dlx @saleor/configurator deploy
```

**Partial recovery** (only fix specific entities):
```bash
# Deploy only the entity types that need fixing
pnpm dlx @saleor/configurator deploy --include=categories,products
```

## See Also

- For complete command reference, see [references/commands.md](references/commands.md)
- For all flags and options, see [references/flags.md](references/flags.md)
- For error code details, see [references/error-codes.md](references/error-codes.md)
- For CI/CD setup, see [references/ci-cd.md](references/ci-cd.md)

### Related Skills

- **`configurator-schema`** - Config.yml structure and validation rules
- **`saleor-domain`** - Entity relationships and Saleor concepts
- **`agent-output-parsing`** - JSON envelope parsing and drill-down patterns
