---
name: web-scraping
description: Extract structured information from websites using web_fetch for simple pages and browser automation for dynamic sites, login-gated flows, pagination, infinite scroll, or pages that require clicking/searching/filtering. Use when the user asks to scrape a site, collect listings, gather fields from many pages, monitor website changes, or turn webpage content into structured summaries/JSON/CSV.
---

# Web Scraping

Extract data with the lightest reliable method first.

## Choose the approach

1. Use `web_fetch` for simple public pages when the needed content is already in HTML.
2. Use `browser` when the site is dynamic, needs clicking, infinite scroll, filters, tabs, or login/session state.
3. Use `web_search` only to discover candidate pages when the target URL is unknown.

## Default workflow

1. Identify the target site and exact fields to collect.
2. Test one page first.
3. Decide the extraction method:
   - `web_fetch` for readable article/listing text
   - `browser snapshot` for dynamic DOM inspection
4. Normalize the output into a stable schema.
5. If scraping multiple pages, avoid tight loops and serialize requests.
6. Deduplicate by URL or stable item id.
7. Save results in the workspace when the task is larger than a quick one-off.

## Browser scraping pattern

1. Open the page.
2. Take a snapshot.
3. Interact only as needed: search, click filters, pagination, expand sections.
4. Re-snapshot after each meaningful state change.
5. Extract only the fields the user asked for.
6. Close tabs when finished.

## Output guidance

Prefer one of these formats:
- concise bullet summary
- JSON array of objects
- CSV/TSV when the user wants exportable rows

Use explicit keys, for example:

```json
[
  {
    "title": "...",
    "url": "...",
    "source": "...",
    "date": "...",
    "summary": "..."
  }
]
```

## Reliability rules

- Do not invent missing fields.
- If a site blocks access, say so and switch sources when appropriate.
- For news/results pages, capture source + title + link at minimum.
- For large jobs, checkpoint partial results to a workspace file.
- Prefer fewer larger writes over many tiny writes.

## Cleanup

- Close browser tabs opened for scraping.
- If you create state/output files, store them under the workspace and name them clearly.
