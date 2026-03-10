---
name: ghost-blog
description: Manage Ghost blog posts via Admin API. Capabilities include list/filter posts (status, tag, featured, search), CRUD operations (create, read, update, delete, publish), bulk operations (mass publish/unpublish, add/remove tags), and tag management. Use when user mentions ghost blog, manage posts, publish drafts, bulk update, or blog management tasks.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Ghost Blog Management

Manage Ghost CMS posts and tags via Admin API.

## Setup

### 1. Install Dependencies

```bash
cd .claude/skills/ghost-blog/scripts
uv venv
uv pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cd .claude/skills/ghost-blog/scripts
cp .env.example .env
# Edit .env with your Ghost credentials
```

**.env file:**

```
GHOST_URL=https://your-blog.ghost.io
GHOST_ADMIN_KEY=your-key-id:your-secret-key
GHOST_API_VERSION=v5.0
```

**Get your Admin API Key:**

1. Go to Ghost Admin → Settings → Integrations
2. Create a Custom Integration
3. Copy the Admin API Key (format: `id:secret`)

### 3. Verify Setup

```bash
cd .claude/skills/ghost-blog/scripts && uv run python ghost_core.py
```

## Quick Start

**List posts:**

```bash
python scripts/posts_browse.py --status draft
python scripts/posts_browse.py --tag news --featured
```

**Manage single post:**

```bash
python scripts/posts_crud.py get --id POST_ID
python scripts/posts_crud.py create --title "New Post" --html "<p>Content</p>"
python scripts/posts_crud.py publish --id POST_ID
```

**Bulk operations:**

```bash
python scripts/posts_bulk.py publish --filter "status:draft" --execute
python scripts/posts_bulk.py add-tag --filter "status:published" --tag "archive" --execute
```

**Manage tags:**

```bash
python scripts/tags_manage.py list
python scripts/tags_manage.py create --name "Tutorial"
```

## Dispatch Rules

| User Intent                           | Script                    | Example Command                      |
| ------------------------------------- | ------------------------- | ------------------------------------ |
| test, run tests                       | pytest                    | `cd scripts && uv run pytest -v`     |
| list posts, show drafts, filter posts | posts\_browse.py          | `--status draft --tag news`          |
| get post, read post, show post        | posts\_crud.py get        | `--id xxx` or `--slug xxx`           |
| create post, new post, write post     | posts\_crud.py create     | `--title "..." --html "..."`         |
| update post, edit post, change post   | posts\_crud.py update     | `--id xxx --title "..."`             |
| delete post, remove post              | posts\_crud.py delete     | `--id xxx --confirm`                 |
| publish post, publish draft           | posts\_crud.py publish    | `--id xxx`                           |
| unpublish post                        | posts\_crud.py unpublish  | `--id xxx`                           |
| bulk publish, publish all drafts      | posts\_bulk.py publish    | `--filter "..." --execute`           |
| bulk unpublish                        | posts\_bulk.py unpublish  | `--filter "..." --execute`           |
| add tag to posts, tag posts           | posts\_bulk.py add-tag    | `--filter "..." --tag xxx --execute` |
| remove tag from posts                 | posts\_bulk.py remove-tag | `--filter "..." --tag xxx --execute` |
| list tags, show tags                  | tags\_manage.py list      | (no options needed)                  |
| create tag, new tag                   | tags\_manage.py create    | `--name "..."`                       |
| delete tag, remove tag                | tags\_manage.py delete    | `--slug xxx --confirm`               |

## Scripts

| Script            | Purpose                                       |
| ----------------- | --------------------------------------------- |
| `ghost_core.py`   | Shared: JWT auth, HTTP client, error handling |
| `posts_browse.py` | List, filter, search posts                    |
| `posts_crud.py`   | CRUD operations for single posts              |
| `posts_bulk.py`   | Batch operations (publish, tags, featured)    |
| `tags_manage.py`  | CRUD operations for tags                      |

## Filter Syntax (NQL)

Ghost uses NQL for filtering:

```
# Status
status:draft
status:published
status:scheduled

# Tags (use slug, not name)
tag:news
tags:[news,tutorial]

# Featured
featured:true

# Combine (AND)
status:published+featured:true

# Combine (OR)
status:draft,status:scheduled
```

**Note:** The `--tag` option in `posts_browse.py` accepts both tag names and slugs. It automatically resolves names to slugs via API lookup.

## Creating Posts from Markdown Files

When creating posts from markdown files (e.g., a blog series):

```python
import markdown
from ghost_core import api_request

# 1. Convert Markdown to HTML
md_content = open('article.md').read()
html_content = markdown.markdown(md_content, extensions=['extra', 'nl2br'])

# 2. Create post with source=html (CRITICAL for Ghost 5.0+)
post_data = {
    'title': 'My Post',
    'html': html_content,
    'status': 'draft',
    'tags': ['my-tag']
}
response = api_request('POST', 'posts/',
                       data={'posts': [post_data]},
                       params={'source': 'html'})  # Required!
```

**Important:** Ghost 5.0+ uses Lexical editor format. The `source=html` param tells Ghost to convert HTML to Lexical. Without it, post content will be empty!

### Fixing Internal Links

If markdown files have internal links like `[Title](other-file.md)`, replace them with Ghost slugs after creating posts:

```python
LINK_MAP = {
    'old-file.md': '/new-ghost-slug/',
}

html = html.replace('href="old-file.md"', 'href="/new-ghost-slug/"')
```

## Safety Features

* **Bulk operations**: Preview mode by default

* **Delete operations**: Require `--confirm` flag

* **API versioning**: Uses Ghost v5.0 API

* **HTML conversion**: Auto-adds `source=html` param for Ghost 5.0+ compatibility

## Testing

### Setup Test Environment

```bash
cd .claude/skills/ghost-blog/scripts
uv venv
uv pip install -r requirements.txt
```

### Run Tests

```bash
cd .claude/skills/ghost-blog/scripts && uv run pytest -v
```

### Run with Coverage

```bash
cd .claude/skills/ghost-blog/scripts && uv run pytest -v --cov=. --cov-report=term-missing
```

## Troubleshooting

| Error                              | Cause                      | Solution                                      |
| ---------------------------------- | -------------------------- | --------------------------------------------- |
| "No virtual environment found"     | Missing venv               | Run `uv venv` in scripts directory            |
| "Failed to spawn: pytest"          | Missing deps               | Run `uv pip install -r requirements.txt`      |
| "GHOST\_URL not set"               | Missing .env               | Copy `.env.example` to `.env` and configure   |
| "GHOST\_ADMIN\_KEY invalid format" | Wrong key format           | Key must be `id:secret` format                |
| "UnauthorizedError"                | Invalid API key            | Check key is valid and has permissions        |
| "UPDATE\_COLLISION"                | Post modified              | Retry operation (auto-refetches updated\_at)  |
| **Post content empty**             | Missing `source=html`      | Ghost 5.0+ requires `source=html` param       |
| **Tag filter returns 0**           | Using name instead of slug | Use tag slug or let script resolve it         |
| **HTTP 422 on tags list**          | Invalid params             | Don't use `include=count.posts` or `order`    |
| **Links point to .md files**       | Internal markdown links    | Replace with Ghost slugs after creating posts |

## References

* [Ghost Admin API Docs](https://docs.ghost.org/admin-api/)

* [NQL Filter Reference](https://ghost.org/docs/content-api/#filtering)

