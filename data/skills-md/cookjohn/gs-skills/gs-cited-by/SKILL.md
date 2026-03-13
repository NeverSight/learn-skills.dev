---
name: gs-cited-by
description: Find papers that cite a given Google Scholar paper. Tracks citation chains using data-cid (cluster ID). Use when user wants to see who cited a specific paper.
argument-hint: "[data-cid or paper title to look up]"
---

# Google Scholar — Cited By (Citation Tracking)

Find all papers that cite a given paper. Uses Google Scholar's `cites` parameter with the paper's cluster ID (data-cid).

## Arguments

$ARGUMENTS can be:
- A `data-cid` from a previous search result (e.g., `TFS2GgoGiNUJ`)
- A paper title (will search first to find the data-cid)

## Steps

### Step 1: Resolve data-cid

**If $ARGUMENTS is a data-cid** (alphanumeric string, no spaces): use it directly.

**If $ARGUMENTS is a title or description**: first search to find the data-cid:
1. Use `gs-search` with the title as keywords
2. Match the target paper in results by title similarity
3. Extract its `dataCid`

### Step 2: Navigate to "Cited by" page

Use `mcp__chrome-devtools__navigate_page`:
- url: `https://scholar.google.com/scholar?cites={DATA_CID}&hl=en&num=10`

Replace `{DATA_CID}` with the resolved cluster ID.

### Step 3: Extract citing papers (evaluate_script)

Same extraction script as gs-search:

```javascript
async () => {
  for (let i = 0; i < 20; i++) {
    if (document.querySelector('#gs_res_ccl') || document.querySelector('#gs_captcha_ccl')) break;
    await new Promise(r => setTimeout(r, 500));
  }

  if (document.querySelector('#gs_captcha_ccl') || document.body.innerText.includes('unusual traffic')) {
    return { error: 'captcha', message: 'Google Scholar requires CAPTCHA verification. Please complete it in your browser, then tell me to continue.' };
  }

  const items = document.querySelectorAll('#gs_res_ccl .gs_r.gs_or.gs_scl');
  const results = Array.from(items).map((item, i) => {
    const titleEl = item.querySelector('.gs_rt a');
    const meta = item.querySelector('.gs_a')?.textContent || '';
    const parts = meta.split(' - ');
    const authors = parts[0]?.trim() || '';
    const journalYear = parts[1]?.trim() || '';
    const citedByEl = item.querySelector('.gs_fl a[href*="cites"]');

    return {
      n: i + 1,
      title: titleEl?.textContent?.trim() || item.querySelector('.gs_rt')?.textContent?.trim() || '',
      href: titleEl?.href || '',
      authors,
      journalYear,
      citedBy: citedByEl?.textContent?.match(/\d+/)?.[0] || '0',
      dataCid: item.getAttribute('data-cid') || '',
      fullTextUrl: (item.querySelector('.gs_ggs a') || item.querySelector('.gs_or_ggsm a'))?.href || '',
      snippet: item.querySelector('.gs_rs')?.textContent?.trim()?.substring(0, 200) || ''
    };
  });

  const totalText = document.querySelector('#gs_ab_md')?.textContent?.trim() || '';
  const currentUrl = window.location.href;
  return { total: totalText, resultCount: results.length, currentUrl, results };
}
```

### Step 4: Report

```
Papers citing [{original paper title}] (data-cid: {DATA_CID}):
{total}

1. {title}
   Authors: {authors} | {journalYear}
   Cited by: {citedBy}
   Data-CID: {dataCid}

2. ...
```

## Follow-up

- **See more citing papers**: use `gs-navigate-pages` (pagination works on cited-by pages too)
- **Export citing papers**: use `gs-export` with the data-cid(s)
- **Recursive citation tracking**: use `gs-cited-by` on any of the citing papers

## Notes

- This skill uses 2-3 tool calls: optional search + `navigate_page` + `evaluate_script`
- The `cites` parameter uses the cluster ID (data-cid), NOT a DOI or paper ID
- Cited-by pages support the same pagination as regular search (`start` parameter)
- Citation count on Google Scholar is typically higher than PubMed because it includes non-PubMed sources (books, theses, preprints, etc.)
