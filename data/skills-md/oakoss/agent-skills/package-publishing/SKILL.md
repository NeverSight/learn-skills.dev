---
name: package-publishing
description: 'npm package publishing patterns for modern TypeScript libraries. Use when configuring package.json exports, setting up dual ESM/CJS builds, or publishing to npm. Use for npm-publish, package-json, exports, main, module, types, dual-package, provenance, prepublishOnly.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://docs.npmjs.com/cli/v10/configuring-npm/package-json'
user-invocable: false
---

# Package Publishing

## Overview

Covers modern npm package authoring: `package.json` configuration with the `exports` field, dual ESM/CJS builds, TypeScript type declarations, and secure publishing workflows with provenance.

**When to use:** Configuring package entry points, setting up conditional exports, building dual-format packages, publishing scoped packages, or troubleshooting module resolution.

**When NOT to use:** Application-level bundling (Vite/webpack app configs), monorepo workspace orchestration (Turborepo/Nx), private registry setup (Verdaccio/Artifactory).

## Quick Reference

| Pattern             | Field / Command                           | Key Points                                       |
| ------------------- | ----------------------------------------- | ------------------------------------------------ |
| Entry point         | `exports` in package.json                 | Replaces `main`/`module`; encapsulates internals |
| CJS fallback        | `main`                                    | Legacy consumers without `exports` support       |
| ESM entry           | `module`                                  | Bundler convention; not used by Node.js          |
| Type declarations   | `types` condition in `exports`            | Must be listed first in each condition block     |
| Subpath exports     | `"./utils": { ... }`                      | Clean public API; blocks deep imports            |
| Conditional exports | `import`/`require` conditions             | Toggle ESM vs CJS per consumer                   |
| Package type        | `"type": "module"`                        | Makes `.js` files ESM; use `.cjs` for CommonJS   |
| Side effects        | `"sideEffects": false`                    | Enables tree-shaking in bundlers                 |
| Peer deps           | `peerDependencies`                        | Shared runtime deps (React, Vue, etc.)           |
| Engine constraints  | `"engines": { "node": ">=18" }`           | Document minimum Node.js version                 |
| Files allowlist     | `"files": ["dist"]`                       | Controls what gets published to npm              |
| Prepublish check    | `"prepublishOnly": "npm run build"`       | Ensure build runs before publish                 |
| Dry run             | `npm pack --dry-run`                      | Preview package contents before publishing       |
| Provenance          | `--provenance` flag or trusted publishers | Cryptographic build attestation                  |
| Scoped publish      | `--access public`                         | Required for first publish of scoped packages    |

## Common Mistakes

| Mistake                                                  | Correct Pattern                                                        |
| -------------------------------------------------------- | ---------------------------------------------------------------------- |
| Putting `types` after `default` in exports               | `types` must be the first condition in every export block              |
| Missing `"./package.json"` in exports                    | Include `"./package.json": "./package.json"` for tooling compatibility |
| Different APIs for `import` vs `require`                 | Same API surface; write ESM source, transpile to CJS                   |
| Using `main` without `exports` for new packages          | Use `exports` as the primary entry point definition                    |
| Forgetting `"type": "module"` with `.js` ESM output      | Set `"type": "module"` or use `.mjs` extension explicitly              |
| Publishing `src/` or `node_modules/`                     | Use `"files"` allowlist to include only `dist/`                        |
| No `prepublishOnly` script                               | Add build step to prevent publishing stale artifacts                   |
| Using `default` export for libraries                     | Prefer named exports for consistent cross-tooling behavior             |
| Not testing with `npm pack` before publish               | Always dry-run to verify package contents and size                     |
| Omitting `peerDependencies` for framework plugins        | Declare shared runtime dependencies as peers                           |
| Publishing without provenance                            | Enable provenance for supply-chain transparency                        |
| Using `.d.ts` for CJS when package is `"type": "module"` | Use `.d.cts` for CJS type declarations, `.d.ts` or `.d.mts` for ESM    |

## Delegation

- **Build tooling setup**: Use `Explore` agent to examine tsup/unbuild/rollup configs
- **Type resolution debugging**: Use `Task` agent with "Are the Types Wrong?" (`attw`)
- **Publish pipeline review**: Delegate to `code-reviewer` agent

## References

- [Package.json configuration: exports, main, types, files, engines, peerDependencies](references/package-json-config.md)
- [Build scripts, prepublishOnly, npm pack, provenance, scoped packages](references/build-and-publish.md)
- [Dual ESM/CJS builds, conditional exports, type declarations](references/dual-format.md)
