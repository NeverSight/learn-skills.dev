---
name: blink-cms
description: Manage Blink documentation and blog articles via the Blink MCP. Create, edit, publish, and version control MDX content on blink.new. Use when the user asks to update docs, write blog posts, or manage content on Blink.
---

# Blink CMS via MCP

Publish and manage content on blink.new using the `user-blink-mcp` server. The MCP treats the Blink CMS like a virtual file system with built-in versioning and draft management.

## Quick Reference

| Task | Tool | Key Params |
|------|------|------------|
| List content | `cms_list_dir` | `path: "docs"` or `"blog"` |
| Read article | `cms_read_file` | `path: "blog/article.mdx"` |
| Create/Update | `cms_write_file` | `path`, `content`, `publish` |
| Edit section | `cms_search_replace` | `path`, `old_string`, `new_string` |
| Publish | `cms_publish` | `paths: ["blog/x.mdx"]` |
| Find text | `cms_grep` | `query`, `type` |
| Semantic search | `cms_search` | `query`, `type` |
| See drafts | `cms_list_drafts` | `type` |
| Version history | `cms_get_versions` | `path` |

## Content Structure

```
/docs/              → Documentation (quickstart, pricing, reference, etc.)
/docs/build/        → Build guides (prompting, tutorials, web-apps)
/docs/extend/       → Backend features (database, auth, storage)
/docs/launch/       → Deployment (domains, analytics)
/blog/              → Blog articles
```

## Frontmatter Schema

Every article must include frontmatter:

```yaml
---
title: "Article Title"
description: "Brief summary for SEO and cards"
category: "Engineering"        # Product, Engineering, Tutorial, Case Study
tags: ["AI", "Productivity"]   # Free-form array
status: "published"            # Overridden by publish action
---
```

**Categories:**
- `Product` — Announcements, launches, feature updates
- `Engineering` — Technical deep-dives, best practices
- `Tutorial` — Step-by-step guides
- `Case Study` — Customer success stories

## Creating a New Article

```
cms_write_file(
  path: "blog/my-article.mdx",
  content: ---
title: "My Article Title"
description: "What this article is about"
category: "Engineering"
tags: ["AI", "Tips"]
---

## Introduction

Your content here with MDX components.

<Tip>Helpful tips use the Tip component.</Tip>
,
  publish: false    # Save as draft first
)
```

Then publish when ready:
```
cms_publish(paths: ["blog/my-article.mdx"])
```

## Editing Existing Articles

**Method 1: Full rewrite** (use sparingly)
```
cms_write_file(path: "blog/article.mdx", content: "...full content...", publish: true)
```

**Method 2: Surgical edit** (preferred)
```
cms_search_replace(
  path: "blog/article.mdx",
  old_string: "## Introduction\n\nOld text here",
  new_string: "## Introduction\n\nNew text here"
)
```

Include 3-5 lines of context for unique matches. Flexible whitespace matching handles indentation differences automatically.

## Finding Content

**Fuzzy text search** (finds exact phrases):
```
cms_grep(query: "deployment", type: "blog", limit: 10)
```

**Semantic search** (finds by meaning):
```
cms_search(query: "how to deploy apps", type: "blog")
```

## Version Control

```
# See all versions
cms_get_versions(path: "blog/article.mdx")

# Restore a specific version
cms_activate_version(path: "blog/article.mdx", version: 3)
```

## Draft Workflow

```
# Check for unpublished changes
cms_list_drafts(type: "blog")

# Discard draft (revert to last published)
cms_discard_draft(path: "blog/article.mdx")
```

## MDX Components

Common components for rich content:

```mdx
<Tip>Helpful tip text</Tip>
<Note>Informational note</Note>
<Warning>Caution about something</Warning>

<Steps>
  <Step title="First Step">Instructions</Step>
  <Step title="Second Step">More instructions</Step>
</Steps>

<CodeGroup>
  <CodeTab title="JavaScript">code here</CodeTab>
  <CodeTab title="Python">code here</CodeTab>
</CodeGroup>

<CardGroup cols={2}>
  <Card title="Feature Name" href="/docs/path" icon="Star">
    Brief description
  </Card>
</CardGroup>

<AccordionGroup>
  <Accordion title="Question?">Answer content</Accordion>
</AccordionGroup>
```

## Workflow Best Practices

1. **Read before editing**: Always `cms_read_file` first to understand current content
2. **Use surgical edits**: Prefer `cms_search_replace` over full rewrites
3. **Preview drafts**: Set `publish: false` to save drafts, review, then `cms_publish`
4. **Version awareness**: `cms_publish` creates version snapshots—use for rollback safety
5. **Search first**: Use `cms_grep` to find exact text before `cms_search_replace`

## Complete Publishing Workflow

```
1. cms_list_dir(path: "blog")           → See current articles
2. cms_write_file(path, content, false) → Create/update as draft
3. cms_read_file(path)                  → Review the saved content
4. cms_publish(paths: [path])           → Go live with version snapshot
```

## MCP Server Name

All tools are accessed via the `user-blink-mcp` server:

```
server: "user-blink-mcp"
toolName: "cms_list_dir"
arguments: { "path": "blog" }
```
