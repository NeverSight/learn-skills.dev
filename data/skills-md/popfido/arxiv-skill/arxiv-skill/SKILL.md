---
name: arxiv-skill
description: Search arXiv, cache papers locally as markdown, inspect cached papers, and perform structured paper analysis. Use when the task involves finding arXiv papers, downloading a paper by ID, reading cached markdown, or doing literature review and deep paper analysis.
license: Apache-2.0
compatibility: Requires Python 3.11+, uv, internet access for arXiv search/download, and local filesystem write access for cached papers.
---

# arXiv Research Workflow

Use this skill when work revolves around arXiv discovery, local paper caching, or structured analysis of research papers.

## Quick workflow

1. Search for candidate papers with `scripts/search_arxiv.py`.
2. Cache any paper that needs full-text analysis with `scripts/cache_paper.py`.
3. Inspect the local cache with `scripts/list_cached_papers.py`.
4. Read cached markdown with `scripts/read_cached_paper.py`.
5. Structure the final write-up with [references/analysis-framework.md](references/analysis-framework.md).

## Scripts

- `scripts/search_arxiv.py`
  Search arXiv with query, category, and date filters.
- `scripts/cache_paper.py`
  Download a paper by arXiv ID, convert the PDF to markdown, and cache it locally.
- `scripts/list_cached_papers.py`
  List cached papers, with optional metadata lookup from arXiv.
- `scripts/read_cached_paper.py`
  Read cached markdown as raw text or JSON.

## When to read references

- Query design and fielded search patterns:
  [references/search-syntax.md](references/search-syntax.md)
- Cache layout, storage path rules, and file behavior:
  [references/storage-format.md](references/storage-format.md)
- End-to-end examples:
  [references/workflow.md](references/workflow.md)
- Paper-analysis rubric and output structure:
  [references/analysis-framework.md](references/analysis-framework.md)

## Execution notes

- Prefer JSON output from the scripts unless the task specifically needs raw markdown.
- Cache files default to `.cache/arxiv-skill/papers` inside the repository.
- Override cache location with `--storage-path` or `ARXIV_SKILL_STORAGE_PATH`.
- Delete PDFs after conversion unless the task requires preserving them; use `--keep-pdf` when needed.
