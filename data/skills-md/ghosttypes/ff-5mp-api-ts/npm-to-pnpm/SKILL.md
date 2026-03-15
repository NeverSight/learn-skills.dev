---
name: npm-to-pnpm
description: Migrate projects from npm to pnpm including lockfile conversion, workspace setup, CI/CD updates, and troubleshooting. Use when converting a single package from npm to pnpm, migrating npm workspaces or monorepos, updating CI/CD pipelines for pnpm, troubleshooting issues after npm to pnpm migration, or converting package-lock.json to pnpm-lock.yaml.
---

# npm to pnpm Migration

## Overview

Migrate existing npm projects to pnpm. Covers single packages, workspaces/monorepos, CI/CD configuration, and common migration issues.

**Current pnpm version:** 10.28 (January 2026) - See `version_info.md` for details.

## Quick Start (Single Package)

```bash
# 1. Install pnpm
npm install -g pnpm

# 2. Remove npm artifacts
rm package-lock.json
rm -rf node_modules

# 3. Generate pnpm lockfile
pnpm import

# 4. Install dependencies
pnpm install

# 5. Verify
pnpm test && pnpm build
```

## Workflow Decision Tree

**Is this a single package or workspace/monorepo?**

- **Single package:** Use `workflow_single_package.md`
- **Workspace/monorepo:** Use `workflow_workspace_monorepo.md`

**Experiencing issues after migration?**

- **Module not found:** See `troubleshooting.md` - Module Resolution Issues
- **Build fails:** See `troubleshooting.md` - Build and Tooling Issues
- **CI fails:** See `troubleshooting.md` - CI/CD Issues
- **Other issues:** See `troubleshooting.md`

**Need npm command equivalents?**

- See `cli_reference.md` for all command translations

## Core Migration Steps

### 1. Install pnpm

See `installation.md` for all installation methods. Quick options:

```bash
# Via npm
npm install -g pnpm

# Via standalone script (recommended)
curl -fsSL https://get.pnpm.io/install.sh | sh -s -- --version=10.28.0

# Windows PowerShell
iwr https://get.pnpm.io/install.ps1 -useb | iex
```

### 2. Convert Lockfile

Use `pnpm import` to convert `package-lock.json` or `yarn.lock` to `pnpm-lock.yaml`:

```bash
pnpm import
```

See `import_command.md` for details on import behavior and workspace considerations.

### 3. Install Dependencies

```bash
pnpm install
```

Key flags:
- `--frozen-lockfile` - CI mode, exact install from lockfile
- `--shamefully-hoist` - Temporarily work around module resolution issues
- `--force` - Regenerate lockfile from package.json

See `install_command.md` for full install options.

### 4. Update Scripts

npm → pnpm command changes:

| npm | pnpm |
|-----|-------|
| `npm run <script>` | `pnpm <script>` or `pnpm run <script>` |
| `npm install <pkg>` | `pnpm add <pkg>` |
| `npm install -D <pkg>` | `pnpm add -D <pkg>` |
| `npm uninstall <pkg>` | `pnpm remove <pkg>` |
| `npx <cmd>` | `pnpm exec <cmd>` or `pnpm dlx <cmd>` |

See `cli_reference.md` for complete command reference.

## Workspaces and Monorepos

npm workspaces require different handling:

1. Create `pnpm-workspace.yaml` to define workspace packages
2. Change workspace dependencies from `*` to `workspace:*` protocol
3. Update scripts to use `pnpm -r` instead of `npm --workspaces`

**Full guide:** `workflow_workspace_monorepo.md`

## Key Differences to Understand

### Module Structure

pnpm uses a content-addressable store with symlinks, not a flat `node_modules`. This:

- Saves disk space (packages stored once globally)
- Creates stricter dependency resolution (reveals hidden dependencies)
- May require explicit dependency declarations

### Lockfile

npm ignores `package-lock.json`. Use `pnpm import` to convert. After conversion, commit `pnpm-lock.yaml` to version control.

See `limitations.md` for details on lockfile differences.

## Common Migration Gotchas

### Missing Dependencies

**Symptom:** "Cannot find module" errors after migration

**Cause:** pnpm's strict layout reveals packages that were "accidentally" available in npm

**Solution:**
```bash
pnpm add <missing-package>
```

### Workspace Protocol

**npm:** `"my-utils": "*"`

**pnpm:** `"my-utils": "workspace:*"`

### Lifecycle Scripts

pnpm may run pre/post scripts differently. If needed:

```ini
# .npmrc
enable-pre-post-scripts=true
```

## CI/CD Updates

Update your CI to use pnpm:

**GitHub Actions:**
```yaml
- uses: pnpm/action-setup@v4
  with:
    version: 10.28.0
- uses: actions/setup-node@v4
  with:
    cache: 'pnpm'
```

See `workflow_single_package.md` for more CI examples.

## Reference Files Index

### Workflow Guides

- `workflow_single_package.md` - Standalone package migration
- `workflow_workspace_monorepo.md` - Workspace and monorepo migration
- `troubleshooting.md` - Common issues and solutions

### Command Reference

- `cli_reference.md` - npm → pnpm command translation
- `install_command.md` - Full pnpm install documentation
- `add_command.md` - Dependency adding options
- `import_command.md` - Lockfile conversion details

### Documentation

- `version_info.md` - Current version (10.28) and installation
- `installation.md` - All installation methods
- `limitations.md` - Known pnpm limitations
- `workspaces.md` - Full workspace documentation
- `npm_vs_pnpm.md` - Feature comparison
- `release_10.28.md` - Latest release notes
- `releases.md` - Full release history

### Configuration (.npmrc)

Common settings for npm migrants:

```ini
# Temporary migration aids
shamefully-hoist=true
auto-install-peers=true

# Strictness settings
strict-peer-dependencies=false
enable-pre-post-scripts=true
```

## Migration Checklist

- [ ] Install pnpm globally
- [ ] Remove `package-lock.json`
- [ ] Run `pnpm import`
- [ ] Run `pnpm install`
- [ ] Verify tests pass
- [ ] Verify build succeeds
- [ ] Update CI/CD configuration
- [ ] Update documentation/README
- [ ] Update team on command changes
- [ ] Commit `pnpm-lock.yaml`

## When NOT to Use pnpm

Consider staying with npm if:

- Project relies on npm-specific features (npx quirks, flat modules)
- Legacy tooling with hardcoded node_modules paths
- Strict requirements for npm compatibility
- See `limitations.md` for full details
