---
name: "gitlab-badge"
description: "GitLab badge operations via API. ALWAYS use this skill when user wants to: (1) list project badges, (2) create pipeline/coverage badges, (3) update or delete badges, (4) preview badge rendering."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Badge Skill

Project badge management for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| List badges | `glab api projects/:id/badges` | - |
| Get badge | `glab api projects/:id/badges/:badge_id` | - |
| Create badge | `glab api projects/:id/badges -X POST -f ...` | ⚠️ |
| Update badge | `glab api projects/:id/badges/:badge_id -X PUT -f ...` | ⚠️ |
| Delete badge | `glab api projects/:id/badges/:badge_id -X DELETE` | ⚠️ |
| Preview badge | `glab api projects/:id/badges/render?...` | - |
| List group badges | `glab api groups/:id/badges` | - |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User mentions "badge", "status badge", "coverage badge"
- User wants to add badges to README
- User wants pipeline or build status indicators
- User mentions badge links or badge images

**NEVER use when:**
- User wants labels on issues/MRs (use gitlab-label)
- User wants status of pipelines (use gitlab-ci)
- User wants project settings (use gitlab-repo)

## API Prerequisites

**Required Token Scopes:** `api`

**Permissions:**
- Read badges: Reporter+
- Manage badges: Maintainer+

## Badge Placeholders

GitLab supports placeholders in badge URLs:

| Placeholder | Description |
|-------------|-------------|
| `%{project_path}` | Full project path (e.g., `group/project`) |
| `%{project_id}` | Numeric project ID |
| `%{project_name}` | Project name |
| `%{project_namespace}` | Project namespace |
| `%{default_branch}` | Default branch name |
| `%{commit_sha}` | Current commit SHA |

## Available Commands

### List Project Badges

```bash
# List all project badges
glab api projects/123/badges --method GET

# Using project path
glab api "projects/$(echo 'mygroup/myproject' | jq -Rr @uri)/badges"
```

### List Group Badges

```bash
# List group badges (inherited by projects)
glab api groups/456/badges --method GET
```

### Get Badge Details

```bash
# Get specific badge
glab api projects/123/badges/1 --method GET
```

### Create Badge

```bash
# Create pipeline status badge
glab api projects/123/badges --method POST \
  -f link_url="https://gitlab.com/%{project_path}/-/pipelines" \
  -f image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg"

# Create coverage badge
glab api projects/123/badges --method POST \
  -f link_url="https://gitlab.com/%{project_path}/-/jobs" \
  -f image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/coverage.svg"

# Create custom badge (e.g., shields.io)
glab api projects/123/badges --method POST \
  -f link_url="https://opensource.org/licenses/MIT" \
  -f image_url="https://img.shields.io/badge/License-MIT-yellow.svg"

# Create named badge
glab api projects/123/badges --method POST \
  -f name="Build Status" \
  -f link_url="https://gitlab.com/%{project_path}/-/pipelines" \
  -f image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg"

# Create release badge
glab api projects/123/badges --method POST \
  -f link_url="https://gitlab.com/%{project_path}/-/releases" \
  -f image_url="https://gitlab.com/%{project_path}/-/badges/release.svg"
```

### Update Badge

```bash
# Update badge URLs
glab api projects/123/badges/1 --method PUT \
  -f link_url="https://new-link.com" \
  -f image_url="https://new-image.com/badge.svg"

# Update badge name
glab api projects/123/badges/1 --method PUT \
  -f name="New Badge Name"
```

### Delete Badge

```bash
# Delete badge
glab api projects/123/badges/1 --method DELETE
```

### Preview Badge Rendering

```bash
# Preview how a badge would render
glab api "projects/123/badges/render?link_url=https://gitlab.com/%{project_path}&image_url=https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg" --method GET
```

## Common Badge Templates

### Pipeline Status Badge

```bash
# Link and image URLs
link_url="https://gitlab.com/%{project_path}/-/pipelines"
image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg"

glab api projects/123/badges --method POST \
  -f link_url="$link_url" \
  -f image_url="$image_url"
```

Markdown: `[![pipeline status](https://gitlab.com/group/project/badges/main/pipeline.svg)](https://gitlab.com/group/project/-/pipelines)`

### Coverage Badge

```bash
link_url="https://gitlab.com/%{project_path}/-/jobs"
image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/coverage.svg"

glab api projects/123/badges --method POST \
  -f link_url="$link_url" \
  -f image_url="$image_url"
```

### Release Badge

```bash
link_url="https://gitlab.com/%{project_path}/-/releases"
image_url="https://gitlab.com/%{project_path}/-/badges/release.svg"

glab api projects/123/badges --method POST \
  -f link_url="$link_url" \
  -f image_url="$image_url"
```

### Custom Shields.io Badges

```bash
# License badge
glab api projects/123/badges --method POST \
  -f name="License" \
  -f link_url="https://opensource.org/licenses/MIT" \
  -f image_url="https://img.shields.io/badge/License-MIT-blue.svg"

# Version badge
glab api projects/123/badges --method POST \
  -f name="Version" \
  -f link_url="https://gitlab.com/%{project_path}/-/releases" \
  -f image_url="https://img.shields.io/badge/version-1.0.0-green.svg"

# Maintenance badge
glab api projects/123/badges --method POST \
  -f name="Maintained" \
  -f link_url="https://gitlab.com/%{project_path}" \
  -f image_url="https://img.shields.io/badge/Maintained%3F-yes-green.svg"
```

## Common Workflows

### Workflow 1: Set Up Standard Badges

```bash
project_id=123

# Pipeline status
glab api projects/$project_id/badges --method POST \
  -f name="Pipeline" \
  -f link_url="https://gitlab.com/%{project_path}/-/pipelines" \
  -f image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg"

# Coverage
glab api projects/$project_id/badges --method POST \
  -f name="Coverage" \
  -f link_url="https://gitlab.com/%{project_path}/-/jobs" \
  -f image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/coverage.svg"

# Latest release
glab api projects/$project_id/badges --method POST \
  -f name="Release" \
  -f link_url="https://gitlab.com/%{project_path}/-/releases" \
  -f image_url="https://gitlab.com/%{project_path}/-/badges/release.svg"
```

### Workflow 2: Generate README Badge Markdown

```bash
# Get all badges and generate markdown
glab api projects/123/badges | \
  jq -r '.[] | "[![\(.name // "badge")](\(.rendered_image_url))](\(.rendered_link_url))"'
```

### Workflow 3: Copy Badges to Another Project

```bash
source_project=123
target_project=456

# Get badges from source
badges=$(glab api projects/$source_project/badges)

# Create in target (using placeholders, so they'll work for the new project)
echo "$badges" | jq -c '.[]' | while read badge; do
  link_url=$(echo "$badge" | jq -r '.link_url')
  image_url=$(echo "$badge" | jq -r '.image_url')
  name=$(echo "$badge" | jq -r '.name // empty')

  glab api projects/$target_project/badges --method POST \
    -f link_url="$link_url" \
    -f image_url="$image_url" \
    ${name:+-f name="$name"}
done
```

### Workflow 4: Audit Badge Configuration

```bash
# List all badges with rendered URLs
glab api projects/123/badges | \
  jq -r '.[] | "ID: \(.id)\n  Name: \(.name // "unnamed")\n  Image: \(.rendered_image_url)\n  Link: \(.rendered_link_url)\n"'
```

### Workflow 5: Replace All Badges

```bash
project_id=123

# Delete existing badges
glab api projects/$project_id/badges | jq -r '.[].id' | while read badge_id; do
  glab api projects/$project_id/badges/$badge_id --method DELETE
done

# Create new badges
glab api projects/$project_id/badges --method POST \
  -f name="Build" \
  -f link_url="https://gitlab.com/%{project_path}/-/pipelines" \
  -f image_url="https://gitlab.com/%{project_path}/badges/%{default_branch}/pipeline.svg"
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Badge not showing | URL incorrect | Check rendered URLs in API response |
| 403 Forbidden | Not maintainer | Need Maintainer+ role |
| Placeholder not replaced | Wrong syntax | Use `%{placeholder}` format |
| Coverage badge shows "unknown" | No coverage report | Configure CI to output coverage |
| Pipeline badge shows old status | Cache | Badge images may be cached |

## Badge Best Practices

1. **Use placeholders**: Make badges portable between projects
2. **Name your badges**: Helps identify them in the list
3. **Link to relevant pages**: Badge clicks should go somewhere useful
4. **Keep badges updated**: Remove stale badges
5. **Use consistent styling**: Mix of GitLab and shields.io can look inconsistent

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Badges API](https://docs.gitlab.com/ee/api/project_badges.html)
