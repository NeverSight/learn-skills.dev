---
name: citation-management
description: Manage BibTeX citations for LaTeX papers. Harvest missing citations from a draft using Semantic Scholar, validate cite keys against .bib files, deduplicate entries, and format bibliography. Use when working with references, BibTeX, or citations.
argument-hint: [tex-or-bib-file]
---

# Citation Management

Manage the full lifecycle of citations in a LaTeX paper.

## Input

- `$0` — Action: `harvest`, `validate`, `add`, `format`
- `$1` — Path to `.tex` or `.bib` file

## Scripts

### Validate citations (check all cite keys resolve)
```bash
python ~/.claude/skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --check-figures --figures-dir paper/figures/
```

Reports: missing citations, unused bib entries, duplicate keys, duplicate sections, duplicate labels, undefined references, missing figures.

### Generate BibTeX from paper database
```bash
python ~/.claude/skills/deep-research/scripts/bibtex_manager.py \
  --jsonl paper_db.jsonl --output references.bib
```

### Search for a specific paper to add
```bash
python ~/.claude/skills/deep-research/scripts/search_semantic_scholar.py \
  --query "attention is all you need" --max-results 5 \
  --api-key "$(grep S2_API_Key /Users/lingzhi/Code/keys.md 2>/dev/null | cut -d: -f2 | tr -d ' ')"
```

### Harvest missing citations automatically
```bash
python ~/.claude/skills/citation-management/scripts/harvest_citations.py \
  --tex paper/main.tex --bib paper/references.bib --output candidates.bib --max-rounds 10
```

Scans .tex for uncited claims, searches Semantic Scholar, outputs candidate BibTeX entries.
Key flags: `--dry-run` (preview only), `--verbose`, `--api-key`

### Auto-fix missing citation placeholders
```bash
python ~/.claude/skills/citation-management/scripts/validate_citations.py \
  --tex paper/main.tex --bib paper/references.bib --fix
```

Generates `references_fixed.bib` with placeholder entries for all missing citation keys.

## Action: `harvest` — Iterative Citation Harvesting

Based on AI-Scientist's 20-round citation harvesting loop. For each round:

1. Read the current `.tex` draft
2. Identify the most important missing citation
3. Search Semantic Scholar via script
4. Select the most relevant paper from results
5. Extract BibTeX and generate a clean key (`lastNameYearWord`)
6. Append to `.bib` (skip if key exists)
7. Insert `\cite{key}` at the appropriate location
8. Stop when no more gaps or 20 rounds reached

**Key rules:**
- DO NOT add a citation that already exists
- Only add citations found via API — never fabricate
- Cite broadly — not just popular papers
- Do not copy verbatim from prior literature

## Action: `validate` — Pre-Compilation Check

Run `validate_citations.py` to catch all issues before compilation. Fix any reported problems.

## Action: `add` — Add Specific Paper

Search Semantic Scholar for the paper, extract BibTeX, clean the key, append to `.bib`.

BibTeX key format: `firstAuthorLastNameYearFirstContentWord` (e.g., `vaswani2017attention`)

## Action: `format` — Standardize .bib

- Sort entries alphabetically by key
- Ensure consistent indentation (2 spaces)
- Remove empty fields
- Protect proper nouns with `{Braces}` in titles
- Ensure required fields per entry type

## Related Skills
- Upstream: [literature-search](../literature-search/), [deep-research](../deep-research/)
- Downstream: [paper-compilation](../paper-compilation/), [latex-formatting](../latex-formatting/)
- See also: [related-work-writing](../related-work-writing/)
