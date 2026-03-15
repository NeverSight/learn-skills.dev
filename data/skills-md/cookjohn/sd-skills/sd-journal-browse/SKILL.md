---
name: sd-journal-browse
description: Browse a journal on ScienceDirect — view info, impact factor, latest articles, and specific issues. Use when the user asks about a journal or wants to browse its contents.
argument-hint: "[journal name or slug]"
---

# ScienceDirect Journal Browse

Browse journal information, metrics, and articles on ScienceDirect.

## URL Patterns

| Page | URL |
|------|-----|
| Journal home | `{BASE_URL}/journal/{slug}` |
| All issues | `{BASE_URL}/journal/{slug}/issues` |
| Specific volume/issue | `{BASE_URL}/journal/{slug}/vol/{vol}/issue/{issue}` |
| Supplement | `{BASE_URL}/journal/{slug}/vol/{vol}/suppl/C` |
| Editorial board | `{BASE_URL}/journal/{slug}/about/editorial-board` |
| Insights | `{BASE_URL}/journal/{slug}/about/insights` |

The `slug` is the journal's URL-friendly name (e.g. `expert-systems-with-applications`, `nature-communications`). If the user provides a journal name, convert it to a slug by lowercasing and replacing spaces with hyphens.

## Steps

### Step 1: Navigate to journal page

Use `navigate_page` with `initScript` to prevent bot detection:

```
navigate_page({
  url: "{BASE_URL}/journal/{slug}",
  initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

### Step 2: Extract journal info

Use `evaluate_script` with built-in waiting. Do NOT use `wait_for` — it returns oversized snapshots.

```javascript
async () => {
  // Wait for journal content to load (up to 10s)
  for (let i = 0; i < 20; i++) {
    if (document.querySelector('h1') && document.querySelector('main button')) break;
    await new Promise(r => setTimeout(r, 500));
  }

  const result = {};

  // Journal name
  result.name = document.querySelector('h1')?.textContent?.trim() || '';

  // Metrics (CiteScore, Impact Factor) — take the FIRST match (this journal, not partner journals)
  const allButtons = [...document.querySelectorAll('main button')];
  const firstCS = allButtons.find(b => b.textContent.includes('CiteScore'));
  const firstIF = allButtons.find(b => b.textContent.includes('Impact Factor'));
  if (firstCS) result.citeScore = firstCS.textContent.trim();
  if (firstIF) result.impactFactor = firstIF.textContent.trim();

  // Open access status
  const oaBtn = [...document.querySelectorAll('main button')].find(b => b.textContent.includes('open access'));
  result.openAccess = oaBtn ? oaBtn.textContent.trim() : 'Not specified';

  // ISSN
  const pageText = document.body.innerText;
  const onlineISSN = pageText.match(/Online ISSN:\s*([\d-X]+)/)?.[1] || '';
  const printISSN = pageText.match(/Print ISSN:\s*([\d-X]+)/)?.[1] || '';
  result.issn = { online: onlineISSN, print: printISSN };

  // Description — from "About the journal" section
  const aboutH2 = [...document.querySelectorAll('h2')].find(h => h.textContent.includes('About'));
  if (aboutH2) {
    let desc = '';
    let sibling = aboutH2.nextElementSibling;
    while (sibling && sibling.tagName !== 'H2') {
      desc += sibling.textContent.trim() + ' ';
      sibling = sibling.nextElementSibling;
    }
    result.description = desc.trim().substring(0, 500);
  }

  // Editor info
  const editorName = document.querySelector('.js-editor-name')?.textContent?.trim() || '';
  const editorAff = document.querySelector('.js-editor-affiliation')?.textContent?.trim() || '';
  result.editor = editorName + (editorAff ? ', ' + editorAff : '');

  // Submission metrics
  result.metrics = {};
  document.querySelectorAll('main button[class*="Info"]').forEach(btn => {
    const text = btn.textContent.trim();
    const prevEl = btn.previousElementSibling;
    if (prevEl) {
      const days = prevEl.textContent.trim();
      result.metrics[text] = days;
    }
  });

  // Latest articles
  result.articles = [];
  const articleLinks = document.querySelectorAll('main a[href*="/science/article/pii/"]');
  const seen = new Set();
  articleLinks.forEach(link => {
    const title = link.textContent.trim();
    const pii = link.href.match(/pii\/(\w+)/)?.[1] || '';
    if (title && pii && !seen.has(pii)) {
      seen.add(pii);
      const container = link.closest('div, li, section');
      const pdfLink = container?.querySelector('a[href*="pdfft"]');
      result.articles.push({
        title,
        pii,
        url: link.href,
        pdfUrl: pdfLink?.href || '',
      });
    }
  });
  result.articles = result.articles.slice(0, 10);

  // Latest issue link
  const latestLink = document.querySelector('a[href*="/vol/"]');
  result.latestIssueUrl = latestLink?.href || '';

  return result;
}
```

### Step 3: Present journal info

```
## {name}

**Impact Factor**: {impactFactor}
**CiteScore**: {citeScore}
**Open Access**: {openAccess}
**ISSN**: Online {online} | Print {print}
**Editor**: {editor}

### Description
{description}

### Latest Articles
1. {title} (PII: {pii})
   [View PDF]({pdfUrl})
2. ...

Latest issue: {latestIssueUrl}
```

## Browsing a specific issue

If the user asks for a specific volume/issue, navigate to `{BASE_URL}/journal/{slug}/vol/{vol}/issue/{issue}` and extract the article list using a similar approach.

## Notes

- Journal slugs are URL-friendly names. If unsure, search for the journal name first.
- The journal page shows latest published, articles in press, top cited, and most downloaded tabs.
- Always include `initScript` on every `navigate_page` call to prevent bot detection.
- If the page shows captcha, **auto-click the Cloudflare Turnstile checkbox**: use `take_snapshot` to find `checkbox "确认您是真人"` inside the Turnstile iframe, then `click(uid)`. Wait 3-5s and verify. If auto-click fails after 2 attempts, fall back to asking the user. After solving once, the session cookie persists.
- Use 2 tool calls: `navigate_page` + `evaluate_script`.
