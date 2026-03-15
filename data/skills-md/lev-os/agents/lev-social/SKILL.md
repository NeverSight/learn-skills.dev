---
name: lev-social
description: "Multi-platform social research: Twitter/X via Bird CLI and Reddit/TikTok via PostCrawl; aggregate results and generate sentiment/trend reports."
skill_type: tool
category: process-research-social
---

# lev-social

[WHAT] Social media research skill integrating Bird CLI (Twitter/X) and PostCrawl (Reddit/TikTok) for sentiment analysis and trend discovery.

[HOW] Executes search queries across platforms, aggregates results, extracts sentiment patterns, and generates research reports.

[WHEN] Use for market research, competitive analysis, sentiment tracking, community feedback collection, and trend identification.

---

## Prerequisites

- **Bird CLI**: `/opt/homebrew/bin/bird` (Twitter/X GraphQL API)
- **PostCrawl**: `pip install postcrawl` (Reddit/TikTok API)
- **Exa API**: `EXA_API_KEY` env var (background research)
- **Tavily API**: `TAVILY_API_KEY` env var (supplemental search)

---

## Commands

### Twitter Search (Bird CLI)

```bash
# Basic search
bird search "query" -n 20 --json

# Search with pagination
bird search "query" --all --max-pages 5 --json

# Search operators
bird search "from:username query"
bird search "query min_faves:10"
bird search "@mention topic"
```

### Reddit/TikTok Search (PostCrawl)

```python
from postcrawl import PostCrawl

pc = PostCrawl(api_key=os.environ["POSTCRAWL_API_KEY"])

# Search
results = await pc.search(
    social_platforms=["reddit"],
    query="topic keywords",
    results=50
)

# Extract with comments
posts = await pc.extract(
    urls=["https://reddit.com/r/..."],
    include_comments=True,
    comment_filter_config={"min_score": 10}
)
```

### Background Research (Exa)

```bash
curl -s "https://api.exa.ai/search" \
  -H "x-api-key: ${EXA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "topic for research",
    "type": "auto",
    "numResults": 20,
    "category": "tweet"
  }'
```

---

## Research Workflow

### 1. Query Expansion
Design queries per category with:
- Core terms
- Sentiment indicators (positive/negative)
- Platform-specific operators
- Alternative phrasings

### 2. Multi-Platform Collection
```bash
# Twitter (Bird)
bird search "query" -n 50 --json > raw/twitter-cat1.json

# Reddit (PostCrawl via Python)
python -c "..." > raw/reddit-cat1.json

# Background (Exa)
curl ... > raw/exa-context.json
```

### 3. Sentiment Extraction
Parse JSON, extract:
- Engagement metrics (likes, retweets, upvotes)
- Author metadata
- Timestamp distribution
- Sentiment keywords

### 4. Report Generation
Aggregate into:
- Sentiment by category
- Top insights (high-engagement content)
- Pain points (negative sentiment)
- Opportunities (unmet needs)

---

## Team Mode Pattern

For large research projects:

```
| Role | Platform | Responsibility |
|------|----------|----------------|
| twitter-researcher-N | Bird CLI | Execute query batches |
| reddit-researcher | PostCrawl | Subreddit extraction |
| context-gatherer | Exa | Background articles |
| synthesizer | All | Aggregate + report |
```

---

## Output Artifacts

Standard output structure:
```
~/lev/ideas/{research-topic}/
├── query-expansion-plan.md
├── raw/
│   ├── twitter-*.json
│   ├── reddit-*.json
│   └── exa-*.json
├── sentiment-by-category.md
├── top-insights.md
└── final-report.md
```

---

## BD Integration

Create epic for research tracking:
```bash
bd create --type epic --title "Research: {topic}" --priority P0
```

Update with findings:
```bash
bd update {epic-id} --notes "Phase 1 complete: {summary}"
```

---

## Example: OpenClaw Research

```bash
# Phase 1: Twitter sentiment
bird search "openclaw hosting" -n 50 --json > raw/twitter-hosting.json
bird search "openclaw pain point" -n 50 --json > raw/twitter-pain.json

# Phase 2: Reddit supplement
postcrawl search --platforms reddit --query "openclaw" --results 50

# Phase 3: Synthesize
# (Agent aggregates JSON, extracts patterns, generates report)
```

---

## Related Skills

- `lev-research` - General research orchestration
- `lev-intake` - URL/content intake
- `lev get` - Code/docs search

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-social, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
