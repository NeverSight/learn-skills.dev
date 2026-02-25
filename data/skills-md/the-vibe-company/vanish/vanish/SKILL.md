---
name: vanish
description: Upload and share files via temporary public URLs using the Vanish CLI (vanish-cli). Use when the user wants to upload files, share screenshots or images, get a public URL for a file, manage temporary file uploads, or embed images in markdown/PRs. Triggers on file sharing, temporary links, screenshot uploads, and vanish commands.
---

# Vanish CLI

Upload files to get temporary public URLs. Install with `npm i -g vanish-cli` or use `npx vanish-cli`.

## Upload

```bash
vanish screenshot.png                    # shorthand for vanish upload
vanish upload file1.png file2.jpg        # multiple files
vanish upload image.png --md             # markdown: ![image.png](url)
vanish upload data.json --json           # JSON: { url, id, filename, size, expires }
vanish upload file.png --no-clipboard    # don't copy URL to clipboard
vanish upload report.pdf --days 90       # custom retention: Pro only, 1-365 days
```

Use `npx vanish-cli` instead of `vanish` when not globally installed.

- Default output is the public URL, automatically copied to clipboard.
- `--md` produces `![filename](url)` — use when embedding in PR descriptions, issues, or markdown files.
- `--json` returns `{ url, id, filename, size, expires }` — use when metadata is needed.
- `--days N` sets custom retention in days (Pro tier only, 1-365).

## Tier Limits

| Tier | File types | Retention | Max Size | Rate Limit |
|------|------------|-----------|----------|------------|
| Anonymous (no login) | Images only | 24 hours | 5 MB | 10/hour |
| Free (`vanish login`) | All (except executables) | 48 hours | 50 MB | 50/hour |
| Pro (`vanish upgrade`) | All (except executables) | 30 days (up to 365 with `--days`) | 1 GB | 200/hour |

Blocked extensions: `.exe`, `.bat`, `.cmd`, `.com`, `.msi`, `.scr`, `.sh`, `.bash`, `.ps1`, `.psm1`.

## Account Commands

```bash
vanish login       # GitHub OAuth (opens browser, saves key)
vanish whoami      # show username and tier
vanish status      # show storage usage, tier, and limits
vanish logout      # remove saved API key
vanish upgrade     # open Stripe checkout for Pro (2 EUR/month)
```

## Upload Management (requires login)

```bash
vanish ls             # list uploads (table: ID | Filename | Size | Expires | URL)
vanish ls --json      # list as JSON array
vanish rm <id>        # delete upload by ID
vanish rm id1 id2     # delete multiple
```

## Configuration

Config file: `~/.config/vanish/config.json` (keys: `api_key`, `api_url`).
Env vars: `VANISH_API_KEY`, `VANISH_API_URL`.
Default API: `https://vanish.sh`.
Priority: env vars > config file > defaults.
