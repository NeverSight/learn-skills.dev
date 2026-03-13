---
name: tsdown
description: tsdown patterns for bundling TypeScript and JavaScript libraries powered by Rolldown. Covers configuration, output formats, type declarations, dependency handling, plugins, monorepo builds, and migration from tsup. Use when building libraries, generating type declarations, bundling for multiple formats, configuring tsdown, or migrating from tsup.
---

# tsdown — Library Bundler

Blazing-fast bundler for TypeScript/JavaScript libraries powered by Rolldown and Oxc. A modern replacement for tsup.

## Setup

```shell
npm install -D tsdown

# Or scaffold a new project
npm create tsdown@latest
```

Requires Node.js 20.19+.

## Basic Configuration

```typescript
// tsdown.config.ts
import { defineConfig } from "tsdown";

export default defineConfig({
    entry: ["src/index.ts"],
    format: ["esm", "cjs"],
    dts: true,
});
```

### Defaults (Different from tsup)

| Option   | tsdown default                                         | tsup default |
| -------- | ------------------------------------------------------ | ------------ |
| `format` | `esm`                                                  | `cjs`        |
| `clean`  | `true`                                                 | `false`      |
| `dts`    | Auto-enabled if `types` field exists in `package.json` | `false`      |

## Entry Points

```typescript
// Single entry
entry: ["src/index.ts"],

// Named entries
entry: {
  index: "src/index.ts",
  utils: "src/utils.ts",
  cli: "src/cli.ts",
},

// Glob with exclusions
entry: ["src/**/*.ts", "!**/*.test.ts"],
```

## Output Formats

```typescript
// Dual ESM + CJS (most common for libraries)
format: ["esm", "cjs"],

// Browser global
format: ["iife"],
globalName: "MyLib",

// UMD for CDN/script tag compatibility
format: ["umd"],
globalName: "MyLib",
```

### Package.json Exports

Auto-generate the `exports` field:

```typescript
export default defineConfig({
    entry: ["src/index.ts"],
    format: ["esm", "cjs"],
    dts: true,
    exports: true, // auto-generates package.json exports field
});
```

## Type Declarations

```typescript
// Basic — generates .d.ts alongside output
dts: true,

// With options
dts: {
  sourcemap: true,
  compilerOptions: {
    composite: false,
  },
},
```

Always enable `dts` for published TypeScript libraries.

## Dependency Handling

tsdown automatically externalizes `dependencies` and `peerDependencies` from `package.json`.

```typescript
// Manually external
external: ["react", "react-dom", /^@myorg\//],

// Force-bundle a dependency (inline it)
noExternal: ["tiny-utility-to-inline"],
```

- External by default: `dependencies`, `peerDependencies`.
- Bundled by default: `devDependencies`.

## Platform and Target

```typescript
// Node.js library (default)
platform: "node",
target: "es2022",

// Browser library
platform: "browser",
target: "es2020",

// Isomorphic
platform: "neutral",
```

## Minification

```typescript
// Full minification
minify: true,

// Dead code elimination only (smaller output, readable)
minify: "dce-only",
```

## Shims

Add ESM/CJS interop shims (`__dirname`, `__filename`, `import.meta.url`):

```typescript
shims: true,
```

Enable when publishing dual ESM/CJS packages that reference Node.js globals.

## Source Maps

```typescript
sourcemap: true,          // external .map files
sourcemap: "inline",      // embedded in output
sourcemap: "hidden",      // generated but not referenced
```

## Unbundle Mode

Preserve the source directory structure instead of bundling into a single file:

```typescript
export default defineConfig({
    entry: ["src/**/*.ts", "!**/*.test.ts"],
    unbundle: true,
    format: ["esm"],
    dts: true,
});
```

Useful for utility libraries where consumers may want to import individual modules.

## Plugins

tsdown supports Rolldown, Rollup, and unplugin plugins:

```typescript
import { wasm } from "rolldown-plugin-wasm";

export default defineConfig({
    entry: ["src/index.ts"],
    plugins: [wasm()],
});
```

## Multiple Configurations

Export an array for different build targets:

```typescript
export default defineConfig([
    {
        entry: ["src/index.ts"],
        format: ["esm", "cjs"],
        dts: true,
    },
    {
        entry: ["src/cli.ts"],
        format: ["esm"],
        platform: "node",
        banner: { js: "#!/usr/bin/env node" },
    },
]);
```

## Conditional Configuration

```typescript
export default defineConfig((options) => {
    const isDev = options.watch;
    return {
        entry: ["src/index.ts"],
        format: ["esm", "cjs"],
        minify: !isDev,
        sourcemap: isDev,
    };
});
```

## Monorepo / Workspace Builds

Build all packages in a monorepo from a single config:

```typescript
export default defineConfig({
    workspace: "packages/*",
    entry: ["src/index.ts"],
    format: ["esm", "cjs"],
    dts: true,
});
```

## Lifecycle Hooks

```typescript
export default defineConfig({
    entry: ["src/index.ts"],
    hooks: {
        "build:before": async (context) => {
            // Pre-build tasks (codegen, validation)
        },
        "build:done": async (context) => {
            // Post-build tasks (copy files, notifications)
        },
    },
});
```

## CI Configuration

Use `'ci-only'` and `'local-only'` to vary behavior by environment:

```typescript
export default defineConfig({
    entry: ["src/index.ts"],
    format: ["esm", "cjs"],
    dts: true,
    failOnWarn: "ci-only", // fail on warnings in CI only
    publint: "ci-only", // validate package structure in CI
    attw: "ci-only", // check "are the types wrong" in CI
});
```

## Common Recipes

### React Component Library

```typescript
export default defineConfig({
    entry: ["src/index.tsx"],
    format: ["esm", "cjs"],
    dts: true,
    external: ["react", "react-dom"],
});
```

### Node.js CLI Tool

```typescript
export default defineConfig({
    entry: ["src/cli.ts"],
    format: ["esm"],
    platform: "node",
    target: "es2022",
    banner: { js: "#!/usr/bin/env node" },
    minify: true,
});
```

### Dual Package with Shims

```typescript
export default defineConfig({
    entry: ["src/index.ts"],
    format: ["esm", "cjs"],
    dts: true,
    shims: true,
    exports: true,
    clean: true,
});
```

## Migration from tsup

```shell
npx tsdown migrate
```

This handles ~90% of config conversion automatically. Key differences to review:

- `format` defaults to `esm` (tsup defaults to `cjs`).
- `clean` is enabled by default.
- `dts` auto-enables if `types` field exists in `package.json`.
- `onSuccess` → use `hooks['build:done']` instead.
- `splitting` → enabled by default, use `splitting: false` to disable.

## CLI Reference

```shell
tsdown                           # Build with defaults
tsdown --watch                   # Watch mode
tsdown --format esm,cjs          # Specify formats
tsdown --dts                     # Generate declarations
tsdown --minify                  # Minify output
tsdown --outDir lib              # Custom output directory
tsdown --sourcemap               # Generate source maps
tsdown --config custom.ts        # Custom config file
tsdown src/a.ts src/b.ts         # Multiple entries
```
