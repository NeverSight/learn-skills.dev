---
name: polars-dovmed
description: Search 2.4M+ full-text PubMed Central Open Access papers for literature reviews, trends, and data extraction.
user-invocable: true
---

# polars-dovmed

Full-text search across 2.4M+ PMC Open Access papers for literature discovery and extraction tasks.

## Instructions

1. Load the API key from a secure location.
2. Run a full-text search or metadata query.
3. Extract required fields (titles, DOIs, accessions, snippets).
4. Summarize results and cite sources.

## Quick Reference

| Task | Action |
|------|--------|
| API key | `POLARS_DOVMED_API_KEY` in env or `~/.config/polars-dovmed/.env` |
| Base URL | `https://api.newlineages.com` |
| Rate limit | 100 queries/hour |

## Input Requirements

- API key (`POLARS_DOVMED_API_KEY`)
- Search query and filters (year, journal, organism, etc.)

## Output

- Paper lists with metadata (PMC ID, DOI, title, year)
- Matched text snippets
- Extracted entities (genes, accessions, terms)

## Quality Gates

- [ ] API key loaded successfully
- [ ] Query results match expected scope
- [ ] Extracted fields validated for completeness

## Examples

### Example 1: Minimal search (Python)

```python
import httpx

headers = {"X-API-Key": "YOUR_KEY"}
resp = httpx.post(
    "https://api.newlineages.com/search",
    headers=headers,
    json={"query": "CRISPR archaea", "limit": 10},
)
print(resp.json())
```

## Troubleshooting

**Issue**: 401 Unauthorized
**Solution**: Verify `POLARS_DOVMED_API_KEY` and reload the environment.

**Issue**: 429 Rate limited
**Solution**: Wait for quota reset or reduce request frequency.
