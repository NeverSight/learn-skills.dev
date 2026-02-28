---
name: monorepo-management
description: Best practices for managing large PNPM monorepos. Use when asked to "manage monorepo", "organize packages", "configure workspace dependencies", or when scaling a multi-package repository.
compatibility: pnpm, lerna, Node.js 18+, TypeScript
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Monorepo Management with PNPM

Best practices for managing large PNPM monorepos following Constructive conventions. Covers workspace configuration, dependency management, selective builds, and package organization.

## When to Apply

Use this skill when:
- Managing a multi-package repository
- Configuring workspace dependencies
- Setting up selective builds and filtering
- Organizing packages in a large codebase
- Configuring lerna versioning strategies

## Workspace Configuration

### pnpm-workspace.yaml

Define package locations:

```yaml
packages:
  - 'packages/*'
```

For larger projects with multiple directories:

```yaml
packages:
  - 'packages/*'
  - 'pgpm/*'
  - 'graphql/*'
  - 'postgres/*'
  - 'apps/*'
  - 'libs/*'
```

### Root package.json

```json
{
  "name": "my-workspace",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "build": "pnpm -r run build",
    "test": "pnpm -r run test",
    "lint": "pnpm -r run lint",
    "clean": "pnpm -r run clean",
    "deps": "pnpm up -r -i -L"
  }
}
```

Key points:
- Root is always `private: true`
- Scripts use `pnpm -r` for recursive execution
- `deps` script for interactive dependency updates

## Workspace Dependencies

### workspace:* Protocol

Reference internal packages:

```json
{
  "dependencies": {
    "my-utils": "workspace:*"
  }
}
```

When published, `workspace:*` is replaced with the actual version.

### Dependency Types

| Protocol | Behavior |
|----------|----------|
| `workspace:*` | Latest version in workspace |
| `workspace:^` | Compatible version range |
| `workspace:~` | Patch version range |

### Adding Workspace Dependencies

```bash
# Add workspace dependency
pnpm add my-utils --filter my-app --workspace

# Add external dependency to specific package
pnpm add lodash --filter my-app

# Add dev dependency to root
pnpm add -D typescript -w
```

## Filtering and Selective Builds

### --filter Flag

Run commands on specific packages:

```bash
# Single package
pnpm --filter my-app run build

# Multiple packages
pnpm --filter my-app --filter my-utils run build

# Glob patterns
pnpm --filter "my-*" run build

# Package and its dependencies
pnpm --filter my-app... run build

# Package and its dependents
pnpm --filter ...my-utils run build

# Exclude packages
pnpm --filter "!my-legacy" run build
```

### Dependency-Aware Builds

```bash
# Build package and all its dependencies
pnpm --filter my-app... run build

# Build only dependencies (not the package itself)
pnpm --filter "my-app^..." run build

# Build dependents (packages that depend on this)
pnpm --filter "...my-utils" run build
```

### Changed Packages

```bash
# Packages changed since main
pnpm --filter "...[origin/main]" run build

# Packages changed in last commit
pnpm --filter "...[HEAD~1]" run build
```

## Package Organization

### Directory Structure

Organize by domain or type:

```
my-workspace/
├── packages/           # Shared utilities
│   ├── utils/
│   ├── types/
│   └── config/
├── apps/               # Applications
│   ├── web/
│   └── api/
├── libs/               # Domain libraries
│   ├── auth/
│   └── database/
├── pgpm/               # PGPM modules (if hybrid)
│   └── migrations/
├── pnpm-workspace.yaml
├── lerna.json
└── package.json
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Scoped packages | `@org/package-name` | `@myorg/utils` |
| Internal packages | `package-name` | `my-utils` |
| Apps | `app-name` | `web-app` |

## Lerna Configuration

### Independent Versioning

Each package versioned separately:

```json
{
  "$schema": "node_modules/lerna/schemas/lerna-schema.json",
  "version": "independent",
  "npmClient": "pnpm",
  "command": {
    "publish": {
      "allowBranch": "main",
      "conventionalCommits": true
    }
  }
}
```

Best for: utility libraries with different release cycles.

### Fixed Versioning

All packages share same version:

```json
{
  "$schema": "node_modules/lerna/schemas/lerna-schema.json",
  "version": "1.0.0",
  "npmClient": "pnpm",
  "command": {
    "publish": {
      "allowBranch": "main",
      "conventionalCommits": true
    }
  }
}
```

Best for: tightly coupled packages that release together.

### Versioning Commands

```bash
# Version changed packages
pnpm lerna version

# Version with specific bump
pnpm lerna version patch
pnpm lerna version minor
pnpm lerna version major

# Preview without changes
pnpm lerna version --no-git-tag-version --no-push
```

## Dependency Management

### Update Dependencies

```bash
# Interactive update all packages
pnpm up -r -i -L

# Update specific dependency everywhere
pnpm up lodash -r

# Update to latest
pnpm up lodash@latest -r
```

### Check for Outdated

```bash
pnpm outdated -r
```

### Dedupe Dependencies

```bash
pnpm dedupe
```

## Build Optimization

### Parallel Builds

PNPM runs in parallel by default. Control concurrency:

```bash
# Limit concurrent tasks
pnpm -r --workspace-concurrency=4 run build
```

### Topological Order

Dependencies are built first automatically:

```bash
# Builds in dependency order
pnpm -r run build
```

### Caching

Use turbo or nx for build caching in large repos:

```json
{
  "scripts": {
    "build": "turbo run build"
  }
}
```

## CI/CD Patterns

### Install Dependencies

```bash
pnpm install --frozen-lockfile
```

### Build Changed Packages

```bash
# Build packages changed since main
pnpm --filter "...[origin/main]" run build
```

### Test Changed Packages

```bash
pnpm --filter "...[origin/main]" run test
```

### Publish Workflow

```bash
# Version and publish
pnpm lerna version --yes
pnpm lerna publish from-package --yes
```

## Common Commands Reference

| Command | Description |
|---------|-------------|
| `pnpm install` | Install all dependencies |
| `pnpm -r run build` | Build all packages |
| `pnpm -r run test` | Test all packages |
| `pnpm --filter <pkg> run <cmd>` | Run command in specific package |
| `pnpm --filter <pkg>... run <cmd>` | Run in package and dependencies |
| `pnpm add <dep> --filter <pkg>` | Add dependency to package |
| `pnpm add <dep> -w` | Add dependency to root |
| `pnpm up -r -i -L` | Interactive dependency update |
| `pnpm lerna version` | Version packages |
| `pnpm lerna publish` | Publish packages |

## Hybrid Workspaces

Some repos (like Constructive) have both PNPM packages and PGPM modules:

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'      # TypeScript packages
  - 'pgpm/*'          # PGPM CLI and tools
  - 'postgres/*'      # PostgreSQL utilities
```

The root may also have a `pgpm.json` for SQL module configuration.

## Troubleshooting

### Dependency Resolution Issues

```bash
# Clear cache and reinstall
pnpm store prune
rm -rf node_modules
pnpm install
```

### Workspace Link Issues

```bash
# Check workspace links
pnpm why <package-name>
```

### Build Order Issues

```bash
# Verify dependency graph
pnpm list -r --depth=0
```

## Best Practices

1. **Keep root private**: Never publish the root package
2. **Use workspace protocol**: Always `workspace:*` for internal deps
3. **Consistent structure**: Same directory layout across packages
4. **Shared config**: Extend root tsconfig.json, eslint.config.js
5. **Filter in CI**: Only build/test changed packages
6. **Lock file**: Always commit pnpm-lock.yaml
7. **Dedupe regularly**: Run `pnpm dedupe` periodically
8. **Document dependencies**: Clear README for each package

## References

- Related skill: `pnpm-workspace` for workspace setup
- Related skill: `pnpm-publishing` for publishing workflow
- Related skill: `pgpm-workspace` for SQL module workspaces
