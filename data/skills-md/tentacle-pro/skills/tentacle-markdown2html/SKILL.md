---
name: tentacle-markdown2html
description: Enterprise markdown-to-html renderer via API service. Sends markdown + templateId to api.tentacle.pro and writes returned html locally.
---

# tentacle-markdown2html (Enterprise Edition)

## Purpose

Call enterprise rendering service instead of local renderer:

- Endpoint: `https://api.tentacle.pro/markdown2html`
- Auth: `API_KEY` from `.agents/skills/.env`
- Supports per-request `templateId`

## Runtime

```bash
bun .agents/skills/tentacle-markdown2html/scripts/main.ts <markdown_file> --template <templateId> [options]
```

## Shared .env (`.agents/skills/.env`)

```dotenv
API_KEY=tentacle-xxx
TENTACLE_BASE_URL=https://api.tentacle.pro
```

## Input/Output

- Input: markdown file
- Request payload: `{ markdown, templateId, title? }`
- Output: html file (default same-name `.html`)

## Options

| Flag | Description |
|------|-------------|
| `--template <id>` | Template ID, default `preset-classic` |
| `--output <path>` | Output HTML path |
| `--title <text>` | Title override |
| `--summary <text>` | Article summary (max 120 chars). Injected as `summary:` into frontmatter so the renderer displays it as a themed lead block after the h1. Use this when the markdown has no frontmatter or when the agent dynamically generates a summary. |
| `--dry-run` | Fetch only, skip file write |

## Preprocessing

- Before request, script normalizes Obsidian image embeds like `![[cover.jpg]]` to standard markdown image syntax.
- This keeps enterprise behavior aligned with community flow and ensures downstream image extraction/replacement can work consistently.

## WeChat-Oriented Expectation

- The generated HTML is expected to be consumed by `tentacle-post2wechat`, where:
	- inline images are uploaded with `uploadimg` semantics and rewritten as URL;
	- cover image is uploaded as permanent material and used as `thumb_media_id`.

## Example

```bash
bun .agents/skills/tentacle-markdown2html/scripts/main.ts 02\ Projects/article.md \
  --template preset-classic \
  --summary "早餐是一个向量空间。煎饼、可丽饼和炒蛋安置在一个单纯形上，是否存在从未被探索的'暗早餐'？"
```
