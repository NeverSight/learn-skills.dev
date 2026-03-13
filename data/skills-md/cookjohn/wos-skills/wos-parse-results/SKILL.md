---
name: wos-parse-results
description: Parse search results from the current WoS results page or API response. Internal skill used by other skills.
argument-hint: "[number of results to extract, default 10]"
user-invocable: false
disable-model-invocation: false
---

# WoS Parse Results

Internal skill for extracting structured data from WoS. Two modes: API response parsing (preferred) or DOM scraping (fallback).

## Mode A: API Response Parsing (preferred)

When using the `runQuerySearch` API, the response is NDJSON. Parse records from the `records` payload:

```javascript
// Parse NDJSON response text
const lines = text.trim().split('\n').map(l => { try { return JSON.parse(l); } catch(e) { return null; } }).filter(Boolean);
const searchInfo = lines.find(l => l.key === 'searchInfo')?.payload;
const recordsData = lines.find(l => l.key === 'records')?.payload;

const records = Object.entries(recordsData).map(([idx, rec]) => ({
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
  abstract: rec.abstract?.basic?.en?.abstract?.replace(/<[^>]*>/g, '') || '',
  docType: rec.doctypes?.[0] || '',
  oa: rec.oa || false
}));
```

## Mode B: DOM Scraping (fallback)

When the browser is on a results page and API is not available:

```javascript
async () => {
  for (let i = 0; i < 20; i++) {
    if (document.querySelector('app-record')) break;
    await new Promise(r => setTimeout(r, 500));
  }

  const records = [...document.querySelectorAll('app-record')].map((rec, idx) => {
    const titleEl = rec.querySelector('a[data-ta="summary-record-title-link"]');
    const title = titleEl?.textContent?.trim() || '';
    const href = titleEl?.href || '';
    const wosId = href.match(/WOS:\w+/)?.[0] || '';
    const authorEls = rec.querySelectorAll('a[data-ta*="DisplayName-author"]');
    const authors = [...authorEls].map(a => a.textContent?.trim()).join('; ');
    const sourceEl = rec.querySelector('a[data-ta="jcr-link-menu"]');
    const source = sourceEl?.textContent?.trim()?.replace('arrow_drop_down', '') || '';
    const citedEl = rec.querySelector('a[data-ta="stat-number-citation-related-count"]');
    const citations = citedEl?.textContent?.trim() || '0';
    return { idx: idx + 1, title, wosId, authors, source, citations };
  });

  return { status: 'ok', recordCount: records.length, records };
}
```

## Notes

- Mode A is always preferred — structured JSON, no selector fragility
- Mode B is fallback when already on a results page without API access
- DOM selectors may miss records due to lazy loading or dynamic rendering
