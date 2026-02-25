---
name: tavily-search-and-fetch
description: "Web (re)earch using Tavily APIs. Search the web, extract content from URLs, discover site maps, or get AI-synthesized research reports with citations. Use for factual search, current events, financial data, full content extraction, site map URLs, or comprehensive research reports. Topics: general, news, finance."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["curl", "jq"], "env": ["TAVILY_API_KEY"] },
        "primaryEnv": "TAVILY_API_KEY",
        "install":
          [
            {
              "id": "jq-brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# Tavily Researcher

Web research via Tavily's LLM-optimized APIs: search, extract, sitemap, and research.

## Setup

Requires `TAVILY_API_KEY` environment variable. Get a free key (1000 credits/month) at https://app.tavily.com

## Choosing the Right Tool

| Need | Script |
|------|--------|
| Web search results | `tavily_search.sh` |
| Content from specific URLs | `tavily_extract.sh` |
| Discover URLs on a site (fast) | `tavily_sitemap.sh` |
| AI-synthesized report with citations | `tavily_research.sh` |

## Quick Start

### Search
```bash
scripts/tavily_search.sh "What is retrieval augmented generation?" --include-answer
```

### News Search
```bash
scripts/tavily_search.sh "AI regulation updates" --topic news --time-range week
```

### Extract Content from URLs
```bash
scripts/tavily_extract.sh https://example.com/article1 https://example.com/article2
```

### Discover URLs on a Site
```bash
scripts/tavily_sitemap.sh https://docs.example.com --max-depth 2 --limit 100
```

### AI Research Report
```bash
scripts/tavily_research.sh "Compare LangGraph vs CrewAI for multi-agent systems" --model pro
```

## Scripts

### `tavily_search.sh`
Standard web search. Returns titles, URLs, snippets, and optional AI answer.

**Key options:**
- `--depth ultra-fast|fast|basic|advanced` — Trade speed for relevance
- `--topic general|news|finance` — Optimize for content type
- `--include-answer` — Get AI-generated summary
- `--include-raw-content` — Get full page content
- `--time-range day|week|month|year` — Filter by recency
- `--chunks-per-source N` — Chunks per source (1-5, advanced/fast)
- `--include-domains` / `--exclude-domains` — Filter sources

### `tavily_extract.sh`
Extract full content from specific URLs (up to 20 at once).

**Key options:**
- `--depth basic|advanced` — Use advanced for JS-heavy pages
- `--query TEXT` — Rerank chunks by relevance
- `--chunks-per-source N` — Return only relevant chunks (1-5, requires --query)
- `--format markdown|text` — Output format

### `tavily_sitemap.sh`
Discover URLs on a website without extracting content. Faster than crawl — use to understand site structure first.

**Key options:**
- `--max-depth N` — Crawl depth 1-5 (start with 1)
- `--limit N` — Total URLs cap (default: 50)
- `--instructions TEXT` — Focus on specific types of pages

### `tavily_research.sh`
AI-synthesized research with citations. Takes 30-120 seconds.

**Key options:**
- `--model mini|pro|auto` — mini for focused queries, pro for comprehensive analysis
- `--citation-format numbered|mla|apa|chicago`
- `--output-schema JSON` — Get structured JSON output
- `--output-file PATH` — Save results to file

## Cost Optimization

| Task | Recommended Approach | Credits |
|------|---------------------|---------|
| Quick fact check | `tavily_search.sh --include-answer` | 1 |
| Deeper search | `tavily_search.sh --depth advanced` | 2 |
| Full article content | `tavily_extract.sh <urls>` | 1 per 5 URLs |
| Discover site URLs | `tavily_sitemap.sh` | 1 |
| AI research report | `tavily_research.sh` | varies |

## Domain-Specific Search
```bash
# Only search specific sites
scripts/tavily_search.sh "async python" --include-domains docs.python.org,realpython.com

# Exclude unreliable sources
scripts/tavily_search.sh "health advice" --exclude-domains reddit.com,quora.com
```

## API Reference

See `references/api_reference.md` for full parameter documentation.
