---
name: confluence-dc
description: Manage Confluence Data Center documentation with downloads, uploads, conversions, and diagrams. Use when asked to "download Confluence pages", "upload to Confluence", "convert Wiki Markup", "create Confluence page", "create Confluence blogpost", or "handle Confluence images".
---

# Confluence Data Center Management Skill

Manage Confluence Data Center documentation through Claude Code: download pages to Markdown, upload large documents with images, convert between formats, and integrate Mermaid/PlantUML diagrams.

## Table of Contents

- [Quick Decision Matrix](#quick-decision-matrix)
- [MCP Size Limits](#mcp-size-limits)
- [Prerequisites](#prerequisites)
- [Core Workflows](#core-workflows)
- [Reference Documentation](#reference-documentation)

## Quick Decision Matrix

| Task | Tool | Notes |
|------|------|-------|
| Read pages | MCP tools | `confluence_getContent`, `confluence_searchContent` |
| Small text-only uploads (<10KB) | MCP tools | `confluence_createContent`, `confluence_updateContent` |
| Large documents (>10KB) | `upload_confluence_v2.py` | REST API, no size limits |
| Documents with images | `upload_confluence_v2.py` | Handles attachments automatically |
| Create blogpost | `upload_confluence_v2.py --type blogpost` | Or MCP with `type: "blogpost"` |
| Download pages to Markdown | `download_confluence.py` | Converts macros, downloads attachments |
| Download page to Markdown (lightweight) | `download_long_page.py` | Stdlib + html2text only, no heavy deps |

## MCP Size Limits

MCP tools have size limits (10-20KB) for uploads. For large documents or pages with images, use the REST API via `upload_confluence_v2.py`:

```bash
# Upload large document
python3 ~/.claude/skills/confluence-dc/scripts/upload_confluence_v2.py \
    document.md --id 780369923

# Dry-run preview
python3 ~/.claude/skills/confluence-dc/scripts/upload_confluence_v2.py \
    document.md --id 780369923 --dry-run
```

MCP works for reading pages but not for uploading large content.

## Prerequisites

### Required

- **Confluence Data Center MCP Server** (`compasify-confluence-dc`) with PAT-based authentication.
- **npm package**: `@compasify/confluence-dc`

### Optional

- **Mermaid CLI**: Diagram rendering (`npm install -g @mermaid-js/mermaid-cli`)

## Core Workflows

### Download Pages to Markdown

```bash
# Single page
python3 ~/.claude/skills/confluence-dc/scripts/download_confluence.py 123456789

# With child pages
python3 ~/.claude/skills/confluence-dc/scripts/download_confluence.py --download-children 123456789

# Custom output directory
python3 ~/.claude/skills/confluence-dc/scripts/download_confluence.py --output-dir ./docs 123456789
```

See [Downloading Guide](references/conversion_guide.md) for details.

### Upload Pages/Blogposts with Images

1. Convert diagrams to images first using `design-doc-mermaid` or `plantuml` skills
2. Reference images with standard markdown: `![Description](./images/diagram.png)`
3. Upload via REST API:

```bash
# Upload as page (default)
python3 ~/.claude/skills/confluence-dc/scripts/upload_confluence_v2.py \
    document.md --id PAGE_ID

# Upload as blogpost
python3 ~/.claude/skills/confluence-dc/scripts/upload_confluence_v2.py \
    document.md --space ARCP --type blogpost
```

See [Image Handling Best Practices](references/image_handling_best_practices.md) for details.

### Search Confluence

```javascript
confluence_searchContent({
  cql: 'space = "DEV" AND text ~ "API"',
  limit: 10
})
```

### Create/Update Pages & Blogposts (Small Documents)

Note: Content format for these tools is Confluence storage format (XML-based), not wiki markup.

```javascript
// Create page
confluence_createContent({
  spaceKey: "DEV",
  title: "API Documentation",
  content: "<h1>Overview</h1><p>Content here...</p>",
  type: "page"
})

// Create blogpost
confluence_createContent({
  spaceKey: "DEV",
  title: "Release Notes v2.0",
  content: "<h1>What's New</h1><p>Content here...</p>",
  type: "blogpost"
})

// Update page
// CRITICAL: updateContent requires explicit version number (fetch current + increment)
confluence_updateContent({
  contentId: "123456789",
  title: "Updated Title",
  content: "<h1>New Content</h1><p>Updated content...</p>",
  version: 2,
  versionComment: "Updated via Claude Code"
})
```

### DC-Specific Notes
- **Authentication**: Uses Personal Access Token (PAT). Ensure `CONFLUENCE_API_TOKEN` is set.
- **SSL**: If using self-signed certificates, ensure appropriate environment variables are configured to allow the connection.
- **Code Blocks**: In Confluence Data Center, `json` language is NOT supported in code blocks. Use `javascript` instead.

### Convert Between Formats

See [Conversion Guide](references/conversion_guide.md) for the complete conversion matrix.

Quick reference:

| Markdown | Wiki Markup |
|----------|-------------|
| `# Heading` | `h1. Heading` |
| `**bold**` | `*bold*` |
| `*italic*` | `_italic_` |
| `` `code` `` | `{{code}}` |
| `[text](url)` | `[text|url]` |

## Reference Documentation

Detailed guides in the `references/` directory:

| Guide | Purpose |
|-------|---------|
| [Wiki Markup Reference](references/wiki_markup_guide.md) | Complete syntax for Confluence Wiki Markup |
| [Conversion Guide](references/conversion_guide.md) | Markdown to Wiki Markup conversion rules |
| [Storage Format](references/confluence_storage_format.md) | Confluence XML storage format details |
| [Image Handling](references/image_handling_best_practices.md) | Workflows for images, Mermaid, PlantUML |
| [Troubleshooting](references/troubleshooting_guide.md) | Common errors and solutions |

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `confluence_getContent` | Get content by ID |
| `confluence_searchContent` | Search with CQL |
| `confluence_createContent` | Create page/blogpost |
| `confluence_updateContent` | Update content (version REQUIRED) |
| `confluence_searchSpace` | Search spaces |
| `confluence_deletePage` | Delete page |
| `confluence_getPageChildren` | Get child pages |
| `confluence_getLabels` | Get labels |
| `confluence_addLabel` | Add label |
| `confluence_getComments` | Get comments |

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `scripts/upload_confluence_v2.py` | Upload large documents with images (supports `--type page\|blogpost`) |
| `scripts/upload_confluence.py` | Upload with frontmatter support (supports `--type page\|blogpost`) |
| `scripts/download_confluence.py` | Download pages to Markdown |
| `scripts/convert_markdown_to_wiki.py` | Convert Markdown to Wiki Markup |
| `scripts/render_mermaid.py` | Render Mermaid diagrams |
| `scripts/download_long_page.py` | Lightweight single-page downloader (stdlib + html2text) |
---

**Version**: 3.2.0 | **Last Updated**: 2026-03-02
