---
name: starepo
description: Search GitHub starred repositories with semantic/hybrid search. Trigger when user asks to find, search, or explore their GitHub stars, or wants to recall starred projects by topic, language, or description.
---

# Starepo — GitHub Stars Semantic Search

Use the `starepo` CLI to help users find repositories in their GitHub starred collection through hybrid (vector + full-text) search.

## When to Use

- User asks: "find my starred repos about X", "search my stars for Y"
- User wants to recall a repo they starred but can't remember the name
- User asks to list stars filtered by language, topic, or date
- User wants to see details about a specific starred repo

## Setup (First Time)

Run these steps once. Skip any step that's already done.

```bash
# 1. Authenticate with GitHub (Device Flow — no token needed)
npx starepo auth

# 2. Sync starred repos and generate embeddings automatically
npx starepo sync
```

Check sync status anytime:
```bash
npx starepo list --limit 5
```

## Semantic Search

```bash
# Search by meaning (recommended)
npx starepo search "fast key-value store in Rust"
npx starepo search "react state management without boilerplate"
npx starepo search "machine learning in Python"

# With language filter
npx starepo search "http server" --lang Go

# With topic filter
npx starepo search "ui components" --topic react

# JSON output (for further processing)
npx starepo search "cli tools" --json

# Control number of results (default: 10)
npx starepo search "databases" --limit 20

# Sort results (default: relevance)
npx starepo search "vector database" --sort stars    # most starred first
npx starepo search "react" --sort forks --order asc  # fewest forks first
```

## List & Filter

```bash
# List all starred repos
npx starepo list

# Filter by language
npx starepo list --lang TypeScript

# Filter by topic
npx starepo list --topic "machine-learning"

# Filter by date starred
npx starepo list --since 2026-01-01
npx starepo list --days 30        # starred in last 30 days
npx starepo list --since 2026-01-01 --until 2026-03-01

# Sort results (default: starred desc — most recently starred first)
npx starepo list --sort stars              # most starred first
npx starepo list --sort updated            # recently updated first
npx starepo list --sort starred --order asc  # oldest starred first
```

## Repo Details

```bash
npx starepo info facebook/react
npx starepo info vercel/next.js
```

## Sync & Embed

```bash
# Quick sync (only new stars since last sync)
npx starepo sync --incremental

# Full re-sync
npx starepo sync

# Fix incomplete embeddings (optional, only if semantic search feels off)
npx starepo embed --force
```

## MCP Server (for Claude Desktop / Cursor)

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "starepo": {
      "command": "npx",
      "args": ["starepo", "serve"]
    }
  }
}
```

## Workflow Tips

1. **First search fails or returns nothing** → Run `npx starepo sync`
2. **Stale results** → Run `npx starepo sync --incremental` to fetch new stars
3. **Poor semantic relevance** → Run `npx starepo embed --force` to fix incomplete embeddings
4. **Filter + search** → Combine `--query` with `--lang`/`--topic`/`--days` for precise results
5. **Automation** → Use `--json` flag to pipe results to `jq` or other tools
