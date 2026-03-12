---
name: wos-search
description: Search Web of Science by topic, author, title, DOI, or advanced query. Supports edition/database filtering and sort.
argument-hint: "[search keywords] [--edition SCI/SSCI/...] [--sort citations/date/relevance] [--db woscc|alldb|...]"
user-invocable: true
disable-model-invocation: false
---

# WoS Search

Search Web of Science via internal API. Supports edition filtering, sorting, and multiple databases — all in a single `evaluate_script` call.

## Important: Browser Prerequisite

The browser must be on any `webofscience.com` page (logged in). The skill calls the WoS internal API directly via `fetch`, so no page navigation is needed.

## Language Guidance

WoS databases (especially SCI/SSCI) primarily index English-language literature. If the user provides Chinese keywords, translate to English (e.g., "价值共创" → "value co-creation"). Inform the user about the translation.

## Parameter Reference

### Database (`product`)

| User says | product | Description |
|-----------|---------|-------------|
| "core collection" / default | `WOSCC` | WoS Core Collection |
| "all databases" | `ALLDB` | All databases combined |
| "medline" | `MEDLINE` | Biomedical literature |
| "preprint" | `PPRN` | Preprint Citation Index |
| "scielo" | `SCIELO` | SciELO Citation Index |

### Edition filtering (Core Collection only)

| User says | editions value |
|-----------|---------------|
| "SCI" / "science" | `WOS.SCI` |
| "SSCI" / "social science" | `WOS.SSCI` |
| "CPCI" / "conference" | `WOS.CPCI-S`, `WOS.CPCI-SSH` |
| "all" / default | omit `editions` field (or include all) |

Multiple editions can be combined: `["WOS.SCI", "WOS.SSCI"]`

### Sort options

| User says | sort value |
|-----------|-----------|
| "citations" / "most cited" | `times-cited-descending` |
| "newest" / "latest" | `date-descending` |
| "oldest" | `date-ascending` |
| "relevance" / default | `relevance` |
| "usage" | `usage-count-last-180-days-descending` |

### Field mapping (for query rows)

| User says | rowField |
|-----------|----------|
| topic / keyword / about | TS |
| title | TI |
| author | AU |
| DOI | DO |
| journal / source | SO |
| year | PY |
| affiliation / institution | OG |
| abstract | AB |
| funding | FO |
| country | CU |

## Steps

### Step 1: Build API Request Body

```json
{
  "product": "WOSCC",
  "searchMode": "general",
  "viewType": "search",
  "serviceMode": "summary",
  "search": {
    "mode": "general",
    "database": "WOSCC",
    "query": [
      {"rowField": "TS", "rowText": "USER_QUERY"}
    ],
    "editions": ["WOS.SSCI"]
  },
  "retrieve": {
    "count": 10,
    "history": true,
    "jcr": true,
    "sort": "times-cited-descending",
    "analyzes": [],
    "locale": "en"
  },
  "eventMode": null
}
```

- `query`: array of `{rowField, rowText}` objects. For multiple conditions, add `rowBoolean` (`AND`/`OR`/`NOT`) to subsequent rows.
- `editions`: optional, omit for all editions.
- `count`: number of records to retrieve (default 10, max 50).
- `sort`: default `relevance`.

### Step 2: Execute API Call via evaluate_script

**This is the only tool call needed — 1 call total.**

If the browser was previously on a non-WoS page (e.g., after following a publisher link), SID will be lost. In that case, **first navigate back to any WoS page** (`navigate_page` to `https://www.webofscience.com/wos/woscc/basic-search`) to re-establish the session, then run the API call. This adds 1 extra tool call (2 total).

Alternatively, use the **URL-based fallback** (Step 2B below) which always works regardless of SID state.

```javascript
async () => {
  // Extract SID from network history
  const sid = performance.getEntriesByType('resource')
    .filter(r => r.name.includes('SID='))
    .map(r => r.name.match(/SID=([^&]+)/)?.[1])
    .filter(Boolean)[0] || '';

  if (!sid) return { status: 'no_session', message: 'SID lost (likely navigated to external site). Use Step 2B or navigate to any WoS page first.' };

  const response = await fetch(`/api/wosnx/core/runQuerySearch?SID=${sid}`, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=UTF-8', 'Accept': 'application/x-ndjson' },
    body: JSON.stringify({
      "product": "{PRODUCT}",
      "searchMode": "general",
      "viewType": "search",
      "serviceMode": "summary",
      "search": {
        "mode": "general",
        "database": "{PRODUCT}",
        "query": [{QUERY_ROWS}],
        "editions": [{EDITIONS}]
      },
      "retrieve": {
        "count": {COUNT},
        "history": true,
        "jcr": true,
        "sort": "{SORT}",
        "analyzes": [],
        "locale": "en"
      },
      "eventMode": null
    })
  });

  const text = await response.text();
  const lines = text.trim().split('\n').map(line => {
    try { return JSON.parse(line); } catch(e) { return null; }
  }).filter(Boolean);

  const searchInfo = lines.find(l => l.key === 'searchInfo')?.payload;
  const recordsData = lines.find(l => l.key === 'records')?.payload;

  let records = [];
  if (recordsData) {
    records = Object.entries(recordsData).map(([idx, rec]) => ({
      idx: parseInt(idx),
      wosId: rec.colluid,
      title: rec.titles?.item?.en?.[0]?.title || '',
      authors: rec.names?.author?.en?.filter(Boolean).map(a => a.wos_standard).join('; ') || '',
      source: rec.titles?.source?.en?.[0]?.title || '',
      year: rec.pub_info?.pubyear || '',
      vol: rec.pub_info?.vol || '',
      issue: rec.pub_info?.issue || '',
      pages: rec.pub_info?.page_no || '',
      doi: rec.doi || '',
      citations: rec.citation_related?.counts?.WOSCC || 0,
      citationsAll: rec.citation_related?.counts?.ALLDB || 0,
      refCount: rec.ref_count || 0,
      abstract: rec.abstract?.basic?.en?.abstract?.replace(/<[^>]*>/g, '')?.substring(0, 300) || '',
      docType: rec.doctypes?.[0] || '',
      oa: rec.oa || false
    }));
  }

  return {
    status: 'ok',
    totalResults: searchInfo?.RecordsFound || 0,
    recordsSearched: searchInfo?.RecordsSearched || 0,
    queryId: searchInfo?.QueryID || '',
    records
  };
}
```

### Step 3: Present Results

Display as a table:

```
Found **{totalResults}** results in {database} ({edition}).
Sorted by: {sort}.

| # | Title | Authors | Source | Year | Cited | WoS ID |
|---|-------|---------|--------|------|-------|--------|
| 1 | {title} | {authors} | {source} | {year} | {citations} | {wosId} |
| ... |
```

Offer next actions:
- "Use `/wos-paper-detail {WoS ID}` for detailed information"
- "Use `/wos-export` to export results"
- To see more results, re-run with higher `count` or use `/wos-navigate-pages`

### Step 2B: URL-based Fallback (when SID is lost)

If API returns `no_session` (e.g., after navigating to an external publisher site), fall back to URL navigation:

```
navigate_page({
  url: "https://www.webofscience.com/wos/{db}/general-summary?queryJson={ENCODED_QUERY_JSON}",
  initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})
```

Then extract results via `evaluate_script` with DOM selectors (see `wos-parse-results` Mode B), or re-attempt the API call (SID will be re-established after the navigation).

**When to use**: After the browser visited an external site (publisher, DOI link, etc.) and `performance.getEntriesByType('resource')` no longer contains WoS SID entries.

## Notes

- **1 tool call** (API) or **2 tool calls** (navigate + API/DOM) if SID is lost
- API returns NDJSON (newline-delimited JSON); parse line by line
- SID is extracted from browser's performance resource entries
- **SID loss**: Navigating to external sites clears performance entries. Recover by navigating to any WoS page first, or use URL-based fallback (Step 2B)
- `editions` field uses format `WOS.SCI`, `WOS.SSCI`, `WOS.CPCI-S`, etc.
- For Chinese keywords in SCI/SSCI, translate to English first
- Max 50 records per request; use `retrieve.count` to control
- `history: true` saves the search to WoS session history
