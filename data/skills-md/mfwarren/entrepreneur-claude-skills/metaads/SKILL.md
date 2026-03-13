---
name: metaads
description: |
  Meta Media Buyer — publish, manage, and analyze Meta (Facebook/Instagram) ad campaigns
  via the Marketing API. Includes guided setup for first-time users.

  USE WHEN user says "meta ads", "facebook ads", "instagram ads", "publish ads",
  "create campaign", "launch campaign", "ad performance", "ROAS", "which ad is winning",
  "ad spend", "campaign metrics", "pause campaign", "resume campaign",
  "upload ad images", "ad set performance", "creative performance",
  "set up meta ads", "connect meta ads", "meta ads setup",
  or needs to publish, manage, or analyze paid Meta advertising campaigns.
---

## Workflow Routing (SYSTEM PROMPT)

**CRITICAL: Route to the correct workflow based on user intent.**

**When user needs to set up or configure Meta Ads API access:**
Examples: "set up meta ads", "connect meta ads", "configure facebook ads", "my token expired", "meta ads setup", credential errors from --check
-> **READ:** ~/.claude/skills/MetaAds/workflows/Setup.md
-> **EXECUTE:** Walk user through complete setup (Business Manager, App, token, .env)

**When user wants to publish, create, or launch a campaign:**
Examples: "publish ads", "create campaign", "launch campaign", "upload ad images", "publish meta ads", "push this campaign to Meta", "create ad set"
-> **READ:** ~/.claude/skills/MetaAds/workflows/PublishCampaign.md
-> **EXECUTE:** Campaign publishing workflow
-> If credentials fail, route to Setup.md first

**When user wants to check performance, metrics, or analyze results:**
Examples: "check meta ad performance", "ROAS", "which ad is winning", "ad spend", "campaign metrics", "how are my ads doing", "audience breakdown", "creative performance"
-> **READ:** ~/.claude/skills/MetaAds/workflows/AnalyzePerformance.md
-> **EXECUTE:** Performance analysis workflow
-> If credentials fail, route to Setup.md first

**When user wants to manage campaigns (pause/resume/status):**
Examples: "pause campaign", "resume campaign", "campaign status", "list campaigns"
-> Use `uv run ~/.claude/skills/MetaAds/tools/Publish.py` directly with --pause, --resume, --status, or --list

---

## When to Activate This Skill

### Setup & Configuration (Category 0)
- "set up meta ads", "connect meta ads API", "configure facebook ads"
- "meta ads setup", "how do I connect my ad account"
- "my token expired", "token error", "can't access meta ads"
- "refresh my meta token", "renew access token"
- Any credential error from --check

### Campaign Publishing (Category 1)
- "publish ads", "create campaign", "launch campaign"
- "push this to Meta", "set up the campaign", "upload ad images"
- "publish meta ads", "create ad set", "build the campaign"
- "publish this campaign config", "go live with the ads"

### Performance Analysis (Category 2)
- "check meta ad performance", "how are my ads doing"
- "ROAS", "return on ad spend", "ad spend", "ad metrics"
- "which ad is winning", "best performing ad"
- "campaign metrics", "ad set performance", "creative performance"
- "audience breakdown", "age/gender breakdown"
- "CTR", "CPC", "CPM", "CPA", "cost per acquisition"

### Campaign Management (Category 3)
- "pause campaign", "resume campaign", "activate campaign"
- "campaign status", "list campaigns", "show my campaigns"

---

## Core Capabilities

**Guided Setup:**
- Complete walkthrough: Business Manager -> Developer App -> Token -> .env
- Two token paths: System User (never expires) or User Token (60-day, with automated refresh)
- Token exchange automation (agent runs the curl command)
- Pixel setup guidance for conversion tracking
- Error diagnosis with specific fixes for every common failure

**Campaign Publishing:**
- Upload images from local directories to Meta
- Create full campaign hierarchy (campaign -> ad set -> creative -> ad)
- Advantage+ flexible creative with multiple images/texts/headlines
- All objects created PAUSED for manual review
- JSON config-driven for reproducible campaigns

**Performance Analytics:**
- Account-level summary with DTC benchmarks (CTR, CPM, CPA, ROAS)
- Campaign, ad set, and ad-level metrics
- Daily trend analysis for campaign deep dives
- Audience breakdowns (age, gender, platform, device)
- Data sync to Analytics/meta-ads/ for cross-channel analysis
- CSV export for spreadsheet analysis

**Campaign Management:**
- List all campaigns with status
- View campaign hierarchy (campaign -> ad sets -> ads)
- Pause/resume campaigns

---

## Scripts

| Script | Purpose |
|--------|---------|
| `tools/Publish.py` | Campaign creation, image upload, pause/resume |
| `tools/Analytics.py` | Performance metrics, breakdowns, sync, export |

Both scripts use PEP 723 inline dependencies — just run with `uv run` directly from the skill directory. No install or copy step needed.

### Usage

Run scripts directly from the skill directory. They load `.env` from the current working directory (`Path.cwd()`), so run them from your project root:

```bash
# From your project root (where .env lives):
uv run ~/.claude/skills/MetaAds/tools/Publish.py --check
uv run ~/.claude/skills/MetaAds/tools/Analytics.py --summary
```

**Prerequisites:** `uv` must be installed. If not: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Environment Variables (`.env`):**
| Variable | Required | Description |
|----------|----------|-------------|
| `META_ADS_ACCESS_TOKEN` | Yes | System User or long-lived User token |
| `META_ADS_ACCOUNT_ID` | Yes | Ad account ID with `act_` prefix |
| `FACEBOOK_APP_ID` | For refresh | App ID for token exchange |
| `FACEBOOK_APP_SECRET` | For refresh | App Secret for token exchange |

---

## Campaign Objective Reference

Use these objectives in campaign configs:

| Objective | When to Use | Optimization Goal |
|-----------|-------------|-------------------|
| `OUTCOME_SALES` | DTC purchases, Shopify conversions | `OFFSITE_CONVERSIONS` |
| `OUTCOME_LEADS` | Lead gen, email signups, quiz funnels | `LEAD_GENERATION` |
| `OUTCOME_TRAFFIC` | Landing page visits, blog traffic | `LINK_CLICKS` |
| `OUTCOME_AWARENESS` | Brand awareness, video views | `REACH` or `IMPRESSIONS` |
| `OUTCOME_ENGAGEMENT` | Post engagement, page likes | `POST_ENGAGEMENT` |

---

## Campaign Config Template

Generic template for any DTC brand:

```json
{
  "campaign": {
    "name": "campaign-name-month-year",
    "objective": "OUTCOME_SALES"
  },
  "adsets": [
    {
      "name": "Broad-25-54-US",
      "daily_budget": 5000,
      "targeting": {
        "age_min": 25,
        "age_max": 54,
        "genders": [0],
        "geo_locations": {"countries": ["US"]},
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "video_feeds", "story", "reels"],
        "instagram_positions": ["stream", "story", "reels", "explore"]
      },
      "optimization_goal": "OFFSITE_CONVERSIONS",
      "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
    }
  ],
  "creative": {
    "images_directory": "./path/to/ad-images/",
    "primary_texts": [
      "Primary text variant 1 — lead with the hook or pain point",
      "Primary text variant 2 — lead with the benefit or social proof",
      "Primary text variant 3 — lead with a comparison or price anchor"
    ],
    "headlines": [
      "Short Punchy Headline",
      "Benefit-Driven Headline",
      "Price/Value Headline"
    ],
    "descriptions": [
      "Supporting description with key differentiator"
    ],
    "link_url": "https://yoursite.com/landing-page",
    "url_parameters": "utm_source=meta&utm_medium=paid-social&utm_campaign=campaign-name&utm_content={{ad.name}}",
    "call_to_action_type": "SHOP_NOW"
  }
}
```

**Config notes:**
- `daily_budget` is in **cents** (5000 = $50.00/day)
- `genders`: 0 = all, 1 = male, 2 = female
- `{{ad.name}}` is a Meta dynamic parameter — auto-fills with the ad name
- `call_to_action_type` options: `SHOP_NOW`, `LEARN_MORE`, `SIGN_UP`, `GET_OFFER`, `ORDER_NOW`, `SUBSCRIBE`, `BOOK_NOW`

---

## DTC Benchmark Reference

| Metric | Good | OK | Needs Work | What It Means |
|--------|------|----|------------|---------------|
| CTR | >1.5% | 1-1.5% | <1% | % of impressions that click. Low = creative isn't resonating |
| CPM | <$15 | $15-25 | >$25 | Cost per 1000 impressions. High = competitive auction or narrow audience |
| CPC | <$1 | $1-2 | >$2 | Cost per click. High = low CTR driving up costs |
| CPA | <$30 | $30-50 | >$50 | Cost per purchase. The ultimate efficiency metric |
| ROAS | >3x | 2-3x | <2x | Revenue per $1 spent. Below 2x usually means losing money after COGS |
| Frequency | 1-3 | 3-5 | >5 | Avg times each person saw the ad. High = ad fatigue |
| Hook Rate | >25% | 15-25% | <15% | % who watch first 3 sec of video. Low = weak opening |
| Hold Rate | >10% | 5-10% | <5% | % who watch 15+ sec. Low = content doesn't sustain interest |

---

## Optimization Playbook

**Scaling winners:**
- Increase budget by 20-30% every 2-3 days (not all at once — resets learning)
- Duplicate winning ad sets with new audiences
- Create lookalike audiences from purchasers

**Fixing underperformers:**
- CTR < 1%: Test new hooks/images — the creative isn't stopping thumbs
- CTR > 2% but no purchases: Landing page problem, not ad problem
- CPA too high: Narrow targeting or test lower-funnel audiences
- Frequency > 4: Rotate in fresh creative
- No spend after 48 hours: Switch optimization to Link Clicks temporarily, then back to Conversions

**Meta learning phase:**
- Each ad set needs ~50 conversions in 7 days to exit learning
- Don't edit during learning (resets the clock)
- If budget is too low for 50 conversions/week, optimize for a higher-funnel event (ATC instead of Purchase)

---

## Examples

**Example 1: First-time Setup**

User: "I want to set up Meta ads for my store"

Skill Response:
1. Routes to Setup.md workflow
2. Checks if .env exists, if Business Manager is set up
3. Walks through Developer App creation
4. Helps generate and exchange token
5. Configures .env
6. Verifies with --check

**Example 2: Publish a Campaign**

User: "Create a campaign for our new product launch"

Skill Response:
1. Routes to PublishCampaign.md workflow
2. Checks credentials (routes to Setup if missing)
3. Asks about images, copy, targeting, budget
4. Builds config JSON
5. Publishes (all PAUSED)
6. Reports campaign ID and review checklist

**Example 3: Check Performance**

User: "How are my Meta ads doing?"

Skill Response:
1. Routes to AnalyzePerformance.md workflow
2. Runs --summary for account overview
3. Compares against DTC benchmarks
4. Identifies winners and losers
5. Provides specific optimization recommendations

**Example 4: Token Expired**

User: "My meta ads token isn't working" / agent sees error code 190

Skill Response:
1. Routes to Setup.md Part 6 (Token Refresh)
2. Checks for FACEBOOK_APP_ID and FACEBOOK_APP_SECRET in .env
3. Tells user to generate new short-lived token in Graph API Explorer
4. Runs the exchange curl command
5. Updates .env with new long-lived token
6. Verifies with --check

**Example 5: Manage Campaign**

User: "Pause campaign 12345678"

Skill Response:
1. Runs `uv run ~/.claude/skills/MetaAds/tools/Publish.py --pause 12345678`
2. Confirms campaign is paused

---

**Last Updated:** 2026-02-07
