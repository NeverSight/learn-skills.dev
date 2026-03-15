---
name: release
description: >
  Manages package release workflows for npm, Python, and Go ecosystems.
  Detects project type from manifest files, bumps versions, transforms
  changelogs (Keep a Changelog format), creates git commits and tags,
  and optionally generates CI publishing workflows. Use when releasing
  packages, cutting versions, publishing to registries, bumping versions,
  or setting up release infrastructure.
---

# Release

One command to release any package. Detects your ecosystem, bumps the version,
updates the changelog, commits, tags, pushes, and watches CI.

## Commands

| Command | What it does |
|---------|-------------|
| `/release patch` | Bump patch version and release |
| `/release minor` | Bump minor version and release |
| `/release major` | Bump major version and release |
| `/release alpha` | Create alpha pre-release |
| `/release beta` | Create beta pre-release |
| `/release rc` | Create release candidate |
| `/release context` | Show version, commits, changelog status (read-only) |
| `/release dry` | Simulate a release without mutations |
| `/release setup-ci` | Generate CI/CD workflow files |

---

## Step 1: Parse Arguments

Determine the release type from the invocation:

- `patch`, `minor`, `major` → stable release
- `alpha`, `beta`, `rc` → pre-release
- `context` → read-only status
- `dry` → dry run simulation
- `setup-ci` → CI workflow generation
- No argument → show this command reference and stop

---

## Step 2: Detect Ecosystem

Scan the project root for manifest files to determine the ecosystem:

| File present | Ecosystem | Next step |
|-------------|-----------|-----------|
| `package.json` with a `version` field | **npm** | Read [adapters/npm.md](adapters/npm.md) |
| `pyproject.toml` | **Python** | Not yet supported — print message and stop |
| `go.mod` | **Go** | Not yet supported — print message and stop |
| None of the above | **Unknown** | Print: "Unsupported project type. This skill supports: npm (now), Python and Go (coming soon)." and stop |

For the **npm** ecosystem, also detect the package manager:

| Lock file present | Package manager |
|-------------------|----------------|
| `bun.lock` or `bun.lockb` | bun |
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn |
| `package-lock.json` | npm |
| None of the above | npm (default) |

If multiple lock files exist, use the highest match from the table (top = highest priority) and note the conflict to the user.

### Guard Rails

Before proceeding, check for known unsupported configurations:

1. Read `package.json` and check for a `workspaces` field. If present:
   - Print: "Monorepo detected (`workspaces` field found). This skill supports single-package repos only. For monorepos, see changesets or release-please."
   - Stop.

2. Check for `"private": true` in `package.json`. If present:
   - Print: "Note: Package is marked `private`. Publishing will be skipped, but version bumping, changelog management, and tagging will still work."
   - Continue (do not stop).

---

## Step 3: Check Infrastructure

Before routing to a flow, check what infrastructure exists:

1. **CHANGELOG.md** — Does it exist? Does it contain `## [Unreleased]` (case-insensitive)?
2. **Pre-push hook** — Does `.git/hooks/pre-push` exist and contain release validation?
3. **CI workflows** — Does `.github/workflows/` contain a file with `npm publish` or a publish step?

If the command is `context`, just report what's missing — don't offer to create anything.

For all other commands, if CHANGELOG.md is missing or has no `[Unreleased]` section:
- Route to [flows/init.md](flows/init.md) to bootstrap before continuing.

After init completes, note missing infrastructure (hook, CI) to offer at the end of the release.

---

## Step 4: Route to Flow

Load the adapter file and the appropriate flow file based on the command:

### Stable Release (`patch`, `minor`, `major`)

1. Read [adapters/npm.md](adapters/npm.md) for ecosystem-specific commands
2. Follow [flows/release.md](flows/release.md) for the 10-step release flow

### Pre-Release (`alpha`, `beta`, `rc`)

1. Read [adapters/npm.md](adapters/npm.md) for ecosystem-specific commands
2. Follow [flows/pre-release.md](flows/pre-release.md) for the pre-release flow

### Context

1. Read [adapters/npm.md](adapters/npm.md) for `read_version`
2. Follow [flows/context.md](flows/context.md) for the status report

### Dry Run

1. Read [adapters/npm.md](adapters/npm.md) for ecosystem-specific commands
2. Follow [flows/dry-run.md](flows/dry-run.md) for the simulation flow

### Setup CI

1. Read [adapters/npm.md](adapters/npm.md) for template selection
2. Follow [flows/setup-ci.md](flows/setup-ci.md) for CI workflow generation

---

## Step 5: Post-Release Offers

After a successful stable release (push completed), check and offer:

1. **Pre-push hook not installed?** → "Would you like to install a pre-push hook to validate releases? It checks that tag versions match your package.json and changelog."

2. **No CI publish workflow?** → Check if the remote contains `github.com`. If yes: "Would you like to generate GitHub Actions workflows for CI and automated publishing? Run `/release setup-ci`." If not on GitHub: "No CI publish workflow detected. `/release setup-ci` can generate GitHub Actions workflows if needed, but note that only GitHub Actions is supported at this time."

These are suggestions only — never install automatically without confirmation.

---

## Rollback

If anything goes wrong during a release, see [reference/rollback.md](reference/rollback.md) for exact recovery commands for every failure scenario.

---

## Design Principles

- **Human-written changelogs.** The skill manages the format; you write the content.
- **Confirm before push.** Every release shows a summary and waits for explicit approval.
- **Ecosystem adapters.** Same flow, different commands. Adding a new ecosystem is one file.
- **Graceful degradation.** Network-dependent steps (push, CI watch) degrade cleanly when unavailable. Steps 1–8 work with just filesystem and git.
- **No tool-specific instructions.** Commands use standard bash — works with any agent that can run shell commands.
