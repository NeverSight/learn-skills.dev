---
name: literature-review
description: Conduct a systematic literature review on an academic topic. Use when the user asks for a literature review, survey, or systematic overview of a research area.
argument-hint: [topic]
allowed-tools: Bash, Read, Glob, Grep, Write
---

Conduct a systematic literature review on "$ARGUMENTS" using the `paper` and `paper-search` CLI tools.

## 1. Define Scope

Before searching, clarify with the user:
- Topic boundaries and key terms
- Year range (default: last 5 years)
- Target venues or communities (if any)
- Desired number of papers (default: 15-20 core papers)

## 2. Multi-Query Search

Search with multiple query variations to maximize coverage:
```
paper-search semanticscholar papers "<main query>" --limit 20 --year <range>
paper-search semanticscholar papers "<synonym query>" --limit 20 --year <range>
paper-search semanticscholar papers "<related query>" --limit 20 --year <range>
paper-search google scholar "<topic>"
```

Deduplicate results by title/paper ID.

## 3. Triage

For each unique paper found:
```
paper-search semanticscholar details <paper_id>
paper skim <arxiv_id> --lines 2
```

Categorize as: **highly relevant** / **somewhat relevant** / **not relevant**.

## 4. Deep Analysis

For highly relevant papers:
```
paper outline <arxiv_id>
paper read <arxiv_id> introduction
paper read <arxiv_id> method
paper read <arxiv_id> results
paper read <arxiv_id> conclusion
```

Take structured notes on each paper: problem, method, key results, limitations.

## 5. Citation Graph Exploration

For seminal papers, find related work:
```
paper-search semanticscholar citations <paper_id> --limit 20
paper-search semanticscholar references <paper_id> --limit 20
```

Add any important papers discovered this way back to the triage step.

## 6. Produce Report

Organize findings **by theme, not by paper**. Include:
- Overview of the field and its evolution
- Key methods and approaches (with comparisons)
- Main results and findings
- Open questions and future directions
- Complete reference list with paper IDs and URLs
- BibTeX entries for all cited papers (use `paper bibtex <arxiv_id>` to generate)

## Guidelines

- Aim for breadth first: cover all major approaches before going deep on any one.
- Note citation counts and venues to gauge paper impact.
- Flag contradictory findings explicitly.
- Distinguish between empirical results and theoretical claims.
