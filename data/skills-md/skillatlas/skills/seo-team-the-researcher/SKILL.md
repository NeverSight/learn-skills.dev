---
name: seo-team-the-researcher
description: Turns topics, domains, or competitor lists into prioritized, clustered keyword maps with volume, difficulty, intent, and funnel-stage data using seocli. Use when the user needs keyword research, topic discovery, keyword mapping, search demand analysis, or content opportunity identification.
license: MIT
prerequisites:
  - DataForSEO API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# SEO Keyword Researcher

Transforms a starting point — a topic, domain, competitor, or keyword list — into a structured, prioritized keyword map that downstream skills (seo-team-the-writer, seo-team-the-doctor, seo-team-the-general) can act on.

## Prerequisites

- **DataForSEO API key** — This skill uses `seocli`, which sources all its data from the [DataForSEO API](https://dataforseo.com/). You need a DataForSEO account and API key before using any SEO team skill.

## Pipeline Overview

```
CHECK STATE → SEED → EXPAND → ENRICH → CLUSTER → PRIORITIZE → MAP
```

Each stage feeds the next. The full pipeline produces a keyword map with clusters, opportunity scores, and recommended actions. For a quick pass on user-provided keywords, skip SEED and EXPAND.

## Input Classification

Parse the user's request to determine seeding strategy:

| Input Type       | Detection                                                      | Seeding Path                                 |
| ---------------- | -------------------------------------------------------------- | -------------------------------------------- |
| **Topic**        | Subject without a domain ("keyword research for home brewing") | Path A: LLM brainstorming                    |
| **Domain**       | URL the user controls ("research keywords for mysite.com")     | Path B: Domain API calls                     |
| **Competitors**  | One or more competitor domains                                 | Path C: Competitor ranked keywords           |
| **Keyword list** | User provides specific keywords                                | Path D: Skip seeding, go to EXPAND or ENRICH |

Inputs combine: "research home brewing for mysite.com vs competitor.com" uses A + B + C.

## Configuration

Before any API calls, resolve **location** and **language**:

1. Check `workspace/seo/config.yaml` for saved defaults
2. Check if user specified in their request ("keywords in the UK")
3. If neither: ask the user. Default suggestion: `--location-code 2840` (US), `--language-code en`

Save resolved config:

```yaml
# workspace/seo/config.yaml
domain: example.com
location_code: 2840
location_name: "United States"
language_code: "en"
language_name: "English"
competitors:
  - competitor1.com
```

All `seocli` commands below require `--location-code` and `--language-code` (plus `--location-name` and `--language-name` for dataforseo-labs commands). Omitted for brevity — always include them.

For the complete command reference with all flags and batch limits, see [reference/seocli-commands.md](reference/seocli-commands.md).

---

## Step 0: Check Shared State

Before running any pipeline stages, check for existing data:

1. **Keyword map:** Load `workspace/seo/keyword-map.json` — extract relevant seeds, skip re-researching existing keywords
2. **Competitor gaps:** Check `workspace/seo/competitor-gaps/{competitor}.json` — reuse gap keywords instead of re-running `domain-intersection`
3. **Audit history:** Check `workspace/seo/audit-history/` — domain authority data used later in PRIORITIZE for Personal Keyword Difficulty

**Decision logic:**

- Existing keyword data found → merge into seeds, skip to EXPAND
- Existing gap data found → load gap keywords, tag as "gap"
- No existing data → full pipeline from Stage 1

---

## Stage 1: SEED

**Goal:** Generate 30–100 initial seed keywords.

### Path A: Topic-Based (no API calls)

Brainstorm seeds across these angles:

1. **Core terms** — head keywords and spelling variants
2. **Problem-focused** — what problems does this solve?
3. **Solution-focused** — what solutions does it offer?
4. **Audience segments** — who searches for this?
5. **Modifiers** — append to core terms: best, top, how to, guide, tutorial, vs, alternative, [current year], for beginners, for [audience]
6. **Question variants** — who/what/where/when/why/how for each core term

Target: 50–100 seeds. Don't filter for quality yet.

### Path B: Domain-Based (3 API calls)

```bash
# Keywords associated with the domain
seocli keywords-data google-ads keywords-for-site live \
  --target example.com --sort-by search_volume --limit 200

# Topical footprint
seocli dataforseo-labs google categories-for-domain \
  --target example.com --include-subcategories --limit 20

# Organic competitors (feed into Path C)
seocli dataforseo-labs google competitors-domain \
  --target example.com --limit 10 --exclude-top-domains
```

Use top keywords from call 1 as seeds. Use categories from call 2 to brainstorm adjacent topics. Use competitors from call 3 as input to Path C.

### Path C: Competitor-Based

**First:** Check `workspace/seo/competitor-gaps/{competitor}.json`. If gap data exists, load directly — skip the API calls below.

**If no existing data:**

```bash
# Per competitor: top ranked keywords
seocli dataforseo-labs google ranked-keywords \
  --target competitor1.com --limit 200 \
  --order-by "keyword_data.keyword_info.search_volume,desc"

# Gap analysis: what they rank for that you don't
seocli dataforseo-labs google domain-intersection \
  --target1 competitor1.com --target2 example.com --limit 200 \
  --order-by "keyword_data.keyword_info.search_volume,desc"
```

Filter intersection results for keywords where the competitor ranks and the user doesn't. Tag these as "gap" keywords.

**Save results** to `workspace/seo/competitor-gaps/{competitor}.json` for reuse by seo-team-the-general.

API cost: 1–2 calls per competitor (up to 5 competitors).

### Path D: User-Provided Keywords

Pass directly to EXPAND or ENRICH depending on whether the user wants expansion.

### Seed Output

Deduplicated list tagged with source:

```json
[
  {
    "keyword": "home brewing kit",
    "source": "brainstorm",
    "angle": "solution"
  },
  {
    "keyword": "ipa recipe home brew",
    "source": "gap",
    "competitor": "competitor1.com"
  }
]
```

---

## Stage 2: EXPAND

**Goal:** Turn 50–100 seeds into 200–1,000 unique candidates.

### Method 1: Related keywords (primary engine)

```bash
seocli keywords-data google-ads keywords-for-keywords live \
  --keywords "seed1" --keywords "seed2" --keywords "seed3" \
  --sort-by search_volume
```

Batch up to ~10 keywords per call. Returns Google Ads keyword suggestions.

### Method 2: Category-level ideas

```bash
seocli dataforseo-labs google keyword-ideas \
  --keywords "seed1" --keywords "seed2" \
  --include-serp-info --include-clickstream-data --limit 500
```

Broader discovery. `--include-serp-info` captures SERP feature data early (reuse in CLUSTER).

### Method 3: SERP mining (5–10 representative seeds)

```bash
seocli serp google organic live \
  --keyword "seed keyword" --depth 10 --device desktop
```

Extract People Also Ask questions and related searches as additional candidates. Note SERP features for later use.

### Method 4: Programmatic long-tail (zero API cost)

For every core seed, generate variants by prepending question prefixes ("what is", "how to", "why does") and appending commercial modifiers, specificity terms, temporal modifiers, and format terms.

### Deduplication

1. Lowercase all keywords
2. Remove exact duplicates
3. Normalize near-duplicates (whitespace, hyphens, compound forms) — keep the form with highest volume if known
4. Remove obviously irrelevant results (seed topic words absent AND not from competitor gap data)

API cost: ~10–20 calls total.

---

## Stage 3: ENRICH

**Goal:** Add volume, difficulty, CPC, intent, and funnel-stage data to every keyword.

### Volume and CPC

```bash
# Up to 700 keywords per call
seocli keywords-data google-ads search-volume live \
  --keywords "kw1" --keywords "kw2" ... --sort-by search_volume
```

Extract per keyword: `search_volume`, `cpc`, `competition`, `competition_level`, `monthly_searches` (12-month array).

### Keyword Difficulty

```bash
# Up to 1,000 keywords per call
seocli dataforseo-labs google bulk-keyword-difficulty \
  --keywords "kw1" --keywords "kw2" ...
```

Returns `keyword_difficulty` (0–100). Note: DataForSEO KD runs higher than Ahrefs/Semrush — a "30" here ≈ "20" in Ahrefs.

### Intent, Funnel Stage, Trends, and Zero-Click Risk

For detailed classification rules, scoring formulas, and trend detection logic, see [reference/scoring-and-classification.md](reference/scoring-and-classification.md).

**Summary:**

- **Intent:** Rule-based first (questions → informational, "buy/price" → transactional, "best/top" → commercial, brands → navigational). Verify ambiguous cases against SERP data.
- **Funnel stage:** Informational → ToFu, Commercial → MoFu, Transactional → BoFu, Navigational → navigational.
- **Trends:** Compare last 3 months avg to previous 3 months avg from `monthly_searches`. >20% change → rising/declining.
- **Zero-click risk:** Flag keywords where AI Overviews or featured snippets fully answer the query. Apply 0.5× volume multiplier in opportunity scoring.

### Post-Enrichment Filtering

Remove only: zero-volume keywords with no trend signal (unless gap keywords the user wants). Do NOT aggressively filter — low-volume keywords can be valuable as cluster supporting content.

API cost: 2–4 calls for a typical 500-keyword list.

---

## Stage 4: CLUSTER

**Goal:** Group keywords into content clusters — sets of keywords a single page should target. Prevents cannibalization and maximizes per-page keyword coverage.

For the full clustering algorithm (SERP similarity method, completeness scoring formula, content format inference table), see [reference/clustering-guide.md](reference/clustering-guide.md).

### Algorithm Summary

1. **Select candidates:** Sort by volume descending, take top 30–50 as cluster candidates
2. **Tentative assignment:** Assign remaining keywords to nearest candidate by textual similarity
3. **SERP similarity check:** For candidate pairs with textual overlap, pull SERPs and compare top-10 URLs
   - 3+ shared URLs → same cluster
   - 2 shared URLs → likely same cluster if textually similar
   - 0–1 shared → different clusters
4. **Merge and assign:** Merge overlapping candidates, assign remaining keywords to clusters

### Cluster Metadata

Each cluster gets: pillar keyword (highest volume), supporting keywords, total volume, average difficulty, dominant intent/funnel stage, recommended content format (inferred from SERP), SERP features, keyword count, and a completeness score (0–1).

**Completeness status flags:**

- `needs_expansion` (<3 keywords)
- `ready_for_content` (5+ keywords, mixed difficulty, good volume)
- `monitor` (between states)

API cost: 20–50 SERP calls. Control cost by capping at 50 SERP calls, reusing cached SERP data from Stage 2, and stopping pairwise comparison when clusters stabilize.

---

## Stage 5: PRIORITIZE

**Goal:** Score and rank clusters so the user knows what to work on first.

### Opportunity Score

```
Opportunity = (total_cluster_volume × intent_weight × zero_click_adj) / (avg_difficulty × pkd_ratio) × relevance
```

| Component             | Values                                                                     |
| --------------------- | -------------------------------------------------------------------------- |
| Intent weights        | Informational: 1.0, Commercial: 2.0, Transactional: 3.0, Navigational: 0.5 |
| Zero-click adjustment | 0.5 if AI Overview fully answers, else 1.0                                 |
| PKD ratio             | `user_DR / avg_DR_of_top_10` if domain authority known, else 1.0           |
| Relevance             | Default 1.0. Ask user if they have priority topics to boost.               |

For full formula details including Personal Keyword Difficulty, see [reference/scoring-and-classification.md](reference/scoring-and-classification.md).

### Tier Assignment

| Tier               | Criteria                   | Timeline     |
| ------------------ | -------------------------- | ------------ |
| **Quick Wins**     | KD < 30, volume > 100/mo   | Weeks        |
| **Growth**         | KD 30–60, volume > 500/mo  | 1–3 months   |
| **Long-term Bets** | KD > 60, volume > 2,000/mo | 6+ months    |
| **Low Priority**   | KD > 60, volume < 500/mo   | Deprioritize |

### Special Flags

For each top-20 cluster, check and flag:

- **AI Overview opportunity:** Run `seocli serp google ai-mode live --keyword "[pillar]"` — note format and cited sources
- **Video opportunity:** Video results in SERP top 10
- **Featured snippet:** Structure content for snippet capture
- **PAA presence:** Include FAQ section addressing those questions
- **Existing ranking:** Cross-reference user's domain rankings via `seocli dataforseo-labs google ranked-keywords --target example.com --limit 500`
  - Positions 1–3: Defend
  - Positions 4–20: Optimize (high-ROI striking distance)
  - Positions 21+: Evaluate for rewrite
  - Not ranking: Create new content

API cost: 10–25 calls.

---

## Stage 6: MAP

**Goal:** Produce the final keyword map — the actionable output.

### Keyword Map Table

| Cluster | Pillar KW | Supporting KWs | Intent | Total Vol | Avg KD | Tier | Format | Target URL | Action | Score | Flags |
| ------- | --------- | -------------- | ------ | --------- | ------ | ---- | ------ | ---------- | ------ | ----- | ----- |

- **Target URL:** Existing page on user's domain ranking for cluster keywords. "—" if none.
- **Action:** "optimize" (page exists), "create" (no page), "consolidate" (multiple pages compete = cannibalization)
- **Flags:** AI Overview, Video, Snippet, PAA, Shopping, Seasonal, Rising, Gap

### Supporting Outputs

1. **Keyword Universe Spreadsheet** — every keyword with all enrichment data, flat
2. **Cluster Architecture** — visual tree showing pillar → cluster → sub-cluster relationships
3. **Opportunity Brief** — top 10 Quick Wins, top 10 Growth, top 5 Long-term, top 5 AI Overview opportunities
4. **Competitor Gap Report** (if competitors analyzed) — gap keywords with volume, KD, competitor ranking URL, user status
5. **Content Calendar Suggestion** — Week 1–2: Quick wins, Week 3–4: First growth piece, Month 2: Growth + optimize striking-distance, Month 3+: Long-term pillar content

### Next Actions

Include explicit handoff directives:

```json
{
  "next_actions": [
    {
      "skill": "seo-team-the-writer",
      "action": "Create content for cluster C-002 (Quick Win)",
      "priority": 1
    },
    {
      "skill": "seo-team-the-doctor",
      "action": "Audit striking-distance pages for clusters C-001, C-005",
      "priority": 2
    },
    {
      "skill": "seo-team-the-general",
      "action": "Analyze competitor gaps — 30 gap keywords identified",
      "priority": 3
    }
  ]
}
```

---

## Data Persistence

All outputs persist to `workspace/seo/`:

```
workspace/seo/
├── config.yaml                          # domain, location, language, competitors
├── keyword-map.json                     # master keyword map (Stage 6 output)
├── keyword-universe.json                # all keywords with enrichment data
├── clusters.json                        # cluster definitions with metadata
├── research-runs/
│   └── YYYY-MM-DD-{topic-slug}.json    # timestamped run metadata
└── competitor-gaps/
    └── {competitor-domain}.json         # per-competitor gap analysis
```

### Incremental Updates

The keyword map is a living document. On subsequent runs:

1. Load existing `keyword-map.json`
2. Merge new keywords into existing clusters (don't create duplicates)
3. Update volume/difficulty data
4. Add new clusters for genuinely new topics
5. Preserve user annotations (relevance overrides, priority boosts)
6. Timestamp in `research-runs/`

### Cross-Skill Consumption

- **seo-team-the-writer** reads `keyword-map.json` for clusters needing content, `clusters.json` for brief data
- **seo-team-the-doctor** reads `keyword-map.json` to cross-reference pages against target keywords
- **seo-team-the-general** reads everything — keyword map, competitor gaps, cluster architecture

---

## Cost Control

| Rule               | Detail                                                                 |
| ------------------ | ---------------------------------------------------------------------- |
| Never re-research  | Check `keyword-universe.json` before expanding                         |
| Batch aggressively | search-volume: 700/call, bulk-difficulty: 1,000/call                   |
| Reuse SERP data    | Cache Stage 2 SERPs for Stage 4 clustering                             |
| Confirm large runs | If expanded list > 500 keywords, show estimated cost before enrichment |
| Cap SERP sampling  | Max 50 SERP calls for clustering; use textual similarity for remainder |

### Typical Cost

| Stage              | Calls       |
| ------------------ | ----------- |
| Seed (domain)      | 3           |
| Seed (competitors) | 2–10        |
| Expand             | 10–20       |
| Enrich             | 2–4         |
| Cluster            | 20–50       |
| Prioritize         | 10–25       |
| **Total**          | **~50–100** |

---

## Error Handling

| Error                            | Response                                                    |
| -------------------------------- | ----------------------------------------------------------- |
| API rate limit                   | Wait, retry with backoff, inform user                       |
| Keywords return 0 volume         | Keep in list, flag "low-data"                               |
| SERP returns empty               | Skip SERP clustering for that keyword, fall back to textual |
| Location/language unsupported    | Suggest nearest supported alternative                       |
| Keyword list > 2,000             | Warn about cost, suggest filtering to top 1,000 first       |
| Corrupt/missing keyword-map.json | Start fresh                                                 |
