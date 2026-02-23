---
name: tanstack-cli
description: >
  TanStack Config for shared build tooling, Vite plugins, and package configuration across TanStack projects.
  Use when configuring TanStack library builds or contributing to TanStack packages.
  Use for tanstack-config, tanstack-cli, vite-plugin, package-config, library-build.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://tanstack.com/config/latest'
---

# TanStack Config

## Overview

TanStack Config provides opinionated tooling to build, version, and publish JavaScript/TypeScript packages with minimal configuration and consistent results. It leverages Vite for library builds with automatic dual ESM/CJS output and type generation, plus automated publishing with conventional-commit-based versioning.

**When to use:** Building TanStack libraries or packages that follow TanStack conventions, contributing to TanStack open-source projects, setting up dual ESM/CJS library builds with Vite, automating package publishing with conventional commits.

**When NOT to use:** Application builds (use framework-specific tooling), non-library projects, projects not using pnpm, projects that need non-Vite build pipelines.

## Quick Reference

| Pattern            | API / Package                                       | Key Points                                              |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------- |
| Vite build config  | `tanstackViteConfig()` from `@tanstack/vite-config` | Merge with `defineConfig` via `mergeConfig`             |
| Entry point        | `entry: './src/index.ts'`                           | Single file or array of entry files                     |
| Source directory   | `srcDir: './src'`                                   | Used for declaration file generation                    |
| CJS output         | `cjs: true` (default)                               | Generates `.cjs` and `.d.cts` alongside ESM             |
| External deps      | `externalDeps: [/^@internal\//]`                    | Auto-detected from `package.json`, extend with patterns |
| Bundled deps       | `bundledDeps: ['tiny-invariant']`                   | Bundle instead of externalize                           |
| Exclude from types | `exclude: ['./src/**/*.test.ts']`                   | Patterns to skip during type generation                 |
| Custom tsconfig    | `tsconfigPath: './tsconfig.build.json'`             | Override default tsconfig for builds                    |
| Declaration hook   | `beforeWriteDeclarationFile(path, content)`         | Transform `.d.ts` content before write                  |
| Publish automation | `publish()` from `@tanstack/publish-config`         | Conventional commits drive versioning                   |
| Branch configs     | `branchConfigs: { main, beta, alpha }`              | Control prerelease and stable channels                  |
| Package list       | `packages: [{ name, packageDir }]`                  | Monorepo package definitions                            |
| Build script       | `vite build && publint --strict`                    | Standard build with strict linting                      |

## Common Mistakes

| Mistake                                          | Correct Pattern                                                            |
| ------------------------------------------------ | -------------------------------------------------------------------------- |
| Missing `"type": "module"` in `package.json`     | Set `"type": "module"` for ESM-first builds                                |
| Using `defineConfig` alone without `mergeConfig` | Use `mergeConfig(defineConfig({...}), tanstackViteConfig({...}))`          |
| Forgetting `entry` or `srcDir` options           | Both are required for `tanstackViteConfig` to work                         |
| Missing `exports` field in `package.json`        | Define `import` and `require` conditions with types                        |
| Not awaiting `publish()` promise                 | Handle with `.then()` and `.catch()` for error reporting                   |
| Using npm or yarn instead of pnpm                | pnpm is the only supported package manager                                 |
| Omitting `publint --strict` from build script    | Add `publint --strict` after `vite build` to catch packaging issues        |
| Setting `tag` without `v` prefix                 | Manual version tags must start with `v` (e.g., `v1.0.0`)                   |
| Wrong commit type for release level              | `fix`/`refactor`/`perf` = patch, `feat` = minor, `BREAKING CHANGE` = major |

## Requirements

- Node.js v18.17+
- pnpm v8+
- Git CLI
- GitHub CLI (pre-installed on GitHub Actions)
- Vite (peer dependency for build config)
- publint (recommended for build validation)

## Delegation

- **Build configuration review**: Use `Task` agent to verify Vite config and `package.json` exports
- **Publishing workflow setup**: Use `Explore` agent to check CI/CD integration patterns
- **Package validation**: Run `publint --strict` after builds to catch packaging issues

## References

- [Configuration and Vite plugin setup](references/configuration.md)
- [Publishing and version management](references/publishing.md)
