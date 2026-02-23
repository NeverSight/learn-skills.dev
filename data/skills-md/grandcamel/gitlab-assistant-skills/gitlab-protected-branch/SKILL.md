---
name: "gitlab-protected-branch"
description: "GitLab protected branch operations via API. ALWAYS use this skill when user wants to: (1) view branch protection rules, (2) protect/unprotect branches, (3) configure push/merge access levels, (4) set up code owner approval requirements."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Protected Branch Skill

Branch protection management for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| List protected | `glab api projects/:id/protected_branches` | - |
| Get protection | `glab api projects/:id/protected_branches/:name` | - |
| Protect branch | `glab api projects/:id/protected_branches -X POST -f ...` | ⚠️ |
| Update protection | `glab api projects/:id/protected_branches/:name -X PATCH -f ...` | ⚠️ |
| Unprotect branch | `glab api projects/:id/protected_branches/:name -X DELETE` | ⚠️⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User mentions "protect branch", "branch protection", "protected branches"
- User wants to restrict who can push/merge to a branch
- User mentions "force push", "code owners", "merge access"
- User wants to configure main/release branch security

**NEVER use when:**
- User wants to create/delete branches (use git or gitlab-repo)
- User wants to manage merge request approvals (different API)
- User wants to configure CI/CD for branches (use gitlab-ci)

## API Prerequisites

**Required Token Scopes:** `api`

**Permissions:**
- View protected branches: Developer+
- Manage protected branches: Maintainer+

**Premium Features:**
- Code owner approval: GitLab Premium
- Multiple access levels: GitLab Premium

## Access Levels

| Level | Value | Description |
|-------|:-----:|-------------|
| No access | 0 | Nobody can perform action |
| Developer | 30 | Developers and above |
| Maintainer | 40 | Maintainers and above |
| Admin | 60 | Instance admins only |

## Available Commands

### List Protected Branches

```bash
# List all protected branches
glab api projects/123/protected_branches --method GET

# With pagination
glab api projects/123/protected_branches --paginate

# Using project path
glab api "projects/$(echo 'mygroup/myproject' | jq -Rr @uri)/protected_branches"
```

### Get Protection Details

```bash
# Get protection for specific branch
glab api projects/123/protected_branches/main --method GET

# Branch with special characters (URL-encode)
glab api "projects/123/protected_branches/$(echo 'release/1.0' | jq -Rr @uri)"

# Branch with wildcard pattern
glab api "projects/123/protected_branches/$(echo 'feature/*' | jq -Rr @uri)"
```

### Protect a Branch

```bash
# Basic protection (maintainers push, developers merge)
glab api projects/123/protected_branches --method POST \
  -f name="main" \
  -f push_access_level=40 \
  -f merge_access_level=30

# Strict protection (only maintainers)
glab api projects/123/protected_branches --method POST \
  -f name="main" \
  -f push_access_level=40 \
  -f merge_access_level=40 \
  -f allow_force_push=false

# With code owner approval (Premium)
glab api projects/123/protected_branches --method POST \
  -f name="main" \
  -f push_access_level=40 \
  -f merge_access_level=30 \
  -f code_owner_approval_required=true

# Protect wildcard pattern
glab api projects/123/protected_branches --method POST \
  -f name="release/*" \
  -f push_access_level=40 \
  -f merge_access_level=40

# Allow developers to push, anyone to merge
glab api projects/123/protected_branches --method POST \
  -f name="develop" \
  -f push_access_level=30 \
  -f merge_access_level=30 \
  -f allow_force_push=false

# No direct push (only through MR)
glab api projects/123/protected_branches --method POST \
  -f name="main" \
  -f push_access_level=0 \
  -f merge_access_level=30
```

### Update Protection

```bash
# Change merge access level
glab api projects/123/protected_branches/main --method PATCH \
  -f merge_access_level=40

# Enable code owner approval (Premium)
glab api projects/123/protected_branches/main --method PATCH \
  -f code_owner_approval_required=true

# Allow force push (not recommended for main)
glab api projects/123/protected_branches/feature%2F* --method PATCH \
  -f allow_force_push=true
```

### Unprotect Branch

**Warning:** This removes all protection from the branch!

```bash
# Unprotect branch
glab api projects/123/protected_branches/main --method DELETE

# Unprotect wildcard pattern (URL-encode)
glab api "projects/123/protected_branches/$(echo 'feature/*' | jq -Rr @uri)" --method DELETE
```

## Protection Options

| Option | Type | Description |
|--------|------|-------------|
| `name` | string | Branch name or wildcard pattern |
| `push_access_level` | integer | Who can push (0, 30, 40, 60) |
| `merge_access_level` | integer | Who can merge MRs (0, 30, 40, 60) |
| `unprotect_access_level` | integer | Who can unprotect (40, 60) |
| `allow_force_push` | boolean | Allow force push to branch |
| `code_owner_approval_required` | boolean | Require code owner approval (Premium) |

## Wildcard Patterns

| Pattern | Matches |
|---------|---------|
| `*` | All branches |
| `feature/*` | `feature/login`, `feature/signup`, etc. |
| `release/*` | `release/1.0`, `release/2.0`, etc. |
| `hotfix/*` | `hotfix/bug-123`, etc. |
| `*-stable` | `1.0-stable`, `2.0-stable`, etc. |

## Common Workflows

### Workflow 1: Standard Branch Protection

```bash
# Protect main branch
glab api projects/123/protected_branches --method POST \
  -f name="main" \
  -f push_access_level=40 \
  -f merge_access_level=30 \
  -f allow_force_push=false

# Protect develop branch
glab api projects/123/protected_branches --method POST \
  -f name="develop" \
  -f push_access_level=30 \
  -f merge_access_level=30 \
  -f allow_force_push=false

# Protect release branches
glab api projects/123/protected_branches --method POST \
  -f name="release/*" \
  -f push_access_level=40 \
  -f merge_access_level=40
```

### Workflow 2: Audit Current Protections

```bash
# List all protections with details
glab api projects/123/protected_branches --paginate | \
  jq -r '.[] | "Branch: \(.name)\n  Push: \(.push_access_levels[0].access_level_description // "none")\n  Merge: \(.merge_access_levels[0].access_level_description // "none")\n  Force Push: \(.allow_force_push)\n"'
```

### Workflow 3: Lock Down Production Branch

```bash
# Strict protection: only maintainers, no force push, require code owners
glab api projects/123/protected_branches --method POST \
  -f name="production" \
  -f push_access_level=40 \
  -f merge_access_level=40 \
  -f allow_force_push=false \
  -f code_owner_approval_required=true
```

### Workflow 4: Temporarily Allow Push to Protected Branch

```bash
# 1. Check current protection
glab api projects/123/protected_branches/main

# 2. Update to allow developer push
glab api projects/123/protected_branches/main --method PATCH \
  -f push_access_level=30

# 3. Do the work...

# 4. Restore protection
glab api projects/123/protected_branches/main --method PATCH \
  -f push_access_level=40
```

### Workflow 5: Set Up GitFlow Protection

```bash
project_id=123

# Main - production (strict)
glab api projects/$project_id/protected_branches --method POST \
  -f name="main" \
  -f push_access_level=0 \
  -f merge_access_level=40 \
  -f allow_force_push=false

# Develop - integration
glab api projects/$project_id/protected_branches --method POST \
  -f name="develop" \
  -f push_access_level=30 \
  -f merge_access_level=30

# Feature branches - allow developers
glab api projects/$project_id/protected_branches --method POST \
  -f name="feature/*" \
  -f push_access_level=30 \
  -f merge_access_level=30

# Release branches - maintainers only
glab api projects/$project_id/protected_branches --method POST \
  -f name="release/*" \
  -f push_access_level=40 \
  -f merge_access_level=40

# Hotfix branches - maintainers only
glab api projects/$project_id/protected_branches --method POST \
  -f name="hotfix/*" \
  -f push_access_level=40 \
  -f merge_access_level=40
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | Not maintainer | Need Maintainer+ role |
| 404 Not Found | Branch doesn't exist or not protected | Check branch name |
| 400 Bad Request | Invalid access level | Use 0, 30, 40, or 60 |
| Branch still protected | Pattern match | Check for wildcard patterns |
| Cannot push to protected | Access level too low | Update protection or get higher role |

## Best Practices

1. **Always protect main**: At minimum, protect your default branch
2. **Use wildcards wisely**: Protect `release/*` instead of individual releases
3. **Avoid force push on main**: Set `allow_force_push=false`
4. **Document protections**: Keep track of your branch protection strategy
5. **Review regularly**: Audit protections periodically

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Protected Branches API](https://docs.gitlab.com/ee/api/protected_branches.html)
