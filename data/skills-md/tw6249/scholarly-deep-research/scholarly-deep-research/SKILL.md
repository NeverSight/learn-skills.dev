---
name: scholarly-deep-research
description: Hybrid Deep Research workflow for scholarly literature retrieval, paper-centric citation tracing, paper reading, and topic synthesis. Use when Codex needs to search papers, supplement with web evidence, trace a seed paper's predecessors/successors/deep citations/author trajectories, read paper PDFs or arXiv sources, and write a research-style briefing for literature reviews, related work, prior work, systematic review scoping, bibliography generation, research trend analysis, or evidence collection; supports OpenAlex, Semantic Scholar, Crossref, PubMed, arXiv, credential-gated IEEE Xplore, normalized CSV/JSON/BibTeX, Chinese topic briefs, citation-neighborhood reports, search logs, and Codex-authored deep research reports.
---

# Scholarly Deep Research

## Overview

Use this skill to turn a research question into a reproducible literature retrieval run plus a Deep Research-style topic report. The bundled CLI creates the auditable academic corpus; Codex web search can then supplement that corpus with project pages, author pages, open PDFs, recent preprints, and reliable web context.

## Mode Router

Before running scripts, choose the smallest mode that satisfies the user's request. Do not run every capability just because this skill is active. Users do not need to say a fixed mode name; infer the mode from natural language.

| Mode | Autonomy | Use when the user asks for | Run | Do not also run |
| --- | --- | --- | --- | --- |
| Topic retrieval | Auto default | paper search, literature survey, related work corpus, bibliography, topic brief | `scripts/lit_retrieve.py` | web synthesis, full-paper reading, citation tracing |
| Hybrid Deep Research | Auto when clear | Deep Research-style report, comprehensive Chinese synthesis, web-supplemented topic report | `scripts/lit_retrieve.py`, then Codex web supplement and `deep_research_report.md` | PDF/LaTeX reading unless explicitly requested |
| Paper trace | Auto when clear | paper-centric related-work tracing, predecessors, follow-up work, citation chain, papers using/comparing a seed paper's method, author trajectories from a seed paper | `scripts/trace_paper.py` | topic-wide retrieval or full-paper reading unless requested |
| Paper reading | Explicit high-cost | read full papers, inspect PDFs, analyze arXiv source/LaTeX, paper-level reading reports, close reading | `scripts/read_papers.py` | broad web supplementation unless requested |

Routing rules:

- Default to Topic retrieval when the request is ambiguous.
- Treat natural-language intent as enough; never require the user to say "paper trace mode" or another exact phrase.
- Escalate to Hybrid Deep Research only when the user asks for synthesis/reporting beyond a deterministic topic brief.
- Escalate to Paper reading only when the user clearly asks for full-text/PDF/LaTeX reading or paper-level analysis.
- Combine expensive modes only when the user explicitly asks for a combined workflow; run them as separate stages with separate logs.
- If unsure whether an expensive mode is needed, run the cheaper metadata stage first and mention the available upgrade path.

## Quick Start

Run the bundled Python CLI from this skill folder:

```powershell
python scripts/lit_retrieve.py --query "retrieval augmented generation for medical question answering" --from-year 2020 --to-year 2026 --limit 50 --sources openalex,semanticscholar,crossref,pubmed,arxiv --email user@example.com --report-language zh --report-style brief
```

For IEEE Xplore, include `ieee` in `--sources` and pass `--ieee-api-key`. If the key is missing, the CLI must skip IEEE and log the reason instead of failing.

## Hybrid Deep Research Workflow

1. Clarify the research question only when scope, domain, time range, or inclusion criteria are materially ambiguous.
2. Generate or refine broad, narrow, synonym, citation-oriented, and recent queries. See `references/deep-research-workflow.md`.
3. Run `scripts/lit_retrieve.py` for reproducible retrieval from official APIs.
4. Inspect `search_log.md` and `topic_brief.md` before making claims.
5. Use web search only as a supplement. Record supplemental pages in `web_supplement.md` with URL, source type, relevance, and reason for inclusion.
6. Write `deep_research_report.md` in Chinese by synthesizing `topic_brief.md`, `papers.json`, `search_log.md`, and `web_supplement.md`.
7. Keep API retrieval results and web supplement evidence separate. Do not silently merge web-only findings into `papers.json`.

## Explicit Paper Reading Mode

Paper reading is a high-cost second stage and must not run by default. Use it only when the user explicitly asks to read full papers, inspect PDFs, analyze arXiv source, or generate paper-level reading reports.

Run it after retrieval:

```powershell
python scripts/read_papers.py --papers-json outputs/run/papers.json --query "multi agent connectivity control" --reading-limit 5 --reading-selection auto
```

Reading mode prefers source quality in this order:

1. arXiv LaTeX source from `https://arxiv.org/src/<arxiv_id>`, cached locally, unpacked, entrypoint detected, then recursive `\input` / `\include` reading.
2. Open-access PDF from arXiv PDF or `open_access_url`, saved under `pdfs/`, then text extracted with `pdftotext` when available.
3. Metadata-only note when neither LaTeX source nor open PDF text is available.

Reading outputs:

- `arxiv_sources/`: unpacked arXiv source for papers with available TeX.
- `pdfs/`: saved open-access PDFs for fallback reading.
- `paper_texts/`: extracted text and metadata JSON.
- `reading_reports/`: one structured Markdown report per selected paper.
- `pdf_manifest.csv`: acquisition status, local paths, and notes.
- `reading_index.md`: overview of what was actually read.

## Paper Trace Mode

Use paper trace mode when the user provides a seed paper and asks to find related work from that paper outward: predecessors, follow-up development, papers that use or compare against its method, or recent work by the seed authors and related-method authors. Natural-language requests are enough; the user does not need to name this mode.

When the Mode Router selects paper trace, run:

```powershell
python scripts/trace_paper.py --paper "10.1109/tnse.2021.3139045" --limit 30 --openalex --output-dir outputs/trace-connectivity-control
```

Trace mode uses Semantic Scholar for references, citations, citation contexts, citation intents, influential-citation signals, and author trajectories. Use `--openalex` as a fallback/supplement when Semantic Scholar references are unavailable or publisher-elided.

Trace outputs:

- `paper_trace.json`: structured seed, predecessor, successor, deep-citation, and author-update data.
- `paper_trace.csv`: table version of related papers.
- `paper_trace_report.md`: Chinese report organized around likely predecessors, follow-up work, deep/method citations, and author latest work.

Interpretation rules:

- Treat seed references as possible predecessors or knowledge sources, not proven inspiration.
- Treat citing papers as follow-up work, not necessarily method users.
- Treat method/deep citations as stronger only when citation contexts, intents, or influential flags support that reading.
- Clearly report when references are unavailable, elided, or metadata-only.

## Outputs

Each run writes a timestamped output directory unless `--output-dir` is provided:

- `papers.csv`: normalized table for spreadsheet screening.
- `papers.json`: normalized records with scores and source metadata.
- `papers.bib`: BibTeX entries suitable for import into citation managers.
- `report.md`: Chinese topic brief by default, or ranked list when `--report-style list` is used.
- `topic_brief.md`: deterministic Chinese research briefing generated from retrieved metadata.
- `web_supplement.md`: Codex-authored supplemental web-search notes when a hybrid run is requested.
- `deep_research_report.md`: Codex-authored final synthesis when a hybrid run is requested.
- `reading_reports/` and `reading_index.md`: explicit paper-reading outputs when `scripts/read_papers.py` is run.
- `paper_trace_report.md`, `paper_trace.json`, and `paper_trace.csv`: explicit paper-trace outputs when `scripts/trace_paper.py` is run.
- `search_log.md`: source parameters, counts, skipped sources, and ranking formula.
- `errors.log`: connector errors, only when failures occur.

## Data Model

Normalize paper records to:

`title`, `authors`, `year`, `venue`, `doi`, `arxiv_id`, `url`, `abstract`, `source`, `citation_count`, `is_open_access`, `open_access_url`, `publication_type`, `keywords`.

Deduplicate in this order:

1. DOI exact match.
2. arXiv ID exact match.
3. High normalized-title similarity.
4. Same normalized title, first author, and nearby year.

Rank with a transparent score combining lexical relevance, citation count, recency, venue/source confidence, and open-access signal. Treat ranking as a screening aid, not a scientific judgment.

## Report Expectations

For Deep Research-style outputs, emphasize the topic rather than the mechanics of search:

- Define the problem and why it matters.
- Group the literature into technical routes.
- Identify representative papers and their roles.
- Describe the research timeline and method evolution.
- Compare major method families.
- State limitations, open problems, and a recommended reading order.
- Cite paper metadata from `papers.json` and web evidence from `web_supplement.md`.

## Boundaries

- Use official APIs only.
- Do not scrape Google Scholar, ResearchGate, publisher pages, or paywalled PDFs.
- Do not claim the Python CLI has ChatGPT's internal web-search capability. Web search is a Codex workflow step, not a CLI connector.
- Do not run paper reading mode unless the user explicitly asks for it; it downloads and parses larger artifacts.
- Do not run paper trace mode unless the user asks for paper-centric relationship tracing in any clear wording; citation graph APIs can be incomplete and rate-limited.
- Do not claim exhaustive coverage unless the user provided a full review protocol, selected databases, exact queries, and inclusion criteria.
- State that results depend on API availability, source coverage, query quality, metadata quality, and credentials.
- Read `references/api-notes.md` when changing connector behavior, API parameters, or source-specific claims.
- Read `references/report-template-zh.md` before writing `deep_research_report.md`.
