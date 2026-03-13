---
name: gs-fulltext
description: Get full-text access links for a Google Scholar paper - PDF, DOI, Sci-Hub, and publisher links. Use when user wants to read or download a paper's full text.
argument-hint: "[data-cid or result number from previous search]"
---

# Google Scholar Full Text Access

Resolve and present all full-text access options for a paper found in Google Scholar search results.

## Arguments

$ARGUMENTS can be:
- A `data-cid` from a previous search result
- A result number (e.g., `3`) referring to a previous search result

## Prerequisites

This skill works best after a previous `gs-search` or `gs-advanced-search` call, which already extracts `fullTextUrl` and `href` for each result. If those are available, use them directly.

## Steps

### Step 1: Collect links from search results

From the previous search result, extract these fields for the target paper:
- `fullTextUrl`: direct PDF/HTML link (from `.gs_ggs a`)
- `href`: link to the paper's publisher page (from `.gs_rt a`)
- `dataCid`: cluster ID

If no previous search context is available, search for the paper first using `gs-search`.

### Step 2: Resolve additional links (evaluate_script)

Navigate to the Google Scholar results page (if not already there), then extract full-text links for the specific paper:

```javascript
async () => {
  const cid = "DATA_CID_HERE";

  // Find the result item by data-cid
  const item = document.querySelector(`.gs_r.gs_or.gs_scl[data-cid="${cid}"]`);
  if (!item) return { error: 'not_found', message: 'Paper not found on current page. Try searching again.' };

  const titleEl = item.querySelector('.gs_rt a');
  const title = titleEl?.textContent?.trim() || item.querySelector('.gs_rt')?.textContent?.trim() || '';
  const paperUrl = titleEl?.href || '';

  // Full-text PDF/HTML link (shown on the right side of results)
  const fullTextEl = item.querySelector('.gs_ggs a') || item.querySelector('.gs_or_ggsm a');
  const fullTextUrl = fullTextEl?.href || '';
  const fullTextType = fullTextEl?.querySelector('span.gs_ctg2')?.textContent?.trim() || '';

  // Meta info for context
  const meta = item.querySelector('.gs_a')?.textContent || '';
  const parts = meta.split(' - ');
  const authors = parts[0]?.trim() || '';
  const journalYear = parts[1]?.trim() || '';

  // Try to extract DOI from paper URL
  let doi = '';
  if (paperUrl.includes('doi.org/')) {
    doi = paperUrl.replace(/^https?:\/\/(dx\.)?doi\.org\//, '');
  }

  // Build access links
  const links = {};

  if (fullTextUrl) {
    links.fullText = fullTextUrl;
    links.fullTextType = fullTextType || (fullTextUrl.endsWith('.pdf') ? '[PDF]' : '[HTML]');
  }

  if (paperUrl) {
    links.publisher = paperUrl;
  }

  if (doi) {
    links.doi = `https://doi.org/${doi}`;
    links.scihub = `https://sci-hub.ru/${doi}`;
  } else if (paperUrl) {
    // Sci-Hub also works with direct URLs
    links.scihub = `https://sci-hub.ru/${paperUrl}`;
  }

  return {
    dataCid: cid,
    title,
    authors,
    journalYear,
    doi,
    fullTextUrl,
    fullTextType,
    paperUrl,
    links
  };
}
```

### Step 3: Report

```
## Full Text Links — {title}

**Authors:** {authors} | {journalYear}

**Direct Full Text:**
{links.fullText ? "- " + links.fullTextType + " " + links.fullText : "No direct full text link available"}

**Publisher Page:**
{links.publisher ? "- " + links.publisher : "N/A"}

**DOI:**
{links.doi ? "- " + links.doi : "No DOI detected"}

**Sci-Hub:**
{links.scihub ? "- " + links.scihub : "N/A"}
```

### Step 4: Open full text (optional)

If the user wants to read the paper immediately, use `mcp__chrome-devtools__new_page` to open the preferred link in this priority:
1. `fullTextUrl` (direct PDF/HTML, usually free)
2. DOI link (may require subscription)
3. Sci-Hub link (fallback)
4. Publisher page

## Notes

- This skill uses 1-2 tool calls: `evaluate_script` (if already on results page) or `navigate_page` + `evaluate_script`
- Google Scholar's full-text links (`.gs_ggs`) are usually free/open-access PDFs
- DOI may not always be extractable from the paper URL
- Sci-Hub works with both DOI and direct URL
- Opening full text in a new tab adds 1 more tool call (`new_page`)
