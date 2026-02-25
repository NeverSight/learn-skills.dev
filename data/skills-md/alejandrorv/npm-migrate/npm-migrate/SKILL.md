---
name: npm-migrate
description: >
  AI-assisted migration and upgrade of npm packages. Handles breaking changes
  between major versions, deprecation cleanup within minor versions, adopting
  new APIs and patterns, security-driven upgrades from npm audit, and full
  dependency replacement (swapping one package for another, e.g. moment → dayjs).
  Analyzes changelogs, git diffs, and docs, scans your codebase for actual usage,
  cross-references to find what's affected, generates targeted code fixes or
  codemods, and verifies with your test suite. Use this skill whenever a user
  mentions upgrading, migrating, or updating npm packages, dealing with breaking
  changes, fixing deprecation warnings, replacing a dependency with an alternative,
  adopting new APIs from a package update, running npm audit fix with code changes,
  or comparing what changed between package versions. Trigger phrases include:
  "upgrade axios to v2", "migrate to express 5", "replace moment with dayjs",
  "fix deprecation warnings", "npm audit says vulnerable", "adopt the new API",
  "what changed between version X and Y", "swap lodash for es-toolkit",
  "help me upgrade my dependencies", "clean up deprecated calls".
---

# npm-migrate

AI-assisted migration of npm packages: major version upgrades, deprecation cleanup,
new API adoption, security-driven updates, and full dependency replacement. Analyzes
what changed, scans your codebase, and generates targeted fixes.

## Core Workflow

Follow these steps in order for every migration request:

### Step 1: Identify Migration Type and Scope

Determine what kind of migration this is:

| Type | Example | Key difference |
|------|---------|---------------|
| **Major upgrade** | express 4 → 5 | Breaking changes, must fix |
| **Minor/patch upgrade** | react 18.2 → 18.3 | Deprecation cleanup, optional but recommended |
| **Deprecation cleanup** | Remove deprecated APIs within same major | Proactive, avoids future breakage |
| **Feature adoption** | Adopt React Server Components | New patterns, not strictly required |
| **Security fix** | npm audit vulnerability | Urgency varies, may require code changes |
| **Dependency swap** | moment → dayjs, enzyme → testing-library | Map old API to new package's API |

Then determine the package(s), source version, and target version (or replacement).

```bash
# Read current version from package.json
cat package.json | jq '.dependencies["<package>"] // .devDependencies["<package>"]'

# If upgrading: find latest major
npm view <package> version

# If swapping: check the replacement package
npm view <new-package> version

# If security: check what npm audit recommends
npm audit --json | jq '.vulnerabilities["<package>"]'
```

If the user says "upgrade X" without specifying versions, detect the current
version from package.json and target the latest major.

If the user says "replace X with Y", treat it as a dependency swap — the
intelligence gathering step will focus on API mapping between the two packages.

### Step 2: Gather Intelligence

Read `references/intelligence-gathering.md` for the full procedure.

Collect migration data from multiple sources in this priority order:

**For version upgrades (major, minor, patch):**

1. **Official migration guide** — Check the package's repo/docs for a MIGRATION.md
   or upgrade guide. This is the highest-signal source.
2. **CHANGELOG / RELEASES** — Parse entries between source and target versions.
   Focus on lines containing: BREAKING, removed, renamed, deprecated, changed.
3. **Git diff of public API** — Compare type definitions, exports, and index files
   between version tags.
4. **npm deprecation messages** — Check if intermediate versions have deprecation
   notices pointing to replacements.

**For dependency swaps (replacing one package with another):**

1. **API comparison** — Map the old package's API surface to the new package's
   equivalents. Read both packages' docs.
2. **Migration guides** — Many replacement packages provide explicit migration
   guides from the package they're replacing (e.g., dayjs has a "from moment" guide).
3. **Feature gap analysis** — Identify features used in the old package that have
   no direct equivalent in the new one.

**For security-driven upgrades:**

1. **npm audit details** — Get the vulnerability description, severity, and
   which versions contain the fix.
2. **Advisory details** — Fetch the GitHub advisory or CVE for context on
   whether the vulnerability actually affects the user's usage pattern.
3. **Then follow the version upgrade path above.**

### Step 3: Analyze User's Codebase

Read `references/codebase-analysis.md` for the full procedure.

Scan the project to build a usage map of the package being migrated:

- All import/require statements for the package
- Which APIs, methods, types, and configs are used
- Usage patterns (e.g., interceptors in axios, middleware in express)
- Related config files (webpack.config.js, babel.config.js, etc.)

### Step 4: Cross-Reference and Plan

Read `references/peer-dependencies.md` to check for peer dependency conflicts
before planning changes. If the upgrade triggers cascading peer dependency
updates, document the full chain and present it to the user first.

Match the breaking changes (or API differences for swaps) found in Step 2
against the usage map from Step 3. Categorize each item as:

| Category | Meaning | Action |
|----------|---------|--------|
| `AFFECTED` | User's code uses a changed/removed API | Must fix |
| `SAFE` | Change exists but user doesn't use it | No action |
| `REVIEW` | Behavioral change that may affect user subtly | Manual review |
| `DEPRECATED` | Still works but will break in next major | Recommend fix |
| `NO_EQUIVALENT` | Used API has no direct replacement (swaps only) | Needs workaround or custom code |
| `SECURITY` | Vulnerable code path in user's usage | Priority fix |

### Step 5: Generate Migration

Read `references/migration-patterns.md` for common transformation patterns.

For each `AFFECTED` item, generate the fix. Prefer this order:

1. **Automated fix** — Direct code transformation (rename, restructure, replace)
2. **Codemod script** — When the change is mechanical but widespread
   (see `references/codemod-generation.md` for templates and patterns)
3. **Manual guidance** — When the fix requires human judgment (architecture changes)

### Step 6: Apply and Verify

```bash
# For version upgrades:
npm install <package>@<target-version>

# For dependency swaps:
npm uninstall <old-package>
npm install <new-package>
```

Run the post-migration verification script to check everything at once:

```bash
# For version upgrades:
node <skill-path>/scripts/post-migration-verify.mjs --package <package>

# For dependency swaps (also checks old package is fully removed):
node <skill-path>/scripts/post-migration-verify.mjs --package <new-package> --swap-from <old-package>
```

The script automatically detects and runs: dependency resolution, TypeScript
compilation, test suite, linter, build, old package removal check (swaps),
and deprecation warning detection. It outputs a JSON report.

If the verification script is not available, run these checks manually:

```bash
npm test
npx tsc --noEmit        # if TypeScript
npm run lint             # if linter configured
npm run build            # if build script exists
```

Report results with a summary table:

```
Migration Summary: <package> v<from> → v<target>
─────────────────────────────────────────────────
✅ Automated fixes applied:    X
⚠️  Manual review required:    Y
ℹ️  No action needed:          Z
❌ Failed transformations:     W
```

## Key Principles

- **Never blindly upgrade** — Always analyze before changing code.
- **Preserve behavior** — The goal is identical behavior on the new version, not refactoring.
- **Be conservative** — When unsure, flag for `REVIEW` rather than auto-fixing.
- **Test after every change** — Run the project's test suite after applying fixes.
- **Explain why** — For every change, briefly explain what broke and why the fix works.

## Edge Cases

- **Monorepos**: Scan all workspace packages for usage, not just root.
- **Re-exports**: Track when the package is re-exported through internal modules.
- **Peer dependencies**: Check if upgrading the package requires upgrading peers.
- **Lock file conflicts**: After migration, ensure lock file is consistent.
- **Multiple packages at once**: Migrate one at a time unless they must move together (e.g., @babel/* packages).

## Output Checklist

Every migration output should include:

- [ ] Summary table of all breaking changes and their status
- [ ] List of files modified with brief explanation per file
- [ ] Any manual review items clearly flagged with context
- [ ] Verification that tests pass (or report of failures)
- [ ] Peer dependency updates if needed
- [ ] Rollback instructions (the original versions to restore)
