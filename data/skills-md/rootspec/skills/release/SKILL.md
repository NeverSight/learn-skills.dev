---
name: release
description: Use when the user wants to create a release. Guides through updating changelogs and running the release script.
argument-hint: [major|minor|patch]
---

You are preparing a release. Follow this workflow in order.

## Versioning

- **patch** — bug fixes only
- **minor** — new features
- **major** — breaking changes or public launch

## Step 1 — Review unreleased changes

Read `CHANGELOG.md` and check what is listed under `## [Unreleased]`. Summarize the changes for the user so they can confirm the release scope and choose the right version bump.

## Step 2 — Update user-facing changelog (optional)

If your project has a user-facing changelog, update it now and commit before continuing.

## Step 3 — Ensure `release` script exists in package.json

Check if `package.json` has a `release` script. If not, add it:

```json
"release": ".agents/skills/release/scripts/release.sh"
```

## Step 4 — Run the release script

```bash
echo "y" | npm run release -- [major|minor|patch]
```

> **Important:** The release script is interactive — it pauses and asks:
> *"Have you updated your changelog(s)? (y/n)"*
> Pipe `y` to answer automatically, since we completed that in the steps above.

The script will:
1. Verify you are on `main` with no uncommitted changes
2. Bump the version in `package.json`
3. Move `[Unreleased]` in `CHANGELOG.md` to the new version with today's date
4. Commit, tag, and push to origin
5. Create a GitHub release with the changelog notes

## Step 5 — Confirm

Report the new version number and GitHub release URL to the user.
