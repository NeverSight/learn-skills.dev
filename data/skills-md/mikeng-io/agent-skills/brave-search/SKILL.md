---
name: brave-search
description: Optional web search enrichment via Brave Search MCP. Provides web, news, and local search with an independent index (no Google dependency). Invokable standalone or called by deep-research, deep-explorer, or any skill needing web search. Non-blocking — falls back to other search tools if unavailable.
location: managed
context: fork
allowed-tools:
  - ToolSearch
  - mcp__brave-search__brave_web_search
  - mcp__brave-search__brave_news_search
  - mcp__brave-search__brave_local_search
  - mcp__brave-search__brave_summarizer
  - mcp__brave-search__brave_video_search
  - mcp__brave-search__brave_image_search
---

# Brave Search MCP — Optional Web Search Enrichment

This skill wraps the Brave Search MCP server to provide structured web, news, and local search capabilities. It is designed to be invoked by other skills or used standalone for general research.

**Setup:** Requires the Brave Search MCP server configured with a Brave Search API key.

```bash
# Add to MCP config (one-time setup)
claude mcp add -s user brave-search npx @brave/search-mcp
# Then set: BRAVE_API_KEY=your_key_here
# Get a free API key at: https://brave.com/search/api/
```

---

## Pre-Flight: Check Availability

```yaml
ToolSearch: "brave-search"
  → Returns: mcp__brave-search__brave_web_search (and news, local, etc.)
  → If found: proceed to Step 1
  → If not found: return availability: "unavailable", fallback to other search tools
```

**Non-blocking fallback chain:** Brave Search → web-search-prime → WebFetch → Bash curl/wget

---

## Step 1: Select Search Mode

Choose the appropriate Brave Search tool based on query type:

```yaml
search_mode_selection:
  brave_web_search:
    trigger: General research, technical questions, documentation lookup
    tool: mcp__brave-search__brave_web_search
    returns: Web results with titles, URLs, descriptions

  brave_news_search:
    trigger: Recent events, breaking news, time-sensitive topics, announcements
    tool: mcp__brave-search__brave_news_search
    returns: News articles with publication dates and source attribution

  brave_local_search:
    trigger: Location-specific queries, "near me", city/region-scoped research
    tool: mcp__brave-search__brave_local_search
    returns: Local business/event results with location data

  brave_summarizer:
    trigger: "Summarize what the web says about X" — AI-distilled summary of top results
    tool: mcp__brave-search__brave_summarizer
    returns: Synthesized summary (does not return individual URLs — use when summary is enough)

  brave_video_search:
    trigger: Tutorial videos, conference talks, demo recordings
    tool: mcp__brave-search__brave_video_search

  brave_image_search:
    trigger: Visual content, diagrams, charts, screenshots
    tool: mcp__brave-search__brave_image_search
```

---

## Step 2: Execute Queries

Run 1-5 queries depending on research scope. Parallel execution is fine for independent queries.

**Query best practices:**
- Be specific: "Kafka consumer group rebalancing Go" not just "Kafka"
- Use quotes for exact phrases: `"distributed tracing" "OpenTelemetry"`
- Add year for recent content: `OpenTelemetry Go 2025`
- For news: use `brave_news_search` with a shorter, more topic-focused query

**Example usage:**
```
# Web search
mcp__brave-search__brave_web_search(query="OpenTelemetry Go SDK distributed tracing 2025", count=10)

# News search
mcp__brave-search__brave_news_search(query="Kubernetes security CVE 2025", count=5)

# Local search
mcp__brave-search__brave_local_search(query="blockchain conferences San Francisco 2025")
```

---

## Step 3: Process Results

For each result, extract and structure:

```json
{
  "source": "brave-search",
  "search_mode": "web | news | local | summarizer | video | image",
  "query": "the query executed",
  "results": [
    {
      "title": "Result title",
      "url": "https://actual-content-url",
      "description": "Excerpt or description",
      "published_date": "2025-01-15",    // news results
      "credibility": "HIGH | MEDIUM | LOW",
      "key_points": ["Extracted insight 1", "Extracted insight 2"]
    }
  ],
  "availability": "available",
  "result_count": 10
}
```

**Credibility assessment:**
- HIGH: Official docs, academic papers, recognized industry authorities
- MEDIUM: Established company blogs, tech publications, conference proceedings
- LOW: Personal blogs, forums, social media, unverified sources

---

## Calling Context Integration

### When invoked by `deep-research`

Return structured results for integration into the domain researcher's findings. Multi-search strategy: run Brave Web and Brave News in parallel for each domain query to get broader coverage.

### When invoked by `context` skill (optional enrichment)

Use `brave_web_search` with 1-2 queries to detect current technology patterns, framework versions, or industry terminology signals that supplement domain selection.

### When invoked standalone

Execute queries, return structured results with source attribution. Suitable for quick research tasks that don't require the full deep-research pipeline.

---

## Output

```json
{
  "skill": "brave-search",
  "availability": "available | unavailable",
  "queries_executed": ["list of queries"],
  "search_modes_used": ["web", "news"],
  "results": [...],
  "result_count": 15,
  "fallback_used": false
}
```

If unavailable:
```json
{
  "skill": "brave-search",
  "availability": "unavailable",
  "reason": "MCP server not configured",
  "setup_hint": "claude mcp add -s user brave-search npx @brave/search-mcp"
}
```

---

## Why Brave Search?

- **Independent index**: Not Google — provides genuine search diversity
- **Privacy-first**: No tracking or personalization affecting results
- **API quality**: Structured JSON responses with rich metadata
- **News freshness**: Separate news endpoint with publication dates
- **No rate limiting drama**: Paid API with predictable quotas
- **Local search**: Useful for geo-specific research without extra configuration
