---
name: taze
description: Keep JavaScript/TypeScript dependencies fresh with safety rails and monorepo support.
metadata:
  author: hairy
  version: "2026.02.24"
  source: Generated from https://github.com/antfu-collective/taze, scripts located at https://github.com/hairyf/skills
---

> The skill is based on `taze` (latest README on GitHub) as of 2026-02-24.

`taze` is a lightweight CLI for upgrading dependencies in JavaScript/TypeScript projects and monorepos. It focuses on safe-by-default version bumps, powerful filtering, and configuration via flags or `taze.config.(js|ts)` so agents can orchestrate dependency maintenance workflows.

This skill is written for agents that:

- Need to review or perform dependency upgrades using `taze`
- Work in monorepos and must keep workspace packages in sync
- Must follow safety policies around tests, lint/typecheck, and upgrade strategy

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overview & CLI modes | `taze` goals, install-free usage, major/minor/patch modes | [core-overview](references/core-overview.md) |
| Monorepo support | `-r` recursive mode, workspaces, local packages | [core-monorepo](references/core-monorepo.md) |

## Features

### Configuration & Filtering

| Topic | Description | Reference |
|-------|-------------|-----------|
| Config file usage | `taze.config.js/ts`, `defineConfig`, options mapping | [features-config-file](references/features-config-file.md) |
| Filters & peer deps | `--include/--exclude`, locked deps, `--peer`, dep fields | [features-filters-and-peer-deps](references/features-filters-and-peer-deps.md) |

## Best Practices & Upgrade Policy

| Topic | Description | Reference |
|-------|-------------|-----------|
| Safe upgrade workflow | When to upgrade, required checks (tests, e2e, lint, typecheck), major-default policy with fallback | [best-practices-upgrade-strategy](references/best-practices-upgrade-strategy.md) |

