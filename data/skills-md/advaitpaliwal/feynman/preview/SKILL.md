---
name: preview
description: Preview Markdown, LaTeX, PDF, or code artifacts when preview commands are visible, or fall back to shell/browser tools. Use when the user wants to review a written artifact, export a report, or view a rendered document.
---

# Preview

Use `/preview` only when that command is visible in the active session. If preview commands are unavailable, render or open artifacts with shell/browser tools and report that the preview package is not installed.

## Commands

| Command | Description |
|---------|-------------|
| `/preview` | Preview the most recent artifact in the browser, when available |
| `/preview --file <path>` | Preview a specific file, when available |
| `/preview-browser` | Force browser preview, when available |
| `/preview-pdf` | Export to PDF via pandoc + LaTeX, when available |
| `/preview-clear-cache` | Clear rendered preview cache, when available |

## Fallback

If the preview commands are not available, use bash:

```bash
open <file.md>          # macOS — opens in default app
open <file.pdf>         # macOS — opens in Preview
pandoc input.md -o output.html
pandoc input.md -o output.pdf
```
