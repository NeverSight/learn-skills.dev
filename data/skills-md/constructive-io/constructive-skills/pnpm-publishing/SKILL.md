---
name: pnpm-publishing
description: Publish TypeScript packages using makage and lerna following Constructive standards. Use when asked to "publish a package", "release to npm", "build for publishing", or when preparing packages for npm distribution.
compatibility: pnpm, makage, lerna, Node.js 18+
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Publishing TypeScript Packages (Constructive Standard)

Publish TypeScript packages to npm using makage for builds and lerna for versioning. This covers the dist-folder publishing pattern that prevents tree-shaking into weird import paths.

## When to Apply

Use this skill when:
- Building TypeScript packages for npm publishing
- Configuring makage for package builds
- Running lerna version and publish workflows
- Setting up the dist-folder publishing pattern

## Why Dist-Folder Publishing?

Constructive publishes from the `dist/` folder to:
- Prevent consumers from importing internal paths (`my-pkg/src/internal`)
- Ensure clean package structure on npm
- Keep source files out of published package
- Maintain consistent import paths

## Anti-Pattern: ESM-Only with Exports Map

**NEVER use the `exports` map pattern:**

```json
{
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./api": {
      "import": "./dist/api/index.js",
      "types": "./dist/api/index.d.ts"
    }
  }
}
```

**Problems with this approach:**
- Breaks CommonJS consumers
- Exposes `dist/` in import paths
- Incompatible with the dist-folder publishing pattern
- Creates inconsistent import paths between development and published package

**Instead, use the Constructive standard pattern shown below.**

## Deep Nested Imports (Recommended for Tree-Shaking)

Deep nested imports via file path are **fully supported and recommended** for tree-shaking. With dist-folder publishing, the `dist/` folder becomes the package root, so consumers can import directly from subdirectories:

```typescript
// These imports work correctly with dist-folder publishing:
import { OrmClient } from '@my-org/sdk/api';
import { AdminClient } from '@my-org/sdk/admin';
import { AuthClient } from '@my-org/sdk/auth';
```

This works because the published package structure looks like:

```text
@my-org/sdk (on npm)
├── index.js           # Main entry point
├── api/
│   └── index.js       # API-specific code
├── admin/
│   └── index.js       # Admin-specific code
└── auth/
    └── index.js       # Auth-specific code
```

**Benefits of this approach:**
- Full tree-shaking support (only import what you need)
- Works with both CommonJS and ESM
- No `exports` map needed
- Clean import paths without `dist/`

**Source structure for nested imports:**

```text
my-package/
├── src/
│   ├── index.ts       # Re-exports or shared code
│   ├── api/
│   │   └── index.ts   # API module
│   ├── admin/
│   │   └── index.ts   # Admin module
│   └── auth/
│       └── index.ts   # Auth module
└── package.json
```

After `makage build`, the `dist/` folder mirrors this structure and becomes the published package root.

## Anti-Pattern: Manual Build Scripts Without Makage

**NEVER use manual build scripts like this:**

```json
{
  "scripts": {
    "clean": "rimraf dist/**",
    "copy": "copyfiles -f ../../LICENSE package.json dist",
    "build": "npm run clean; tsc -p tsconfig.json; tsc -p tsconfig.esm.json; npm run copy"
  },
  "devDependencies": {
    "copyfiles": "^2.4.1",
    "rimraf": "^6.0.1"
  }
}
```

**Problems with this approach:**
- Reinvents what makage already does
- Requires multiple devDependencies (copyfiles, rimraf) instead of one (makage)
- Manual tsconfig management for CJS/ESM builds
- Inconsistent build behavior across packages
- Missing features like automatic source map handling

**Instead, use makage which handles all of this automatically.**

## Makage Overview

[makage](https://www.npmjs.com/package/makage) is a tiny build helper that replaces cpy, rimraf, and other build tools:

| Command | Description |
|---------|-------------|
| `makage build` | Clean, compile TypeScript, copy assets |
| `makage build --dev` | Build with source maps |
| `makage clean` | Remove dist folder |
| `makage assets` | Copy LICENSE, README, package.json to dist |

## Package Configuration

### package.json

```json
{
  "name": "my-package",
  "version": "0.1.0",
  "description": "Package description",
  "author": "Constructive <developers@constructive.io>",
  "main": "index.js",
  "module": "esm/index.js",
  "types": "index.d.ts",
  "homepage": "https://github.com/org/my-workspace",
  "license": "MIT",
  "publishConfig": {
    "access": "public",
    "directory": "dist"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/org/my-workspace"
  },
  "scripts": {
    "copy": "makage assets",
    "clean": "makage clean",
    "prepublishOnly": "npm run build",
    "build": "makage build",
    "lint": "eslint . --fix",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "devDependencies": {
    "makage": "0.1.10"
  }
}
```

**Critical fields:**
- `publishConfig.directory: "dist"` — Publish from dist folder
- `main: "index.js"` — Points to CJS build (in dist)
- `module: "esm/index.js"` — Points to ESM build (in dist)
- `types: "index.d.ts"` — Points to type declarations (in dist)

## Build Output Structure

After `makage build`:

```text
my-package/
├── src/
│   └── index.ts
├── dist/
│   ├── index.js          # CJS build
│   ├── index.d.ts        # Type declarations
│   ├── esm/
│   │   └── index.js      # ESM build
│   ├── package.json      # Copied from root
│   ├── README.md         # Copied from root
│   └── LICENSE           # Copied from root
└── package.json
```

The `dist/` folder is what gets published to npm.

## Build Workflow

### Development Build

```bash
# Build with source maps for debugging
makage build --dev
```

### Production Build

```bash
# Full build: clean, compile, copy assets
makage build
```

### Clean

```bash
# Remove dist folder
makage clean
```

## Publishing Workflow

### 1. Prepare

```bash
# Install dependencies
pnpm install

# Build all packages
pnpm -r run build

# Run tests
pnpm -r run test

# Run linting
pnpm -r run lint
```

### 2. Version

```bash
# Interactive versioning (independent mode)
pnpm lerna version

# Or with conventional commits
pnpm lerna version --conventional-commits
```

### 3. Publish

```bash
# Publish to npm
pnpm lerna publish from-package
```

**Note:** Use `from-package` to publish packages that have been versioned but not yet published.

### One-Liner

```bash
pnpm install && pnpm -r run build && pnpm -r run test && pnpm lerna version && pnpm lerna publish from-package
```

## Dry Run Commands

Test without making changes:

```bash
# Test versioning (no git operations)
pnpm lerna version --no-git-tag-version --no-push

# Test publishing
pnpm lerna publish from-package --dry-run
```

## Lerna Configuration

### lerna.json

```json
{
  "$schema": "node_modules/lerna/schemas/lerna-schema.json",
  "version": "independent",
  "npmClient": "pnpm",
  "registry": "https://registry.npmjs.org",
  "command": {
    "create": {
      "homepage": "https://github.com/org/my-workspace",
      "license": "MIT",
      "access": "restricted"
    },
    "publish": {
      "allowBranch": "main",
      "message": "chore(release): publish",
      "conventionalCommits": true
    }
  }
}
```

## Access Control

### Public Packages

```json
{
  "publishConfig": {
    "access": "public",
    "directory": "dist"
  }
}
```

### Private/Scoped Packages

```json
{
  "publishConfig": {
    "access": "restricted",
    "directory": "dist"
  }
}
```

## TypeScript Configuration

### tsconfig.json (package level)

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true
  },
  "include": ["src/**/*"]
}
```

### ESM Build

makage handles dual CJS/ESM builds automatically. The ESM output goes to `dist/esm/`.

## Workspace Dependencies

When publishing, `workspace:*` references are converted to actual versions:

**Before publish (package.json):**
```json
{
  "dependencies": {
    "my-other-package": "workspace:*"
  }
}
```

**After publish (in dist/package.json):**
```json
{
  "dependencies": {
    "my-other-package": "^0.5.0"
  }
}
```

## Common Issues

### Package Not Found After Publish

Ensure `publishConfig.directory` is set to `"dist"`.

### Types Not Found

Ensure `types` field points to declaration file in dist:
```json
{
  "types": "index.d.ts"
}
```

### ESM Import Errors

Ensure `module` field points to ESM build:
```json
{
  "module": "esm/index.js"
}
```

## Best Practices

1. **Always build before publish**: Use `prepublishOnly` script
2. **Test the build**: Run tests against built output
3. **Use dry-run first**: Test versioning and publishing before committing
4. **Keep dist clean**: Run `makage clean` before builds
5. **Conventional commits**: Enable for automatic changelogs

## References

- Related skill: `pnpm-workspace` for workspace setup
- Related skill: `pgpm-publishing` for SQL module publishing
- [makage on npm](https://www.npmjs.com/package/makage)
