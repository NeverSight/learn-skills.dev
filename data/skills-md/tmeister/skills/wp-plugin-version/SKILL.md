---
name: wp-plugin-version
description: Analyze changes and update WordPress plugin version references safely.
---

# WordPress Plugin Version

Use this skill to suggest and apply semantic version updates for a WordPress plugin.

## Inputs

- Optional: action (analyze, update, list files), target version.
- If no action is provided, start with analysis and recommend a version.

## Safety Rules

- Ask before modifying files.
- Update only version references that match the current version.
- Do not commit or tag; the user decides when to commit.

## Workflow

1. **Identify the main plugin file**
   - Look for a PHP file in repo root containing a `Plugin Name:` header.
   - If multiple candidates exist, ask the user to choose.

2. **Read current version**
   - Extract `Version:` from the plugin header.
   - Warn if it is not in MAJOR.MINOR.PATCH format.

3. **Analyze changes**
   - Prefer comparing against the latest version tag when available.
   - If no tags exist, compare against the default branch.
   - Recommend a SemVer bump:
     - MAJOR: removed or breaking public APIs, hooks, or behavior.
     - MINOR: new features, new hooks/endpoints, backward compatible.
     - PATCH: bug fixes, internal improvements.

4. **List version references**
   - Search for the current version string across plugin files and docs.
   - Present the list for confirmation.

5. **Update version**
   - Propose the new version and ask for confirmation.
   - Update:
     - Main plugin header `Version:`
     - Any defined version constants
     - readme.txt and README files
     - package.json if present
   - Keep changes minimal and review with `git diff`.

6. **Report**
   - Summarize files updated and next steps.
   - Suggest running `/wp-plugin-changelog` and `/wp-plugin-tag` when ready.

## Output Template

Use the summary template when reporting changes.
