---
name: workleap-web-configs
description: |
  Workleap's shared web configuration packages (@workleap/eslint-configs, typescript-configs, rsbuild-configs, rslib-configs, stylelint-configs, browserslist-config).

  Use when:
  (1) Setting up or customizing shared web tooling configs in a Workleap project
  (2) Configuring ESLint by project type (web app, React library, TS library, monorepo)
  (3) Configuring TypeScript by project type (web-application, library, monorepo-workspace)
  (4) Configuring Rsbuild or Rslib bundling (dev, build, Storybook)
  (5) Configuring Stylelint, Browserslist, or monorepo (Turborepo) vs polyrepo strategies
  (6) Extending or customizing shared configs, troubleshooting ESM/ESNext constraints
metadata:
  version: 1.2
---

# wl-web-configs

Workleap's shared configuration library for web tooling. Provides pre-configured packages for ESLint, TypeScript, Rsbuild, Rslib, Stylelint, and Browserslist.

## Philosophy

- **No lock-in**: Default configurations can always be extended or overridden
- **By project type**: Configurations are composed internally and offered per project type for simplicity
- **ESM/ESNext by default**: Targets modern JavaScript environments
- **Distributed via NPM**: Easy to adopt new features by bumping package versions

## Supported Tools (Active)

| Tool | Package | Purpose |
|------|---------|---------|
| Browserslist | `@workleap/browserslist-config` | Browser targets for apps |
| ESLint | `@workleap/eslint-configs` | Code linting |
| Stylelint | `@workleap/stylelint-configs` | CSS linting |
| TypeScript | `@workleap/typescript-configs` | Type checking (linting only) |
| Rsbuild | `@workleap/rsbuild-configs` | Web application bundling |
| Rslib | `@workleap/rslib-configs` | Library bundling |

**In maintenance mode** (do not recommend): PostCSS, SWC, webpack, tsup

## Quick Reference

### Which Configuration to Use?

| Project Type | ESLint | TypeScript | Bundler |
|--------------|--------|------------|---------|
| Web app with React | `defineWebApplicationConfig` | `web-application.json` | `@workleap/rsbuild-configs` |
| React library | `defineReactLibraryConfig` | `library.json` | `@workleap/rslib-configs` |
| TypeScript library (no React) | `defineTypeScriptLibraryConfig` | `library.json` | `@workleap/rslib-configs` |
| Monorepo workspace root | `defineMonorepoWorkspaceConfig` | `monorepo-workspace.json` | N/A |

### Browserslist (Apps Only)

```bash
pnpm add -D @workleap/browserslist-config browserslist
```

```text
# .browserslistrc
extends @workleap/browserslist-config
```

Only for projects emitting application bundles. Libraries should NOT include Browserslist.

To add custom browser targets while still using the shared config:

```text
# .browserslistrc
extends @workleap/browserslist-config
IE 11
last 2 OperaMobile 12.1 versions
```

## Reference Guide

For comprehensive setup guides, options, and examples, read the appropriate reference file:

- **ESLint** — [references/eslint.md](references/eslint.md): Installation, `define*Config` functions, rule categories, customization, and VS Code integration
- **TypeScript** — [references/typescript.md](references/typescript.md): Config files by project type, compiler option overrides, path mappings, and CLI scripts
- **Rsbuild** — [references/rsbuild.md](references/rsbuild.md): Dev/build/Storybook configs, predefined options, transformers, and Turborepo setup
- **Rslib** — [references/rslib.md](references/rslib.md): Library build/dev/Storybook configs, bundleless vs bundle, transformers, and type declarations
- **Stylelint** — [references/stylelint.md](references/stylelint.md): Installation, `.stylelintrc.json` setup, Prettier integration, and VS Code settings

## Critical Rules

1. **Never invent APIs**: Only suggest documented options and patterns
2. **Respect maintenance mode**: Do not recommend PostCSS, SWC, webpack, or tsup configs
3. **ESM by default**: All configs target ESM/ESNext unless migrating legacy code
4. **Browserslist for apps only**: Libraries should not include Browserslist config
5. **TypeScript for linting**: The shared TypeScript configs focus on linting; bundlers handle transpilation
