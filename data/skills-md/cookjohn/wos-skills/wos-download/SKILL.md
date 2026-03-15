---
name: wos-download
description: Download PDF full text for a WoS paper via publisher links.
argument-hint: "[WoS ID or DOI]"
user-invocable: true
disable-model-invocation: true
---

# WoS Download

Download PDF full text for a paper from Web of Science.

## Important Limitations

- **PDF access depends on institutional subscription**. Even Open Access papers may require authentication on the publisher site.
- **Cross-origin download**: The `a.download` trick only works when the browser is on the same-origin page displaying the PDF. It does NOT work for cross-origin redirects (e.g., WoS → Wiley).
- **Publisher login walls**: Wiley, Elsevier, Springer, etc. may redirect to a login page even for OA papers when accessed without institutional proxy.

## Steps

### Step 1: Navigate to Full Record

If not already on the full record page:

```
navigate_page({
  url: "{BASE_URL}/wos/woscc/full-record/{WOS_ID}",
  initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})
```

### Step 2: Find Full Text Links

```javascript
async () => {
  for (let i = 0; i < 20; i++) {
    if (document.querySelector('[data-ta="FullRTa-fullRecordtitle-0"]')) break;
    await new Promise(r => setTimeout(r, 500));
  }
  await new Promise(r => setTimeout(r, 1000));

  const title = document.querySelector('[data-ta="FullRTa-fullRecordtitle-0"]')?.textContent?.trim() || '';

  const links = [...document.querySelectorAll('a[data-ta^="FRLinkTa"]')].map(a => ({
    text: a.textContent?.trim()?.replace(/open_in_new/g, '').trim(),
    href: a.href,
    dataTa: a.getAttribute('data-ta')
  }));

  const doiEl = document.querySelector('a[href*="doi.org"]');
  const doi = doiEl?.href || '';

  return { title, links, doi };
}
```

### Step 3: Follow Full Text Link

Navigate to the publisher link:

```
navigate_page({
  url: "{CHOSEN_LINK}",
  initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})
```

### Step 4: Check PDF Status & Attempt Download

```javascript
async () => {
  await new Promise(r => setTimeout(r, 5000));

  const url = window.location.href;
  const contentType = document.contentType;

  // Direct PDF — trigger download immediately
  if (contentType === 'application/pdf') {
    const a = document.createElement('a');
    a.href = url;
    a.download = '{FILENAME}';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    return { status: 'downloaded', url };
  }

  // Publisher HTML page — look for PDF links
  const pdfLinks = [...document.querySelectorAll('a')].filter(a => {
    const href = a.href || '';
    const text = a.textContent || '';
    return href.includes('/pdf/') || href.includes('.pdf') ||
           text.toLowerCase().includes('download pdf') || text.toLowerCase() === 'pdf';
  }).map(a => ({
    text: a.textContent?.trim()?.substring(0, 50),
    href: a.href?.substring(0, 120)
  }));

  // Check for access denial
  const bodyText = document.body.innerText?.substring(0, 1000) || '';
  const loginRequired = bodyText.includes('Sign in') || bodyText.includes('Log in') ||
                         bodyText.includes('Individual login') || bodyText.includes('Institutional login');
  const paywall = bodyText.includes('Purchase') || bodyText.includes('Subscribe') ||
                  bodyText.includes('Access Denied');

  return {
    status: loginRequired ? 'login_required' : paywall ? 'paywall' : pdfLinks.length > 0 ? 'pdf_links_found' : 'publisher_page',
    url: url.substring(0, 100),
    pdfLinks: pdfLinks.slice(0, 5),
    pageTitle: document.title
  };
}
```

### Step 5: Handle Result

| Status | Action |
|--------|--------|
| `downloaded` | Report success, file saved to default download folder |
| `pdf_links_found` | Click the "Download PDF" link on the publisher page |
| `login_required` | Inform user: "Publisher requires login. Try accessing via institutional VPN/WebVPN or download manually." |
| `paywall` | Inform user: "This paper requires a subscription." |
| `publisher_page` | Inform user: "On publisher page but no direct PDF link found." |

### Clicking Publisher's Download PDF Button

If `pdf_links_found`, use `take_snapshot` to find the Download PDF button, then `click` it:

```
1. take_snapshot → find "Download PDF" link uid
2. click(uid)
3. evaluate_script → wait 5s, check if PDF loaded (contentType === 'application/pdf')
4. If PDF loaded → trigger download with a.download
```

## Filename Convention

`{FirstAuthor}_{Year}_{ShortTitle}.pdf`

Example: `Johnson_2025_Citizen-Centric_AI_Government.pdf`

## Known Issues

- **WoS gateway links** (`/api/gateway?...DestURL=...`) redirect through GetFTR to publisher. The final destination depends on institutional access.
- **Wiley**: Even OA papers show login page without institutional cookie. The ePDF viewer (`/doi/epdf/...`) is an iframe-based reader, not a downloadable PDF.
- **Elsevier/ScienceDirect**: May serve PDF directly if institution has access, otherwise shows abstract page.
- **After download attempt, SID is lost**: Navigating to an external publisher site clears WoS performance entries. When returning to WoS, use URL-based search or navigate to any WoS page first to re-establish SID.

## Notes

- This skill uses 3-4 tool calls: navigate to record + extract links + navigate to publisher + download
- PDF access depends on institutional subscriptions
- Always use `initScript` on every navigation
- If download fails, suggest user try via institutional VPN or manual browser download
