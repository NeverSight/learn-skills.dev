---
name: account-structure-review
description: Google and Meta paid media account structure evaluation. Audits campaign/ad set architecture against conversion volume minimums, budget thresholds, and targeting overlap. Identifies over-segmentation, under-segmentation, budget fragmentation, and structural anti-patterns blocking algorithmic learning. Provides consolidation roadmaps with migration plans. Use when inheriting accounts, quarterly health checks, or before scaling budgets.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: paid-media
  domain: cross-platform
  updated: 2026-03-11
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Account Structure Review — Google + Meta

Expert-level guidance for evaluating paid media account structure against goals, budget, and conversion volume thresholds. Identifies structural anti-patterns that fragment data, starve budgets, or block algorithms from learning.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/account-structure-review ~/.claude/skills/
```

## Core Capabilities

### Structural Anti-Pattern Detection
- **Over-segmentation**: Too many campaigns/ad sets splitting data and budget below learning thresholds
- **Under-segmentation**: Everything in one campaign, can't isolate performance by intent or funnel stage
- **Budget fragmentation**: Daily budgets too low to exit learning phase or sustain delivery
- **Targeting overlap**: Multiple campaigns competing in same auctions, bidding against yourself
- **Objective mismatch**: Using Traffic when you need Conversions, mixing lead gen and ecommerce goals in one campaign

### Google-Specific Structure Auditing
- Campaign type separation (Search ≠ Display ≠ Shopping ≠ PMax)
- Ad group theme coherence (SKAGs are dead, STAGs with 5-15 keywords)
- Match type strategy alignment per campaign intent
- PMax cannibalizing branded Search
- Shared budgets causing cross-campaign interference
- Search Partners eating budget without conversions
- Automated bid strategies applied to low-volume campaigns

### Meta-Specific Structure Auditing
- CBO vs ABO alignment with goals and budget levels
- Advantage+ Shopping adoption readiness
- Prospecting vs retargeting separation
- Funnel exclusions (retargeting excludes purchasers, prospecting excludes retargeting audiences)
- Advantage+ Audience stability (broad targeting with signal-based constraints)
- Campaign duplication testing without isolation
- Multiple ad sets in prospecting CBO campaigns (common waste vector)

### Consolidation Decision Framework
- How to merge campaigns without losing historical data
- Campaign experiments for migration testing (Google) or 50/50 A/B tests (Meta)
- Incremental changes vs wholesale restructure
- Sequencing: What to consolidate first, what to defer

## Structure Health Criteria

### Google Ads: Minimum Conversion Volume Thresholds

| Bid Strategy | Minimum Monthly Conversions | Ideal Monthly Conversions | Warning Signs |
|--------------|----------------------------|--------------------------|---------------|
| Manual CPC | N/A (no learning required) | N/A | Using manual in 2026 means you're leaving performance on the table |
| Maximize Clicks | 0 (but why?) | N/A | You have conversion tracking — use it |
| Maximize Conversions | 15/month | 30+/month | <15/month = erratic, algorithm thrashing |
| Target CPA | 30/month | 50+/month | <30/month = CPA target won't be hit reliably |
| Target ROAS | 50/month | 100+/month | <50/month = ROAS variance too high, poor signal |

**Learning Phase**: Campaigns need ~50 conversions in 30 days to exit learning. Campaigns with <30 conversions/month perpetually re-enter learning with every creative refresh or bid change.

### Meta: Ad Set-Level Conversion Volume Thresholds

| Optimization Goal | Minimum Weekly Conversions | Ideal Weekly Conversions | Warning Signs |
|-------------------|----------------------------|--------------------------|---------------|
| Landing Page Views | N/A (top funnel) | N/A | Using this when you have purchase tracking = waste |
| Link Clicks | N/A (top funnel) | N/A | Same as above |
| Leads (Lead Gen) | 10/week per ad set | 20+/week | <10/week = unstable CPL |
| Add to Cart | 15/week per ad set | 30+/week | <15/week = algorithm can't optimize reliably |
| Initiate Checkout | 20/week per ad set | 40+/week | <20/week = CPA variance too high |
| Purchase | 50/week per ad set | 100+/week | <50/week = learning limited, poor delivery |
| Purchase (Advantage+) | 50/week per campaign | 150+/week | Advantage+ needs high volume, consolidate aggressively |

**Learning Phase**: Ad sets need ~50 conversions/week to exit learning. Ad sets with <50/week perpetually re-enter learning with every edit.

### Budget Fragmentation Thresholds

| Platform | Minimum Daily Budget | Ideal Daily Budget | Why |
|----------|---------------------|-------------------|-----|
| Google Search (tCPA) | $150/day | $300+/day | 10x target CPA minimum for stable delivery |
| Google PMax | $100/day | $300+/day | PMax needs volume to test assets across channels |
| Google Display | $50/day | $100+/day | Lower conversion rate = need more spend to gather signal |
| Meta CBO (Conversions) | $100/day | $300+/day | CBO needs budget to test ad sets before allocating |
| Meta ABO (Conversions) | $20/day per ad set | $50+/day per ad set | Ad sets under $20/day starve before learning completes |
| Meta Advantage+ | $200/day | $500+/day | Consolidated campaigns need higher budgets to sustain delivery |

**Critical Rule**: If your campaign can't sustain the minimum daily budget for 30 consecutive days without pausing, your account is over-segmented.

### Targeting Overlap Indicators (Meta)

| Overlap % | Status | Action Required |
|-----------|--------|-----------------|
| 0-10% | Healthy | No action |
| 11-25% | Moderate | Monitor, consider consolidation if both ad sets underperform |
| 26-50% | High | Consolidate or add exclusions immediately |
| 51%+ | Critical | You're bidding against yourself, merge now |

Check overlap in Meta Ads Manager > Tools > Audience Overlap. Run this monthly for all active prospecting campaigns.

### Google: Keyword Overlap Indicators

| Scenario | Status | Action Required |
|----------|--------|-----------------|
| Same keyword, different match types, same campaign | Healthy | This is fine, broad/phrase/exact in same ad group is valid |
| Same keyword, same match type, different campaigns | High Risk | Unless separated by geo/device/schedule, you're competing with yourself |
| Broad keyword in Campaign A matching exact keyword in Campaign B | Critical | Broad will steal traffic from exact unless you add exact as negative in Campaign A |
| PMax active + Brand Search campaign | Critical | PMax WILL cannibalize branded search. Add brand terms as negatives in PMax or pause PMax. |

Run Search Terms Report monthly and cross-reference against all campaigns to find cannibalization.

## Platform-Specific Structure Best Practices

### Google Ads: Campaign Hierarchy

**Search Campaigns** (Hierarchy: Campaign > Ad Group > Keywords > Ads)
- **One theme per campaign**: Brand, Competitor, Category, Product Line, Intent Stage
- **Ad groups**: 5-15 keywords per ad group, tightly themed (STAGs, not SKAGs)
- **Match types**: Use Phrase and Broad in most campaigns. Exact only for ultra-high-intent/high-value terms.
- **Negatives**: Aggressive negative keyword lists at campaign level to prevent overlap
- **Structure example**:
  - Campaign: Brand Search
    - Ad Group: Brand Exact (5 exact match brand terms)
    - Ad Group: Brand Misspellings (10 phrase match variants)
  - Campaign: Category - Running Shoes
    - Ad Group: Trail Running (8 phrase match keywords)
    - Ad Group: Road Running (10 phrase match keywords)
    - Ad Group: Racing Flats (5 phrase match keywords)

**Shopping Campaigns**
- Standard Shopping: One campaign per product category OR one campaign with ad groups by product type
- PMax: One campaign for entire catalog OR separate campaigns by margin/goal (e.g., high-margin PMax vs volume PMax)
- **Do NOT run PMax + Standard Shopping simultaneously** — PMax will dominate, Standard Shopping becomes a reporting shell

**Performance Max (PMax)**
- **When to use**: E-commerce with feed, lead gen with dynamic assets, omnichannel goals
- **Structure**: 1-3 campaigns max. PMax is designed to consolidate. Multiple PMax campaigns only if goals differ (ROAS target, audience strategy, geo)
- **Asset groups**: 3-5 per campaign, themed by product category or customer segment
- **Critical negative keywords**: Add brand terms if you want branded search to stay in Search campaigns

**Display Campaigns**
- Separate campaigns by goal: Prospecting vs Retargeting
- Prospecting: Use Responsive Display Ads (RDA) with demographic/interest targeting or Custom Audiences
- Retargeting: Website visitors, cart abandoners, customer lists. Lower bids, higher ROAS targets.

### Meta: Campaign Hierarchy

**Campaign** (Objective + Budget type)
- Choose objective: Awareness, Traffic, Engagement, Leads, App Promotion, Sales
- Choose budget: Campaign Budget Optimization (CBO) or Ad Set Budget Optimization (ABO)

**Ad Set** (Audience + Placement + Optimization)
- Define audience (Advantage+ Audience, Custom Audiences, Lookalikes)
- Choose placement (Advantage+ Placements or manual)
- Set optimization event (Purchase, Add to Cart, Lead, etc.)
- Set bid strategy (Lowest Cost, Cost Cap, Bid Cap)

**Ad** (Creative)
- Image, video, carousel, collection
- Primary text, headline, description, CTA

**CBO vs ABO Decision Tree**:
- **Use CBO when**:
  - Budget >$300/day
  - Testing multiple audiences against each other
  - Want Meta to auto-allocate budget to best performers
  - Have 2-5 ad sets per campaign
- **Use ABO when**:
  - Budget <$300/day
  - Need strict budget control per ad set (e.g., prospecting gets $100, retargeting gets $50)
  - Testing one audience or creative set in isolation
  - Running Advantage+ (CBO is required)

**Advantage+ Shopping Campaigns**
- Consolidates prospecting + retargeting into one campaign with one ad set
- Requires Conversions API (CAPI) + pixel
- Needs 50+ purchases/week to perform (ideally 150+/week)
- Best for brands spending $10K+/month on Meta with mature pixel
- **When NOT to use**: New pixels (<1000 events), low conversion volume, need granular audience control

**Prospecting vs Retargeting Separation**
- **Always separate** prospecting and retargeting into different campaigns
- **Prospecting**: Broad targeting (Advantage+ Audience with interest/demo signals), lookalikes, cold traffic
- **Retargeting**: Website visitors (180d), cart abandoners (30d), video viewers (30d), engaged users
- **Critical exclusions**:
  - Prospecting: Exclude website visitors 180d, customer lists
  - Retargeting: Exclude purchasers (unless running replenishment/upsell)

## Consolidation Decision Framework

### Step 1: Conversion Volume Audit
Pull last 30 days of data. For each campaign/ad set:
1. Count conversions
2. Compare to minimum threshold (see tables above)
3. Flag campaigns/ad sets below threshold as "Under-Volume"

### Step 2: Budget Fragmentation Audit
For each campaign:
1. Calculate average daily spend
2. Compare to minimum daily budget threshold
3. Flag campaigns below threshold as "Under-Budget"
4. Check: Does campaign run out of budget before end of day? If yes, flag "Budget-Constrained"

### Step 3: Targeting Overlap Audit
**Google**:
1. Run Search Terms Report for all Search campaigns
2. Cross-reference search terms against all other campaigns' keyword lists
3. Flag any search term appearing in 2+ campaigns

**Meta**:
1. Go to Ads Manager > Tools > Audience Overlap
2. Compare all active prospecting audiences
3. Flag any overlap >25%

### Step 4: Objective Mismatch Audit
For each campaign:
1. Check objective (Google: bid strategy; Meta: campaign objective)
2. Check conversion tracking setup
3. Flag mismatches:
   - Google: Manual CPC or Maximize Clicks when conversions are tracked
   - Meta: Traffic or Engagement objective when Purchase pixel fires
   - Mixing lead gen (form fills) and ecommerce (purchases) in same campaign

### Step 5: Consolidation Plan
For each flagged campaign, decide:
- **Merge**: Combine with similar campaign (same intent, same goal, compatible targeting)
- **Pause**: Discontinue if redundant or no clear goal
- **Restructure**: Keep separate but change targeting/budget/objective
- **Defer**: Flag for later (e.g., seasonal campaigns, test campaigns)

**Merge Rules**:
- **Google Search**: Merge campaigns with similar keyword themes and match types into one campaign with multiple ad groups
- **Google PMax**: Consolidate multiple PMax campaigns into one unless goals differ by >20% (e.g., tROAS of 300% vs 500%)
- **Meta Prospecting**: Merge lookalike audiences into one Advantage+ Audience campaign with signals
- **Meta Retargeting**: Merge retargeting ad sets into one campaign with CBO, separate ad sets by funnel stage (website visitors, cart abandoners, etc.)

### Step 6: Migration Plan
**Option A: Campaign Experiments (Google)**
1. Create experiment in original campaign
2. Build new consolidated structure in experiment arm
3. Split traffic 50/50 for 14-30 days
4. Compare performance, roll out winner

**Option B: Gradual Migration**
1. Launch new consolidated campaigns at 25% of total budget
2. Run for 7 days, compare performance
3. Increase to 50%, decrease old campaigns to 50%
4. Run for 7 days, compare again
5. If new campaigns outperform, shift 100% budget and pause old campaigns

**Option C: Immediate Cutover** (risky, only for emergencies)
1. Launch new campaigns
2. Pause old campaigns same day
3. Expect 7-14 day learning phase, performance dip

**Historical Data Preservation**:
- Do NOT delete old campaigns — pause them
- Export historical data to spreadsheet/dashboard before pausing
- Keep old campaigns paused for 90 days for reference, then archive

## Minimum Viable Structure by Budget Level

### $5K/month ($167/day)
**Google**:
- 2-4 campaigns max: Brand Search ($50/day), Category Search ($70/day), Display Retargeting ($30/day), Shopping or PMax ($17/day)
- Do NOT run PMax + Shopping simultaneously at this budget

**Meta**:
- 2 campaigns: Prospecting CBO ($100/day, 2 ad sets), Retargeting ABO ($67/day, 2 ad sets)
- If running Advantage+, go all-in: 1 Advantage+ campaign ($167/day)

### $20K/month ($667/day)
**Google**:
- 5-8 campaigns: Brand Search ($100/day), Competitor Search ($100/day), Category Search ($150/day), PMax ($200/day), Display Retargeting ($50/day), Display Prospecting ($67/day)
- Or: Consolidate into PMax ($400/day) + Brand Search ($100/day) + Display Retargeting ($167/day)

**Meta**:
- 3-4 campaigns: Prospecting CBO ($400/day, 3-5 ad sets), Retargeting CBO ($150/day, 3 ad sets), Testing Campaign ($117/day, 2 ad sets)
- Or: Advantage+ Shopping ($500/day) + Retargeting ($167/day)

### $100K/month ($3,333/day)
**Google**:
- 10-15 campaigns: Brand Search, Competitor Search, 3-5 Category Search campaigns, PMax, Display Prospecting (demographics), Display Prospecting (interests), Display Retargeting, YouTube Prospecting, YouTube Retargeting, Discovery
- Budget allocation: 40% PMax, 20% Search (Brand/Competitor/Category), 20% Display, 20% YouTube/Discovery

**Meta**:
- 6-10 campaigns: Advantage+ Shopping, Prospecting Lookalikes, Prospecting Interests, Prospecting Broad, Retargeting (Website), Retargeting (Engaged), Creative Testing, Offer Testing, New Market Testing
- Budget allocation: 50% Advantage+, 20% Prospecting (other), 15% Retargeting, 15% Testing

### $500K/month ($16,667/day)
**Google**:
- 15-25 campaigns: Separate by geo (US, CA, UK, etc.), product line, margin tier, funnel stage, device (if performance warrants), dayparting (if 24/7 doesn't work)
- Heavy investment in PMax ($8K/day), Brand ($2K/day), Category Search ($4K/day), YouTube ($2K/day)

**Meta**:
- 10-20 campaigns: Multiple Advantage+ campaigns by geo or product line, separate prospecting campaigns by demo or interest cluster, retargeting by funnel stage and recency, heavy creative testing budget
- Budget allocation: 60% Advantage+, 15% Prospecting, 10% Retargeting, 15% Testing

**Key principle**: Structure complexity should scale with budget and conversion volume, not with number of products or "just because."

## Output Format Template

When conducting an account structure review, provide output in this format:

```
# Account Structure Review — [Client Name] — [Date]

## Executive Summary
- Total monthly spend: $X
- Total campaigns: X (Google: X, Meta: X)
- Campaigns flagged: X (X% of total)
- Primary issues: [List top 3]
- Recommended consolidation: X campaigns → X campaigns
- Expected impact: [Estimated improvement in CPA, ROAS, or learning phase stability]

## Structural Health Score: X/100
- Conversion volume: X/30 (campaigns meeting minimum thresholds)
- Budget allocation: X/25 (campaigns with sufficient daily budgets)
- Targeting efficiency: X/25 (overlap score)
- Objective alignment: X/20 (campaigns using correct objectives for goals)

## Google Ads Findings

### Campaign Inventory
[Table: Campaign Name | Type | Daily Budget | Monthly Conversions | Status | Flag]

### Issues Identified
1. **[Issue Category]** (e.g., Over-Segmentation, Budget Fragmentation)
   - **Finding**: [Specific data point]
   - **Impact**: [Why this matters]
   - **Recommendation**: [What to do]

### Google Consolidation Plan
- Merge: [Campaign A + Campaign B] → [New Campaign Name]
- Pause: [Campaign C] (reason: redundant with PMax)
- Restructure: [Campaign D] (change from Maximize Clicks to tCPA)

## Meta Findings

### Campaign Inventory
[Table: Campaign Name | Objective | Budget Type | Daily Budget | Weekly Conversions | Status | Flag]

### Issues Identified
1. **[Issue Category]**
   - **Finding**: [Specific data point]
   - **Impact**: [Why this matters]
   - **Recommendation**: [What to do]

### Meta Consolidation Plan
- Merge: [Ad Set A + Ad Set B] → [New Campaign Name] (CBO)
- Migrate to Advantage+: [Campaign E] (conversion volume meets threshold)
- Pause: [Campaign F] (overlap with retargeting campaign)

## Migration Roadmap

### Phase 1 (Week 1-2): [Immediate Actions]
- Launch: [New Campaign X] at $X/day
- Reduce: [Old Campaign Y] to $X/day (from $X/day)
- Pause: [Campaign Z] (no conversions in 60 days)

### Phase 2 (Week 3-4): [Performance Validation]
- Monitor: [Campaigns] for learning phase completion
- Compare: [Old vs New] performance
- Decision: Roll out 100% or revert

### Phase 3 (Week 5-6): [Full Migration]
- Shift: 100% budget to new structure
- Pause: All old campaigns
- Archive: Export historical data

## Expected Outcomes
- **Learning phase stability**: [X campaigns] will exit learning phase with consolidated volume
- **Budget efficiency**: [X campaigns] will sustain delivery throughout day instead of exhausting budget early
- **Reporting clarity**: [Benefit of cleaner structure]
- **Algorithmic performance**: Expect CPA to improve [X%] as algorithms get more signal

## Risks & Mitigations
- **Risk**: Performance dip during learning phase
  - **Mitigation**: Gradual migration, keep 50% budget in proven campaigns during transition
- **Risk**: Loss of granular reporting
  - **Mitigation**: Use labels, UTM parameters, or asset groups (PMax) to maintain visibility

## Next Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

## Worked Example

**Scenario**: Mid-market DTC brand, $30K/month spend, Google + Meta

**Google Ads Audit**:
- 28 Search campaigns (Brand, Category, Product, Competitor)
- 22 campaigns have <20 conversions/month (below tCPA threshold)
- 15 campaigns have daily budgets <$20 (exhaust by 10am)
- PMax campaign active + Standard Shopping campaign active (PMax dominating, Standard Shopping getting <5% of budget)
- Shared budget across 8 campaigns causing unpredictable allocation

**Findings**:
1. **Over-Segmentation (Search)**: 28 campaigns should be 6-8 campaigns grouped by intent
2. **Budget Fragmentation**: 15 campaigns can't sustain delivery
3. **PMax Cannibalization**: Standard Shopping is redundant
4. **Shared Budget Chaos**: 8 campaigns competing for shared budget instead of predictable allocation

**Consolidation Plan**:
- **Merge Search campaigns**: 28 → 6 (Brand, Competitor, Category A, Category B, Category C, Generic)
- **Pause Standard Shopping**, increase PMax budget from $200/day to $400/day
- **Remove shared budgets**, assign fixed daily budgets to each campaign
- **Resulting structure**: 6 Search campaigns + 1 PMax + 1 Display Retargeting = 8 campaigns total

**Meta Audit**:
- 12 campaigns (10 prospecting, 2 retargeting)
- 10 prospecting campaigns have overlapping audiences (Lookalike 1%, Lookalike 2-3%, Interest: Fitness, Interest: Running, Broad, etc.)
- Audience overlap tool shows 35-60% overlap across all prospecting campaigns
- 6 campaigns have <30 purchases/week (below Conversions optimization threshold)
- Using ABO with $50/day per campaign

**Findings**:
1. **Targeting Overlap**: 10 prospecting campaigns bidding against each other
2. **Under-Volume**: 6 campaigns don't have enough conversions to optimize
3. **Budget Fragmentation**: $50/day per campaign is marginal for Conversions objective

**Consolidation Plan**:
- **Merge prospecting campaigns**: 10 → 2 (Advantage+ Shopping at $700/day, Lookalike Testing at $100/day)
- **Consolidate retargeting**: 2 campaigns → 1 CBO campaign with 3 ad sets (Website 7-30d, Cart Abandoners, Engaged Video Viewers) at $200/day
- **Resulting structure**: 3 campaigns total (Advantage+, Lookalike Testing, Retargeting)

**Expected Impact**:
- **Google**: Campaigns will have 40-60 conversions/month (vs 8-15 currently), tCPA will stabilize, learning phase will complete
- **Meta**: Advantage+ will have 120+ purchases/week (vs 20-30 per campaign currently), audience overlap eliminated, CBO will optimize budget allocation
- **Overall**: CPA expected to improve 15-25% within 30 days post-migration

## Guidelines

- **Never consolidate blindly**: Check conversion data, budget sustainability, and targeting logic before merging
- **Preserve historical data**: Pause, don't delete
- **Test migrations when possible**: Use experiments (Google) or gradual budget shifts (Meta)
- **Monitor learning phases**: Expect 7-14 days of instability after structural changes
- **Document everything**: Keep audit findings, consolidation plan, and migration steps in shared doc for team visibility
- **Revisit quarterly**: Account structure should evolve as budget, conversion volume, and goals change

## How to Use This Skill

Ask questions like:
- "Audit my Google Ads account structure and identify consolidation opportunities"
- "My Meta campaigns have low conversion volume — should I consolidate?"
- "I'm inheriting a messy account with 40+ campaigns — where do I start?"
- "What's the right campaign structure for a $50K/month budget on Google and Meta?"
- "My campaigns keep re-entering learning phase — is my structure the problem?"
- "Should I migrate to Advantage+ Shopping or keep my current prospecting setup?"
- "Create a consolidation plan for my Search campaigns — they're all under $30/day budget"

## Safety & Data Handling

- **Analysis only** — this skill produces recommendations, not live changes. Always review before implementing in any ad platform.
- **No PII** — do not paste customer emails, phone numbers, names, or order-level data. Use aggregated/anonymized exports only.
- **Projections are estimates** — financial forecasts are based on historical data and carry uncertainty. Label them as projections in client deliverables.
- **Confirm before acting** — never pause, delete, or modify live campaigns based solely on this analysis without human review.
