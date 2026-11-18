---
name: exa-people-research
description: People research using Exa search. Finds LinkedIn profiles, professional backgrounds, experts, team members, and public bios. Use when searching for people, finding experts, or looking up professional profiles.
user-invocable: true
---

# People Research (Exa)

## Tool

Call the native MCP tool `exa-search__web_search_advanced_exa` directly. Parameters go in a JSON object.

## Critical Rules

- **Never run searches in main context.** Spawn subagents or run sequentially.
- **Query variation:** 2-3 phrasings, run in parallel, deduplicate.
- **Dynamic numResults:** "a few" → 10-20, "comprehensive" → 50-100.

## Categories

| Category | Use for |
|----------|---------|
| `people` | LinkedIn profiles, public bios (primary) |
| `personal site` | Blogs, portfolios, about pages |
| `news` | Press mentions, interviews, speaker bios |
| _(none)_ | General web, broader context |

### Restrictions with `category=people`

Do NOT use: `startPublishedDate`, `endPublishedDate`, `startCrawlDate`, `endCrawlDate`, `excludeDomains`, `includeText`, `excludeText`.
`includeDomains` → LinkedIn only: `["linkedin.com"]`.

## Call Examples

Tool: `exa-search__web_search_advanced_exa`

```
# Find people by role
{ query: "VP Engineering AI infrastructure", category: "people", numResults: 20, type: "auto" }

# Deep dive on specific person
{ query: "Dario Amodei Anthropic CEO background", type: "auto", livecrawl: "fallback", numResults: 15 }

# News mentions
{ query: "Dario Amodei interview 2024", category: "news", numResults: 10, startPublishedDate: "2024-01-01" }

# LinkedIn only
{ query: "Machine learning engineer San Francisco", category: "people",
  includeDomains: ["linkedin.com"], numResults: 25 }
```

## Output Format

Return:
1. Results — name, title, company, location (if available)
2. Sources — profile URLs
3. Notes — profile completeness, verification status

## Browser Fallback

If content is auth-gated (private LinkedIn, etc.) → use `browser` tool with logged-in session.
