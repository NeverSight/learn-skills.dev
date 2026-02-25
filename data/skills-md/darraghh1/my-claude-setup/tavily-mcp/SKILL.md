---
name: tavily-mcp
description: "Web search, content extraction, site crawling, and multi-source research via the Tavily MCP server."
metadata:
  version: 1.0.0
  mcp-server: tavily
---

# Tavily Web Search & Research

You are an expert at using the Tavily MCP server for web search, content extraction, site crawling, and multi-source research. Tavily provides high-quality, AI-optimized search results and deep content extraction.

## Critical: These Are Direct Tool Calls

MCP tools are **direct tool calls** — exactly like `Read`, `Grep`, or `Bash`. They are NOT CLI commands.

**CORRECT** — call the tool directly:
```
Tool: mcp__tavily__tavily_search
Parameters: { "query": "Next.js 15 server actions best practices 2026" }
```

**WRONG** — do NOT shell out:
```
Bash: claude mcp call tavily tavily_search ...  # This does not work
```

All Tavily MCP tools use the `mcp__tavily__` prefix.

## Critical: Output Size Awareness

| Tool | Output Size | Cost | Notes |
|------|------------|------|-------|
| `tavily_search` (basic) | Small-Medium | Low | 5-10 results with snippets |
| `tavily_search` (advanced) | Medium | Medium | More results, deeper analysis |
| `tavily_extract` | Medium-Large | Medium | Full page content — scales with page size |
| `tavily_crawl` | Large-Very Large | High | Multiple pages — scales with depth/breadth settings |
| `tavily_map` | Medium | Low | URL list only (no content) |
| `tavily_research` | Very Large | Very High | Multi-source synthesis — use sparingly |

**Start with `tavily_search`** for most questions. Only escalate to `tavily_research` for comprehensive multi-source analysis.

## Workflow 1: Quick Search

**Trigger:** User asks a factual question, needs current information, or wants a quick answer.

### Steps

1. **Search with targeted query:**
   ```
   tavily_search({
     query: "Supabase RLS best practices 2026",
     search_depth: "basic"
   })
   ```

2. **If results are insufficient, try advanced search:**
   ```
   tavily_search({
     query: "Supabase RLS best practices 2026",
     search_depth: "advanced"
   })
   ```

3. **Optionally filter by domain:**
   ```
   tavily_search({
     query: "Next.js middleware",
     include_domains: ["nextjs.org", "vercel.com"]
   })
   ```

## Workflow 2: Extract Content from URL

**Trigger:** User provides a URL and wants its content, or search results point to a page needing deeper extraction.

### Steps

1. **Extract page content:**
   ```
   tavily_extract({
     urls: ["https://example.com/article"],
     extract_depth: "basic"
   })
   ```

2. **For protected sites or complex pages (tables, dynamic content):**
   ```
   tavily_extract({
     urls: ["https://example.com/pricing"],
     extract_depth: "advanced"
   })
   ```

**Note:** `tavily_extract` can handle multiple URLs in parallel — pass them all in the `urls` array.

## Workflow 3: Site Discovery & Crawling

**Trigger:** User says "explore this site", "what pages does this site have?", "crawl the docs", "map the site structure"

### Steps

1. **Map the site first** (URL structure only, no content):
   ```
   tavily_map({
     url: "https://docs.example.com",
     max_depth: 2,
     max_urls: 50
   })
   ```

2. **Then crawl specific sections** (full content):
   ```
   tavily_crawl({
     url: "https://docs.example.com/guides",
     max_depth: 1,
     max_breadth: 10
   })
   ```

### Key Patterns

- Always `tavily_map` before `tavily_crawl` — understand structure first, then extract content
- `tavily_crawl` defaults: `max_depth: 1`, `max_breadth: 20` — increase carefully
- Crawling entire sites is expensive — target specific sections

## Workflow 4: Deep Research

**Trigger:** User says "research this topic thoroughly", "give me a comprehensive analysis", "compare options for X"

### Steps

1. **Start with a search to gauge complexity:**
   ```
   tavily_search({ query: "...", search_depth: "advanced" })
   ```

2. **If a single search isn't enough, use research:**
   ```
   tavily_research({
     query: "Comprehensive comparison of Supabase vs Firebase for multi-tenant SaaS in 2026",
     max_results: 10
   })
   ```

**Use `tavily_research` sparingly** — it makes multiple internal requests and produces very large output. Most questions are answered by `tavily_search` alone.

## Decision Tree

| User Needs | Best Tool | Why |
|------------|-----------|-----|
| Quick factual answer | `tavily_search` (basic) | Fast, low cost |
| Thorough search results | `tavily_search` (advanced) | More results, deeper snippets |
| Content from a specific URL | `tavily_extract` | Direct page content |
| Site structure overview | `tavily_map` | URL list only, no content |
| Multiple pages from a site | `tavily_crawl` | Follows links, extracts content |
| Comprehensive multi-source analysis | `tavily_research` | Multi-source synthesis (expensive) |

## Search Tips

- **Include the year** for current info: "React server components 2026" not just "React server components"
- **Use `include_domains`** to target authoritative sources: `["nextjs.org", "supabase.com"]`
- **Use `exclude_domains`** to filter noise: `["medium.com", "w3schools.com"]`
- **Be specific:** "Supabase RLS policies for multi-tenant SaaS with account_id" beats "Supabase security"

## Troubleshooting

### Search Returns Outdated Results

1. Add the current year to your query: "topic 2026"
2. Use `search_depth: "advanced"` for better results
3. Use `include_domains` to target official docs or recent sources

### Extract Returns Empty or Partial Content

1. Try `extract_depth: "advanced"` for JavaScript-rendered pages
2. Some sites block extraction — fall back to `WebFetch` or `browser_navigate` (Playwright MCP)
3. Check if the URL requires authentication — Tavily cannot access authenticated content

### Crawl Produces Too Much Output

1. Reduce `max_depth` (default 1 is usually sufficient)
2. Reduce `max_breadth` (default 20 — try 5-10 for targeted crawls)
3. Use `tavily_map` first to identify the specific URLs you need, then `tavily_extract` those URLs directly

### Research Takes Too Long

`tavily_research` makes multiple internal API calls. If it's too slow:
1. Use `tavily_search` with `search_depth: "advanced"` instead
2. Run multiple targeted `tavily_search` calls in parallel
3. Only use `tavily_research` when comprehensive synthesis is truly needed
