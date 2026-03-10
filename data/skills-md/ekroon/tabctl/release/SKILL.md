---
name: release
description: 'Bump version, test, build, tag, push, and create a GitHub Release. Use when user asks to release, bump version, cut a release, or mentions "/release". Analyzes conventional commits to auto-detect bump type. Always confirms before pushing.'
license: MIT
allowed-tools: Bash, AskUser
---

# Release

Automate the full release cycle: version bump → test → build → commit → push branch → open PR → merge → tag → GitHub Release.

Direct pushes to `main` are blocked by a branch ruleset. All releases go through a PR.

## Preferred GitHub Actions flow

The default release path is now GitHub Actions-driven:

1. Run the **Prepare Release** workflow (`.github/workflows/prepare-release.yml`)
2. Review/approve the generated release PR
3. Let GitHub auto-merge the PR after checks pass
4. The **Tag Release** workflow (`.github/workflows/tag-release.yml`) tags the merge commit
5. The **Release** workflow (`.github/workflows/release.yml`) runs for that tag and publishes the artifacts

The manual flow below remains the fallback/operator path when you need to release outside GitHub Actions.

## Version files

All version files must stay in sync. The Rust workspace manifest is the canonical Rust version source, and `scripts/bump-version.js` (exposed via `npm run bump:*`) updates the mirrored package versions in one command. The release workflow (`release.yml`) validates they match:

1. `rust/Cargo.toml` — workspace package version (Rust source of truth)
2. `package.json` — root npm package version (mirrors the workspace version) and `optionalDependencies.tabctl-win32-x64`
3. `package-lock.json` — lockfile
4. `packages/win32-x64/package.json` — Windows platform package
5. `rust/crates/tabctl/Cargo.toml` — main Rust binary (inherits workspace version)
6. `rust/crates/host/Cargo.toml` — host crate (inherits workspace version)
7. `rust/crates/graphql/Cargo.toml` — GraphQL crate (inherits workspace version)
8. `rust/crates/shared/Cargo.toml` — shared crate (inherits workspace version)
9. `rust/Cargo.lock` — Rust lockfile

Never edit these version fields manually. Always use `npm run bump:<kind>`.

## Prerequisites

- Working tree is clean (`git status` shows no uncommitted changes)
- On the `main` branch
- `gh` CLI is authenticated (`gh auth status`)
- `npm test` and `npm run build` pass

## Workflow

### Step 1: Pre-flight checks

```bash
git status --porcelain
git branch --show-current
gh auth status
```

If the working tree is dirty, stop and ask the user to commit or stash first.
If not on `main`, warn the user and ask whether to proceed.

### Step 2: Determine version bump

Find the last tag and analyze commits since then:

```bash
LAST_TAG=$(git tag --sort=-v:refname | head -1)
git log "${LAST_TAG}..HEAD" --oneline --no-decorate
```

**Auto-detect bump type from conventional commits:**

| Signal | Bump |
|--------|------|
| Any commit with `BREAKING CHANGE` in body/footer, or type ending in `!` (e.g. `feat!:`) | **major** |
| Any `feat:` or `feat(scope):` commit | **minor** |
| Only `fix:`, `perf:`, `docs:`, `chore:`, `refactor:`, `test:`, `ci:`, `build:`, `style:` | **patch** |

**Pre-release version handling:**

If the current version is a pre-release (e.g. `0.6.0-alpha.9`), compute the next version based on what the user requests:

- **Next alpha**: increment the alpha number → `0.6.0-alpha.10`
- **Release candidate**: `0.6.0-rc.1`
- **Stable release**: `0.6.0`
- **New minor/major alpha**: e.g. `0.7.0-alpha.1` or `1.0.0-alpha.1`

For stable versions, use standard semver bumping:

```bash
CURRENT=$(echo "$LAST_TAG" | sed 's/^v//')
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

# For major bump:
NEW="$((MAJOR + 1)).0.0"
# For minor bump:
NEW="$MAJOR.$((MINOR + 1)).0"
# For patch bump:
NEW="$MAJOR.$MINOR.$((PATCH + 1))"
```

### Step 3: Show plan and confirm

Before making any changes, present a summary and use AskUser to confirm:

```
Release plan:
  Current version: v{CURRENT}
  New version:     v{NEW} ({BUMP_TYPE})
  Commits:         {N} commits since {LAST_TAG}

  {commit list}

  Steps:
  1. Create branch chore/release-v{NEW}
  2. Update all version files to {NEW}
  3. Run npm test
  4. Run npm run build
  5. Commit: chore(release): v{NEW}
  6. Push branch, open PR
  7. Wait for CI, merge PR (normal merge, not squash)
  8. Tag v{NEW} on main
  9. Create GitHub Release (triggers release.yml → npm publish + binary builds)
```

Ask the user to confirm the version. Offer the recommended bump plus alternatives.
If the user picks a different bump or types a custom version, use that instead.

### Step 4: Create release branch

```bash
git checkout -b "chore/release-v${NEW}"
```

### Step 5: Update all version files

Use the bump script which updates all version files (package.json, package-lock.json, packages/win32-x64/package.json, 3× Cargo.toml, Cargo.lock) in one command:

```bash
# For the recommended bump type:
npm run bump:alpha    # 0.6.0-alpha.9 → 0.6.0-alpha.10
npm run bump:rc       # 0.6.0-alpha.10 → 0.6.0-rc.1
npm run bump:stable   # 0.6.0-rc.1 → 0.6.0
npm run bump:patch    # 0.6.0 → 0.6.1
npm run bump:minor    # 0.6.1 → 0.7.0
npm run bump:major    # 0.7.0 → 1.0.0
```

If the user chose a custom version that doesn't match a standard bump, update manually:
```bash
node scripts/bump-version.js <kind>
```

Verify the output matches the expected version.

### Step 6: Run tests

```bash
npm test
```

If tests fail, stop and report the failure. Do NOT proceed with the release.

### Step 7: Build

```bash
npm run build
```

If the build fails, stop and report the failure. Do NOT proceed with the release.

### Step 8: Commit

```bash
git add package.json package-lock.json packages/win32-x64/package.json \
       rust/crates/tabctl/Cargo.toml rust/crates/host/Cargo.toml \
       rust/crates/graphql/Cargo.toml rust/crates/shared/Cargo.toml rust/Cargo.lock
git commit -m "chore(release): v${NEW}"
```

All these files are updated by `scripts/bump-version.js` in Step 5.

### Step 9: Push branch and open PR

```bash
git push -u origin "chore/release-v${NEW}"
GH_PAGER="" gh pr create \
  --title "chore(release): v${NEW}" \
  --body "Bump all version files to ${NEW}. After merge, tag and create release." \
  --base main
```

Note the PR number from the output.

### Step 10: Merge, tag, and release

Use the existing helper script which waits for CI, merges (normal merge, not squash), tags on main, and creates the GitHub release:

```bash
scripts/ci-wait-merge.sh <PR_NUMBER> --tag "v${NEW}"
```

This script:
1. Waits for all CI checks to pass (`gh pr checks --watch`)
2. Merges the PR with `--merge --delete-branch` (normal merge commit)
3. Checks out main and pulls
4. Creates annotated tag `v{NEW}`
5. Pushes the tag
6. Creates a GitHub release (with `--prerelease` for `-alpha.N` / `-rc.N` versions)

The release triggers the `release.yml` workflow which builds binaries and publishes to npm.

After completion, display the release URL so the user can review.

## Dry-run mode

If the user asks for a dry run (or passes `--dry-run`), perform Steps 1-3 only: pre-flight checks, version analysis, and show the plan. Do NOT modify any files, commit, tag, push, or create a release.

## Abort and rollback

If any step after Step 5 fails (tests, build, commit, push, or PR creation), provide rollback instructions:

```bash
# Switch back to main and delete the release branch
git checkout main
git branch -D "chore/release-v${NEW}"

# If PR was created, close it
gh pr close <PR_NUMBER> --delete-branch

# If tag was created locally
git tag -d "v${NEW}"

# If tag was pushed — only with explicit user confirmation
git push origin --delete "v${NEW}"
```

## Safety rules

- NEVER skip tests or build
- NEVER force push
- NEVER push directly to main — always use a PR
- NEVER squash merge release PRs — use normal merge to preserve commit identity
- NEVER create a release without user confirmation
- NEVER delete existing tags or releases without explicit user request
- If `--dry-run`, do NOT modify anything
