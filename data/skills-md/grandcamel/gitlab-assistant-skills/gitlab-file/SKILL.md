---
name: "gitlab-file"
description: "GitLab repository file operations via API. ALWAYS use this skill when user wants to: (1) read file content from GitLab, (2) create/update/delete files via API, (3) get file blame info, (4) download raw files."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# File Skill

Repository file operations for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| Get file info | `glab api projects/:id/repository/files/:path?ref=:branch` | - |
| Get raw content | `glab api projects/:id/repository/files/:path/raw?ref=:branch` | - |
| Get blame | `glab api projects/:id/repository/files/:path/blame?ref=:branch` | - |
| Create file | `glab api projects/:id/repository/files/:path -X POST -f ...` | ⚠️ |
| Update file | `glab api projects/:id/repository/files/:path -X PUT -f ...` | ⚠️ |
| Delete file | `glab api projects/:id/repository/files/:path -X DELETE -f ...` | ⚠️⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to read file content from GitLab (not local)
- User wants to create/update/delete files via GitLab API
- User needs file blame information
- User wants to download raw file content
- User mentions "repository file", "blob", "raw content"

**NEVER use when:**
- User wants to edit local files (use file editing tools)
- User wants to search code (use gitlab-search)
- User wants to browse repository tree (use gitlab-repo)
- User wants to commit multiple files (use git locally)

## API Prerequisites

**Required Token Scopes:** `api`

**Permissions:**
- Read files: Reporter+ (for private repos)
- Create/update/delete files: Developer+ (need push access)

## URL Encoding

File paths must be URL-encoded. Slashes in paths become `%2F`:

```bash
# src/main.py -> src%2Fmain.py
echo 'src/main.py' | jq -Rr @uri
# Output: src%2Fmain.py
```

## Available Commands

### Get File Info (Base64 Encoded)

```bash
# Get file metadata and content (base64)
glab api "projects/123/repository/files/README.md?ref=main" --method GET

# With URL-encoded path
glab api "projects/123/repository/files/$(echo 'src/main.py' | jq -Rr @uri)?ref=main"

# From specific branch
glab api "projects/123/repository/files/config.json?ref=develop" --method GET

# From tag
glab api "projects/123/repository/files/version.txt?ref=v1.0.0" --method GET

# From commit SHA
glab api "projects/123/repository/files/app.py?ref=abc123" --method GET
```

**Response includes:**
- `file_name` - File name
- `file_path` - Full path
- `size` - File size in bytes
- `encoding` - Content encoding (base64)
- `content` - Base64-encoded content
- `content_sha256` - SHA256 hash
- `ref` - Branch/tag/commit
- `blob_id` - Blob SHA
- `commit_id` - Last commit SHA
- `last_commit_id` - Same as commit_id

### Decode Base64 Content

```bash
# Get and decode file content
glab api "projects/123/repository/files/README.md?ref=main" | \
  jq -r '.content' | base64 -d
```

### Get Raw File Content

```bash
# Get raw file content (not base64)
glab api "projects/123/repository/files/README.md/raw?ref=main" --method GET

# With encoded path
glab api "projects/123/repository/files/$(echo 'src/app.py' | jq -Rr @uri)/raw?ref=main"

# Binary file (save to file)
glab api "projects/123/repository/files/$(echo 'images/logo.png' | jq -Rr @uri)/raw?ref=main" > logo.png
```

### Get File Blame

```bash
# Get blame information
glab api "projects/123/repository/files/$(echo 'src/main.py' | jq -Rr @uri)/blame?ref=main" --method GET

# Parse blame output
glab api "projects/123/repository/files/$(echo 'src/main.py' | jq -Rr @uri)/blame?ref=main" | \
  jq -r '.[] | "\(.commit.author_name): lines \(.lines | length)"'
```

### Create File

```bash
# Create new file with content
glab api "projects/123/repository/files/$(echo 'docs/new-file.md' | jq -Rr @uri)" --method POST \
  -f branch="main" \
  -f content="# New File\n\nContent here" \
  -f commit_message="Add new documentation file"

# Create with base64 content
glab api "projects/123/repository/files/$(echo 'data/config.json' | jq -Rr @uri)" --method POST \
  -f branch="main" \
  -f content="$(cat config.json | base64)" \
  -f encoding="base64" \
  -f commit_message="Add configuration file"

# Create on new branch
glab api "projects/123/repository/files/$(echo 'feature/new.txt' | jq -Rr @uri)" --method POST \
  -f branch="feature-branch" \
  -f start_branch="main" \
  -f content="Feature content" \
  -f commit_message="Add feature file"

# Create with author info
glab api "projects/123/repository/files/script.sh" --method POST \
  -f branch="main" \
  -f content="#!/bin/bash\necho Hello" \
  -f commit_message="Add script" \
  -f author_email="dev@example.com" \
  -f author_name="Developer"
```

### Update File

```bash
# Update file content
glab api "projects/123/repository/files/README.md" --method PUT \
  -f branch="main" \
  -f content="# Updated README\n\nNew content here" \
  -f commit_message="Update README"

# Update with base64 (for binary or complex files)
glab api "projects/123/repository/files/$(echo 'config/settings.json' | jq -Rr @uri)" --method PUT \
  -f branch="main" \
  -f content="$(cat settings.json | base64)" \
  -f encoding="base64" \
  -f commit_message="Update settings"

# Update on feature branch
glab api "projects/123/repository/files/src%2Fapp.py" --method PUT \
  -f branch="feature-update" \
  -f content="$(cat app.py | base64)" \
  -f encoding="base64" \
  -f commit_message="Refactor app module"

# Update with last known commit (for conflict detection)
glab api "projects/123/repository/files/data.json" --method PUT \
  -f branch="main" \
  -f content="{ \"updated\": true }" \
  -f commit_message="Update data" \
  -f last_commit_id="abc123def456"
```

### Delete File

```bash
# Delete file
glab api "projects/123/repository/files/$(echo 'old-file.txt' | jq -Rr @uri)" --method DELETE \
  -f branch="main" \
  -f commit_message="Remove deprecated file"

# Delete with author info
glab api "projects/123/repository/files/$(echo 'temp/test.txt' | jq -Rr @uri)" --method DELETE \
  -f branch="main" \
  -f commit_message="Clean up temp files" \
  -f author_email="dev@example.com" \
  -f author_name="Developer"
```

## File Operation Options

| Option | Type | Description |
|--------|------|-------------|
| `branch` | string | Target branch (required for write ops) |
| `start_branch` | string | Source branch for new files |
| `content` | string | File content (plain text or base64) |
| `encoding` | string | Content encoding: `text` (default) or `base64` |
| `commit_message` | string | Commit message (required for write ops) |
| `author_email` | string | Custom author email |
| `author_name` | string | Custom author name |
| `last_commit_id` | string | Expected last commit (for conflict detection) |

## Common Workflows

### Workflow 1: Download and View File

```bash
# Get file content
glab api "projects/123/repository/files/$(echo 'config/app.yml' | jq -Rr @uri)/raw?ref=main"
```

### Workflow 2: Update Configuration File

```bash
# 1. Download current file
glab api "projects/123/repository/files/config.json/raw?ref=main" > config.json

# 2. Edit locally
# ... make changes to config.json ...

# 3. Upload updated file
glab api "projects/123/repository/files/config.json" --method PUT \
  -f branch="main" \
  -f content="$(cat config.json | base64)" \
  -f encoding="base64" \
  -f commit_message="Update configuration"
```

### Workflow 3: Create File on Feature Branch

```bash
# Create new file on new branch
glab api "projects/123/repository/files/$(echo 'docs/feature.md' | jq -Rr @uri)" --method POST \
  -f branch="feature-docs" \
  -f start_branch="main" \
  -f content="# Feature Documentation\n\nDetails here..." \
  -f commit_message="Add feature documentation"
```

### Workflow 4: Check File History via Blame

```bash
# Get blame info for a file
glab api "projects/123/repository/files/$(echo 'src/critical.py' | jq -Rr @uri)/blame?ref=main" | \
  jq -r '.[] | "\(.commit.short_id) \(.commit.author_name): \(.lines | length) lines"'
```

### Workflow 5: Batch Read Multiple Files

```bash
# Read multiple files
for file in "README.md" "package.json" "Dockerfile"; do
  echo "=== $file ==="
  glab api "projects/123/repository/files/$(echo "$file" | jq -Rr @uri)/raw?ref=main"
  echo ""
done
```

### Workflow 6: Copy File Between Branches

```bash
# 1. Get file from source branch
content=$(glab api "projects/123/repository/files/config.json/raw?ref=develop")

# 2. Create/update on target branch
echo "$content" | base64 > /tmp/content.b64
glab api "projects/123/repository/files/config.json" --method PUT \
  -f branch="main" \
  -f content="$(cat /tmp/content.b64)" \
  -f encoding="base64" \
  -f commit_message="Sync config from develop"
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | File doesn't exist | Verify path and branch |
| 400 Path encoding | Slashes not encoded | Use `jq -Rr @uri` to encode |
| Binary content garbled | Not using base64 | Use `/raw` endpoint or decode base64 |
| Conflict on update | File changed | Use `last_commit_id` for optimistic locking |
| 403 Forbidden | No push access | Need Developer+ role |
| Large file fails | Size limit | GitLab has file size limits |

## Size Limits

- Default max file size: 10 MB via API
- Large files: Use Git LFS instead
- Binary files: Always use base64 encoding

## Best Practices

1. **URL-encode paths**: Always encode file paths with slashes
2. **Use base64 for binary**: Encode binary files as base64
3. **Meaningful commits**: Write descriptive commit messages
4. **Use feature branches**: Don't commit directly to main for big changes
5. **Check for conflicts**: Use `last_commit_id` for critical updates

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Repository Files API](https://docs.gitlab.com/ee/api/repository_files.html)
