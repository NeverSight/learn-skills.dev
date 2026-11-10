---
name: openalex
description: Query and analyze scholarly literature using the OpenAlex API. Use for literature searches, finding papers by author or institution, citation analysis, and bibliometric queries.
---

# OpenAlex literature search

Query the [OpenAlex](https://openalex.org) API for academic papers, authors, institutions, and citation data.

## CLI

Use the bundled dependency-aware CLI. Its inline script metadata installs
`requests` in an isolated uv environment without modifying the caller's lockfile.

```bash
OPENALEX="<skill-directory>/scripts/openalex.py"
uv run --script "$OPENALEX" search-works "CRISPR"
```

Do not import `openalex_client.py` from `uv run python -`; stdin scripts ignore
the client's inline dependency metadata.

The client handles rate limiting and retries. Set `OPENALEX_API_KEY` in the
environment; OpenAlex permits limited no-key requests.

## Key Patterns

### Search works
```bash
uv run --script "$OPENALEX" search-works "CRISPR" \
  --filter 'publication_year=>2020' --filter is_oa=true \
  --sort cited_by_count:desc
```

### Resolve names before filtering

Names are ambiguous. Search for the entity, inspect candidate identifiers, affiliations, and topics, then filter by the selected OpenAlex ID:

```bash
uv run --script "$OPENALEX" search-works "Jennifer Doudna" --per-page 5
# Inspect candidates, then filter with the selected OpenAlex author ID:
uv run --script "$OPENALEX" search-works "CRISPR" \
  --filter authorships.author.id=A1969205032
```

### Get entity by external ID
```bash
uv run --script "$OPENALEX" get-entity works \
  'https://doi.org/10.1038/s41586-021-03819-2'
uv run --script "$OPENALEX" get-entity authors \
  'https://orcid.org/0000-0003-1613-5981'
```

### Batch DOI lookup (up to 100 per request)
```bash
uv run --script "$OPENALEX" batch-lookup works \
  10.1038/s41586-021-03819-2 10.1038/s41586-020-2649-2 --id-field doi
```

### Aggregate by field
```bash
uv run --script "$OPENALEX" group-by works publication_year \
  --filter authorships.author.id=A1969205032
```

## Filter Syntax

```
Single:     --filter publication_year=2023
AND:        --filter 'publication_year=>2020' --filter is_oa=true
OR:         --filter 'type=journal-article|book'
NOT:        --filter 'type=!paratext'
Range:      --filter publication_year=2020-2024
Greater:    --filter 'cited_by_count=>100'
Both inst:  --filter authorships.institutions.id=ID1+ID2
Either:     --filter 'authorships.institutions.id=ID1|ID2'
```

Common filters: `publication_year`, `is_oa`, `cited_by_count`, `type`, `authorships.author.id`, `authorships.institutions.id`, `primary_location.source.id`, `topics.id`, `has_doi`.

## Attribution

OpenAlex client adapted from [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) (MIT License).
