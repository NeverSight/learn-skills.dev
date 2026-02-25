---
name: changesets
description: 'Changesets for versioning and changelog management in monorepos. Use when managing package versions, generating changelogs, or publishing packages. Use for changesets, versioning, changelog, semver, monorepo-versioning, release, publish, bump.'
license: MIT
metadata:
  author: oakoss
  version: '1.2'
  source: 'https://github.com/changesets/changesets'
user-invocable: false
---

# Changesets

## Overview

Changesets is a versioning and changelog management tool focused on multi-package repositories. Contributors declare the semver impact of each change (major/minor/patch) via changeset files, then Changesets aggregates them to bump versions, update changelogs, and publish packages in a single coordinated release.

**When to use:** Monorepo versioning, automated changelog generation, coordinated multi-package releases, CI-driven publishing, prerelease/snapshot workflows.

**When NOT to use:** Single-file projects with no npm publishing, projects using commit-message-based versioning (semantic-release), manual version management without an npm registry, projects where a single maintainer controls all releases without PR collaboration.

### How It Works

1. A contributor adds a changeset file declaring affected packages, bump types, and a summary
2. The changeset file is committed alongside the code change in the PR
3. When ready to release, `changeset version` consumes all pending changesets and updates versions and changelogs
4. `changeset publish` publishes the updated packages to npm and creates git tags
5. In CI, the official GitHub Action automates steps 3-4 via an auto-maintained "Version Packages" PR

## Key Concepts

- **Changeset file** — A markdown file in `.changeset/` declaring which packages are affected, their bump type (major/minor/patch), and a human-readable summary that appears in the changelog
- **Version command** — Consumes all pending changeset files, calculates final version bumps, updates `package.json` versions, generates `CHANGELOG.md` entries, and bumps internal dependency ranges
- **Publish command** — Publishes updated packages to npm and creates git tags; must run immediately after `version` with no commits in between
- **Linked packages** — Packages that share the highest bump type within a release but maintain independent version numbers
- **Fixed packages** — Packages that always share the exact same version number across the group
- **Prerelease mode** — A mode where `version` produces prerelease versions (e.g., `1.0.0-beta.0`) for testing before stable release
- **Snapshot releases** — Temporary `0.0.0-timestamp` versions for ad-hoc testing without affecting the main release line

## Configuration Quick Reference

| Option                       | Default                         | Description                                                   |
| ---------------------------- | ------------------------------- | ------------------------------------------------------------- |
| `changelog`                  | `"@changesets/cli/changelog"`   | Changelog generator package or `false` to disable             |
| `commit`                     | `false`                         | Auto-commit on `version` and `add` commands                   |
| `access`                     | `"restricted"`                  | npm publish access; set `"public"` for public scoped packages |
| `baseBranch`                 | `"main"`                        | Branch used for change detection                              |
| `linked`                     | `[]`                            | Groups of packages that share highest bump type               |
| `fixed`                      | `[]`                            | Groups of packages that share exact version                   |
| `ignore`                     | `[]`                            | Packages excluded from changeset versioning                   |
| `updateInternalDependencies` | `"patch"`                       | When to bump dependents: `"patch"` or `"minor"`               |
| `privatePackages`            | `{ version: true, tag: false }` | Version/tag behavior for `"private": true` packages           |

## Quick Reference

| Pattern             | Command / Config                                        | Key Points                                                   |
| ------------------- | ------------------------------------------------------- | ------------------------------------------------------------ |
| Initialize          | `npx @changesets/cli init`                              | Creates `.changeset/` folder with config                     |
| Add changeset       | `npx @changesets/cli add`                               | Interactive prompt for packages and bump type                |
| Add empty changeset | `npx @changesets/cli add --empty`                       | Declares no packages need versioning (satisfies CI)          |
| Version packages    | `npx @changesets/cli version`                           | Consumes changesets, bumps versions, updates changelogs      |
| Publish packages    | `npx @changesets/cli publish`                           | Publishes to npm, creates git tags                           |
| Check status        | `npx @changesets/cli status`                            | Lists pending changesets; exits 1 if changes lack changesets |
| Status since branch | `npx @changesets/cli status --since=main`               | Only checks changes since diverging from main                |
| Enter prerelease    | `npx @changesets/cli pre enter <tag>`                   | Enables prerelease mode (beta, alpha, rc, next)              |
| Exit prerelease     | `npx @changesets/cli pre exit`                          | Returns to normal versioning mode                            |
| Snapshot version    | `npx @changesets/cli version --snapshot`                | Creates 0.0.0-timestamp versions for testing                 |
| Snapshot publish    | `npx @changesets/cli publish --tag canary --no-git-tag` | Publishes snapshot without overwriting latest dist-tag       |
| Link packages       | `"linked": [["pkg-a", "pkg-b"]]` in config              | Packages share the highest version bump type                 |
| Fix packages        | `"fixed": [["pkg-*"]]` in config                        | Packages share the exact same version number                 |
| Ignore packages     | `"ignore": ["pkg-internal"]` in config                  | Excludes packages from changeset versioning                  |
| Public access       | `"access": "public"` in config                          | Required for publishing public scoped packages               |
| GitHub changelog    | `"changelog": ["@changesets/changelog-github", ...]`    | Adds PR links and contributor attribution                    |
| Auto-commit         | `"commit": true` in config                              | Version and add commands auto-commit changes                 |
| Internal deps       | `"updateInternalDependencies": "patch"` in config       | Controls when internal dependents get bumped                 |

## Common Mistakes

| Mistake                                                | Correct Pattern                                                           |
| ------------------------------------------------------ | ------------------------------------------------------------------------- |
| Committing between `version` and `publish`             | Run `publish` immediately after `version` with no commits in between      |
| Forgetting `--empty` for PRs with no package changes   | Use `npx @changesets/cli add --empty` to satisfy CI checks                |
| Using `linked` when packages must share exact versions | Use `fixed` for identical versions; `linked` only shares bump magnitude   |
| Setting `access: "restricted"` for public packages     | Set `access: "public"` in config for public npm packages                  |
| Not including `fetch-depth: 0` in CI checkout          | Full git history is needed for changeset detection                        |
| Running `publish` without building first               | Always run build step before `changeset publish`                          |
| Entering prerelease mode on main branch                | Use a dedicated branch for prereleases to avoid blocking normal releases  |
| Ignoring packages that others depend on                | Ignored packages skip bumps, breaking dependents — use sparingly          |
| Publishing snapshots with default tag                  | Always use `--tag` flag to avoid overwriting `latest` dist-tag            |
| Not setting `NPM_TOKEN` in CI environment              | Both `GITHUB_TOKEN` and `NPM_TOKEN` are required for automated publishing |
| Using `changeset publish` in CI without the action     | The official `changesets/action` handles the two-mode workflow correctly  |
| Manually editing generated `CHANGELOG.md`              | Edit changeset files instead; changelogs are regenerated on `version`     |

## Delegation

- **CI pipeline debugging**: Use `Explore` agent for repository-specific workflow discovery
- **npm publishing issues**: Use `Task` agent for debugging publish and registry authentication failures

> If the `turborepo` skill is available, delegate build orchestration, task caching, and CI optimization to it.
> If the `pnpm-workspace` skill is available, delegate workspace setup, dependency linking, catalogs, and Docker deployment to it. See its monorepo integration reference for the end-to-end release pipeline.

## References

- [Basic workflow: adding changesets, versioning, publishing, CI integration](references/basic-workflow.md)
- [Monorepo setup: configuration, linked packages, fixed versioning, ignore patterns](references/monorepo-setup.md)
- [CI automation: GitHub Actions, automated PRs, snapshot releases, prerelease channels](references/ci-automation.md)
