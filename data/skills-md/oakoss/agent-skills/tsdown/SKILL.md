---
name: tsdown
description: 'tsdown TypeScript bundler built on Rolldown for libraries and packages. Use when bundling TypeScript libraries, generating declaration files, or publishing npm packages. Use for tsdown, bundler, rolldown, dts, declaration, library-build, esm, cjs, treeshake.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://tsdown.dev/'
user-invocable: false
---

# tsdown

## Overview

tsdown is an elegant library bundler built on Rolldown (Rust-based), providing a complete out-of-the-box solution for building TypeScript and JavaScript libraries. It handles source transformation, multiple output formats (ESM, CJS, IIFE, UMD), TypeScript declaration file generation, and package.json exports field generation with sensible defaults.

**When to use:** Building TypeScript libraries for npm, generating declaration files, producing dual ESM/CJS packages, bundling CLI tools, library development with watch mode, migrating from tsup.

**When NOT to use:** Application bundling (use Vite/Rolldown directly), server-side rendering frameworks (use framework bundlers), projects that need Webpack-specific features, simple scripts that need no bundling.

## Quick Reference

| Pattern           | API                          | Key Points                                   |
| ----------------- | ---------------------------- | -------------------------------------------- |
| Basic build       | `npx tsdown`                 | Auto-detects `src/index.ts` entry            |
| Config file       | `tsdown.config.ts`           | `defineConfig()` for type safety             |
| Entry points      | `entry: ['src/index.ts']`    | String, array, or object for named entries   |
| Output formats    | `format: ['esm', 'cjs']`     | ESM, CJS, IIFE, UMD supported                |
| Declaration files | `dts: true`                  | Auto-detects from package.json `types` field |
| Fixed extensions  | `fixedExtension: true`       | Forces `.mjs`/`.cjs` and `.d.mts`/`.d.cts`   |
| Externals         | `external: ['react']`        | node_modules external by default             |
| Bundle deps       | `noExternal: ['lodash-es']`  | Force-bundle specific dependencies           |
| Target            | `target: 'node18'`           | ES version or Node version                   |
| Platform          | `platform: 'node'`           | `node`, `browser`, or `neutral`              |
| Minification      | `minify: true`               | Tree shaking enabled separately              |
| Tree shaking      | `treeshake: true`            | Dead code elimination                        |
| Source maps       | `sourcemap: true`            | Inline or external source maps               |
| Watch mode        | `tsdown --watch`             | Auto-rebuild on file changes                 |
| Clean output      | `clean: true`                | Remove output directory before build         |
| Validation        | `--publint --attw`           | Package quality checks post-build            |
| Size report       | `--report`                   | Bundle size with gzip/brotli stats           |
| Multiple configs  | `defineConfig([...])`        | Array of configs for different outputs       |
| Dynamic config    | `defineConfig((opts) => {})` | Function receiving CLI options               |
| Programmatic API  | `import { build }`           | Use in Node.js scripts                       |
| Banner/Footer     | `banner: { js: '...' }`      | Prepend/append to output files               |
| onSuccess hook    | `onSuccess: async () => {}`  | Run after successful build                   |
| Node protocol     | `nodeProtocol: true`         | Add/strip `node:` prefix on built-in imports |

## Common Mistakes

| Mistake                                         | Correct Pattern                                                               |
| ----------------------------------------------- | ----------------------------------------------------------------------------- |
| Not setting `fixedExtension` with dual formats  | Use `fixedExtension: true` for `.mjs`/`.cjs` when publishing both ESM and CJS |
| Bundling all node_modules into library output   | Dependencies are external by default; use `noExternal` only for specific deps |
| Using `dts: true` without TypeScript configured | Ensure `tsconfig.json` exists with proper `compilerOptions`                   |
| Setting `target` too low for modern syntax      | Match target to your minimum supported Node/browser version                   |
| Missing `types` field in package.json           | Add `types` or `exports` types condition for declaration resolution           |
| Not cleaning output before format changes       | Use `clean: true` to avoid stale files from previous builds                   |
| Inline `external` for Node built-ins            | Node built-ins (`node:fs`, etc.) are auto-externalized on `platform: 'node'`  |
| Using interactive CLI flags in CI               | Use config file or non-interactive CLI flags for CI builds                    |

## Delegation

- **Build configuration review**: Use `Task` agent to analyze tsdown config for correctness
- **Package publishing**: Use `Explore` agent to verify package.json exports and types fields
- **Migration from tsup**: Use `Task` agent to map tsup options to tsdown equivalents

## References

- [Configuration: config file, entry points, output formats, target, platform, externals](references/configuration.md)
- [Declaration files: DTS generation, isolated declarations, type bundling](references/declaration-files.md)
- [Advanced features: plugins, code splitting, tree shaking, watch mode, validation](references/advanced-features.md)
