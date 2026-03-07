---
name: pypi-doppler
description: LOCAL-ONLY PyPI publishing with Doppler credentials. TRIGGERS - publish to PyPI, pypi upload, local publish. NEVER use in CI/CD.
allowed-tools: Bash, Read
---

# PyPI Publishing with Doppler (Local-Only)

## When to Use This Skill

Use this skill when:

- Publishing Python packages to PyPI from local machine
- Setting up Doppler for PyPI token management
- Creating local publish scripts with CI detection guards
- Validating repository ownership before release

## WORKSPACE-WIDE POLICY: LOCAL-ONLY PUBLISHING

**This skill supports LOCAL machine publishing ONLY.**

### FORBIDDEN

- Publishing from GitHub Actions
- Publishing from any CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins, CircleCI)
- `publishCmd` in semantic-release configuration
- Building packages in CI (`uv build` in prepareCmd)
- Storing PyPI tokens in GitHub secrets

### REQUIRED

- Use `scripts/publish-to-pypi.sh` on local machine
- CI detection guards in publish script
- Manual approval before each release
- Doppler credential management (no plaintext tokens)
- Repository verification (prevents fork abuse)

### Rationale

- **Security**: No long-lived PyPI tokens in GitHub secrets
- **Speed**: 30 seconds locally vs 3-5 minutes in CI
- **Control**: Manual approval step before production release
- **Flexibility**: Centralized credential management via Doppler

**See**: ADR-0027, `docs/development/PUBLISHING.md`

---

## Overview

This skill provides **local-only PyPI publishing** using Doppler for secure credential management. It integrates with the workspace-wide release workflow where:

1. **GitHub Actions**: Automated versioning ONLY (tags, releases, CHANGELOG)
2. **Local Machine**: Manual PyPI publishing with Doppler credentials

## Bundled Scripts

| Script                                                       | Purpose                                        |
| ------------------------------------------------------------ | ---------------------------------------------- |
| [`scripts/publish-to-pypi.sh`](./scripts/publish-to-pypi.sh) | Local PyPI publishing with CI detection guards |

**Usage**: Copy to your project's `scripts/` directory:

```bash
/usr/bin/env bash << 'DOPPLER_EOF'
# Environment-agnostic path
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}"
cp "$PLUGIN_DIR/skills/pypi-doppler/scripts/publish-to-pypi.sh" scripts/
chmod +x scripts/publish-to-pypi.sh
DOPPLER_EOF
```

---

## Prerequisites

### One-Time Setup

1. **Install Doppler CLI**:

   ```bash
   brew install dopplerhq/cli/doppler
   ```

2. **Authenticate with Doppler**:

   ```bash
   doppler login
   ```

3. **Verify access to `claude-config` project**:

   ```bash
   doppler whoami
   doppler projects
   ```

### PyPI Token Setup

1. **Create PyPI API token**:
   - Visit: <https://pypi.org/manage/account/token/>
   - Enable 2FA if not already enabled (required since 2024)
   - Create token with scope: "Entire account" or specific project
   - Copy token (starts with `pypi-AgEIcHlwaS5vcmc...`, ~180 characters)

2. **Store token in Doppler**:

   ```bash
   doppler secrets set PYPI_TOKEN='pypi-AgEIcHlwaS5vcmc...' \
     --project claude-config \
     --config prd
   ```

3. **Verify token stored**:

   ```bash
   doppler secrets get PYPI_TOKEN \
     --project claude-config \
     --config prd \
     --plain
   ```

---

## Publishing Workflow

### MANDATORY: Verify Version Increment Before Publishing

**Pre-publish validation**: Before publishing to PyPI, verify that the version has incremented from the previous release. Publishing without a version increment is invalid and wastes resources.

**Autonomous check sequence**:

1. Compare local `pyproject.toml` version against latest PyPI version
2. If versions match -- **STOP** - do not proceed with publishing
3. Inform user: "Version not incremented. Run semantic-release first or verify commits include `feat:` or `fix:` types."

### Complete Release Workflow

**Step 1: Development & Commit** (Conventional Commits):

```bash
git add .
git commit -m "feat: add new feature"  # MINOR bump
git push origin main
```

**Step 2: Automated Versioning** (GitHub Actions - 40-60s):

GitHub Actions automatically: analyzes commits, determines next version, updates `pyproject.toml`/`package.json`, generates CHANGELOG, creates git tag, creates GitHub release.

**PyPI publishing does NOT happen here** (by design - see ADR-0027).

**Step 3: Local PyPI Publishing** (30 seconds):

```bash
git pull origin main
./scripts/publish-to-pypi.sh
```

### Using Bundled Script (Recommended)

```bash
/usr/bin/env bash << 'GIT_EOF'
# First time: copy script from skill to your project (environment-agnostic)
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/itp}"
cp "$PLUGIN_DIR/skills/pypi-doppler/scripts/publish-to-pypi.sh" scripts/
chmod +x scripts/publish-to-pypi.sh

# After semantic-release creates GitHub release
git pull origin main

# Publish using local copy of bundled script
./scripts/publish-to-pypi.sh
GIT_EOF
```

**Bundled script features**: CI detection guards, repository verification, Doppler integration, build + publish + verify workflow, clear error messages.

### Manual Publishing (Advanced)

For manual publishing without the canonical script:

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# Retrieve token from Doppler
PYPI_TOKEN=$(doppler secrets get PYPI_TOKEN \
  --project claude-config \
  --config prd \
  --plain)

# Build package
uv build

# Publish to PyPI
UV_PUBLISH_TOKEN="${PYPI_TOKEN}" uv publish
CONFIG_EOF
```

**WARNING**: Manual publishing bypasses CI detection guards and repository verification. Use canonical script unless you have a specific reason not to.

---

## Reference Documentation

| Topic                 | Reference                                                           |
| --------------------- | ------------------------------------------------------------------- |
| CI Detection          | [CI Detection Enforcement](./references/ci-detection.md)            |
| Credential Management | [Doppler & Token Management](./references/credential-management.md) |
| Troubleshooting       | [Troubleshooting Guide](./references/troubleshooting.md)            |
| TestPyPI Testing      | [TestPyPI Testing](./references/testpypi-testing.md)                |
| mise Task Integration | [mise Task Integration](./references/mise-task-integration.md)      |

---

## Related Documentation

- **ADR-0027**: `docs/architecture/decisions/0027-local-only-pypi-publishing.md` - Architectural decision for local-only publishing
- **ADR-0028**: `docs/architecture/decisions/0028-skills-documentation-alignment.md` - Skills alignment with ADR-0027
- **PUBLISHING.md**: `docs/development/PUBLISHING.md` - Complete release workflow guide
- **semantic-release Skill**: [`semantic-release`](../semantic-release/SKILL.md) - Versioning automation (NO publishing)
- **mise-tasks Skill**: [`mise-tasks`](../mise-tasks/SKILL.md) - Task orchestration with dependency management
- **Release Workflow Patterns**: [`release-workflow-patterns.md`](../mise-tasks/references/release-workflow-patterns.md) - DAG patterns and anti-patterns
- **Bundled Script**: [`scripts/publish-to-pypi.sh`](./scripts/publish-to-pypi.sh) - Reference implementation with CI guards

---

## Validation History

- **2025-12-03**: Refactored to discovery-first, environment-agnostic approach
  - `discover_uv()` checks PATH, direct installs, version managers (priority order)
  - Supports: curl install, Homebrew, cargo, mise, asdf - doesn't force any method
- **2025-11-22**: Created with ADR-0027 alignment (workspace-wide local-only policy)
- **Validation**: CI detection guards tested, Doppler integration verified

---

**Last Updated**: 2025-12-03
**Policy**: Workspace-wide local-only PyPI publishing (ADR-0027)
**Supersedes**: None (created with ADR-0027 compliance from start)
