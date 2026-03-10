---
name: use-screenshot
description: Get the latest screenshot or clipboard image and return a temp file path. Use when the user wants to inspect a screenshot or clipboard image.
---

# Use Screenshot

## Trigger
When the user asks to check the latest screenshot, clipboard image, or a recent downloaded image.

## Usage
- Repo: `node skills/use-screenshot/scripts/screenshot-agent.js`
- Downloads: `node skills/use-screenshot/scripts/screenshot-agent.js --downloads`
- Clipboard only: `node skills/use-screenshot/scripts/screenshot-agent.js --clipboard-only`
- Output is two lines:
  1. source (`clipboard` or original file path)
  2. temp file path (PNG/JPG/JPEG)

## Agent pattern
```bash
out="$(node skills/use-screenshot/scripts/screenshot-agent.js)"
tmp="$(printf "%s\n" "$out" | sed -n '2p')"
```
If `tmp` is empty, treat as not found.

## Notes
- Desktop files are copied to temp then trashed.
- Downloads files are moved to temp (not trashed).
- Clipboard has no copy timestamp; the tool prefers a file modified within ~30s, otherwise clipboard.
- Linux: requires wl-clipboard or xclip for clipboard images.
