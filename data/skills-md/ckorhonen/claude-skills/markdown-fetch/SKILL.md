---
name: markdown-fetch
description: Fetch and extract web content as clean Markdown when provided with URLs. Use this skill whenever a user provides a URL (http/https link) that needs to be read, analyzed, summarized, or extracted. Converts web pages to Markdown with 80% fewer tokens than raw HTML. Handles all content types including JS-heavy sites, documentation, articles, and blog posts. Supports three conversion methods (auto, AI, browser rendering). Always use this instead of web_fetch when working with URLs - it's more efficient and provides cleaner output.
---

# Markdown Fetch

Efficiently fetch web content as clean Markdown using the markdown.new service.

## Why Use This

- **80% fewer tokens** than raw HTML
- **5x more content** fits in context window  
- **No external dependencies** or parsing libraries needed
- **Three-tier conversion** (Markdown-first, AI fallback, browser rendering)

## Triggering

This skill should trigger automatically when:
- User provides a URL (e.g., "Read https://example.com")
- User asks to extract/fetch/analyze web content
- User requests summarization of a webpage
- User needs to process article/blog/documentation URLs

## Quick Start

```bash
# Fetch any URL
scripts/fetch.sh "https://example.com"

# Use browser rendering for JS-heavy sites
scripts/fetch.sh "https://example.com" --method browser

# Retain images in output
scripts/fetch.sh "https://example.com" --retain-images
```

## Typical Usage Patterns

When a user says:
- "Read this article: https://..." → Use this skill to fetch the content
- "Summarize https://..." → Fetch with this skill first, then summarize
- "What does this page say: https://..." → Fetch the content
- "Extract the text from https://..." → Use this skill

## Conversion Methods

**auto** (default) - Try Markdown-first, fall back to AI or browser as needed  
**ai** - Use Cloudflare Workers AI for conversion  
**browser** - Full browser rendering for JS-heavy content

## Options

`--method <auto|ai|browser>` - Conversion method  
`--retain-images` - Keep image references in output  
`--output <file>` - Save to file instead of stdout

## Output

Returns clean Markdown with metadata:

```markdown
---
title: Page Title
tokens: 725
---

# Content here...
```

## When to Use

- Extracting articles, documentation, or blog posts
- Building RAG pipelines with web content
- Summarizing web pages
- Fetching content for analysis
- Converting sites to Markdown format

## Implementation Notes

The service handles:
- Content negotiation (Accept: text/markdown)
- Cloudflare Workers AI conversion
- Browser rendering for dynamic content
- Automatic fallback between methods