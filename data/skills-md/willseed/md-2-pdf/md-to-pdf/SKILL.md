---
name: md-to-pdf
description: Convert Markdown files to PDF using a Node.js CLI script. Use when the user asks to export .md content into a .pdf file.
---

# Markdown to PDF (Node.js + TypeScript)

## Quick start

Use the included TypeScript script:

```bash
cd /Users/willseed/GitRepo/skill/md-to-pdf
npm install
npm run convert -- --input /path/to/file.md --output /path/to/file.pdf
```

## Notes

- Required argument: `--input` (or `-i`)
- Optional argument: `--output` (or `-o`)
- If `--output` is omitted, the script writes PDF next to the source markdown file.
- Supports basic markdown rendering: headings, lists, blockquotes, horizontal rules, and fenced code blocks.
