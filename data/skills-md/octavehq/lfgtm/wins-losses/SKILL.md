---
name: wins-losses
description: Analyze won and lost deals for patterns, insights, and actionable learnings. Use when user says "win/loss analysis", "why did we lose", "deal patterns", "win themes", or asks about deal outcome trends. Do NOT use for visual HTML reports — use /octave:win-loss-report instead.
---

# /octave:wins-losses - Deal Intelligence

Analyze your won and lost deals to understand what's working, why you're losing, and how to improve win rates. Surface patterns, competitor intelligence, and actionable recommendations.

## Usage

```
/octave:wins-losses [--status won|lost|both] [--period <time-range>]
```

## Options

- `--status <status>` - Focus on won, lost, or both (default: both)
- `--period <range>` - Time range (month, quarter, year, custom)
- `--competitor <name>` - Filter by competitor involvement
- `--segment <name>` - Filter by segment
- `--min-amount <amount>` - Minimum deal size
- `--company <domain>` - Analyze specific deal

## Examples

```
/octave:wins-losses                                  # Overview of recent wins/losses
/octave:wins-losses --status lost --period quarter   # Lost deals this quarter
/octave:wins-losses --competitor "Salesforce"        # Deals involving Salesforce
/octave:wins-losses --segment "Enterprise"           # Enterprise deals analysis
/octave:wins-losses --company acme.com               # Deep dive on Acme deal
```

## Instructions

When the user runs `/octave:wins-losses`:

### Step 1: Determine Focus

If no options provided, show overview:

```
What would you like to analyze?

1. Full Win/Loss Report - Compare wins and losses
2. Win Analysis - What's working, why we win
3. Loss Analysis - Why we're losing, patterns
4. Competitor Analysis - Win/loss by competitor
5. Deal Deep Dive - Analyze specific deal

Your choice:
```

### Step 2: Query Deal Data

**For Overview:**
```
# Get won deals
list_events({
  eventTypes: ["DEAL_WON"],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 50
})

# Get lost deals
list_events({
  eventTypes: ["DEAL_LOST"],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 50
})

# Get findings from won deals
list_findings({
  opportunityStatus: ["WON"],
  extractionTypes: [
    "CALL_EXTERNAL_OBJECTIONS",
    "CALL_INTERNAL_VALUE_PROP_PRESENTATIONS",
    "CALL_INTERNAL_PROOF_POINTS",
    "CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING"
  ],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 100
})

# Get findings from lost deals
list_findings({
  opportunityStatus: ["LOST"],
  extractionTypes: [
    "CALL_EXTERNAL_OBJECTIONS",
    "CALL_INTERNAL_VALUE_PROP_PRESENTATIONS",
    "CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING"
  ],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 100
})
```

**For Competitor Analysis:**
```
list_findings({
  extractionTypes: ["CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING", "EMAIL_COMPETITOR_MENTION"],
  dateRange: { start: "<period start>", end: "<today>" },
  entityMatches: {
    competitorOIds: ["<competitor_oId>"]
  }
})
```

**For Deal Deep Dive:**
```
list_events({
  eventTypes: ["DEAL_WON", "DEAL_LOST", "CALL", "EMAIL"],
  companyDomains: ["<domain>"]
})

list_findings({
  companyDomains: ["<domain>"]
})

get_event_detail({
  eventOId: "<event_oId>",
  includeTranscript: true
})
```

### Step 3: Analyze Patterns

Aggregate findings across won/lost deals:

```
list_findings({
  eventTypes: ["DEAL_WON", "DEAL_LOST"],
  dateRange: { start: "<period start>", end: "<today>" }
})
```

### Step 4: Present Analysis

---

#### Full Win/Loss Report

```
WIN/LOSS ANALYSIS: Q4 2025
==========================

EXECUTIVE SUMMARY
-----------------
Win Rate: 34% (down from 38% in Q3)
Deals Won: 12 ($1.2M total)
Deals Lost: 23 ($2.8M total)
Average Deal Size: Won $100K | Lost $122K
Average Sales Cycle: Won 45 days | Lost 62 days

Key Insight: Losing more on larger deals, faster on smaller wins

---

WIN PATTERNS
============

Why We Won (Top Themes):
------------------------

1. STRONG CHAMPION (8 of 12 wins)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 67%

   Pattern: Deals with an engaged internal champion closed
   Examples:
   • Acme Corp - VP Ops drove evaluation internally
   • TechCo - CTO was previous customer at another company

   Insight: Champion development is critical path

2. CLEAR ROI STORY (7 of 12 wins)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 58%

   Pattern: Quantified value proposition with specific metrics
   Value props that worked:
   • "80% reduction in manual work" (used in 6 wins)
   • "ROI within 90 days" (used in 5 wins)
   • Customer-specific ROI calculation (used in 4 wins)

3. COMPETITIVE DIFFERENTIATION (5 of 12 wins)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 42%

   Competitors beaten:
   • Competitor A: 3 wins (we won on ease of use)
   • Competitor B: 2 wins (we won on integration)

   Key differentiators that closed:
   • "Implementation in weeks not months"
   • "Native Salesforce integration"

Objections We Overcame:
-----------------------
| Objection | Wins Where Raised | How We Won |
|-----------|-------------------|------------|
| Pricing | 4 | ROI calculator + pilot offer |
| Implementation | 3 | Customer references + timeline guarantee |
| Security | 2 | SOC2 cert + security review |

Proof Points That Closed:
-------------------------
1. "Customer X achieved 85% time savings" - cited in 5 wins
2. "Average 6-week implementation" - cited in 4 wins
3. Industry-specific reference - cited in 4 wins

---

LOSS PATTERNS
=============

Why We Lost (Top Themes):
-------------------------

1. LOST TO COMPETITOR (10 of 23 losses)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 43%

   Competitor breakdown:
   • Competitor A: 5 losses
     - Lost on: Price (3), Features (2)
     - Common objection: "They're 40% cheaper"

   • Competitor B: 3 losses
     - Lost on: Existing relationship (2), Brand (1)
     - Common objection: "We already use their other products"

   • Competitor C: 2 losses
     - Lost on: Specific feature gap

2. NO DECISION (8 of 23 losses)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 35%

   Pattern: Deal stalled, no budget, reprioritized
   Common signals:
   • "Budget got reallocated" (3x)
   • "Other projects took priority" (3x)
   • "Leadership change" (2x)

   Insight: Better qualification needed at discovery

3. UNRESOLVED OBJECTIONS (5 of 23 losses)
   ━━━━━━━━━━━━━━━━━━━━━━━━ 22%

   Objections that killed deals:
   • "Need on-prem option" (2 losses, $340K)
   • "Missing [specific integration]" (2 losses, $180K)
   • "Can't justify ROI to board" (1 loss, $200K)

Lost Deal Objections (Not Overcome):
------------------------------------
| Objection | Losses | Value Lost | Win Rate When Raised |
|-----------|--------|------------|---------------------|
| Price | 8 | $980K | 33% |
| Feature gap | 4 | $520K | 20% |
| No budget | 3 | $400K | 0% |
| Security/compliance | 2 | $280K | 50% |

---

COMPARATIVE ANALYSIS
====================

| Metric | Wins | Losses | Delta |
|--------|------|--------|-------|
| Avg deal size | $100K | $122K | Losing bigger deals |
| Sales cycle | 45 days | 62 days | Losses drag longer |
| Meetings held | 5.2 avg | 3.8 avg | Less engagement in losses |
| Stakeholders | 3.4 avg | 2.1 avg | Fewer contacts in losses |
| Champions | 67% had | 22% had | Champion is key |

Value Props Comparison:
| Value Prop | Used in Wins | Used in Losses | Effectiveness |
|------------|--------------|----------------|---------------|
| 80% time savings | 6 (50%) | 4 (17%) | HIGH |
| ROI in 90 days | 5 (42%) | 2 (9%) | HIGH |
| Easy implementation | 4 (33%) | 8 (35%) | MEDIUM |
| Enterprise security | 2 (17%) | 5 (22%) | LOW |

Insight: "Easy implementation" used equally but not a closer

---

RECOMMENDATIONS
===============

Immediate Actions:
1. ⚡ Address Competitor A pricing gap
   - Lost $600K to "40% cheaper" objection
   - Create TCO comparison showing hidden costs
   - Consider competitive pricing tier

2. ⚡ Improve qualification on budget
   - 35% of losses were "no decision"
   - Add budget confirmation earlier in process
   - Create "budget not confirmed" stage gate

3. ⚡ Double down on champion development
   - 67% win rate with champion vs 22% without
   - Add champion identification to discovery checklist
   - Create champion enablement materials

Library Updates Recommended:
1. UPDATE: Competitor A battlecard
   - Add: TCO comparison framework
   - Add: "40% cheaper" objection response

2. ADD: Proof point for on-prem concerns
   - Lost $340K on this objection
   - Need hybrid/security story

3. UPDATE: Discovery playbook
   - Add: Budget qualification questions
   - Add: Champion identification criteria

---

Want me to:
1. Deep dive on losses to Competitor A
2. Show specific deal details
3. Create updated battlecard content
4. Update library with recommendations
```

---

#### Loss Analysis (--status lost)

```
LOSS ANALYSIS: Last Quarter
===========================

23 Deals Lost | $2.8M Total Value

---

LOSS REASONS BREAKDOWN
----------------------

┌──────────────────────────────────────────────────────┐
│ Lost to Competitor     ██████████████████░░░░ 43% (10)│
│ No Decision            ██████████████░░░░░░░░ 35% (8) │
│ Unresolved Objection   █████████░░░░░░░░░░░░░ 22% (5) │
└──────────────────────────────────────────────────────┘

---

COMPETITOR LOSSES (10 deals, $1.3M)
-----------------------------------

COMPETITOR A (5 deals, $600K)
Primary loss reasons:
• Price (3 deals): "40% cheaper"
• Feature parity (2 deals): "Does everything you do"

Where they beat us:
• Lower price point
• Aggressive discounting
• Faster initial response

Where we SHOULD have won:
• Better integration story
• Stronger customer success
• More robust platform

Winnable if: We had addressed price earlier with TCO story

---

COMPETITOR B (3 deals, $480K)
Primary loss reasons:
• Existing relationship (2 deals): "Already using their CRM"
• Brand recognition (1 deal): "Safer choice"

Where they beat us:
• Bundle pricing with existing tools
• Executive relationships
• Brand trust with board

Winnable if: We had engaged earlier, before competitor expanded

---

NO DECISION LOSSES (8 deals, $1.1M)
-----------------------------------

Why deals died:
• Budget reallocation: 3 deals
• Priority shift: 3 deals
• Leadership change: 2 deals

Warning signs we missed:
• Long gaps between meetings (avg 18 days vs 7 in wins)
• Single-threaded (1.5 contacts vs 3.4 in wins)
• No executive sponsor identified

These were likely not real opportunities.
→ Recommendation: Improve qualification at discovery

---

UNRESOLVED OBJECTION LOSSES (5 deals, $720K)
--------------------------------------------

| Objection | Deals | Value | Could We Have Saved? |
|-----------|-------|-------|---------------------|
| Need on-prem | 2 | $340K | No - product gap |
| Missing integration | 2 | $180K | Maybe - roadmap item |
| ROI not clear | 1 | $200K | Yes - poor execution |

Product Feedback:
• On-prem: Lost $340K this quarter alone
• [Integration] gap: Lost $180K, requested 4x in calls

---

LOSS TIMELINE ANALYSIS
----------------------

Average days in each stage before loss:

Discovery → Demo: 12 days (vs 8 in wins)
Demo → Proposal: 18 days (vs 10 in wins)
Proposal → Decision: 32 days (vs 27 in wins)

Deals that drag past 45 days have 20% win rate
→ Create re-qualification checkpoint at day 45

---

PERSONAS IN LOST DEALS
----------------------

| Persona | Deals Lost | Win Rate Overall |
|---------|------------|------------------|
| CTO | 8 | 28% |
| VP Ops | 6 | 42% |
| CFO | 5 | 25% |
| Director | 4 | 38% |

CTO and CFO deals have lowest win rates
→ Review messaging for these personas

---

Want me to:
1. Show specific lost deal details
2. Create competitive counter-messaging
3. Build re-qualification checklist
4. Compare to previous quarter
```

---

#### Deal Deep Dive (--company)

```
DEAL DEEP DIVE: Acme Corp
=========================

Status: LOST
Amount: $180,000
Close Date: January 15, 2026
Lost To: Competitor A
Sales Cycle: 78 days

---

DEAL TIMELINE
-------------

Nov 1 - Inbound lead from CTO
Nov 8 - Discovery call (CTO + VP Eng)
Nov 15 - Technical demo (4 attendees)
Nov 22 - Security review call
Dec 5 - Proposal sent
Dec 12 - Pricing discussion (CFO joined)
Dec 20 - "Comparing with Competitor A"
Jan 5 - "Going with Competitor A"
Jan 15 - Deal marked lost

Red flags in hindsight:
⚠ Dec 12: CFO joined late - pricing concern
⚠ Dec 20: Competitor mentioned - should have addressed immediately
⚠ 14 days gap Dec 20 → Jan 5 - lost momentum

---

KEY CONVERSATIONS
-----------------

Discovery Call (Nov 8):
Findings:
• Pain: "Spending 30 hours/week on manual reporting"
• Goal: "Need real-time visibility into pipeline"
• Concern: "Budget is tight this year"

Signals missed: Budget concern mentioned early

---

Pricing Discussion (Dec 12):
Findings:
• Objection: "This is more than we budgeted"
• Objection: "Competitor A quoted 40% less"

Our response: "Let's focus on value..."
→ Should have: Offered pilot, provided TCO analysis

---

Final Call (Jan 5):
Findings:
• Decision: "Going with Competitor A"
• Reason: "Price was the deciding factor"
• Feedback: "Your product was better, but couldn't justify 40% premium"

---

WHAT WE DID WELL
----------------
✓ Strong technical demo - "best demo we've seen"
✓ Good rapport with CTO
✓ Security review passed quickly

WHAT WE MISSED
--------------
✗ Didn't address budget concern from Day 1
✗ CFO engaged too late (day 42)
✗ No TCO analysis provided
✗ Didn't set competitive trap early
✗ Lost to price, not product

---

LESSONS FOR NEXT TIME
---------------------

1. When prospect mentions budget is tight:
   → Immediately align on budget range
   → Position value before pricing
   → Identify economic buyer early

2. When competitor is mentioned:
   → Acknowledge directly
   → Set differentiation landmines
   → Provide TCO comparison proactively

3. For deals in this segment:
   → Engage CFO/finance earlier
   → Have ROI model ready by demo
   → Consider pilot offer for price-sensitive

---

LIBRARY IMPLICATIONS
--------------------

Update Competitor A battlecard:
• Add: "40% cheaper" response
• Add: TCO comparison framework
• Add: Trap questions about hidden costs

Update CTO persona:
• Add concern: "Justifying premium pricing"

Update Enterprise playbook:
• Add: CFO engagement requirement by Day 30
• Add: Budget qualification in discovery

---

Apply these updates?
```

### Step 5: Generate Recommendations

Based on analysis, offer actionable next steps:

```
Based on this analysis, I recommend:

IMMEDIATE ACTIONS
-----------------
1. Create Competitor A TCO battlecard section
   → /octave:pmm battlecard --competitor "Competitor A" --focus pricing

2. Update discovery checklist with budget qualification
   → /octave:library update pb_xxx --add "Budget qualification by meeting 2"

3. Review current pipeline for similar patterns
   → /octave:research --for pipeline-review

STRATEGIC RECOMMENDATIONS
-------------------------
1. Consider pricing/packaging review for competitive segment
2. Create "pilot program" offer for price-sensitive deals
3. Develop CFO-specific value story

Would you like me to execute any of these?
```

## MCP Tools Used

### Deal & Event Access
- `list_events` - Filter by DEAL_WON, DEAL_LOST
- `list_findings` - Get findings from won/lost deals
- `get_event_detail` - Get detailed event info with transcript/content

### Library Context
- `get_entity` - Get competitor, persona details
- `get_playbook` - Get playbook for recommendations
- `search_knowledge_base` - Find related content

### Library Updates
- `update_entity` - Apply recommendations to library

## Error Handling

**No Deals Found:**
> No won/lost deals found for this period.
>
> This could mean:
> 1. CRM integration isn't syncing deal outcomes
> 2. Date range has no closed deals
> 3. Filters are too restrictive
>
> Check your Octave CRM integration settings, or expand the date range.

**Missing Deal Data:**
> Deal found but limited conversation data.
>
> For better analysis, ensure:
> - Calls are being recorded and synced
> - Emails are connected
> - Findings extraction is enabled

## Related Skills

- `/octave:insights` - Broader findings across all events
- `/octave:analyzer` - Deep dive on specific conversations
- `/octave:battlecard` - Competitive battlecards from win/loss data
- `/octave:research` - Research for current pipeline deals
- `/octave:icp-refine` - Refine ICP definitions from deal patterns
- `/octave:enablement` - Turn win/loss learnings into training materials
