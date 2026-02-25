---
name: turborepo
description: |
  Turborepo monorepo build system and orchestration. Covers task pipelines, dependsOn syntax, caching configuration, remote cache, filtering, CI optimization, environment variables, workspace management, watch mode, package boundaries, and code generation.

  Use when configuring tasks, creating packages, setting up monorepo, sharing code between apps, running changed packages, debugging cache, optimizing CI, resolving workspace dependencies, enforcing package boundaries, or generating code.
license: MIT
metadata:
  author: oakoss
  version: '1.2'
user-invocable: false
---

# Turborepo

## Overview

Build system for JavaScript/TypeScript monorepos. Caches task outputs and runs tasks in parallel based on dependency graph. Always create package tasks (not root tasks), use `turbo run` in scripts, and let `dependsOn` manage execution order. Configuration uses `turbo.json` (or `turbo.jsonc` for comments).

**When to use:** Monorepo task orchestration, build caching, CI optimization, workspace dependency management, package boundary enforcement.

**When NOT to use:** Single-package projects, non-JavaScript monorepos, projects without build steps.

## Quick Reference

| Pattern                 | Syntax                                           | Key Points                                      |
| ----------------------- | ------------------------------------------------ | ----------------------------------------------- |
| Schema                  | `"$schema": "https://turborepo.dev/schema.json"` | Always include in turbo.json                    |
| Dependency build        | `"dependsOn": ["^build"]`                        | Build dependencies first                        |
| Same-package task       | `"dependsOn": ["codegen"]`                       | Run in same package first                       |
| Specific package        | `"dependsOn": ["pkg#task"]`                      | Named package's task                            |
| Parallel lint/typecheck | Transit Nodes pattern                            | Cache invalidation without sequential execution |
| Dev server              | `"persistent": true, "cache": false`             | Long-running, non-cacheable                     |
| Sidecar tasks           | `"with": ["api#dev"]`                            | Run tasks concurrently alongside                |
| Watch mode              | `turbo watch dev`                                | Re-run on file changes                          |
| Filter by package       | `--filter=web`                                   | Single package                                  |
| Filter with deps        | `--filter=web...`                                | Package + dependencies                          |
| Changed packages        | `--affected`                                     | Changed + dependents                            |
| Debug cache             | `--summarize` or `--dry`                         | See hash inputs                                 |
| Package config          | `turbo.json` with `"extends": ["//"]`            | Per-package overrides                           |
| Composable config       | `"extends": ["@repo/config"]`                    | Extend from any workspace package               |
| Extend arrays           | `"$TURBO_EXTENDS$"` in arrays                    | Append to inherited config instead of replacing |
| Env vars in hash        | `"env": ["API_URL"]`                             | Cache invalidation on change                    |
| Boundaries              | `turbo boundaries`                               | Enforce package isolation and import rules      |
| Query graph             | `turbo query`                                    | GraphQL interface to package/task graphs        |
| Code generation         | `turbo generate`                                 | Scaffold new packages and components            |
| List packages           | `turbo ls`                                       | List all packages in monorepo                   |
| Devtools                | `turbo devtools`                                 | Visual Package Graph and Task Graph explorer    |
| Docker pruned workspace | `turbo prune <pkg> --docker`                     | Minimal monorepo slice for container builds     |

## Decision Trees

### Configure a Task

```text
Configure a task?
+-- Define task dependencies       -> dependsOn in turbo.json
+-- Lint/check-types (parallel)    -> Transit Nodes pattern
+-- Specify build outputs          -> outputs key
+-- Handle environment variables   -> env key or globalEnv
+-- Dev/watch tasks                -> persistent: true, cache: false
+-- Sidecar tasks (run alongside)  -> with key
+-- Package-specific config        -> Package turbo.json with extends: ["//"]
+-- Composable config              -> extends from any workspace package
+-- Global settings                -> globalEnv, globalDependencies, cacheDir
```

### Cache Problems

```text
Cache problems?
+-- Outputs not restored           -> Missing outputs key
+-- Unexpected cache misses        -> Use --summarize or --dry to debug
+-- Skip cache entirely            -> --force or cache: false
+-- Remote cache not working       -> Check turbo login/link
+-- Environment causing misses     -> Var not in env key
```

### Filter Packages

```text
Filter packages?
+-- By package name                -> --filter=web
+-- By directory                   -> --filter=./apps/*
+-- Package + dependencies         -> --filter=web...
+-- Package + dependents           -> --filter=...web
+-- Changed + dependents           -> --affected
```

### Explore Repository

```text
Explore repository?
+-- List all packages              -> turbo ls
+-- Query dependency graph         -> turbo query
+-- Visualize graphs               -> turbo devtools
+-- Check boundary violations      -> turbo boundaries
+-- Generate new package           -> turbo generate workspace
+-- Run custom generator           -> turbo generate run [name]
```

## Common Mistakes

| Mistake                                                                   | Correct Pattern                                                                                          |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Putting build logic in root `package.json` scripts instead of per-package | Define scripts in each package and use `turbo run` in root to delegate                                   |
| Using `^build` without declaring `workspace:*` dependency                 | Add the dependency in `package.json` first; `^build` only triggers for declared dependencies             |
| Chaining turbo tasks with `&&` in package scripts                         | Use `dependsOn` in `turbo.json` to declare task ordering                                                 |
| Not adding environment variables to the `env` key in turbo.json           | Declare all build-affecting env vars in `env` so cache hashes correctly                                  |
| Using `--parallel` flag to bypass dependency ordering                     | Configure `dependsOn` correctly or use transit nodes for parallel tasks with proper cache invalidation   |
| Using outdated schema URL                                                 | Use `https://turborepo.dev/schema.json` in `$schema` field                                               |
| Overriding inherited arrays in package configs                            | Use `$TURBO_EXTENDS$` in arrays to append instead of replace                                             |
| Defining tasks in root `turbo.json` that belong to a specific package     | Define tasks inside the package's own `turbo.json` with `extends: ["//"]`                                |
| Using `turbo <task>` shorthand in scripts or CI                           | Use `turbo run <task>` in `package.json` scripts and CI pipelines; shorthand is for interactive use only |

## Delegation

- **Monorepo structure exploration**: Use `Explore` agent to discover packages, workspace layout, and dependency relationships
- **Pipeline configuration and optimization**: Use `Task` agent to set up turbo.json tasks, configure caching, and debug cache misses
- **Monorepo architecture planning**: Use `Plan` agent to design package boundaries, shared libraries, and CI optimization strategy

> If the `pnpm-workspace` skill is available, delegate workspace setup, dependency linking, catalogs, and `pnpm deploy` to it.
> If the `changesets` skill is available, delegate versioning, changelog generation, and npm publishing to it.

## References

- [Task configuration and dependsOn patterns](references/task-configuration.md)
- [Caching, outputs, and debugging cache issues](references/caching.md)
- [Filtering, affected packages, and CI patterns](references/filtering-and-ci.md)
- [Workspace structure and package management](references/workspace-structure.md)
- [Environment variables and modes](references/environment-variables.md)
- [Watch mode, dev tasks, and anti-patterns](references/dev-and-anti-patterns.md)
- [Boundaries, query, and code generation](references/boundaries-and-tooling.md)
