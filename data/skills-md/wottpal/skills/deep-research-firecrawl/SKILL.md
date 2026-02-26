---
name: deep-research-firecrawl
description: Conducts citation-backed research using Firecrawl MCP search, scrape, map, crawl, and agent tools with selectable quick, standard, deep, and ultradeep modes. Use for multi-source comparisons, technical evaluations, market research, and high-stakes decision support.
---

# Deep Research (Firecrawl)

## Purpose

Deliver verifiable research reports with explicit citations, clear fact-vs-analysis boundaries, and user-selectable depth.

## Tooling requirements

- Use Firecrawl MCP for web retrieval:
  - `firecrawl:firecrawl_search` for discovery
  - `firecrawl:firecrawl_scrape` for page extraction
  - `firecrawl:firecrawl_map` for URL discovery on known domains
  - `firecrawl:firecrawl_crawl` for controlled multi-page capture
  - `firecrawl:firecrawl_agent` for autonomous broad collection when scope is unclear
- Prefer parallel retrieval whenever tasks are independent.
- Hard-stop policy: if Firecrawl MCP is unavailable, pause and ask the user to re-enable it. Do not switch to other web retrieval tools.

## When to use

Use this skill when the request needs multiple sources, synthesis, and evidence quality controls.

Do not use this skill for:

- Simple one-off lookups
- Debugging or code-only tasks
- Questions answerable with 1-2 sources

## Mode selection

If the user does not specify a mode, default to `standard`.

| Mode | Typical runtime | Source target | Output depth |
| --- | --- | --- | --- |
| `quick` | 3-6 min | 6-10 sources | 800-1,500 words |
| `standard` | 8-15 min | 12-20 sources | 2,000-4,000 words |
| `deep` | 15-30 min | 25-40 sources | 4,000-8,000 words |
| `ultradeep` | 30-60+ min | 40-80 sources | 8,000-15,000+ words |

## Execution workflow

### 1) Scope

- Restate the research question.
- Capture explicit constraints (time window, geography, sector, audience).
- Define assumptions only when missing.

### 2) Retrieval plan

- Break the topic into 5-10 search angles.
- Include opposing viewpoints and recent developments.
- Mark which angles need domain deep-dives.

### 3) Retrieve with Firecrawl

- Run parallel `firecrawl:firecrawl_search` queries for all angles.
- Scrape top results with `firecrawl:firecrawl_scrape` for primary evidence.
- For known high-value sites:
  - discover URLs via `firecrawl:firecrawl_map`
  - crawl key paths with bounded `firecrawl:firecrawl_crawl` limits
- Use `firecrawl:firecrawl_agent` when the topic is open-ended or highly fragmented.

### 4) Triangulate

- Verify important claims across at least 3 independent sources.
- Prefer primary sources over commentary when possible.
- Flag conflicts and unresolved uncertainty.

### 5) Synthesize

- Separate facts from interpretation.
- Explain what is known, what is likely, and what is uncertain.
- Include alternative explanations for contested topics.

### 6) Critique and refine (required for `deep`/`ultradeep`)

- Stress-test weak claims.
- Check for recency bias and survivorship bias.
- Add missing counterevidence.

### 7) Package output

Use `templates/report_template.md` and include:

- Executive Summary
- Method and Scope
- Key Findings
- Counterevidence and Risks
- Recommendations
- Bibliography

## Citation and quality rules

- Every major factual claim must include a citation marker like `[1]`.
- Bibliography entries must map one-to-one with cited markers.
- If evidence is weak or contradictory, say so explicitly.
- Never invent citations.

## Stop conditions

Pause and report limitations when:

- Required Firecrawl MCP tools are unavailable (hard-stop policy).
- Source count stays below minimum for the selected mode after broad retrieval attempts.
- Core claims cannot be verified from reliable sources.

## Progressive disclosure

Load only what is needed:

- Method details: `reference/methodology.md`
- Output template: `templates/report_template.md`

## Quick invocation examples

- "Use `deep-research-firecrawl` in `quick` mode on edge AI chip trends in 2025."
- "Run `deep-research-firecrawl` in `deep` mode comparing Auth0, Clerk, and Supabase Auth."
- "Use `deep-research-firecrawl` in `ultradeep` mode for US longevity biotech funding and risks."
