---
name: update-github-actions-version
description: Update GitHub Actions versions in workflow files, focusing only on major version changes. Use when the user wants to update action versions, check for outdated GitHub Actions, or upgrade workflow dependencies to their latest major versions.
metadata:
  original-prompt: update-github-actions-version.prompt.md
---

# Update GitHub Actions Version

Update action versions in GitHub Actions workflow files, focusing on major version changes only.

## Important Principles: Explanation of GitHub Actions Version Tagging System

- Using a major version number (e.g., `v4`) automatically fetches the latest minor and patch versions.
- For example, `actions/checkout@v4` will automatically get versions like `v4.2.2`, `v4.3.0`.
- **Do not** update from `v4` to a specific version like `v4.2.2` — this is unnecessary.
- **Only update when the major version changes** (e.g., from `v5` to `v6`).

> **Note:** Skip `fatjyc/update-submodule-action@v6.0` updates as the new version is broken.

## Steps

### 0. Find Workflow Files
Look for files in `.github/workflows/` recursively. Note that composite actions may be used — read both the composite action and the calling workflow simultaneously.

### 1. Check Current Versions
Analyze the action versions used in the workflow files.

### 2. Query Latest Versions
Query each action's latest version:
```
https://github.com/{owner}/{repo}/releases/latest
```

### 3. Identify Actions Needing Updates
Only update actions where the major version has changed:
- ✅ Update: `docker/build-push-action@v5` → `@v6`
- ❌ Skip: `actions/checkout@v4` → `@v4.2.2`

> **Note:** Skip `fatjyc/update-submodule-action@v6.0` updates as the new version is broken and v6.0 is fine.

### 4. Obtain Changelogs
For actions requiring updates, retrieve changelogs to understand breaking changes.

### 5. Update Files
Update version numbers and make adjustments for any breaking changes.

### 6. Commit Changes
Git add and commit your changes with a clear message indicating the updates made.

## Example Illustration

### ✅ Correct Update

```yaml
# From
uses: docker/build-push-action@v5
# Update to 
uses: docker/build-push-action@v6
```

### ❌ Incorrect Update (Unnecessary)

```yaml
# From 
uses: actions/checkout@v4 
# Incorrectly updated to 
uses: actions/checkout@v4 .2 .2  
```

### ✅ Correct Practice (Keep Unchanged)

```yaml
# Keep unchanged 
uses :actions / checkout @ v 4  
GitHub will automatically use the latest v 4.x.x release   
```
