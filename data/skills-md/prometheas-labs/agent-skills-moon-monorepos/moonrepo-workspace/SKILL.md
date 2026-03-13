---
name: moonrepo-workspace
description: "Use when configuring .moon/workspace.yml, .moon/toolchains.yml, project discovery, caching, CI pipelines, or running affected detection"
---

# Moon v2 — Workspace Configuration

Reference for `.moon/workspace.yml` and workspace-level concerns.

## workspace.yml Structure

```yaml
$schema: './cache/schemas/workspace.json'
versionConstraint: '>=2.0.0'

projects:
  - 'apps/*'
  - 'packages/*'

vcs:
  client: 'git'           # not "manager" (v1 name)
  defaultBranch: 'main'

pipeline:                  # not "runner" (v1 name)
  cacheLifetime: '7 days'
  autoCleanCache: true
  logRunningCommand: false

telemetry: false
```

## Key v2 Renames

| v1 | v2 |
|----|-----|
| `runner` | `pipeline` |
| `vcs.manager` | `vcs.client` |
| `vcs.syncHooks` | `vcs.sync` |
| `constraints.enforceProjectTypeRelationships` | `constraints.enforceLayerRelationships` |
| `.moon/toolchain.yml` | `.moon/toolchains.yml` (plural) |

## Project Discovery

```yaml
# Glob patterns (auto-discover by directory)
projects:
  - 'apps/*'
  - 'packages/*'
  - '.'              # root project

# Explicit mapping
projects:
  web: 'apps/web'
  api: 'apps/api'
```

Projects need a `moon.yml` file to be recognized.

## Toolchains (.moon/toolchains.yml)

Configures language runtimes. Each toolchain has its own settings.

```yaml
javascript:
  packageManager: 'bun'

node:
  version: '22.0.0'

bun:
  version: '1.2.0'
```

Run `moon toolchain info <name>` to see available settings for any toolchain.

## Caching and CI

### Cache behavior

- Tasks with `cache: true` and defined `outputs` are cached
- `pipeline.cacheLifetime` controls retention (default: 7 days)
- Remote caching configured via `remote` block with gRPC or HTTP endpoint

### CI commands

```bash
moon ci                          # Run affected tasks in CI
moon ci --include-relations      # Include dependent projects
moon run :task --affected        # Run specific task for affected projects
moon run project:task --force    # Bypass cache
```

### Affected detection

```bash
moon query changed-files         # List changed files (was "touched-files" in v1)
moon run :test --affected        # Run tests for affected projects only
```

Use `--include-relations` to include projects that depend on affected projects. Relations are no longer included by default in v2.

## CLI Quick Reference

All flags use **kebab-case** in v2 (not camelCase).

```bash
moon check                       # Validate workspace config
moon project list                # List all projects
moon project <name>              # Show project details
moon run <project>:<task>        # Run a task
moon run :task                   # Run task across all projects
moon task <project>:<task>       # Show task details
moon toolchain info <name>       # Show toolchain settings
```
