---
name: enablement
description: Generate sales enablement materials — cheat sheets, objection guides, discovery question banks, competitive sheets, and onboarding kits from your library. Use when user says "cheat sheet", "objection guide", "discovery questions", "onboarding kit", "enablement materials", or asks for quick-reference sales tools.
---

# /octave:enablement - Sales Enablement Studio

Generate consumable sales enablement materials — quick reference cards, objection handling guides, discovery question banks, competitive cheat sheets, and onboarding kits — all grounded in your library data and real conversation evidence.

## Usage

```
/octave:enablement [type] [--persona <name>] [--competitor <name>] [--product <name>]
```

## Content Types

```
/octave:enablement                                        # Interactive mode
/octave:enablement quick-ref                              # Quick reference card
/octave:enablement objections                             # Objection handling guide
/octave:enablement discovery                              # Discovery question bank
/octave:enablement competitive-sheet                      # Competitive cheat sheet
/octave:enablement onboarding                             # New hire enablement kit
/octave:enablement persona-guide                          # Persona deep-dive for reps
/octave:enablement playbook-summary                       # Playbook quick reference
```

## Instructions

When the user runs `/octave:enablement`:

### Step 1: Determine Content Type

If no type specified, ask:

```
What enablement material do you need?

DAILY REFERENCE
1. Quick Reference Card - One-page cheat sheet for a topic
2. Objection Handling Guide - "They say X, we say Y" from real conversations
3. Discovery Question Bank - Questions organized by persona and stage

COMPETITIVE
4. Competitive Cheat Sheet - Pocket-sized competitive positioning guide

TEAM DEVELOPMENT
5. New Hire Onboarding Kit - Library walkthrough + essentials for new reps
6. Persona Deep-Dive - Everything a rep needs to know about selling to a persona
7. Playbook Quick Reference - Condensed playbook for quick consumption

Your choice:
```

Then ask for focus:
```
What's the focus?

1. Specific persona: [List personas]
2. Specific product: [List products]
3. Specific competitor: [List competitors]
4. Specific playbook: [List playbooks]
5. General / all
```

### Step 2: Gather Intelligence

Enablement materials are unique because they blend library data with conversation evidence:

```
# Get the focus entity
get_entity({ oId: "<entity_oId>" })

# Get related playbook
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Get real objections from conversations
list_findings({
  query: "objections pushback concerns hesitation",
  startDate: "<180 days ago>",
  eventFilters: {
    personas: ["<persona_oId>"]  // if persona-focused
  }
})

# Get positive signals (what's working)
list_findings({
  query: "positive reaction excited interested resonated",
  startDate: "<180 days ago>",
  eventFilters: {
    sentiments: ["POSITIVE"]
  }
})

# Get pain points mentioned
list_findings({
  query: "pain points challenges frustrations problems",
  startDate: "<180 days ago>"
})

# Get proof points
search_knowledge_base({
  query: "<focus area> results metrics",
  entityTypes: ["proof_point", "reference"]
})

# Get competitors for context
list_all_entities({ entityType: "competitor" })

# Get brand voice
list_brand_voices()
```

### Step 3: Generate Content Type

---

#### Type: Quick Reference Card

```
generate_content({
  instructions: "Create a quick reference card for sales reps about [focus area].
    Format: Single-page cheat sheet. Scannable. No fluff.
    Sections: Key stats, elevator pitch, top 3 pain points, top 3 value props,
    proof points, common objections (brief), recommended CTA.
    Keep each item to 1-2 lines max.",
  customContext: "<library + conversation data>"
})
```

Present as:
```
QUICK REFERENCE: [Topic]
=========================

ELEVATOR PITCH
--------------
"[30-second pitch]"

---

KEY STATS
---------
• [Stat 1]
• [Stat 2]
• [Stat 3]

---

TOP PAIN POINTS (what they're feeling)
--------------------------------------
1. [Pain point] — Ask: "[Discovery question]"
2. [Pain point] — Ask: "[Discovery question]"
3. [Pain point] — Ask: "[Discovery question]"

---

VALUE PROPS (what we solve)
---------------------------
1. [Value prop] — Proof: "[Evidence]"
2. [Value prop] — Proof: "[Evidence]"
3. [Value prop] — Proof: "[Evidence]"

---

QUICK OBJECTION HANDLING
-------------------------
"[Objection 1]" → "[One-line response]"
"[Objection 2]" → "[One-line response]"
"[Objection 3]" → "[One-line response]"

---

RECOMMENDED CTA
---------------
First meeting: "[CTA]"
Follow-up: "[CTA]"

---

Sources: [Library entities used]
```

---

#### Type: Objection Handling Guide

```
OBJECTION HANDLING GUIDE: [Focus Area]
=======================================

[Source: Library intelligence + real conversation data]

---

PRICING OBJECTIONS
------------------

"It's too expensive"
Frequency: [High/Med/Low based on conversation data]
Response: "[Detailed response with reframe]"
Follow-up: "[Probing question]"
Proof: "[Evidence that overcomes this]"
From the field: "[Real example of handling this successfully, if available]"

"We don't have budget"
Frequency: [High/Med/Low]
Response: "[Response]"
Follow-up: "[Question]"
Proof: "[Evidence]"

---

PRODUCT/FEATURE OBJECTIONS
---------------------------

"We need [feature X]"
Frequency: [High/Med/Low]
Response: "[Response — acknowledge, reframe, alternative]"
Follow-up: "[Question to understand underlying need]"
Proof: "[Evidence]"

"It seems complex"
Frequency: [High/Med/Low]
Response: "[Response]"
Proof: "[Time-to-value metric, implementation story]"

---

COMPETITIVE OBJECTIONS
----------------------

"We're already using [Competitor]"
Frequency: [High/Med/Low]
Response: "[Displacement angle]"
Follow-up: "[Question to uncover dissatisfaction]"
Proof: "[Switching success story]"

"[Competitor] is better at [X]"
Frequency: [High/Med/Low]
Response: "[Honest counter with reframe]"
Proof: "[Evidence]"

---

TIMING/PRIORITY OBJECTIONS
----------------------------

"Not the right time"
Response: "[Response — create urgency without pressure]"
Follow-up: "[Question about triggers/timeline]"

"We have other priorities"
Response: "[Response — connect to their priorities]"
Follow-up: "[Question to understand priorities]"

---

STATUS QUO OBJECTIONS
---------------------

"What we have works fine"
Response: "[Response — challenge the status quo]"
Follow-up: "[Question to surface hidden pain]"
Proof: "[Cost of doing nothing metric]"

---

WIN/LOSS EVIDENCE
-----------------
[If conversation data available:]

Objections in WON deals (we overcame these):
• "[Objection]" — Won by: [approach/what worked]

Objections in LOST deals (we failed to overcome):
• "[Objection]" — Lost because: [what went wrong]
• Lesson: [What to do differently]

---

Sources: [Conversation findings, competitor entities, proof points]

---

Want me to:
1. Deep dive on a specific objection
2. Role-play objection scenarios
3. Add objections for a specific competitor
4. Create a training exercise from these objections
```

---

#### Type: Discovery Question Bank

```
DISCOVERY QUESTION BANK: [Focus Area]
=======================================

---

OPENING / RAPPORT
-----------------
• "[Question about their role/background]"
• "[Question about recent company news]"
• "[Open-ended question about their day-to-day]"

---

PAIN POINT EXPLORATION
-----------------------

[Pain Point 1]: [Description from persona]
• "[Primary question]"
  → Listen for: [Signals that confirm this pain]
  → Follow up: "[Deeper question]"

• "[Alternative angle on same pain]"
  → Listen for: [Different signals]

[Pain Point 2]: [Description]
• "[Primary question]"
  → Listen for: [Signals]
  → Follow up: "[Deeper question]"

[Pain Point 3]: [Description]
• "[Primary question]"
  → Listen for: [Signals]

---

CURRENT SOLUTION / PROCESS
----------------------------
• "How are you handling [process] today?"
  → Listen for: [Tool names, manual processes, frustrations]

• "What does your team spend the most time on?"
  → Listen for: [Time sinks that your product solves]

• "What would you change about your current approach?"
  → Listen for: [Openness to change, specific gaps]

---

IMPACT / URGENCY
-----------------
• "What happens if this problem doesn't get solved?"
  → Listen for: [Business impact, personal impact]

• "How does this affect [their team / their goals / the business]?"
  → Listen for: [Scale of impact]

• "Is this something you're actively trying to solve, or more of a 'nice to have'?"
  → Listen for: [Priority level, budget signals]

---

QUALIFICATION (BANT/MEDDIC)
-----------------------------
Budget:
• "[Budget question appropriate for this persona]"

Authority:
• "Who else would be involved in evaluating this?"
• "How does your team typically make decisions like this?"

Need:
• "[Already covered in pain exploration]"

Timeline:
• "Is there a specific timeline you're working toward?"
• "What would trigger you to make a change?"

---

COMPETITIVE DISCOVERY
---------------------
• "Have you looked at other solutions?"
  → If yes: "[Follow-up about what they liked/didn't]"
  → If no: "[Follow-up about evaluation criteria]"

• "What's most important to you in a solution like this?"
  → Listen for: [Criteria we win on vs. competitor wins on]

---

CLOSING QUESTIONS
-----------------
• "Based on what we've discussed, does this seem like it could help?"
• "What would need to be true for you to move forward?"
• "What's the best next step from here?"

---

FROM THE FIELD
--------------
[If conversation data available:]
Questions that led to positive outcomes:
• "[Question]" — Used in [N] won deals
• "[Question]" — Frequently surfaces real pain

Questions to avoid:
• "[Question]" — Tends to [kill momentum / confuse / derail]

---

Sources: [Personas, playbooks, conversation findings, deal outcomes]
```

---

#### Type: Competitive Cheat Sheet

```
COMPETITIVE CHEAT SHEET
========================

[Condensed from battlecard intelligence for quick reference]

| Competitor | Quick Counter | Our Advantage |
|-----------|--------------|---------------|
| [Comp 1] | "[One-liner]" | [Key strength] |
| [Comp 2] | "[One-liner]" | [Key strength] |
| [Comp 3] | "[One-liner]" | [Key strength] |

---

PER COMPETITOR (abbreviated)

[Competitor 1]
When they say: "[Claim]" → We say: "[Counter]"
Trap question: "[Question]"
Best proof: "[Proof point]"

[Competitor 2]
When they say: "[Claim]" → We say: "[Counter]"
Trap question: "[Question]"
Best proof: "[Proof point]"

---

Sources: [Competitor entities, deal data, conversation findings]
```

---

#### Type: New Hire Onboarding Kit

```
NEW HIRE ENABLEMENT KIT
========================

Welcome to [Product/Company] sales! Here's everything you need.

---

1. THE PRODUCT
--------------
What we do: [2-3 sentence overview]
How we're different: [Key differentiators]
Our customers: [Profile of ideal customer]

---

2. WHO WE SELL TO
-----------------
[For each persona:]
[Persona Name]: [Title]
They care about: [Top 3 priorities]
Their pain: [Top 3 pain points]
Our value to them: [Top value prop]

---

3. HOW WE WIN
--------------
Common win factors:
• [Factor 1]
• [Factor 2]
• [Factor 3]

Common loss factors:
• [Factor 1] — How to avoid: [tip]
• [Factor 2] — How to avoid: [tip]

---

4. COMPETITORS TO KNOW
-----------------------
[For each competitor: one-paragraph summary]

---

5. KEY PROOF POINTS
--------------------
• [Top proof point 1]
• [Top proof point 2]
• [Top proof point 3]

---

6. PLAYBOOKS
------------
[For each playbook: 2-3 sentence summary and when to use]

---

7. TOP OBJECTIONS
-----------------
[Top 5 objections with brief responses]

---

8. TOOLS & RESOURCES
---------------------
• Octave Library: Your GTM knowledge base
• Key skills: /octave:research, /octave:generate, /octave:battlecard

---

Sources: [Full library scan]
```

---

#### Type: Persona Deep-Dive

```
PERSONA GUIDE: [Persona Name]
==============================

[Everything a rep needs to know about selling to this persona]

PROFILE
-------
Title: [Common titles]
Reports to: [Typical reporting line]
Team: [Typical team composition]
KPIs: [What they're measured on]

---

WHAT THEY CARE ABOUT
---------------------
1. [Priority 1] — [Why and context]
2. [Priority 2] — [Why and context]
3. [Priority 3] — [Why and context]

---

PAIN POINTS
-----------
[Detailed pain points with context on how to uncover each]

---

HOW TO SELL TO THEM
--------------------
Opening: [Best approach]
Discovery: [Key questions]
Value prop: [What resonates]
Proof: [Best evidence]
Objections: [Common + responses]
CTA: [Best next step]

---

MESSAGING DOS AND DON'TS
--------------------------
✓ Do: [Effective messaging approaches]
✗ Don't: [What turns them off]

---

FROM REAL CONVERSATIONS
-----------------------
[Insights from conversation data about this persona]

---

Sources: [Persona entity, playbooks, conversation findings]
```

---

#### Type: Playbook Quick Reference

```
PLAYBOOK QUICK REFERENCE: [Playbook Name]
==========================================

[Condensed, scannable version of the full playbook]

PURPOSE: [When to use this playbook]

TARGET: [Persona] at [Segment]

KEY INSIGHT: [Playbook's central thesis]

VALUE PROPS:
1. [VP 1] — Proof: [Evidence]
2. [VP 2] — Proof: [Evidence]
3. [VP 3] — Proof: [Evidence]

DISCOVERY QUESTIONS:
• [Top question 1]
• [Top question 2]
• [Top question 3]

OBJECTIONS:
• "[Objection]" → "[Response]"
• "[Objection]" → "[Response]"

COMPETITIVE ANGLE:
vs [Competitor]: [One-line positioning]

RECOMMENDED CTA: [Best next step to propose]

---

Sources: [Playbook entity, value props]
```

### Step 4: Offer Follow-Up Actions

```
What would you like to do next?

1. Create another enablement piece
2. Re-generate any piece using a saved agent
3. Create a version for a different persona/product
4. Combine into a full enablement package
5. Export as a document
6. Done
```

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Library Context
- `list_all_entities` - All entity types for comprehensive coverage
- `get_entity` - Full entity details
- `get_playbook` - Playbook with value props
- `list_value_props` - Value propositions
- `search_knowledge_base` - Proof points, references, messaging

### Conversation Evidence
- `list_findings` - Real objections, pain points, signals from calls/emails
- `list_events` - Deal outcomes for win/loss evidence
- `get_event_detail` - Specific interaction details

### Content Generation
- `generate_content` - All enablement content types
- `list_brand_voices` - Brand voice consistency

## Error Handling

**No Conversation Data:**
> No conversation data available yet.
>
> I'll generate enablement materials from your library.
> As your team logs calls and emails, these materials will get richer
> with real-world evidence.

**No Competitors:**
> No competitors in your library for competitive enablement.
>
> Options:
> 1. Add competitors: `/octave:library create competitor`
> 2. Skip competitive sections
> 3. I'll create a general competitive awareness template

**Empty Library:**
> Your library needs more content for a comprehensive enablement kit.
>
> Start with:
> 1. `/octave:library create product` - Add your product
> 2. `/octave:library create persona` - Add buyer personas
> Then run this skill again.

## Related Skills

- `/octave:train` - Practice with role-play simulations and quizzes using your enablement content
- `/octave:battlecard` - Full competitive intelligence (deeper than cheat sheet)
- `/octave:insights` - Surface field intelligence trends
- `/octave:wins-losses` - Win/loss patterns for objection effectiveness
- `/octave:pmm` - Marketing collateral (different audience than enablement)
- `/octave:research` - Deep research for specific accounts
