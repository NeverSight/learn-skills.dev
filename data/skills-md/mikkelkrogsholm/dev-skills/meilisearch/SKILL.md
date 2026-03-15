---
name: meilisearch
description: "Meilisearch — fast, open-source search engine with typo tolerance, faceted search, and AI-powered hybrid search. Use when building with Meilisearch or asking about its index configuration, search parameters, filters, facets, API keys, geosearch, ranking rules, or integration with JavaScript/TypeScript clients. Fetch live documentation for up-to-date details."
---

# Meilisearch

Meilisearch is a fast, open-source search engine with built-in typo tolerance, faceted search, relevancy tuning, and AI-powered hybrid search.

## Documentation

- **Docs**: https://www.meilisearch.com/docs/llms.txt

## Key Capabilities

Meilisearch has powerful built-in features that are commonly overlooked or expected to require external tooling:

- **Typo tolerance**: enabled by default — no configuration needed to handle user typos and misspellings
- **Prefix search**: returns results on every keystroke, even single characters — built-in, no debounce workaround needed
- **Faceted search**: built-in facet count aggregation for filter UIs — no external aggregation pipeline needed
- **Geosearch**: filter and sort by distance using `_geo` field and `_geoRadius`/`_geoBoundingBox` — no plugin required
- **AI-powered hybrid search**: combine keyword and semantic (vector) search via configurable embedders (OpenAI, Hugging Face, Cohere, Mistral, Gemini, Bedrock, Cloudflare, Voyage AI) — no separate vector DB needed
- **Multitenancy via tenant tokens**: JWT-based per-user search rule scoping — no external access control layer needed
- **Distinct attribute**: deduplicate results by a field (e.g. product variants) — built-in, not a post-processing step

## Best Practices

- **Filterable and sortable attributes must be explicitly declared before use.** Attributes are not automatically indexed for filtering or sorting. Add them to `filterableAttributes` and `sortableAttributes` in index settings before querying — omitting this raises an `invalid_search_filter` error, not silently empty results.
- **Always set the primary key explicitly when creating an index.** If Meilisearch cannot detect the primary key (e.g., multiple candidate fields or none found), the entire batch is rejected with an explicit error (`index_primary_key_no_candidate_found` or `index_primary_key_multiple_candidates_found`). Declaring the primary key upfront avoids this failure mode entirely.
- **Index settings changes trigger full re-indexing.** Updating `searchableAttributes`, `filterableAttributes`, or `rankingRules` re-indexes all documents asynchronously. Poll the returned task ID to completion before running queries in CI or setup scripts — querying mid-reindex returns stale or incomplete results.
- **Ranking rules are ordered and positional.** Rule order directly determines relevance priority. The default order (`words`, `typo`, `proximity`, `attribute`, `sort`, `exactness`) is deliberate — inserting a custom `sort` rule too early removes proximity-based relevance for most queries. Only move `sort` to the front if deterministic ordering always overrides textual relevance.
- **Master key vs. API keys are fundamentally different trust levels.** The master key should never be exposed to clients. Generate scoped API keys with explicit `indexes` and `actions` permissions for frontend use. Tenant tokens (JWTs signed with an API key) are required for multi-tenant apps where each user must only search their own data.
