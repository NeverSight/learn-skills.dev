---
name: pnpm-workspace
description: 'pnpm workspace monorepo management with filtering, catalogs, and shared configs. Use when setting up monorepos, managing workspace dependencies, filtering package commands, or sharing configuration across packages.'
license: MIT
metadata:
  author: oakoss
  version: '1.2'
  source: https://pnpm.io/workspaces
---

# pnpm Workspace

## Overview

pnpm workspaces provide built-in monorepo support through `pnpm-workspace.yaml`, the `workspace:` protocol for local package linking, and powerful filtering to run commands across specific packages. Catalogs enforce consistent dependency versions across all workspace packages.

**When to use:** Multi-package repositories, shared libraries with consuming apps, consistent dependency management across packages, running commands on subsets of packages.

**When NOT to use:** Single-package projects, projects already using npm/yarn workspaces (migration required), projects that need floating dependency versions per package.

## Quick Reference

| Pattern                  | API / Config                                   | Key Points                                              |
| ------------------------ | ---------------------------------------------- | ------------------------------------------------------- |
| Define workspace         | `pnpm-workspace.yaml` with `packages` globs    | Globs match directories containing `package.json`       |
| Link local package       | `"dep": "workspace:*"`                         | Always resolves to local workspace package              |
| Link with version range  | `"dep": "workspace:^1.0.0"`                    | Fails install if local version does not satisfy range   |
| Default catalog          | `catalog:` key in `pnpm-workspace.yaml`        | Single source of truth for dependency versions          |
| Named catalog            | `catalogs:` key with named groups              | Multiple version sets (e.g., `react18`, `react17`)      |
| Use catalog in package   | `"dep": "catalog:"` or `"dep": "catalog:name"` | Resolved to actual version on `pnpm publish`            |
| Filter by name           | `--filter <name>` or `-F <name>`               | Exact name or glob pattern (`@scope/*`)                 |
| Filter with dependencies | `--filter "foo..."`                            | Package and all its dependencies                        |
| Filter with dependents   | `--filter "...foo"`                            | Package and all packages that depend on it              |
| Filter by directory      | `--filter "./packages/app"`                    | All packages under a directory path                     |
| Filter by git changes    | `--filter "[origin/main]"`                     | Packages changed since a commit or branch               |
| Exclude from filter      | `--filter "!foo"`                              | Remove matching packages from selection                 |
| Run script in package    | `pnpm --filter <pkg> <script>`                 | Runs script only in matched packages                    |
| Recursive run            | `pnpm -r run <script>`                         | Runs script in all workspace packages                   |
| Install all              | `pnpm install`                                 | Single lockfile for entire workspace                    |
| Publish workspace pkg    | `pnpm publish`                                 | Replaces `workspace:` and `catalog:` with real versions |
| Inject workspace deps    | `inject-workspace-packages=true` in `.npmrc`   | Hard-links instead of symlinks; required for deploy     |
| Script security (v10+)   | `allowBuilds` in `package.json`                | Lifecycle scripts blocked by default; opt-in per dep    |

## Common Mistakes

| Mistake                                                 | Correct Pattern                                                         |
| ------------------------------------------------------- | ----------------------------------------------------------------------- |
| Using `workspace:*` then publishing as-is               | pnpm automatically replaces `workspace:*` with real versions on publish |
| Forgetting to list directory in `packages:`             | Every package directory must match a glob in `pnpm-workspace.yaml`      |
| Using `npm install` in workspace packages               | Always use `pnpm install` from the workspace root                       |
| Hardcoding versions duplicated across packages          | Use `catalog:` to centralize version definitions                        |
| Running `pnpm install` inside a sub-package             | Run from workspace root; use `--filter` to target packages              |
| Expecting `--filter` to match directory names           | `--filter` matches `package.json` `name` field, not directory names     |
| Not escaping `!` in zsh for exclude filters             | Use `\!` or quote the filter: `--filter="!foo"`                         |
| Using `workspace:` for non-workspace deps               | `workspace:` protocol only works for packages defined in the workspace  |
| Lifecycle scripts failing after pnpm 10 upgrade         | pnpm 10 blocks scripts by default; add deps to `allowBuilds` in config  |
| Using `pnpm deploy` without `inject-workspace-packages` | Set `inject-workspace-packages=true` in `.npmrc` (required in pnpm 10)  |

## Delegation

- **Workspace scaffolding**: Use `Explore` agent to discover existing package structure
- **Dependency auditing**: Use `Task` agent to check version consistency across packages

> If the `turborepo` skill is available, delegate build orchestration, task caching, and CI optimization to it.
> If the `changesets` skill is available, delegate versioning, changelog generation, and npm publishing to it.

## References

- [Workspace setup, workspace protocol, and catalogs](references/workspace-setup.md)
- [Filtering packages for targeted commands](references/filtering.md)
- [Shared configuration across workspace packages](references/shared-configs.md)
- [Monorepo integration: pnpm + Turborepo + Changesets pipeline](references/monorepo-integration.md)
