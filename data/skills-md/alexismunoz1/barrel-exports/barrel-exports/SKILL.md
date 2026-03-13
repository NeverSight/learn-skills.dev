---
name: barrel-exports
description: >
  Analyzes and migrates barrel export patterns in TypeScript/React projects to
  reduce bundle size. Detects barrel files (index.ts re-exports), checks for
  side effects, measures bundle impact, and safely rewrites imports to direct
  paths. Proven to reduce page chunks by up to 19x in Next.js apps.
  Use when user mentions "analyze barrels", "check barrel exports",
  "migrate barrels", "fix barrel exports", "bundle size too big",
  "tree-shaking not working", "index.ts re-exports", or "optimize imports".
  Do NOT use for general import/export questions or ESM/CJS migration.
compatibility: Claude Code
license: MIT
metadata:
  author: alexismunoz1
  version: 1.0.0
---

# Barrel Exports Analyzer & Migrator

Detects barrel export anti-patterns and safely migrates to direct imports. Every recommendation is backed by real experiment data: barrel imports produced a **224 KB page chunk** vs **11.7 KB with direct imports** — a 19x difference in a controlled Next.js monorepo test.

## How It Works

This skill operates in two phases:

1. **Analysis** — Find barrel files, detect side effects, check bundler config, measure bundle impact
2. **Migration** — Rewrite imports file-by-file with user confirmation, update config, verify with before/after metrics

You can run analysis alone (read-only, always safe) or follow up with migration.

## Phase 1: Analysis

When the user asks to analyze barrels, check barrel exports, or investigate bundle size, follow these four steps.

### Step 1: Find Barrel Files

Search for `index.ts` and `index.tsx` files that primarily re-export from other modules:

```bash
# Find all index files
find src/ -name "index.ts" -o -name "index.tsx" | head -50
```

For each file found, read it and classify:

- **Pure barrel** — contains ONLY `export * from` or `export { X } from` statements
- **Mixed barrel** — has re-exports AND original code (types, constants, logic)
- **Entry point** — has original code, not primarily re-exports
- **Side-effect barrel** — has re-exports AND side effects (console.log, global mutations, event listeners)

> For the complete classification algorithm and side-effect taxonomy, see `references/analysis-guide.md`

### Step 2: Check Configuration

Inspect the project's bundler and package configuration:

**package.json:**
- Check for `"exports"` field — subpath exports enable direct imports
- Check for `"type": "module"` — ESM enables better tree-shaking

**next.config.js/ts** (if Next.js):
- Check `experimental.optimizePackageImports` — Next.js's built-in barrel optimization
- Check `transpilePackages` — required for monorepo internal packages

**tsconfig.json:**
- Check `"moduleResolution"` — must be `"bundler"` or `"node16"` for subpath exports

### Step 3: Measure Bundle (Next.js)

If the project uses Next.js, measure the current bundle:

```bash
npx next build 2>&1
```

Parse the route table from build output. Look for the `First Load JS` column — this is the total JS sent to the browser for each route. Record the baseline values.

Key metrics to capture:
- First Load JS for each route
- Shared chunk size (listed under `+ First Load JS shared by all`)
- Individual page chunk sizes

### Step 4: Report Findings

Present findings in this format:

```
## Barrel Export Analysis

### Barrel Files Found: N

| File | Type | Exports | Side Effects | Risk |
|------|------|---------|-------------|------|
| src/index.ts | Pure barrel | 45 | None | High |
| src/components/index.ts | Pure barrel | 20 | None | Medium |
| src/utils/index.ts | Mixed | 12 | console.log | Critical |

### Configuration Issues

- ⚠️ No subpath exports configured
- ✅ `transpilePackages` includes internal packages

### Bundle Impact (if measured)

- Current First Load JS: 155 kB
- Estimated savings: 30-50% (based on barrel depth and export count)

### Recommendations

1. [Specific actions based on findings]
```

Risk levels:
- **Critical** — barrel with side effects, bundler cannot tree-shake
- **High** — barrel re-exporting 20+ modules, high import fan-out
- **Medium** — barrel with 5-20 re-exports
- **Low** — barrel with <5 re-exports or already optimized via config

## Phase 2: Migration

When the user asks to migrate barrels, fix barrel exports, or optimize imports, follow these six steps. **Always run Phase 1 first** if analysis hasn't been done.

### Step 1: Establish Baseline

If working with Next.js, run a build and record baseline metrics before any changes:

```bash
npx next build 2>&1
```

Save the First Load JS values for comparison after migration.

### Step 2: Find Consumers

For each barrel file identified in analysis, find all files that import from it:

```bash
# Find all imports from a barrel path
grep -rn "from ['\"]@repo/ui['\"]" src/ --include="*.ts" --include="*.tsx"
grep -rn "from ['\"]./components['\"]" src/ --include="*.ts" --include="*.tsx"
```

Build a mapping: `{ consumer_file → [imported_names] → barrel_path → direct_path }`.

### Step 3: Verify Direct Paths Exist

Before rewriting any imports, verify that each target module file exists:

```
@repo/ui → @repo/ui/components/Button  →  packages/ui/src/components/Button.tsx ✓
@repo/ui → @repo/ui/hooks/useDebounce  →  packages/ui/src/hooks/useDebounce.ts  ✓
```

If subpath exports are configured in the package's `package.json`, use those paths. Otherwise, use relative paths.

### Step 4: Apply Changes (With Confirmation)

**CRITICAL: Never auto-apply all changes. Process file by file.**

For each consumer file, show the user the proposed change:

```
File: src/app/page.tsx

BEFORE:
import { Button, Card, Badge, IconHome, useDebounce, formatDate, cn } from "@repo/ui";

AFTER:
import { Button } from "@repo/ui/components/Button";
import { Card } from "@repo/ui/components/Card";
import { Badge } from "@repo/ui/components/Badge";
import { IconHome } from "@repo/ui/icons/IconHome";
import { useDebounce } from "@repo/ui/hooks/useDebounce";
import { formatDate } from "@repo/ui/utils/formatDate";
import { cn } from "@repo/ui/utils/cn";
```

Wait for user confirmation before applying each file. Group related files if the user prefers batch mode.

> For detailed transformation rules covering type imports, namespace imports, re-exports, and edge cases, see `references/migration-guide.md`

### Step 5: Update Configuration

After import migration, update configuration:

**package.json** (of the library being imported):
```json
{
  "exports": {
    ".": "./src/index.ts",
    "./components/*": "./src/components/*.tsx",
    "./hooks/*": "./src/hooks/*.ts",
    "./utils/*": "./src/utils/*.ts"
  }
}
```

**next.config.js** (if Next.js, for external packages):
```js
experimental: {
  optimizePackageImports: ["@repo/ui"]
}
```

### Step 6: Post-Migration Verification

Run the build again and compare:

```
## Migration Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| First Load JS (/) | 155 kB | 106 kB | -31.6% |
| Page chunk (/) | 224 kB | 11.7 kB | -94.8% |
```

Verify:
- All routes build without errors
- No runtime errors (if dev server available)
- TypeScript compilation passes: `npx tsc --noEmit`
- Bundle size decreased or stayed the same

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Type-only imports (`import type { X }`) | Keep or convert to direct — types are erased at build, low impact |
| Dynamic imports (`import("./barrel")`) | Flag as high-risk — dynamic imports pull the entire barrel at runtime |
| Side-effect imports (`import "./init"`) | Never remove — these run code on import, flag for manual review |
| Circular dependencies | Detect and warn — migration may expose hidden circular deps |
| External packages (lodash, etc.) | Use `optimizePackageImports` instead of rewriting — don't modify node_modules |
| Monorepo internal packages | Prefer subpath exports in package.json `exports` field |
| CSS/asset imports in barrels | Preserve as-is — these are side-effect imports |
| Default exports | Use `import X from "./path"` not `import { default as X }` |

## Guidelines

- **Never auto-apply changes** — always show the diff and get confirmation
- **Preserve type imports** — `import type` has zero runtime cost, migration is optional
- **Handle external packages differently** — use `optimizePackageImports` for third-party, rewrite for internal
- **Always measure** — run builds before AND after to prove impact with numbers
- **One file at a time** — process consumer files individually unless user requests batch mode
- **Keep barrel files initially** — don't delete index.ts until all consumers are migrated
- **Check for side effects first** — if a barrel has side effects, migration requires more care

## Usage Examples

### "My Next.js app bundle is too big"

1. Run analysis to find barrel files and measure current bundle
2. Identify the highest-impact barrels (most re-exports, most consumers)
3. Show expected savings based on experiment data
4. Offer to migrate the top offenders first

### "Check if my project has barrel export problems"

1. Run Phase 1 analysis only
2. Report all barrel files with risk levels
3. Check configuration for missing optimizations
4. Provide specific recommendations without making changes

### "Migrate all my barrel imports to direct imports"

1. Run Phase 1 if not already done
2. Establish build baseline
3. Process each consumer file with confirmation
4. Update package.json exports
5. Run post-migration build and show before/after comparison

## Reference Materials

- `references/analysis-guide.md` — Detection methodology, side-effect taxonomy, and reporting format
- `references/migration-guide.md` — Import transformation rules, edge cases, and rollback procedures
- `references/barrel-patterns.md` — 7 anti-patterns catalog with experiment data and decision matrix
