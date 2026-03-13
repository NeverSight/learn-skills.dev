---
name: New Deal from Meeting
description: |
  Detect new sales opportunity from meeting transcript and create a deal in CRM with AI-extracted context.
  Use when a user asks "create a deal from this meeting", "new opportunity", "create opportunity", or when
  a meeting transcript contains clear buying signals (budget discussed, timeline, pain points, decision process).
  Returns deal recommendation with confidence score and pre-filled fields.
metadata:
  author: sixty-ai
  version: "2"
  category: sales-ai
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - pipeline
    - meetings
  triggers:
    - pattern: "new deal from meeting"
      intent: "create_deal_from_meeting"
      confidence: 0.90
      examples:
        - "create a deal from this meeting"
        - "turn this into a deal"
        - "make a deal from this conversation"
    - pattern: "new opportunity"
      intent: "opportunity_detected"
      confidence: 0.80
      examples:
        - "this is a new opportunity"
        - "new opp from this call"
        - "capture this as an opportunity"
    - pattern: "create opportunity"
      intent: "create_opportunity"
      confidence: 0.85
      examples:
        - "create an opportunity for this"
        - "set up an opportunity"
        - "new opportunity in CRM"
  keywords:
    - "deal"
    - "opportunity"
    - "create"
    - "meeting"
    - "new"
    - "pipeline"
    - "forecast"
    - "prospect"
  required_context:
    - meeting
    - company_name
  inputs:
    - name: meeting_id
      type: string
      description: "The meeting identifier to analyze for opportunity signals"
      required: true
    - name: auto_create
      type: boolean
      description: "If true, create the deal immediately; if false, return recommendation only (default: false)"
      required: false
      default: false
  outputs:
    - name: opportunity_detected
      type: boolean
      description: "Whether a legitimate sales opportunity was detected in the meeting"
    - name: confidence_score
      type: number
      description: "Confidence that this is a real opportunity (0.0-1.0)"
    - name: deal_recommendation
      type: object
      description: "Recommended deal fields with AI-extracted context"
    - name: created_deal
      type: object
      description: "The created deal record (if auto_create is true)"
  priority: high
  requires_capabilities:
    - crm
    - meetings
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# New Deal from Meeting

## Goal
Analyze a meeting transcript to detect genuine sales opportunities and create a deal in the CRM with AI-extracted context: company, contact, estimated value, stage, key requirements, pain points, timeline, and next steps. This skill saves reps from manual deal creation and ensures that opportunities identified in conversations are immediately captured in the pipeline.

## Why Meeting-to-Deal Conversion Matters

Most sales opportunities are first expressed in conversations -- demos, discovery calls, executive briefings, account reviews. But many of these opportunities never make it into the CRM:

- **47% of opportunities are lost in the gap between conversation and CRM entry** (Salesforce State of Sales, 2023). Reps leave the meeting intending to "create the deal later" and then forget or deprioritize it.
- **Speed matters.** Opportunities entered into CRM within 24 hours of discovery have a 31% higher close rate than those entered 3+ days later (InsightSquared).
- **AI-extracted context is more accurate than manual entry.** Reps often misremember key details (budget, timeline, pain points) when entering deals manually. Transcript-based extraction captures what was actually said.
- **Opportunity qualification improves.** Forcing the AI to extract MEDDIC-style signals (pain, budget, timeline, decision process) from the transcript ensures the deal has real substance, not just "they seemed interested."
- **Follow-up improves.** Deals with AI-extracted next steps and requirements have 2.3x higher engagement rates because reps know exactly what to do next (Gong research).

## Required Capabilities
- **CRM**: To create deals, fetch company/contact data
- **Meetings**: To fetch meeting transcript and metadata

## Inputs
- `meeting_id`: The meeting identifier (required)
- `auto_create`: If true, create the deal immediately. If false, return recommendation only for user approval. Default: false (recommendation mode).

## Data Gathering (via execute_action)

1. **Fetch meeting transcript**: `execute_action("get_meeting_transcript", { meeting_id })` -- full transcript text
2. **Fetch meeting metadata**: `execute_action("get_meeting", { id: meeting_id })` -- attendees, date, title
3. **Fetch attendee contacts**: `execute_action("list_contacts", { meeting_id })` -- map attendees to CRM contacts
4. **Fetch existing deals**: `execute_action("list_deals", { company_name })` -- check if a deal already exists for this company/opportunity to avoid duplicates

If transcript is not available, return an error: "Meeting transcript not found. Ensure the meeting has been recorded and transcribed before creating a deal."

## Opportunity Detection Framework

Not every meeting should generate a deal. Apply these criteria to determine if a legitimate opportunity exists:

### Strong Opportunity Signals (at least 2 required)
- **Budget discussed**: Buyer mentioned a specific budget amount, budget range, or confirmed budget is available
- **Timeline discussed**: Buyer mentioned a target go-live date, decision deadline, or fiscal year timing
- **Pain clearly articulated**: Buyer described a specific problem, gap, or inefficiency they need to solve
- **Decision process mentioned**: Buyer explained who is involved in the decision, approval steps, or evaluation process
- **Competitive evaluation**: Buyer is actively evaluating solutions (including competitors) -- shows active buying intent
- **ROI/business case**: Buyer discussed expected outcomes, metrics, or value they expect from a solution
- **Executive presence**: VP+ level buyer participated in the meeting (signals seriousness)

### Weak or False Signals (do NOT create a deal)
- Meeting was purely educational (no buying intent, just learning)
- Buyer said "just exploring" with no timeline or budget
- Meeting was a courtesy/networking call (relationship-building, not evaluation)
- Buyer was vague on all key questions (pain, timeline, budget, decision process)
- Meeting was a demo but buyer showed no engagement or follow-up intent
- Meeting was an existing customer discussing support or minor feature requests (not a new deal)

### Confidence Scoring
Assign a confidence score (0.0 to 1.0) based on how many strong signals are present:
- **0.9-1.0**: 5+ strong signals, explicit buying intent, clear next steps agreed
- **0.7-0.89**: 3-4 strong signals, buyer is actively evaluating but some gaps remain
- **0.5-0.69**: 2 strong signals, buyer is interested but early-stage, may need more qualification
- **0.3-0.49**: 1 strong signal, buyer expressed interest but lacks substance (recommend more discovery before creating deal)
- **0.0-0.29**: No strong signals, meeting was exploratory or educational (do not create deal)

Only recommend deal creation if confidence is 0.5+ (2+ strong signals).

## Deal Field Extraction

For each detected opportunity, extract the following fields from the transcript:

### Required Fields
- **Company**: Company name (extracted from attendees or transcript). If multiple companies on the call, choose the buyer's company (not partners or observers).
- **Deal Name**: Format: `[Company Name] - [Product/Solution]`. Example: "Acme Corp - Enterprise Platform License"
- **Primary Contact**: The main buyer stakeholder on the call (typically the person who spoke most or who owns the initiative)
- **Stage**: Map to CRM stages based on signals:
  - "Discovery" if pain and timeline discussed but no budget or decision process
  - "Evaluation" if budget discussed and buyer is actively comparing solutions
  - "Proposal" if buyer requested a proposal, pricing, or contract
  - "Negotiation" if buyer is negotiating terms, pricing, or timelines
  - Default: "Discovery" if unclear

### Recommended Fields (extract if available)
- **Estimated Value**: Extract from transcript if mentioned. If not mentioned, estimate based on:
  - Company size (employee count, revenue if known)
  - Number of users/seats discussed
  - Solution scope (enterprise-wide vs. departmental)
  - Use conservative estimate if uncertain
- **Close Date**: Extract from timeline discussion. If buyer said "need this by Q2," set close date to end of Q2. If no timeline mentioned, default to 90 days from meeting date.
- **Pain Points**: Bullet list of specific problems the buyer mentioned. Quote the buyer when possible: "Buyer said: 'We're losing 20 hours per week on manual data entry.'"
- **Key Requirements**: Features, capabilities, or integration requirements the buyer mentioned
- **Decision Makers**: Names and roles of people involved in the decision process (if mentioned)
- **Next Steps**: Agreed next steps from the meeting (e.g., "Send proposal by Friday", "Schedule technical deep-dive next week")
- **Competitors Mentioned**: List any competitors the buyer mentioned evaluating
- **Budget Authority**: If the buyer mentioned who controls the budget, note it

### Deal Description Template
Use this format for the deal description field:
```
**Opportunity Source:** Meeting on [Date] - [Meeting Title]

**Pain Points:**
- [Pain 1]
- [Pain 2]
- [Pain 3]

**Key Requirements:**
- [Requirement 1]
- [Requirement 2]

**Timeline:** [Buyer's stated timeline or "None specified"]
**Budget:** [Mentioned budget or "Not discussed"]
**Decision Process:** [Who's involved, approval steps, or "Not discussed"]

**Competitors:** [List or "None mentioned"]

**Next Steps:**
- [Next step 1]
- [Next step 2]

**Confidence:** [X%] - [Brief reasoning for confidence score]
```

## Duplicate Deal Detection

Before creating a deal, check if one already exists for this company and opportunity:

1. Fetch existing deals for the company: `execute_action("list_deals", { company_name })`
2. Check for deals with similar names or overlapping timelines (created within last 90 days)
3. If a similar deal exists:
   - Flag it: "Potential duplicate detected: '[Existing Deal Name]' created on [Date]. Recommend reviewing before creating a new deal."
   - Suggest updating the existing deal instead: "Consider adding this meeting's context to the existing deal rather than creating a duplicate."
   - If user confirms they want to proceed anyway, allow creation with a note in the description: "Note: Similar deal exists ([Deal Name]). This is a separate opportunity because [reason]."

## Deal Creation (if auto_create is true)

If `auto_create` is true and confidence is 0.5+, create the deal using:
```
execute_action("create_deal", {
  company_name: [extracted company],
  name: [generated deal name],
  value: [estimated value],
  stage: [extracted stage],
  close_date: [extracted or estimated close date],
  description: [formatted deal description],
  primary_contact_id: [contact ID],
  source: "meeting",
  source_meeting_id: meeting_id
})
```

If creation succeeds, also create a task reminder to follow up on the agreed next steps:
```
execute_action("create_task", {
  title: "Follow up: [Next step from meeting]",
  description: "From meeting on [Date]: [Details of agreed next step]",
  due_date: [Date based on urgency -- typically 1-3 days from meeting],
  priority: "high",
  deal_id: [newly created deal ID]
})
```

## Output Contract

Return a SkillResult with:
- `data.opportunity_detected`: boolean (true if 2+ strong signals present)
- `data.confidence_score`: number (0.0-1.0, based on signal strength)
- `data.deal_recommendation`: object
  - `company`: string
  - `deal_name`: string
  - `primary_contact`: string (name and title)
  - `stage`: string
  - `estimated_value`: number | null
  - `close_date`: string | null (ISO date)
  - `pain_points`: string[] (specific pains extracted from transcript)
  - `key_requirements`: string[] (features/capabilities buyer mentioned)
  - `decision_makers`: string[] | null (names and roles if mentioned)
  - `timeline`: string | null (buyer's stated timeline)
  - `budget`: string | null (mentioned budget or "Not discussed")
  - `competitors`: string[] | null (competitors mentioned)
  - `next_steps`: string[] (agreed next steps from meeting)
  - `description`: string (formatted deal description)
  - `signals_detected`: string[] (list of strong signals found: "budget_discussed", "timeline_discussed", etc.)
  - `recommendation`: string (should you create this deal? why or why not?)
  - `duplicate_warning`: string | null (if potential duplicate detected)
- `data.created_deal`: object | null
  - If `auto_create` is true and deal was created: full deal record
  - If `auto_create` is false: null (recommendation only)
  - `deal_id`: string
  - `deal_name`: string
  - `created_at`: string

## Quality Checklist

Before returning the deal recommendation, verify:

- [ ] Confidence score is based on actual signals from the transcript (not guessed)
- [ ] At least 2 strong signals are present before recommending deal creation
- [ ] Company name is correctly extracted (buyer's company, not seller's company or partners)
- [ ] Deal name follows format: "[Company] - [Product/Solution]"
- [ ] Pain points are SPECIFIC (quoted from transcript when possible, not generic)
- [ ] Key requirements are actionable (what the buyer actually needs, not what you want to sell)
- [ ] Close date is realistic (extracted from buyer's timeline or estimated conservatively)
- [ ] Stage is appropriate based on signals (do not default to "Proposal" if buyer is still in discovery)
- [ ] Duplicate check was performed (do not create redundant deals)
- [ ] Next steps are clear and actionable (not vague like "follow up")
- [ ] If confidence is below 0.5, do NOT recommend creating the deal -- recommend more discovery instead
- [ ] Deal description is formatted and readable (use bullet points, not walls of text)

## Examples

### Good Opportunity Detection (High Confidence)

**Meeting Transcript Excerpt:**
> Buyer: "We're currently using Excel for inventory tracking and it's a disaster. We lose about 15 hours per week on manual reconciliation. We have budget approved for a new system -- around $50K for this fiscal year. We need to have something in place by end of Q2 because we're opening a new warehouse in May. I'll need to get buy-in from our CFO and our Head of Operations, but if the pricing and features work, I can move quickly."

**Deal Recommendation:**
```json
{
  "opportunity_detected": true,
  "confidence_score": 0.85,
  "deal_recommendation": {
    "company": "Acme Corp",
    "deal_name": "Acme Corp - Inventory Management Platform",
    "primary_contact": "Sarah Chen, Director of Supply Chain",
    "stage": "Evaluation",
    "estimated_value": 50000,
    "close_date": "2026-06-30",
    "pain_points": [
      "Excel-based inventory tracking causing inefficiency",
      "15 hours per week lost on manual reconciliation",
      "New warehouse opening in May requires scalable solution"
    ],
    "key_requirements": [
      "Inventory tracking and reconciliation",
      "Must be operational by end of Q2 (May)",
      "Integration with existing warehouse systems"
    ],
    "decision_makers": ["Sarah Chen (Director of Supply Chain)", "CFO", "Head of Operations"],
    "timeline": "Need solution in place by end of Q2 (May 2026)",
    "budget": "$50K approved for this fiscal year",
    "competitors": null,
    "next_steps": [
      "Send proposal with pricing for 50-user license",
      "Schedule technical demo focused on warehouse integration",
      "Include implementation timeline showing go-live by May"
    ],
    "signals_detected": ["pain_clearly_articulated", "budget_discussed", "timeline_discussed", "decision_process_mentioned"],
    "recommendation": "Strong opportunity. Buyer has clear pain, confirmed budget, urgent timeline (May deadline), and identified decision-makers. Recommend creating deal immediately and sending proposal by end of week.",
    "duplicate_warning": null
  }
}
```

### Bad Opportunity (Low Confidence)

**Meeting Transcript Excerpt:**
> Buyer: "Yeah, we're always looking for ways to improve our processes. This looks interesting. I'll need to think about it and talk to my team. Maybe we can reconnect in a few months and see where we're at."

**Deal Recommendation:**
```json
{
  "opportunity_detected": false,
  "confidence_score": 0.15,
  "deal_recommendation": {
    "signals_detected": [],
    "recommendation": "Do not create a deal. No strong signals detected. Buyer is in exploratory mode with no pain, budget, timeline, or decision process discussed. Recommend: (1) Send a follow-up email with a relevant case study, (2) Set a reminder to re-engage in 3 months, (3) Do not add to pipeline -- this is not an active opportunity yet."
  }
}
```

### Duplicate Detection Example

**Scenario:** Meeting on Feb 16, 2026. Existing deal "Acme Corp - Enterprise Platform" created on Feb 10, 2026.

**Deal Recommendation:**
```json
{
  "opportunity_detected": true,
  "confidence_score": 0.70,
  "deal_recommendation": {
    "company": "Acme Corp",
    "deal_name": "Acme Corp - Data Platform License",
    "duplicate_warning": "Potential duplicate detected: 'Acme Corp - Enterprise Platform' created on Feb 10, 2026. Review existing deal before creating a new one. These may be the same opportunity or separate workstreams."
  }
}
```

## Error Handling

### Transcript not available
If meeting transcript is missing:
- `opportunity_detected`: false
- Error message: "Meeting transcript not found. Ensure the meeting has been recorded and transcribed before analyzing for opportunities."

### Meeting is too short (under 5 minutes)
If meeting duration is under 5 minutes, it is unlikely to contain a substantive opportunity:
- `opportunity_detected`: false
- Recommendation: "Meeting was only [X] minutes. Too short to evaluate for opportunity signals. If this was a discovery call, schedule a longer follow-up."

### No buyer attendees identified
If the meeting attendees are all from the seller's company (internal meeting):
- `opportunity_detected`: false
- Recommendation: "No external buyer attendees detected. This appears to be an internal meeting. Cannot create a deal without buyer involvement."

### Existing customer renewal or upsell
If the meeting is with an existing customer discussing renewal or expansion (not a new logo):
- Detect this from transcript keywords: "renewal", "expand", "add more users"
- Adjust the recommendation: "This appears to be a renewal or expansion opportunity for existing customer [Company]. Recommend creating an 'Expansion' or 'Renewal' deal rather than a new logo deal."

### Low confidence but user insists
If confidence is below 0.5 but user manually requests deal creation anyway:
- Proceed with creation but include a warning in the deal description: "Note: AI confidence for this opportunity was [X%] due to limited signals in the meeting transcript. Recommend additional discovery to qualify further."

### Multiple companies on the call (partnership, multi-party)
If transcript shows 3+ companies (e.g., buyer, seller, and a partner):
- Identify the buyer company vs. partners/observers
- Create the deal for the buyer company only
- Note the partner involvement in the deal description: "Partner [Partner Name] was involved in this discussion."

## Tone and Presentation

- Be honest about confidence. If signals are weak, say so: "Confidence is low (30%) because no budget or timeline was discussed."
- Extract what was actually said, not what you wish was said. If budget was not mentioned, do not invent a number.
- Pain points should be specific and quoted when possible: "Buyer said: 'We're losing 15 hours per week.'" not "Buyer has inefficiency problems."
- Recommendations should be clear: "Create deal immediately" or "Do not create deal -- recommend more discovery first."
- If duplicate detected, be direct: "A similar deal already exists. Review before creating a duplicate."
- Frame next steps as what the REP should do, not what the buyer should do: "Send proposal by Friday" not "Buyer will review proposal."
- Confidence scores are NOT certainty. 0.85 confidence means "strong signals, likely a real opportunity" not "this will definitely close."
