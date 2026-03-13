---
name: legal-risk-assessment-zacharie-laik
description: Conduct legal research and risk analysis using GoodLegal MCP tools. Use this skill whenever the user asks a legal question, wants to research case law or legislation, needs a legal risk assessment, or asks about French or EU law. Trigger on any mention of jurisprudence, legal research, contract risk, regulatory analysis, legal memo, or references to GoodLegal tools — even if the user just says something like "can you look into whether this clause is enforceable" or "what does the case law say about X".
metadata:
  author: Zacharie Laïk
  license: AGPL-3.0
  version: 2026.02.25
---

## Legal Risk Analysis

Assist an in-house legal team with legal research, risk evaluation, and analysis using GoodLegal's research tools. Do not provide legal advice — flag that analyses must be reviewed by qualified legal professionals.

## Output Format

Adapt the output to whatever structure best serves the question — memo, bullet-point summary, narrative analysis, comparison table, or any combination. Two hard requirements:

- **Inline citations**: every legal claim must link to its source (see [references/citations.md](references/citations.md))
- **Sources section**: a consolidated list of all authorities at the end

## Research Methodology

Follow these three steps before concluding on any legal question.

### Step 1: Adversarial search for contradicting jurisprudence

After identifying the established legal position, actively search for decisions that contradict it. Formulate queries using terms like "nullité", "inopposable", "revirement", "contraire", or "primauté" in opposition to the position found.

Example: if case law validates extra-statutory acts signed unanimously, immediately search for "nullité acte extrastatutaire contraire statuts" or "primauté statuts décision unanime".

### Step 2: Doctrinal and web search

Run at least one `web_search` per legal question targeting recent doctrinal commentary. Effective queries: "[topic] revirement jurisprudence [year]" or "[topic] arrêt récent Cour de cassation".

### Step 3: Temporal confidence check

Check the date of the most recent decision supporting the position. If older than 3 years:

- Lower confidence in the assessment
- Run date-filtered `case_search` for the last 24 months
- Flag in the analysis that the position relies on older jurisprudence

### Research flow

For any legal question requiring case law analysis, complete at minimum:

1. Initial search for the established position (`case_search` + `legislation_search`)
2. Adversarial search for contradicting jurisprudence (`case_search` with contrary terms)
3. Doctrinal web search for recent commentary (`web_search`)
4. Temporal check: if the newest supporting case is >3 years old, run date-filtered searches for the last 24 months

Only after completing all four steps, proceed to the analysis. If any step reveals a contradiction or reversal, account for it and inform the user of the jurisprudential evolution.

## GoodLegal MCP Tools

### French law

| Tool | Purpose | When to use |
|------|---------|-------------|
| `legislation_search` | Search across all French codes by topic | Starting point for identifying relevant articles |
| `legislation_retrieve` | Retrieve a specific article by reference | When you know the exact article (e.g., "article 1240 code civil") |
| `case_search` | Search French case law | Core research tool — use date filters for temporal checks |
| `case_retrieve` | Retrieve a specific decision by case number | When you have a pourvoi number — use `include_full_text: true` for raw text |
| `case_legislation` | Get cases organized by codes/articles they cite | Understanding how a specific area of law is applied |
| `article_citation_search` | Find cases citing a specific Légifrance article ID | Tracing how an article has been interpreted over time |

### EU law

| Tool | Purpose | When to use |
|------|---------|-------------|
| `eu_caselaw_search` | Search EU court decisions | Questions involving EU law, directives, or cross-border issues |
| `eu_retrieve` | Retrieve EU legal texts by CELEX/directive number | When you need a specific directive or regulation |

### General

| Tool | Purpose | When to use |
|------|---------|-------------|
| `web_search` | AI-powered web search via Perplexity | Doctrinal commentary, law firm articles — essential for Step 2 |
| `search` | Intelligent routing across all GoodLegal endpoints | Quick general queries when unsure which tool to use |
| `single_text_legislation` | Extract legal references from text | Analyzing a contract clause or decision to identify all articles cited |

### Research strategy

1. **Start broad**: `legislation_search` → `legislation_retrieve` for exact articles
2. **Established position**: `case_search` with descriptive terms
3. **Adversarial check**: `case_search` with contrary terms (Step 1)
4. **Doctrinal check**: `web_search` for recent commentary (Step 2)
5. **Temporal check**: `case_search` with `start_date` set to 2 years ago if key cases are old (Step 3)
6. **Deep dive**: `case_retrieve` on the most important decisions

Launch parallel searches (e.g., initial + adversarial) simultaneously.

## Citation Standards

**Golden rule**: every hyperlink must come from a `uri` field returned by a GoodLegal tool call. Never fabricate Légifrance URLs — they contain opaque identifiers (LEGIARTI, JORFTEXT, etc.) that cannot be guessed. See [references/citations.md](references/citations.md) for full formatting rules and examples.

## When to Escalate

See [references/escalation.md](references/escalation.md) for guidance on when to engage outside counsel (mandatory, recommended, and discretionary triggers).
