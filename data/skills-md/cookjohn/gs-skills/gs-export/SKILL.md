---
name: gs-export
description: Export Google Scholar paper(s) to Zotero via BibTeX. Gets citation data from Google Scholar's cite dialog, then pushes to Zotero desktop. Supports single or batch export.
argument-hint: "[data-cid or space-separated data-cids]"
---

# Google Scholar Export to Zotero

Export Google Scholar paper citation data via BibTeX extraction and push to Zotero desktop.

## Arguments

$ARGUMENTS contains one or more data-cids (space-separated), e.g.:
- `TFS2GgoGiNUJ` — single paper
- `TFS2GgoGiNUJ abc123XYZ def456UVW` — batch export

## Steps

### Step 1: Get BibTeX for each paper

For each data-cid, perform 3 tool calls to bypass CORS:

#### 1a. Fetch cite dialog to get BibTeX link (evaluate_script)

```javascript
async () => {
  const cid = "DATA_CID_HERE";
  const resp = await fetch(
    `https://scholar.google.com/scholar?q=info:${cid}:scholar.google.com/&output=cite`,
    { credentials: 'include' }
  );
  const html = await resp.text();
  const doc = new DOMParser().parseFromString(html, 'text/html');

  // Extract export links
  const links = Array.from(doc.querySelectorAll('#gs_citi a')).map(a => ({
    format: a.textContent.trim(),
    url: a.href
  }));

  // Extract citation format texts
  const citations = Array.from(doc.querySelectorAll('#gs_citt tr')).map(tr => {
    const cells = tr.querySelectorAll('td');
    return {
      style: cells[0]?.textContent?.trim() || '',
      text: cells[1]?.textContent?.trim() || ''
    };
  });

  const bibtexLink = links.find(l => l.format === 'BibTeX');
  return { cid, bibtexLink: bibtexLink?.url || '', links, citations };
}
```

#### 1b. Navigate to BibTeX URL (navigate_page)

Use `mcp__chrome-devtools__navigate_page`:
- url: the `bibtexLink` URL from step 1a (on `scholar.googleusercontent.com`)

This bypasses CORS restrictions that block fetch() to googleusercontent.com.

#### 1c. Read BibTeX content (evaluate_script)

```javascript
async () => {
  return { bibtex: document.body.innerText || document.body.textContent || '' };
}
```

### Step 2: Parse BibTeX and push to Zotero

Save the BibTeX data as JSON, then call the push script:

```bash
python "E:/gscholar-skills/.claude/skills/gs-export/scripts/push_to_zotero.py" /tmp/gs_papers.json
```

Before calling the script, construct a JSON file at `/tmp/gs_papers.json` containing paper data parsed from BibTeX. Parse the BibTeX yourself and create the JSON array:

```json
[
  {
    "pmid": "",
    "title": "The title from BibTeX",
    "authors": [
      {"lastName": "Smith", "firstName": "John"}
    ],
    "journal": "Journal Name",
    "journalAbbr": "",
    "pubdate": "2022",
    "volume": "14",
    "issue": "4",
    "pages": "1054",
    "doi": "",
    "pdfUrl": "https://example.com/paper.pdf",
    "abstract": "",
    "keywords": [],
    "language": "en",
    "pubtype": ["Journal Article"]
  }
]
```

**IMPORTANT**: Set `pdfUrl` from the search result's `fullTextUrl` field (the PDF link extracted by gs-search). The Python script will download the PDF and upload it to Zotero via `/connector/saveAttachment` (Zotero 7.x ignores attachments in saveItems). PDF download may fail for some publishers (403, JS-redirect); these are reported as "PDF skip".

BibTeX fields mapping:
- `@article{key,` → `itemType: journalArticle`
- `@inproceedings{key,` → `itemType: conferencePaper`
- `@book{key,` → `itemType: book`
- `title={...}` → `title`
- `author={Last1, First1 and Last2, First2}` → `authors` array
- `journal={...}` → `journal`
- `year={...}` → `pubdate`
- `volume={...}` → `volume`
- `number={...}` → `issue`
- `pages={...}` → `pages`
- `publisher={...}` → (included in extra or publisher field)

### Step 3: Report

Single paper:
```
Exported to Zotero from Google Scholar:
  Title: {title}
  Authors: {authors}
  Journal: {journal} ({year})
  Data-CID: {dataCid}
```

Batch:
```
Exported {count} papers to Zotero from Google Scholar:
  1. {title1} ({journal1}, {year1})
  2. {title2} ({journal2}, {year2})
  ...
```

## Batch Export Optimization

For multiple papers, process sequentially to avoid CAPTCHA:
1. Get all BibTeX links in one evaluate_script call (fetch all cite dialogs)
2. Navigate to each BibTeX URL one at a time
3. Collect all BibTeX entries
4. Push all to Zotero in a single batch

## Notes

- Single paper export uses 3-4 tool calls: `evaluate_script` (cite dialog) + `navigate_page` (BibTeX URL) + `evaluate_script` (read BibTeX) + `bash python` (Zotero push)
- Batch export: 2N+1 tool calls (N papers: N navigate + N evaluate + 1 bash)
- BibTeX links are on `scholar.googleusercontent.com` — CORS blocks fetch(), so we use navigate_page to bypass
- Reuses `push_to_zotero.py` for Zotero Connector API communication
- Google Scholar BibTeX does NOT include abstract or DOI — these fields will be empty in Zotero
- After export, navigate back to Google Scholar page: `navigate_page` with type `back`
