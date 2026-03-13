---
name: wos-paper-detail
description: Get detailed information for a paper by WoS ID (e.g., WOS:000779183600001).
argument-hint: "[WoS ID or full-record URL]"
user-invocable: true
disable-model-invocation: false
---

# WoS Paper Detail

Navigate to a WoS full record page and extract comprehensive paper metadata.

## Steps

### Step 1: Parse Input

Accept either:
- WoS Accession Number: `WOS:000779183600001`
- Full URL: `https://www.webofscience.com/wos/woscc/full-record/WOS:000779183600001`

Extract the WoS ID if a full URL is provided.

### Step 2: Navigate

```
navigate_page({
  url: "{BASE_URL}/wos/woscc/full-record/{WOS_ID}",
  initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})
```

### Step 3: Extract Full Record Data

```javascript
async () => {
  // Wait for full record to load
  for (let i = 0; i < 30; i++) {
    if (document.querySelector('[data-ta="FullRTa-fullRecordtitle-0"]')) break;
    await new Promise(r => setTimeout(r, 500));
  }
  await new Promise(r => setTimeout(r, 1500));

  // Check access
  if (document.body.innerText.includes('Sign in') && !document.querySelector('[data-ta="FullRTa-fullRecordtitle-0"]')) {
    return { status: 'login_required' };
  }

  // Helper: get value for a labeled field (h3 label -> parent's non-h3 children)
  const getField = (label) => {
    const h3 = [...document.querySelectorAll('h3')].find(h => h.textContent.trim() === label);
    if (!h3) return '';
    const parent = h3.parentElement;
    const valueEls = [...parent.children].filter(el => el.tagName !== 'H3');
    return valueEls.map(s => s.textContent?.trim()).join(' ').substring(0, 300) || '';
  };

  // Title
  const title = document.querySelector('[data-ta="FullRTa-fullRecordtitle-0"]')?.textContent?.trim() || '';

  // Authors
  const authors = [...document.querySelectorAll('[data-ta^="SumAuthTa-DisplayName-author-en"]')]
    .map(a => a.textContent?.trim());

  // Abstract
  const abstract = document.querySelector('div.abstract--instance')?.textContent?.trim() || '';

  // Source/Journal - extract only journal name from the JCR sidenav component
  let source = '';
  const sourceSpan = document.querySelector('h3[data-ta="FullRTa-sourceLabel"]')?.parentElement?.querySelector('span.section-label-data');
  if (sourceSpan) {
    // The span contains app-jcr-sidenav with journal name + popup. Get first text content before "arrow_back"
    const fullText = sourceSpan.textContent?.trim() || '';
    source = fullText.split('arrow_back')[0].trim();
  }
  if (!source) {
    source = document.querySelector('.summary-source-title-link')?.firstChild?.textContent?.trim() || '';
  }

  // DOI - try link first, fall back to h3 label extraction
  const doiEl = document.querySelector('a[href*="doi.org"]');
  const doi = doiEl?.textContent?.trim() || doiEl?.href?.replace(/.*doi\.org\//, '') || getField('DOI');

  // Metadata fields
  const volume = getField('Volume');
  const issue = getField('Issue');
  const pages = getField('Page');
  const published = getField('Published');
  const earlyAccess = getField('Early Access');
  const docType = getField('Document Type');
  const language = getField('Language');
  const accessionNumber = getField('Accession Number');
  const issn = getField('ISSN');
  const eissn = getField('eISSN');

  // Keywords - use parentElement.querySelectorAll('a') to get ALL keyword links
  const getKeywords = (label) => {
    const h3 = [...document.querySelectorAll('h3')].find(h => h.textContent.trim() === label);
    if (!h3) return [];
    return [...h3.parentElement.querySelectorAll('a')].map(a => a.textContent?.trim()).filter(Boolean);
  };
  const authorKeywords = getKeywords('Author Keywords');
  const keywordsPlus = getKeywords('Keywords Plus');

  // Categories
  const researchAreas = getField('Research Areas');
  const wosCategories = getField('Web of Science Categories');

  // Citations - full record page uses FullRRPTa selectors, NOT stat-number selectors
  const citedLinks = [...document.querySelectorAll('a[data-ta*="times-cited-count-link"]')];
  // WOSCC link text is "992 In Web of Science Core Collection" - extract leading number
  const extractNum = (text) => (text?.match(/^[\d,]+/) || ['0'])[0];
  const wosccCited = extractNum(citedLinks.find(a => a.getAttribute('data-ta')?.includes('-WOSCC'))?.textContent?.trim());
  const alldbCited = extractNum(citedLinks.find(a => a.getAttribute('data-ta')?.includes('-ALLDB'))?.textContent?.trim());
  const mainCited = extractNum(citedLinks.find(a => /^\d/.test(a.textContent?.trim()))?.textContent?.trim());
  const citedCount = wosccCited || mainCited || '0';

  // References
  const refsCount = document.querySelector('a[data-ta*="refCountLink"]')?.textContent?.trim() || '0';

  // JIF - extract from JCR popup/sidenav text content
  let jif = '', jifYear = '', jifFiveYear = '', jcrQuartile = '';
  const jcrPopup = document.querySelector('[class*="journal-content"], app-jcr-sidenav');
  if (jcrPopup) {
    const jcrText = jcrPopup.textContent || '';
    // Pattern: "Journal Impact Factor ™20242.8Five Year3.4"
    const jifMatch = jcrText.match(/Impact Factor\s*(?:™|TM)?\s*(\d{4})\s*([\d.]+)/);
    if (jifMatch) { jifYear = jifMatch[1]; jif = jifMatch[2]; }
    const fyMatch = jcrText.match(/Five Year\s*([\d.]+)/);
    if (fyMatch) jifFiveYear = fyMatch[1];
    // Quartile: "159/316 Q3" pattern in JCR summary
    const qMatch = jcrText.match(/\d+\/\d+\s*(Q[1-4])/);
    if (qMatch) jcrQuartile = qMatch[1];
  }

  // Full text links
  const ftLinks = [...document.querySelectorAll('a[data-ta^="FRLinkTa"]')].map(a => ({
    text: a.textContent?.trim()?.replace(/open_in_new/g, '').trim(),
    href: a.href
  })).filter(l => l.text);

  return {
    status: 'ok',
    title, authors, abstract, source, doi,
    volume, issue, pages, published, earlyAccess,
    docType, language, accessionNumber, issn, eissn,
    authorKeywords, keywordsPlus,
    researchAreas, wosCategories,
    citedCount, alldbCited, refsCount,
    jif, jifYear, jifFiveYear, jcrQuartile,
    ftLinks
  };
}
```

### Step 4: Present Results

Format the output as a structured summary:

```
## {Title}

**Authors**: {authors joined by "; "}
**Source**: {source}, Vol. {volume}, Iss. {issue}, pp. {pages}
**Published**: {published}
**DOI**: {doi}
**Document Type**: {docType}
**WoS ID**: {accessionNumber}

### Abstract
{abstract}

### Keywords
- **Author Keywords**: {authorKeywords}
- **Keywords Plus**: {keywordsPlus}

### Metrics
- **Times Cited (WOSCC)**: {citedCount}
- **Times Cited (All DB)**: {alldbCited}
- **References**: {refsCount}
- **JIF ({jifYear})**: {jif} (Five Year: {jifFiveYear})
- **JCR Quartile**: {jcrQuartile}

### Classification
- **Research Areas**: {researchAreas}
- **WoS Categories**: {wosCategories}
- **ISSN**: {issn} | **eISSN**: {eissn}

### Full Text Links
{list of ftLinks}
```

Offer next actions:
- "Use `/wos-export {WoS ID}` to export this paper"
- "Use `/wos-download {WoS ID}` to download PDF"

## Key CSS Selectors (Full Record Page)

| Element | Selector | Notes |
|---------|----------|-------|
| Title | `[data-ta="FullRTa-fullRecordtitle-0"]` | |
| Authors | `[data-ta^="SumAuthTa-DisplayName-author-en"]` | |
| Abstract | `div.abstract--instance` | |
| Source label | `h3[data-ta="FullRTa-sourceLabel"]` | Parent span has JCR popup; split on "arrow_back" |
| DOI | `a[href*="doi.org"]` | |
| Author Keywords | `h3#FRkeywordsTa-authorKeywordsLabel` → parent `a` tags | Use `parentElement.querySelectorAll('a')` |
| Keywords Plus | Same pattern with "Keywords Plus" label | |
| Citations (WOSCC) | `a[data-ta*="times-cited-count-link-WOSCC"]` | Full record page only |
| Citations (All DB) | `a[data-ta*="times-cited-count-link-ALLDB"]` | Full record page only |
| References | `a[data-ta*="refCountLink"]` | Full record page only |
| Metadata fields | h3 label → `parentElement` → non-h3 children | Volume, Issue, Page, Published, etc. |
| JIF | Inside `app-jcr-sidenav` text content | Regex: `/Impact Factor\s*™?\s*(\d{4})\s*([\d.]+)/` |
| Full text links | `a[data-ta^="FRLinkTa"]` | |

## Notes

- This skill uses 2 tool calls: `navigate_page` + `evaluate_script`
- **IMPORTANT**: Full record page uses different citation selectors than search results page:
  - Search results: `a[data-ta="stat-number-citation-related-count"]`
  - Full record: `a[data-ta*="times-cited-count-link-WOSCC"]`
- Source extraction must split on "arrow_back" to avoid capturing JCR popup content
- Keywords must use `parentElement.querySelectorAll('a')`, NOT `nextElementSibling`
- JIF is embedded in JCR sidenav popup text, not in a standalone element
