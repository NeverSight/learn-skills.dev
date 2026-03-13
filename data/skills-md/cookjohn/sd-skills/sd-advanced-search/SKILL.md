---
name: sd-advanced-search
description: Advanced search on ScienceDirect with filters like author, journal, year, title, keywords. Use when the user wants filtered academic paper search.
argument-hint: "[search terms and filters]"
---

# ScienceDirect Advanced Search

Perform a filtered search on ScienceDirect by constructing URL parameters directly.

## URL Parameter Reference

Build the search URL as `{BASE_URL}/search?{params}&show=25` using these parameters:

| Param | Field | Example |
|-------|-------|---------|
| `qs` | All fields (keywords) | `machine learning` |
| `tak` | Title, abstract or keywords | `neural network` |
| `title` | Title only | `transformer` |
| `authors` | Author name(s) | `Hinton` |
| `pub` | Journal or book title | `Nature` |
| `date` | Year or year range | `2023` or `2020-2025` |
| `volume` | Volume number(s) | `5` or `7-11` |
| `issue` | Issue number(s) | `1` or `1-3` |
| `page` | Page number(s) | `55` or `1-9` |
| `docId` | ISSN or ISBN | `0957-4174` |
| `affiliations` | Author affiliation | `MIT` |
| `references` | Cited references | `Smith 2020` |

Multiple parameters can be combined. For example:
```
{BASE_URL}/search?tak=deep+learning&authors=LeCun&date=2020-2025&show=25
```

## Steps

### Step 1: Parse user intent

From `$ARGUMENTS`, identify which fields the user wants to filter on. Map natural language to URL parameters:
- "by author X" → `authors=X`
- "in journal Y" → `pub=Y`
- "from 2020 to 2025" / "since 2020" → `date=2020-2025`
- "about topic Z" → `tak=Z` or `qs=Z`
- "titled ..." → `title=...`

### Step 2: Navigate

Use `navigate_page` to the constructed URL. **Always include `initScript`** to prevent bot detection:
```
initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
```

### Step 3: Check access

- If the page shows "Are you a robot" or captcha: **auto-click the Cloudflare Turnstile checkbox** using the procedure below. If auto-click fails after 2 attempts, tell the user "请在浏览器中完成验证后告知我。"
- If the URL no longer contains `sciencedirect` or `search` after navigation, the user may have been redirected to a login/authentication page. Tell the user: "页面被重定向，请在浏览器中完成登录或认证后告知我。" Then wait.

#### Cloudflare Turnstile auto-click procedure

When a captcha page is detected (title "请稍候…" or body contains "Are you a robot"):

1. **Wait for the Turnstile iframe to load** — use `evaluate_script` to poll for `#captcha-box` (up to 8s).
2. **Take a snapshot** — use `take_snapshot` to get the a11y tree. The checkbox is inside a cross-origin iframe but Chrome DevTools MCP can see it:
   ```
   Iframe "包含 Cloudflare 安全质询的小组件"
     checkbox "确认您是真人"   ← target uid
   ```
3. **Click the checkbox** — use `click(uid)` on the checkbox element.
4. **Wait and verify** — wait 3-5s, then check if `document.contentType` changed or the page URL changed (indicating success). If still on captcha, retry once or fall back to asking the user.

### Step 4: Extract results

Use `evaluate_script` with built-in waiting (same as `sd-search`). Do NOT use `wait_for` — it returns oversized snapshots.

```javascript
async () => {
  // Wait for results to load (up to 10s)
  for (let i = 0; i < 20; i++) {
    if (document.querySelector('li.ResultItem') || document.querySelector('.search-body-results-text')) break;
    await new Promise(r => setTimeout(r, 500));
  }

  const items = document.querySelectorAll('li.ResultItem');
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

    papers.push({
      rank: i + 1,
      title: titleLink?.textContent?.trim() || '',
      pii, doi: doi || '',
      journal: journal?.textContent?.trim() || '',
      date, authors, articleType, openAccess: isOpenAccess,
    });
  }

  const totalText = document.querySelector('.search-body-results-text')?.textContent?.trim() || '';
  const pageInfo = document.querySelector('.Pagination li:first-child')?.textContent?.trim() || '';
  return { papers, totalResults: totalText, pageInfo };
}
```

### Step 5: Present results

Same format as sd-search. Additionally, show the applied filters at the top:

```
Search filters: author={X}, journal={Y}, year={Z}
Found {totalResults}. {pageInfo}

1. {title} ...
```

## Notes

- URL parameter approach avoids form filling, keeping operations to 2 tool calls.
- All parameters are optional and combinable.
- If the user provides a very specific query (e.g., DOI or PII), consider using `sd-paper-detail` instead.
