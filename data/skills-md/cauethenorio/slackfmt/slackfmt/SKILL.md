---
name: slackfmt
description: Use when formatting or copying content, markdown or plain text, for Slack with rich text preserved
---

# slackfmt

Convert markdown (or HTML) to Slack's native rich text format and copy to clipboard. When pasted into Slack, all formatting (bold, italic, lists, code blocks, links, blockquotes) is preserved.

## When to Use

- User wants to format a message for Slack
- User wants to copy formatted content to clipboard for pasting into Slack
- User has markdown, HTML, or Quill Delta content destined for Slack
- User asks to "copy to Slack", "format for Slack", or "paste into Slack"

**Slack limitations:** Headings are converted to bold text. Only basic formatting is supported (bold, italic, strikethrough, code, links, lists, blockquotes, code blocks).

## CLI Usage

```bash
# Pipe content to slackfmt (copies to clipboard by default)
echo "**bold** and _italic_" | npx @slackfmt/cli@latest

# Specify input format explicitly
echo "<b>hello</b>" | npx @slackfmt/cli@latest -f html

```

**Flags:**

- `-f, --format` — Input format: `markdown` (default), `html`, `slack-html`, `quill-delta`
- `--stdout` — Print Quill Delta JSON to stdout instead of copying to clipboard

**Format auto-detection:** If no `-f` flag, slackfmt detects JSON (quill-delta), HTML tags (html), or falls back to markdown.

## Instructions

1. Compose the content as markdown in an `echo` or `printf` command
2. Pipe it to `npx @slackfmt/cli@latest`
3. The formatted content is copied to the system clipboard
4. User can paste directly into Slack with formatting preserved

### Example

```bash
echo '- **Performance**
  - Dashboard speed improvements
  - 90% faster queries
- **Bug Fixes**
  - Fixed mobile layout issue' | npx @slackfmt/cli@latest
```

### Tips

- Use `*` for bold, `_` for italic (Slack conventions)
- Nested lists work — use 2-space indentation
- Links: `[text](url)` becomes clickable in Slack
- Code blocks: use triple backticks
- Blockquotes: use `>`
- Headings (`#`, `##`, etc.) are converted to bold paragraphs
