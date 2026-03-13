---
name: Deal Handoff Brief
description: |
  Generate a structured handoff document for deal transfer between reps or to customer success.
  Use when a user asks "hand off this deal", "create handoff brief", "transfer this deal",
  "deal handover", or needs comprehensive documentation for relationship transition.
  Returns detailed brief with deal history, stakeholder map, relationship context, and next steps.
metadata:
  author: sixty-ai
  version: "2"
  category: sales-ai
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - pipeline
    - outreach
  triggers:
    - pattern: "hand off this deal"
      intent: "deal_handoff"
      confidence: 0.90
      examples:
        - "hand this deal off"
        - "handoff this deal to"
        - "transfer deal ownership"
    - pattern: "create handoff brief"
      intent: "handoff_documentation"
      confidence: 0.85
      examples:
        - "generate handoff document"
        - "create deal handoff"
        - "build handoff brief"
    - pattern: "transfer this deal"
      intent: "deal_transfer"
      confidence: 0.85
      examples:
        - "transfer deal to new rep"
        - "move this deal to"
        - "reassign this deal"
    - pattern: "deal handover"
      intent: "deal_transition"
      confidence: 0.80
      examples:
        - "deal transition document"
        - "handover documentation"
        - "transition this deal"
  keywords:
    - "handoff"
    - "transfer"
    - "handover"
    - "transition"
    - "reassign"
    - "deal"
    - "brief"
    - "document"
  required_context:
    - deal
    - company_name
  inputs:
    - name: deal_id
      type: string
      description: "Deal identifier to create handoff brief for"
      required: true
    - name: new_owner
      type: string
      description: "Name or ID of person receiving the deal"
      required: false
    - name: handoff_type
      type: string
      description: "Type of handoff: rep_to_rep, sales_to_cs, expansion, coverage"
      required: false
      default: "rep_to_rep"
    - name: transition_reason
      type: string
      description: "Why the deal is being transferred"
      required: false
  outputs:
    - name: handoff_brief
      type: object
      description: "Structured document with deal summary, history, stakeholders, risks, next steps"
    - name: transition_email
      type: object
      description: "Draft email introducing new owner to customer"
    - name: internal_notes
      type: string
      description: "Private context for new owner (risks, sensitivities, politics)"
  priority: high
  requires_capabilities:
    - crm
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Deal Handoff Brief

## Goal
Create a comprehensive, actionable handoff document that enables a new owner to take over a deal or customer relationship with full context, minimal disruption to the buyer, and preserved momentum. The handoff should feel like continuity, not a restart.

## Why Deal Handoffs Matter (and Often Fail)

Deal and account transitions are high-risk moments that often destroy value:

- **61% of deals in transition experience a timeline delay of 2+ weeks** due to poor handoff documentation (CSO Insights).
- **34% of customers report "starting over" when a new rep takes over**, requiring them to re-explain their needs and history (Salesforce Customer Experience Study).
- **The #1 complaint from buyers about vendor relationships**: "We keep having to repeat ourselves to new people" (Gartner B2B Buying Survey, 2024).
- **Deals handed off without a formal brief are 2.7x more likely to stall or close-lost** within 30 days of transition (RAIN Group analysis).
- **Poor sales-to-CS handoffs account for 23% of first-year churn** in B2B SaaS (ChurnZero benchmark data).

The root cause: most handoffs are verbal ("I'll fill you in on a call") or rely on scattered CRM notes. The new owner does not know what they do not know, and by the time they realize they are missing critical context, the damage is done.

## Required Capabilities
- **CRM**: To fetch deal history, contacts, activities, MEDDICC data, and pipeline context

## Inputs
- `deal_id`: Deal identifier (required)
- `new_owner`: Name or ID of person receiving the deal (optional, can be added later)
- `handoff_type`: Type of transition (optional, default: `rep_to_rep`)
  - `rep_to_rep`: AE to AE (territory change, role change, coverage)
  - `sales_to_cs`: Closed deal transitioning from sales to customer success
  - `expansion`: CSM handing expansion opportunity back to sales
  - `coverage`: Temporary coverage during PTO or leave
- `transition_reason`: Why the deal is being transferred (optional but recommended)

## Data Gathering (via execute_action)

Gather comprehensive deal context:

1. **Deal record**: `execute_action("get_deal", { id: deal_id })` — stage, value, close date, health, MEDDICC fields
2. **All contacts**: `execute_action("get_deal_contacts", { deal_id })` — stakeholder map with roles, engagement levels
3. **Full activity history**: `execute_action("get_deal_activities", { deal_id, limit: 100 })` — meetings, emails, calls, notes (capture the relationship arc)
4. **Open tasks**: `execute_action("list_tasks", { deal_id })` — what is in flight
5. **All meetings**: `execute_action("get_meetings", { deal_id })` — meeting history with summaries/transcripts
6. **Pipeline context**: `execute_action("get_pipeline_summary", {})` — deal priority relative to pipeline
7. **Company data**: `execute_action("get_company", { id: company_id })` — firmographics, industry, tech stack

**Critical**: The handoff brief must be based on COMPLETE data. Incomplete handoffs are worse than no handoff at all because they create false confidence.

## Handoff Brief Structure (Markdown Document)

The brief should be a standalone document that the new owner can read in 10-15 minutes and reference indefinitely. Format as structured markdown for readability and portability.

### Section 1: Executive Summary (3-5 sentences)
**Purpose**: Allow the new owner to understand the deal at a glance before diving into details.

**Include**:
- Deal stage and value
- Customer's core need or pain point
- Current momentum (positive, neutral, stalled)
- Immediate next steps
- Biggest risk or opportunity

**Good example**:
```
**Deal: Acme Corp — $180K ARR — Evaluation Stage**

Acme is migrating from legacy data platform to modern cloud stack. Primary pain: manual data reconciliation consuming 20+ hours/week. Deal momentum is positive — demo completed Feb 10, POC scoped, technical review scheduled Feb 20. Primary risk: competitor [Competitor X] is also in evaluation and has stronger API documentation. Champion is Sarah Chen (VP Eng), highly engaged. Close target: end of Q1.
```

**Bad example**:
```
Deal is in evaluation stage. Customer is interested in our product. Next step is a follow-up call.
```

### Section 2: Deal Snapshot (Structured Data)
**Purpose**: Key facts in scannable format.

**Include**:
```
| Field | Value |
|-------|-------|
| **Company** | Acme Corp |
| **Industry** | SaaS / B2B Marketing Tech |
| **Size** | 250 employees, $40M ARR |
| **Deal Value** | $180K ARR |
| **Stage** | Evaluation |
| **Close Date** | March 31, 2026 |
| **Days in Stage** | 18 |
| **Health Score** | 78 (Healthy) |
| **Probability** | 60% |
| **Competitor** | [Competitor X] (active evaluation) |
| **Source** | Inbound demo request |
| **Original Owner** | [Previous Rep Name] |
| **Handoff Date** | Feb 15, 2026 |
| **Handoff Reason** | Territory realignment |
```

### Section 3: Stakeholder Map (Critical Section)
**Purpose**: Relationships are the most valuable and fragile asset in a deal. The new owner needs to know who matters, who supports the deal, who is neutral, and who is blocking.

**Format** (for each stakeholder):
```
**[Name, Title]**
- **Role in Deal**: [Champion | Economic Buyer | Evaluator | Blocker | Coach | Unknown]
- **Engagement Level**: [High | Medium | Low]
- **Last Contact**: [Date and context]
- **Relationship Notes**: [1-2 sentences about rapport, communication style, priorities]
- **Influence**: [High | Medium | Low]
- **Sentiment**: [Positive | Neutral | Negative | Unknown]
```

**Example**:
```
**Sarah Chen, VP Engineering**
- **Role in Deal**: Champion
- **Engagement Level**: High (responds within hours, attended 4 meetings)
- **Last Contact**: Feb 12 — technical deep-dive on OAuth requirements
- **Relationship Notes**: Ex-Google, highly technical, no-BS communication style. Loves data and proof points. Allergic to sales fluff. Prefers concise emails. Strong advocate internally but does not have final budget authority (reports to CTO).
- **Influence**: High (technical decision-maker, trusted by CTO)
- **Sentiment**: Positive (quoted in meeting: "This is exactly what we need")

**James Park, CTO**
- **Role in Deal**: Economic Buyer
- **Engagement Level**: Low (attended 1 intro meeting, delegated evaluation to Sarah)
- **Last Contact**: Jan 28 — 20-minute intro call
- **Relationship Notes**: Strategy-focused, less interested in technical details. Cares about risk mitigation and team velocity. Will defer to Sarah's technical recommendation but holds budget authority. Mentioned competitor [Competitor X] casually in intro call.
- **Influence**: High (final decision-maker)
- **Sentiment**: Neutral (interested but not engaged yet)

**Mike Torres, Senior Engineer**
- **Role in Deal**: Evaluator
- **Engagement Level**: Medium (attended demo, asked detailed API questions)
- **Last Contact**: Feb 10 — product demo
- **Relationship Notes**: Hands-on technical evaluator. Concerned about integration complexity. Needs reassurance that implementation will not disrupt current workflows. Slight skepticism about migration effort.
- **Influence**: Medium (Sarah trusts his technical judgment)
- **Sentiment**: Neutral to slightly negative (integration concerns not fully addressed)
```

**Critical**: If you have never met a stakeholder but know they exist (e.g., mentioned in conversation), include them with `Role: Unknown` and `Sentiment: Unknown`. This prevents blind spots.

### Section 4: Relationship History (Timeline)
**Purpose**: Show the arc of the relationship so the new owner understands context and momentum.

**Format**: Reverse chronological timeline of key moments (most recent first).

**Example**:
```
**Feb 12** — Technical deep-dive meeting with Sarah and engineering team. Discussed OAuth/SAML integration requirements. Sarah confirmed SOC 2 deadline (Q3) is non-negotiable. POC scope agreed.

**Feb 10** — Product demo with Sarah, Mike, and 2 other engineers. Positive reception overall, but Mike raised concerns about API integration complexity. Demo recording shared same day.

**Feb 3** — Follow-up call with Sarah. Discussed pricing (she said budget is $150-200K range). Confirmed they are evaluating [Competitor X] in parallel. Sarah mentioned CTO (James) needs to sign off but she has strong influence on decision.

**Jan 28** — Intro call with James (CTO) and Sarah (VP Eng). James explained migration initiative: moving from legacy platform to modern cloud stack. Timeline: decision by end of Q1, implementation in Q2. James mentioned competitor casually.

**Jan 22** — First contact: Acme submitted inbound demo request via website. Sarah's initial message: "Interested in learning about your data platform for our migration project."
```

**Quality rule**: Include at least 5-7 key moments if the deal is mid-to-late stage. A single-line timeline indicates insufficient data gathering.

### Section 5: Deal Dynamics and Context
**Purpose**: Explain what is really happening beneath the surface — the politics, motivations, risks, and nuances that are not captured in CRM fields.

**Include**:
- **Why are they buying?** (Pain point, compelling event, strategic initiative)
- **Why now?** (Deadline, trigger event, budget cycle)
- **What is the decision process?** (Who decides, what criteria, what timeline)
- **What are the risks?** (Competitor, budget, technical blocker, stakeholder objection)
- **What is the competitive landscape?** (Who else are they evaluating, how are we positioned)
- **What is the relationship dynamic?** (Trust level, communication frequency, champion strength)
- **What is unsaid or unclear?** (Gaps in information, assumptions that need validation)

**Example**:
```
**Why they're buying**: Acme is migrating from a legacy on-prem data platform (built in-house 8 years ago) to a modern SaaS solution. The legacy system is brittle, requires 20+ hours/week of manual reconciliation, and is blocking new product features. This is a strategic priority for the CTO.

**Why now**: Two forcing functions: (1) SOC 2 audit in Q3 requires better data governance, and the legacy system cannot pass compliance review. (2) Product team is planning a major feature release in Q2 that depends on better data infrastructure. If they do not decide by end of Q1, implementation will not be complete in time for the Q2 release.

**Decision process**: Sarah (VP Eng) is leading the technical evaluation and has strong influence. James (CTO) has final budget authority. Sarah will make a recommendation, and James will approve unless there is a major red flag. Procurement is not involved yet (will come in during contracting). Timeline: decision by March 31.

**Primary risk**: [Competitor X] is in active evaluation. Sarah mentioned their API docs are more comprehensive than ours. Mike (Senior Eng) raised integration complexity concerns in the demo. If we cannot de-risk the integration during the POC, they may choose [Competitor X] for ease of implementation even if our product is stronger.

**Secondary risk**: Budget has not been formally approved. Sarah said "$150-200K is in the ballpark" but James has not confirmed. If the deal drags into Q2, budget may get reallocated.

**Relationship strength**: Strong with Sarah (high trust, frequent communication, she is an active champion). Weak with James (only one interaction, he delegated to Sarah, we have not built a direct relationship). Need to engage James before final decision to ensure executive buy-in.

**Unknown factors**: We do not know (1) what [Competitor X]'s pricing is, (2) whether there are other stakeholders we have not met (procurement, security, legal), (3) whether Sarah has the internal political capital to push this through if there is resistance.
```

### Section 6: MEDDICC Assessment
**Purpose**: Structured qualification framework to identify gaps and risks.

**Format**:
```
| MEDDICC | Status | Notes |
|---------|--------|-------|
| **Metrics** | ✅ Strong | 20 hours/week manual work eliminated = $80K/year labor savings. Sarah validated these numbers. |
| **Economic Buyer** | ⚠️ Partial | James (CTO) is EB but only engaged once. Need stronger relationship. |
| **Decision Criteria** | ✅ Strong | Technical fit (OAuth/SAML), ease of integration, SOC 2 compliance, API quality. |
| **Decision Process** | ✅ Strong | Sarah evaluates → Sarah recommends → James approves. Timeline: decision by March 31. |
| **Identify Pain** | ✅ Strong | Legacy system is brittle, blocks product roadmap, fails SOC 2 audit. Acute pain. |
| **Champion** | ✅ Strong | Sarah is highly engaged, has influence, actively selling internally. |
| **Competition** | ⚠️ Risk | [Competitor X] in active evaluation. Better API docs. Need to differentiate on implementation support. |
```

### Section 7: Next Steps (Immediate Actions)
**Purpose**: Tell the new owner exactly what to do in the first 48 hours to maintain momentum.

**Format**: Prioritized action list with deadlines and success criteria.

**Example**:
```
**Immediate (Next 48 Hours)**
1. **Intro email to Sarah** — Send warm handoff email introducing yourself. Reference the Feb 12 technical call to show continuity. Confirm POC timeline still on track for Feb 20 review. [Draft provided in transition_email output]
2. **Review POC scope document** — Shared with Sarah on Feb 12. Familiarize yourself with OAuth/SAML requirements before Feb 20 call.
3. **Schedule prep call with Solutions Engineer** — Sarah (our SE, not the customer) needs to brief you on the technical architecture before the Feb 20 customer call.

**Week 1**
4. **Feb 20 technical review call** — Already scheduled. Review POC progress with Sarah and Mike. Address integration concerns head-on.
5. **Outreach to James (CTO)** — Build direct relationship. Propose brief executive sync to discuss strategic alignment. Low-pressure, value-add approach.
6. **Competitive research** — Deep-dive on [Competitor X]. Understand their positioning and prepare differentiation talking points.

**Week 2**
7. **POC success confirmation** — Get explicit confirmation from Sarah that POC met requirements.
8. **Proposal preparation** — Assuming POC success, prepare proposal with pricing options ($150K, $180K, $200K tiers).
9. **Executive alignment** — Sync with James on strategic fit and timeline.
```

### Section 8: Internal Notes (Private Context)
**Purpose**: Things the new owner needs to know but should NEVER share with the customer.

**Include**:
- Pricing flexibility (discount authority, what has been quoted vs. what is approved)
- Internal politics or sensitivities
- Competitor intelligence (pricing, weaknesses)
- Stakeholder concerns that were raised privately
- Anything said "off the record"

**Example**:
```
**Pricing Context**: Quoted $180K ARR (list). Sarah mentioned budget is $150-200K. We have approval to go as low as $150K if needed to close, but hold at $180K unless they push back. Do NOT offer discount proactively.

**Stakeholder Dynamics**: Sarah is a strong champion but mentioned (off the record) that James can be "unpredictable" and sometimes overrides technical recommendations for strategic reasons. She suggested getting James aligned early to avoid late-stage surprises.

**Competitor Intel**: Sarah mentioned [Competitor X]'s API docs are better than ours, but she also said their customer support is "terrible" based on backchannel reference calls. If integration concerns come up, lean into our implementation support and customer success.

**Sensitivity**: Mike (Senior Engineer) is skeptical about the migration effort. Sarah trusts his judgment. If Mike becomes a vocal blocker, the deal is at risk. Prioritize addressing his integration concerns during the POC.
```

## Transition Email to Customer (Separate Output)

In addition to the internal handoff brief, generate a draft email introducing the new owner to the customer. This email should:

1. **Acknowledge the transition** (briefly, without over-explaining internal changes)
2. **Introduce the new owner** (credentials, relevant experience)
3. **Reassure continuity** (the deal is not starting over)
4. **Reference recent context** (prove the new owner is already up to speed)
5. **Confirm next steps** (no disruption to timeline)

**Good example**:
```
Subject: Quick Intro — Your New Point of Contact at Sixty

Hi Sarah,

Quick update: I'm transitioning some of my accounts due to a territory realignment, and I wanted to introduce you to Alex Rivera, who will be your main point of contact at Sixty going forward.

Alex has been with Sixty for 4 years and specializes in data platform migrations for engineering-led organizations like Acme. He has worked with companies like [Peer Company A] and [Peer Company B] on similar OAuth/SAML implementations, so he is very familiar with the type of architecture challenges we discussed on Feb 12.

I have briefed Alex fully on your evaluation, the POC scope, and the Feb 20 technical review. He will be joining that call along with our Solutions Engineer, Sarah Torres. Nothing changes on your end — same timeline, same POC, same commitment.

Alex, I'll let you take it from here. Sarah, you're in great hands.

Best,
[Previous Owner]
```

**Bad example**:
```
Hi,

I'm leaving this account and Alex will be taking over. He'll reach out to schedule a call.

Thanks
```

## Output Contract

Return a SkillResult with:

### `data.handoff_brief`
Object:
- `markdown`: string (full handoff brief in markdown format, ready to save as a document)
- `sections`: array of section objects:
  - `type`: "executive_summary" | "deal_snapshot" | "stakeholder_map" | "relationship_history" | "deal_dynamics" | "meddicc" | "next_steps" | "internal_notes"
  - `content`: string
- `completeness_score`: number (0-100, based on how much data was available)
- `missing_data`: string[] (list of data gaps that could not be filled)

### `data.transition_email`
Object:
- `subject`: string
- `body`: string (draft email introducing new owner to customer)
- `to`: string[] (customer contact emails)
- `cc`: string[] (optional, may include previous owner for visibility)

### `data.internal_notes`
String: Private context for new owner (sensitive information not for customer)

### `data.stakeholder_summary`
Array of stakeholder objects:
- `name`: string
- `title`: string
- `role`: "champion" | "economic_buyer" | "evaluator" | "blocker" | "coach" | "unknown"
- `engagement_level`: "high" | "medium" | "low"
- `sentiment`: "positive" | "neutral" | "negative" | "unknown"
- `relationship_notes`: string

### `data.immediate_actions`
Array of action objects (next 48 hours):
- `action`: string
- `deadline`: string
- `priority`: "critical" | "high" | "medium"
- `success_criteria`: string

## Quality Checklist

Before returning results, validate:

- [ ] Executive summary is 3-5 sentences and gives complete deal context
- [ ] Stakeholder map includes at least 2 contacts (champion + 1 other)
- [ ] Each stakeholder has role, engagement level, sentiment, and relationship notes
- [ ] Relationship history has at least 5 key moments (if deal is mid-to-late stage)
- [ ] Deal dynamics section explains WHY they are buying, WHY NOW, and PRIMARY RISK
- [ ] MEDDICC assessment identifies at least 1 gap or risk (no deal is perfect)
- [ ] Next steps include at least 3 immediate actions with deadlines
- [ ] Internal notes include pricing context and any sensitivities
- [ ] Transition email references specific recent context (not generic)
- [ ] Completeness score reflects actual data availability (not inflated)

## Error Handling

### Minimal deal data available
If deal record exists but has minimal activity history or contact data: Generate brief with available data and set `completeness_score` to low (0-40). Include prominent warning: "Limited data available for this deal. Handoff brief is incomplete. Schedule a live handoff call with [previous owner] to fill gaps."

### No stakeholder data
If no contacts are associated with the deal: Return error: "No stakeholders found for this deal. Cannot generate handoff brief without contact information. Add at least one primary contact to the deal."

### Deal is very early stage
If deal is in "Discovery" or "Qualification" stage with minimal history: Generate a simplified brief focusing on "What we know so far" rather than comprehensive handoff. Flag: "Early-stage deal — handoff brief reflects limited engagement to date."

### New owner not specified
If `new_owner` is not provided: Generate full brief but omit the transition email. Flag: "New owner not specified. Transition email cannot be generated. Add new_owner parameter when ready to send customer communication."

### Conflicting or unclear data
If CRM data has conflicts (e.g., close date has passed but deal is still open, or MEDDICC fields contradict activity notes): Flag conflicts explicitly in the brief under a "Data Conflicts to Resolve" section and recommend the new owner verify with the previous owner.

## Examples

See inline examples in each section above for good vs. bad handoff brief content.

## Handoff Best Practices (Included in Brief as Appendix)

The handoff brief should optionally include a "Handoff Best Practices" appendix for first-time deal recipients:

```
## Handoff Best Practices

**First 48 Hours**:
1. Read this entire brief (10-15 minutes)
2. Review recent meeting recordings if available (focus on last 2 meetings)
3. Send transition email to primary contact (draft provided)
4. Schedule live handoff call with previous owner to ask questions (30 minutes)

**First Week**:
5. Have at least one live conversation with the primary contact (do not rely on email only)
6. Review all open tasks and confirm deadlines are still valid
7. Assess deal health independently (do not assume previous owner's assessment is current)

**First Month**:
8. Meet every stakeholder mentioned in the stakeholder map at least once
9. Re-validate MEDDICC (especially Economic Buyer and Decision Criteria)
10. Update CRM with your own notes and observations

**What NOT to Do**:
- Do not tell the customer "I'm new and getting up to speed" — this signals disruption
- Do not ask the customer to "catch me up" on the deal history — that is your job
- Do not change the deal strategy or next steps without understanding why the previous approach was chosen
- Do not ghost the previous owner — ask questions if anything is unclear
```
