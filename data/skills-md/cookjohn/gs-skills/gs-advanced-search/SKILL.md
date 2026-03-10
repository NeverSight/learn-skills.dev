---
name: gs-advanced-search
description: Perform advanced Google Scholar search with filters - author, journal, date range, exact phrase, title-only. Constructs proper URL parameters from natural language. Use for precise filtered searches.
argument-hint: "[describe search criteria in natural language]"
---

# Google Scholar Advanced Search

Construct and execute a Google Scholar search using URL parameters based on the user's natural language description.

## Arguments

$ARGUMENTS is a natural language description of the search criteria, e.g.:
- "Search for Einstein's papers on relativity after 2020"
- "Find reviews about CRISPR in Nature"
- "Search for exact phrase 'machine learning' in title only"

## Step 1: Parse search criteria into URL parameters

Map the user's intent to Google Scholar URL parameters:

| Criteria | Parameter | Example |
|----------|-----------|---------|
| Keywords | `q` | `q=gastric+cancer` |
| Author | `as_sauthors` | `as_sauthors="Albert Einstein"` |
| Journal/Source | `as_publication` | `as_publication=Nature` |
| Start year | `as_ylo` | `as_ylo=2020` |
| End year | `as_yhi` | `as_yhi=2025` |
| Exact phrase | `as_epq` | `as_epq=machine+learning` |
| Any of these words (OR) | `as_oq` | `as_oq=immunotherapy+checkpoint` |
| Exclude words | `as_eq` | `as_eq=review` |
| Search scope | `as_occt` | `as_occt=title` (title only) / `as_occt=any` (anywhere) |
| Results per page | `num` | `num=10` (default) or `num=20` (max) |
| Language | `hl` | `hl=en` or `hl=zh-CN` |

**Construction examples:**
- "Einstein 2020 年以后在 Nature 上的论文" → `scholar?as_sauthors=Einstein&as_publication=Nature&as_ylo=2020&hl=en`
- "标题包含 CRISPR 的论文" → `scholar?q=CRISPR&as_occt=title&hl=en`
- "精确搜索 'deep learning' 排除 review" → `scholar?as_epq=deep+learning&as_eq=review&hl=en`
- "搜索 immunotherapy 或 checkpoint 相关论文" → `scholar?as_oq=immunotherapy+checkpoint&hl=en`

**Notes:**
- When `as_sauthors`, `as_publication`, etc. are used, `q` can be omitted or used for additional keywords
- Always include `hl=en` for consistent results
- Use `num=10` (default) to minimize CAPTCHA risk

## Step 2: Navigate

Use `mcp__chrome-devtools__navigate_page`:
- url: `https://scholar.google.com/scholar?{CONSTRUCTED_PARAMS}`

## Step 3: Extract results (evaluate_script)

Same extraction script as gs-search step 2:

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
      citedByUrl: citedByEl?.href || '',
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

## Step 4: Report

```
Advanced search on Google Scholar:
Query parameters: {list the parameters used}
{total}

1. {title}
   Authors: {authors} | {journalYear}
   Cited by: {citedBy} | [Full text]({fullTextUrl})
   Data-CID: {dataCid}

2. ...
```

Always show the constructed URL parameters so the user understands how the query was built.

## Notes

- This skill uses 2 tool calls: `navigate_page` + `evaluate_script`
- Google Scholar does NOT support publication type filtering (review, clinical trial, etc.) — use keywords instead
- Impact factor is not available in Google Scholar — use citation count as a proxy
- The key difference from gs-search is URL parameter construction — this skill translates natural language to Google Scholar query parameters
