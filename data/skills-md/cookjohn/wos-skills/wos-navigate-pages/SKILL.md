---
name: wos-navigate-pages
description: Navigate to a specific page of WoS search results, or load more results from the last search.
argument-hint: "[page number or 'next'/'prev']"
user-invocable: true
disable-model-invocation: false
---

# WoS Navigate Pages

Load a specific page of results from the current WoS search.

## Two Approaches

### Approach A: URL-based (when browser is on a results page)

The results URL follows the pattern:
```
/wos/woscc/summary/{session-uuid}/{sort}/{page-number}
```

Modify the page number in the URL and navigate. Then extract via `evaluate_script` with DOM selectors. Uses **2 tool calls**.

### Approach B: API-based (preferred, 1 tool call)

Re-run the search API with `retrieve.first` offset:

```javascript
async () => {
  const sid = performance.getEntriesByType('resource')
    .filter(r => r.name.includes('SID='))
    .map(r => r.name.match(/SID=([^&]+)/)?.[1])
    .filter(Boolean)[0] || '';

  const page = {TARGET_PAGE};  // 1-based
  const perPage = 50;
  const first = (page - 1) * perPage + 1;

  const response = await fetch(`/api/wosnx/core/runQuerySearch?SID=${sid}`, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=UTF-8', 'Accept': 'application/x-ndjson' },
    body: JSON.stringify({
      "product": "WOSCC",
      "searchMode": "general",
      "viewType": "search",
      "serviceMode": "summary",
      "search": {
        "mode": "general",
        "database": "WOSCC",
        "query": [{SAME_QUERY_AS_ORIGINAL_SEARCH}],
        "editions": [{SAME_EDITIONS}]
      },
      "retrieve": {
        "first": first,
        "count": perPage,
        "history": false,
        "jcr": true,
        "sort": "{SAME_SORT}",
        "analyzes": [],
        "locale": "en"
      },
      "eventMode": null
    })
  });

  const text = await response.text();
  const lines = text.trim().split('\n').map(l => { try { return JSON.parse(l); } catch(e) { return null; } }).filter(Boolean);
  const searchInfo = lines.find(l => l.key === 'searchInfo')?.payload;
  const recordsData = lines.find(l => l.key === 'records')?.payload;

  let records = [];
  if (recordsData) {
    records = Object.entries(recordsData).map(([idx, rec]) => ({
      idx: first + parseInt(idx) - 1,
      wosId: rec.colluid,
      title: rec.titles?.item?.en?.[0]?.title || '',
      authors: rec.names?.author?.en?.filter(Boolean).map(a => a.wos_standard).join('; ') || '',
      source: rec.titles?.source?.en?.[0]?.title || '',
      year: rec.pub_info?.pubyear || '',
      doi: rec.doi || '',
      citations: rec.citation_related?.counts?.WOSCC || 0
    }));
  }

  return { status: 'ok', page, totalResults: searchInfo?.RecordsFound || 0, records };
}
```

## Notes

- API approach uses **1 tool call** only
- Requires remembering the original search query/editions/sort from the prior `wos-search` call
- `retrieve.first` is 1-based record offset (1 = first record, 51 = page 2, etc.)
- 50 records per page, max 100,000 records accessible
