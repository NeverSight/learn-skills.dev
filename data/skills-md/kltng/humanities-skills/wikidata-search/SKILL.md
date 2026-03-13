---
name: wikidata-search
description: Search for items and properties on Wikidata and retrieve entity details, claims, and external identifiers. Supports both keyword search (Wikidata Action API) and semantic/hybrid search (Wikidata Vector Database), plus direct entity retrieval (Special:EntityData) and structured querying (WDQS SPARQL).
version: 1.1.0
---

# Wikidata Search Skill

Search and retrieve data from Wikidata, the free knowledge base.

## Critical: Things Claude Won't Know Without This Skill

### Wikidata Vector Database (semantic search)

This is the highest-value feature of this skill. The **Wikidata Vector Database** at `wd-vectordb.wmcloud.org` provides semantic/hybrid search over all Wikidata items — something you can't do with the standard Action API or SPARQL.

**A descriptive `User-Agent` header is required or you get 403.**

```bash
curl -H 'User-Agent: WikidataSearchSkill/1.0 (contact: you@example.com)' \
  'https://wd-vectordb.wmcloud.org/item/query/?query=historical+Chinese+cartography&lang=all&K=20'
```

Response includes `QID`, `similarity_score`, `rrf_score`, and `source` (vector vs keyword).

Property search: replace `/item/query/` with `/property/query/`.

Optional params: `lang`, `K` (result count), `instanceof` (comma-separated QIDs), `rerank`.

### WDQS SPARQL also requires User-Agent

```bash
curl -G 'https://query.wikidata.org/sparql' \
  --data-urlencode 'query=SELECT ?item ?label WHERE { ?item wdt:P31 wd:Q12857432 . ?item rdfs:label ?label . FILTER(LANG(?label)="en") }' \
  -H 'Accept: application/sparql-results+json' \
  -H 'User-Agent: WikidataSearchSkill/1.0 (contact: you@example.com)'
```

### External identifiers live in claims

```python
# claims[property_id][0]["mainsnak"]["datavalue"]["value"] → identifier string
# Common: P214 (VIAF), P244 (LoC), P227 (GND), P213 (ISNI), P268 (BnF)
```

## Choosing an Access Method

| Need | Method |
|------|--------|
| Keyword search by label/alias | Action API `wbsearchentities` |
| Semantic / fuzzy concept discovery | **Vector Database** (hybrid vector + keyword) |
| Fetch a known entity's JSON | `Special:EntityData/{ID}.json` |
| Complex graph queries / reporting | WDQS SPARQL |

## Python Script

Use `scripts/wikidata_api.py` for programmatic access (zero dependencies):

```python
from scripts.wikidata_api import WikidataAPI
wd = WikidataAPI()

# Keyword search
results = wd.search("Zhu Xi", language="en", limit=5)

# Semantic search (Vector DB) — the key differentiator
candidates = wd.vector_search_items("historical Chinese cartography", lang="all", k=20)

# Entity retrieval
entity = wd.get_entity("Q9397", props=["labels", "descriptions", "claims"])

# External identifiers
ids = wd.get_identifiers("Q9397", include_labels=True)
# → {'VIAF ID (P214)': '46768804', 'Library of Congress ID (P244)': 'n81008179', ...}

# SPARQL
results = wd.sparql_json("SELECT ?item ?label WHERE { ?item wdt:P31 wd:Q12857432 . ?item rdfs:label ?label . FILTER(LANG(?label)='en') }")

# Direct entity JSON (fast for current state)
data = wd.get_entitydata("Q42", flavor="simple")
```

## API Endpoints Quick Reference

| Endpoint | URL |
|----------|-----|
| Action API | `https://www.wikidata.org/w/api.php` |
| Entity JSON | `https://www.wikidata.org/wiki/Special:EntityData/{ID}.json` |
| SPARQL | `https://query.wikidata.org/sparql` |
| Vector DB | `https://wd-vectordb.wmcloud.org` |

## API Etiquette

- **Rate limit**: 0.5–1s between requests
- **User-Agent**: Required for Vector DB and WDQS (include contact info)
- **Respect 429**: Honor `Retry-After` headers
- **Action API**: Use `maxlag` parameter; batch with pipe-separated IDs (max 50)
- **SPARQL**: Request only needed fields; use `LIMIT`

## Related Skills

- **cbdb-api**: Cross-reference Wikidata entities with CBDB biographical data for Chinese historical figures
- **chgis-tgaz**: Look up historical places found via Wikidata in the CHGIS Temporal Gazetteer for detailed administrative history

## Resources

- `references/api_reference.md` — Complete API specs for all four access methods
- `scripts/wikidata_api.py` — Full-featured Python client with rate limiting, retries, and identifier extraction
