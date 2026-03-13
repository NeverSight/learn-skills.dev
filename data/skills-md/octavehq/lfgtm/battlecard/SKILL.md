---
name: battlecard
description: Generate competitive battlecards, displacement campaigns, trap questions, and objection counters as text-based analysis grounded in library data and real deal evidence. Use when user says "battlecard for [competitor]", "how do we beat [competitor]", "competitive intel", "trap questions", "displacement campaign", or mentions competing against a rival. Do NOT use for visual HTML battlecard documents — use /octave:battlecard-doc instead.
---

# /octave:battlecard - Competitive War Room

Dedicated competitive intelligence skill that generates living competitive artifacts — battlecards, displacement campaigns, trap questions, objection counters, and side-by-side comparisons — all grounded in your library's competitive data and real conversation evidence.

## Usage

```
/octave:battlecard [mode] [--competitor <name>] [--persona <name>]
```

## Modes

```
/octave:battlecard                                        # Interactive - pick competitor and mode
/octave:battlecard battlecard --competitor "Acme"         # Full competitive battlecard
/octave:battlecard displacement --competitor "Acme"       # Displacement campaign
/octave:battlecard traps --competitor "Acme"              # Trap questions to expose weaknesses
/octave:battlecard objections --competitor "Acme"         # "They say X, we say Y" guide
/octave:battlecard compare --competitor "Acme"            # Side-by-side comparison
/octave:battlecard landscape                              # Full competitive landscape overview
```

## Instructions

When the user runs `/octave:battlecard`:

### Step 1: Identify Competitor and Mode

If no competitor specified, list available competitors:

```
# Get all competitors
list_all_entities({ entityType: "competitor" })
```

Present:
```
Which competitor are you focused on?

COMPETITORS IN YOUR LIBRARY
1. [Competitor 1] - [Brief description]
2. [Competitor 2] - [Brief description]
3. [Competitor 3] - [Brief description]

OTHER
4. Research a new competitor (provide name/domain)
5. Full competitive landscape (all competitors)

Your choice:
```

If no mode specified, ask:
```
What do you need?

1. Full Battlecard - Comprehensive positioning guide for sales
2. Displacement Campaign - Outreach to steal their customers
3. Trap Questions - Discovery questions that expose their weaknesses
4. Objection Counters - "They say X, we say Y" paired responses
5. Side-by-Side Compare - Feature/capability comparison
6. Competitive Landscape - Overview of all competitors

Your choice:
```

### Step 2: Gather Competitive Intelligence

```
# Get competitor entity
get_entity({ oId: "<competitor_oId>" })

# Search for playbooks that mention this competitor
search_knowledge_base({
  query: "<competitor name> competitive positioning",
  entityTypes: ["playbook"]
})

# Get relevant playbook with value props
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Search for proof points (especially competitive wins)
search_knowledge_base({
  query: "<competitor name> win switch migration",
  entityTypes: ["proof_point", "reference"]
})

# Search conversation data for competitor mentions
list_findings({
  query: "<competitor name> objections competitive mentions",
  startDate: "<90 days ago>",
  eventFilters: {
    competitors: ["<competitor_oId>"]
  }
})

# Get won deals where this competitor was present
list_events({
  startDate: "<180 days ago>",
  filters: {
    eventTypes: ["DEAL_WON"],
    competitors: ["<competitor_oId>"]
  }
})

# Get lost deals to this competitor
list_events({
  startDate: "<180 days ago>",
  filters: {
    eventTypes: ["DEAL_LOST"],
    competitors: ["<competitor_oId>"]
  }
})

# Get product details for comparison
list_all_entities({ entityType: "product" })
get_entity({ oId: "<product_oId>" })
```

### Step 3: Generate Mode-Specific Output

---

#### Mode: Full Battlecard

```
BATTLECARD: [Your Product] vs [Competitor]
==========================================

Last Updated: [Date]
Based on: [N] deal outcomes, [N] conversation mentions

---

QUICK POSITIONING
-----------------
When you hear: "[Competitor name]"
Lead with: "[Key differentiator in one sentence]"

30-Second Pitch:
"[Elevator pitch that positions against this competitor]"

---

COMPETITOR OVERVIEW
-------------------
What they do: [Brief description from library]
Target market: [Their focus]
Pricing: [If known]
Key customers: [Notable logos]
Recent moves: [Latest news, features, funding]

---

WHERE WE WIN
------------
| Capability | Us | Them |
|------------|-----|------|
| [Area 1] | ✓ [Our strength] | ✗ [Their weakness] |
| [Area 2] | ✓ [Our strength] | ~ [Partial/weaker] |
| [Area 3] | ✓ [Our strength] | ✗ [Their gap] |

Win Themes (from real deals):
1. [Theme 1] — "[Evidence from conversation data]"
2. [Theme 2] — "[Evidence from conversation data]"
3. [Theme 3] — "[Evidence from conversation data]"

---

WHERE THEY WIN (BE HONEST)
--------------------------
| Capability | Them | Our Response |
|------------|------|-------------|
| [Area] | ✓ [Their strength] | [How we counter/reframe] |

How to handle:
• "[Their advantage]" → "[Reframe that shifts the conversation]"

---

COMMON OBJECTIONS
-----------------

"[Competitor] is cheaper"
→ [Response: value, TCO, hidden costs, proof point]

"[Competitor] has [feature X]"
→ [Response: why it matters/doesn't, our alternative approach]

"We already use [Competitor]"
→ [Displacement angle: migration story, switching cost offset]

"[Competitor] has more [integrations/customers/etc.]"
→ [Response: quality vs quantity, specific advantage]

Evidence: [Cite real objections from conversation data if available]

---

TRAP QUESTIONS
--------------
Ask these to expose their weaknesses:

1. "[Question targeting known weakness]"
   Why: [What this reveals]
   If they say: "[Likely response]" → You say: "[Follow-up]"

2. "[Question about scalability/support/depth]"
   Why: [What this reveals]

3. "[Question about specific capability gap]"
   Why: [What this reveals]

---

LANDMINES TO SET
----------------
Plant these criteria early in the evaluation:

1. "[Evaluation criterion]" — plays to our strength in [area]
2. "[Technical requirement]" — exposes their limitation in [area]
3. "[Process question]" — highlights our advantage in [area]

---

PROOF POINTS
------------
• [Customer who switched from competitor] — [Outcome]
• [Metric: "X% better than [competitor] in Y"]
• [Industry analyst or review quote]
• [Head-to-head evaluation win]

---

DISPLACEMENT SUCCESS STORY
---------------------------
[Customer] switched from [Competitor] because:
• [Reason 1]
• [Reason 2]
Results after switching:
• [Metric improvement]
• [Time saved / value gained]

---

DEAL WIN/LOSS PATTERNS
-----------------------
Wins against [Competitor]: [N] in last 180 days
Losses to [Competitor]: [N] in last 180 days
Win Rate: [X%]

Common win factors:
• [Factor 1]
• [Factor 2]

Common loss factors:
• [Factor 1]
• [Factor 2]

---

Sources Used:
- Competitor entity: [name]
- Deals analyzed: [N] wins, [N] losses
- Conversation mentions: [N]
- Proof points: [list]
- Playbooks: [list]

---

Want me to:
1. Deep dive on a specific objection
2. Generate displacement outreach
3. Create persona-specific version
4. Add more trap questions
5. Update the competitor entity with new insights
```

---

#### Mode: Displacement Campaign

```
generate_email({
  person: { firstName: "[Persona Name]", jobTitle: "[Persona Title]" },
  numEmails: 4,
  sequenceType: "COLD_OUTBOUND",
  allEmailsContext: "This person currently uses [Competitor]. Key competitor weaknesses: [list]. Our advantages: [list]. Proof of successful switches: [proof points]. Do NOT name the competitor unless the prospect mentions them first.",
  allEmailsInstructions: "Displacement campaign. Progressive structure: Email 1: Pain-point their current tool likely causes. Email 2: Vision of what's possible (results from switchers). Email 3: Specific differentiation without naming competitor. Email 4: Direct offer with migration support."
})
```

Present as:
```
DISPLACEMENT CAMPAIGN: [Your Product] vs [Competitor]
=====================================================

Target: [Persona] currently using [Competitor]
Strategy: [Lead with pain, prove with results, close with support]

---

POSITIONING STRATEGY
--------------------
Don't lead with: "[Competitor] is bad"
Lead with: "[Pain they're likely experiencing because of competitor limitations]"

Key angles:
1. [Pain point caused by competitor weakness]
2. [Results achieved by companies who switched]
3. [Capability they're missing]

---

EMAIL 1: [Subject]
Timing: Day 1 | Angle: Pain recognition
---
[Email body]

EMAIL 2: [Subject]
Timing: Day 4 | Angle: Social proof from switchers
---
[Email body]

EMAIL 3: [Subject]
Timing: Day 8 | Angle: Differentiation
---
[Email body]

EMAIL 4: [Subject]
Timing: Day 12 | Angle: Migration offer
---
[Email body]

---

LINKEDIN COMPANION MESSAGES
----------------------------
Connection note: [Short message]
Follow-up: [After connection]

---

TALK TRACK (if they respond)
-----------------------------
Opening: "[How to start the conversation]"
Discovery: "[Questions to understand their pain with current tool]"
Transition: "[How to introduce your solution]"
Close: "[Specific next step to offer]"

---

Sources: [Competitor entity, proof points, deal data]
```

---

#### Mode: Trap Questions

```
TRAP QUESTIONS: vs [Competitor]
================================

Use these discovery questions to expose [Competitor]'s weaknesses
without mentioning them directly.

---

QUESTION 1: [Area of weakness]
"[Natural discovery question]"

Why this works: [Competitor] struggles with [X], so their answer reveals gaps.
If they say "[typical response]": Follow up with "[deeper question]"
Our advantage: [What we do better here]

---

QUESTION 2: [Area of weakness]
"[Natural discovery question]"

Why this works: [Explanation]
If they say "[typical response]": Follow up with "[deeper question]"
Our advantage: [What we do better]

---

[Continue for 5-8 questions]

---

SEQUENCING ADVICE
-----------------
Ask in this order for maximum impact:
1. [Question N] — establishes [criterion] as important
2. [Question N] — builds on first, reveals gap
3. [Question N] — introduces area where we dominate

---

Sources: [Competitor weaknesses, deal win patterns, conversation data]
```

---

#### Mode: Objection Counters

```
OBJECTION COUNTERS: vs [Competitor]
====================================

PRICING OBJECTIONS
------------------

"[Competitor] is cheaper"
→ [Response with TCO analysis, value framing]
  Proof: "[Customer quote or metric]"

"We don't have budget to switch"
→ [Response about migration support, ROI timeline]
  Proof: "[Switching ROI proof point]"

---

FEATURE OBJECTIONS
------------------

"[Competitor] has [Feature X]"
→ [Response: our approach, why ours is better/different]
  Proof: "[Evidence]"

"[Competitor] integrates with [Tool Y]"
→ [Response about our integrations or API]
  Proof: "[Evidence]"

---

RELATIONSHIP OBJECTIONS
-----------------------

"We've been with [Competitor] for years"
→ [Response: switching cost vs. opportunity cost]
  Proof: "[Long-time customer who finally switched]"

"Our team knows [Competitor]"
→ [Response: onboarding experience, time to value]
  Proof: "[Evidence]"

---

RISK OBJECTIONS
---------------

"Switching is too risky"
→ [Response: migration support, phased approach]
  Proof: "[Smooth migration story]"

---

FROM REAL CONVERSATIONS
-----------------------
[If conversation data available, cite actual objections heard and what worked]

• "[Real objection from call]" — Handled by: [rep name/approach] — Outcome: [won/lost]

---

Sources: [Competitor entity, conversation findings, deal outcomes]
```

---

#### Mode: Side-by-Side Compare

```
COMPARISON: [Your Product] vs [Competitor]
==========================================

| Category | [Your Product] | [Competitor] |
|----------|---------------|-------------|
| [Category 1] | [Our capability] | [Their capability] |
| [Category 2] | [Our capability] | [Their capability] |
| [Category 3] | [Our capability] | [Their capability] |
| ... | ... | ... |

DETAILED COMPARISON
-------------------

[Category 1]: [Category Name]
Us: [Detailed description of our approach]
Them: [Detailed description of their approach]
Verdict: [Where each wins and why it matters]

[Repeat for each major category]

---

SUMMARY
-------
Choose [Your Product] when: [Scenarios where you win]
[Competitor] may be better when: [Be honest about their strengths]

---

Sources: [Competitor entity, product entity, proof points]
```

---

#### Mode: Competitive Landscape

```
COMPETITIVE LANDSCAPE
=====================

[Fetch all competitors and generate overview]

MARKET MAP
----------
| Competitor | Focus | Threat Level | Our Win Rate |
|-----------|-------|-------------|-------------|
| [Comp 1] | [Focus] | [High/Med/Low] | [X%] |
| [Comp 2] | [Focus] | [High/Med/Low] | [X%] |
| [Comp 3] | [Focus] | [High/Med/Low] | [X%] |

KEY THEMES
----------
• [Common competitive dynamic 1]
• [Common competitive dynamic 2]
• [Market trend affecting competition]

PER-COMPETITOR SNAPSHOT
-----------------------
[Short battlecard summary for each competitor]

---

Want me to deep-dive on any competitor?
```

### Step 4: Offer Follow-Up Actions

```
What would you like to do next?

1. Deep dive on a specific area
2. Generate displacement outreach for a specific person
3. Create a persona-specific version
4. Re-generate any piece using a saved agent
5. Update competitor entity with new insights
6. Share with team (export)
7. Done
```

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Competitive Intelligence
- `list_all_entities` (competitor) - List all competitors
- `get_entity` - Get competitor details
- `search_knowledge_base` - Find competitive positioning, proof points
- `list_findings` - Real conversation mentions and objections
- `list_events` - Deal win/loss data against competitor
- `get_event_detail` - Deep dive into specific competitive deals

### Library Context
- `get_playbook` - Competitive playbooks and value props
- `list_value_props` - Value propositions per persona
- `get_entity` (product) - Product capabilities for comparison

### Content Generation
- `generate_email` - Displacement email campaigns
- `generate_content` - Trap questions, objection guides, comparisons

## Error Handling

**No Competitors in Library:**
> No competitors found in your library.
>
> Options:
> 1. Add a competitor first: `/octave:library create competitor`
> 2. Tell me the competitor name and I'll create a basic comparison

**No Deal Data:**
> No win/loss data found against [Competitor].
>
> I'll build the battlecard from library data and general positioning.
> As you log deals, the battlecard will get richer with real evidence.

**Competitor Not in Library:**
> "[Name]" isn't in your library yet.
>
> Options:
> 1. Create the competitor entity first: `/octave:library create competitor "[name]"`
> 2. I'll generate a basic comparison with available information

## Related Skills

- `/octave:research` - Research a specific account in a competitive deal
- `/octave:campaign` - Generate competitive campaign content
- `/octave:insights` - Surface competitive mentions from conversations
- `/octave:wins-losses` - Analyze win/loss patterns against competitors
- `/octave:enablement` - Package competitive intel for the team
