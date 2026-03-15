---
name: gh-oss-release
description: >
  Create GitHub releases across multiple OSS repositories. Checks release status via `gh oss-watch releases`,
  analyzes unreleased commits to recommend semver bumps, confirms with user, then creates releases.
  Triggers: "create releases", "release my packages", "check for releases", "oss releases",
  "gh oss-watch releases", "/oss-release", "release status", "bump versions"
compatibility: Requires gh CLI and gh oss-watch extension
metadata:
  author: jackchuka
  scope: generic
  confirms:
    - create GitHub releases
    - push to homebrew-tap
    - save to filesystem
---

# OSS Release

Batch release workflow for multiple OSS repositories using `gh oss-watch releases`.

## Workflow

### Step 1: Check Release Status

Run `gh oss-watch releases` to identify repos with unreleased commits.

If all repos are up to date, report that and stop.

### Step 2: Analyze Unreleased Commits

For each repo needing a release, fetch commit messages since the last tag in parallel:

```bash
gh api repos/<owner>/<repo>/compare/<last-tag>...HEAD --jq '[.commits[] | .commit.message | split("\n")[0]] | .[]'
```

### Step 3: Recommend Semver Bump

Classify each commit's first line and recommend the highest applicable bump:

| Commit pattern                                          | Bump      |
| ------------------------------------------------------- | --------- |
| `deps:`, `deps-dev:`, `ci:`, `chore:`, maintenance-only | **patch** |
| `feat:`, new functionality, non-breaking additions      | **minor** |
| `BREAKING CHANGE`, `!:` suffix, API removals            | **major** |

If ALL commits are deps/ci/chore, recommend **patch**. If any commit adds a feature, recommend **minor**. If any commit has breaking changes, recommend **major**.

### Step 4: Present Recommendations

Present a table for user confirmation:

```
| Repo | Current | Recommended | Commits | Rationale |
|------|---------|-------------|---------|-----------|
| repo-name | v1.2.3 | v1.2.4 | 5 | All dependency bumps |
```

Use AskUserQuestion or wait for explicit user confirmation before proceeding.

### Step 5: Create Releases

After confirmation, create releases in parallel:

```bash
gh release create <new-tag> --repo <owner>/<repo> --generate-notes
```

### Step 6: Verify

Run `gh oss-watch releases` again to confirm all repos show "up to date".

### Step 7: Update Homebrew Tap

Ask the user if they want to update the homebrew tap before proceeding. If they decline, stop here.

After confirmation, update the homebrew-tap formulae:

```bash
cd ~/ghq/github.com/jackchuka/homebrew-tap
git pull origin main
make update
```

Then commit with a message listing the updated versions (e.g., `update: gql-ingest v3.1.6, slackcli v0.3.0`) and push:

```bash
git add -A
git commit -m "<version summary>"
git push origin main
```

## Important Notes

- **Tag-triggered CI**: Most repos have CI that triggers on tag push (goreleaser, gh-extension-precompile, npm publish). The `gh release create` command creates the tag which triggers the CI build.
- **npm packages with tag-triggered workflows**: These repos derive version from the git tag during CI — no package.json bump needed.
- **Parallel execution**: Fetch commits and create releases in parallel across repos for speed.
- **Never force**: Always confirm with user before creating any releases.
