---
name: frontend-init
description: Initialize frontend projects with opinionated modern toolchain - Bun (package manager), Oxfmt (formatter), Oxlint (linter), tsdown (npm bundler), tsgo (type checker). Use when creating new frontend/TypeScript projects, setting up project tooling, or mentions "init project", "new frontend", "setup tooling".
---

# Frontend Project Initialization

Opinionated setup using fast, Rust/Go-based tools.

| Tool       | Purpose                  | Replaces      |
| ---------- | ------------------------ | ------------- |
| **Bun**    | Package manager, runtime | npm/yarn/pnpm |
| **Oxfmt**  | Formatter                | Prettier      |
| **Oxlint** | Linter                   | ESLint        |
| **tsdown** | Library bundler          | tsup, rollup  |
| **tsgo**   | Type checker             | tsc           |

## Quick Start

```bash
# 1. Initialize
bun init my-project
cd my-project

# 2. Add tools (choose based on project type)
bun add -d oxlint oxfmt                              # app
bun add -d oxlint oxfmt tsdown @typescript/native-preview  # library

# 3. Configure oxlint
bunx oxlint --init
```

Add scripts to `package.json`:

```json
{
  "scripts": {
    "lint": "oxlint src",
    "lint:fix": "oxlint src --fix",
    "format": "oxfmt src",
    "format:check": "oxfmt src --check",
    "typecheck": "tsgo"
  }
}
```

## Project Types

### Application

```json
{
  "name": "my-app",
  "type": "module",
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "start": "bun run src/index.ts",
    "lint": "oxlint src",
    "format": "oxfmt src",
    "typecheck": "tsgo"
  }
}
```

### Library (npm package)

```bash
bun add -d tsdown @typescript/native-preview
```

```json
{
  "name": "my-lib",
  "version": "0.0.1",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist"],
  "scripts": {
    "dev": "tsdown --watch",
    "build": "tsdown",
    "prepublishOnly": "bun run build"
  }
}
```

**tsdown.config.ts**:

```typescript
import { defineConfig } from "tsdown";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["esm", "cjs"],
  dts: true,
  clean: true,
});
```

### React

```bash
bun init my-react-app --template react
```

Add to `.oxlintrc.json`:

```json
{
  "plugins": ["react", "react-hooks"],
  "rules": {
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn"
  }
}
```

## Configuration

### .oxlintrc.json

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["typescript", "unicorn", "import"],
  "rules": {
    "eqeqeq": "warn",
    "no-console": "warn",
    "import/no-cycle": "error"
  },
  "overrides": [
    {
      "files": ["*.test.ts", "*.spec.ts"],
      "rules": { "no-console": "off" }
    }
  ]
}
```

### .oxfmtrc.json (optional)

Defaults work well. Custom if needed:

```json
{
  "printWidth": 100,
  "semi": false,
  "singleQuote": true
}
```

### tsconfig.json

Bun generates this. Ensure tsgo compatibility:

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true
  },
  "include": ["src"]
}
```

### .gitignore

```
node_modules/
dist/
*.log
.DS_Store
```

## Editor Setup (VS Code / Cursor)

**.vscode/settings.json**:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "oxc.oxc-vscode"
}
```

**.vscode/extensions.json**:

```json
{
  "recommendations": ["oxc.oxc-vscode", "oven.bun-vscode"]
}
```

## CI/CD

**.github/workflows/ci.yml**:

```yaml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun run lint
      - run: bun run format:check
      - run: bun run typecheck
      - run: bun run build # library only
```

## Notes

**Tool maturity**: Bun, Oxlint, tsdown are stable. Oxfmt is alpha. tsgo is preview.

**Migration from existing project**:

1. Delete `node_modules`, lockfiles
2. `bun install`
3. `bun add -d oxlint oxfmt`
4. Remove eslint/prettier configs
5. Update scripts
