---
name: exa-company-research
description: Company research using Exa search. Finds company info, competitors, news, tweets, financials, LinkedIn profiles, builds company lists. Use when researching companies, doing competitor analysis, market research, or building company lists.
user-invocable: true
---

# Company Research (Exa)

## Tool

Call the native MCP tool `exa-search__web_search_advanced_exa` directly. Parameters go in a JSON object — examples below use shorthand key=value.

## Critical Rules

- **Never run searches in main context.** Always spawn subagents via `llm_task` or run in sequence with isolated results.
- **Query variation:** generate 2-3 phrasings, run in parallel, merge + deduplicate.
- **Dynamic numResults:** "a few" → 10-20, "comprehensive" → 50-100, explicit number → match it.

## Categories

| Category | Use for |
|----------|---------|
| `company` | Homepages, metadata (headcount, location, funding) |
| `news` | Press coverage, announcements |
| `tweet` | Social presence |
| `people` | LinkedIn profiles |
| _(none)_ | General web, deep dives |

**Start with `category=company`** for discovery, then use other categories for deeper research.

### Category Restrictions

With `category=company`: do NOT use `includeDomains`, `excludeDomains`, or date filters — causes errors.
`includeText`/`excludeText`: only single-value strings.

## Call Examples

Tool: `exa-search__web_search_advanced_exa`

```
# Company discovery
{ query: "AI infrastructure startups San Francisco", category: "company", numResults: 20, type: "auto" }

# Deep dive on specific company
{ query: "Anthropic funding rounds valuation 2024", type: "neural", livecrawl: "fallback", numResults: 10,
  includeDomains: ["techcrunch.com","crunchbase.com","bloomberg.com"] }

# News coverage
{ query: "Anthropic AI safety 2024", category: "news", numResults: 15, startPublishedDate: "2024-01-01" }

# Tweets/social
{ query: "Anthropic Claude new features", category: "tweet", numResults: 20 }
```

## Output Format

Return:
1. Results — structured list, one company per row (name, URL, description, key facts)
2. Sources — URLs with 1-line relevance
3. Notes — any uncertainty or conflicts

## Browser Fallback

If Exa returns insufficient results or content is auth-gated → use `browser` tool as fallback.
