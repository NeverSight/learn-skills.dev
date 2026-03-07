---
name: defuddle
description: Extract clean article content from web pages or local HTML files. Removes clutter (ads, sidebars, nav) and returns readable content with metadata.
trigger: Use when user wants to extract/clean web page content, strip clutter from HTML, get article text from a URL, or convert web pages to clean markdown. Triggers include "defuddle", "extract article", "clean this page", "get content from URL", "strip clutter", "web extract".
---

# Defuddle - Web Content Extraction

Extract main article content from web pages, removing ads, sidebars, navigation, and other clutter. Output clean Markdown with metadata.

## Prerequisites

Before first use, check if `defuddle` is installed:

```bash
command -v defuddle >/dev/null 2>&1 || npm install -g defuddle jsdom
```

## Default Workflow

When user provides a URL, follow this workflow:

### Step 1: Extract content as Markdown + JSON metadata

Always use both `-m` and `-j` flags to get markdown content with full metadata:

```bash
defuddle parse "<url>" -m -j
```

### Step 2: Present a summary to the user

Show the user:
- **Title**: from JSON `title` field
- **Author**: from JSON `author` field
- **Source**: domain
- **Word count**: from JSON `wordCount` field
- A brief preview (first 2-3 sentences)

### Step 3: Ask where to save

If this is the **first time** using defuddle in this conversation, ask the user:
> "Save to which directory? (e.g. `~/Documents`, `~/Desktop`, or a custom path)"

Remember the user's chosen directory for subsequent uses in the same conversation.

### Step 4: Save as Markdown file

Write the file with frontmatter + full content:

```markdown
---
title: {title}
author: {author}
source: {url}
date: {published or "Unknown"}
clipped: {today's date YYYY-MM-DD}
wordCount: {wordCount}
---

# {title}

{markdown content}
```

**File naming**: Use the article title as filename, sanitized for filesystem:
- Replace special characters with spaces
- Trim whitespace
- Example: `The Shape of the Essay Field.md`

### Step 5: Confirm to user

Tell the user the file path where it was saved.

## CLI Reference

```bash
defuddle parse <source> [options]
```

**Arguments:**
- `<source>` — URL (`https://...`) or local HTML file path

**Options:**
| Flag | Description |
|------|-------------|
| `-m, --markdown` | Convert content to Markdown |
| `-j, --json` | Output as JSON with full metadata |
| `-o, --output <file>` | Write to file instead of stdout |
| `-p, --property <name>` | Extract single property (title, description, domain, author, published, wordCount, content) |
| `--debug` | Verbose logging |

## JSON Response Fields

When using `-j`, the response includes:
- `title` — Article title
- `author` — Author name
- `published` — Publication date
- `description` — Meta description
- `content` — Extracted Markdown (when `-m` used)
- `domain` — Source domain
- `favicon` — Favicon URL
- `image` — Featured image URL
- `site` — Site name
- `wordCount` — Word count
- `parseTime` — Processing time in ms

## Notes
- Requires Node.js and npm
- `jsdom` is required as a peer dependency
- Works best with article-style pages (blogs, news, documentation)
- Not designed for SPAs or JavaScript-heavy pages (e.g. WeChat articles need browser rendering)
