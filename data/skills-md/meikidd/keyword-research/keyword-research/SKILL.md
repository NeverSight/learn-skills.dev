---
name: keyword-research
description: Keyword research and analysis skill for any website. Performs systematic keyword discovery, competitive gap analysis, intent classification, difficulty scoring, and priority ranking. Use when the user wants to find new keyword opportunities, analyze which keywords competitors rank for, audit existing keyword coverage, build a keyword map, or plan content around search demand. Works for any domain, language, or niche.
version: 1.0.1
---

# Keyword Research Skill

Must load the web-access skill and follow its instructions.

## Startup workflow

### Step 1: Load the domain profile

Extract the domain from the URL the user provides (e.g. `example.com`), then read the profile file:

```
~/.claude/skills/keyword-research/data/{domain}.json
```

- **Profile exists** → Load it directly; skip questions for fields already known; only ask for "focus of this analysis"
- **Profile missing** → Create one; ask for all required fields in order, then save

If the user did not provide a URL, ask for the target site URL first, extract the domain, then check for a profile.

### Step 2: Fill in missing fields

Only ask for fields not yet stored in the profile:

| Field | Description | First run | Later runs |
|-----|------|---------|-----|
| `url` | Full site URL | Required | Skip if known |
| `business` | One-line business description | Required | Skip if known |
| `region` | Target region (e.g. Singapore) | Required | Skip if known |
| `language` | Target language(s) (e.g. English, Chinese) | Required | Skip if known |
| `competitors` | Competitor site list | Optional | Skip if known; user can update anytime |
| `tools.gsc` | GSC access | Ask first time GSC is needed | Skip if known |
| `tools.ahrefs` | Ahrefs account tier | Ask first time | Skip if known; `"none"` skips all Ahrefs steps |
| `tools.semrush` | Semrush account tier | Ask first time | Skip if known; `"none"` skips all Semrush steps |
| `tools.gkp` | Has Google Ads account (GKP) | Ask first time | If `false`, use Ahrefs free keyword tools instead |
| `focus` | Focus of this analysis | **Ask every time** (tasks vary) | Ask every time |

### Step 3: Save or update the profile

After each run (or whenever new info is added), write back to the profile file immediately so the next session starts with complete data.

Profile format (JSON):

```json
{
  "url": "https://www.sunriselink.sg",
  "business": "MOM-licensed domestic helper agency in Singapore, helping families hire maids from Indonesia, Myanmar, Philippines",
  "region": "Singapore",
  "language": ["English", "Chinese"],
  "competitors": ["nationmaid.com.sg", "universal.com.sg", "firstmaid.com.sg"],
  "tools": {
    "gsc": true,
    "ahrefs": "none",
    "semrush": "free",
    "gkp": true
  },
  "updated": "2026-04-15 10:05:23"
}
```

Valid values for `tools.ahrefs` and `tools.semrush`:
- `"paid"` — Paid account; full feature access
- `"free"` — Free account; limited features (see skip rules)
- `"none"` — No account; skip all steps for that tool

If the profile directory does not exist, create it first: `mkdir -p ~/.claude/skills/keyword-research/data/`

### Tool skip rules

**Ahrefs**:

| Account tier | Step 2B behavior | Step 3 behavior |
|---------|------------|-----------|
| `"paid"` | Use Site Explorer + Content Gap (full competitor gap analysis) | Use Keywords Explorer |
| `"free"` | Skip Site Explorer/Content Gap; use `site:` search to infer competitor content structure | Use ahrefs.com/keyword-generator (no login) |
| `"none"` | Skip all Ahrefs; do not open any Ahrefs page | Same as left |

**Semrush**:

| Account tier | Step 2B behavior | Step 3 behavior |
|---------|------------|-----------|
| `"paid"` | Use Keyword Gap (full competitor gap analysis) | Use Keyword Magic Tool (unlimited queries) |
| `"free"` | Skip Keyword Gap; use Keyword Magic Tool (10 queries/day cap—watch usage) | Use Keyword Magic Tool (mind the cap) |
| `"none"` | Skip all Semrush; do not open any Semrush page | Same as left |

**Other tools**:
- `tools.gkp: false` → In Step 3D use Ahrefs free keyword tools instead; do not push signing up for Ads
- `tools.gsc: false` → Skip Step 1 entirely; start from Step 2

The user may say at any time e.g. "I upgraded Ahrefs to paid" — update `tools.ahrefs` from `"free"` to `"paid"` and save.

---

## Four-step analysis framework

### Step 1 — Baseline from existing queries (GSC)

**Goal**: Find queries that already get impressions but are underutilized—the fastest wins.

**Actions (via CDP automation)**:

Navigate directly to this URL (replace domain) to enable the 28-day window and Position column in one step:

```
https://search.google.com/search-console/performance/search-analytics?resource_id=sc-domain%3A{domain}&num_of_days=28&metrics=CLICKS%2CIMPRESSIONS%2CCTR%2CPOSITION
```

> ⚠️ **Use 28 days, not the default 3 months**: If the site has not been SEO-optimized for long, a 3-month average mixes in a lot of pre-optimization low-rank data and skews conclusions badly (in practice ~4× difference).

Then set rows-per-page to 500 and extract all data in one pass (steps in `references/gsc-operations.md`).

**Priority filters**:
- Impressions ≥ 30 and CTR 0% → **Meta fix opportunity** (good rank but no clicks—title/description issue)
- Average position 11–20 → **Page-one push opportunity** (page two—close enough to optimize into the top 10)
- Impressions ≥ 30 and position > 20 → **Needs new page or deeper content**
- Queries absent from GSC → Not covered at all; see Step 2

**Hit a login wall**: Tell the user to log into GSC in Chrome with a property-verified account, then continue. If there is no GSC data (new site), skip to Step 2.

**Note**: GSC only shows queries the site has already appeared for. Fully uncovered queries are invisible here; discover them in Steps 2–3.

**CDP playbook**: See `references/gsc-operations.md`.

---

### Step 2 — Competitor keyword gap

**Goal**: Find queries competitors rank for where the target site has no presence—the highest-value uncovered opportunities.

**A. Identify competitors** (if the user did not provide any):
- Google 2–3 core business terms for the target site
- Record domains in the top 5 organic SERP results → these are real SEO competitors (not necessarily who the user *thinks* competes)

**B. Competitor analysis (paid Ahrefs/Semrush)**:
- Ahrefs: https://ahrefs.com/site-explorer → enter competitor domain → Organic Keywords
- Semrush: https://www.semrush.com/analytics/organic/overview → enter competitor domain
- Use Content Gap / Keyword Gap: competitor vs target site → queries competitors have and the target lacks

**B. Competitor analysis (free alternatives)**:
- Ahrefs free keyword tool: https://ahrefs.com/keyword-generator (no signup, 100 keywords per run)
- Semrush free tier: https://www.semrush.com/features/keyword-magic-tool/ (10/day)
- For each competitor domain search `site:competitor.com` → infer content structure and topic coverage
- Google competitor brand terms; read SERP titles and descriptions → infer keyword strategy

**Hit a paywall**: Ask if the user has an account; if not, use the free path or ask for screenshots/copied data.

---

### Step 3 — Keyword expansion and discovery

**Goal**: From seed terms, systematically mine long-tail, question, and local variants.

**A. Google Autocomplete** (free, closest to real search behavior):
- For each core term, type these patterns in Google and capture all suggestions:
  - `[term]`, `[term] how`, `[term] what`, `[term] why`
  - `best [term]`, `[term] vs`, `[term] cost`, `[term] near me`
  - Mid-query suggestions: add a space mid-phrase, e.g. `maid _ singapore`

**B. AnswerThePublic (3 free searches/day)**:
- Open https://answerthepublic.com
- Enter a core term; pick language/region
- Export Questions and Prepositions → use for FAQ and blog ideas

**C. AlsoAsked (3 free runs)**:
- Open https://alsoasked.com
- Enter a core term → Google PAA question tree
- PAA queries are SERP-feature opportunities (People Also Ask box)

**D. Google Keyword Planner (free; needs Google Ads)**:
- Open https://ads.google.com/home/tools/keyword-planner/
- "Discover new keywords" → enter seeds or target URL
- Filter by region; review volume bands and competition
- Note: Without active ads, volume shows as wide bands (e.g. 1K–10K); accounts with spend history get tighter numbers

**Google Ads login required**: Ads accounts are free to create; no need to run ads. Guide signup if needed, then use Planner.

---

### Step 4 — Intent classification and prioritization

Classify collected queries by intent; rank by difficulty and conversion potential.

**Intent taxonomy** (every query gets one code):

| Code | Intent type | Typical signals | Content angle |
|-----|---------|----------|---------|
| I | Informational | how/what/why/guide/tips | Blog posts, FAQ |
| C | Commercial investigation | best/vs/compare/review/top | Comparison pages, listicles |
| T | Transactional | buy/hire/contact/book/price | Service pages, landing pages |
| N | Navigational | brand, site name | Brand defense, homepage |

**Priority score**:

```
Priority score = intent fit (1–5) × conversion potential (1–5) ÷ competition difficulty (1–5)
```

- **Intent fit**: How well the query intent matches the business (perfect = 5, weak = 1)
- **Conversion potential**: T=5, C=4, I=2–3, N=1
- **Competition (KD)**: 0–20=1, 21–40=2, 41–60=3, 61–80=4, 81–100=5

Prioritize: queries with score ≥ 10.

Methodology and sources: `references/methodology.md`.  
Full tool playbook: `references/tools.md`.  
GSC CDP guide (including pitfalls): `references/gsc-operations.md`.

---

## Output format

```markdown
## Keyword research report — [Site name]
Date: YYYY-MM-DD | Region: XX | Language(s): XX

### 1. GSC optimization opportunities (existing queries)
| Keyword | Current rank | Impressions | CTR | Recommendation |
|--------|---------|-------|-------|---------|

### 2. Competitor gap keywords (highest value)
| Keyword | Intent | Monthly volume | KD | Competitor has / we lack | Priority score |
|--------|-----|---------|-----|--------------|---------|

### 3. Uncovered long-tail keywords
| Keyword | Intent | Monthly volume | KD | Content recommendation |
|--------|-----|---------|-----|-----------|

### 4. Priority action list (Top 10)
Sort by priority score descending; each row: suggested action (new page / optimize existing / blog) + suggested target URL
```
