---
name: citecheck
version: 0.1.0
description: Use when the user asks to "verify citations", "check references", "validate paper citations", or "evaluate reference relevance". It extracts references from LaTeX/PDF papers, checks formatting rules, verifies existence via Crossref / Semantic Scholar / OpenAlex / PubMed / arXiv / dblp / Google Scholar / WebSearch, and scores thematic/semantic relevance.
---

# CiteCheck — Paper Citation Verification

## Overview

CiteCheck verifies academic paper citations by combining structured parsing with agent-native LLM evaluation. It supports LaTeX source files (preferred) and PDF fallback.

## Workflow

1. **Parse paper**: Call `citecheck` CLI to read LaTeX (preferred) or PDF, extract references and body text
2. **Format check**: Call `citecheck` CLI to validate bibliography entries
3. **Queryability verification**: Call `citecheck` CLI to verify existence via Crossref / Semantic Scholar
4. **Evaluate thematic relevance**: Evaluate directly using the agent's reasoning capabilities — compare cited paper title/abstract/venue against the citing paper
5. **Evaluate semantic accuracy**: Evaluate directly using the agent's reasoning capabilities — compare in-text citation context against cited source content
6. **Generate report**: Aggregate all results into a Markdown report

> **Why matching steps are not done by the CLI**
> The `citecheck` CLI can run standalone with optional `--api-key` for external LLM-powered matching. When used as a Skill, the host agent itself possesses LLM reasoning capabilities. Direct evaluation is faster, more consistent, and **requires no additional API keys from the user**.

---

## 1. Parse Paper (CLI)

### LaTeX source (preferred)

```bash
citecheck path/to/latex_project/ --skip-verification --skip-semantic -o parsed_report.md
```

Or parse a single file:

```bash
citecheck main.tex --skip-verification --skip-semantic -o parsed_report.md
```

### PDF (fallback)

```bash
citecheck paper.pdf --skip-verification --skip-semantic -o parsed_report.md
```

> `--skip-verification` and `--skip-semantic` are required in Skill mode because steps 3–5 are performed directly by the agent.

---

## 2. Format Check (CLI)

Call `citecheck` to check and report format issues:

| Check item | Description |
|------------|-------------|
| Required fields | Author, title, year, venue completeness |
| Format consistency | Punctuation, capitalization, abbreviation uniformity |
| DOI/URL | If present, whether format is correct and accessible |
| Year sanity | No `202x` placeholders, not in the future |

Detailed rules: see [./references/format-check-rules.md](./references/format-check-rules.md).

---

## 3. Queryability Verification (CLI + Agent Supplement)

Call `citecheck` to query Crossref and Semantic Scholar public APIs for citation existence.

API details: see [./references/api-reference.md](./references/api-reference.md).

**If the CLI fails due to network/SSL issues**, use WebSearch to directly query suspicious citations (especially those marked "unverifiable"), supplementing the verification results.

---

## 4. Evaluate Thematic Relevance (Agent Direct)

**Do not call the CLI or any external API.** Evaluate directly using the agent's reasoning capabilities.

For each reference, extract:
- Citing paper: `title`, `abstract`, `keywords`
- Cited paper: `title`, `abstract` (from API results or WebSearch), `venue`

Evaluation prompt template: see [./references/thematic-scoring-prompt.md](./references/thematic-scoring-prompt.md).

---

## 5. Evaluate Semantic Accuracy (Agent Direct)

**Do not call the CLI or any external API.** Evaluate directly using the agent's reasoning capabilities.

For each in-text citation position:

1. Extract 1–2 sentences before and after the citation marker as `citing_text`
2. Obtain the cited paper's abstract via Semantic Scholar or WebSearch as `cited_text`
3. Evaluate semantic consistency using the prompt template: see [./references/semantic-matching-prompt.md](./references/semantic-matching-prompt.md).

---

## 6. Output Report

Generate a Markdown report containing:

### Summary
- Total references
- Format issues count
- Query failures / suspicious count
- Average thematic relevance score
- Average semantic accuracy score

### Detailed Results Table

| No. | Title | Format | Queryable | Thematic | Semantic | Notes |
|-----|-------|--------|-----------|----------|----------|-------|
| 1 | ... | ✅/⚠️/❌ | ✅/❌ | 0.85 | 0.90 | DOI mismatch |

### Issue Summary
- List all findings and recommendations by severity

---

## Dependencies

```bash
pip install CiteCheck
```

For PDF support:

```bash
pip install CiteCheck[pdf]
```

---

## Notes

- **No `--api-key` is required in Skill mode**. Thematic and semantic matching are performed directly by the agent, with no external LLM API calls.
- Prioritize LaTeX source files; parsing accuracy is far higher than PDF.
- Add delays and retries to API calls to avoid rate limiting.
- When Semantic Scholar abstracts are missing, fall back to Crossref + title keywords.
- Semantic matching requires the cited paper's abstract; mark "source unreachable" when unavailable.
- If placeholder citations like `=?` or `[?, ?]` are found, mark them as "unverifiable references".
