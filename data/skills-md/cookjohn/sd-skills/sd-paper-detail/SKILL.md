---
name: sd-paper-detail
description: Extract full metadata from a ScienceDirect article page (abstract, authors, keywords, DOI, references, PDF link). Use when the user wants details about a specific paper.
argument-hint: "[PII or article URL]"
---

# ScienceDirect Paper Detail Extraction

Extract complete metadata from a ScienceDirect article page.

## Steps

### Step 1: Navigate to article

Determine the article URL from `$ARGUMENTS`:
- If a PII is given (e.g. `S0957417426005245`): URL is `{BASE_URL}/science/article/pii/{PII}`
- If a full URL is given: use that URL directly
- If a DOI is given: URL is `https://doi.org/{DOI}` (will redirect to ScienceDirect)

Use `navigate_page` with `initScript` to prevent bot detection:

```
navigate_page({
  url: "{article_url}",
  initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})
```

If the article is already open in the current tab, you can skip this and go directly to Step 3.

### Step 2: Check access

After navigation, verify:
- If the page shows "Are you a robot" or captcha: **auto-click the Cloudflare Turnstile checkbox** using the procedure below. If auto-click fails after 2 attempts, tell the user "请在浏览器中完成验证后告知我。"
- If the page URL no longer points to a ScienceDirect article, the user may need to log in. Tell the user: "页面被重定向，请在浏览器中完成登录或认证后告知我。" Then wait.

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

### Step 3: Extract metadata

Use `evaluate_script` with built-in waiting. Do NOT use `wait_for` — it returns oversized snapshots on article pages.

```javascript
async () => {
  // Wait for article content to load (up to 10s)
  for (let i = 0; i < 20; i++) {
    if (document.querySelector('.title-text') || document.querySelector('#abstracts')) break;
    await new Promise(r => setTimeout(r, 500));
  }

  const result = {};

  // Title
  result.title = document.querySelector('.title-text')?.textContent?.trim() || '';

  // Authors
  result.authors = [...document.querySelectorAll('.author-group .react-xocs-alternative-link')]
    .map(el => el.textContent.trim())
    .filter(Boolean);
  if (result.authors.length === 0) {
    result.authors = [...document.querySelectorAll('.author-group .button-link-text')]
      .map(el => el.textContent.trim().replace(/\s*\d+$/, ''))
      .filter(Boolean);
  }

  // Affiliations
  result.affiliations = [...document.querySelectorAll('.affiliation dd')]
    .map(el => el.textContent.trim()).filter(Boolean);

  // Abstract (content is in div, not p tags)
  const absDiv = document.querySelector('.abstract.author');
  if (absDiv) {
    const h2 = absDiv.querySelector('h2');
    const contentDiv = h2?.nextElementSibling;
    result.abstract = contentDiv?.textContent?.trim() || '';
  }
  if (!result.abstract) {
    // Fallback: try p tags inside #abstracts
    const absSection = document.querySelector('#abstracts, .Abstracts');
    if (absSection) {
      const absParagraphs = absSection.querySelectorAll('p');
      result.abstract = [...absParagraphs].map(p => p.textContent.trim()).join(' ');
    }
  }

  // Highlights
  const highlights = [...document.querySelectorAll('.author-highlights li')];
  if (highlights.length > 0) {
    result.highlights = highlights.map(li => li.textContent.trim());
  }

  // Keywords
  const kwSet = new Set();
  document.querySelectorAll('.keyword span').forEach(k => kwSet.add(k.textContent.trim()));
  result.keywords = [...kwSet];

  // DOI
  const doiLink = document.querySelector('a[href*="doi.org"]');
  result.doi = doiLink?.href || '';

  // Journal & volume info
  result.journal = document.querySelector('.publication-title-link')?.textContent?.trim() || '';
  const volText = document.querySelector('.publication-volume .text-xs, .publication-volume')?.textContent?.trim() || '';
  result.volumeInfo = volText;

  // PII
  result.pii = window.location.pathname.match(/pii\/(\w+)/)?.[1] || '';

  // Article type
  result.articleType = document.querySelector('.article-dochead')?.textContent?.trim() || '';

  // PDF link
  const pdfLink = document.querySelector('a[href*="pdfft"][class*="accessbar"]');
  result.pdfUrl = pdfLink?.href || '';

  // Publication dates
  const dateInfo = document.querySelector('.publication-history');
  result.dates = dateInfo?.textContent?.trim() || '';

  // References count
  result.referenceCount = document.querySelectorAll('.reference, .bibliography li').length;

  // Section headings (article structure)
  result.sections = [...document.querySelectorAll('.Body h2, .article-content h2')]
    .map(h => h.textContent.trim()).filter(Boolean);

  return result;
}
```

### Step 4: Present metadata

Format the output clearly:

```
## {title}

**Authors**: {authors}
**Journal**: {journal}, {volumeInfo}
**DOI**: {doi}
**Type**: {articleType}
**PII**: {pii}

### Abstract
{abstract}

### Highlights
- {highlight1}
- {highlight2}

### Keywords
{keywords}

### Article Structure
{sections}

**References**: {referenceCount} cited
**PDF**: {pdfUrl or "Not available"}
```

## Key CSS Selectors

| Element | Selector |
|---------|----------|
| Title | `.title-text` |
| Authors | `.author-group .react-xocs-alternative-link` |
| Affiliations | `.affiliation dd` |
| Abstract | `.abstract.author` (div after h2) |
| Highlights | `.author-highlights li` |
| Keywords | `.keyword span` |
| DOI link | `a[href*="doi.org"]` |
| Journal name | `.publication-title-link` |
| Volume/issue | `.publication-volume .text-xs` |
| PDF link | `a[href*="pdfft"][class*="accessbar"]` |
| References | `.reference, .bibliography li` |
| Section headings | `.Body h2, .article-content h2` |

## Notes

- PDF link format: `{BASE_URL}/science/article/pii/{PII}/pdfft?md5={hash}&pid=1-s2.0-{PII}-main.pdf`
- The PDF URL contains an `md5` hash that must be extracted from the page; it cannot be constructed.
- Always include `initScript` on every `navigate_page` call to prevent bot detection.
- This skill uses 2 tool calls: `navigate_page` + `evaluate_script`.
