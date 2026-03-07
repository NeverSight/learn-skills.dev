---
name: next-upgrade
version: 1.1.0
description: Structured workflow for upgrading Next.js applications across major versions. Use when migrating a Next.js project from one major version to another (e.g., 13 to 14, 14 to 15, 15 to 16). Covers codemod automation, breaking change detection, incremental migration paths, and post-upgrade validation.
license: MIT
category: Frameworks
tags:
  - nextjs
  - upgrade
  - migration
  - codemod
  - breaking-changes
agents:
  - nextjs-pro
  - developer
  - devops
tools:
  - Read
  - Write
  - Edit
  - Bash
invoked_by: "Skill({ skill: 'next-upgrade' })"
user_invocable: true
metadata:
  author: vercel-labs
  source: vercel-labs/next-skills
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Next.js Upgrade Workflow

Structured 9-step workflow for upgrading Next.js applications across major versions. Handles codemod automation, dependency updates, breaking change resolution, and validation.

## When to Apply

Use this skill when:

- Upgrading Next.js to a new major version (13, 14, 15, 16)
- Running codemods to automate breaking change migrations
- Resolving deprecation warnings in an existing Next.js project
- Planning an incremental migration path for large codebases
- Validating that an upgrade did not introduce regressions

## 9-Step Upgrade Workflow

### Step 1: Detect Current Version

Identify the current Next.js version and target version.

```bash
# Check current version
cat package.json | grep '"next"'

# Check Node.js version (Next.js 15+ requires Node 18.18+, Next.js 16 requires Node 20+)
node --version
```

**Version Requirements:**

| Next.js | Minimum Node.js | Minimum React |
| ------- | --------------- | ------------- |
| 13      | 16.14           | 18.2.0        |
| 14      | 18.17           | 18.2.0        |
| 15      | 18.18           | 19.0.0        |
| 16      | 20.0            | 19.0.0        |

### Step 2: Create Upgrade Branch

```bash
git checkout -b upgrade/nextjs-{target-version}
```

Always upgrade on a dedicated branch. Never upgrade on main directly.

### Step 3: Run Codemods

Use the official Next.js codemod CLI to automate breaking change migrations.

```bash
# Interactive mode (recommended) -- selects applicable codemods
npx @next/codemod@latest upgrade latest

# Or target a specific version
npx @next/codemod@latest upgrade 15
npx @next/codemod@latest upgrade 16
```

**Key Codemods by Version:**

#### Next.js 13 to 14

- `next-image-to-legacy-image` -- Renames `next/image` imports to `next/legacy/image`
- `next-image-experimental` -- Migrates from `next/legacy/image` to new `next/image`
- `metadata` -- Moves Head metadata to Metadata API exports

#### Next.js 14 to 15

- `next-async-request-apis` -- Converts synchronous dynamic APIs (`cookies()`, `headers()`, `params`, `searchParams`) to async
- `next-dynamic-ssr-false` -- Replaces `ssr: false` with `{ loading }` pattern for `next/dynamic`
- `next-og-import` -- Moves OG image generation imports to `next/og`

#### Next.js 15 to 16

- `next-use-cache` -- Converts `unstable_cache` to `'use cache'` directive
- `next-cache-life` -- Migrates cache revalidation to `cacheLife()` API
- `next-form` -- Wraps `<form>` elements with `next/form` where applicable

### Step 4: Update Dependencies

```bash
# Update Next.js and React together
npm install next@latest react@latest react-dom@latest

# For Next.js 15+, also update React types
npm install -D @types/react@latest @types/react-dom@latest

# Update eslint config
npm install -D eslint-config-next@latest
```

**Peer Dependency Conflicts:**

If you encounter peer dependency conflicts:

1. Check which packages require older React/Next versions
2. Update those packages first, or check for newer versions
3. Use `--legacy-peer-deps` only as a last resort (document why)

### Step 5: Update Configuration

Review and update `next.config.js` / `next.config.ts`:

```javascript
// next.config.ts (Next.js 15+ recommends TypeScript config)
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Next.js 15+: experimental features that graduated
  // Remove these from experimental:
  // - serverActions (now stable in 14+)
  // - appDir (now stable in 14+)
  // - ppr (now stable in 16+)

  // Next.js 16+: new cache configuration
  cacheComponents: true,  // Enable component-level caching
};

export default nextConfig;
```

**Configuration Changes by Version:**

| Version | Change                                                 |
| ------- | ------------------------------------------------------ |
| 14      | `appDir` removed from experimental (now default)       |
| 14      | `serverActions` removed from experimental (now stable) |
| 15      | `bundlePagesRouterDependencies` now default true       |
| 15      | `swcMinify` removed (now always enabled)               |
| 16      | `dynamicIO` replaces several caching behaviors         |
| 16      | `cacheComponents: true` enables component caching      |

### Step 6: Resolve Breaking Changes

After running codemods, manually resolve remaining breaking changes.

**Common Breaking Changes (15 to 16):**

1. **Async Request APIs**: `cookies()`, `headers()`, `params`, `searchParams` are now async

   ```typescript
   // Before (Next.js 14)
   export default function Page({ params }: { params: { id: string } }) {
     const { id } = params;
   }

   // After (Next.js 15+)
   export default async function Page({ params }: { params: Promise<{ id: string }> }) {
     const { id } = await params;
   }
   ```

2. **Caching Default Changed**: `fetch()` requests are no longer cached by default in Next.js 15+

   ```typescript
   // Before: cached by default
   fetch('https://api.example.com/data');

   // After: explicitly opt-in to caching
   fetch('https://api.example.com/data', { cache: 'force-cache' });
   // Or use 'use cache' directive in Next.js 16
   ```

3. **Route Handlers**: GET route handlers are no longer cached by default

   ```typescript
   // Next.js 15+: explicitly set caching
   export const dynamic = 'force-static';
   ```

### Step 7: Run Tests

```bash
# Run existing test suite
npm test

# Run build to catch compile-time errors
npm run build

# Run dev server and check key pages manually
npm run dev
```

**Validation Checklist:**

- [ ] Build completes without errors
- [ ] All existing tests pass
- [ ] Key user flows work in dev mode
- [ ] No console warnings about deprecated APIs
- [ ] Server-side rendering works correctly
- [ ] Client-side navigation works correctly
- [ ] API routes return expected responses
- [ ] Middleware functions correctly
- [ ] Static generation (SSG) pages build correctly

### Step 8: Update TypeScript Types

```bash
# Regenerate TypeScript declarations
npm run build

# Fix any new type errors
npx tsc --noEmit
```

**Common Type Fixes:**

- `PageProps` type changes (params/searchParams become Promise in 15+)
- `Metadata` type updates (new fields added)
- `NextRequest`/`NextResponse` API changes
- Route handler parameter types

### Step 9: Document and Commit

```bash
# Create detailed commit
git add -A
git commit -m "chore: upgrade Next.js from {old} to {new}

Breaking changes resolved:
- [list specific changes]

Codemods applied:
- [list codemods run]

Manual fixes:
- [list manual changes]"
```

## Incremental Upgrade Path

For large version jumps (e.g., 13 to 16), upgrade incrementally:

```
Next.js 13 -> 14 -> 15 -> 16
```

**Why incremental?**

- Codemods are version-specific and may not compose correctly across multiple versions
- Easier to debug issues when changes are smaller
- Each version has its own set of breaking changes to resolve
- Tests can validate each intermediate step

**For each version step:**

1. Run codemods for that version
2. Update deps
3. Fix breaking changes
4. Run tests
5. Commit checkpoint
6. Proceed to next version

## Troubleshooting

### Build fails after upgrade

1. Clear `.next` directory: `rm -rf .next`
2. Clear node_modules: `rm -rf node_modules && npm install`
3. Clear Next.js cache: `rm -rf .next/cache`

### Module not found errors

1. Check if package was renamed or merged
2. Update imports per migration guide
3. Check if package needs separate update

### Hydration mismatches after upgrade

1. Check for server/client rendering differences
2. Ensure dynamic imports use correct options
3. Verify date/locale handling is consistent

### Middleware issues

1. Middleware API changed in Next.js 13 (moved to root)
2. `NextResponse.rewrite()` behavior changed in 15
3. Check matcher configuration syntax

## Iron Laws

1. **ALWAYS** upgrade on a dedicated branch, never on main directly — upgrade branches can be rebased or reverted without disrupting production; direct main upgrades risk deploying half-migrated code.
2. **NEVER** skip intermediate versions in a multi-version jump — Next.js codemods are version-specific and do not compose correctly across major versions; skipping steps leaves un-migrated breaking changes.
3. **ALWAYS** run official codemods before making manual changes — codemods handle the bulk of mechanical migrations; manual-first approaches miss patterns and create divergence from the reference migration path.
4. **NEVER** use `--legacy-peer-deps` without documenting the specific conflict and resolution plan — suppressing peer errors hides version conflicts that will cause runtime failures.
5. **ALWAYS** validate with a full build plus test suite before merging — the dev server does not exercise SSG, edge runtime, or build optimizations that can fail silently post-upgrade.

## Anti-Patterns

| Anti-Pattern                                     | Why It Fails                                                                                  | Correct Approach                                                                        |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Upgrading on the main branch directly            | Half-migrated code can reach production; rollback requires a revert commit                    | Always create `upgrade/nextjs-{version}` branch; merge only after full validation       |
| Skipping intermediate versions                   | Version-specific codemods are not composable; skipped breaking changes cause runtime failures | Upgrade one major version at a time: 13→14→15→16; commit a checkpoint at each step      |
| Manual migration before running codemods         | Creates divergence from codemod output; codemods cannot merge cleanly with manual edits       | Run codemods first; apply manual fixes only for patterns codemods could not handle      |
| Using `--legacy-peer-deps` without documentation | Hidden version conflicts cause runtime failures not visible at install time                   | Resolve conflicts explicitly; use the flag only with a documented justification         |
| Validating only in dev mode                      | Dev server skips SSG, edge runtime, and build optimizations that can fail post-upgrade        | Run `npm run build` plus the full test suite; check SSR, SSG, and API routes explicitly |

## References

- [Next.js Upgrade Guide](https://nextjs.org/docs/app/building-your-application/upgrading)
- [Next.js Codemods](https://nextjs.org/docs/app/building-your-application/upgrading/codemods)
- [Next.js Changelog](https://github.com/vercel/next.js/releases)
