---
name: icp-refine
description: Analyze deal outcomes and conversation patterns to refine ICP definitions and targeting criteria. Use when user says "refine ICP", "who should we target", "update our ICP", "ideal customer profile", or asks why deals are being won or lost.
---

# /octave:icp-refine - ICP Intelligence

Analyze deal outcomes, conversation patterns, and qualification scores to refine your ICP definitions. Compares what your library says your ideal customer looks like against what actually wins — then recommends updates.

## Usage

```
/octave:icp-refine [--period <days>] [--segment <name>] [--focus wins|losses|both]
```

## Examples

```
/octave:icp-refine                                        # Full ICP analysis (last 180 days)
/octave:icp-refine --period 90                            # Last quarter
/octave:icp-refine --segment "Enterprise"                 # Specific segment
/octave:icp-refine --focus wins                           # Only analyze what's working
/octave:icp-refine --focus losses                         # Only analyze what's not working
```

## Instructions

When the user runs `/octave:icp-refine`:

### Step 1: Set Parameters

If no options specified, use defaults and confirm:

```
I'll analyze your deal data to refine your ICP.

Period: Last 180 days (change with --period)
Segments: All (change with --segment)
Focus: Wins and losses

Starting analysis...
```

### Step 2: Gather Current ICP Definition

```
# Get current segments (this IS the ICP definition)
list_all_entities({ entityType: "segment" })

# Get full segment details
get_entity({ oId: "<segment_oId>" })  // for each segment

# Get current personas
list_all_entities({ entityType: "persona" })
get_entity({ oId: "<persona_oId>" })  // for key personas

# Get products/services (what we're selling)
list_all_entities({ entityType: "product" })
list_all_entities({ entityType: "service" })
```

### Step 3: Analyze Deal Outcomes

```
# Get won deals
list_events({
  startDate: "<period start>",
  filters: {
    eventTypes: ["DEAL_WON"]
  }
})

# Get lost deals
list_events({
  startDate: "<period start>",
  filters: {
    eventTypes: ["DEAL_LOST"]
  }
})

# Get findings from won deals
list_findings({
  query: "why we won success factors decision criteria champion",
  startDate: "<period start>",
  eventFilters: {
    outcomeFilters: ["WON"]
  }
})

# Get findings from lost deals
list_findings({
  query: "why we lost objections blockers competition pricing",
  startDate: "<period start>",
  eventFilters: {
    outcomeFilters: ["LOST"]
  }
})

# Get positive conversation signals
list_findings({
  query: "excited interested positive resonated value",
  startDate: "<period start>",
  eventFilters: {
    sentiments: ["POSITIVE"]
  }
})

# Get negative signals
list_findings({
  query: "concerned hesitant not a fit wrong timing",
  startDate: "<period start>",
  eventFilters: {
    sentiments: ["NEGATIVE"]
  }
})
```

### Step 4: Analyze Patterns

For each won deal, extract:
- Company profile (industry, size, stage, tech stack)
- Persona(s) involved
- Pain points that resonated
- Value props that closed the deal
- Deal cycle length
- Deal size
- Competitors in the deal

For each lost deal, extract:
- Same attributes
- Why it was lost (competitor, timing, budget, fit, champion)

### Step 5: Generate ICP Refinement Report

```
ICP REFINEMENT REPORT
======================

Period: [Start] to [End]
Deals Analyzed: [N] won, [N] lost
Win Rate: [X%]

===================================

CURRENT ICP DEFINITION (from library)
-------------------------------------

Segment: [Segment Name]
  Industry: [Defined industries]
  Company Size: [Defined range]
  Stage: [Defined stage]
  Characteristics: [Key attributes]

Personas: [List current personas with titles]

---

WHAT THE DATA SHOWS
--------------------

WINNING CUSTOMER PROFILE
-------------------------
Based on [N] won deals:

Industry:
  [Industry 1]: [N] wins ([X%]) ← [matches/exceeds/below ICP definition]
  [Industry 2]: [N] wins ([X%])
  [Industry 3]: [N] wins ([X%])
  Surprise: [Any industry winning that's not in current ICP]

Company Size:
  [Range 1]: [N] wins ([X%])
  [Range 2]: [N] wins ([X%])
  Sweet Spot: [Most common size range in wins]
  Current ICP says: [What's defined] ← [Match/Mismatch]

Deal Size:
  Average: [$X]
  Median: [$X]
  Range: [$X - $Y]

Cycle Length:
  Average: [X days]
  Fastest: [X days] (what made it fast)
  Slowest: [X days] (what slowed it down)

Common Characteristics of Wins:
✓ [Pattern 1 — e.g., "Had a technical champion"]
✓ [Pattern 2 — e.g., "Were actively replacing a competitor"]
✓ [Pattern 3 — e.g., "Had budget approved before evaluation"]
✓ [Pattern 4 — e.g., "Multiple stakeholders engaged early"]

---

LOSING PROFILE (anti-ICP)
---------------------------
Based on [N] lost deals:

Common Characteristics of Losses:
✗ [Pattern 1 — e.g., "No clear champion"]
✗ [Pattern 2 — e.g., "Evaluated on price alone"]
✗ [Pattern 3 — e.g., "Single-threaded with junior evaluator"]
✗ [Pattern 4 — e.g., "No defined timeline or budget"]

Lost to Competitors:
  [Competitor 1]: [N] losses — Common reason: [reason]
  [Competitor 2]: [N] losses — Common reason: [reason]

Lost to Status Quo: [N] — Why: [common reason]
Lost to Budget/Timing: [N] — Why: [common reason]

---

PERSONA EFFECTIVENESS
---------------------

| Persona | Deals Involved | Win Rate | Avg Deal Size | Notes |
|---------|---------------|----------|-------------|-------|
| [Persona 1] | [N] | [X%] | [$X] | [Observation] |
| [Persona 2] | [N] | [X%] | [$X] | [Observation] |
| [Persona 3] | [N] | [X%] | [$X] | [Observation] |

Observations:
• [Persona X] has highest win rate — consider prioritizing
• [Persona Y] has low win rate — investigate why
• [Missing persona] appeared in [N] deals but isn't defined in library

---

VALUE PROP EFFECTIVENESS
-------------------------

What's resonating (from won deals):
1. "[Value prop]" — Mentioned in [N] wins, [X%] positive reactions
2. "[Value prop]" — Mentioned in [N] wins
3. "[Value prop]" — Mentioned in [N] wins

What's not landing (from lost deals):
1. "[Value prop]" — Failed to resonate in [N] losses
   Why: [Insight from conversation data]
2. "[Value prop]" — [Analysis]

---

GAPS: DEFINED ICP vs. REALITY
-------------------------------

UNDERWEIGHTED (winning but not in ICP):
⚠ [Industry/size/characteristic] — [N] wins but not defined as target
  Recommendation: [Add to ICP / investigate further]

OVERWEIGHTED (in ICP but not winning):
⚠ [Industry/size/characteristic] — [N] losses, only [N] wins
  Recommendation: [Narrow ICP / adjust approach / investigate]

MISSING SIGNALS (new qualification criteria):
⚠ [Signal] — Appears in [X%] of wins, absent in [X%] of losses
  Recommendation: Add as qualification criterion

DISQUALIFICATION SIGNALS (new anti-patterns):
🚫 [Signal] — Present in [X%] of losses
  Recommendation: Add as disqualification criterion

---

RECOMMENDED UPDATES
--------------------

SEGMENT UPDATES:
1. [Update 1] — "[Specific change to segment definition]"
   Evidence: [Data supporting this change]
   Impact: [Expected improvement]

2. [Update 2] — "[Specific change]"
   Evidence: [Data]

PERSONA UPDATES:
1. [Update 1] — "[Specific change to persona definition]"
   Evidence: [Data]

2. [New persona suggestion] — "[Why we should add this persona]"
   Evidence: [Appeared in N deals, X% win rate]

PLAYBOOK UPDATES:
1. [Update 1] — "[Add/modify value props based on what resonates]"
2. [Update 2] — "[Update objection handling based on loss patterns]"

QUALIFICATION CRITERIA UPDATES:
Add:
+ [New criterion] — "[Why: seen in X% of wins]"
+ [New criterion] — "[Why]"

Remove or de-emphasize:
- [Criterion] — "[Why: not predictive of wins]"

---

Apply these updates?

1. Apply segment updates
2. Apply persona updates
3. Apply playbook updates
4. Apply all updates
5. Review specific recommendation first
6. Export report only
```

### Step 6: Apply Updates (if requested)

```
# Update segment
update_entity({
  entityType: "segment",
  oId: "<segment_oId>",
  instructions: "<specific updates based on findings>"
})

# Update persona
update_entity({
  entityType: "persona",
  oId: "<persona_oId>",
  instructions: "<specific updates>"
})

# Update playbook value props
update_value_props({
  playbookOId: "<playbook_oId>",
  updates: [{ oId: "<vp_oId>", details: "<updated details>" }],
  reasoning: "Updated based on ICP refinement analysis: [evidence]"
})

# Create new persona if recommended
create_entity({
  entityType: "persona",
  name: "<new persona name>",
  instructions: "<details from deal analysis>"
})
```

### Step 7: Offer Follow-Up Actions

```
What would you like to do next?

1. Deep dive on a specific finding
2. Analyze a specific segment or persona
3. Compare current quarter vs. previous
4. Update a specific library entity
5. Generate updated enablement materials
6. Export the full report
7. Done
```

## MCP Tools Used

### Library Context
- `list_all_entities` - Segments, personas, products
- `get_entity` - Full entity details for ICP definition

### Deal Analytics
- `list_events` - Won/lost deals
- `list_findings` - Conversation insights, objections, signals
- `get_event_detail` - Deep dive into specific deals

### Library Updates
- `update_entity` - Update segments, personas
- `update_value_props` - Update playbook value props
- `create_entity` - New personas or segments

### Intelligence
- `search_knowledge_base` - Cross-reference patterns

## Error Handling

**No Deal Data:**
> No deal outcomes found in the last [N] days.
>
> ICP refinement requires win/loss data.
> Options:
> 1. Extend the time period (try --period 365)
> 2. Review conversation data instead (calls/emails without deal outcomes)
> 3. Do a manual ICP review using your library definitions

**Insufficient Data:**
> Found only [N] deals. Statistical patterns may not be reliable.
>
> I'll highlight patterns but flag low-confidence findings.
> Consider extending the period or combining with qualitative analysis.

**No Segments Defined:**
> No segments found in your library.
>
> I can still analyze deal patterns, but there's nothing to compare against.
> Consider creating segments first: `/octave:library create segment`
> Or I'll suggest segment definitions based on the deal data.

## Related Skills

- `/octave:wins-losses` - Deeper win/loss analysis (complements ICP refinement)
- `/octave:insights` - Field intelligence trends
- `/octave:prospector` - Use refined ICP to find new prospects
- `/octave:audit` - Check library health after updates
- `/octave:library` - Manually update entities
