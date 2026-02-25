---
name: firecrawl
description: Scrapes and crawls web pages, converting them to clean markdown or structured JSON for LLM consumption. Use when needing to extract content from URLs, crawl entire websites, map site structure, search the web with scraping, or extract structured data from pages. Best for web scraping, site crawling, URL discovery, and converting web content to LLM-ready formats.
---

# Firecrawl Web Scraping

Converts web pages into clean, LLM-ready markdown or structured data. Handles JavaScript rendering, anti-bot measures, and complex sites.

## When to Use

**Use Firecrawl** when you need to:
- Scrape a specific URL and get its content as markdown/HTML
- Crawl an entire website or section recursively
- Map a website to discover all its URLs
- Search the web AND scrape the results in one operation
- Extract structured JSON data from web pages
- Handle JavaScript-rendered or dynamic content
- Get screenshots of web pages

## Protocol

### Step 1: Scrape a Single URL

```bash
scripts/firecrawl.sh scrape "<url>" [format]
```

**Formats:** `markdown` (default), `html`, `links`, `screenshot`

**Example:**
```bash
scripts/firecrawl.sh scrape "https://docs.firecrawl.dev/introduction"
scripts/firecrawl.sh scrape "https://example.com" "html"
```

### Step 2: Search Web + Scrape Results

```bash
scripts/firecrawl.sh search "<query>" [limit]
```

**Example:**
```bash
scripts/firecrawl.sh search "firecrawl web scraping API" 5
```

### Step 3: Map Website URLs

```bash
scripts/firecrawl.sh map "<url>" [limit] [search]
```

**Example:**
```bash
scripts/firecrawl.sh map "https://firecrawl.dev" 50
scripts/firecrawl.sh map "https://docs.firecrawl.dev" 100 "api reference"
```

### Step 4: Extract Structured JSON (Single Page)

```bash
scripts/firecrawl.sh extract "<url>" "<prompt>"
```

Uses Firecrawl's LLM extraction to return structured JSON from a single page.

**Example:**
```bash
scripts/firecrawl.sh extract "https://firecrawl.dev" "Extract company name, mission, and pricing tiers"
```

### Step 5: Crawl Entire Site

```bash
scripts/firecrawl.sh crawl "<url>" [limit] [depth]
```

**Example:**
```bash
scripts/firecrawl.sh crawl "https://docs.firecrawl.dev" 20 2
```

## Critical Rules

1. **Scrape for single pages** - Use `scrape` when you have specific URLs
2. **Map before crawl** - Use `map` to discover URLs, then scrape specific ones
3. **Search for discovery** - Use `search` to find relevant pages when you don't know URLs
4. **Extract for structure** - Use `extract` when you need JSON, not markdown
5. **Respect rate limits** - Script auto-retries on 429 with key rotation
6. **Current year is 2026** - Use this when recency matters; omit for timeless topics or use older years when historically relevant

## Resources

See `reference/troubleshooting.md` for error handling, configuration, and common issues.
