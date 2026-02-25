---
name: firecrawl
description: |
  Comprehensive web scraping, crawling, and data extraction toolkit powered by Firecrawl API.
  Provides scripts for single-page scraping (scrape.py), web search (search.py),
  URL discovery (map.py), multi-page crawling (crawl.py), structured data extraction (extract.py),
  and autonomous data gathering (agent.py).
  Use when you need to: (1) extract content from web pages, (2) search and scrape the web,
  (3) discover URLs on websites, (4) crawl multiple pages, (5) extract structured data with JSON schemas,
  or (6) autonomously gather data from anywhere on the web.
  Requires FIRECRAWL_API_KEY environment variable.
---

# Firecrawl Web Scraping & Data Extraction

## Installation

```bash
pip install firecrawl-py
```

## Environment Setup

Set your Firecrawl API key:
```bash
export FIRECRAWL_API_KEY="your-api-key-here"
```

## Scripts

Note: Set `SKILL_ROOT` to this skill's base directory. Reference bundled scripts as `python3 "$SKILL_ROOT/scripts/<script>.py" ...` (not relative paths from the current working directory).

### scrape.py - Single Page Scraping

The most powerful and reliable scraper. Use when you know exactly which page contains the information.

```bash
# Basic scrape (returns markdown)
python3 "$SKILL_ROOT/scripts/scrape.py" "https://example.com"

# Get HTML format
python3 "$SKILL_ROOT/scripts/scrape.py" "https://example.com" --format html

# Extract only main content (removes headers, footers, etc.)
python3 "$SKILL_ROOT/scripts/scrape.py" "https://example.com" --only-main

# Combine options
python3 "$SKILL_ROOT/scripts/scrape.py" "https://docs.example.com/api" --format markdown --only-main
```

### search.py - Web Search

Search the web when you don't know which website has the information.

```bash
# Basic search
python3 "$SKILL_ROOT/scripts/search.py" "latest AI research papers 2024"

# Limit results
python3 "$SKILL_ROOT/scripts/search.py" "Python web scraping tutorials" --limit 5

# Search with scraping (get full content)
python3 "$SKILL_ROOT/scripts/search.py" "firecrawl documentation" --limit 3
```

### map.py - URL Discovery

Discover all URLs on a website. Use before deciding what to scrape.

```bash
# Map a website
python3 "$SKILL_ROOT/scripts/map.py" "https://docs.example.com"

# Limit number of URLs
python3 "$SKILL_ROOT/scripts/map.py" "https://example.com" --limit 100

# Search within mapped URLs
python3 "$SKILL_ROOT/scripts/map.py" "https://docs.example.com" --search "authentication"
```

### crawl.py - Multi-Page Crawling

Extract content from multiple related pages. Warning: can be slow and return large results.

```bash
# Basic crawl
python3 "$SKILL_ROOT/scripts/crawl.py" "https://docs.example.com"

# Limit pages
python3 "$SKILL_ROOT/scripts/crawl.py" "https://docs.example.com" --limit 20

# Control crawl depth
python3 "$SKILL_ROOT/scripts/crawl.py" "https://docs.example.com" --limit 10 --depth 2
```

### extract.py - Structured Data Extraction

Extract specific structured data using LLM capabilities.

```bash
# Extract with prompt
python3 "$SKILL_ROOT/scripts/extract.py" "https://example.com/pricing" \
  --prompt "Extract all pricing tiers with their features and prices"

# Extract with JSON schema
python3 "$SKILL_ROOT/scripts/extract.py" "https://example.com/team" \
  --prompt "Extract team member information" \
  --schema '{"type":"object","properties":{"members":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"role":{"type":"string"},"bio":{"type":"string"}}}}}}'

# Extract from multiple URLs
python3 "$SKILL_ROOT/scripts/extract.py" "https://example.com/page1" "https://example.com/page2" \
  --prompt "Extract product information"
```

### agent.py - Autonomous Data Gathering

Autonomous agent that searches, navigates, and extracts data from anywhere on the web.

```bash
# Simple research task
python3 "$SKILL_ROOT/scripts/agent.py" --prompt "Find the founders of Firecrawl and their backgrounds"

# Complex data gathering
python3 "$SKILL_ROOT/scripts/agent.py" --prompt "Find the top 5 AI startups founded in 2024 and their funding amounts"

# Focus on specific URLs
python3 "$SKILL_ROOT/scripts/agent.py" \
  --prompt "Compare the features and pricing" \
  --urls "https://example1.com,https://example2.com"

# With output schema
python3 "$SKILL_ROOT/scripts/agent.py" \
  --prompt "Find recent tech layoffs" \
  --schema '{"type":"object","properties":{"layoffs":{"type":"array","items":{"type":"object","properties":{"company":{"type":"string"},"count":{"type":"number"},"date":{"type":"string"}}}}}}'
```

## Output Format

All scripts output JSON to stdout. Errors are written to stderr.

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message"
}
```

## Tips

1. **Performance**: Use `scrape` for single pages - it's 500% faster with caching
2. **Discovery**: Use `map` first to find URLs, then `scrape` specific pages
3. **Large sites**: Prefer `map` + `scrape` over `crawl` for better control
4. **Structured data**: Use `extract` with a JSON schema for consistent output
5. **Research**: Use `agent` when you don't know where to find the data
