---
name: pdf-composer
description: Generate PDF documents from Markdown with headers/footers.
status: implemented
category: Data & Content
last_updated: '2026-02-13'
tags:
  - automation
  - documentation
  - gemini-skill
---

# Pdf Composer

Generate PDF documents from Markdown with headers/footers.

## Usage

node pdf-composer/scripts/compose.cjs [options]

## Options

| Flag      | Alias | Type   | Required | Description              |
| --------- | ----- | ------ | -------- | ------------------------ |
| `--input` | `-i`  | string | Yes      | Input markdown file path |
| `--out`   | `-o`  | string | Yes      | Output PDF file path     |

## Troubleshooting

| Error                                       | Cause                                 | Fix                                         |
| ------------------------------------------- | ------------------------------------- | ------------------------------------------- |
| `Missing required input markdown file path` | Input file not specified or not found | Check file path with `ls`                   |
| `PDF generation timed out after 30s`        | markdown-pdf failed to render         | Check markdown syntax, reduce document size |
| `Cannot find module 'markdown-pdf'`         | Dependency not installed              | Run `npm install` from project root         |
| `ENOENT: no such file or directory`         | Output directory doesn't exist        | Create the output directory first           |

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
