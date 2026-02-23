---
name: "gitlab-wiki"
description: "GitLab wiki operations via API. ALWAYS use this skill when user wants to: (1) list wiki pages, (2) read wiki content, (3) create/update/delete wiki pages, (4) upload wiki attachments."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Wiki Skill

Wiki page management for GitLab using `glab api` raw endpoint calls.

## Quick Reference

| Operation | Command Pattern | Risk |
|-----------|-----------------|:----:|
| List pages | `glab api projects/:id/wikis` | - |
| Get page | `glab api projects/:id/wikis/:slug` | - |
| Create page | `glab api projects/:id/wikis -X POST -f ...` | ⚠️ |
| Update page | `glab api projects/:id/wikis/:slug -X PUT -f ...` | ⚠️ |
| Delete page | `glab api projects/:id/wikis/:slug -X DELETE` | ⚠️⚠️ |
| Upload attachment | `glab api projects/:id/wikis/attachments -X POST ...` | ⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User mentions "wiki", "wiki page", "documentation page"
- User wants to create/edit project documentation in GitLab
- User mentions wiki slugs or wiki content
- User wants to upload images to wiki

**NEVER use when:**
- User wants README files (use gitlab-file)
- User wants to search wiki content (use gitlab-search with `wiki_blobs` scope)
- User wants external documentation (not GitLab wiki)

## API Prerequisites

**Required Token Scopes:** `api`

**Permissions:**
- Read wiki: Reporter+ (for private repos)
- Write wiki: Developer+ (or based on project settings)

**Note:** Wiki must be enabled for the project.

## Available Commands

### List Wiki Pages

```bash
# List all wiki pages
glab api projects/123/wikis --method GET

# With pagination
glab api projects/123/wikis --paginate

# Using project path
glab api "projects/$(echo 'mygroup/myproject' | jq -Rr @uri)/wikis"
```

### Get Wiki Page

```bash
# Get page by slug
glab api projects/123/wikis/home --method GET

# Get page with spaces in slug (URL-encode)
glab api "projects/123/wikis/$(echo 'Getting Started' | jq -Rr @uri)" --method GET

# Get nested page
glab api "projects/123/wikis/$(echo 'docs/installation' | jq -Rr @uri)" --method GET

# Get page with specific version
glab api "projects/123/wikis/home?version=abc123" --method GET

# Render HTML
glab api "projects/123/wikis/home?render_html=true" --method GET
```

### Create Wiki Page

```bash
# Create simple page
glab api projects/123/wikis --method POST \
  -f title="Getting Started" \
  -f content="# Getting Started\n\nWelcome to the project!"

# Create with Markdown format
glab api projects/123/wikis --method POST \
  -f title="Installation Guide" \
  -f content="# Installation\n\n## Prerequisites\n\n- Node.js 18+\n- npm" \
  -f format="markdown"

# Create with custom slug
glab api projects/123/wikis --method POST \
  -f title="API Reference" \
  -f slug="api-docs" \
  -f content="# API Documentation\n\nEndpoints..."

# Create nested page (using directory in slug)
glab api projects/123/wikis --method POST \
  -f title="Database Setup" \
  -f slug="guides/database-setup" \
  -f content="# Database Setup\n\nConfiguration steps..."
```

### Update Wiki Page

```bash
# Update content
glab api "projects/123/wikis/$(echo 'Getting Started' | jq -Rr @uri)" --method PUT \
  -f content="# Getting Started\n\n## Updated content\n\nNew information..."

# Update title and content
glab api projects/123/wikis/home --method PUT \
  -f title="Home Page" \
  -f content="# Welcome\n\nUpdated home page content."

# Change format (markdown, rdoc, asciidoc)
glab api projects/123/wikis/readme --method PUT \
  -f format="asciidoc" \
  -f content="= README\n\nAsciidoc content here."
```

### Delete Wiki Page

```bash
# Delete page
glab api projects/123/wikis/old-page --method DELETE

# Delete nested page (URL-encode)
glab api "projects/123/wikis/$(echo 'drafts/temp-page' | jq -Rr @uri)" --method DELETE
```

### Upload Attachment

```bash
# Upload image
glab api projects/123/wikis/attachments --method POST \
  -F "file=@screenshot.png"

# The response contains the markdown link to use
# {"file_name":"screenshot.png","file_path":"uploads/...","branch":"master","link":{"url":"...","markdown":"![screenshot](uploads/...)"}}
```

## Wiki Page Options

| Option | Type | Description |
|--------|------|-------------|
| `title` | string | Page title (required for create) |
| `slug` | string | Page URL slug (auto-generated from title if not provided) |
| `content` | string | Page content |
| `format` | string | Content format: `markdown` (default), `rdoc`, `asciidoc` |

## Format Support

| Format | Extension | Description |
|--------|-----------|-------------|
| `markdown` | `.md` | GitHub-flavored Markdown |
| `rdoc` | `.rdoc` | Ruby documentation format |
| `asciidoc` | `.asciidoc` | AsciiDoc format |
| `org` | `.org` | Org mode format |

## Common Workflows

### Workflow 1: Create Documentation Structure

```bash
project_id=123

# Create home page
glab api projects/$project_id/wikis --method POST \
  -f title="Home" \
  -f content="# Project Wiki\n\n- [Getting Started](Getting-Started)\n- [API Reference](API-Reference)\n- [FAQ](FAQ)"

# Create getting started guide
glab api projects/$project_id/wikis --method POST \
  -f title="Getting Started" \
  -f content="# Getting Started\n\n## Installation\n\n\`\`\`bash\nnpm install\n\`\`\`"

# Create API reference
glab api projects/$project_id/wikis --method POST \
  -f title="API Reference" \
  -f content="# API Reference\n\n## Endpoints\n\n| Method | Path | Description |\n|--------|------|-------------|\n| GET | /users | List users |"
```

### Workflow 2: Backup Wiki Content

```bash
# List all pages and save content
mkdir -p wiki_backup
glab api projects/123/wikis --paginate | jq -r '.[].slug' | while read slug; do
  echo "Backing up: $slug"
  glab api "projects/123/wikis/$(echo "$slug" | jq -Rr @uri)" | \
    jq -r '.content' > "wiki_backup/${slug//\//_}.md"
done
```

### Workflow 3: Migrate Wiki Content

```bash
# Get page from source project
content=$(glab api projects/123/wikis/home | jq -r '.content')
title=$(glab api projects/123/wikis/home | jq -r '.title')

# Create in target project
glab api projects/456/wikis --method POST \
  -f title="$title" \
  -f content="$content"
```

### Workflow 4: Add Image to Wiki Page

```bash
# 1. Upload image
response=$(glab api projects/123/wikis/attachments --method POST -F "file=@diagram.png")

# 2. Get markdown link
markdown_link=$(echo "$response" | jq -r '.link.markdown')

# 3. Update page to include image
current_content=$(glab api projects/123/wikis/architecture | jq -r '.content')
new_content="$current_content

## Diagram

$markdown_link"

glab api projects/123/wikis/architecture --method PUT \
  -f content="$new_content"
```

### Workflow 5: List All Wiki Pages with Titles

```bash
glab api projects/123/wikis --paginate | \
  jq -r '.[] | "[\(.title)](\(.slug))"'
```

## Wiki Slugs

Slugs are URL-safe versions of titles:
- Spaces become hyphens: `Getting Started` → `Getting-Started`
- Special characters are removed
- Case is preserved

For nested pages, use directory structure in slug:
- `guides/installation` creates a page under `guides/`

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | Wiki disabled or page doesn't exist | Enable wiki in project settings, check slug |
| 403 Forbidden | No write access | Need Developer+ role or check wiki permissions |
| Empty content | Encoding issue | Check content string escaping |
| Slug mismatch | Auto-generated slug differs | Explicitly set `slug` parameter |
| Upload fails | Wrong content type | Use `-F` flag for file uploads |

## Best Practices

1. **Use meaningful slugs**: Keep URLs readable and consistent
2. **Create a home page**: Start with a home/index page
3. **Use relative links**: Link between wiki pages using slugs
4. **Organize with structure**: Use slug directories for organization
5. **Include images**: Upload screenshots and diagrams for clarity

## Related Documentation

- [API Helpers](../shared/docs/API_HELPERS.md)
- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
- [GitLab Wiki API](https://docs.gitlab.com/ee/api/wikis.html)
