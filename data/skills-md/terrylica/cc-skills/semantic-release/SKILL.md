---
name: semantic-release
description: Automate versioning with Node.js semantic-release v25+. TRIGGERS - npm run release, version bump, changelog, conventional commits, release automation.
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
disable-model-invocation: true
---

# semantic-release

## Overview

Automate semantic versioning and release management using **semantic-release v25+ (Node.js)** following 2025 best practices. Works with **all languages** (JavaScript, TypeScript, Python, Rust, Go, C++, etc.) via the `@semantic-release/exec` plugin. Create shareable configurations for multi-repository setups, initialize individual projects with automated releases, and configure GitHub Actions workflows with OIDC trusted publishing.

**Important**: This skill uses semantic-release (Node.js) exclusively, NOT python-semantic-release, even for Python projects. Rationale: 23.5x larger community, 100x+ adoption, better future-proofing.

## When to Use This Skill

Invoke when:

- Setting up local releases for a new project (any language)
- Creating shareable semantic-release configuration for organization-wide use
- Migrating existing projects to 2025 semantic-release patterns
- Troubleshooting semantic-release setup or version bumps
- Setting up Python projects (use Node.js semantic-release, NOT python-semantic-release)
- Configuring GitHub Actions (optional backup, not recommended as primary due to speed)
- Rust workspaces using release-plz (see [Rust reference](./references/rust.md))

## Why Node.js semantic-release

**22,900 GitHub stars** - Large, active community
**1.9M weekly downloads** - Proven adoption
**126,000 projects using it** - Battle-tested at scale
**35+ official plugins** - Rich ecosystem
**Multi-language support** - Works with any language via `@semantic-release/exec`

**Do NOT use python-semantic-release.** It has a 23.5x smaller community (975 vs 22,900 stars), ~100x less adoption, and is not affiliated with the semantic-release organization.

---

## Release Workflow Philosophy: Local-First

**Default approach: Run releases locally, not via GitHub Actions.**

### Why Local Releases

**Primary argument: GitHub Actions is slow**

- ⏱️ GitHub Actions: 2-5 minute wait for release to complete
- ⚡ Local release: Instant feedback and file updates
- 🔄 Immediate workflow continuity - no waiting for CI/CD

**Additional benefits:**

- ✅ **Instant local file sync** - `package.json`, `CHANGELOG.md`, tags updated immediately
- ✅ **No pull required** - Continue working without `git pull` after release
- ✅ **Dry-run testing** - `npm run release:dry` to preview changes before release
- ✅ **Offline capable** - Can release without CI/CD dependency
- ✅ **Faster iteration** - Debug release issues immediately, not through CI logs

### GitHub Actions: Optional Backup Only

GitHub Actions workflows are provided as **optional automation**, not the primary method:

- Use for team consistency if required
- Backup if local environment unavailable
- **Not recommended as primary workflow due to speed**

### Authentication Setup

```bash
gh auth login
# Browser authentication once
# Credentials stored in keyring
# All future releases: zero manual intervention
```

**This is the minimum manual intervention possible** for local semantic-release with GitHub plugin functionality.

### Multi-Account Authentication via mise [env]

For multi-account GitHub setups, use mise `[env]` to set per-directory GH_TOKEN:

```toml
# ~/your-project/.mise.toml
[env]
GH_TOKEN = "{{ read_file(path=env.HOME ~ '/.claude/.secrets/gh-token-accountname') | trim }}"
GITHUB_TOKEN = "{{ read_file(path=env.HOME ~ '/.claude/.secrets/gh-token-accountname') | trim }}"
```

This overrides gh CLI's global authentication, ensuring semantic-release uses the correct account for each directory.

See the [`mise-configuration` skill](../mise-configuration/SKILL.md#github-token-multi-account-patterns) for complete setup.

### mise Task Detection

When `.mise.toml` has release tasks, prefer `mise run` over `npm run`:

| Priority | Condition                            | Command                    |
| -------- | ------------------------------------ | -------------------------- |
| **1**    | `.mise.toml` has `[tasks.release:*]` | `mise run release:version` |
| **2**    | `package.json` has `scripts.release` | `npm run release`          |
| **3**    | Global semantic-release              | `semantic-release --no-ci` |

See [Python Guide](./references/python.md#mise-4-phase-workflow) for complete mise workflow example.

### GitHub Actions Policy

**CRITICAL: No testing or linting in GitHub Actions.** See CLAUDE.md for full policy.

| Forbidden                      | Allowed                |
| ------------------------------ | ---------------------- |
| pytest, npm test, cargo test   | semantic-release       |
| ruff, eslint, clippy, prettier | CodeQL, npm audit      |
| mypy                           | Deployment, Dependabot |

---

## Separation of Concerns (4-Level Architecture)

semantic-release configuration follows a hierarchical, composable pattern:

**Level 1: Skill** - `${CLAUDE_PLUGIN_ROOT}/skills/semantic-release/` (Generic templates, system-wide tool)
**Level 2: User Config** - `~/semantic-release-config/` (`@username/semantic-release-config`)
**Level 3: Organization Config** - npm registry (`@company/semantic-release-config`)
**Level 4: Project Config** - `.releaserc.yml` in project root

### Configuration Precedence

```
Level 4 (Project) → overrides → Level 3 (Org) → overrides → Level 2 (User) → overrides → Defaults
```

---

## Conventional Commits Format

semantic-release analyzes commit messages to determine version bumps:

```
<type>(<scope>): <subject>
```

### Version Bump Rules (Default)

- `feat:` → MINOR version bump (0.1.0 → 0.2.0)
- `fix:` → PATCH version bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` or `feat!:` → MAJOR version bump (0.1.0 → 1.0.0)
- `docs:`, `chore:`, `style:`, `refactor:`, `perf:`, `test:` → No version bump (by default)

### Release Notes Visibility (Important)

**Warning**: The `@semantic-release/release-notes-generator` (Angular preset) only includes these types in release notes:

- `feat:` → **Features** section
- `fix:` → **Bug Fixes** section
- `perf:` → **Performance Improvements** section

Other types (`docs:`, `chore:`, `refactor:`, etc.) trigger releases when configured but **do NOT appear in release notes**.

**Recommendation**: For documentation changes that should be visible in release notes, use:

```
fix(docs): description of documentation improvement
```

This ensures the commit appears in the "Bug Fixes" section while still being semantically accurate (fixing documentation gaps is a fix).

### Marketplace Plugin Configuration (Always Bump)

For Claude Code marketplace plugins, **every change requires a version bump** for users to receive updates.

**Option A: Shareable Config (if published)**

```yaml
# .releaserc.yml
extends: "@terryli/semantic-release-config/marketplace"
```

**Option B: Inline Configuration**

```yaml
# .releaserc.yml
plugins:
  - - "@semantic-release/commit-analyzer"
    - releaseRules:
        # Marketplace plugins require version bump for ANY change
        - { type: "docs", release: "patch" }
        - { type: "chore", release: "patch" }
        - { type: "style", release: "patch" }
        - { type: "refactor", release: "patch" }
        - { type: "test", release: "patch" }
        - { type: "build", release: "patch" }
        - { type: "ci", release: "patch" }
```

**Result after configuration:**

| Commit Type                                                        | Release Type       |
| ------------------------------------------------------------------ | ------------------ |
| `feat:`                                                            | minor (default)    |
| `fix:`, `perf:`, `revert:`                                         | patch (default)    |
| `docs:`, `chore:`, `style:`, `refactor:`, `test:`, `build:`, `ci:` | patch (configured) |

**Why marketplace plugins need this**: Plugin updates are distributed via version tags. Without a version bump, users running `/plugin update` see no changes even if content was modified.

### MANDATORY: Every Release Must Increment Version

**Pre-release validation**: Before running semantic-release, verify releasable commits exist since last tag. A release without version increment is invalid.

**Autonomous check sequence**:

1. List commits since last tag: compare HEAD against latest version tag
2. Identify commit types: scan for `feat:`, `fix:`, or `BREAKING CHANGE:` prefixes
3. If NO releasable commits found → **STOP** - do not proceed with release
4. Inform user: "No version-bumping commits since last release. Use `feat:` or `fix:` prefix for releasable changes."

**Commit type selection guidance**:

- Use `fix:` for any change that improves existing behavior (bug fixes, enhancements, documentation corrections that affect usage)
- Use `feat:` for new capabilities or significant additions
- Reserve `chore:`, `docs:`, `refactor:` for changes that truly don't warrant a release

**Why this matters**: A release without version increment creates confusion - users cannot distinguish between releases, package managers may cache old versions, and changelog entries become meaningless.

### MAJOR Version Breaking Change Confirmation

**Trigger**: `BREAKING CHANGE:` footer or `feat!:` / `fix!:` prefix in commits.

When MAJOR is detected, this skill runs a **3-phase confirmation workflow**:

1. **Detection**: Scan commits for breaking change markers
2. **Analysis**: Spawn 3 parallel subagents (User Impact, API Compat, Migration)
3. **Confirmation**: AskUserQuestion with proceed/downgrade/abort options

See [MAJOR Confirmation Workflow](./references/major-confirmation.md) for complete details including subagent prompts, decision tree, and example output.

### Examples

**Feature (MINOR)**:

```
feat: add BigQuery data source support
```

**Bug Fix (PATCH)**:

```
fix: correct timestamp parsing for UTC offsets
```

**Breaking Change (MAJOR)**:

```
feat!: change API to require authentication

BREAKING CHANGE: All API calls now require API key in Authorization header.
```

---

## Documentation Linking

Auto-include doc changes in release notes. Add to `.releaserc.yml`:

```yaml
- - "@semantic-release/exec"
  - generateNotesCmd: "node plugins/itp/skills/semantic-release/scripts/generate-doc-notes.mjs ${lastRelease.gitTag}"
```

Detects: ADRs, Design Specs, Skills, Plugin READMEs. See [Doc Release Linking](./references/doc-release-linking.md).

> **Note**: The `@semantic-release/exec` plugin uses Lodash templates (`${var}`). This conflicts with bash default syntax (`${VAR:-default}`) and subshell syntax (`$(cmd)`). **Preferred fix**: remove `successCmd` entirely if your task runner already handles post-release steps. See [Troubleshooting: Lodash Template Conflicts](./references/troubleshooting.md#semantic-releaseexec-lodash-template-conflicts).

---

## Quick Start

### Prerequisites

| Check                   | Command                       | Fix                                                                                       |
| ----------------------- | ----------------------------- | ----------------------------------------------------------------------------------------- |
| gh CLI authenticated    | `gh auth status`              | `gh auth login`                                                                           |
| GH_TOKEN for directory  | `gh api user --jq '.login'`   | See [Authentication](./references/authentication.md)                                      |
| Git remote is HTTPS     | `git remote get-url origin`   | `git-ssh-to-https`                                                                        |
| semantic-release global | `command -v semantic-release` | See [Troubleshooting](./references/troubleshooting.md#macos-gatekeeper-blocks-node-files) |

### Initialize Project

```bash
./scripts/init-project.mjs --project   # Initialize current project
./scripts/init-project.mjs --user      # Create user-level shareable config
./scripts/init-project.mjs --help      # See all options
```

### Run Release

| Priority | Condition                      | Commands                                             |
| -------- | ------------------------------ | ---------------------------------------------------- |
| **1**    | `.mise.toml` has release tasks | `mise run release:version` / `mise run release:full` |
| **2**    | `package.json` has scripts     | `npm run release:dry` (preview) / `npm run release`  |
| **3**    | Global CLI                     | `semantic-release --no-ci`                           |

See [Local Release Workflow](./references/local-release-workflow.md) for the complete 4-phase process.

### Python Projects

semantic-release handles versioning. For PyPI publishing, see [`pypi-doppler` skill](../pypi-doppler/SKILL.md).

**Version pattern** (importlib.metadata - never hardcode):

```python
from importlib.metadata import PackageNotFoundError, version
try:
    __version__ = version("your-package-name")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"
```

See [Python Projects Guide](./references/python.md) for complete setup including Rust+Python hybrids.

### GitHub Actions (Optional)

Not recommended as primary (2-5 minute delay). Repository Settings → Actions → Workflow permissions → Enable "Read and write permissions".

---

## Reference Documentation

| Category      | Reference                                                        | Description                                              |
| ------------- | ---------------------------------------------------------------- | -------------------------------------------------------- |
| **Setup**     | [Authentication](./references/authentication.md)                 | HTTPS-first setup, multi-account patterns                |
| **Workflow**  | [Local Release Workflow](./references/local-release-workflow.md) | 4-phase process (PREFLIGHT → RELEASE → POSTFLIGHT)       |
| **Languages** | [Python Projects](./references/python.md)                        | Python + Rust+Python hybrid patterns                     |
|               | [Rust Projects](./references/rust.md)                            | release-plz, cargo-rdme README SSoT                      |
| **Config**    | [Version Alignment](./references/version-alignment.md)           | Git tags as SSoT, manifest patterns                      |
|               | [Monorepo Support](./references/monorepo-support.md)             | Polyglot monorepo with Pants + mise, pnpm/npm workspaces |
| **Advanced**  | [MAJOR Confirmation](./references/major-confirmation.md)         | Breaking change analysis workflow                        |
|               | [Doc Release Linking](./references/doc-release-linking.md)       | Auto-link ADRs/specs in release notes                    |
| **Help**      | [Troubleshooting](./references/troubleshooting.md)               | All common issues consolidated                           |
|               | [Evolution Log](./references/evolution-log.md)                   | Skill change history                                     |

**Cross-skill references**:

- [`mise-tasks` skill: polyglot-affected](../mise-tasks/references/polyglot-affected.md) - Complete Pants + mise integration guide
- [`mise-tasks` skill: bootstrap-monorepo](../mise-tasks/references/bootstrap-monorepo.md) - Autonomous polyglot monorepo setup
- [`pypi-doppler` skill](../pypi-doppler/SKILL.md) - Local PyPI publishing with Doppler

---

## Post-Change Checklist

After modifying THIS skill (semantic-release):

1. [ ] SKILL.md and references remain aligned
2. [ ] New references documented in Reference Documentation table
3. [ ] All referenced files in references/ exist
4. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)
5. [ ] Validate with `bun scripts/validate-plugins.mjs`
6. [ ] Run `npm run release:dry` to verify no regressions

---

## Troubleshooting

| Issue                        | Cause                           | Solution                                                 |
| ---------------------------- | ------------------------------- | -------------------------------------------------------- |
| No release created           | No releasable commits since tag | Use `feat:` or `fix:` prefix for version-bumping commits |
| Wrong version bump           | Commit type mismatch            | Check conventional commit format and releaseRules        |
| GitHub release not created   | Missing GH_TOKEN or permissions | Check token is set and has repo scope                    |
| CHANGELOG not updated        | Missing changelog plugin        | Add `@semantic-release/changelog` to plugins array       |
| "Authentication failed"      | HTTPS vs SSH remote mismatch    | Convert to HTTPS: `git-ssh-to-https`                     |
| semantic-release not found   | Not installed globally          | `npm install -g semantic-release`                        |
| Gatekeeper blocks on macOS   | Unsigned Node files             | See [Troubleshooting](./references/troubleshooting.md)   |
| dry-run shows no changes     | Already released at HEAD        | Make new commits before running release                  |
| Multi-account token conflict | Wrong GH_TOKEN for directory    | Configure mise [env] per-directory token                 |
