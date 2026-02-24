---
name: deep-research
description: Conduct systematic academic literature reviews in 6 phases, producing structured notes, a curated paper database, and a synthesized final report. Output is organized by phase for clarity.
argument-hint: [topic]
---

# Deep Research Skill

## Trigger

Activate this skill when the user wants to:
- "Research a topic", "literature review", "find papers about", "survey papers on"
- "Deep dive into [topic]", "what's the state of the art in [topic]"
- Uses `/research <topic>` slash command

## Overview

This skill conducts systematic academic literature reviews in 6 phases, producing structured notes, a curated paper database, and a synthesized final report. Output is organized **by phase** for clarity.

**Installation**: `~/.claude/skills/deep-research/` — scripts, references, and this skill definition.
**Output**: `.//Users/lingzhi/Code/deep-research-output/{slug}/` relative to the current working directory.

## Paper Quality Policy

**Peer-reviewed conference papers take priority over arXiv preprints.** Many arXiv papers have not undergone peer review and may contain unverified claims.

### Source Priority (highest to lowest)
1. **Top AI conferences**: NeurIPS, ICLR, ICML, ACL, EMNLP, NAACL, AAAI, IJCAI, CVPR, KDD, CoRL
2. **Peer-reviewed journals**: JMLR, TACL, Nature, Science, etc.
3. **Workshop papers**: NeurIPS/ICML workshops (lower bar but still reviewed)
4. **arXiv preprints with high citations**: Likely high-quality but unverified
5. **Recent arXiv preprints**: Use cautiously, note "preprint" status explicitly

### When to Use arXiv Papers
- As **supplementary** evidence alongside peer-reviewed work
- For **very recent** results (< 3 months old) not yet at conferences
- When a peer-reviewed version doesn't exist yet — note `(preprint)` in citations
- For **survey/review** papers (these are useful even without peer review)

## Search Tools (by priority)

### 1. paper_finder (primary — conference papers only)
**Location**: `/Users/lingzhi/Code/documents/tool/paper_finder/paper_finder.py`

Searches ai-paper-finder.info (HuggingFace Space) for published conference papers. Supports filtering by conference + year. Outputs JSONL with BibTeX.

```bash
python /Users/lingzhi/Code/documents/tool/paper_finder/paper_finder.py --mode scrape --config <config.yaml>
python /Users/lingzhi/Code/documents/tool/paper_finder/paper_finder.py --mode download --jsonl <results.jsonl>
python /Users/lingzhi/Code/documents/tool/paper_finder/paper_finder.py --list-venues
```

Config example:
```yaml
searches:
  - query: "long horizon reasoning agent"
    num_results: 100
    venues:
      neurips: [2024, 2025]
      iclr: [2024, 2025, 2026]
      icml: [2024, 2025]
output:
  root: /Users/lingzhi/Code/deep-research-output/{slug}/phase1_frontier/search_results
  overwrite: true
```

### 2. search_semantic_scholar.py (supplementary — citation data + broader coverage)
**Location**: `/Users/lingzhi/.claude/skills/deep-research/scripts/search_semantic_scholar.py`
Supports `--peer-reviewed-only` and `--top-conferences` filters. API key: `/Users/lingzhi/Code/keys.md` (field `S2_API_Key`)

### 3. search_arxiv.py (supplementary — latest preprints)
**Location**: `/Users/lingzhi/.claude/skills/deep-research/scripts/search_arxiv.py`
For searching recent papers not yet published at conferences. Mark citations with `(preprint)`.

### Other Scripts
| Script | Location | Key Flags |
|--------|----------|-----------|
| `download_papers.py` | `~/.claude/skills/deep-research/scripts/` | `--jsonl`, `--output-dir`, `--max-downloads`, `--sort-by-citations` |
| `extract_pdf.py` | `~/.claude/skills/deep-research/scripts/` | `--pdf`, `--pdf-dir`, `--output-dir`, `--sections-only` |
| `paper_db.py` | `~/.claude/skills/deep-research/scripts/` | subcommands: `merge`, `search`, `filter`, `tag`, `stats`, `add`, `export` |
| `bibtex_manager.py` | `~/.claude/skills/deep-research/scripts/` | `--jsonl`, `--output`, `--keys-only` |
| `compile_report.py` | `~/.claude/skills/deep-research/scripts/` | `--topic-dir` |

### WebFetch Mode (no Bash)
1. **Paper discovery**: `WebSearch` + `WebFetch` to query Semantic Scholar/arXiv APIs
2. **Paper reading**: `WebFetch` on ar5iv HTML or `Read` tool on downloaded PDFs
3. **Writing**: `Write` tool for JSONL, notes, report files

## 6-Phase Workflow

### Phase 1: Frontier
Search the **latest** conference proceedings and preprints to understand current trends.
1. Write `phase1_frontier/paper_finder_config.yaml` targeting latest 1-2 years
2. Run paper_finder scrape
3. WebSearch for latest accepted paper lists
4. Identify trending directions, key breakthroughs
→ Output: `phase1_frontier/frontier.md`, `phase1_frontier/search_results/`

### Phase 2: Survey
Build a comprehensive landscape with broader time range. Target **35-80 papers** after filtering.
1. Write `phase2_survey/paper_finder_config.yaml` covering 2023-2025
2. Run paper_finder + Semantic Scholar + arXiv
3. Merge all results: `python /Users/lingzhi/.claude/skills/deep-research/scripts/paper_db.py merge`
4. Filter to 35-80 most relevant: `python /Users/lingzhi/.claude/skills/deep-research/scripts/paper_db.py filter --min-score 0.80 --max-papers 70`
5. Cluster by theme, write survey notes
→ Output: `phase2_survey/survey.md`, `phase2_survey/search_results/`, `paper_db.jsonl`

### Phase 3: Deep Dive
Select 8-15 papers. **Prefer peer-reviewed papers for deep reading.**
Write selection rationale, then read fully and take structured notes.
→ Output: `phase3_deep_dive/selection.md`, `phase3_deep_dive/deep_dive.md`, `phase3_deep_dive/papers/`

### Phase 4: Code & Tools
Extract GitHub URLs, web search for implementations, benchmarks.
→ Output: `phase4_code/code_repos.md`

### Phase 5: Synthesis
Cross-paper analysis. **Weight peer-reviewed findings higher**.
Taxonomy, comparative tables, gap analysis.
→ Output: `phase5_synthesis/synthesis.md`, `phase5_synthesis/gaps.md`

### Phase 6: Compilation
Assemble final report. Mark preprint citations with `(preprint)` suffix.
→ Output: `phase6_report/report.md`, `phase6_report/references.bib`

## Output Directory

```
output/{topic-slug}/
├── paper_db.jsonl                    # Master database (accumulated)
├── phase1_frontier/
│   ├── paper_finder_config.yaml
│   ├── search_results/
│   └── frontier.md
├── phase2_survey/
│   ├── paper_finder_config.yaml
│   ├── search_results/
│   └── survey.md
├── phase3_deep_dive/
│   ├── papers/
│   ├── selection.md
│   └── deep_dive.md
├── phase4_code/
│   └── code_repos.md
├── phase5_synthesis/
│   ├── synthesis.md
│   └── gaps.md
└── phase6_report/
    ├── report.md
    └── references.bib
```

## Key Conventions

- **Paper IDs**: Use `arxiv_id` when available, otherwise Semantic Scholar `paperId`
- **Citations**: `[@key]` format, key = firstAuthorYearWord (e.g., `[@vaswani2017attention]`)
- **JSONL schema**: title, authors, abstract, year, venue, venue_normalized, **peer_reviewed**, citationCount, paperId, arxiv_id, pdf_url, tags, source
- **Preprint marking**: Always note `(preprint)` when citing non-peer-reviewed work
- **Incremental saves**: Each phase writes to disk immediately
- **Paper count**: Target 35-80 papers in final paper_db.jsonl (use `paper_db.py filter`)

## References

- `/Users/lingzhi/.claude/skills/deep-research/references/workflow-phases.md` — Detailed 6-phase methodology
- `/Users/lingzhi/.claude/skills/deep-research/references/note-format.md` — Note templates, BibTeX format, report structure
- `/Users/lingzhi/.claude/skills/deep-research/references/api-reference.md` — arXiv, Semantic Scholar, ar5iv API guide

## Related Skills
- Downstream: [literature-search](../literature-search/), [literature-review](../literature-review/), [citation-management](../citation-management/)
- See also: [novelty-assessment](../novelty-assessment/), [survey-generation](../survey-generation/)
