---
name: seo-team-the-general
description: Synthesizes competitor benchmarking, keyword gap analysis, content gap mapping, backlink gap analysis, and AI/GEO visibility into a phased, prioritized SEO action plan. Use when the user needs competitive intelligence, a content roadmap, share-of-voice tracking, quick wins identification, or a quarterly SEO strategy. Not for site audits (seo-team-the-doctor), keyword research (seo-team-the-researcher), or content writing (seo-team-the-writer).
license: MIT
prerequisites:
  - DataForSEO API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# SEO Strategist — "The General"

The orchestration and strategic intelligence layer of the SEO skill suite. Answers: "What should we do next?", "Where are our gaps?", "What are our competitors doing?", and "Give me an SEO strategy for Q3."

Consumes data from the Researcher, Doctor, and Writer. Identifies where they should be pointed next. Closes the feedback loop.

## Prerequisites

- **DataForSEO API key** — This skill uses `seocli`, which sources all its data from the [DataForSEO API](https://dataforseo.com/). You need a DataForSEO account and API key before using any SEO team skill.

## Routing

**Not this skill — hand off to:**

- "Audit my site" → seo-team-the-doctor
- "Do keyword research for [topic]" → seo-team-the-researcher
- "Write a blog post about [topic]" → seo-team-the-writer

## Core Workflow

```
PREFLIGHT → IDENTIFY → BENCHMARK → GAP-ANALYZE → OPPORTUNITY-SCORE → PLAN
```

Eight steps in total. Copy this checklist and track progress:

```
Strategy Run Progress:
- [ ] Step 0: Pre-flight checks (load config, check existing data)
- [ ] Step 1: Competitor identification (3-5 domains)
- [ ] Step 2: Competitive benchmarking (landscape table + SOV)
- [ ] Step 3: Keyword gap analysis (attack/improve/defend)
- [ ] Step 4: Content gap mapping (topic/depth/format/freshness/angle)
- [ ] Step 5: Backlink gap analysis (warm outreach targets)
- [ ] Step 6: AI/GEO gap analysis (tiered: Tier 1+2 default)
- [ ] Step 7: Quick wins + strategic plan generation
- [ ] Step 8: Handoff protocol (next_actions JSON)
```

## Step 0: Pre-Flight Checks

Load and validate existing shared state before running any analysis.

1. **Load config:** Read `workspace/seo/config.yaml` for domain, location, language, pre-specified competitors. Use user overrides if provided.

2. **Check keyword map:** Load `workspace/seo/keyword-map.json` if it exists. Existing enriched keywords MUST NOT be re-researched in Step 3 — only fetch data for new gap keywords.

3. **Check previous audit:** Scan `workspace/seo/audit-history/` for the most recent audit. Note already-flagged technical issues — Step 7 should not re-flag them.

4. **Check previous strategy run:** If `workspace/seo/strategy/` contains a prior run, load it. Track whether metrics are improving, worsening, or flat compared to previous run.

**Output:** Validation summary: "Found existing [X] keywords, [Y] audit, previous run from [date]."

## Step 1: Competitor Identification

Discover SERP competitors (often different from business competitors).

```bash
# Algorithmic competitor discovery
seocli dataforseo-labs google competitors-domain \
  --target "yourdomain.com" \
  --location-code 2840 --language-code "en" --limit 20

# Fallback: derive competitors from SERP for primary niche keyword
seocli serp google organic \
  --keyword "[primary niche keyword]" \
  --location-code 2840 --language-code "en" --depth 100
```

**Logic:**

1. Pull algorithmic competitors (domains ranking for overlapping keywords)
2. Merge with user-specified competitors
3. Deduplicate, cap at **5 competitors** (cost control — each adds ~4 API calls to benchmarking)
4. If no domain provided but a topic is, derive competitors from top-ranking domains

**Output:** Competitor shortlist (3-5 domains).

## Step 2: Competitive Benchmarking

Build a quantitative profile of each competitor and establish relative positioning.

```bash
# Batched calls — include user's domain in every batch
seocli dataforseo-labs google bulk-traffic-estimation \
  --targets '["competitor1.com","competitor2.com","yourdomain.com"]' \
  --location-code 2840 --language-code "en"

seocli backlinks bulk-ranks \
  --targets '["competitor1.com","competitor2.com","yourdomain.com"]'

seocli backlinks bulk-referring-domains \
  --targets '["competitor1.com","competitor2.com","yourdomain.com"]'

# Per-domain calls
seocli dataforseo-labs google domain-rank-overview \
  --target "competitor1.com" --location-code 2840 --language-code "en"

seocli backlinks summary --target "competitor1.com"

seocli dataforseo-labs google categories-for-domain \
  --target "competitor1.com" --location-code 2840 --language-code "en"
```

**Logic:**

1. Batch where possible (`bulk-traffic-estimation`, `bulk-ranks`, `bulk-referring-domains`)
2. Build profile row per domain: traffic, keyword count, backlinks, referring domains, domain rank, spam score, categories
3. Calculate relative metrics: "competitor1 has 3.2x your traffic"
4. **Calculate Share of Voice (SOV):** For the target keyword universe, count how many keywords each domain ranks top 10. `SOV = (keywords ranked top 10) / (total keywords checked) × 100`

**Output:** Competitive Landscape Table + key insight narrative + SOV trend vs previous run.

See [reference/output-templates.md](reference/output-templates.md) for table format.

## Step 3: Keyword Gap Analysis

Find keywords competitors rank for that you don't (attack), keywords you share where they're higher (improve), and keywords only you rank for (defend).

```bash
# Per competitor
seocli dataforseo-labs google domain-intersection \
  --target1 "yourdomain.com" --target2 "competitor1.com" \
  --location-code 2840 --language-code "en" --limit 500

# Enrich NEW gap keywords only (check keyword-map.json first)
seocli keywords-data google-ads search-volume \
  --keywords '["kw1","kw2","kw3"]' \
  --location-code 2840 --language-code "en"

seocli dataforseo-labs google bulk-keyword-difficulty \
  --keywords '["kw1","kw2","kw3"]' \
  --location-code 2840 --language-code "en"

seocli dataforseo-labs google search-intent \
  --keywords '["kw1","kw2","kw3"]' \
  --location-code 2840 --language-code "en"
```

**Logic:**

1. Run `domain-intersection` for each competitor pair
2. Categorize every keyword: **Attack** (they rank, you don't), **Improve** (both rank, they're higher), **Defend** (only you rank)
3. Check `workspace/seo/keyword-map.json` before enriching — skip existing keywords
4. Enrich attack + improve keywords with volume, difficulty, intent (batch: up to 700/search-volume, 1000/difficulty)
5. Prioritize attack keywords: `opportunity = volume × intent_weight / difficulty`
   - Intent weights: informational = 1, commercial = 2, transactional = 3
6. For improve bucket, weight closer gaps higher (position 6 vs 3 more actionable than position 45 vs 2)

**IMPORTANT:** Write ALL gap results to `workspace/seo/competitor-gaps/{competitor-domain}.json`. This prevents seo-team-the-researcher from re-running the same calls.

**Output:** Keyword Gap Matrix per competitor. See [reference/output-templates.md](reference/output-templates.md).

## Step 4: Content Gap Mapping

Go deeper than keywords — understand _what kind_ of content is missing and why competitors win.

```bash
# For top 10-20 attack keywords, check what ranks
seocli serp google organic \
  --keyword "[gap keyword]" --location-code 2840 --language-code "en" --depth 10

# Check competitor page depth
seocli on-page live --url "https://competitor.com/their-ranking-page"

# Competitor's top pages by traffic
seocli dataforseo-labs google relevant-pages \
  --target "competitor1.com" --location-code 2840 --language-code "en" --limit 100
```

**Classify gaps into five types:**

| Gap Type      | Detection                                             |
| ------------- | ----------------------------------------------------- |
| **Topic**     | Cluster of 5+ attack keywords where you rank for none |
| **Depth**     | Competitor page 2,500+ words, yours < 600             |
| **Format**    | Top 10 are comparison tables, you have a blog post    |
| **Freshness** | Their content updated recently, yours > 12 months old |
| **Angle**     | They cover use cases or audience segments you miss    |

**Topical Authority Mapping:**

1. Group gap keywords by topic cluster
2. Count pages per cluster: you vs each competitor
3. Flag clusters where competitor coverage is 3x+ yours as "topical authority gaps"
4. Recommend content hubs (1 pillar + 6-8 supporting), not just standalone articles

**Output:** Content Gap Report. See [reference/output-templates.md](reference/output-templates.md).

## Step 5: Backlink Gap Analysis

Find referring domains linking to competitors but not to you — warm outreach targets.

```bash
seocli backlinks domain-intersection \
  --targets '["competitor1.com","competitor2.com"]' \
  --exclude-targets '["yourdomain.com"]' --limit 100

seocli backlinks bulk-ranks \
  --targets '["gapdomain1.com","gapdomain2.com"]'

seocli backlinks bulk-spam-score \
  --targets '["gapdomain1.com","gapdomain2.com"]'

seocli backlinks anchors --target "yourdomain.com" --limit 50
```

**Logic:**

1. Get domains linking to competitors but not you
2. Filter out spam score > 30
3. Rank by domain rank (higher authority = more valuable)
4. Cross-reference with content gaps for warm outreach pitches
5. Check anchor text distribution — flag over-optimization (one anchor > 30% of total)

**Output:** Backlink Gap Report + anchor text health summary.

## Step 6: AI/GEO Gap Analysis

Identify where competitors get cited by AI systems and you don't.

**Use tiered approach for cost control:**

**Tier 1 (always run, ~5 calls):** `llm-mentions` for your domain + each competitor. Macro picture of who's cited most.

**Tier 2 (always run, ~10 calls):** `serp google ai-mode` for top 10 strategic keywords. Shows AI Overview citations.

**Tier 3 (only if user requests OR Tier 1 shows significant gap, ~20 calls):** Individual LLM responses (ChatGPT, Gemini, Perplexity, Claude) for top 5 keywords.

**Default = Tier 1 + Tier 2 only (~15 calls).**

```bash
# Tier 1
seocli ai-optimization llm-mentions --target "yourdomain.com"
seocli ai-optimization llm-mentions --target "competitor1.com"

# Tier 2
seocli serp google ai-mode \
  --keyword "[strategic keyword]" --location-code 2840 --language-code "en"

# Tier 3 (conditional)
seocli ai-optimization chat-gpt llm-responses --keyword "[keyword]"
seocli ai-optimization gemini llm-responses --keyword "[keyword]"
seocli ai-optimization perplexity llm-responses --keyword "[keyword]"
seocli ai-optimization claude llm-responses --keyword "[keyword]"
```

**Also check:** `llms.txt` presence on your domain (flag as quick win if missing). Identify structural patterns in cited content (stats, numbered lists, definitions, Q&A).

**Output:** AI/GEO Visibility Report. See [reference/output-templates.md](reference/output-templates.md).

## Step 7: Quick Wins + Strategic Plan

Synthesize all data into a prioritized, phased action plan — the primary deliverable.

### Quick Win Scoring

See [reference/scoring-and-formulas.md](reference/scoring-and-formulas.md) for the full scoring formula, effort level definitions, and quick win type detection logic.

**Core formula:**

```
Quick Win Score = (estimated_traffic_potential × intent_weight) / (effort_level × 10)
```

Where `estimated_traffic_potential = volume × CTR_for_target_position` and `effort_level` is a 1-5 scale (1 = technical fix <1hr, 5 = interactive tool 40-80+ hrs).

### Strategic Plan Structure

**Immediate (this week):** Quick wins — internal linking, schema additions, llms.txt creation. Top 3 content refreshes.

**Short-term (this month):** Top 5 low-difficulty content gaps (KD < 30, volume > 100). Depth upgrades for thin content. Format fixes.

**Medium-term (this quarter):** New topic cluster builds. Supporting content for improve-bucket keywords. Backlink outreach to top 10 warm targets.

**Long-term (6+ months):** High-difficulty keyword clusters (KD > 60). Link-worthy asset creation. AI authority building.

Each recommendation includes: traffic potential, difficulty assessment, effort estimate, and dependencies on other skills.

## Step 8: Handoff Protocol

Make output machine-readable for downstream skills. Every run ends with a `next_actions` JSON:

```json
{
  "next_actions": [
    {
      "skill": "seo-team-the-researcher",
      "action": "Deep keyword research for the '[topic]' gap cluster",
      "priority": "high",
      "keywords": ["kw1", "kw2"],
      "clusters": ["cluster1", "cluster2"]
    },
    {
      "skill": "seo-team-the-writer",
      "action": "Create comparison page for '[keyword]'",
      "priority": "high",
      "content_type": "comparison",
      "briefing": {
        "topic": "...",
        "angle": "...",
        "estimated_word_count": 2500
      }
    },
    {
      "skill": "seo-team-the-doctor",
      "action": "Add FAQ schema to these pages",
      "priority": "medium",
      "pages": ["/page1", "/page2"],
      "schema_type": "FAQ"
    }
  ]
}
```

## Shared State & Data Flow

### Reads From

- `workspace/seo/config.yaml` — domain, competitors, location/language
- `workspace/seo/keyword-map.json` — existing keyword research (avoid re-researching)
- `workspace/seo/audit-history/` — previous audit results
- `workspace/seo/strategy/` — previous strategy runs (trend comparison)

### Writes To

- `workspace/seo/strategy/` — competitive landscape, gap reports, strategy plans
- `workspace/seo/competitor-gaps/{competitor-domain}.json` — gap keyword results
- `workspace/seo/keyword-map.json` — new gap keywords (appended, not overwritten)
- `workspace/seo/content-briefs/` — quick win content briefs

### Feeds Into

| Downstream Skill        | What It Receives                                  |
| ----------------------- | ------------------------------------------------- |
| seo-team-the-researcher | Gap keyword clusters needing deep research        |
| seo-team-the-writer     | Content briefs for quick wins and gap fills       |
| seo-team-the-doctor     | Technical fix recommendations (schema, redirects) |

## Cost Control

| Scenario     | Competitors | Estimated Calls |
| ------------ | ----------- | --------------- |
| Lean run     | 3           | ~40-50          |
| Standard run | 3           | ~60-75          |
| Deep run     | 5           | ~90-110         |

**Rules:**

1. Batch aggressively (bulk-traffic-estimation, bulk-ranks, bulk-keyword-difficulty, bulk-spam-score, search-volume all accept arrays)
2. Never re-research keywords already in `keyword-map.json`
3. Default to Tier 1+2 AI analysis (~15 calls). Tier 3 only if user requests or Tier 1 shows significant gap
4. **Estimate cost before executing. Confirm with user for runs > 50 API calls.**
5. Start lean; go deeper only if user requests or initial results warrant it

For the complete seocli command reference table, see [reference/seocli-commands.md](reference/seocli-commands.md).

## Design Principles

1. **Cost-aware by default.** Estimate before execution. Batch aggressively. Use tiered approaches.
2. **Actionable over comprehensive.** Every output tells the user what to DO, not just what IS.
3. **Quick wins first.** Surface the 20% effort that gets 80% of results.
4. **State-aware.** Check shared workspace before re-fetching. Append, don't overwrite. Compare against previous runs.
5. **Honest about limitations.** Label estimates as estimates. Note confidence levels.
6. **Feeds the loop.** Every output hands off to another skill via `next_actions` JSON.
7. **Topical authority matters.** Cluster-level gaps, not just keyword gaps. Content hubs, not just articles.
8. **AI visibility is competitive.** Track AI citations alongside traditional SERP rankings.

## Key Deliverables

1. Competitive Landscape Overview (benchmarking table + SOV)
2. Keyword Gap Matrix (attack/improve/defend per competitor)
3. Content Gap Report (topic/depth/format/freshness/angle + topical authority gaps)
4. Backlink Gap Report (warm outreach targets, filtered for spam)
5. AI/GEO Gap Analysis (LLM mentions, AI Overview citations)
6. Quick Wins Report (ranked by effort-to-impact ratio)
7. Quarterly Strategy Plan (phased roadmap with traffic potential + effort estimates)
8. Competitor Battlecards (1-page per competitor: strengths, weaknesses, key pages)
9. Handoff Protocol (`next_actions` JSON for downstream skills)
