---
name: dependency-upgrader
description: Safely upgrades project dependencies by inventorying outdated packages, reading changelogs and migration guides, staging upgrades in isolated commits, running tests at each step, and rolling back cleanly on failure. Use this skill when asked to "upgrade dependencies", "bump packages", "update npm/pip/cargo/go modules", "resolve a CVE / security advisory", "migrate to the latest version of <library>", "fix outdated dependencies", "do a dependency bump PR", or when a Dependabot/Renovate PR needs review and verification.
license: MIT
---

# Dependency Upgrader

## Overview

This skill drives safe, auditable dependency upgrades across ecosystems
(npm/yarn/pnpm, pip/poetry/uv, cargo, go modules, bundler, maven/gradle,
composer). The core discipline: **one upgrade per commit, tests green between
each, and a known-good rollback point at all times**. Never bulk-upgrade
everything and hope.

Keywords: dependency upgrade, bump packages, outdated, semver, breaking change,
changelog, migration guide, lockfile, CVE, security advisory, Dependabot,
Renovate, rollback, npm audit, pip-audit.

Use this skill when the user wants to update libraries, patch a vulnerability,
migrate a major version, or vet an automated bump PR.

## Core Principles

1. **Isolate.** One package (or one tightly-coupled group) per commit. A failed
   upgrade must be revertable without touching unrelated work.
2. **Read before you write.** Always inspect the changelog / release notes /
   migration guide before bumping across a major version.
3. **Tiered risk.** Patch < minor < major. Batch low-risk; isolate high-risk.
4. **Test gate.** The test suite (or a defined verification command) must pass
   before each commit. No green, no commit.
5. **Always have a rollback.** Know the exact git SHA and lockfile state to
   return to. See `references/rollback.md`.

## Workflow

Follow these steps in order. Do not skip the inventory or the changelog read.

### 1. Establish a clean baseline
- Confirm the working tree is clean (`git status`). If not, stop and ask the
  user how to proceed — never upgrade on top of uncommitted changes.
- Record the current commit SHA as the rollback anchor.
- Run the test suite once to confirm it is **green before** you start. If tests
  are already failing, report that and stop — you cannot attribute later
  failures otherwise.
- Identify the ecosystem and the verification command. See
  `references/ecosystems.md` for the canonical commands per package manager.

### 2. Inventory outdated dependencies
- Run the detector script: `python3 scripts/check_outdated.py --dir <repo>`.
  It auto-detects the ecosystem and prints a risk-tiered table (patch / minor /
  major) plus any known advisories it can surface from the native auditor.
- Or run the native tool directly (`npm outdated`, `pip list --outdated`,
  `cargo outdated`, `go list -m -u all`) — see `references/ecosystems.md`.
- Classify each candidate by semver jump and by whether it is a direct or
  transitive dependency.

### 3. Plan the upgrade order
- **Security first.** Any package with a CVE/advisory jumps to the front.
- Group: (a) safe batch = all patch + most minor of well-behaved libs;
  (b) isolated = every major bump, every framework/build-tool, anything with a
  published breaking-change list.
- Order isolated upgrades so that foundational packages (type systems, build
  tools, test frameworks) go first, then their dependents.
- Present the plan to the user before executing if there is more than one major
  bump or any framework migration.

### 4. Execute — patch & safe minor batch
- Apply the batch (e.g. `npm update`, or pin the resolved versions in the
  manifest), regenerate the lockfile.
- Run the verification command. If green: commit with a clear message
  (see template below). If red: bisect by splitting the batch in half, or fall
  back to upgrading each package individually to find the culprit.

### 5. Execute — major bumps, one at a time
For each isolated upgrade:
1. Read the changelog / release notes / migration guide. Use `WebFetch` or
   `WebSearch` for the project's CHANGELOG and "migration guide vX". Note every
   breaking change that touches the codebase.
2. Bump the single package, regenerate the lockfile.
3. Apply required code changes for the breaking changes you found
   (renamed APIs, removed options, config schema changes, peer-dep bumps).
4. Run the verification command.
   - **Green** → commit (one package per commit). Move on.
   - **Red** → fix forward only if the cause is clear and small. Otherwise
     **roll back this single upgrade** (see `references/rollback.md`) and report
     the blocker to the user with the changelog evidence. Do not leave the tree
     broken.

### 6. Final verification & report
- Run the full test suite (and a build, and a smoke run if applicable) one more
  time on the final state.
- Re-run the auditor to confirm advisories are resolved.
- Summarize: what was upgraded (old → new), what code changed, what was
  deferred and why, and the rollback SHA. Use `templates/upgrade-report.md`.

## Risk Tiers (decision framework)

| Semver jump | Default action | Gate |
|-------------|----------------|------|
| Patch `x.y.Z` | Batch | Tests green |
| Minor `x.Y.z` (well-behaved lib) | Batch | Tests green |
| Minor with deprecation notices | Isolate | Read changelog, tests green |
| Major `X.y.z` | Isolate, one commit | Read migration guide, code changes, tests green |
| Build tool / framework / test runner | Isolate, extra scrutiny | Migration guide + full build + smoke test |
| `0.y.z` libraries | Treat minor as major (0ver) | Read changelog |
| Has CVE/advisory | Front of queue, isolate | Verify advisory resolved post-upgrade |

See `references/breaking-changes.md` for ecosystem-specific breaking-change
patterns (peer deps, ESM/CJS, Python type stubs, Rust edition bumps, etc.).

## Commit message template

```
chore(deps): upgrade <package> from <old> to <new>

- <breaking change handled> / <reason>
- Changelog: <url>
- Resolves: <CVE-id or advisory>   # if applicable

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

## Best Practices
- Commit the lockfile in the same commit as the manifest change — never split.
- Keep manifest version ranges intentional; don't silently widen `^` to `*`.
- For monorepos, upgrade a package in one workspace, verify, then propagate.
- When a CVE has no fixed version yet, document the mitigation and the tracking
  issue rather than forcing an incompatible bump.
- Prefer the project's own scripts (`npm test`, `make test`) over guessing.
- If a Dependabot/Renovate PR exists, verify it: read the diff, run tests
  locally, check the changelog — don't merge on green CI alone for majors.

## Common Pitfalls
- **Bulk upgrading then having an opaque red suite** — you can't attribute the
  failure. Always isolate majors.
- **Skipping the changelog** and discovering a removed API at runtime, not
  build time.
- **Forgetting transitive/peer deps** — a major bump often demands its peers
  move too; the lockfile resolution may silently downgrade something.
- **Leaving the tree broken on a failed major** instead of rolling back.
- **Ignoring `0.x` semver semantics** — minor bumps there are breaking.
- **Regenerating the lockfile with a different package-manager version**,
  causing huge unintended churn. Pin the PM version.
- **Upgrading on a dirty tree**, making rollback ambiguous.

## Bundled files
- `references/ecosystems.md` — per-ecosystem commands: detect outdated, audit,
  upgrade, regenerate lockfile, run tests.
- `references/breaking-changes.md` — common breaking-change patterns and how to
  detect/handle them per ecosystem.
- `references/rollback.md` — precise rollback procedures (single upgrade, whole
  batch, lockfile-only) using git.
- `scripts/check_outdated.py` — auto-detecting outdated-dependency reporter with
  risk tiers; pure stdlib, shells out to native tools.
- `templates/upgrade-report.md` — fill-in final report.
- `examples/npm-major-upgrade.md` — worked example: a React major bump.
