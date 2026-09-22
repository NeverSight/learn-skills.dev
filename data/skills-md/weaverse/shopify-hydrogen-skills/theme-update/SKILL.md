---
name: theme-update
description: "Safely update a Weaverse Pilot theme to the latest version — detects current version, fetches release diffs, plans changes category-by-category, preserves customizations, verifies build."
---

# Theme Update — Weaverse Pilot

Safely upgrade a Weaverse Pilot theme from its current version to a newer release. This skill walks through detection, planning, execution, and verification — never overwriting user customizations without explicit approval.

## Source

- Theme repo: https://github.com/Weaverse/pilot
- Releases: https://github.com/Weaverse/pilot/releases
- Package name: `@weaverse/pilot`
- Versioning: `YYYY.M.D` (e.g., `2026.4.7`). Older: semver (`v8.1.0`)

## Quick Check

```bash
node skills/theme-update/scripts/check_pilot_updates.mjs
node skills/theme-update/scripts/check_pilot_updates.mjs --target v2026.4.7
```

---

## Procedure

Follow these phases in order. Do NOT skip steps.

### Phase 1 — Detection

1. Read `package.json` → get `version` field
2. If `name` is not `@weaverse/pilot`, ask the user to confirm this is a Pilot-based project
3. Fetch releases:

```bash
curl -s "https://api.github.com/repos/Weaverse/pilot/releases?per_page=50"
```

4. Identify all releases between current version and latest (or user-specified target)
5. Present to user:
   - Current version
   - Target version (latest unless specified)
   - Number of intermediate releases
   - Summary of key changes (features, fixes, breaking changes)

**If already on latest → stop here and tell the user.**

### Phase 2 — Branch

```bash
git checkout -b update/v{CURRENT}-to-v{TARGET}
git push -u origin update/v{CURRENT}-to-v{TARGET}
```

Always work on a branch. Never update on main directly.

### Phase 3 — Plan

For each release in the update range (oldest to newest):

1. **Fetch the diff** between consecutive versions:

```bash
# Full comparison URL
https://api.github.com/repos/Weaverse/pilot/compare/v{OLD}...v{NEW}

# Raw diff
https://github.com/Weaverse/pilot/compare/v{OLD}...v{NEW}.diff
```

2. **Download the target version's source** (for reference files):

```bash
curl -sL "https://api.github.com/repos/Weaverse/pilot/tarball/v{TARGET}" | tar xz
```

3. **Categorize every changed file** into three buckets:

#### Auto-merge (safe to apply without asking)
- `package.json` version bump, dependencies
- Lock files (`package-lock.json`, `bun.lockb`, `pnpm-lock.yaml`)
- `tsconfig.json`, `vite.config.ts`, `tailwind.config.ts` — ONLY if user hasn't customized them
- New files that don't exist in user's project (additive only)
- `.github/`, `CHANGELOG.md`, `LICENSE`

#### Needs review (show diff, get approval)
- `app/components/` — UI components user may have customized
- `app/routes/` — route files user may have modified
- `app/lib/` — utility modules
- `app/root.tsx`, `app/entry.client.tsx`, `app/entry.server.tsx`
- `app/styles/` — CSS/Tailwind changes
- Any file where the user has local changes (`git diff` shows modifications from Pilot base)

#### Skip (mention but don't touch)
- Files the user deleted (they removed the feature intentionally)
- Files in directories the user reorganized
- `.env`, `.env.example` — never overwrite environment files

4. **Present the plan** in a clear table:

```
## Update Plan: v2026.3.23 → v2026.4.7

### Auto-merge (3 files)
✅ package.json — version + dependency bumps
✅ bun.lockb — lock file update
✅ app/lib/utils.ts — new helper function added

### Needs Review (5 files)
⚠️  app/components/Header.tsx — Pilot added shopify-account web component
    Your version: custom mega menu logic
    Pilot change: replaced AccountButton with <shopify-account>
    → Recommend: keep your mega menu, add shopify-account separately

⚠️  app/routes/_index.tsx — performance improvements
    Your version: added custom hero section
    Pilot change: caching + skeleton loading
    → Recommend: apply caching, keep your hero

### New Files (2 files)
➕ app/components/ScrollReveal.tsx — new scroll animation component
➕ app/lib/reviews.ts — extracted reviews API

### Skipped (1 file)
⏭️  app/components/CombinedListings.tsx — you deleted this file
```

**Wait for user confirmation before proceeding.** Ask:
> "Review the plan above. Approve to continue, or tell me which files to handle differently."

### Phase 4 — Execute

Apply changes in order, one release at a time if multi-version jump:

#### 4a. Auto-merge files

```bash
# Copy new file from Pilot source
cp /tmp/pilot-reference/{FILE_PATH} {FILE_PATH}

# Or apply targeted patch
git apply --3way <patch-file>
```

After each auto-merge, verify with `git diff --stat`.

#### 4b. Needs-review files

For each file:

1. Show a **three-way comparison**:
   - Pilot at user's version (baseline)
   - Pilot at target version (their changes)
   - User's current file (local modifications)

2. Identify what the user changed vs what Pilot changed:
   - User-only changes → preserve
   - Pilot-only changes → apply
   - Overlapping changes → flag conflict

3. For conflicts, present options:
   - Accept Pilot's version (lose user customization)
   - Keep user's version (skip Pilot improvement)
   - Manual merge (show both, let user edit)
   - Smart merge (try to combine both — only if non-overlapping regions)

4. Wait for user decision on each conflict before proceeding.

#### 4c. Commit per release

```bash
git add -A
git commit -m "chore: update Pilot v{OLD} → v{NEW}

- [list key changes applied]
- [list files with manual merge decisions]
"
```

If doing multi-version jump, repeat for each intermediate release.

### Phase 5 — Verify

After all changes applied:

```bash
# 1. Install dependencies
bun install  # or npm install / pnpm install based on lockfile

# 2. TypeScript check
bun run typecheck

# 3. Build check
bun run build
```

**If build fails:**
1. List the errors
2. Analyze root cause (dependency mismatch? breaking change missed?)
3. Propose fixes
4. Apply fixes with user approval
5. Re-run build

**If build succeeds:**
1. Run `bun run dev` briefly to check no runtime errors
2. Summarize all changes made
3. List any **manual follow-up steps**:
   - New features that need configuration
   - Breaking changes requiring code updates in customized files
   - Deprecated patterns to migrate later

### Phase 6 — Finalize

1. Present final summary:

```
## Update Complete: v2026.3.23 → v2026.4.7

✅ 12 files auto-merged
✅ 5 files reviewed and merged
✅ 2 new files added
✅ Build passes
✅ TypeCheck passes

### New features available
- Shopify Account Web Component (<shopify-account>)
- Vite chunk splitting for better caching
- ScrollReveal component for animations

### Manual follow-up (optional)
- Configure shopify-account in your Header if you want native sign-in
- Review ScrollReveal component for use in custom sections

### Rollback
git checkout main
git branch -D update/v2026.3.23-to-v2026.4.7
```

2. Ask user: "Ready to merge into main?"

```bash
# If approved
git checkout main
git merge update/v{CURRENT}-to-v{TARGET}
git push origin main
```

---

## Safety Rules

1. **Always branch first** — never update on main directly
2. **Never overwrite without asking** — every file that could have user changes needs review
3. **Commit per release** — easy to bisect if something breaks
4. **Build must pass** — don't declare success until `typecheck` + `build` both pass
5. **Offer rollback** — always tell user how to undo the whole update
6. **Respect user deletions** — if they removed a file, don't re-add it without asking

## Common Pitfalls

- **Version format**: package.json has no `v` prefix (`2026.4.7`), GitHub tags have `v` prefix (`v2026.4.7`). Always normalize.
- **Lock files**: After updating `package.json`, MUST run the correct package manager (check which lockfile exists)
- **Custom components**: User components not in original Pilot are always preserved — never delete or move them
- **Route structure**: If user reorganized routes, don't force Pilot's structure — apply route logic changes to user's structure instead
- **CSS conflicts**: Pilot may change Tailwind classes or base styles — these need careful merge to avoid breaking user styling

## SDK-Only Bumps (`@weaverse/hydrogen`)

Sometimes the ask is only "update the Weaverse SDK", not a full theme update. Verified procedure (used for a 5.5.0 → 5.15.1 client jump):

1. **Baseline before bumping.** Run `npx react-router typegen && npm run typecheck` on the CURRENT version and record every error (client forks usually have pre-existing failures). After the bump, diff against this baseline — you only own the delta. Without the baseline you'll chase errors that were always there.
2. **Peer check first**: `npm view @weaverse/hydrogen@<target> peerDependencies`. 5.15.x/5.16.x need `@shopify/hydrogen >=2025.5`, react 19, react-router 7, `@shopify/remix-oxygen` 3. `react-error-boundary` and `@weaverse/schema` arrive transitively — their absence in the theme's package.json is fine.
3. **Known break at 5.15**: `errorComponent` is typed `FC<{ error: unknown }>` (was an Error-like object). Port upstream Pilot's `GenericError`, which narrows at runtime (`error && typeof error === "object" && "message" in error`).
4. Finish with full `shopify hydrogen build --codegen` — typecheck alone misses bundler-level issues.

## Weaverse-Internal: Pilot Lock & Demo Deploy

- Pilot lives inside the Weaverse pnpm monorepo but ships an **npm** lockfile. Refresh it with `npm i --package-lock-only --workspaces=false`; plain `npm i` fails on the monorepo's `catalog:` protocol.
- Deploying `pilot.weaverse.dev`: merge to `Weaverse/pilot` `main`, then `gh repo sync Weaverse/pilot-demo --source Weaverse/pilot` — the fork carries the Oxygen deploy action and ships on sync (~1 min).
