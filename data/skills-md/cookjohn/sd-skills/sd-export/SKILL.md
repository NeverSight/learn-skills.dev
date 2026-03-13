---
name: sd-export
description: Export citations from ScienceDirect in RIS, BibTeX, or plain text format. Supports pushing to Zotero.
argument-hint: "[PII(s)] [format: ris|bibtex|text] [zotero]"
---

# ScienceDirect Citation Export

Export article citations from ScienceDirect search results. Supports RIS, BibTeX, plain text, and Zotero push.

## Export API

ScienceDirect uses a POST endpoint for citation export:

```
{BASE_URL}/search/api/export-citations
```

**Parameters** (form POST):
| Field | Description |
|-------|-------------|
| `pii` | Article PII (e.g. `S0957417426005245`). Multiple PIIs for batch. |
| `type` | Export format: `ris`, `bibtex`, `text` |
| `t` | Security token (must be extracted from the page) |

## Single Article Export

### Step 1: Ensure on search results page

The export API requires a token that exists only on search results pages. If you have a PII but are not on a search results page, first search for the article or navigate back to results.

**Note**: When navigating to search results, always include `initScript` to prevent bot detection:
```
initScript: "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
```

### Step 2: Click the article's Export button and extract token

Use `evaluate_script`:

```javascript
(pii) => {
  // Find the result item with this PII
  const checkbox = document.getElementById(pii);
  const resultItem = checkbox?.closest('li.ResultItem');
  if (!resultItem) return { error: 'Article with PII ' + pii + ' not found on this page.' };

  // Click the Export button for this result
  const exportBtn = resultItem.querySelector('button[aria-label="Export"]');
  if (exportBtn) exportBtn.click();

  // Wait briefly for the export panel to appear, then extract token
  return new Promise(resolve => {
    setTimeout(() => {
      const form = resultItem.querySelector('.ExportCitationOptions form');
      if (!form) { resolve({ error: 'Export panel did not open.' }); return; }

      const token = form.querySelector('input[name="t"]')?.value || '';
      const formAction = form.action;

      resolve({ token, formAction, pii });
    }, 500);
  });
}
```

### Step 3: Submit export request

Use `evaluate_script` to submit the form with the desired format:

```javascript
(token, pii, format) => {
  // format: 'ris', 'bibtex', or 'text'
  const typeMap = {
    'ris': 'ris',
    'bibtex': 'bibtex',
    'text': 'text',
  };

  const form = document.createElement('form');
  form.method = 'POST';
  form.action = window.location.origin + '/search/api/export-citations';
  form.target = '_blank';

  const fields = { type: typeMap[format] || 'ris', t: token, pii: pii };
  for (const [name, value] of Object.entries(fields)) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    form.appendChild(input);
  }

  document.body.appendChild(form);
  form.submit();
  document.body.removeChild(form);

  return { success: true, format: format, pii: pii };
}
```

## Batch Export

### Step 1: On search results page, click the top Export button

Use `evaluate_script` to select multiple articles and trigger batch export:

```javascript
(piis) => {
  // Select all specified articles
  piis.forEach(pii => {
    const cb = document.getElementById(pii);
    if (cb && !cb.checked) cb.click();
  });

  // Click the batch export button
  const exportBtn = document.querySelector('.export-all-link-button');
  if (exportBtn) exportBtn.click();

  return { success: true, selected: piis.length };
}
```

Then wait for the export dropdown to appear and select the desired format.

## Zotero Push

To push citations to a locally running Zotero instance. Two modes are supported:

**Prerequisites**: Zotero desktop must be running with the Connector API enabled (default on port 23119).

### Mode 1: RIS import (simple, no PDF)

Use when you have RIS data from the export API or constructed from metadata.

```bash
python {SKILL_DIR}/scripts/push_to_zotero.py --ris-file "{RIS_FILE_PATH}"
```

Or push RIS content directly:

```bash
python {SKILL_DIR}/scripts/push_to_zotero.py --ris-data "{RIS_CONTENT}"
```

The script uses a **deterministic session ID** (MD5 hash of content) so:
- First call → 201 (saved successfully)
- Repeat call → 409 → treated as success ("already saved, no duplicates")

This avoids the `SESSION_EXISTS` error that occurs with random session IDs, since Zotero's session cleanup is buggy and sessions persist until restart.

### Mode 2: JSON import (structured data with optional PDF attachment)

Use when you have structured paper data (e.g., from `sd-paper-detail`) and want to attach PDFs.

Save paper data as a JSON file, then run:

```bash
python {SKILL_DIR}/scripts/push_to_zotero.py --json "{JSON_FILE_PATH}"
```

**JSON format** (single paper or array):

```json
{
  "title": "Paper Title",
  "authors": ["Author One", "Author Two"],
  "journal": "Journal Name",
  "date": "2026",
  "doi": "10.1016/...",
  "volume": "76",
  "issue": "3",
  "pages": "109460",
  "abstract": "...",
  "keywords": ["keyword1", "keyword2"],
  "url": "https://www.sciencedirect.com/science/article/pii/{PII}",
  "pdfUrl": "https://www.sciencedirect.com/..../pdfft?md5=...&pid=...",
  "cookies": "cf_clearance=...; JSESSIONID=..."
}
```

When `pdfUrl` and `cookies` are provided, the script will:
1. Save metadata via `/connector/saveItems`
2. Download PDF using the browser cookies
3. Upload PDF as attachment via `/connector/saveAttachment`

### Listing Zotero collections

```bash
python {SKILL_DIR}/scripts/push_to_zotero.py --list
```

## Export Format Buttons on Page

Each result item has these export option buttons (inside `.export-options`):

| Button text | data-aa-button attribute | Format |
|-------------|--------------------------|--------|
| Save to RefWorks | `srp-export-single-refworks` | RefWorks |
| Export citation to RIS | `srp-export-single-ris` | RIS |
| Export citation to BibTeX | `srp-export-single-bibtex` | BibTeX |
| Export citation to text | `srp-export-single-text` | Plain text |

## Notes

- **Authentication required**: Export buttons, result checkboxes, and the batch action toolbar are only visible to authenticated users. The user must be logged in (institutional or personal account) for export to work.
- The security token `t` is session-specific and page-specific. It must be extracted from the export form on the page.
- Batch export is much more efficient than exporting one-by-one.
- For Zotero push, ensure Zotero desktop is running before invoking.
- If the page shows captcha during export, **auto-click the Cloudflare Turnstile checkbox**: use `take_snapshot` to find `checkbox "确认您是真人"` inside the Turnstile iframe, then `click(uid)`. Wait 3-5s and verify. If auto-click fails after 2 attempts, fall back to asking the user. After solving once, the session cookie persists.
