---
name: sd-parse-results
description: Re-parse the currently open ScienceDirect search results page. Internal skill used by other skills.
user-invokable: false
---

# Parse Current ScienceDirect Results Page

Extract structured data from an already-open ScienceDirect search results page without navigating.

## When to use

- After the user has manually navigated to a search results page
- When re-parsing results after sorting or filtering changes
- Called internally by other skills

## Steps

### Step 1: Extract results from current page

Use `evaluate_script` (no navigation needed):

```javascript
() => {
  // Verify we are on a search results page
  if (!window.location.pathname.includes('/search')) {
    return { error: 'Not on a ScienceDirect search results page.' };
  }

  const items = document.querySelectorAll('li.ResultItem');
  if (items.length === 0) {
    return { error: 'No results found on the current page. The page may still be loading.' };
  }

  const papers = [];
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    const titleLink = item.querySelector('a.result-list-title-link');
    const journal = item.querySelector('a.subtype-srctitle-link');
    const dateSpans = item.querySelectorAll('.srctitle-date-fields > span');
    const date = dateSpans.length > 1 ? dateSpans[dateSpans.length - 1].textContent.trim() : '';
    const authors = [...item.querySelectorAll('.Authors .author')].map(a => a.textContent.trim());
    const doi = item.getAttribute('data-doi');
    const pii = titleLink?.href?.match(/pii\/(\w+)/)?.[1] || '';
    const articleType = item.querySelector('.article-type')?.textContent?.trim() || '';
    const isOpenAccess = !!item.querySelector('.access-label');
    const checkboxId = item.querySelector('.checkbox-input')?.id || '';

    papers.push({
      rank: i + 1,
      title: titleLink?.textContent?.trim() || '',
      pii, doi: doi || '',
      journal: journal?.textContent?.trim() || '',
      date, authors, articleType, openAccess: isOpenAccess,
      checkboxId,
    });
  }

  const totalText = document.querySelector('.search-body-results-text')?.textContent?.trim() || '';
  const pageInfo = document.querySelector('.Pagination li:first-child')?.textContent?.trim() || '';
  const currentUrl = window.location.href;

  return { papers, totalResults: totalText, pageInfo, currentUrl };
}
```

### Step 2: Return structured data

Return the extracted data. The `checkboxId` field (= PII) is important for batch export and download operations.

## Notes

- This skill uses only 1 tool call (`evaluate_script`).
- It does NOT navigate — it reads the current page as-is.
- If results are empty, the page may still be loading; consider adding a wait loop inside the script or retrying after a brief delay.
