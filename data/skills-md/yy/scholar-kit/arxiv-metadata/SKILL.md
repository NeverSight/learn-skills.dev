---
name: arxiv-metadata
user_invocable: true
description: Fetch structured metadata for an arXiv paper. Use when you have an arXiv ID or URL and need title, authors, date, categories, and DOI.
---

# arXiv Metadata

## Fetch metadata

```bash
./scripts/arxiv_metadata.py <arXiv-ID-or-URL>
```

> Paths are relative to this skill's directory.

Accepts bare IDs (`2301.10140`), old-style IDs (`hep-ph/9901234`), or full URLs (`https://arxiv.org/abs/2301.10140`).

## Output

Returns JSON:

```json
{
  "arxiv_id": "2301.10140",
  "title": "Paper title",
  "authors": ["Author One", "Author Two"],
  "published": "2023-01-24",
  "primary_category": "cs.CL",
  "categories": ["cs.CL", "cs.AI"],
  "doi": "10.1234/..." or null,
  "url": "https://arxiv.org/abs/2301.10140"
}
```

- `url` prefers the DOI link (`https://doi.org/...`) when a published DOI exists, otherwise uses the arXiv abstract page.
- `published` is the original arXiv submission date (YYYY-MM-DD).
