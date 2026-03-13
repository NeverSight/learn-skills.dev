---
name: export-chatgpt
description: Export a ChatGPT shared conversation to Markdown or JSON via a share URL.
---

# Export ChatGPT Share

ChatGPT doesn't have a native way to export conversations. Use this skill to export a ChatGPT via share link into agent-friendly Markdown or JSON.

1. In ChatGPT, click Share on the conversation you'd like to export. Note that this makes it public to all who have a link; beware sharing sensitive content!

2. Invoke this skill via coding agent with `$export-chatgpt <chatgpt.com share url>`.

## Usage

Invoke the skill as:

`export-chatgpt <chatgpt.com share url>`

The skill runner should pass the URL as the first argument to the Python script:

`python3 skills/export-chatgpt/scripts/export_chatgpt.py <chatgpt.com share url>`

## Options

- `--format md|json|both` (default: `md`)
- `--out <path>` (file path for `md` or `json`, base path for `both`)
- `--roles user,assistant` (comma-separated roles to include)

## Examples

`export-chatgpt https://chatgpt.com/share/6982c1ad-265c-800b-9f52-103f81d4386e`

`python3 skills/export-chatgpt/scripts/export_chatgpt.py https://chatgpt.com/share/6982c1ad-265c-800b-9f52-103f81d4386e --format json --out ./export.json`

`python3 skills/export-chatgpt/scripts/export_chatgpt.py https://chatgpt.com/share/6982c1ad-265c-800b-9f52-103f81d4386e --format both --out ./export`
