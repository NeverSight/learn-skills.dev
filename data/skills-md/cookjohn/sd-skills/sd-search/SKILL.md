---
name: sd-search
description: Search for academic papers on ScienceDirect. Use when the user wants to find papers by keyword on ScienceDirect/Elsevier.
argument-hint: "[search keywords]"
---

# ScienceDirect Basic Search

Search for academic papers on ScienceDirect using Chrome DevTools MCP.

## Important: Determine the ScienceDirect base URL

Before the first operation, check the current browser page URL to determine which ScienceDirect domain the user is accessing. Store it as `BASE_URL`. Common patterns:
- Direct access: `https://www.sciencedirect.com`
- Institutional proxy: URL containing `sciencedirect` in the hostname (e.g. WebVPN or EZProxy)

Use whatever origin the user's browser is currently on. If no ScienceDirect page is open, ask the user which URL to use.

## Steps

### Step 1: Navigate to search results

Use `navigate_page` to go to:

```
{BASE_URL}/search?qs={QUERY}&show=25
```

Where `{QUERY}` is the URL-encoded search keywords from `$ARGUMENTS`.

**Important**: Always include `initScript` to prevent bot detection:
```
initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
```

### Step 2: Check access

After navigation, verify the page loaded correctly:
- If the page shows "Are you a robot" or captcha: **auto-click the Cloudflare Turnstile checkbox** using the procedure below. If auto-click fails after 2 attempts, tell the user "请在浏览器中完成验证后告知我。"
- If the URL no longer contains `sciencedirect` or `search`, the user may have been redirected to a login/authentication page. Tell the user: "页面被重定向，请在浏览器中完成登录或认证后告知我。" Then wait.
- Otherwise, proceed.

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

### Step 3: Extract search results

Use `evaluate_script` with built-in waiting. Do NOT use `wait_for` — it returns the full page snapshot which can exceed token limits (250K+ chars) on ScienceDirect pages.

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
      pii,
      doi: doi || '',
      journal: journal?.textContent?.trim() || '',
      date,
      authors,
      articleType,
      openAccess: isOpenAccess,
    });
  }

  const totalText = document.querySelector('.search-body-results-text')?.textContent?.trim() || '';
  const pageInfo = document.querySelector('.Pagination li:first-child')?.textContent?.trim() || '';

  return { papers, totalResults: totalText, pageInfo };
}
```

### Step 4: Present results

Format results as a numbered list:

```
Found {totalResults}. {pageInfo}

1. {title}
   Authors: {authors}
   Journal: {journal} | {date}
   DOI: {doi} | PII: {pii}
   Type: {articleType} | Open Access: {yes/no}

2. ...
```

## Key CSS Selectors

| Element | Selector |
|---------|----------|
| Result items | `li.ResultItem` |
| Title link | `a.result-list-title-link` |
| Journal link | `a.subtype-srctitle-link` |
| Authors | `.Authors .author` |
| Date | `.srctitle-date-fields > span` (last span) |
| DOI | `data-doi` attribute on `li.ResultItem` |
| Article type | `.article-type` |
| Open access indicator | `.access-label` |
| Total results | `.search-body-results-text` |
| Checkbox (for batch ops) | `.checkbox-input` (id = PII) |
| Next page link | `.next-link a` |

## URL Parameters

| Param | Description | Example |
|-------|-------------|---------|
| `qs` | Query string | `deep learning` |
| `show` | Results per page | `25`, `50`, `100` |
| `offset` | Pagination offset | `0`, `25`, `50` |
| `sortBy` | Sort order | `date` (omit for relevance) |

## Notes

- Results include PII identifiers needed for detail extraction, PDF download, and citation export.
- Each result checkbox `id` equals the PII, used for batch export/download.
- This skill performs at most 2 tool calls: `navigate_page` + `evaluate_script`.
