---
name: "gitlab-search"
description: "GitLab search operations via API. ALWAYS use this skill when user wants to: (1) search across GitLab globally, (2) find issues/MRs/code/commits, (3) search within a group or project, (4) find users or projects by keyword."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Search Skill

Search operations for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| Search projects | `glab api "search?scope=projects&search=..."` | - |
| Search issues | `glab api "search?scope=issues&search=..."` | - |
| Search MRs | `glab api "search?scope=merge_requests&search=..."` | - |
| Search code | `glab api "search?scope=blobs&search=..."` | - |
| Search commits | `glab api "search?scope=commits&search=..."` | - |
| Search users | `glab api "search?scope=users&search=..."` | - |
| Search wiki | `glab api "search?scope=wiki_blobs&search=..."` | - |
| Project search | `glab api "projects/:id/search?scope=...&search=..."` | - |
| Group search | `glab api "groups/:id/search?scope=...&search=..."` | - |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to search or find something across GitLab
- User mentions "search", "find", "query", "look for"
- User asks "where is", "which project has", "find all"
- User wants to search code, issues, MRs, commits, or wikis

**NEVER use when:**
- User wants to list all items (use specific skill: gitlab-issue, gitlab-mr, etc.)
- User knows the exact project/issue/MR ID
- User wants to search local files (use grep/find locally)

## API Prerequisites

**Required Token Scopes:** `read_api` or `api`

**Note:** Search results are limited to resources the authenticated user can access.

## Search Scopes

| Scope | Description | Available At |
|-------|-------------|--------------|
| `projects` | Search project names/descriptions | Global, Group |
| `issues` | Search issue titles/descriptions | Global, Group, Project |
| `merge_requests` | Search MR titles/descriptions | Global, Group, Project |
| `milestones` | Search milestone titles | Global, Group, Project |
| `snippet_titles` | Search snippet titles | Global |
| `wiki_blobs` | Search wiki content | Global, Group, Project |
| `commits` | Search commit messages | Global, Group, Project |
| `blobs` | Search code/file content | Global, Group, Project |
| `notes` | Search comments | Global, Group, Project |
| `users` | Search usernames/names | Global |

## Available Commands

### Global Search

```bash
# Search projects by name
glab api "search?scope=projects&search=api+gateway" --method GET

# Search issues globally
glab api "search?scope=issues&search=authentication+bug" --method GET

# Search merge requests
glab api "search?scope=merge_requests&search=refactor" --method GET

# Search code (blobs)
glab api "search?scope=blobs&search=TODO+fixme" --method GET

# Search commits
glab api "search?scope=commits&search=fix+security" --method GET

# Search wiki content
glab api "search?scope=wiki_blobs&search=installation" --method GET

# Search users
glab api "search?scope=users&search=john" --method GET

# Search milestones
glab api "search?scope=milestones&search=v2.0" --method GET

# Search comments/notes
glab api "search?scope=notes&search=approved" --method GET
```

### Project-Scoped Search

```bash
# Search issues in specific project
glab api "projects/123/search?scope=issues&search=bug" --method GET

# Search code in project
glab api "projects/123/search?scope=blobs&search=function+authenticate" --method GET

# Search commits in project
glab api "projects/123/search?scope=commits&search=fix" --method GET

# Search wiki in project
glab api "projects/123/search?scope=wiki_blobs&search=setup" --method GET

# Search MRs in project
glab api "projects/123/search?scope=merge_requests&search=feature" --method GET

# Search notes in project
glab api "projects/123/search?scope=notes&search=LGTM" --method GET

# Search milestones in project
glab api "projects/123/search?scope=milestones&search=sprint" --method GET

# Using project path (URL-encoded)
glab api "projects/$(echo 'mygroup/myproject' | jq -Rr @uri)/search?scope=blobs&search=TODO"
```

### Group-Scoped Search

```bash
# Search issues in group
glab api "groups/456/search?scope=issues&search=urgent" --method GET

# Search code across group
glab api "groups/456/search?scope=blobs&search=api+key" --method GET

# Search projects in group
glab api "groups/456/search?scope=projects&search=backend" --method GET

# Search MRs in group
glab api "groups/456/search?scope=merge_requests&search=hotfix" --method GET

# Using group path (URL-encoded)
glab api "groups/$(echo 'mygroup' | jq -Rr @uri)/search?scope=issues&search=bug"
```

### Pagination

```bash
# Get more results per page
glab api "search?scope=issues&search=bug&per_page=50" --method GET

# Get specific page
glab api "search?scope=issues&search=bug&per_page=50&page=2" --method GET

# Auto-paginate all results
glab api "search?scope=projects&search=api" --paginate
```

### Advanced Search Syntax

```bash
# Exact phrase search (use quotes, URL-encoded)
glab api "search?scope=blobs&search=%22exact+phrase%22" --method GET

# Filename filter in code search
glab api "search?scope=blobs&search=authenticate+filename:auth.py" --method GET

# Extension filter
glab api "search?scope=blobs&search=class+extension:java" --method GET

# Path filter
glab api "search?scope=blobs&search=config+path:src/main" --method GET
```

## Output Processing

### Extract Key Fields

```bash
# Get issue IDs and titles
glab api "search?scope=issues&search=bug" | \
  jq -r '.[] | "\(.project_id)#\(.iid): \(.title)"'

# Get project names and URLs
glab api "search?scope=projects&search=api" | \
  jq -r '.[] | "\(.path_with_namespace): \(.web_url)"'

# Get code matches with file paths
glab api "search?scope=blobs&search=TODO" | \
  jq -r '.[] | "\(.project_id):\(.path):\(.startline) \(.data)"'

# Get commit info
glab api "search?scope=commits&search=fix" | \
  jq -r '.[] | "\(.short_id): \(.title)"'
```

### Count Results

```bash
# Count matching issues
glab api "search?scope=issues&search=bug" --paginate | jq 'length'

# Count by project
glab api "search?scope=issues&search=bug" --paginate | \
  jq 'group_by(.project_id) | map({project: .[0].project_id, count: length})'
```

## Common Workflows

### Workflow 1: Find All TODOs in Codebase

```bash
# Search for TODO comments across all accessible projects
glab api "search?scope=blobs&search=TODO" --paginate | \
  jq -r '.[] | "\(.project_id):\(.path):\(.startline)"'
```

### Workflow 2: Find Issues Across Team Projects

```bash
# Get group ID
group_id=$(glab api "groups/$(echo 'myteam' | jq -Rr @uri)" | jq -r '.id')

# Search for critical issues in group
glab api "groups/$group_id/search?scope=issues&search=critical" --paginate | \
  jq -r '.[] | "\(.references.full): \(.title)"'
```

### Workflow 3: Find Who Worked on Feature

```bash
# Search commits mentioning feature
glab api "projects/123/search?scope=commits&search=authentication" | \
  jq -r '.[] | "\(.author_name): \(.title)"'
```

### Workflow 4: Find Security-Related Code

```bash
# Search for potential security patterns
for term in "password" "secret" "api_key" "token"; do
  echo "=== Searching for: $term ==="
  glab api "projects/123/search?scope=blobs&search=$term" | \
    jq -r '.[] | "\(.path):\(.startline)"'
done
```

### Workflow 5: Find Related MRs

```bash
# Search MRs by feature name
glab api "search?scope=merge_requests&search=oauth+integration" | \
  jq -r '.[] | "!\(.iid) [\(.state)]: \(.title)"'
```

## Search Tips

### Effective Search Terms

| For | Search Examples |
|-----|-----------------|
| Bug fixes | `fix bug`, `resolve issue`, `patch` |
| Features | `add feature`, `implement`, `new` |
| Refactoring | `refactor`, `cleanup`, `improve` |
| Security | `security`, `vulnerability`, `CVE` |
| Performance | `performance`, `optimize`, `speed` |
| Documentation | `docs`, `readme`, `documentation` |

### URL Encoding Special Characters

```bash
# Space -> +
glab api "search?scope=issues&search=fix+bug"

# Quotes (for exact match) -> %22
glab api "search?scope=blobs&search=%22exact+phrase%22"

# Hash -> %23
glab api "search?scope=issues&search=issue%231234"
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Empty results | No matches or no access | Verify search term, check permissions |
| Partial results | Pagination needed | Use `--paginate` flag |
| 400 Bad Request | Invalid scope | Check scope is valid for endpoint |
| Slow search | Large result set | Add filters or narrow scope |
| No code results | Basic search disabled | Contact admin to enable advanced search |

## Search Limitations

- Basic search searches titles/descriptions only
- Advanced search (Elasticsearch) required for code search
- Results limited to accessible resources
- Rate limits apply for large searches

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Search API](https://docs.gitlab.com/ee/api/search.html)
