---
name: "gitlab-group"
description: "GitLab group operations via API. ALWAYS use this skill when user wants to: (1) list/view groups, (2) create/update/delete groups, (3) manage group members, (4) list subgroups or group projects, (5) share projects with groups."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Group Skill

Group management operations for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| List groups | `glab api groups` | - |
| Get group | `glab api groups/:id` | - |
| Create group | `glab api groups -X POST -f ...` | ⚠️ |
| Update group | `glab api groups/:id -X PUT -f ...` | ⚠️ |
| Delete group | `glab api groups/:id -X DELETE` | ⚠️⚠️⚠️ |
| List members | `glab api groups/:id/members` | - |
| Add member | `glab api groups/:id/members -X POST -f ...` | ⚠️ |
| Update member | `glab api groups/:id/members/:uid -X PUT -f ...` | ⚠️ |
| Remove member | `glab api groups/:id/members/:uid -X DELETE` | ⚠️⚠️ |
| List subgroups | `glab api groups/:id/subgroups` | - |
| List projects | `glab api groups/:id/projects` | - |
| Share with group | `glab api projects/:id/share -X POST -f ...` | ⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User mentions "group", "team", "organization", "namespace"
- User wants to manage group membership
- User asks about subgroups or group projects
- User wants to share a project with another group

**NEVER use when:**
- User wants project-level settings (use gitlab-repo)
- User wants to manage CI/CD group variables (use gitlab-variable with -g flag)

## API Prerequisites

**Required Token Scopes:** `api`

**Permissions:**
- List/view groups: Any authenticated user (for visible groups)
- Create groups: Depends on instance settings
- Manage members: Owner or Maintainer role
- Delete groups: Owner role

## Access Levels

| Level | Value | Description |
|-------|:-----:|-------------|
| Guest | 10 | View issues and comments |
| Reporter | 20 | View code, create issues |
| Developer | 30 | Push code, create MRs |
| Maintainer | 40 | Manage project settings |
| Owner | 50 | Full control |

## Available Commands

### List Groups

```bash
# List accessible groups
glab api groups --method GET

# List with pagination
glab api groups --paginate

# Filter by search term
glab api "groups?search=devops" --method GET

# List only owned groups
glab api "groups?owned=true" --method GET

# List top-level groups only
glab api "groups?top_level_only=true" --method GET
```

### Get Group Details

```bash
# Get by numeric ID
glab api groups/123 --method GET

# Get by path (URL-encode slashes)
glab api "groups/$(echo 'my-group' | jq -Rr @uri)" --method GET

# Get nested group
glab api "groups/$(echo 'parent/child' | jq -Rr @uri)" --method GET

# Include additional details
glab api "groups/123?with_projects=true" --method GET
```

### Create Group

```bash
# Create top-level group
glab api groups --method POST \
  -f name="My Team" \
  -f path="my-team" \
  -f visibility="private"

# Create subgroup
glab api groups --method POST \
  -f name="Backend Team" \
  -f path="backend" \
  -f parent_id=123 \
  -f visibility="internal"

# Create with description and features
glab api groups --method POST \
  -f name="Dev Group" \
  -f path="dev-group" \
  -f description="Development team" \
  -f visibility="private" \
  -f request_access_enabled=true
```

**Visibility Options:**
- `private` - Only members can see
- `internal` - Any authenticated user
- `public` - Anyone can see

### Update Group

```bash
# Update name
glab api groups/123 --method PUT \
  -f name="New Name"

# Update visibility
glab api groups/123 --method PUT \
  -f visibility="internal"

# Update multiple settings
glab api groups/123 --method PUT \
  -f name="Updated Team" \
  -f description="New description" \
  -f request_access_enabled=false
```

### Delete Group

**Warning:** This permanently deletes the group and all its projects!

```bash
# Delete group
glab api groups/123 --method DELETE

# With permanently_remove flag (immediate deletion)
glab api "groups/123?permanently_remove=true" --method DELETE
```

### List Group Members

```bash
# List all members
glab api groups/123/members --method GET

# Include inherited members
glab api groups/123/members/all --method GET

# Search members
glab api "groups/123/members?query=john" --method GET
```

### Add Group Member

```bash
# Add as Developer
glab api groups/123/members --method POST \
  -f user_id=456 \
  -f access_level=30

# Add as Maintainer with expiration
glab api groups/123/members --method POST \
  -f user_id=456 \
  -f access_level=40 \
  -f expires_at="2025-12-31"
```

### Update Group Member

```bash
# Change access level
glab api groups/123/members/456 --method PUT \
  -f access_level=40

# Set expiration
glab api groups/123/members/456 --method PUT \
  -f expires_at="2025-06-30"
```

### Remove Group Member

```bash
# Remove member
glab api groups/123/members/456 --method DELETE
```

### List Subgroups

```bash
# List immediate subgroups
glab api groups/123/subgroups --method GET

# List all descendant groups
glab api groups/123/descendant_groups --method GET

# With pagination
glab api groups/123/subgroups --paginate
```

### List Group Projects

```bash
# List projects in group
glab api groups/123/projects --method GET

# Include subgroup projects
glab api "groups/123/projects?include_subgroups=true" --method GET

# Filter archived
glab api "groups/123/projects?archived=false" --method GET

# With pagination
glab api groups/123/projects --paginate
```

### Share Project with Group

```bash
# Share project with group (Developer access)
glab api projects/789/share --method POST \
  -f group_id=123 \
  -f group_access=30

# Share with expiration
glab api projects/789/share --method POST \
  -f group_id=123 \
  -f group_access=30 \
  -f expires_at="2025-12-31"

# Unshare
glab api projects/789/share/123 --method DELETE
```

## Common Workflows

### Workflow 1: Create Team Structure

```bash
# 1. Create parent group
glab api groups --method POST \
  -f name="Engineering" \
  -f path="engineering" \
  -f visibility="internal"

# 2. Get parent group ID
parent_id=$(glab api "groups/$(echo 'engineering' | jq -Rr @uri)" | jq -r '.id')

# 3. Create subgroups
glab api groups --method POST \
  -f name="Backend" \
  -f path="backend" \
  -f parent_id=$parent_id

glab api groups --method POST \
  -f name="Frontend" \
  -f path="frontend" \
  -f parent_id=$parent_id
```

### Workflow 2: Onboard Team Member

```bash
# 1. Find user ID
user_id=$(glab api "users?search=john.doe" | jq -r '.[0].id')

# 2. Add to group as Developer
glab api groups/123/members --method POST \
  -f user_id=$user_id \
  -f access_level=30

# 3. Verify membership
glab api groups/123/members/$user_id
```

### Workflow 3: Audit Group Access

```bash
# List all members including inherited
glab api groups/123/members/all --paginate | \
  jq -r '.[] | [.username, .access_level_description] | @tsv'
```

### Workflow 4: Transfer Project Between Groups

```bash
# 1. Get project ID
project_id=$(glab api "projects/$(echo 'old-group/my-project' | jq -Rr @uri)" | jq -r '.id')

# 2. Transfer to new group
glab api "projects/$project_id/transfer" --method PUT \
  -f namespace=456
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 403 on create group | Group creation disabled | Check instance settings or contact admin |
| 404 on group | Path not found | Verify group exists, check URL encoding |
| Cannot add member | User not found | Search users first with `glab api users?search=...` |
| Cannot delete group | Not owner | Need Owner role or admin access |
| Subgroup creation fails | Parent not found | Verify parent_id is correct |

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Groups API](https://docs.gitlab.com/ee/api/groups.html)
