---
name: migrate
description: "Use when bulk-migrating import paths, renaming workspace packages, or reorganizing modules across many files in a monorepo. Uses scripted bulk operations with verification gates and atomic commits. Keywords: migrate imports, rename package, bulk import path change, module reorganization, monorepo refactor."
---

# Migrate

Orchestrates monorepo migrations: import path changes, package renames, module moves. Uses scripted bulk operations (never file-by-file edits), deduplicates against existing work, verifies types at each step, and commits atomically.

Do NOT load this skill when the change only touches one or two files, the user wants exploratory refactoring, or the package boundary decision is still unresolved.

## NEVER

- Never use the Edit tool file-by-file for bulk migrations — use `grep | xargs sed` instead (10x faster, no missed files).
- Never start without a deduplication check — duplicate migrations cause import conflicts that are hard to debug.
- Never commit without typecheck — silent import breakage is worse than a failed commit.
- Never skip the residual check — 2 files left pointing to the old path cause subtle runtime errors.
- Never migrate without a manifest — you must know the blast radius before touching anything.
- Never run bulk sed without confirming the manifest count with the user if > 20 files or if `packages/` is touched.

## Decision Tree

```
Does the new import path already exist in the codebase?
├── Yes (many files) → Already migrated; verify or skip
├── Yes (some files) → Partial migration; check what's left
└── No → Proceed with full migration

How many files are affected?
├── 1-2 files → Don't use this skill; use Edit tool directly
├── 3-20 files → Proceed with manifest + scripted sed
└── > 20 files → Show manifest, get user confirmation before sed

Does the change touch packages/ (shared across workspaces)?
├── Yes → Get user confirmation before running sed
└── No → Proceed
```

## Scripts

```bash
bash scripts/build-manifest.sh @old/pkg/name
bash scripts/replace-imports.sh @old/pkg/name @new/pkg/name /tmp/migration-manifest.txt
```

## Pipeline

### Step 1: Deduplication Check

```bash
git log --oneline -20
grep -r "<new-import-path>" apps/ packages/ --include="*.ts" --include="*.svelte" -l | head -10
```

If migration is already complete or partial: report what exists, ask whether to verify/clean up or skip.

### Step 2: Build Migration Manifest

```bash
grep -rl "<old-import-path>" apps/ packages/ --include="*.ts" --include="*.tsx" --include="*.svelte" > /tmp/migration-manifest.txt
echo "Files to migrate: $(wc -l < /tmp/migration-manifest.txt)"
cat /tmp/migration-manifest.txt
```

Print summary grouped by workspace. Ask user to confirm before proceeding if > 20 files or `packages/` is affected.

### Step 3: Scripted Bulk Replacement

```bash
grep -rl "@old/pkg" apps/api/ --include="*.ts" | \
  xargs sed -i '' "s|@old/pkg|@new/pkg|g"

grep -rl "@old/pkg" apps/frontend/ --include="*.ts" --include="*.svelte" | \
  xargs sed -i '' "s|@old/pkg|@new/pkg|g"
```

**macOS note:** `sed -i ''` (empty string required for in-place edit without backup). Linux uses `sed -i` without the empty string.

### Step 4: Verification Gate

```bash
cd apps/api && npx tsc --noEmit 2>&1 | head -30
cd apps/frontend && npx svelte-check --threshold error 2>&1 | tail -20
cd packages/server && npx tsc --noEmit 2>&1 | head -20
```

Common causes of type errors after migration:
- Import path changed but exported symbol name also differs → check the actual export
- Package not yet built → `pnpm --filter @portal/server build`
- Circular dependency introduced → `pnpm run check:circular`

### Step 5: Residual Check

```bash
grep -r "<old-import-path>" apps/ packages/ --include="*.ts" --include="*.svelte" -l
```

Remaining occurrences may be in:
- Dynamically constructed import strings → manual inspection required
- Test fixture data (strings, not imports) → may be intentional
- Comments or docs → update if they describe the API

### Step 6: Run Tests

```bash
npx vitest run apps/api --reporter=dot
npx vitest run apps/frontend --reporter=dot
```

If tests fail: check if mock paths still point to the old module path (common missed case in test files).

### Step 7: Atomic Commit

```bash
git commit -m "refactor(imports): migrate @old/pkg → @new/pkg

Affects N files across apps/api, apps/frontend, packages/server.
All typechecks pass. Full test suite green.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

Stage only migrated files — never `git add -A`.

## Common Migration Patterns

| Pattern | From | To |
|---------|------|----|
| Package rename | `@company/old-pkg` | `@company/new-pkg` |
| Path restructure | `@app/shared/utils` | `@app/core/utils` |
| Index consolidation | `./auth/helpers` | `./auth/index` |
| Framework alias | `$lib/server/*` | `src/lib/server/*` |

## Arguments

- `$ARGUMENTS`: Migration description
  - `"@old/pkg/utils → @new/pkg/utils"` — import path migration
  - `"move packages/server/src/auth.ts to packages/server/src/auth/index.ts"` — file move
  - `"rename @company/old-shared → @company/core"` — package rename
  - If empty: ask for source and target
