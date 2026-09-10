---
name: geo-audit
description: Run a comprehensive GEO visibility audit on any website. Analyzes AI citability, structured data, AI crawler access, llms.txt, and content quality. Produces a 0-30 citability score and prioritized action plan.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebSearch, WebFetch
context: fork
---

# GEO Audit Skill

You are running a GEO (Generative Engine Optimization) audit. This skill analyzes a URL for AI search visibility across platforms like ChatGPT, Perplexity, Google AI Overviews, and Claude.

## Input

The user may provide:
- A specific URL to audit (e.g., `example.com/blog/some-post`)
- A keyword to check visibility for (e.g., "best project management tools")
- "full" for a complete site audit
- A competitor URL for comparative analysis

If no URL is provided, ask the user for one.

## Preparation

If a `brand.md` file exists in the project root, read it for brand context. Otherwise, infer context from the target site's content.

## Audit Steps

### Step 1: Run Python Scripts

Run deterministic checks first — do not skip this step.

```bash
# Technical infrastructure
python3 scripts/check-site.py <url>

# On-page signals + GEO structure
python3 scripts/check-page.py <url>

# Schema markup validation
python3 scripts/check-schema.py <url>

# 0-30 citability score
python3 scripts/check-geo.py <url> --verbose
```

Parse the JSON output from each script. Note any `llm_review_required: true` fields — those require semantic judgment in Step 3.

### Step 2: AI Visibility Check

Derive 5-8 queries from the target page's topic and keywords. Search these queries to check if the target site appears in AI-generated answers.

For each query:
- Use WebSearch to identify top results and AI snippet sources
- Note which competitors appear instead
- Observe what content format and structure cited sources use

### Step 3: Semantic Analysis

Review script output fields marked `llm_review_required: true` and apply judgment:
- Partial keyword matches in title/H1 — natural variant or mismatch?
- Cross-domain canonical — intentional syndication or error?
- Schema completeness — are required fields semantically correct?
- First-sentence quality — does it function as a standalone extractable answer?

### Step 4: Citability Scoring

Use `check-geo.py` output as the base score. Supplement with your semantic analysis to adjust where the script flagged `llm_review_required`.

| Dimension | Abbrev | Score |
|-----------|--------|-------|
| Direct Answer | DA | /5 |
| Data Density | DD | /5 |
| Authority Signals | AS | /5 |
| Structure Quality | SQ | /5 |
| Freshness | FR | /5 |
| Uniqueness | UQ | /5 |
| **Total** | | **/30** |

Grades: A (27–30) · B (22–26) · C (17–21) · D (12–16) · F (<12)

### Step 5: Competitor Benchmark

Identify top 3 competitors appearing in AI responses and compare:

| Factor | Target | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|--------|-------------|-------------|-------------|
| AI Citations | | | | |
| Schema Types | | | | |
| Content Depth | | | | |
| Data Density | | | | |
| FAQ Sections | | | | |

### Step 6: Recommendations

Produce a prioritized action list:

```markdown
## Priority Actions

### P0 — Critical (fix immediately)
1. [Action] — [Expected impact]

### P1 — High Impact (this week)
1. [Action] — [Expected impact]

### P2 — Medium Impact (this month)
1. [Action] — [Expected impact]
```

## Output

Save the audit report to `audits/geo-audit-[domain]-YYYY-MM-DD.md` and display a summary with the citability score and top 3 priority actions.
