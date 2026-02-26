---
name: perigon-api-best-practices
description: Best practices for building with the Perigon News Intelligence API. Use this skill when searching or filtering news articles, tracking evolving stories, generating AI-powered summaries, performing semantic vector search over news or Wikipedia, querying people, companies, journalists, or sources databases, or integrating any Perigon API endpoint into an application.
license: Apache-2.0
metadata:
  author: goperigon
  version: "1.0.0"
  organization: Perigon
  date: February 2026
  abstract: Comprehensive guide for integrating the Perigon News Intelligence API into applications. Covers all endpoints including article search, stories, summaries, vector search (news and Wikipedia), Wikipedia knowledge base, people, companies, journalists, sources, and topics. Includes authentication, query construction, pagination, error handling, and best practices.
---

# Perigon API Best Practices

Comprehensive guide for building with the Perigon News Intelligence API. Covers all endpoints, query patterns, and integration best practices.

## When to Apply

Reference these guidelines when:
- Searching or filtering news articles by keyword, topic, category, date, source, sentiment, or location
- Tracking evolving news stories and clustered article groups
- Generating AI-powered summaries of news coverage
- Performing semantic/vector search over news articles or Wikipedia content
- Querying the Wikipedia knowledge base for structured page data
- Looking up people, companies, journalists, or media sources
- Browsing available topics and categories
- Building dashboards, alerts, or monitoring tools powered by news data
- Integrating Perigon into any application or AI agent workflow

## API Overview

**Base URL:** `https://api.perigon.io`

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/articles/all` | GET | Search and filter news articles with rich parameters |
| `/v1/stories/all` | GET | Clustered news stories with summaries and metadata |
| `/v1/summarize` | POST | AI-powered summarization over matched articles |
| `/v1/vector/news/all` | POST | Semantic/vector search over news articles |
| `/v1/wikipedia/all` | GET | Search and filter Wikipedia pages |
| `/v1/vector/wikipedia/all` | POST | Semantic/vector search over Wikipedia content |
| `/v1/people/all` | GET | People mentioned in the news (650k+ database) |
| `/v1/companies/all` | GET | Company data with financial metadata |
| `/v1/journalists/all` | GET | Journalist profiles (230k+ database) |
| `/v1/journalists/{id}` | GET | Single journalist by ID |
| `/v1/sources/all` | GET | Media sources database (200k+ sources) |
| `/v1/topics/all` | GET | Topics taxonomy browser |

## Authentication

The API key can be passed in two ways:
1. **Query parameter:** `?apiKey=YOUR_API_KEY`
2. **Header:** `x-api-key: YOUR_API_KEY`

**Best practices:**
- Store the API key in an environment variable (e.g., `PERIGON_API_KEY`). Never hardcode it.
- Prefer the header method (`x-api-key`) to keep keys out of URLs and logs.
- Get your API key at [perigon.io](https://www.perigon.io/).

## Endpoint Selection Guide

Choose the right endpoint based on the task:

```
Need individual articles? → /v1/articles/all
Need grouped stories with summaries? → /v1/stories/all
Need an AI-generated summary of coverage? → /v1/summarize
Need semantic similarity search for news? → /v1/vector/news/all
Need Wikipedia knowledge? → /v1/wikipedia/all
Need semantic search over Wikipedia? → /v1/vector/wikipedia/all
Need person/company/journalist/source info? → /v1/people|companies|journalists|sources/all
Need to browse available topics? → /v1/topics/all
```

## Core Query Patterns

### Text Search (`q` parameter)
The `q` parameter searches across title, description, and content. It supports:
- **Boolean operators:** `AND`, `OR`, `NOT`
- **Exact phrases:** `"climate change"`
- **Wildcards:** `*` (multiple chars), `?` (single char)
- **Combining:** `"electric vehicles" AND (Tesla OR Rivian) NOT recalls`

### Date Filtering
- `from` / `to` — Filter by publication date (ISO 8601 or `yyyy-mm-dd`)
- `addDateFrom` / `addDateTo` — Filter by ingestion date
- `refreshDateFrom` / `refreshDateTo` — Filter by last-updated date

### Pagination
- `page` — Page number (starts at 0)
- `size` — Results per page
- Set `showNumResults=true` to get total counts (slightly slower)

### Sentiment Filtering
Filter by sentiment scores (0.0 to 1.0):
- `positiveSentimentFrom` / `positiveSentimentTo`
- `negativeSentimentFrom` / `negativeSentimentTo`
- `neutralSentimentFrom` / `neutralSentimentTo`

### Array Filters (OR logic)
Many filters accept arrays and combine with OR logic:
`category`, `topic`, `source`, `language`, `country`, `label`, `personName`, `companyDomain`, `companySymbol`, `journalistId`, `medium`, `sourceGroup`

### Exclude Filters (AND-exclude logic)
Prefix any array filter with `exclude` to remove matches:
`excludeCategory`, `excludeTopic`, `excludeSource`, `excludeLanguage`, etc.

## Vector Search (Semantic)

For natural language queries that don't map well to keyword search, use the vector endpoints:

**News:** `POST /v1/vector/news/all` — searches articles from the last 6 months by semantic similarity.

**Wikipedia:** `POST /v1/vector/wikipedia/all` — searches Wikipedia page sections by semantic similarity.

Both accept a `prompt` (natural language query), `page`, `size`, and a `filter` object for structured filtering with nested `AND`/`OR`/`NOT` logic.

## How to Use References

Read individual reference files for detailed endpoint documentation:

```
references/authentication.md        — API key setup and security
references/articles-search.md       — /v1/articles/all deep dive
references/stories-clustering.md    — /v1/stories/all deep dive
references/smart-summaries.md       — /v1/summarize deep dive
references/vector-search.md         — /v1/vector/news/all and /v1/vector/wikipedia/all
references/wikipedia-knowledge.md   — /v1/wikipedia/all deep dive
references/people-companies.md      — /v1/people/all and /v1/companies/all
references/journalists-sources.md   — /v1/journalists/all and /v1/sources/all
references/topics-categories.md     — /v1/topics/all and category taxonomy
references/pagination-filtering.md  — Common query patterns and pagination
references/error-handling.md        — HTTP status codes and retry logic
references/rate-limits.md           — Rate limit management
```

Each reference file contains:
- Endpoint URL and HTTP method
- All query/body parameters with types and descriptions
- Example requests (curl) and response JSON
- Common patterns and best practices
- When to use this endpoint vs. alternatives

## Best Practices Summary

1. **Start narrow, then broaden** — Use specific filters first, then relax constraints if results are too few.
2. **Prefer `from`/`to` over `addDateFrom`/`addDateTo`** for publication-date filtering unless you specifically need ingestion-date filtering.
3. **Use `showReprints=false`** to deduplicate wire-service content (AP, Reuters) that appears on multiple sites.
4. **Use `sourceGroup`** (e.g., `top100`, `top25tech`) for quality-filtered results.
5. **Combine endpoints** — Use `/v1/stories/all` to find story clusters, then `/v1/articles/all` with `clusterId` for all articles in a story.
6. **Use vector search for intent-based queries** — When the user's query is conversational or conceptual rather than keyword-based.
7. **Use Wikipedia endpoints for factual background** — Combine with news search to enrich coverage with encyclopedic context.
8. **Handle pagination properly** — Always check `numResults` and iterate pages when building comprehensive datasets.
9. **Cache strategically** — News data changes frequently, but entity data (people, companies, sources) changes slowly.
10. **Respect rate limits** — Implement exponential backoff on 429 responses.

## External References

- [Perigon Documentation](https://perigon.io/docs)
- [Perigon API Reference](https://www.perigon.io/reference)
- [Perigon Go SDK](https://github.com/goperigon/perigon-go-sdk)
