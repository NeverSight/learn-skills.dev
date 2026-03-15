---
name: reddit
description: >-
  Monitor Reddit communities worldwide to discover niche product opportunities
  — unmet pain points, frustrated users, tool-seeking posts — from high-purchasing-power
  markets (US, UK, EU, DACH, Nordics, JP, KR, AU). Use this skill whenever the user
  mentions Reddit, product opportunities, pain point hunting, market research, niche
  discovery, subreddit monitoring, or wants to find SaaS/product ideas from real user
  discussions. Also use for /reddit commands and /loop /reddit scheduled scans.
---

# Reddit Opportunity Hunter

## Mission

Product Opportunity Hunting, NOT Lead Hunting.

- **Input:** Reddit discussions from high-purchasing-power markets
- **Output:** Actionable product opportunity reports with build assessments
- **Goal:** Surface 1-2 week MVP opportunities in USD/EUR/GBP markets
- You are scanning for *patterns of unmet need*, not individual sales leads
- Every recommendation must pass the Solo Dev Fit test before being highlighted
- Reference data lives in `references/` — subreddits, keywords, seasonal patterns

## Quick Start / First Run

1. Install dependencies: `brew install curl jq`
2. Run health check: `reddit.sh diagnose` — verifies curl, jq, network connectivity
3. The script auto-creates `.reddit/` with `reports/`, `opportunities/`, `archive/`
4. Verify `.gitignore` includes `.reddit/` — the script warns if missing
5. Review `references/subreddits.json` — confirm subreddits match the user's domain
6. Review `references/intent_keywords.json` — adjust if the user targets a specific niche
7. Configure preferences: `reddit.sh config show` — set language, industries, currency
8. First scan:
   ```bash
   reddit.sh fetch --campaign global_english --sort new --pages 1
   ```
9. Inspect the enriched JSON output, then proceed to Phase 2 (Analysis)

## Configuration

On first run, `.reddit/config.json` is auto-created with defaults. Check and customize it:

```bash
reddit.sh config show          # view current config
reddit.sh config set <key> <value>   # change a setting
reddit.sh config reset         # restore defaults
```

| Setting | Description | Default | Example |
|---------|-------------|---------|---------|
| `output_language` | Language for reports and analysis | `en` | `zh`, `ja`, `de` |
| `focus_industries` | Only surface opportunities in these industries | `[]` (all) | `["SaaS","DevTools"]` |
| `excluded_subreddits` | Skip these subreddits during scan | `[]` | `["Entrepreneur"]` |
| `score_threshold` | Minimum score to include in reports | `7` | `8` |
| `max_build_complexity` | Filter out opportunities above this level | `Heavy` | `Medium` |
| `currency_display` | Currency for revenue estimates | `USD` | `CNY`, `EUR` |

**First-run prompt:** If no `config.json` exists when the skill is triggered, ask the user:

> "This is your first time using Reddit Opportunity Hunter. Quick setup:
> 1. What language should reports be in? (default: en)
> 2. Any industries to focus on? (default: all)
> 3. What currency for revenue estimates? (default: USD)
>
> Or say 'use defaults' to skip."

Save answers via `reddit.sh config set`.

## Core Workflow

### Phase 1: Data Collection

Run `reddit.sh fetch` for each campaign defined in `references/subreddits.json`, ordered by `scan_priority`:

```bash
reddit.sh fetch --campaign global_english --sort new --pages 2
reddit.sh fetch --campaign dach_german --sort new --pages 1
reddit.sh fetch --campaign nordic_scandi --sort new --pages 1
```

Key details:
- Multi-sub merge: the script combines subreddits as `r/A+B+C/new.json` to reduce API calls
- Output is enriched JSON — jq computes `_jq_enriched` fields (intent matches, sentiment, age)
- **Do NOT re-compute** what jq already provides; read the enriched fields directly
- Rate limit budget: ~100 requests per ~260 seconds; a single fetch loop uses ~40-45
- Fetch Tier S campaigns every loop, Tier A daily, Tier B weekly

### Phase 2: Analysis (Claude)

**Before analyzing, read user config:**
- `reddit.sh config show` — check `output_language`, `focus_industries`, `score_threshold`
- Write ALL reports and analysis in the configured `output_language`
- If `focus_industries` is set, prioritize opportunities matching those industries
- If `excluded_subreddits` is set, skip posts from those subreddits
- Use `currency_display` when estimating revenue (convert from USD)
- Only include opportunities with `final_score >= score_threshold`
- Only include opportunities with complexity ≤ `max_build_complexity`

Read the enriched JSON from Phase 1. For each batch:

1. **Pain point clustering** — group similar complaints across posts and subreddits
2. **Frequency counting** — how many posts mention this pain this week?
3. **Intensity assessment** — use `intent_keywords_matched` and `negative_signals` from the enriched data
4. **Market validation signals** — look for: budget mentions, team size, `already_tried` products, willingness to pay
5. **Score each opportunity** using the scoring algorithm below
6. **Deduplicate** against `seen_posts` in `.reddit/.reddit.json`

### Phase 3: Deep Verification (score >= 8)

For opportunities scoring 8 or above:

1. Fetch comment trees: `reddit.sh comments <post_id> <subreddit>`
2. Search competitive landscape: `reddit.sh search "competitor alternative" --global`
3. Add post to `watched_threads` for ongoing monitoring
4. Optional: use WebSearch for cross-platform validation (Twitter/X, HN, G2, Capterra)

### Phase 3.5: Micro-Validation

Before promoting an opportunity to "validated":
- Suggest a landing page smoke test to the user
- Cross-platform search: Twitter/X, Hacker News, Indie Hackers for the same pain
- Search for failed attempts at similar products (important signal)
- Check Product Hunt / GitHub for recent launches in the space

### Phase 4: Report

- **Daily scan report** -> `.reddit/reports/YYYY-MM-DD-scan.md`
- **High-value opportunities** -> `.reddit/opportunities/<slug>.md`
- Use the templates defined below

## reddit.sh Reference

| Mode | Usage | Purpose |
|------|-------|---------|
| fetch | `reddit.sh fetch --campaign X --sort new --pages 2` | Fetch & enrich posts |
| comments | `reddit.sh comments <id> <sub>` | Comment tree for deep-dive |
| search | `reddit.sh search "query" [--global] [--type post\|user\|subreddit]` | Reddit search |
| discover | `reddit.sh discover <keyword> [--method keyword\|autocomplete]` | Find new subreddits |
| profile | `reddit.sh profile <user> [--enrich]` | User history analysis |
| crosspost | `reddit.sh crosspost [--campaign X]` | Cross-poster detection |
| stickied | `reddit.sh stickied [subreddit]` | Stickied post mining |
| firehose | `reddit.sh firehose [sub1+sub2]` | Real-time comment stream |
| duplicates | `reddit.sh duplicates <post_id>` | Link propagation tracking |
| wiki | `reddit.sh wiki <sub> [page]` | Community wiki content |
| stats | `reddit.sh stats` | Database / state statistics |
| export | `reddit.sh export [--format csv\|json]` | CRM-ready export |
| cleanup | `reddit.sh cleanup` | Purge expired data |
| diagnose | `reddit.sh diagnose` | Health check (jq, dirs, state) |
| config | `reddit.sh config [show\|set <key> <val>\|reset]` | User preferences |

**Helper functions** (called during loop cycles, not directly by user):
- `watch_check` — check watched threads for new comments since last check
- `competitor_search <campaign>` — expand competitor query templates from config
- `update_subreddit_quality <sub> <scanned> [opportunities]` — track hit rates per subreddit

## Scoring Algorithm

```
raw_score = intensity      * 0.20
          + competitive_gap * 0.20
          + build_feasibility * 0.20
          + market_value   * 0.20
          + frequency      * 0.15
          + timeliness     * 0.05
```

Each dimension is scored 1-10 individually.

**Adjustments:**
```
adjusted = raw_score
  + cross_market_bonus   (same pain in 3+ Tier S markets -> +1.5)
  + seasonal_bonus       (matches upcoming seasonal pattern -> +1.0; just passed -> -1.0)
  - false_positive_penalty (see below)

final_score = clamp(adjusted, 1, 10)
```

**Weekly decay:** if no new mentions this week: `final_score *= 0.88`

**Market tier bonuses** (applied to `market_value` dimension, not final score):
- Tier S (US, UK, DE, FR, NL, JP, AU, KR, Nordics): +3
- Tier A (IN, BR, SEA, LATAM, PL, CZ): +1
- Tier B (Africa, South Asia, rest): +0

**Thresholds:**
- >= 8: Deep verification (Phase 3) + highlight in report
- >= 7: Show in daily report under New Opportunities
- < 7: Aggregate only under Trending Pain Points

**False positive penalties:**
- Single user mention, no corroboration: **-3**
- One-time complaint (user has no topic history): **-2**
- Strong open-source alternative (>5k GitHub stars): **-2**
- Requires enterprise sales process: mark as "not solo dev fit", do not penalize score but flag

## Intent Tiers

Reference `references/intent_keywords.json` for the full keyword list. You classify intent tier from context — jq only provides raw keyword matches.

| Tier | Signal | Examples |
|------|--------|---------|
| 1 | Direct purchase intent | "willing to pay", "budget for", "take my money" |
| 2 | Active solution seeking | "looking for a tool", "switching from", "need alternative" |
| 3 | Pain expression | "frustrated with", "too expensive", "waste of time" |
| 4 | Research | "what do you use for", "best practices", "recommendations" |
| 5 | Indirect signals | Domain discussions implying unmet need |

## Solo Dev Fit Assessment

Evaluate independently of opportunity score. All must be true for a pass:

- Build time < 2 weeks for MVP
- No ongoing compliance burden (HIPAA, SOC2, etc.)
- Self-serve distribution (no enterprise sales cycle)
- Subscription or usage-based pricing model viable
- Known tech stack (no deep domain R&D)
- No network effects required for initial value

## Opportunity Report Template

```markdown
## Product Opportunity: [Name]

**Score:** X.X/10 | **Intent Tier:** N | **Solo Dev Fit:** Yes/No

### Pain Point
[2-3 sentence summary of the unmet need]

### Market Evidence
- **Frequency:** N posts in last 7 days across M subreddits
- **Intensity:** [low/medium/high] — key signals: ...
- **Geography:** [primary markets]
- **Target user:** [persona]
- **Budget signals:** [quotes or indicators]

### Competitive Landscape
- **Existing paid tools:** [list with pricing]
- **Open-source alternatives:** [list with GitHub stars]
- **Why they fail:** [gap analysis]
- **Recent launches:** [last 6 months]

### Build Assessment
- **Complexity:** [low/medium/high]
- **MVP scope:** [3-5 core features]
- **Build time:** [estimate]
- **Tech stack:** [recommendation]
- **Technical moat:** [if any]
- **Solo Dev Fit:** [Yes/No + reasoning]

### Revenue Model
- **Pricing anchor:** [competitor pricing context]
- **Suggested tiers:** [USD/EUR with PPP notes]
- **Distribution:** [channels]
- **Market size estimate:** [TAM/SAM]
- **Revenue potential:** [12-month projection]
- **CAC / Payback:** [estimate]
- **Churn risk:** [assessment]

### Cross-Market Signal
[Evidence from other markets/platforms]

### Source Posts
- [post title](url) — r/subreddit — N upvotes, M comments — YYYY-MM-DD
```

## Daily Report Template

```markdown
# Reddit Opportunity Scan — YYYY-MM-DD

## New Opportunities (score >= 7)
[Opportunity cards with score, pain summary, top source post]

## Trending Pain Points
[Clusters below threshold but gaining frequency]

## Time-Sensitive (< 2h old, high intent)
[Posts needing immediate attention — Tier 1-2 intent, fresh]

## Scan Stats
- Subreddits scanned: N
- Posts analyzed: N
- New opportunities: N
- Watched threads updated: N
- API calls used: N / 100
```

## Loop Integration

Trigger with:
```
/loop 30m /reddit
```

Each cycle:
1. Read config: `reddit.sh config show` — load user preferences
2. Read `references/subreddits.json` (hot reload — picks up edits between cycles)
3. Fetch per `scan_priority`: Tier S every loop, Tier A daily, Tier B weekly
4. Deduplicate against `seen_posts` in `.reddit/.reddit.json`
5. `watch_check` for watched threads with new activity
6. `competitor_search` for configured campaigns
7. Analyze, score, cluster new posts
8. Output incremental report (append to daily scan file)
9. Score >= 8 -> alert: `OPPORTUNITY: [title] (score X.X)`
10. `update_subreddit_quality` with hit rates

**Scheduled reports:**
- Weekly summary: trigger on Sundays (or first loop after Sunday midnight)
- Monthly summary: last day of month (or first loop after)
- If a scheduled report was missed, generate it on next run

## State Management

`.reddit/.reddit.json` tracks:

| Key | Purpose | TTL |
|-----|---------|-----|
| `seen_posts` | Deduplication | 30 days |
| `watched_threads` | Monitor for new comments | 7 days default |
| `opportunities` | Lifecycle tracking | Permanent |
| `products_seen` | Known tools/competitors | Permanent |
| `influencers` | High-value Reddit users | Permanent |
| `community_overlap` | Cross-sub posting patterns | 30 days |
| `subreddit_quality` | Hit rate per subreddit | Permanent |

Opportunity lifecycle: `discovered -> investigating -> validated -> building -> launched -> revenue -> archived`

## Safety

- **Public data only** — no PII beyond Reddit usernames
- **Rate limit compliant** — respect the ~100 req/260s budget
- `.reddit/` must be in `.gitignore` — never commit user data
- Reply drafts always marked **[REVIEW BEFORE POSTING]**
- Suggest max 5 replies per day to avoid spam patterns

## Skill Integration

Related skills for downstream workflows:
- **content-strategy** — turn validated pain points into content calendars
- **copywriting** — turn opportunities into landing page copy
- **competitor-alternatives** — deep competitive analysis
- **cold-email** — draft outreach / DM templates
- **social-content** — repurpose Reddit insights for social posts
