---
name: fieldtheory-cli-bookmarks
description: Sync, search, classify, and query X/Twitter bookmarks locally using the Field Theory CLI
triggers:
  - sync my Twitter bookmarks
  - search my X bookmarks
  - classify my bookmarks
  - set up fieldtheory cli
  - ft sync bookmarks
  - download all my X bookmarks locally
  - use bookmarks with Claude Code agent
  - schedule bookmark sync
---

# Field Theory CLI — X/Twitter Bookmark Manager

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Field Theory CLI (`ft`) syncs all your X/Twitter bookmarks locally, indexes them for full-text search, classifies them by category and domain, and exposes them to AI agents via shell commands. No official API required for the default sync mode.

## Installation

```bash
npm install -g fieldtheory
```

**Requirements:**
- Node.js 20+
- Google Chrome (logged into X/Twitter) for default sync mode
- macOS for Chrome session sync; Linux/Windows use OAuth mode

Verify installation:

```bash
ft --version
ft status
```

## Quick Start

```bash
# Sync bookmarks (reads Chrome session automatically)
ft sync

# Search immediately
ft search "machine learning"

# Explore with terminal dashboard
ft viz
```

Data is stored at `~/.ft-bookmarks/` by default.

## Core Commands

### Syncing

```bash
# Incremental sync (new bookmarks only)
ft sync

# Sync then auto-classify with LLM
ft sync --classify

# Full history crawl from the beginning
ft sync --full

# Sync via OAuth API (cross-platform, no Chrome needed)
ft sync --api

# Show sync status
ft status
```

### Searching

```bash
# Full-text BM25 search
ft search "distributed systems"
ft search "rust async runtime"
ft search "cancer immunotherapy"

# Filter results
ft list --author elonmusk
ft list --category tool
ft list --domain ai
ft list --since 2024-01-01
ft list --category research --domain biology

# Show a single bookmark by ID
ft show 1234567890
```

### Classification

```bash
# LLM-powered classification (requires LLM access)
ft classify

# Regex-based classification (no LLM needed, faster)
ft classify --regex

# Rebuild search index (preserves existing classifications)
ft index
```

### Exploration & Stats

```bash
# Terminal dashboard with sparklines and charts
ft viz

# Category distribution
ft categories

# Subject domain distribution
ft domains

# Top authors, languages, date range
ft stats

# Print data directory path
ft path
```

### Media

```bash
# Download static images from bookmarks
ft fetch-media
```

## OAuth Setup (Cross-Platform / API Mode)

```bash
# Interactive OAuth setup
ft auth

# Then sync via API
ft sync --api
```

OAuth token stored at `~/.ft-bookmarks/oauth-token.json` with `chmod 600`.

## Configuration

### Custom Data Directory

```bash
# Set in shell profile (~/.zshrc or ~/.bashrc)
export FT_DATA_DIR=/path/to/custom/dir

# Or per-command
FT_DATA_DIR=/Volumes/external/bookmarks ft sync
```

### Data File Layout

```
~/.ft-bookmarks/
  bookmarks.jsonl       # raw bookmarks, one JSON object per line
  bookmarks.db          # SQLite FTS5 search index
  bookmarks-meta.json   # sync cursor and metadata
  oauth-token.json      # OAuth credentials (API mode only)
```

## Scheduling Sync

Add to crontab (`crontab -e`):

```bash
# Sync every morning at 7am
0 7 * * * ft sync

# Sync and classify every morning at 7am
0 7 * * * ft sync --classify

# Full sync every Sunday at midnight
0 0 * * 0 ft sync --full
```

## Categories Reference

| Category | Description |
|----------|-------------|
| `tool` | GitHub repos, CLI tools, npm packages, open-source |
| `security` | CVEs, vulnerabilities, exploits, supply chain |
| `technique` | Tutorials, demos, code patterns, how-to threads |
| `launch` | Product launches, announcements, "just shipped" |
| `research` | ArXiv papers, studies, academic findings |
| `opinion` | Takes, analysis, commentary, threads |
| `commerce` | Products, shopping, physical goods |

## Working with Bookmark Data (TypeScript/Node.js)

The `bookmarks.jsonl` file can be consumed directly in scripts:

```typescript
import { createReadStream } from "fs";
import { createInterface } from "readline";
import { homedir } from "os";
import { join } from "path";

interface Bookmark {
  id: string;
  text: string;
  author: string;
  created_at: string;
  url: string;
  category?: string;
  domain?: string;
  media?: string[];
}

async function loadBookmarks(): Promise<Bookmark[]> {
  const dataDir = process.env.FT_DATA_DIR ?? join(homedir(), ".ft-bookmarks");
  const filePath = join(dataDir, "bookmarks.jsonl");

  const bookmarks: Bookmark[] = [];
  const rl = createInterface({
    input: createReadStream(filePath),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    if (line.trim()) {
      bookmarks.push(JSON.parse(line));
    }
  }

  return bookmarks;
}

// Usage
const bookmarks = await loadBookmarks();
const tools = bookmarks.filter((b) => b.category === "tool");
console.log(`Found ${tools.length} tool bookmarks`);
```

### Query SQLite Index Directly

```typescript
import Database from "better-sqlite3";
import { join } from "path";
import { homedir } from "os";

const dataDir = process.env.FT_DATA_DIR ?? join(homedir(), ".ft-bookmarks");
const db = new Database(join(dataDir, "bookmarks.db"), { readonly: true });

// Full-text search using SQLite FTS5
function searchBookmarks(query: string, limit = 20) {
  const stmt = db.prepare(`
    SELECT id, text, author, created_at, category, domain
    FROM bookmarks
    WHERE bookmarks MATCH ?
    ORDER BY rank
    LIMIT ?
  `);
  return stmt.all(query, limit);
}

// Filter by category
function getByCategory(category: string) {
  const stmt = db.prepare(`
    SELECT * FROM bookmarks WHERE category = ? ORDER BY created_at DESC
  `);
  return stmt.all(category);
}

const results = searchBookmarks("transformer architecture");
console.log(results);
```

### Shell Integration in Agent Scripts

```typescript
import { execSync } from "child_process";

// Run ft commands from Node.js
function ftSearch(query: string): string {
  return execSync(`ft search "${query}"`, { encoding: "utf8" });
}

function ftList(options: { category?: string; since?: string; author?: string }) {
  const flags = [
    options.category ? `--category ${options.category}` : "",
    options.since ? `--since ${options.since}` : "",
    options.author ? `--author ${options.author}` : "",
  ]
    .filter(Boolean)
    .join(" ");

  return execSync(`ft list ${flags}`, { encoding: "utf8" });
}

// Example: find AI memory tools bookmarked this year
const memoryTools = ftSearch("AI memory");
const recentTools = ftList({ category: "tool", since: "2025-01-01" });
```

## Agent Integration Patterns

Tell your AI agent to use `ft` directly in natural language:

```
"Search my bookmarks for distributed tracing tools and summarize the top 5."

"Sync any new X bookmarks, then list all research papers from 2025."

"Find everything I've bookmarked about Rust and categorize it by subtopic."

"Every morning, run ft sync --classify to keep my bookmarks up to date."
```

Claude Code example prompt:
```
Use the `ft` CLI to search my bookmarks for "vector database" 
and pick the best open-source option to add to this project.
Run: ft search "vector database" --category tool
```

## Troubleshooting

### Chrome session not found
```bash
# Ensure Chrome is open and logged into X
# Then retry
ft sync

# If Chrome session still fails, use OAuth mode
ft auth
ft sync --api
```

### Sync stalls or returns 0 bookmarks
```bash
# Check sync status and metadata
ft status

# Force full re-crawl
ft sync --full

# Check data directory permissions
ls -la ~/.ft-bookmarks/
```

### Search returns no results
```bash
# Rebuild the search index
ft index

# Verify bookmarks exist
ft stats
wc -l ~/.ft-bookmarks/bookmarks.jsonl
```

### Classification not running
```bash
# LLM classify requires an LLM — use regex fallback
ft classify --regex

# Or sync with regex classify
ft sync --classify --regex
```

### Reset all data
```bash
rm -rf ~/.ft-bookmarks
ft sync
```

### Custom data directory issues
```bash
# Confirm the env var is set
echo $FT_DATA_DIR
ft path

# Ensure directory is writable
mkdir -p "$FT_DATA_DIR"
chmod 755 "$FT_DATA_DIR"
```

## Security Notes

- All data is **local only** — no telemetry or external calls except to X during sync
- Chrome cookies are read temporarily for sync and never stored separately
- OAuth token is stored `chmod 600` — treat it like a password
- Default sync uses X's internal GraphQL API (same as browser); `--api` uses official v2 API

## Platform Support

| Feature | macOS | Linux | Windows |
|---------|-------|-------|---------|
| `ft sync` (Chrome session) | ✅ | ❌ | ❌ |
| `ft sync --api` (OAuth) | ✅ | ✅ | ✅ |
| Search, classify, viz | ✅ | ✅ | ✅ |

Linux/Windows users must run `ft auth` first, then use `ft sync --api`.

## Resources

- Homepage: [fieldtheory.dev/cli](https://fieldtheory.dev/cli)
- Repository: [github.com/afar1/fieldtheory-cli](https://github.com/afar1/fieldtheory-cli)
- License: MIT
