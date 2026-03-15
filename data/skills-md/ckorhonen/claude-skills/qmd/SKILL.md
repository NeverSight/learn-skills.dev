---
name: qmd
description: Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections.
---

# qmd - Quick Markdown Search

Local search engine for Markdown notes, docs, and knowledge bases. Index once, search fast.

## When to use (trigger phrases)

- "search my notes / docs / knowledge base"
- "find related notes"
- "retrieve a markdown document from my collection"
- "search local markdown files"

## Default behavior (important)

- Prefer `qmd search` (BM25). It's typically instant and should be the default.
- Use `qmd vsearch` only when keyword search fails and you need semantic similarity (can be very slow on a cold start).
- Avoid `qmd query` unless the user explicitly wants the highest quality hybrid results and can tolerate long runtimes/timeouts.

## Search modes

| Mode | Command | Speed | Use case |
|------|---------|-------|----------|
| BM25 (default) | `qmd search` | Instant | Keyword matching |
| Vector | `qmd vsearch` | ~1 min cold | Semantic similarity |
| Hybrid | `qmd query` | Slowest | LLM reranking (skip unless requested) |

## Common commands

```bash
qmd search "query"              # default - fast keyword search
qmd search "query" -c notes     # search specific collection
qmd search "query" -n 10        # more results
qmd search "query" --json       # JSON output
qmd search "query" --all --files --min-score 0.3
```

## Useful options

- `-n <num>`: number of results
- `-c, --collection <name>`: restrict to a collection
- `--all --min-score <num>`: return all matches above a threshold
- `--json` / `--files`: agent-friendly output formats
- `--full`: return full document content

## Retrieve documents

```bash
qmd get "path/to/file.md"       # Full document
qmd get "#docid"                # By ID from search results
qmd multi-get "journals/2025-05*.md"
qmd multi-get "doc1.md, doc2.md, #abc123" --json
```

## Maintenance

```bash
qmd status                      # Index health
qmd update                      # Re-index changed files
qmd embed                       # Update embeddings
```

## Setup (if not installed)

```bash
# Install
bun install -g https://github.com/tobi/qmd

# Create collection
qmd collection add /path/to/notes --name notes --mask "**/*.md"
qmd context add qmd://notes "Description of this collection"  # optional
qmd embed  # one-time to enable vector + hybrid search
```

## Performance notes

- `qmd search` is typically instant
- `qmd vsearch` can be ~1 minute on cold start (loads local LLM for query expansion)
- `qmd query` adds LLM reranking on top of `vsearch`, even slower
