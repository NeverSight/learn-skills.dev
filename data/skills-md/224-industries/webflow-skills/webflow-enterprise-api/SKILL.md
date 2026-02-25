---
name: webflow-enterprise-api
description: Webflow Enterprise API endpoints for workspace management, audit logs, site activity, 301 redirects, robots.txt, and well-known files. Use when working with Enterprise-only Webflow API endpoints that require an Enterprise workspace.
license: MIT
metadata:
  author: "Ben Sabic"
  repository: "https://github.com/224-industries/webflow-skills"
  url: "https://skills.224ai.au/webflow-enterprise-api.skill"
  version: "1.0.0"
  keywords: "ai, agent, skill, enterprise, workspace management, site activity, audit logs, 301 redirects, robots-txt, well-known files, webflow api"
---

# Webflow Enterprise API

Enterprise-only API endpoints for managing Webflow workspaces and site configurations. All endpoints require an Enterprise workspace and appropriate token scopes.

## Endpoints Overview

| Endpoint | Method | Scope | Description |
|----------|--------|-------|-------------|
| `/workspaces/{id}/audit_logs` | GET | `workspace_activity:read` | Workspace audit logs |
| `/sites/{id}/activity_logs` | GET | `site_activity:read` | Site activity logs |
| `/sites/{id}/redirects` | GET | `sites:read` | List 301 redirect rules |
| `/sites/{id}/redirects` | POST | `sites:write` | Create a 301 redirect |
| `/sites/{id}/redirects/{rid}` | PATCH | `sites:write` | Update a 301 redirect |
| `/sites/{id}/redirects/{rid}` | DELETE | `sites:write` | Delete a 301 redirect |
| `/sites/{id}/robots_txt` | GET | `site_config:read` | Get robots.txt configuration |
| `/sites/{id}/robots_txt` | PUT | `site_config:write` | Replace robots.txt configuration |
| `/sites/{id}/robots_txt` | PATCH | `site_config:write` | Update robots.txt configuration |
| `/sites/{id}/robots_txt` | DELETE | `site_config:write` | Delete robots.txt rules |
| `/sites/{id}/well_known` | PUT | `site_config:write` | Upload a well-known file |
| `/sites/{id}/well_known` | DELETE | `site_config:write` | Delete well-known files |
| `/workspaces/{id}/sites` | POST | `workspace:write` | Create a new site |
| `/sites/{id}` | PATCH | `sites:write` | Update a site |
| `/sites/{id}` | DELETE | `sites:write` | Delete a site |
| `/sites/{id}/plan` | GET | `sites:read` | Get site hosting plan |

All endpoints use `https://api.webflow.com/v2` as the base URL and require `Authorization: Bearer <token>`.

## Important Notes

- All endpoints require an **Enterprise workspace** — they will return errors on non-Enterprise plans
- Use workspace API tokens (not site tokens) for workspace-level endpoints
- Rate limits apply — check the `X-RateLimit-Remaining` response header
- Pagination is available via `limit` and `offset` query parameters on list endpoints

## Reference Documentation

Each reference file includes YAML frontmatter with `name`, `description`, and `tags` for searchability. Use the search script in `scripts/search_references.py` to find relevant references.

### Audit & Activity

- **[references/workspace-audit-logs.md](references/workspace-audit-logs.md)**: Workspace audit logs — login/logout, role changes, membership, invitations
- **[references/site-activity-logs.md](references/site-activity-logs.md)**: Site activity logs — design changes, publishing, CMS, branches, libraries

### Site Configuration

- **[references/301-redirects.md](references/301-redirects.md)**: 301 redirect rules for a site — list, create, update, and delete
- **[references/robots-txt.md](references/robots-txt.md)**: Robots.txt crawler rules and sitemap URL — get, replace, update, and delete
- **[references/well-known-files.md](references/well-known-files.md)**: Upload files to the .well-known directory

### Workspace Management

- **[references/workspace-management.md](references/workspace-management.md)**: Create, update, delete sites, and get site plans within a workspace

### Searching References

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag <tag>

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search <query>
```

## Scripts

- **`scripts/search_references.py`**: Search reference files by tag, keyword, or list all with metadata
