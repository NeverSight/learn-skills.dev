---
name: generate-barrels
description: "Generate barrel index.ts files for TypeScript projects. Use when user mentions: (1) barrel files, (2) index.ts exports, (3) re-export files, (4) simplify import paths, (5) create index files for directory, or (6) generate export aggregators."
---

# Generate Barrel Files

Generate barrel index.ts files for TypeScript directories to simplify imports.

> **Note**: Generation commands (`model gen`, `aptx functions`, `react-query`, `vue-query`) automatically update barrel files after generation. Use this command only for manual fixes or special cases.

## When to Use This Command

| Scenario | Action |
|----------|--------|
| Normal generation | Barrel files are auto-updated - no action needed |
| Fixing corrupted barrel files | Use this command |
| Processing non-standard directory structures | Use this command |
| One-time batch updates across multiple directories | Use this command |

## Prerequisites

```bash
pnpm add -D @aptx/frontend-tk-cli
```

## Usage

```bash
pnpm exec aptx-ft barrel gen -i <input-dir>
```

Alternative (without pnpm):

```bash
npx aptx-ft barrel gen -i ./src/functions
```

## Workflow

1. Ask user for target directory path
2. Show complete command and confirm with user
3. Execute and report results

### Common Directories

| Directory | Purpose |
|-----------|---------|
| `./src/functions` | Function modules |
| `./src/api` | API modules |
| `./src` | Entire source directory |

### Examples

```bash
# Generate for functions directory
pnpm exec aptx-ft barrel gen -i ./src/functions

# Generate for entire src directory
pnpm exec aptx-ft barrel gen -i ./src

# Generate for specific module
pnpm exec aptx-ft barrel gen -i ./src/api
```

## Output

Recursively scans directory and generates barrel files at **all levels**:

```
src/
├── index.ts                    # Exports functions, react-query, spec
├── functions/
│   ├── index.ts                # Exports application, assignment, ...
│   └── application/
│       └── index.ts            # Exports getXXX, setXXX, ...
├── react-query/
│   ├── index.ts                # Exports application, assignment, ...
│   └── application/
│       └── index.ts            # Exports *.query.ts, *.mutation.ts
└── spec/
    └── ...
```

## Boundaries

- Only generates index.ts barrel files, no other code
- Subdirectory index.ts files are overwritten
- Root index.ts is NOT overwritten if it exists with different content (protects manual entry files)
- Automatically skips `node_modules` and hidden directories (starting with `.`)
- Only processes `.ts` files, not `.tsx`, `.js`, etc.
