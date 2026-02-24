---
name: actions-updater
description: This skill should be used when the user asks to "update GitHub Actions", "check for action updates", "upgrade workflow actions", "update actions to latest version", "replace dependabot for actions", "check for outdated actions", or wants to find outdated GitHub Actions in workflow files and update them to the latest release versions.
version: 0.1.0
---

# GitHub Actions Version Updater

Update GitHub Actions in workflow files to their latest released versions. This replaces Dependabot's `package-ecosystem: "github-actions"` functionality.

## Process

### Step 1: Check for Updates

Run the bundled script to parse all `uses:` lines and query each action's latest release:

    uv run actions-updater/scripts/check_updates.py

With no arguments, the script scans `.github/workflows/*.yml` and `*.yaml`. To check specific files:

    uv run actions-updater/scripts/check_updates.py path/to/workflow.yaml

The script parses workflow YAML, recursively extracts all `uses: owner/repo@version` entries, queries `gh release view --repo owner/repo` for each, and outputs a comparison table showing the current and latest major versions. It skips local actions (`./...`) and Docker actions (`docker://...`).

### Step 2: Update Workflow Files

For each action with an available update, edit the workflow file using the Edit tool.

**Version format rules:**
- If the current pin is a major version tag (e.g., `@v3`), extract the major version from the latest release tag and update to that (e.g., `v4.2.1` becomes `@v4`)
- If the current pin is an exact version (e.g., `@v3.1.0`), update to the full latest release tag
- If the current pin is a SHA, flag it for the user but do not auto-update

### Step 3: Summarize

Present a table of all updates applied, showing the action, old version, and new version.

## Scripts

### `scripts/check_updates.py`

Check all workflow actions for available updates. Requires authenticated `gh` CLI.

    uv run scripts/check_updates.py                      # scans .github/workflows/
    uv run scripts/check_updates.py path/to/ci.yaml      # specific file(s)
