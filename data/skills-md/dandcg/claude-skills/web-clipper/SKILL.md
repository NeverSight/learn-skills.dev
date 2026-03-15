---
name: web-clipper
description: Clip web pages to clean markdown for later reading and search. Use when needing to save a URL, bookmark an article, clip a page, build a read-later collection, or archive web content. Trigger on phrases like "clip this", "save this page", "bookmark", "read later", "web clip", "save article".
---

# Web Clipper

Save any web page as clean markdown with YAML frontmatter. Optionally search your clips or ingest them into repo-search for semantic search.

## Prerequisites

- Python 3 with venv
- Docker (optional, for FlareSolverr fallback on Cloudflare-protected sites)

## Setup

### First-Time Setup

```bash
~/.claude/skills/web-clipper/setup.sh
```

This creates a `.venv` and installs dependencies (trafilatura, requests, python-slugify, pyyaml).

## Usage

### Clip a URL

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url>
```

With tags:

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url> --tags "python,web-dev"
```

Force FlareSolverr (for Cloudflare-protected sites):

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url> --force-flaresolverr
```

JSON output:

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url> -f json
```

Clips are saved to `~/web-clips/` as markdown files with YAML frontmatter (title, url, domain, author, date, tags).

### List Clips

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py
```

Filter by domain, tag, or date:

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py --domain "example.com"
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py --tag "python"
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py --after 2026-01-01 --before 2026-02-01
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py -f json
```

### Search Clips

Full-text search across all clips:

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/search.py "search terms"
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/search.py "search terms" -f json
```

### Delete a Clip

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/delete.py <filename>
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/delete.py --url "https://example.com/article"
```

### Ingest into Repo Search (semantic search)

Requires the repo-search skill. Pushes all clips into ChromaDB:

```bash
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/ingest.py
```

After ingestion, clips are searchable via repo-search:

```bash
~/.claude/skills/repo-search/.venv/bin/python ~/.claude/skills/repo-search/query.py "query" --collection web-clips
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Could not extract article content` | Page has no extractable article text (e.g., SPA, login wall) | Try `--force-flaresolverr` for JS-rendered pages |
| `FlareSolverr error` | FlareSolverr container not running | Run `~/.claude/skills/flaresolverr/scripts/flaresolverr-ensure.sh` |
| `repo-search skill not found` | repo-search not installed | Run `./install.sh repo-search` |

## Limitations

- Extracts article text only — does not preserve images, videos, or interactive elements
- JavaScript-rendered SPAs may need FlareSolverr for content extraction
- Login-walled content cannot be accessed
