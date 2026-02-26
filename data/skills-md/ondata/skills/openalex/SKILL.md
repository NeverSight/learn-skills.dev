---
name: openalex
description: Query OpenAlex API from the command line with curl and jq for publication discovery, filtering, sorting, pagination, and PDF availability checks. Use when searching scholarly works/authors/sources, building or debugging OpenAlex queries, extracting results, or downloading available PDFs using OPENALEX_API_KEY.
compatibility: Requires curl, jq, bash, OPENALEX_API_KEY environment variable, and internet access.
license: CC BY-SA 4.0 (Creative Commons Attribution-ShareAlike 4.0 International)
metadata:
  version: "0.2"
  author: "Andrea Borruso <aborruso@gmail.com>"
  tags: [api, research, scholarly, bibliometrics, open-access, curl, jq, pdf]
---

# OpenAlex

Use this skill to run reliable OpenAlex API workflows from shell.

> **IMPORTANT:** Always write `curl` commands on a **single line**. Multi-line `\` continuation breaks argument parsing in agent environments and will cause errors.

## Definition of Done

A task is complete when:

**Results**
- The API returns at least one result (or a clear "no results found" message)
- Each result shows: title (`display_name`), year, citation count
- Output is readable — not a raw JSON blob

**Process**
- `curl` written on a single line
- `api_key` included in every request
- `select=` used to limit returned fields
- `jq` used to format output

**PDF download** (when requested)
- If PDF is available: file saved locally, path printed
- If PDF is not available: clear message, exit code 2, no crash

## Quick Start

1. Export API key:

```bash
export OPENALEX_API_KEY='...'
```

2. Run list query (works):

```bash
curl -sS --get 'https://api.openalex.org/works' --data-urlencode 'search="data quality" AND "open government data"' --data-urlencode 'filter=type:article,from_publication_date:2023-01-01' --data-urlencode 'sort=relevance_score:desc' --data-urlencode 'per-page=200' --data-urlencode 'select=id,display_name,publication_year,cited_by_count,doi' --data-urlencode "api_key=$OPENALEX_API_KEY" | jq '.results[] | {title:.display_name, year:.publication_year, cited_by:.cited_by_count, doi}'
```

## Workflow

1. Define entity endpoint (`works`, `authors`, `sources`, etc.).
2. Build a `search` block with boolean logic (`AND`, `OR`, `NOT`, quotes, parentheses).
3. Add structured `filter` constraints (type/date/language/OA/citation fields).
4. Restrict output with `select` (root-level fields only).
5. Page results with `page` or `cursor=*`.
6. Extract fields via `jq` and save/transform as needed.

## Iterative Validation Workflow

Use this when building or debugging non-trivial queries.

1. Start with a toy query (`per-page=5` or `per-page=10`) and minimal `select=`.
2. Manually inspect 5-10 records for relevance and field quality (`display_name`, year, DOI).
3. Compare a baseline and a variant before scaling:
   - baseline: `filter=title.search:"..."`
   - variant: `search=...` with same filters
4. Tune one parameter at a time (`search`, `filter`, `sort`, `per-page`, pagination mode).
5. Scale only after validation (`per-page=200`, then `cursor=*` for deep pagination).
6. Log each run: command, key parameters, result count, and quick notes.

Avoid jumping directly from a paper/spec to a full extraction script without this short validation loop.

## Query Blocks

- `title.search=`: searches only in the title — use this by default for focused results. Must be passed inside `filter=`, not as a standalone parameter: `filter=title.search:"your query"`.
- `search=`: full-text search across the entire document — use only when title-only matching is too restrictive.
- `search.semantic=`: semantic/conceptual search (costs $0.001/request; requires API key).
- `filter=`: exact/structured constraints; comma means AND.
- `sort=`: `relevance_score:desc`, `cited_by_count:desc`, `publication_date:desc`, etc.
- `per-page=`: 1..200. **Default is 25 — always set `per-page=200` for bulk queries (8× fewer API calls).**
- `page=`: page number for standard pagination.
- `cursor=*`: deep pagination beyond first 10k records.
- `select=`: reduce payload; nested paths are not allowed in `select`.
- `group_by=`: aggregate results by a field (e.g. `group_by=publication_year`, `group_by=topics.id`).
- `sample=`: random sample of N results (e.g. `sample=20`). Add `seed=42` for reproducibility.

## Filter Syntax

Filters are comma-separated AND conditions. Within a single attribute:

| Logic | Syntax | Example |
|-------|--------|---------|
| AND (comma) | `filter=a:x,b:y` | `filter=type:article,is_oa:true` |
| OR (pipe) | `filter=type:article\|book` | multiple values for same field |
| NOT (exclamation) | `filter=type:!journal-article` | negation |
| Greater than | `filter=cited_by_count:>100` | comparison |
| Less than | `filter=publication_year:<2020` | comparison |
| Range | `filter=publication_year:2020-2023` | inclusive range |

## Batch Lookup

Combine up to **50 IDs in one request** using the pipe operator — avoid sequential calls:

```bash
# Batch DOI lookup (up to 50 per request)
curl -sS --get 'https://api.openalex.org/works' --data-urlencode 'filter=doi:https://doi.org/10.1/abc|https://doi.org/10.2/def' --data-urlencode 'per-page=50' --data-urlencode "api_key=$OPENALEX_API_KEY" | jq '.results[] | {title:.display_name, doi}'
```

## Two-Step Entity Lookup

Names are ambiguous; always resolve to an OpenAlex ID first, then filter.

**Step 1 — find the entity ID:**

```bash
curl -sS --get 'https://api.openalex.org/authors' --data-urlencode 'search=Heather Piwowar' --data-urlencode 'per-page=5' --data-urlencode "api_key=$OPENALEX_API_KEY" | jq '.results[] | {id, display_name}'
```

**Step 2 — use the ID in a filter:**

```bash
curl -sS --get 'https://api.openalex.org/works' --data-urlencode 'filter=authorships.author.id:A5023888391' --data-urlencode 'per-page=200' --data-urlencode 'select=id,display_name,publication_year,cited_by_count' --data-urlencode "api_key=$OPENALEX_API_KEY" | jq '.results[] | {title:.display_name, year:.publication_year}'
```

Applies to: authors (`authorships.author.id`), institutions (`authorships.institutions.id`), sources/journals (`primary_location.source.id`). External IDs are also accepted: ORCID, ROR, ISSN, DOI.

## PDF Retrieval

For a work ID:

1. Fetch work metadata.
2. Resolve PDF URL in this order:
   - `.content_urls.pdf`
   - `.best_oa_location.pdf_url`
   - `.primary_location.pdf_url`
   - first non-null `.locations[].pdf_url`
3. Download with `api_key` query parameter when source is `content.openalex.org`.

## Output Format

When displaying results, always show `display_name` as the title — never use `doi` or `id` in its place.

Minimal jq for a results table:

```bash
| jq -r '.results[] | [.display_name, .publication_year, .cited_by_count, .doi] | @tsv'
```

Or as structured objects:

```bash
| jq '.results[] | {title: .display_name, year: .publication_year, cited_by: .cited_by_count, doi}'
```

## CSV Export

To save results as a CSV file, use `jq` with `@csv` and include a header row:

```bash
curl -sS --get 'https://api.openalex.org/works' ... --data-urlencode "api_key=$OPENALEX_API_KEY" | jq -r '["title","year","cited_by","doi"], (.results[] | [.display_name, .publication_year, .cited_by_count, (.doi // "")]) | @csv' > results.csv
```

Rules:
- Use `// ""` for fields that may be null (e.g. `doi`) — `@csv` fails on null values.
- The header array and data array must have the same number of columns.
- Use `-r` (raw output) so `@csv` produces plain text, not JSON strings.

## Error Handling

Implement exponential backoff on 403 (rate limit) and 500 (server error):

```
attempt 1 → wait 1s → attempt 2 → wait 2s → attempt 3 → wait 4s → attempt 4 → wait 8s
```

HTTP codes:
- `200` — success
- `400` — invalid parameter or filter syntax; fix the query
- `403` — rate limit exceeded; back off and retry
- `404` — entity not found
- `500` — temporary server error; retry with backoff

## Endpoint Costs

With the free $1/day budget:

| Request type | Cost | Daily limit |
|---|---|---|
| Singleton (`/works/W123`) | free | unlimited |
| List / filter | $0.0001 | ~10,000 requests |
| Search (full-text or semantic) | $0.001 | ~1,000 requests |
| PDF download (`content.openalex.org`) | $0.01 | ~100 downloads |

Use `select=` and `per-page=200` to minimize request count.

## Common Pitfalls

- Do not sort by `relevance_score` without a search query.
- Do not use nested fields in `select` (example: use `open_access`, then parse `.open_access.is_oa` with `jq`).
- Do not filter by entity names directly — use the two-step entity lookup to get the ID first.
- Do not use sequential calls for batch ID lookups — batch up to 50 with the pipe operator.
- Do not use `per-page=25` (default) for bulk extraction — always set `per-page=200`.
- Expect some records to have no downloadable PDF.
- `search=` searches full text and can return loosely related results. Use `title.search=` when the topic must appear in the title.
- Always write `curl` commands on a single line — multi-line `\` continuation breaks argument parsing in agent environments.
- `title.search` is NOT a valid standalone parameter — always pass it inside `filter=`: `filter=title.search:"your query"`.
- Always include `api_key=$OPENALEX_API_KEY` in every request.

## Resources

- Query recipes and jq snippets: `references/query-recipes.md`
- Generic query helper: `scripts/openalex_query.sh`
- PDF downloader for work IDs: `scripts/openalex_download_pdf.sh`
