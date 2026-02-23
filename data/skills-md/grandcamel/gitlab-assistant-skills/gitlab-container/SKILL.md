---
name: "gitlab-container"
description: "GitLab container registry operations via API. ALWAYS use this skill when user wants to: (1) list container repositories, (2) view/delete image tags, (3) clean up old images, (4) manage Docker registry."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Container Registry Skill

Container registry management for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| List repositories | `glab api projects/:id/registry/repositories` | - |
| Get repository | `glab api projects/:id/registry/repositories/:repo_id` | - |
| Delete repository | `glab api projects/:id/registry/repositories/:repo_id -X DELETE` | ⚠️⚠️⚠️ |
| List tags | `glab api projects/:id/registry/repositories/:repo_id/tags` | - |
| Get tag | `glab api projects/:id/registry/repositories/:repo_id/tags/:tag` | - |
| Delete tag | `glab api projects/:id/registry/repositories/:repo_id/tags/:tag -X DELETE` | ⚠️⚠️ |
| Bulk delete tags | `glab api projects/:id/registry/repositories/:repo_id/tags -X DELETE -f ...` | ⚠️⚠️⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User mentions "container", "registry", "docker image", "container image"
- User wants to list or delete Docker tags
- User mentions "image cleanup", "registry cleanup"
- User wants to view container repository information

**NEVER use when:**
- User wants to build/push Docker images (use CI/CD or docker CLI)
- User wants to run containers (use docker CLI or orchestrator)
- User wants package registry (different API)

## API Prerequisites

**Required Token Scopes:** `read_registry`, `write_registry` (for delete operations), or `api`

**Permissions:**
- Read registry: Reporter+
- Delete images: Developer+ (or Maintainer depending on settings)

**Note:** Container Registry must be enabled for the project.

## Available Commands

### List Container Repositories

```bash
# List all repositories in project
glab api projects/123/registry/repositories --method GET

# With pagination
glab api projects/123/registry/repositories --paginate

# Include tags count
glab api "projects/123/registry/repositories?tags_count=true" --method GET

# Using project path
glab api "projects/$(echo 'mygroup/myproject' | jq -Rr @uri)/registry/repositories"
```

### Get Repository Details

```bash
# Get specific repository
glab api projects/123/registry/repositories/456 --method GET

# With tags count
glab api "projects/123/registry/repositories/456?tags_count=true" --method GET
```

### Delete Repository

**Warning:** This deletes the repository and ALL its tags!

```bash
# Delete entire repository
glab api projects/123/registry/repositories/456 --method DELETE
```

### List Tags in Repository

```bash
# List all tags
glab api projects/123/registry/repositories/456/tags --method GET

# With pagination
glab api projects/123/registry/repositories/456/tags --paginate
```

### Get Tag Details

```bash
# Get specific tag
glab api projects/123/registry/repositories/456/tags/latest --method GET

# Get tag with digest info
glab api projects/123/registry/repositories/456/tags/v1.0.0 --method GET
```

### Delete Single Tag

```bash
# Delete specific tag
glab api projects/123/registry/repositories/456/tags/v1.0.0 --method DELETE

# Delete 'latest' tag
glab api projects/123/registry/repositories/456/tags/latest --method DELETE
```

### Bulk Delete Tags

```bash
# Delete tags matching regex (keep none)
glab api projects/123/registry/repositories/456/tags --method DELETE \
  -f name_regex_delete=".*"

# Delete all tags except last 5
glab api projects/123/registry/repositories/456/tags --method DELETE \
  -f name_regex_delete=".*" \
  -f keep_n=5

# Delete tags older than 30 days, keep last 10
glab api projects/123/registry/repositories/456/tags --method DELETE \
  -f name_regex_delete=".*" \
  -f keep_n=10 \
  -f older_than="30d"

# Delete only dev/snapshot tags
glab api projects/123/registry/repositories/456/tags --method DELETE \
  -f name_regex_delete="^dev-.*"

# Keep tags matching pattern (exclude from deletion)
glab api projects/123/registry/repositories/456/tags --method DELETE \
  -f name_regex_delete=".*" \
  -f name_regex_keep="^v[0-9]+\\.[0-9]+\\.[0-9]+$" \
  -f keep_n=5
```

## Bulk Delete Options

| Option | Type | Description |
|--------|------|-------------|
| `name_regex_delete` | string | Regex pattern for tags to delete |
| `name_regex_keep` | string | Regex pattern for tags to keep (overrides delete) |
| `keep_n` | integer | Number of latest tags to keep |
| `older_than` | string | Delete tags older than duration (e.g., `30d`, `1w`) |

## Common Workflows

### Workflow 1: List All Images and Tags

```bash
project_id=123

# Get all repositories
repos=$(glab api projects/$project_id/registry/repositories --paginate)

# For each repository, list tags
echo "$repos" | jq -r '.[].id' | while read repo_id; do
  repo_name=$(echo "$repos" | jq -r ".[] | select(.id == $repo_id) | .path")
  echo "=== $repo_name ==="
  glab api projects/$project_id/registry/repositories/$repo_id/tags | \
    jq -r '.[].name'
  echo ""
done
```

### Workflow 2: Find Large Images

```bash
project_id=123
repo_id=456

# List tags with sizes
glab api projects/$project_id/registry/repositories/$repo_id/tags --paginate | \
  jq -r 'sort_by(.total_size) | reverse | .[] | "\(.name): \(.total_size / 1024 / 1024 | floor) MB"'
```

### Workflow 3: Clean Up Old Development Images

```bash
project_id=123
repo_id=456

# Delete dev images older than 7 days, keep last 3
glab api projects/$project_id/registry/repositories/$repo_id/tags --method DELETE \
  -f name_regex_delete="^dev-.*" \
  -f older_than="7d" \
  -f keep_n=3
```

### Workflow 4: Keep Only Release Tags

```bash
project_id=123
repo_id=456

# Delete everything except semver tags, keep last 10
glab api projects/$project_id/registry/repositories/$repo_id/tags --method DELETE \
  -f name_regex_delete=".*" \
  -f name_regex_keep="^v[0-9]+\\.[0-9]+\\.[0-9]+$" \
  -f keep_n=10
```

### Workflow 5: Audit Registry Usage

```bash
project_id=123

# Get total size per repository
glab api "projects/$project_id/registry/repositories?tags_count=true" --paginate | \
  jq -r '.[] | "\(.path): \(.tags_count) tags"'

# Get detailed size info for a repository
repo_id=456
glab api projects/$project_id/registry/repositories/$repo_id/tags --paginate | \
  jq '[.[] | .total_size] | add / 1024 / 1024 | "Total: \(. | floor) MB"'
```

### Workflow 6: Find and Delete Untagged Images

```bash
project_id=123
repo_id=456

# Note: Untagged images are automatically cleaned up by GitLab
# You can trigger cleanup by deleting all tags and then the repo
# Or wait for the scheduled cleanup job
```

### Workflow 7: Export Tag List for Backup

```bash
project_id=123
repo_id=456

# Export tag names
glab api projects/$project_id/registry/repositories/$repo_id/tags --paginate | \
  jq -r '.[].name' > tags_backup.txt

# Export with details
glab api projects/$project_id/registry/repositories/$repo_id/tags --paginate | \
  jq -r '.[] | [.name, .created_at, .total_size] | @csv' > tags_details.csv
```

## Registry URL Format

GitLab Container Registry URLs follow this pattern:
```
registry.gitlab.com/<namespace>/<project>
registry.gitlab.com/<namespace>/<project>/<image>
```

For example:
- `registry.gitlab.com/mygroup/myproject`
- `registry.gitlab.com/mygroup/myproject/app`
- `registry.gitlab.com/mygroup/myproject/api`

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | No registry access | Check token scopes, need `read_registry` |
| 404 Not Found | Registry disabled or repo doesn't exist | Enable registry in project settings |
| Delete fails | Insufficient permissions | Need Developer+ role or `write_registry` scope |
| Bulk delete no effect | No matching tags | Check regex pattern |
| Old images persist | GitLab cleanup job | Wait for scheduled cleanup or delete manually |

## Size Limits and Quotas

- GitLab.com has storage quotas per namespace
- Self-managed instances may have different limits
- Check namespace storage usage in Settings > Usage Quotas

## Best Practices

1. **Regular cleanup**: Set up scheduled cleanup with `older_than` and `keep_n`
2. **Tag strategy**: Use meaningful tags (semver, commit SHA, branch name)
3. **Keep release tags**: Use `name_regex_keep` to preserve important versions
4. **Monitor storage**: Check registry size regularly
5. **Use CI cleanup**: Add cleanup job to CI pipeline

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Container Registry API](https://docs.gitlab.com/ee/api/container_registry.html)
