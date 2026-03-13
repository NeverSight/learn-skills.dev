---
name: arcfetch
description: Use when working with arcfetch CLI for URL fetching, article extraction, and cache management. Triggers on fetching URLs, batch processing, managing cached references, promoting/deleting content, extracting/fetching links, or integrating arcfetch into automation pipelines.
---

# arcfetch

Guide for using the arcfetch CLI to fetch web content, extract articles as clean markdown, and manage cached references.

## Overview

arcfetch converts web pages to clean markdown with:
- Automatic Playwright fallback when simple HTTP fetch produces low-quality results
- Quality scoring (0-100) with boilerplate/error page/login wall/paywall detection
- Content-to-source ratio analysis to catch JS-rendered or gated content
- Anti-bot detection measures (stealth plugin, viewport/timezone rotation, realistic headers)

## Installation

```bash
# Use via bunx (no install needed)
bunx arcfetch <command>

# Or install globally
bun install -g arcfetch
```

## Commands

### fetch

Fetch a URL and save extracted markdown to the temp folder.

```bash
arcfetch fetch <url> [options]
```

**Options:**
- `-q, --query <text>` - Search query (saved as metadata)
- `-o, --output <format>` - Output format:
  - `text` - Plain text, LLM-friendly (default)
  - `json` - Structured JSON
  - `path` - Just the filepath
  - `summary` - slug|filepath format
- `--pretty` - Human-friendly output with emojis
- `-v, --verbose` - Show detailed output (quality scores, pipeline decisions)
- `--min-quality <n>` - Minimum quality score 0-100 (default: 60)
- `--temp-dir <path>` - Temp folder (default: .tmp/arcfetch)
- `--docs-dir <path>` - Docs folder (default: docs/ai/references)
- `--wait-strategy <mode>` - Playwright wait: networkidle (default), domcontentloaded, load
- `--force-playwright` - Skip simple fetch, use Playwright directly
- `--refetch` - Re-fetch even if URL already cached

**Examples:**

```bash
# Basic fetch (plain text output for LLMs)
arcfetch fetch https://example.com/article

# Get just the filepath
arcfetch fetch https://example.com -o path

# Human-friendly output
arcfetch fetch https://example.com --pretty

# JSON output for scripting
arcfetch fetch https://example.com -o json

# With search query metadata
arcfetch fetch https://example.com -q "search term"

# Verbose mode to see pipeline decisions
arcfetch fetch https://example.com -v

# Force Playwright for JS-heavy sites
arcfetch fetch https://example.com --force-playwright
```

**Quality Pipeline:**
1. Simple HTTP fetch with browser-like User-Agent
2. Extract content with Readability + Turndown
3. Quality score (0-100) with boilerplate detection
4. Score >= 85: accept as-is
5. Score 60-84: try Playwright, use whichever scores higher
6. Score < 60: require Playwright, fail if still below threshold

### list

List all cached references.

```bash
arcfetch list [options]
```

**Options:**
- `-o, --output <format>` - Output format: text, json
- `--pretty` - Human-friendly output

```bash
arcfetch list --pretty
arcfetch list -o json
```

### links

Extract all links from a cached reference.

```bash
arcfetch links <ref-id> [options]
```

**Options:**
- `-o, --output <format>` - Output format: text, json
- `--pretty` - Human-friendly output

```bash
arcfetch links my-article --pretty
arcfetch links my-article -o json
```

### fetch-links

Fetch all links from a cached reference (parallel, max 5 concurrent).

```bash
arcfetch fetch-links <ref-id> [options]
```

**Options:**
- `--refetch` - Force re-fetch even if already cached
- `-o, --output <format>` - Output format: text, json
- `--pretty` - Human-friendly output

```bash
arcfetch fetch-links my-article --pretty
```

### promote

Move reference from temp to permanent docs folder.

```bash
arcfetch promote <ref-id> [options]
```

```bash
arcfetch promote my-article --pretty
arcfetch promote my-article -o json
```

### delete

Delete a cached reference.

```bash
arcfetch delete <ref-id> [options]
```

```bash
arcfetch delete my-article --pretty
```

### config

Show current configuration.

```bash
arcfetch config
```

### mcp

Start the MCP server (for Claude Code integration).

```bash
arcfetch mcp
```

## Workflow Patterns

### Single Article

```bash
arcfetch fetch https://example.com/guide --pretty
cat .tmp/arcfetch/example-guide.md  # Review content
arcfetch promote example-guide      # Move to docs if good
```

### Batch Fetch

```bash
for url in "url1" "url2" "url3"; do
  arcfetch fetch "$url" --pretty
done
arcfetch list --pretty         # Review all
arcfetch promote my-article    # Promote desired ones
```

### Fetch All Links from a Page

```bash
arcfetch fetch https://example.com/resources --pretty
arcfetch links resources --pretty           # See what links exist
arcfetch fetch-links resources --pretty     # Fetch them all
```

### Scripting with JSON Output

```bash
RESULT=$(arcfetch fetch https://example.com -o json)
REF_ID=$(echo "$RESULT" | jq -r '.refId')
QUALITY=$(echo "$RESULT" | jq -r '.quality')

if (( QUALITY >= 85 )); then
  arcfetch promote "$REF_ID"
fi
```

### Cleanup

```bash
arcfetch list --pretty
arcfetch delete unwanted-ref
```

## Configuration

### Priority Order

1. CLI arguments
2. Environment variables
3. `arcfetch.config.json`
4. `.arcfetchrc` / `.arcfetchrc.json`
5. Built-in defaults

### Config File (`arcfetch.config.json`)

```json
{
  "quality": {
    "minScore": 60,
    "jsRetryThreshold": 85
  },
  "paths": {
    "tempDir": ".tmp/arcfetch",
    "docsDir": "docs/ai/references"
  },
  "playwright": {
    "timeout": 30000,
    "waitStrategy": "networkidle"
  }
}
```

### Environment Variables

```bash
export SOFETCH_MIN_SCORE=60
export SOFETCH_TEMP_DIR=".tmp/arcfetch"
export SOFETCH_DOCS_DIR="docs/ai/references"
```

## Quality Scoring

Score starts at 100 and deductions apply:

| Check | Deduction | Severity |
|-------|-----------|----------|
| Blank content | Score = 0 | Issue |
| Content < 50 chars | -50 | Issue |
| Content < 300 chars | -15 | Warning |
| HTML tags > 100 | -40 | Issue |
| HTML tags > 50 | -20 | Warning |
| HTML tags > 10 | -5 | Warning |
| HTML ratio > 30% | -25 | Issue |
| HTML ratio > 15% | -10 | Warning |
| Table tags > 50 | -30 | Issue |
| Script tags present | -15 | Warning |
| Style tags present | -10 | Warning |
| Extraction ratio < 0.5% (from large page) | -35 | Issue |
| Extraction ratio < 2% (from large page) | -20 | Warning |
| Boilerplate detected (error/login/paywall) | -40 | Issue |
| Excessive newlines | -5 | Warning |

**Boilerplate patterns detected** (on short content < 2000 chars):
- Error pages: "something went wrong", "an error occurred", "unexpected error"
- 404 pages: "page not found", "404 not found"
- Login walls: "log in to continue", "please log in", "sign in to continue"
- Paywalls: "subscribe to continue reading"
- Bot detection: "are you a robot", "complete the captcha", "verify you are human"
- Access denied, JS-required, unsupported browser pages

**Score thresholds:**
- **>= 90**: Excellent
- **>= 75**: Good
- **>= 60**: Acceptable (minimum to pass)
- **< 60**: Poor (rejected)

## MCP Server

The MCP server exposes 6 tools for Claude Code integration:

| Tool | Description |
|------|-------------|
| `fetch_url` | Fetch URL, extract markdown, save to temp |
| `list_cached` | List all cached references |
| `promote_reference` | Move temp reference to docs folder |
| `delete_cached` | Delete a cached reference |
| `extract_links` | Extract links from a cached reference |
| `fetch_links` | Fetch all links from a cached reference |

Start via CLI: `arcfetch mcp`

Or configure in Claude Code MCP settings to run `bunx arcfetch` as stdio server.

## File Format

Cached files use markdown with YAML frontmatter:

```markdown
---
title: "Article Title"
source_url: https://example.com/article
fetched_date: 2026-02-06
type: web
status: temporary
query: "optional search query"
---

# Article Title

Extracted markdown content...
```

- **Ref IDs** are slugified titles (e.g., `how-to-build-react-apps`)
- **Temp storage**: `.tmp/arcfetch/<slug>.md` (status: temporary)
- **Permanent storage**: `docs/ai/references/<slug>.md` (status: permanent, after promote)
- **Duplicate detection**: re-fetching same URL returns existing ref unless `--refetch`

## References

- Package: https://www.npmjs.com/package/arcfetch
- Repository: https://github.com/briansunter/arcfetch
- MCP Protocol: https://modelcontextprotocol.io
