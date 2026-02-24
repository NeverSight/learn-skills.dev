---
name: literature-search
description: Search academic literature using Semantic Scholar, arXiv, and OpenAlex APIs. Returns structured JSONL with title, authors, year, venue, abstract, citations, and BibTeX. Use when the user needs to find papers, check related work, or build a bibliography.
argument-hint: [search-query]
---

# Literature Search

Search multiple academic databases to find relevant papers.

## Input

- `$ARGUMENTS` — The search query (natural language)

## Scripts

### Semantic Scholar (primary — best for ML/AI, has BibTeX)
```bash
python ~/.claude/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "QUERY" --max-results 20 --year-range 2022-2026 \
  --api-key "$(grep S2_API_Key /Users/lingzhi/Code/keys.md 2>/dev/null | cut -d: -f2 | tr -d ' ')" \
  -o results_s2.jsonl
```

Key flags: `--peer-reviewed-only`, `--top-conferences`, `--min-citations N`, `--venue NeurIPS ICML`

### arXiv (latest preprints)
```bash
python ~/.claude/skills/deep-research/scripts/search_arxiv.py \
  --query "QUERY" --max-results 10 -o results_arxiv.jsonl
```

### OpenAlex (broadest coverage, free, no API key)
```bash
python ~/.claude/skills/literature-search/scripts/search_openalex.py \
  --query "QUERY" --max-results 20 --year-range 2022-2026 \
  --min-citations 5 -o results_openalex.jsonl
```

### Merge & Deduplicate
```bash
python ~/.claude/skills/deep-research/scripts/paper_db.py merge \
  --inputs results_s2.jsonl results_arxiv.jsonl results_openalex.jsonl \
  --output merged.jsonl
```

### CrossRef (DOI-based lookup, broadest type coverage)
```bash
python ~/.claude/skills/literature-search/scripts/search_crossref.py \
  --query "QUERY" --rows 10 --output results_crossref.jsonl
```

Key flags: `--bibtex` (output .bib format), `--rows N`

### Download arXiv Source (get .tex files)
```bash
python ~/.claude/skills/literature-search/scripts/download_arxiv_source.py \
  --title "Paper Title" --output-dir arxiv_papers/
```

Key flags: `--arxiv-id 1706.03762`, `--metadata`, `--max-results N`

### Generate BibTeX from results
```bash
python ~/.claude/skills/deep-research/scripts/bibtex_manager.py \
  --jsonl merged.jsonl --output references.bib
```

## Workflow

1. Expand the user's query into 2-4 complementary search queries
2. Run Semantic Scholar search (primary) with expanded queries
3. Run arXiv for very recent preprints (< 3 months)
4. Optionally run OpenAlex for broader coverage
5. Merge and deduplicate results
6. Rank by: citations (0.3) + recency (0.3) + venue quality (0.2) + relevance (0.2)
7. Present structured results table

## Venue Quality Tiers

**Tier 1:** NeurIPS, ICML, ICLR, ACL, EMNLP, NAACL, CVPR, ICCV, ECCV, KDD, AAAI, IJCAI, SIGIR, WWW
**Tier 2:** AISTATS, UAI, COLT, COLING, EACL, WACV, JMLR, TACL
**Tier 3:** Workshops, arXiv preprints — mark with `(preprint)`

## Output Format

Present results as a table + detailed entries with BibTeX keys. Always note preprint status.

## Related Skills
- Downstream: [citation-management](../citation-management/), [literature-review](../literature-review/), [related-work-writing](../related-work-writing/)
- See also: [deep-research](../deep-research/), [novelty-assessment](../novelty-assessment/)
