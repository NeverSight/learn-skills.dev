---
name: impression-share-diagnostics
description: Impression share analysis and root cause diagnosis for Google Ads Search campaigns. Auto-invoke when investigating underspending, analyzing auction competitiveness, or diagnosing budget vs. quality issues. Interprets Search IS, Budget Lost IS, and Rank Lost IS metrics in smart bidding context.
allowed-tools: [Read]
---

# Impression Share Diagnostics Skill

**Purpose:** Provides expert analysis of impression share metrics to diagnose root causes of underspending and auction performance issues in Google Ads Search campaigns.

**Type:** Domain knowledge skill (auto-invoked)

---

## What This Skill Deliberately Does NOT Do

- **Calculate the budget change.** Diagnosis ends at "budget is (or isn't) the constraint" — the sizing math (5-10% caps, adjustment factors, daily translation) lives in [`budget-recommendation-calculator`](../budget-recommendation-calculator/).
- **Diagnose PMax with the decision tree.** Performance Max has no impression share metrics — the scenarios apply to Search campaigns (plus the bid-cap check for Display/Video remarketing). PMax gets budget-utilization and asset diagnostics instead (see the campaign-type section).
- **Treat Rank Lost IS as a target.** The skill reads it as evidence for the constraint diagnosis, never as a number to optimize down — chasing it is the misconception this skill exists to correct.
- **Pull the metrics.** The required API fields are listed under Data Sources Required; the query templates live in [`gaql-query-patterns`](../gaql-query-patterns/).

---

## Core Impression Share Metrics

### Search Impression Share (Search IS)
**What it measures:** Percentage of impressions you received out of total eligible impressions

**How to interpret:**
- **>80%:** Excellent - capturing most available impressions
- **50-80%:** Good - moderate market coverage
- **30-50%:** Limited - missing significant opportunity
- **<30%:** Very limited - major opportunity loss

**Note:** Higher is better, but 100% is rarely achievable or necessary

### Budget Lost Impression Share (Budget Lost IS)
**What it measures:** Percentage of impressions lost due to budget constraints

**How to interpret:**
- **<10%:** Budget is sufficient for current demand
- **10-30%:** Moderate budget constraint (minor opportunity loss)
- **30-50%:** Significant budget constraint (primary limiting factor)
- **>50%:** Severe budget constraint (major spend potential untapped)

**Primary indicator:** If high, increasing budget will likely increase spend

### Rank Lost Impression Share (Rank Lost IS)
**What it measures:** Percentage of impressions lost due to ad rank (quality + bid)

**How to interpret:**
- **<10%:** Excellent competitive position
- **10-30%:** Good competitive position (normal)
- **30-60%:** Moderate competitive disadvantage
- **>60%:** Significant competitive disadvantage

**CRITICAL CONTEXT:** Rank Lost IS is **informational, not a primary optimization target**

---

## Smart Bidding Context (CRITICAL)

### Most Portfolio Campaigns Use Smart Bidding

**Common bidding strategies:**
- **Max Conversions** (no target) - Automated, no manual bid control
- **Max Conversion Value** (no target) - Automated, ROAS focus
- **Max Clicks** (with optional max CPC limit) - Automated, traffic focus

**YOU CANNOT MANUALLY ADJUST BIDS** - Google's algorithm controls them.

**Primary Control Lever:** Monthly budget (translates to daily budget)

**Budget Management Philosophy:**
1. **#1 Priority:** Hit monthly spend targets (pacing)
2. **#2 Priority:** Maintain acceptable CPA/ROAS goals
3. **Budget increases are CONSERVATIVE:** 5-10% monthly budget increases

---

## Root Cause Diagnosis Decision Tree

### Scenario 1: Budget Too Low (Most Common)

**Pattern:**
- Budget Lost IS: >10% (any level of budget constraint)
- Rank Lost IS: >50% (high competitive pressure)
- Search IS: <70% (missing impressions)

**What's happening:**
- Google's algorithm wants to bid higher to compete
- Budget cap prevents it from spending more
- Algorithm is forced to bid conservatively to stay within budget
- Result: Lower bids → Worse ad rank → Lost impressions

**Diagnosis:** Budget is too low for competitive auction environment

**Recommendation:** Increase monthly budget by 5-10%

**Why this works:**
- With smart bidding, budget is the primary lever
- Higher budget → algorithm can bid more aggressively
- More aggressive bids → better ad rank → more impressions → more spend

---

### Scenario 2: Quality Score Issues (Secondary)

**Pattern:**
- Rank Lost IS: >60% (very high)
- Budget Lost IS: <10% (budget is sufficient)
- CPA significantly above goals
- Search IS: Low despite budget availability

**What's happening:**
- Low quality score = higher cost per click
- Google charges more for lower quality ads
- Algorithm can't compete efficiently
- Result: Fewer impressions even with budget available

**Diagnosis:** Ad relevance, landing page, or keyword quality issues

**Recommendation:**
1. Improve ad relevance (match ad copy to keywords)
2. Improve landing page experience (speed, mobile, relevance)
3. Refine keyword quality (remove low-performing keywords)
4. Secondary to budget fixes - quality improvements take time

---

### Scenario 3: Low Demand (Normal, Not a Problem)

**Pattern:**
- Search IS: >80% (capturing most impressions)
- Budget Lost IS: <10% (budget is sufficient)
- Rank Lost IS: <10% (good competitive position)
- Still underspending vs. budget

**What's happening:**
- You're capturing most available impressions
- Low search volume for these keywords
- This is **NORMAL** - not every keyword has high volume

**Diagnosis:** Account is operating efficiently, just low organic demand

**Recommendation:**
- **Option 1:** Accept that this is normal (low search volume markets)
- **Option 2:** Consider reducing budget to match actual demand
- **Option 3:** Expand targeting (new keywords, looser match types, new geos)

**DO NOT** increase budget in this scenario - you're already capturing available demand

---

### Scenario 3a: Brand Campaign Demand Ceiling (Budget Reallocation)

**Pattern:**
- Brand campaign Search IS: >90% (near-maxed)
- Budget Lost IS: <10%
- Brand campaign spending 40-60% of allocated budget
- Other campaigns (GEO, BDRM) have lower IS (more headroom)

**What's happening:**
- Brand search demand is capped - not enough searches for "[Property] apartments"
- At 90%+ IS, you're capturing nearly all available brand demand
- Budget allocated to Brand cannot be spent
- Meanwhile, GEO/BDRM campaigns have impression share headroom

**Diagnosis:** Budget misallocation - too much budget on demand-capped Brand, not enough on campaigns with headroom

**Recommendation:**
- **Reallocate budget** from Brand → GEO or BDRM campaigns
- Brand continues capturing all available demand (just with smaller budget)
- GEO/BDRM can compete more aggressively with additional budget
- Total account spend increases toward daily target

**Example:**
```
Before reallocation:
- Brand: $20/day budget, $10/day actual (50% util), 94% IS
- GEO: $45/day budget, $27/day actual (60% util), 18% IS
- BDRM: $45/day budget, $20/day actual (44% util), 44% IS

Action: Move $5-10/day from Brand to GEO/BDRM

After reallocation:
- Brand: $12/day budget (still captures 94% IS)
- GEO: $50/day budget (can now compete for more of the 82% lost IS)
- BDRM: $48/day budget (can compete for more of the 56% lost IS)
```

**Key Insight:** You can't force demand that doesn't exist - put budget where there's opportunity

---

### Scenario 4: Recent Budget Increase (Ramp-Up Period)

**Pattern:**
- Budget was increased in last 3-7 days
- Currently underspending vs. new budget
- Impression share metrics not yet stabilized

**What's happening:**
- Smart bidding algorithms need time to adjust
- Algorithm gradually increases bids after budget increase
- Normal ramp-up period (3-7 days typical)

**Diagnosis:** Normal ramp-up period after budget increase

**Recommendation:**
- **No action needed**
- Monitor for 3-5 more days
- If still underspending after 7 days, re-investigate

**DO NOT** increase budget again during ramp-up period

---

## Impression Share Context for Different Campaign Types

### Search Campaigns (GEO, Bedroom, Brand)
- **Full IS metrics available:** Search IS, Budget Lost IS, Rank Lost IS
- **Use decision tree above** to diagnose root cause
- **Primary focus:** Budget Lost IS (indicates spend potential)

### Performance Max Campaigns
- **NO impression share metrics available** (different auction dynamics)
- **Cannot use IS for diagnosis**
- **Alternative diagnostics:**
  - Budget utilization % (MTD spend ÷ MTD budget)
  - Asset performance scores
  - Auction insights (when available)

### Demand Gen Campaigns
- **Limited IS metrics** (display network, different from search)
- **Focus on:** Reach, frequency, view rate
- **Not applicable:** Search IS decision tree

### Display/Video Campaigns (Remarketing)

**Key Diagnostic:** Check for "Bid setting limited" status in Google Ads UI

**Common Issue:** Max CPC bid cap too restrictive on Maximize Clicks strategy

**Pattern:**
- Campaign status shows "Bid setting limited"
- Very low click volume despite budget availability
- Spending well below daily budget

**Root Cause:** Max CPC cap (e.g., $2-3) is lower than auction clearing prices for Display network. Campaign can't compete for impressions.

**Standard Fix for Display Remarketing:**
- Increase max CPC bid limit to **$4.00** (standard floor)
- This provides headroom to compete while maintaining reasonable ceiling

**Context:** Accounts may use standardized content suitability settings which restrict available inventory. This means bid caps need to be higher ($4+) to compete in the smaller placement pool. If content suitability settings change, bid cap requirements may need adjustment.

**Verification:**
1. Check campaign settings → Bidding → "Maximum CPC bid limit"
2. If under $4.00, increase to $4.00
3. Monitor for 2-3 days - spend should increase toward budget

**Expected CPC Range:** $2-3 after auctions normalize (the $4 cap acts as ceiling)

**Note:** Display campaigns don't have Search IS metrics - diagnose via campaign status and bid strategy settings

---

## How to Interpret Rank Lost IS in Context

### Common Misconception:
"Rank Lost IS is high (60-80%), so we need to improve quality score or increase bids"

### Reality:
- **Rank Lost IS is informational, not a target**
- High Rank Lost IS (60-80%) is common in competitive auctions
- **Don't optimize TO a specific Rank Lost IS target**
- **Use it to understand WHY underspending** (competitive pressure signals budget need)

### Correct Interpretation:
- **High Rank Lost IS + High Budget Lost IS** → Budget is the constraint
- **High Rank Lost IS + Low Budget Lost IS** → Quality/efficiency is the constraint
- **Low Rank Lost IS + Low Budget Lost IS** → No constraint (low demand)

**Primary focus:** Pacing variance and CPA/ROAS performance, not Rank Lost IS itself

---

## Budget vs. Quality Trade-offs

### When Budget Increase is Appropriate:
✅ Underspending vs. monthly budget (pacing variance >±8%)
✅ Budget Lost IS >10% (spend potential exists)
✅ CPA is acceptable or below goal
✅ ROAS is acceptable or above goal
✅ No recent budget increase in last 7 days

### When Budget Increase is NOT Appropriate:
❌ CPA is significantly above goal (>20% over target)
❌ ROAS is below minimum threshold
❌ Recent budget increase within last 3-7 days (ramp-up period)
❌ Search IS >80% + Budget Lost IS <10% (low demand, not budget constraint)
❌ Quality score issues evident (very high CPA despite budget availability)

### The Conservative Approach:
- **Start with 5% budget increase** (not 10-20%)
- **Monitor for 5-7 days** before additional increases
- **Never increase budget >10% in single change** (algorithm shock risk)
- **Quality improvements are secondary** to budget optimization

---

## Integration with Underspending Investigation

### How This Skill Fits:
This skill provides the **Step 3: Impression Share Analysis** framework for underspending investigations.

### Typical Investigation Flow:
1. **Step 1:** Check recent optimizations (ramp-up period check)
2. **Step 2:** Analyze campaign spend patterns (which campaigns, budget structure)
3. **Step 3:** **USE THIS SKILL** → Diagnose root cause via impression share
4. **Output:** Budget recommendation or quality improvement recommendation

### Expected Output from This Skill:
After analyzing IS metrics, you should be able to answer:
- **What is the primary constraint?** (Budget | Quality | Low Demand | Ramp-Up)
- **What evidence supports this?** (specific IS metric values)
- **What action is recommended?** (budget increase | quality improvement | monitor | reduce budget)
- **Why will this work?** (mechanism explanation)

---

## Quick Reference: IS Patterns Cheat Sheet

| Search IS | Budget Lost IS | Rank Lost IS | Diagnosis | Recommendation |
|-----------|----------------|--------------|-----------|----------------|
| <70% | >30% | >50% | Budget too low | Increase budget 5-10% |
| <70% | <10% | >60% | Quality issues | Improve quality (secondary) |
| >80% | <10% | <10% | Low demand | Normal (or reduce budget) |
| Any | Any | Any | Recent budget ↑ | Monitor 3-5 more days |
| 50-70% | 10-30% | 30-60% | Mixed constraint | Increase budget 5% + monitor |

---

## When to Use This Skill

### Auto-Invoked When:
- Investigating underspending issues
- Analyzing impression share metrics
- Diagnosing auction competitiveness
- Determining budget vs. quality constraints
- User mentions "impression share", "lost IS", "rank lost", or "budget lost"
- Creating budget increase recommendations
- Explaining why campaigns are underspending

### Data Sources Required:
- Google Ads API: `metrics.search_impression_share`
- Google Ads API: `metrics.search_budget_lost_impression_share`
- Google Ads API: `metrics.search_rank_lost_impression_share`
- Campaign bidding strategy: `campaign.bidding_strategy_type`
- Campaign CPA/ROAS: `metrics.cost_per_conversion`, `metrics.conversions_value_per_cost`

### CRITICAL: API Returns Decimals, Not Percentages

**The Google Ads API returns impression share as decimals (0.0 to 1.0), NOT percentages.**

| API Value | Actual Percentage |
|-----------|-------------------|
| 0.2464 | 24.64% |
| 0.1017 | 10.17% |
| 0.0999 | 9.99% |
| 0.6337 | 63.37% |

**When displaying to users or applying thresholds, always multiply by 100:**
```python
# Correct
search_is_pct = row.metrics.search_impression_share * 100
print(f"Search IS: {search_is_pct:.1f}%")  # Output: "Search IS: 24.6%"

# WRONG - will show misleading values like "0.25%"
print(f"Search IS: {row.metrics.search_impression_share:.2f}%")
```

**Threshold comparisons must use percentage values (after multiplying by 100):**
```python
search_is = api_value * 100  # Convert to percentage first
if search_is > 80:  # 80% threshold
    print("High impression share")
```

---

## Using Impression Share as Demand Ceiling (Budget Viability Analysis)

### The Pattern

When evaluating whether an ad group or campaign can absorb a budget increase (or sustain spend after pausing other segments), use impression share as a demand signal to calculate the spending ceiling.

**Key Insight:**
- Current spend tells you what you *are* spending
- Impression Share tells you what you *could* spend (the demand ceiling)

### Formula

```
Potential Spend = Current Spend / (Search IS / 100)
```

### Example

**Scenario:** Client asks to pause all ad groups except one single-geo ad group. Can it absorb the budget?

| Metric | Single Ad Group |
|--------|-----------------|
| Current spend | $91/month |
| Search IS | 15.8% |
| **Potential ceiling** | $91 / 0.158 = **$577/month** |
| Required budget | $1,800/month |
| **Verdict** | Will severely underpace (68% under) |

### When to Use This

- Client asks to pause ad groups and consolidate budget into fewer segments
- Evaluating if a single geo/segment can absorb increased spend
- Predicting underspend risk before making changes
- Sizing addressable demand for a keyword set or geography
- Answering "can X absorb Y budget?"

### Ad Group Level IS

**Important:** Search Impression Share is available at the ad group level, not just campaign level.

Query pattern:
```sql
SELECT
    ad_group.name,
    metrics.impressions,
    metrics.cost_micros,
    metrics.search_impression_share
FROM ad_group
WHERE campaign.name LIKE "%GEO%"
AND segments.date DURING LAST_30_DAYS
```

### Nuances & Limitations

- This is a **rough estimate**, not exact
- Assumes similar CPCs at higher volume (CPCs may increase with more aggressive bidding)
- Smart Bidding may adjust behavior when segments change
- Works best for Search campaigns (PMAX has no IS metrics)
- The ceiling assumes 100% IS capture, which is rarely achievable in practice

### Probability Assessment

Use the gap between potential ceiling and required budget to estimate underpacing risk:

| Gap | Probability of Underpacing |
|-----|---------------------------|
| Ceiling < 50% of required | >90% (near certain) |
| Ceiling 50-75% of required | 70-90% (very likely) |
| Ceiling 75-100% of required | 40-70% (likely) |
| Ceiling > 100% of required | <40% (may work) |

---

## When to Load Other Skills

| Skill | When |
|-------|------|
| [`budget-recommendation-calculator`](../budget-recommendation-calculator/) | AFTER diagnosis, when the verdict is "budget constraint" — it turns the diagnosis into a conservative, capped recommendation |
| [`underspending-investigation`](../underspending-investigation/) | The producing investigation workflow that routes here — this skill is its impression-share analysis step |
| [`investigation-methodology`](../investigation-methodology/) | When IS analysis is one layer of a broader performance investigation rather than a standalone underspend question |
| [`gaql-query-patterns`](../gaql-query-patterns/) | When pulling the IS metrics this skill interprets |

---

Built by [Kurt Henninger](https://fourteenwebmedia.com). More free skills: [github.com/fourteenwm/ppc-ai-skills](https://github.com/fourteenwm/ppc-ai-skills)
