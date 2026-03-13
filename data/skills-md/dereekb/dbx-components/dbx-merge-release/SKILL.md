---
name: dbx-merge-release
description: Merge main branch changes back into develop after a release. Handles pulling latest, merging with conflict resolution, and creating the merge commit with dev tag.
triggers:
  - merge release
  - merge main
  - merge in main
  - post-release merge
  - start merge
  - end merge
  - merge after release
---

# dbx-merge-release

Automated workflow for merging the main branch back into develop after a release has been cut. Uses the shell scripts in the repository root.

## Context

After a release is published (via CircleCI), the main branch has release commits (version bumps, changelog, tag) that need to be merged back into develop.

**Important constraint:** Main and develop do NOT share linear history — main gets force-merged release commits. This means `git rebase origin/main` will never work (it tries to replay the entire repo). Always use the merge scripts.

## How It Works

The scripts handle two cases automatically:

1. **No new commits on develop:** Simple merge. Conflicts (if any) are from CI-generated version bumps — resolve with `--theirs`.

2. **New commits on develop after the release:** The `start-merge-in-main.sh` script detects commits on develop that have a UTC timestamp after the latest commit on `origin/main`. It saves them to a temporary branch (`temp/develop-new-commits`), resets develop back, then does the merge. After `end-merge-in-main.sh` completes, the agent rebases the saved commits on top of develop so they appear after the new `-dev` tag and will be included in the next release.

## Workflow

### Step 1: Start the Merge

Ensure you're on `develop` with a clean working tree, then:

```bash
sh start-merge-in-main.sh
```

This script:
1. Checks for uncommitted changes (exits if dirty)
2. Fetches and pulls latest `develop` and `main` from origin
3. Compares timestamps: finds any develop commits after the latest main commit
4. If found: saves them to `temp/develop-new-commits`, resets develop back
5. Starts a merge of `origin/main` into develop with `--no-commit --no-ff`

### Step 2: Resolve Conflicts

Check for conflicts:

```bash
git diff --name-only --diff-filter=U
```

Since develop has been reset to before any new work, conflicts should only be from CI-generated files. Resolve with:

```bash
git checkout --theirs .
git add .
```

If there are develop-only files that conflict (rare after the reset), keep ours:
```bash
git checkout --ours <file>
git add <file>
```

### Step 3: Verify

```bash
git status
git diff --cached --stat
```

Ensure all conflicts are resolved and staged changes look reasonable (mostly package.json version bumps + CHANGELOG).

### Step 4: Complete the Merge

```bash
sh end-merge-in-main.sh
```

This script:
1. Creates the merge commit with message: `merge(release): merge <tag> release`
2. Runs `make-dev-tag.sh` to create the new `-dev` tag
3. Prints a reminder if `temp/develop-new-commits` exists (but does NOT rebase it)

### Step 5: Rebase Saved Commits (if applicable)

If `start-merge-in-main.sh` saved commits to `temp/develop-new-commits`, rebase them onto develop now:

```bash
git rebase develop temp/develop-new-commits
```

If there are conflicts during the rebase, resolve them per-commit:
- Check conflicts: `git status`
- For CI-generated files (package.json versions): accept the develop version (which now has the release versions)
- For source code: keep the temp branch's changes (the new development work)
- Continue: `git rebase --continue`

After the rebase completes, fast-forward develop to include the rebased commits:

```bash
git checkout develop
git merge --ff-only temp/develop-new-commits
git branch -d temp/develop-new-commits
```

### Step 6: Verify Tags

After the merge (and optional rebase), verify tags:

```bash
git tag --list "v*" --sort=-v:refname | head -5
```

Expected output (e.g., after v13.0.6 release):
```
v13.0.6-dev
v13.0.6
v13.0.5-dev
v13.0.5
...
```

If the `-dev` tag is missing: `sh make-dev-tag.sh`

### Step 7: Push

If there were **no saved commits** (simple merge):
```bash
git push origin develop --tags
```

If saved commits **were rebased** back onto develop, the branch history was rewritten and a force push is needed. **Always confirm with the user before force pushing:**
```bash
git push origin develop --tags --force-with-lease
```

## How the Tagging System Works

### Tag Flow

1. **Release on CircleCI:** The release script (`tools/scripts/release.mjs`) runs on a release branch. It:
   - Finds the last stable tag (e.g., `v13.0.5`) and its `-dev` counterpart (`v13.0.5-dev`)
   - Uses the `-dev` tag as the anchor — only commits **after** the `-dev` tag are considered for the next release
   - Bumps the version, generates a changelog, commits, and creates a new release tag (e.g., `v13.0.6`)

2. **Merge back to develop:** This workflow. After merging main into develop, `end-merge-in-main.sh` creates the new `-dev` tag (e.g., `v13.0.6-dev`).

3. **Next release cycle:** The next release looks for `v13.0.6-dev` as the starting point. Only commits after that tag are included.

### Why the `-dev` Tag Matters

The release script uses this logic:

```
fromTag = allTags.includes(devTag) ? devTag : lastStableTag
```

- The `-dev` tag marks where post-release development begins on `develop`
- Without it, the release script would compare from the wrong point and produce incorrect changelogs
- Commits made before the merge (and before the `-dev` tag) would NOT be included in the next release — this is why the scripts save and rebase new commits to appear after the tag

### Tag Naming Convention

| Tag | Created By | Lives On | Purpose |
|-----|-----------|----------|---------|
| `v13.0.6` | CircleCI release | `main` | Marks the release commit |
| `v13.0.6-dev` | `make-dev-tag.sh` | `develop` | Marks the start of the next dev cycle |

## Important Notes

- **Always start from a clean working tree** — the start script checks for this
- **Must be on the develop branch** before starting
- **Never use `git rebase origin/main`** — main and develop don't share linear history
- **The merge commit type is `merge`** — this is a reserved type (see dbx-commit-messages skill)
- **The dev tag is required** — without it, the next release will analyze the wrong set of commits
- **Do not amend** the merge commit — the format is generated by the script
- **The temp branch `temp/develop-new-commits`** is created and cleaned up automatically by the scripts

## Error Recovery

- If the start script fails due to dirty state: stash or commit changes first
- If the merge has unresolvable conflicts: `git merge --abort` and investigate
- If the end script fails: manually create the commit following the `merge(release): merge <tag> release` format, then run `sh make-dev-tag.sh`
- If the `-dev` tag is missing after completion: run `sh make-dev-tag.sh` manually
- If the temp branch exists from a failed previous run: the start script will clean it up automatically

## Related Scripts

- `start-merge-in-main.sh` — Detects new commits, saves them, initiates the merge
- `end-merge-in-main.sh` — Commits the merge and creates dev tag
- `make-dev-tag.sh` — Creates the `<tag>-dev` git tag
- `tools/scripts/release.mjs` — Release script that consumes the `-dev` tags
