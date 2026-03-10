---
name: release
description: >
  Automates the release workflow for this plugin: runs `make check`, bumps the
  version in plugin.json and marketplace.json, creates a release/vX.Y.Z branch
  if needed, and commits/pushes/opens a PR. Use this skill when the user says
  "release", "cut a release", "bump version", "prepare a release", "make a
  release", "create release branch", or any variation of shipping a new version.
---

# Release Workflow

This skill handles the full release cycle for a Claude Code plugin that keeps
its version in two files:

- `.claude-plugin/plugin.json` — the `"version"` field
- `.claude-plugin/marketplace.json` — the `"metadata"."version"` field

Both must always be in sync.

## Workflow

### 1. Determine the bump type

Ask the user which kind of version bump they want — **patch**, **minor**, or
**major** — unless they already specified it. Show the current version from
`plugin.json` and what the new version would be for each option so the choice
is concrete.

### 2. Run quality checks

Run `make check` (which verifies shared refs use correct paths and all shared
files exist). This is the gate — if it fails, stop and report the errors so
they can be fixed before retrying. Do not proceed past this step on failure.

### 3. Ensure we're on the right branch

The release branch must be named `release/vX.Y.Z` where X.Y.Z is the **new**
version (after bumping).

- If already on `release/vX.Y.Z` matching the new version, stay on it.
- If on `main` or any other branch, create and switch to `release/vX.Y.Z` from
  the current HEAD.
- If on a `release/` branch for a **different** version, warn the user and ask
  how to proceed — they may have started a release they want to abandon.

### 4. Bump the version

Edit both files to the new version string:

1. **`.claude-plugin/plugin.json`** — change the `"version"` value.
2. **`.claude-plugin/marketplace.json`** — change the `"metadata"."version"`
   value.

Only change the version fields — don't touch anything else in either file.
Verify both files now contain the same new version.

### 5. Commit and push

Stage `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, then
commit with the message:

```
Bump version to vX.Y.Z
```

Push the branch to origin with `-u` to set up tracking.

### 6. Open a PR

Create a pull request targeting `main` with:

- **Title:** `Release vX.Y.Z`
- **Body:** A short summary noting the version bump from old to new. Keep it
  minimal — this is a version bump PR, not a changelog.

Report the PR URL back to the user.

## Important details

- The version follows semver: `MAJOR.MINOR.PATCH`.
- Both `plugin.json` and `marketplace.json` must always have the same version.
- Always confirm the bump type with the user before making changes.
- If `make check` fails, the release is blocked — help the user fix the issues
  rather than skipping the checks.
- If there are uncommitted changes when starting, warn the user and ask whether
  to stash them, commit them first, or abort.
