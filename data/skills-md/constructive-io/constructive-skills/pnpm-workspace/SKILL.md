---
name: pnpm-workspace
description: Create and manage PNPM workspaces following Constructive standards. Use when asked to "create a monorepo", "set up a workspace", "configure pnpm", or when starting a new TypeScript/JavaScript project with multiple packages.
compatibility: pnpm, Node.js 18+, lerna
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PNPM Workspaces (Constructive Standard)

Create and manage PNPM monorepo workspaces following Constructive conventions. This covers pure TypeScript/JavaScript workspaces (not pgpm workspaces for SQL modules).

## When to Apply

Use this skill when:
- Creating a new TypeScript/JavaScript monorepo
- Setting up a pnpm workspace structure
- Configuring lerna for versioning and publishing
- Managing internal package dependencies

## Workspace Structure

A Constructive-standard pnpm workspace:

```text
my-workspace/
├── .eslintrc.json
├── .gitignore
├── .prettierrc.json
├── lerna.json
├── package.json
├── packages/
│   ├── package-a/
│   │   ├── package.json
│   │   ├── src/
│   │   └── tsconfig.json
│   └── package-b/
│       ├── package.json
│       ├── src/
│       └── tsconfig.json
├── pnpm-lock.yaml
├── pnpm-workspace.yaml
└── tsconfig.json
```

## Core Configuration Files

### pnpm-workspace.yaml

Defines which directories contain packages:

```yaml
packages:
  - 'packages/*'
```

For larger projects with multiple package directories:

```yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - 'libs/*'
```

### Root package.json

```json
{
  "name": "my-workspace",
  "version": "0.0.1",
  "private": true,
  "repository": {
    "type": "git",
    "url": "https://github.com/org/my-workspace"
  },
  "license": "MIT",
  "publishConfig": {
    "access": "restricted"
  },
  "scripts": {
    "build": "pnpm -r run build",
    "clean": "pnpm -r run clean",
    "test": "pnpm -r run test",
    "lint": "pnpm -r run lint",
    "deps": "pnpm up -r -i -L"
  },
  "devDependencies": {
    "@types/jest": "^30.0.0",
    "@types/node": "^22.10.2",
    "@typescript-eslint/eslint-plugin": "^8.53.1",
    "@typescript-eslint/parser": "^8.53.1",
    "eslint": "^9.39.2",
    "eslint-config-prettier": "^10.1.8",
    "jest": "^30.2.0",
    "lerna": "^8.2.4",
    "prettier": "^3.8.0",
    "ts-jest": "^29.4.6",
    "ts-node": "^10.9.2",
    "typescript": "^5.6.3"
  }
}
```

**Key points:**
- Root package is `private: true` (never published)
- Scripts use `pnpm -r` to run recursively across packages
- `deps` script for interactive dependency updates

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

**Versioning modes:**
- `"version": "independent"` — Each package versioned separately (recommended for utility libraries)
- `"version": "0.0.1"` — Fixed versioning, all packages share same version (recommended for tightly coupled packages)

## Package Configuration

### Individual package.json

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
    "clean": "makage clean",
    "build": "makage build",
    "lint": "eslint . --fix",
    "test": "jest"
  },
  "devDependencies": {
    "makage": "0.1.10"
  }
}
```

**Key patterns:**
- `publishConfig.directory: "dist"` — Publish from dist folder (prevents tree-shaking into weird paths)
- `main` and `module` point to built files (not src)
- Uses makage for build tooling

## Internal Dependencies

Reference workspace packages using `workspace:*`:

```json
{
  "dependencies": {
    "my-other-package": "workspace:*"
  }
}
```

When published, `workspace:*` is replaced with the actual version number.

## Common Commands

| Command | Description |
|---------|-------------|
| `pnpm install` | Install all dependencies |
| `pnpm -r run build` | Build all packages |
| `pnpm -r run test` | Test all packages |
| `pnpm --filter <pkg> run build` | Build specific package |
| `pnpm up -r -i -L` | Interactive dependency update |
| `pnpm lerna version` | Version packages |
| `pnpm lerna publish` | Publish packages |

## Creating a New Package

```bash
# Create package directory
mkdir -p packages/my-new-package/src

# Initialize package.json
cd packages/my-new-package
pnpm init
```

Then configure package.json following the pattern above.

## TypeScript Configuration

### Root tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "declaration": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  }
}
```

### Package tsconfig.json

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

## PNPM vs PGPM Workspaces

| Aspect | PNPM Workspace | PGPM Workspace |
|--------|----------------|----------------|
| Purpose | TypeScript/JS packages | SQL database modules |
| Config | pnpm-workspace.yaml | pnpm-workspace.yaml + pgpm.json |
| Build | makage build | pgpm package |
| Output | dist/ folder | SQL bundles |
| Registry | npm | npm (for @pgpm/* packages) |

Some repos (like constructive) are **hybrid** — they have both pnpm packages and pgpm modules.

## Best Practices

1. **Keep root private**: Never publish the root package
2. **Use workspace protocol**: Always use `workspace:*` for internal deps
3. **Consistent structure**: All packages follow same directory layout
4. **Shared config**: Extend root tsconfig.json in packages
5. **Independent versioning**: Use for utility libraries with different release cycles
6. **Fixed versioning**: Use for tightly coupled packages that should release together

## References

- Related skill: `pnpm-publishing` for publishing workflow with makage
- Related skill: `pgpm-workspace` for SQL module workspaces
- Related skill: `pgpm-publishing` for publishing pgpm modules
