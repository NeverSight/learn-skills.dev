---
name: storybook-rsbuild
description: Set up or migrate Storybook to use the Rsbuild builder. Handles fresh setup for React, Vue 3, HTML, Web Components, and React Native Web, migration from webpack5 or Vite frameworks, and integrations with Rslib, Modern.js, and Rspack. Use when asked to add Storybook, migrate Storybook to Rsbuild, configure rsbuildFinal, or integrate Storybook with Rslib/Modern.js/Rspack.
compatibility: Requires network access to read upstream docs at storybook.rsbuild.rs
---

# Storybook Rsbuild

## Step 1 — Detect scenario

Read `package.json` and project structure to determine existing Storybook state:

1. Check for `.storybook/` directory (in monorepos, check both root and per-package)
2. Check `package.json` for `storybook` scripts or `@storybook/*` / `storybook-*-rsbuild` in dependencies or devDependencies
3. If Storybook exists **and already uses `storybook-*-rsbuild`** → already set up; go to [Configuration](#configuration) or [Troubleshooting](#troubleshooting) as needed
4. If Storybook exists **with a non-Rsbuild builder** (`@storybook/*-webpack5`, `@storybook/*-vite`, etc.) → go to [Migration Workflow](#migration-workflow)
5. **No Storybook found** → go to [Fresh Setup Workflow](#fresh-setup-workflow)

---

## Fresh Setup Workflow

### 1. Detect ecosystem integration

Read `package.json` dependencies and devDependencies, check in order:

| Signal                                 | Ecosystem   | Integration guide                                        |
| -------------------------------------- | ----------- | -------------------------------------------------------- |
| `@rslib/core`                          | Rslib       | https://storybook.rsbuild.rs/guide/integrations/rslib    |
| `@modern-js/app-tools`                 | Modern.js   | https://storybook.rsbuild.rs/guide/integrations/modernjs |
| `@rspack/core` without `@rsbuild/core` | Pure Rspack | https://storybook.rsbuild.rs/guide/integrations/rspack   |

If matched, read the integration guide and **apply its constraints as an overlay** alongside the steps below.

### 2. Detect UI framework

Infer the UI framework from app dependencies (`react`, `vue`, `lit`, etc.):

| UI Framework     | Framework package                    | Guide                                                         |
| ---------------- | ------------------------------------ | ------------------------------------------------------------- |
| React            | `storybook-react-rsbuild`            | https://storybook.rsbuild.rs/guide/framework/react            |
| Vue 3            | `storybook-vue3-rsbuild`             | https://storybook.rsbuild.rs/guide/framework/vue              |
| Vanilla JS/TS    | `storybook-html-rsbuild`             | https://storybook.rsbuild.rs/guide/framework/vanilla          |
| Web Components   | `storybook-web-components-rsbuild`   | https://storybook.rsbuild.rs/guide/framework/web-components   |
| React Native Web | `storybook-react-native-web-rsbuild` | https://storybook.rsbuild.rs/guide/framework/react-native-web |

### 3. Set up Storybook

1. In monorepos, operate in the package that will host stories
2. Read and follow the framework guide matched above
3. Ensure `.storybook/main.*` uses the correct `framework: '<storybook-*-rsbuild>'`
4. Ensure `package.json` has `storybook dev` and `storybook build` scripts
5. Run [Verification](#verification) below

## Migration Workflow

Read the upstream migration guide: https://storybook.rsbuild.rs/guide/migration

Follow these steps **in order**:

1. **Detect migration type** — read `.storybook/main.*` (`framework` field and/or `core.builder`) and `package.json` dependencies to classify as "from webpack5" or "from Vite", then select the matching section in the migration guide
2. **Resolve version compatibility** — read the "Version compatibility" section in the migration guide, select the correct `storybook-rsbuild` major based on installed Storybook version
3. **Replace packages** — apply the install/remove mapping from the migration guide using the project's package manager (detect from lockfile); only change packages required by the migration
4. **Update `.storybook/main.*`** — apply the config changes exactly as shown in the migration guide for the detected framework
5. **Migrate custom builder hooks** — search for legacy builder hooks (`webpackFinal` / `viteFinal`); if found, convert following the upstream configuration guide (https://storybook.rsbuild.rs/guide/configuration)
6. **Handle addon compatibility** — keep addons unchanged initially; if build errors indicate addon incompatibility, consult the migration guide's addon section and apply the recommended fix
7. **Verify** — confirm the migration is complete, then run [Verification](#verification) below

If a factual mapping is needed (version table, package names, conversion patterns) and not present in this skill, fetch it from the upstream docs — do not guess.

---

## Verification

1. `storybook dev` starts without errors
2. Stories render correctly
3. HMR works
4. `storybook build` completes
5. Check startup logs to confirm the Rsbuild builder is active (not webpack/vite)

## Troubleshooting

- **Cache issues**: remove `node_modules/.cache/storybook` and retry
- **Residual config**: if dev fails after migration, temporarily remove custom `rsbuildFinal` block to isolate the issue, then re-add incrementally
- For debugging and other issues, consult the upstream migration guide's "Debugging" section and https://storybook.rsbuild.rs/guide/configuration

## Edge Cases

- **Monorepo**: locate the package that hosts stories; operate there, not at root
- **Multiple `.storybook/` dirs**: pick the one referenced by `package.json` scripts
- **TS path aliases**: ensure aliases are preserved after migration; consult the upstream configuration guide for how to configure `rsbuildFinal`

## Configuration

For `rsbuildFinal`, builder options, TypeScript, and framework-specific options → read https://storybook.rsbuild.rs/guide/configuration

## Examples

For working sandboxes → https://storybook.rsbuild.rs/guide/examples
