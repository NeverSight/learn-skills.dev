---
name: publish
description: Publish a new version of klaude-code to PyPI. This skill handles version bumping, changelog updates, git tagging, and package publishing. Use when the user wants to release a new version.
---

# Publish Skill

This skill manages the release process for klaude-code, including version management, changelog updates, git tagging, and PyPI publishing.

## Prerequisites

- `UV_PUBLISH_TOKEN` environment variable must be set for PyPI publishing
- `pnpm` must be available to build the bundled web frontend before release
- Working directory must be the klaude-code repository root
- Git repository must be clean (no uncommitted changes)
- Git submodules must be initialized and up-to-date (`src/klaude_code/skill/assets`)

Before starting the release workflow, run:

```bash
git submodule sync --recursive
git submodule update --init --recursive
```

## Release Workflow

### Step 1: Determine Version Bump Type

Ask the user which version bump type to apply:
- `major` - Breaking changes (X.0.0)
- `minor` - New features, backwards compatible (x.Y.0)
- `patch` - Bug fixes, backwards compatible (x.y.Z)

### Step 2: Run Version Bump Script

Execute the version bump script to update `pyproject.toml`:

```bash
uv run .claude/skills/publish/scripts/bump_version.py <bump_type>
```

The script will:
1. Read current version from `pyproject.toml`
2. Calculate new version based on bump type
3. Update `pyproject.toml` with new version
4. Output the old and new version numbers

### Step 3: Update CHANGELOG.md

Execute the changelog update script:

```bash
uv run .claude/skills/publish/scripts/update_changelog.py <new_version>
```

The script will:
1. Get commits since the last tag
2. Categorize commits by type (feat, fix, refactor, etc.)
3. Update CHANGELOG.md with the new version section
4. Move [Unreleased] changes to the new version

### Step 4: Commit and Tag

This project uses jj (Jujutsu) in colocated mode with git. Create a release commit and tag:

```bash
# Describe current change as release commit
jj describe -m "chore(release): v<new_version>"

# Create new empty change for future work
jj new

# Get the git commit id of the release commit (jj's @- syntax doesn't work with git)
jj log -r @- -T 'commit_id' --no-graph

# Create tag using the git commit id
git tag v<new_version> <commit_id>
```

### Step 5: Push Changes

Push the commit and tag to remote:

```bash
# Move main bookmark to the release commit, then push
jj bookmark set main -r @-
jj git push

# Push the tag
git push origin v<new_version>

# Ensure submodule commit is reachable to other environments
git submodule update --init --recursive
```

### Step 6: Build and Publish

Build the frontend, verify the wheel bundles the web assets and system skill assets, then publish to PyPI:

```bash
pnpm --dir web install --frozen-lockfile
pnpm --dir web build

uv build

uv run python - <<'PY'
from pathlib import Path
from zipfile import ZipFile

wheel = sorted(Path("dist").glob("*.whl"))[-1]
with ZipFile(wheel) as archive:
    names = set(archive.namelist())

required = {
    "klaude_code/web/dist/index.html",
    "klaude_code/skill/assets/web-search/SKILL.md",
}
missing = sorted(required - names)
if missing:
    raise SystemExit(f"Wheel is missing bundled assets: {', '.join(missing)}")

print(f"Verified bundled web + skill assets in {wheel.name}")
PY

uv publish
```

Do not publish if the wheel verification fails. That means the package build no longer includes required bundled assets (web or skills).

## Error Handling

- If git working directory is dirty, prompt user to commit or stash changes first
- If UV_PUBLISH_TOKEN is not set, warn user before publishing step
- If any step fails, provide clear error message and recovery instructions

## Scripts

- `scripts/bump_version.py` - Handles semantic version bumping
- `scripts/update_changelog.py` - Updates CHANGELOG.md with commits since last tag
