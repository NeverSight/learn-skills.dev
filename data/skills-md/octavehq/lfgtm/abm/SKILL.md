---
name: abm
description: Account-based planning with stakeholder mapping, persona matching, and coordinated outreach strategy. Use when user says "plan for [company]", "account plan", "stakeholder map", "ABM strategy", or mentions targeting a specific named company.
---

# /octave:abm - Account Planner

Create comprehensive account plans for target accounts by combining deep research, stakeholder mapping, persona matching, and coordinated outreach — all grounded in your library's playbooks and proof points.

## Usage

```
/octave:abm <company> [--stakeholders <N>] [--playbook <name>] [--depth quick|full]
```

## Examples

```
/octave:abm acme.com                                      # Full account plan
/octave:abm acme.com --stakeholders 5                     # Map top 5 stakeholders
/octave:abm acme.com --playbook "Enterprise"              # Use specific playbook
/octave:abm acme.com --depth quick                        # Quick assessment only
/octave:abm "Acme Corp"                                   # Search by company name
```

## Instructions

When the user runs `/octave:abm`:

### Step 1: Identify Target Account

Parse input:
- Domain (e.g., `acme.com`) → Use directly
- Company name → Search for domain
- LinkedIn URL → Extract domain

If company name provided without domain:
```
find_company({ name: "<company_name>" })
```

### Step 2: Deep Account Research

```
# Full company enrichment
enrich_company({ companyDomain: "<domain>" })

# Qualify against ICP
qualify_company({
  companyDomain: "<domain>",
  additionalContext: "Evaluate fit against all segments. Identify which segment, use cases, and playbooks are most relevant."
})
```

### Step 3: Stakeholder Mapping

```
# Find decision makers and influencers
# Use persona titles from library to guide search
list_all_entities({ entityType: "persona" })

# Search for stakeholders matching each persona
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<titles from persona 1>"],
  limit: <stakeholders_param or 3>
})

# Repeat for other relevant personas if needed
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<titles from persona 2>"],
  limit: 3
})
```

For each key stakeholder found:
```
# Enrich top stakeholders
enrich_person({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>"
  }
})

# Qualify against personas
qualify_person({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>",
    jobTitle: "<title>"
  },
  additionalContext: "Match to our buyer personas. Identify their likely role in a buying decision (champion, evaluator, economic buyer, blocker)."
})
```

### Step 4: Match Playbooks and Gather Intelligence

```
# Find best-fit playbook
search_knowledge_base({
  query: "<company industry> <company size> <identified personas>",
  entityTypes: ["playbook"]
})

# Get playbook with value props
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Find relevant proof points (industry, size match)
search_knowledge_base({
  query: "<company industry> <company size> results case study",
  entityTypes: ["proof_point", "reference"]
})

# Check for competitive context
search_knowledge_base({
  query: "<company name> <any tech stack signals>",
  entityTypes: ["competitor"]
})

# Check for any existing conversation history
list_events({
  startDate: "<365 days ago>",
  filters: {
    companyDomains: ["<domain>"]
  }
})
```

### Step 5: Generate Account Plan

```
ACCOUNT PLAN: [Company Name]
============================

Generated: [Date]
Depth: [Quick / Full]

===================================

ACCOUNT OVERVIEW
----------------
Company: [Name]
Domain: [domain]
Industry: [Industry]
Size: [Employees] | Revenue: [If known]
Location: [HQ]
Stage: [Funding stage / maturity]

Key Signals:
• [Recent news, funding, hiring]
• [Technology stack relevant to your product]
• [Strategic initiatives or changes]
• [Growth trajectory]

---

ICP FIT ASSESSMENT
------------------
Overall Score: [X/100]
Segment Match: [Segment name]
Confidence: [High / Medium / Low]

Why They Fit:
✓ [Fit reason 1]
✓ [Fit reason 2]
✓ [Fit reason 3]

Watch Outs:
⚠ [Concern or unknown 1]
⚠ [Concern or unknown 2]

---

BUYING COMMITTEE
----------------

[For each stakeholder found:]

STAKEHOLDER 1: [Name]
Role: [Title]
LinkedIn: [URL]
Persona Match: [Persona name] ([confidence]%)
Buying Role: [Champion / Evaluator / Economic Buyer / User / Blocker]

Profile:
• [Background highlights]
• [Relevant experience]
• [Likely motivations based on persona]

Messaging Angle:
• Lead with: "[Value prop most relevant to this persona]"
• Pain point: "[Most likely pain point]"
• Proof point: "[Most relevant evidence for them]"

---

STAKEHOLDER 2: [Name]
[Same structure]

---

STAKEHOLDER MAP SUMMARY
------------------------
| Name | Title | Persona | Buying Role | Priority |
|------|-------|---------|-------------|----------|
| [Name 1] | [Title] | [Persona] | [Role] | [1-5] |
| [Name 2] | [Title] | [Persona] | [Role] | [1-5] |
| ... | ... | ... | ... | ... |

Missing Roles: [Identify gaps - e.g., "No economic buyer identified"]

---

RECOMMENDED PLAYBOOK
--------------------
Playbook: [Name]
Key Insight: [Playbook's central thesis]

Value Props for This Account:
1. [Value prop 1] — Relevant because: [why for this account]
2. [Value prop 2] — Relevant because: [why]
3. [Value prop 3] — Relevant because: [why]

---

COMPETITIVE LANDSCAPE
---------------------
[If competitive signals detected:]
Likely current solution: [Tool/competitor if detected]
Competitive risks:
• [Risk 1]
• [Risk 2]

Positioning strategy:
• [How to differentiate for this account]

[If no competitive signals:]
No competitive intelligence detected for this account.
Consider asking about current solutions during discovery.

---

PROOF POINTS & REFERENCES
--------------------------
Most Relevant:
• [Proof point 1] — [Why relevant: same industry, size, use case]
• [Proof point 2] — [Why relevant]
• [Reference customer] — [Why relevant]

---

ENGAGEMENT STRATEGY
-------------------

Entry Point: [Recommended first contact]
Rationale: [Why start here]

Recommended Sequence:
1. [Week 1] [Action] → [Who] → [Channel]
2. [Week 1-2] [Action] → [Who] → [Channel]
3. [Week 2-3] [Action] → [Who] → [Channel]
4. [Week 3-4] [Action] → [Who] → [Channel]

Multi-Threading Plan:
• After initial engagement with [Stakeholder 1]:
  → Introduce [Stakeholder 2] via [method]
  → Engage [Stakeholder 3] with [different angle]

---

RISK FACTORS
------------
• [Risk 1: e.g., "Long procurement cycles in this industry"]
• [Risk 2: e.g., "No champion identified yet"]
• [Mitigation strategy for each]

---

NEXT STEPS
----------
Immediate:
1. [Action 1 — specific and concrete]
2. [Action 2]

This Week:
3. [Action 3]
4. [Action 4]

---

Sources Used:
- Company enrichment: [domain]
- Stakeholders researched: [N]
- Playbook: [name]
- Proof Points: [list]
- Segment: [name]

---

Want me to:
1. Generate outreach for the top stakeholder
2. Create a full email sequence for [Name]
3. Deep-dive research on a specific stakeholder
4. Generate call prep for the first meeting
5. Find similar accounts to build a target list
6. Export the account plan
```

### Step 6: Generate Initial Outreach (if requested)

For the recommended entry point stakeholder:
```
generate_email({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>",
    jobTitle: "<title>"
  },
  numEmails: 4,
  sequenceType: "COLD_OUTBOUND",
  allEmailsContext: "Account plan context: [company signals, persona match, value props, proof points]",
  allEmailsInstructions: "Personalized to [company] specifically. Reference [relevant signals]. Use [proof points] progressively."
})
```

## MCP Tools Used

### Research
- `enrich_company` - Deep company intelligence
- `enrich_person` - Stakeholder background
- `qualify_company` - ICP fit scoring
- `qualify_person` - Persona matching
- `find_person` - Stakeholder discovery
- `find_company` - Company lookup by name

### Library Context
- `list_all_entities` (persona) - Get persona definitions for stakeholder matching
- `get_playbook` - Get recommended playbook
- `list_value_props` - Persona-specific value props
- `search_knowledge_base` - Proof points, references, competitive intel
- `list_events` - Existing conversation history with account

### Content Generation
- `generate_email` - Outreach sequences
- `generate_content` - Account-specific content
- `generate_call_prep` - Meeting preparation

## Error Handling

**Company Not Found:**
> Couldn't find "[input]".
>
> Try:
> 1. Provide the company's website domain (e.g., acme.com)
> 2. Check spelling
> 3. Search by name: I'll look it up

**No Stakeholders Found:**
> No contacts found at [Company] matching your personas.
>
> Options:
> 1. Broaden the search (search all titles, not just persona matches)
> 2. Search for specific titles you know
> 3. Proceed with company-level plan only

**Low ICP Score:**
> [Company] scored [X/100] against your ICP.
>
> This is below typical qualification thresholds.
> Continue anyway? Or:
> 1. Find similar companies with better fit
> 2. See why the score is low and if any signals are missing
> 3. Proceed with adjusted expectations

## Related Skills

- `/octave:research` - Deep-dive on a specific stakeholder
- `/octave:campaign` - Generate multi-channel campaign for this account
- `/octave:battlecard` - Competitive intel if competitor detected
- `/octave:pipeline` - Coach on deal progression after engagement starts
- `/octave:prospector` - Find more accounts like this one
