---
name: llm-wiki-skill
description: Build and maintain a personal knowledge base using Karpathy's llm-wiki methodology across Claude Code, Codex, and OpenClaw agents.
triggers:
  - set up my personal knowledge base
  - install llm-wiki skill
  - add this article to my wiki
  - digest this content into my knowledge base
  - build a wiki from my notes
  - process this URL into my knowledge library
  - create a wiki page for this topic
  - check my knowledge base health
---

# llm-wiki-skill — Multi-Platform Knowledge Base Builder

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Build a persistent, interlinked personal knowledge base from URLs, PDFs, markdown files, and raw text. Based on Karpathy's llm-wiki methodology: knowledge is **compiled once and maintained**, not re-derived from raw docs on every query.

## What It Does

- Ingests articles, tweets, PDFs, YouTube transcripts, WeChat posts, and plain text
- Routes each source type to the best extraction tool automatically
- Generates structured wiki pages with `[[bidirectional links]]`
- Produces entity pages, topic pages, source summaries, and comparisons
- Outputs Obsidian-compatible local markdown files
- Detects orphaned pages, broken links, and contradictions via health checks

## Installation

### Recommended: Let Your Agent Install It

Give your agent the repo URL and ask it to install for your platform:

```
https://github.com/sdyckjq-lab/llm-wiki-skill
```

### Manual Installation

Clone the repo anywhere, then run the installer for your platform:

```bash
# Claude Code
bash install.sh --platform claude

# Codex
bash install.sh --platform codex

# OpenClaw
bash install.sh --platform openclaw

# Auto-detect (only if one platform directory exists)
bash install.sh --platform auto

# Custom target directory (OpenClaw non-standard path)
bash install.sh --platform openclaw --target-dir /path/to/your/skills
```

### Default Install Locations

| Platform | Path |
|----------|------|
| Claude Code | `~/.claude/skills/llm-wiki` |
| Codex | `~/.codex/skills/llm-wiki` |
| OpenClaw | `~/.openclaw/skills/llm-wiki` |

### Legacy Claude Setup (existing users)

```bash
bash setup.sh
# This is now a compatibility shim for the unified installer
```

### Prerequisites

```bash
# Check Chrome debug mode is running (needed for web extraction)
google-chrome --remote-debugging-port=9222 &

# Check uv is installed (needed for WeChat + YouTube extraction)
uv --version

# Install bun OR npm (one is enough for web extraction deps)
curl -fsSL https://bun.sh/install | bash
# OR: npm is already available in most environments
```

## Platform Entry Points

After installation, read the platform-specific instructions:

- **Claude Code**: `platforms/claude/CLAUDE.md`
- **Codex**: `platforms/codex/AGENTS.md`
- **OpenClaw**: `platforms/openclaw/README.md`

## Knowledge Base Structure

```
your-wiki/
├── raw/                    # Immutable source material
│   ├── articles/           # Web articles
│   ├── tweets/             # X/Twitter
│   ├── wechat/             # WeChat posts
│   ├── xiaohongshu/        # Xiaohongshu (manual paste only)
│   ├── zhihu/              # Zhihu
│   ├── pdfs/               # PDFs
│   ├── notes/              # Notes
│   └── assets/             # Images, attachments
├── wiki/                   # AI-generated knowledge base
│   ├── entities/           # People, concepts, tools
│   ├── topics/             # Topic pages
│   ├── sources/            # Source summaries
│   ├── comparisons/        # Side-by-side analysis
│   └── synthesis/          # Cross-source synthesis
├── index.md                # Master index
├── log.md                  # Operation log
└── .wiki-schema.md         # Config
```

## Core Workflows

### Initialize a New Knowledge Base

```bash
# Ask your agent:
"Create a new knowledge base at ~/my-wiki"

# The agent will scaffold the directory structure,
# generate index.md, log.md, and .wiki-schema.md
```

### Ingest a Web Article

```bash
# Agent command pattern:
"Add this article to my wiki: https://example.com/article"

# Under the hood, the agent routes to baoyu-url-to-markdown:
npx baoyu-url-to-markdown https://example.com/article > raw/articles/article-slug.md
```

### Ingest a YouTube Video

```bash
# Agent command pattern:
"Digest this YouTube video into my knowledge base: https://youtube.com/watch?v=abc123"

# Uses youtube-transcript via uv:
uvx youtube-transcript https://youtube.com/watch?v=abc123 > raw/articles/video-slug.md
```

### Ingest a WeChat Article

```bash
# Agent command pattern:
"Add this WeChat article to my wiki: https://mp.weixin.qq.com/s/..."

# Uses wechat-article-to-markdown via uv:
uvx wechat-article-to-markdown https://mp.weixin.qq.com/s/... > raw/wechat/article-slug.md
```

### Ingest a PDF

```bash
# Agent command pattern:
"Process this PDF into my wiki: /path/to/paper.pdf"
# OR drag a file into the chat

# No external tool needed — goes directly into main pipeline:
cp /path/to/paper.pdf raw/pdfs/paper.pdf
```

### Ingest Raw Text or Notes

```bash
# Just paste text to your agent:
"Add these notes to my wiki: [paste content]"

# Agent writes directly to:
echo "your content" > raw/notes/note-slug.md
```

### Batch Process a Folder

```bash
# Agent command pattern:
"Process all files in ~/Downloads/research into my wiki"

# Agent iterates over files and routes each by type
for f in ~/Downloads/research/*; do
  # agent determines type and processes accordingly
done
```

### Health Check

```bash
# Agent command pattern:
"Run a health check on my knowledge base"

# Agent checks for:
# - Orphaned pages (no incoming links)
# - Broken [[wiki links]]
# - Contradictory information across pages
# - Missing source summaries
```

## Source Routing Reference

| Source Type | Tool Used | Requires |
|-------------|-----------|----------|
| Web articles | `baoyu-url-to-markdown` | Chrome debug mode |
| X/Twitter | `baoyu-url-to-markdown` | Chrome debug mode + X login |
| Zhihu | `baoyu-url-to-markdown` | Chrome debug mode |
| WeChat | `wechat-article-to-markdown` | `uv` |
| YouTube | `youtube-transcript` | `uv` |
| Xiaohongshu | Manual paste | Nothing |
| PDF / Markdown / Text | Direct pipeline | Nothing |

Source registry lives at: `scripts/source-registry.tsv`
Routing logic lives at: `scripts/source-registry.sh`

## Wiki Page Conventions

### Entity Page (wiki/entities/andrej-karpathy.md)

```markdown
# Andrej Karpathy

## Overview
Former OpenAI/Tesla researcher, creator of llm-wiki methodology.

## Key Ideas
- [[llm-wiki]] — compile knowledge once, maintain over time
- [[nanoGPT]] — minimal GPT implementation for education

## Sources
- [[sources/llm-wiki-gist-2024]]
- [[sources/karpathy-interview-2023]]

## Related
- [[topics/language-models]]
- [[entities/openai]]
```

### Topic Page (wiki/topics/retrieval-augmented-generation.md)

```markdown
# Retrieval-Augmented Generation

## Summary
...

## Key Entities
- [[entities/langchain]]
- [[entities/llamaindex]]

## Comparisons
- [[comparisons/rag-vs-finetuning]]

## Sources
- [[sources/rag-paper-2020]]
```

### Source Summary (wiki/sources/article-slug.md)

```markdown
# Source: Article Title

- **URL**: https://example.com/article
- **Date ingested**: 2026-04-10
- **Type**: web article

## Key Points
1. ...
2. ...

## Entities Mentioned
- [[entities/...]]

## Raw**: [[raw/articles/article-slug]]
```

## Troubleshooting

### Chrome / Web Extraction Fails

```bash
# Start Chrome with remote debugging enabled
google-chrome --remote-debugging-port=9222 --no-first-run &

# Verify it's running
curl http://localhost:9222/json/version

# For X/Twitter: make sure you're logged in on that Chrome session
# Then retry the extraction
```

### WeChat or YouTube Extraction Fails

```bash
# Install uv if missing
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Re-run installer to pick up uv
bash install.sh --platform claude  # or your platform

# Verify uv tools work
uvx youtube-transcript --help
uvx wechat-article-to-markdown --help
```

### bun/npm Dependency Install Fails

```bash
# The installer auto-selects bun or npm — check which is available
which bun && echo "bun found"
which npm && echo "npm found"

# Manually install web extraction deps with npm
npm install -g baoyu-url-to-markdown
```

### Codex Legacy Path Compatibility

```bash
# Old path still supported automatically:
~/.Codex/skills  # capital C — installer handles both
~/.codex/skills  # lowercase — new default
```

### Agent Can't Find Installed Skill

```bash
# Verify install location for your platform
ls ~/.claude/skills/llm-wiki/   # Claude Code
ls ~/.codex/skills/llm-wiki/    # Codex
ls ~/.openclaw/skills/llm-wiki/ # OpenClaw

# Re-run installer if directory is missing
bash install.sh --platform <your-platform>
```

### Source Registry Lookup

```bash
# Check registered sources and routing
cat scripts/source-registry.tsv

# Test routing for a URL
bash scripts/source-registry.sh route "https://mp.weixin.qq.com/s/example"
```

## Key Design Principles

1. **Compile once, maintain** — wiki pages are living documents, not ephemeral answers
2. **Bidirectional links** — every entity and topic links to related nodes with `[[name]]`
3. **Immutable raw** — source files in `raw/` are never modified after ingestion
4. **Graceful degradation** — if a tool fails, agent prompts for manual paste instead of crashing
5. **Platform-agnostic** — same knowledge base works across all supported agents
6. **Obsidian-compatible** — open `your-wiki/` directly in Obsidian at any time

## Quick Reference for Agents

```
Initialize wiki:     "Create a new wiki at <path>"
Add URL:             "Add <url> to my wiki"
Add file:            "Process <file path> into my wiki"
Add text:            "Add these notes to my wiki: <text>"
Batch process:       "Process all files in <folder> into my wiki"
Health check:        "Check my wiki for broken links and orphans"
Find information:    "What does my wiki say about <topic>"
Update a page:       "Update the [[entity]] page with new info from <source>"
```
