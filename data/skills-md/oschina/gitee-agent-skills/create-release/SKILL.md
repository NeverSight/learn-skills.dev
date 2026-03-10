---
name: create-release
description: Use this skill when the user asks to publish a release, create a release, "create release", "create-release", "tag a release", or generate a changelog. Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Create Release via Gitee MCP

Auto-generate a changelog from merged PR history and publish a well-structured release on Gitee.

## Prerequisites

- Gitee MCP Server configured (tools: `list_releases`, `list_repo_pulls`, `create_release`)
- User must provide: repository owner, repository name, version number
- Optional: previous version number (to determine the changelog range)

## Steps

### Step 1: Confirm the Version Number

Confirm the version number with the user, following Semantic Versioning:

```
vMAJOR.MINOR.PATCH

- MAJOR: incompatible API changes
- MINOR: backward-compatible new features
- PATCH: backward-compatible bug fixes
```

If the user hasn't provided one, suggest an appropriate version based on the nature of the changes.

### Step 2: Review Release History

Use `list_releases` to retrieve existing releases:
- Confirm the previous version number
- Understand the version naming convention (e.g., whether a `v` prefix is used)
- Avoid version number conflicts

### Step 3: Collect PR Changes

Use `list_repo_pulls` to get PRs merged since the last release:
- `state`: `merged`
- Sort by merge time, filtering for PRs after the last release

Classify each PR:
- `feat` / `feature`: new feature
- `fix` / `bugfix`: bug fix
- `refactor`: code refactoring
- `perf`: performance improvement
- `docs`: documentation update
- `chore`: dependency / build / toolchain changes
- `breaking`: breaking change (title contains `breaking` or `!:`)

### Step 4: Analyze Code Changes

As a supplement to PR titles, use `compare_branches_tags` to get a more detailed diff analysis:

```
compare_branches_tags(owner="[owner]", repo="[repo]", target="[current_branch]", base="[previous_version_tag]")
```

This returns:
- Files changed (added, modified, deleted)
- Commit history between versions
- Code statistics (additions, deletions)

Use this to understand the actual code changes behind each PR, especially useful when PR titles are unclear.

### Step 5: Generate Changelog

Generate the changelog using this template:

```markdown
## [v{version}] - YYYY-MM-DD

### ⚠️ Breaking Changes
- [PR title] (#PR number) @author

### ✨ New Features
- [PR title] (#PR number) @author
- [PR title] (#PR number) @author

### 🐛 Bug Fixes
- [PR title] (#PR number) @author

### ⚡ Performance
- [PR title] (#PR number) @author

### 📖 Documentation
- [PR title] (#PR number) @author

### 🔧 Other
- [PR title] (#PR number) @author

---

**Full changelog**: [link comparing previous version...current version]
```

Omit sections with no changes.

### Step 6: Confirm and Create the Release

Show the generated changelog to the user for confirmation. After confirmation, use `create_release` with these parameters:
- `tag_name`: version number (e.g., `v1.2.0`)
- `name`: release title (e.g., `Release v1.2.0`)
- `body`: changelog generated in Step 4
- `prerelease`: set to `true` for pre-release versions (alpha / beta / rc)

After successful creation, output the link to the Release page.

## Notes

- Use the `v` prefix in version numbers (e.g., `v1.2.0`) to match common project conventions
- Breaking changes must be prominently highlighted to warn users upgrading
- If PR titles are not semantic, lightly rephrase them in the changelog while preserving the original intent
- Pre-release versions (alpha / beta / rc) should be marked `prerelease=true` so they don't affect the stable release line
