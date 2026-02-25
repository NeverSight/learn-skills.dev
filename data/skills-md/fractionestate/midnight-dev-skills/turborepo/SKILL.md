---
name: turborepo
description: >-
  High-performance monorepo build system with Turborepo. Use when configuring workspaces,
  optimizing build pipelines, setting up caching, or managing multi-package repositories. Triggers
  on Turborepo, monorepo, workspace, build caching, or pipeline questions.
metadata:
  author: FractionEstate
  version: '2.7.2'
---

# Turborepo

Turborepo is a high-performance build system for JavaScript/TypeScript monorepos. It provides
intelligent caching, parallel execution, and incremental builds.

## Core Concepts

### Monorepo Structure

```text
my-turborepo/
├── apps/
│   ├── web/              # Next.js app
│   │   ├── package.json
│   │   └── next.config.js
│   └── docs/             # Documentation site
│       └── package.json
├── packages/
│   ├── ui/               # Shared component library
│   │   ├── package.json
│   │   └── src/
│   ├── config/           # Shared configs (ESLint, TS, etc.)
│   │   └── package.json
│   └── utils/            # Shared utilities
│       └── package.json
├── turbo.json            # Turborepo configuration
├── package.json          # Root package.json
└── pnpm-workspace.yaml   # Workspace definition
```

### turbo.json Configuration

```json
{
  "$schema": "https://turborepo.com/schema.json",
  "ui": "stream",
  "envMode": "strict",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"],
      "env": ["NODE_ENV", "DATABASE_URL", "NEXT_PUBLIC_*"]
    },
    "dev": {
      "cache": false,
      "persistent": true,
      "interactive": true
    },
    "lint": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "test/**"],
      "outputs": ["coverage/**"]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "outputs": []
    }
  }
}
```

### Workspace Package.json

```json
{
  "name": "my-turborepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "typecheck": "turbo run typecheck",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.7.2"
  },
  "packageManager": "pnpm@10.26.0"
}
```

### pnpm-workspace.yaml

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

## Task Configuration

### Dependency Types

```json
{
  "tasks": {
    // Topological dependency (dependencies first)
    "build": {
      "dependsOn": ["^build"] // Run build in all dependencies first
    },

    // Same-package dependency
    "test": {
      "dependsOn": ["build"] // Run build in same package first
    },

    // Cross-package specific dependency
    "deploy": {
      "dependsOn": ["build", "test", "^build"]
    },

    // Arbitrary package#task dependency
    "e2e": {
      "dependsOn": ["web#build", "api#build"] // Specific packages
    }
  }
}
```

### Input/Output Configuration

```json
{
  "tasks": {
    "build": {
      // Files that affect cache
      "inputs": [
        "$TURBO_DEFAULT$", // Default: all non-gitignored files
        "!README.md", // Exclude README changes
        ".env.production", // Include specific env file
        "$TURBO_ROOT$/tsconfig.json" // Reference files from repo root
      ],
      // Files produced by task
      "outputs": [
        "dist/**",
        ".next/**",
        "!.next/cache/**" // Exclude .next/cache
      ]
    }
  }
}
```

**Note:** The following files are always considered inputs and cannot be ignored:

- `package.json`
- `turbo.json`
- Package manager lockfiles (automatically included in global hash)

### Environment Variables

```json
{
  "globalEnv": ["CI", "VERCEL"],
  "globalPassThroughEnv": ["AWS_ACCESS_KEY"],
  "tasks": {
    "build": {
      "env": [
        "DATABASE_URL",
        "NEXT_PUBLIC_*", // Wildcard: all vars starting with NEXT_PUBLIC_
        "!GITHUB_*" // Negation: exclude GITHUB_ vars from strict mode
      ],
      "passThroughEnv": ["AWS_SECRET_KEY"] // Available but not in cache hash
    }
  }
}
```

## Caching

### Local Caching

```bash
# Cache stored in node_modules/.cache/turbo
turbo run build

# Force cache miss
turbo run build --force
```

### Remote Caching

```bash
# Login to Vercel Remote Cache
npx turbo login

# Link project
npx turbo link

# Or use custom cache server
TURBO_API="https://cache.example.com"
TURBO_TOKEN="your-token"
TURBO_TEAM="your-team"
```

### Cache Configuration

```json
{
  "tasks": {
    "build": {
      "cache": true, // Enable caching (default)
      "outputLogs": "new-only" // Show logs only on cache miss
    },
    "dev": {
      "cache": false, // Disable caching for dev
      "persistent": true, // Long-running task
      "interactive": true // Accepts keyboard input (stdin)
    },
    "db:studio": {
      "cache": false,
      "persistent": true,
      "interruptible": true // Can be restarted when dependencies change
    }
  }
}
```

## Development Mode

### turbo watch

Re-run tasks automatically when files change:

```bash
# Watch all tasks
turbo watch build lint typecheck

# Watch specific packages
turbo watch build --filter=web

# Write cache in watch mode (experimental)
turbo watch build --experimental-write-cache
```

Watch mode is dependency-aware - when a package changes, all dependent packages re-run their tasks.
Persistent tasks (dev servers) are automatically handled.

## Docker Optimization

### turbo prune

Generate a partial monorepo for efficient Docker builds:

```bash
# Basic prune
turbo prune web

# Docker-optimized output (recommended)
turbo prune web --docker
```

The `--docker` flag creates:

- `out/json/` - package.json files only (for dependency layer)
- `out/full/` - Complete pruned workspace (for build layer)

### Dockerfile Pattern

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app

# Install turbo globally
RUN npm install -g turbo

# Copy all files and prune
COPY . .
RUN turbo prune web --docker

# Install dependencies (cached layer)
FROM node:22-alpine AS installer
WORKDIR /app
COPY --from=builder /app/out/json/ .
RUN npm install

# Build the app
COPY --from=builder /app/out/full/ .
RUN npx turbo run build --filter=web

# Production image
FROM node:22-alpine AS runner
WORKDIR /app
COPY --from=installer /app/apps/web/.next/standalone ./
COPY --from=installer /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=installer /app/apps/web/public ./apps/web/public

CMD ["node", "apps/web/server.js"]
```

## Filtering

### Package Filters

```bash
# Run build only in web app
turbo run build --filter=web

# Run in web and its dependencies
turbo run build --filter=web...

# Run in packages that depend on ui
turbo run build --filter=...^ui

# Target specific task in specific package
turbo run web#lint
```

### Source Control Filters

```bash
# Packages changed since main branch
turbo run build --filter=[main...my-feature]

# Packages changed since previous commit
turbo run build --filter=[HEAD^1]

# Packages changed between specific commits
turbo run build --filter=[a1b2c3d...e4f5g6h]

# Build all packages depending on changes in branch
turbo run build --filter=...[origin/my-feature]

# Combine package and source control filters
turbo run build --filter=@acme/ui...[HEAD^1]
turbo run test --filter=@acme/*{./packages/*}[HEAD^1]
```

### Affected Flag (CI Optimized)

```bash
# Run only on packages with code changes (auto-detects CI environment)
turbo run build --affected

# Override comparison branches via environment
TURBO_SCM_BASE=main TURBO_SCM_HEAD=HEAD turbo run build --affected
```

### Workspace Filters

```bash
# All apps
turbo run build --filter="./apps/*"

# All packages
turbo run build --filter="./packages/*"

# Exclude specific package
turbo run build --filter=./apps/* --filter=!./apps/admin

# Multiple specific packages
turbo run build --filter=docs --filter=web
```

## Package Configuration

### Internal Package (packages/ui/package.json)

```json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "exports": {
    ".": "./src/index.tsx",
    "./button": "./src/button.tsx",
    "./card": "./src/card.tsx"
  },
  "scripts": {
    "build": "tsup",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "@repo/config": "workspace:*",
    "typescript": "^5.0.0"
  }
}
```

### App Package (apps/web/package.json)

```json
{
  "name": "web",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "next build",
    "dev": "next dev",
    "lint": "next lint",
    "start": "next start"
  },
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/utils": "workspace:*",
    "next": "^16.1.1",
    "react": "^19.0.0"
  }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Full history for --affected flag

      - uses: pnpm/action-setup@v4
        with:
          version: 10

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Option 1: Run all tasks with remote caching
      - run: pnpm turbo run build lint test
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}

      # Option 2: Run only affected packages (optimized for large repos)
      - run: pnpm turbo run build lint test --affected
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

## Best Practices

1. **Keep packages focused** - Single responsibility
2. **Use workspace protocol** - `workspace:*` for internal deps
3. **Share configs** - Put ESLint, TS config in packages/config
4. **Cache aggressively** - Remote caching for CI
5. **Filter in CI** - Only build what changed

## References

- [references/configuration.md](references/configuration.md) - Full config reference
- [references/filters.md](references/filters.md) - Filter patterns
