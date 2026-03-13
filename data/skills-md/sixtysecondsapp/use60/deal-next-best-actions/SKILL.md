---
name: Deal Next Best Actions
description: |
  Generate a ranked action plan for advancing a specific deal based on its stage,
  recent activity, historical conversation context (via RAG transcript search), and
  external trigger events (via web research). Use when a user asks "what should I do
  next on this deal", "next steps for the Acme deal", or "how do I move this deal
  forward". Returns prioritized actions grounded in real conversation history and
  enriched with company intelligence, with ROI rationale and time estimates.
metadata:
  author: sixty-ai
  version: "3"
  category: sales-ai
  skill_type: atomic
  is_active: true
  context_profile: sales
  agent_affinity:
    - pipeline
  triggers:
    - pattern: "next steps for this deal"
      intent: "deal_next_actions"
      confidence: 0.90
      examples:
        - "what should I do next on this deal"
        - "next best actions for this deal"
        - "what are the next steps"
    - pattern: "how do I move this deal forward"
      intent: "deal_advancement"
      confidence: 0.85
      examples:
        - "how to advance this deal"
        - "move this deal forward"
        - "push this deal to the next stage"
    - pattern: "deal action plan"
      intent: "deal_actions"
      confidence: 0.80
      examples:
        - "action plan for this deal"
        - "what actions should I take on this deal"
        - "recommend actions for this deal"
  keywords:
    - "next steps"
    - "actions"
    - "deal"
    - "advance"
    - "move forward"
    - "priorities"
    - "what to do"
    - "recommendations"
  required_context:
    - deal_id
    - company_name
  inputs:
    - name: deal_id
      type: string
      description: "The deal identifier to generate next best actions for"
      required: true
    - name: deal_context
      type: object
      description: "Additional deal context such as recent activity or health signals"
      required: false
    - name: user_capacity
      type: string
      description: "User's current workload level affecting action volume"
      required: false
      default: "normal"
      example: "busy"
  outputs:
    - name: actions
      type: array
      description: "Ranked action items with type, priority, ROI rationale, and time estimates"
    - name: priorities
      type: object
      description: "Summary of priority distribution across actions"
    - name: roi_rationale
      type: string
      description: "Overall rationale for the recommended action plan"
    - name: minimum_viable_action
      type: object
      description: "Single most important action if user is busy"
    - name: rag_context_used
      type: array
      description: "Specific transcript findings that informed the recommended actions"
    - name: confidence_level
      type: string
      description: "high/medium/low — based on data richness across all intelligence layers"
    - name: trigger_events
      type: array
      description: "External events creating action opportunities (from web search enrichment)"
  requires_capabilities:
    - crm
    - web_search
  priority: high
  tags:
    - sales-ai
    - deals
    - actions
    - pipeline
    - prioritization
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Deal Next Best Actions

## Goal
Generate a ranked, prioritized action plan for advancing a deal based on stage, activity patterns, conversation history, external intelligence, and capacity. This is not a generic checklist -- it is a 5-layer situational analysis that reads the deal's signals from CRM data, past transcripts, and external triggers, diagnoses what is blocking progress, and prescribes specific actions with the highest probability of moving this deal to close.

## Why Prescriptive Actions Matter

The difference between a good rep and a great rep is not effort -- it is allocation:

- **Top-performing reps spend 65% of their time on deals they will win** (Salesforce State of Sales, 2023). Average reps spread time evenly, wasting 40%+ on dead deals.
- **The #1 reason deals stall is inaction, not objections** (Gong Labs, analysis of 70,000+ deals). 56% of "lost" deals were actually "abandoned."
- **Deals that receive a meaningful seller action every 5-7 business days close at 2.3x the rate** of deals with gaps longer than 14 days (InsightSquared pipeline analytics).
- **The right action at the right time matters more than volume.** A single well-timed executive introduction outperforms 10 follow-up emails (RAIN Group).
- **Reps who follow a next-best-action framework achieve 23% higher quota attainment** than reps who rely on intuition alone (CSO Insights, 2022).

The goal is not "do more" -- it is "do the one thing that moves the needle most, right now."

## Required Capabilities
- **CRM**: To fetch deal data, stage, recent activity, and related records
- **Web Search**: To discover company news, trigger events, and stakeholder changes that create action opportunities

## Inputs
- `deal_id`: The deal identifier (required)
- `user_capacity` (optional): "busy" | "normal" | "available" -- affects action volume
- `organization_id`: Current organization context (from session)

## The 5-Layer Intelligence Model

Work through these layers in order. Each layer builds on the previous. Skip layers only when data is unavailable (see Graceful Degradation).

### Layer 1: Deal Context (CRM Data)

Gather the foundational deal state from CRM:

1. Fetch deal: `execute_action("get_deal", { id: deal_id, include_health: true })` -- stage, value, close date, contacts, health score
2. Fetch deal health score: Check `deal_health_scores` table for `overall_health_score`, `risk_factors`, `risk_level`, `days_in_current_stage`, `sentiment_trend`, `meeting_count_last_30_days`
3. Fetch pipeline summary: `execute_action("get_pipeline_summary", {})` -- overall pipeline context
4. Fetch recent activities: `execute_action("get_deal_activities", { deal_id, limit: 20 })` -- meeting history, emails, calls
5. Fetch tasks: `execute_action("list_tasks", { deal_id })` -- existing planned actions
6. Fetch relationship health: Check `relationship_health_scores` for primary contact -- `overall_health_score`, `is_ghost_risk`, `ghost_probability_percent`, `days_since_last_contact`

**Health data integration**: Use `deal_health_score.overall_health_score` and `deal_health_score.risk_factors` to inform action prioritization. Low health scores (< 50) should trigger rescue actions before advancement actions. High ghost risk on the primary contact should trigger multi-threading or channel-switching actions.

If any data call fails, proceed with available data. Note the gap and adjust recommendations accordingly.

### Layer 2: Enrichment (Web Search)

Search for external intelligence that creates action opportunities:

1. **Company news**: Search for `"{company_name}" news` -- funding rounds, acquisitions, leadership changes, product launches, layoffs, earnings reports within last 90 days
2. **Trigger events**: Look for events that change buying urgency -- new executive hire (budget holder), competitor deal, regulatory change, expansion announcement
3. **Contact enrichment**: For key stakeholders, check for role changes, promotions, public speaking, published content that reveals priorities
4. **Industry signals**: Relevant market trends, competitor moves, or regulatory changes affecting the buyer's business

**How to use enrichment in actions**: A funding round means budget unlocked -- propose a larger deal. A leadership change means priorities may shift -- re-qualify. A competitor announcement creates urgency -- position against it. Every trigger event maps to a specific action (see `references/action-library.md` for the trigger-to-action mapping).

### Layer 3: Historical Context (RAG Transcript Search)

Before generating actions, search meeting transcripts for conversation history that should ground recommendations:

1. **Commitments made**: Search transcripts for promises by either side -- "I will send you...", "We agreed to...", "Next step is..."
2. **Concerns raised**: Search for objections, hesitations, risk language -- "Our concern is...", "We are worried about...", "The challenge is..."
3. **Agreed next steps**: Search for explicit action items from past meetings
4. **Competitive mentions**: Search for competitor names or comparison language
5. **Buying signals**: Search for positive intent -- "We would like to...", "When can we start...", "What does pricing look like..."
6. **Decision criteria**: Search for how the buyer evaluates -- "What matters most is...", "We need to see...", "The key requirement is..."

**How to use RAG context**: Every action should reference specific transcript findings where available. Instead of "Send a follow-up email," say "Send a follow-up addressing Sarah's concern from the Jan 15 call about data migration timelines." Ground actions in real conversation history, not generic playbook advice.

### Layer 4: Intelligence Signals (Health + Pattern Analysis)

Synthesize Layers 1-3 into diagnostic signals. Enhance the existing health and pattern analysis with RAG insights:

- **Health-informed prioritization**: See the Action Prioritization Framework section below
- **Activity pattern analysis**: See the Activity Pattern Analysis section below
- **RAG-enhanced signals**: If transcripts reveal an unaddressed objection, that becomes a top-priority action. If a commitment was made and not fulfilled, flag it. If competitive mentions are increasing, address the competitive threat.

### Layer 5: Action Strategy (Stage Playbooks + RAG-Grounded Specifics)

See `references/action-library.md` for the full action catalog with impact ratings, effort levels, and templates for each action type. See `references/stage-playbooks.md` for complete stage-by-stage playbooks with exit criteria, risk indicators, time limits, and worked examples.

Select and rank actions using the prioritization framework, but personalize them with specifics from Layers 2-3. Every action should be grounded in something concrete: a transcript quote, a trigger event, a health signal, or a pattern from the activity timeline.

## Action Prioritization Framework

### Health-Informed Prioritization

Before applying the Impact-Urgency-Effort matrix, check the deal's health score and risk factors:

- **Critical health (< 30)**: Prioritize rescue actions first (re-engagement, multi-threading, addressing root cause). Advancement actions are secondary until the deal is stabilized.
- **Warning health (30-60)**: Balance rescue and advancement. Address the top risk factor while maintaining momentum.
- **Healthy (60+)**: Focus on advancement actions. Optimize for speed to close.

**Risk factor mapping to actions**:
- `stage_stall` -> Identify and remove the blocker, propose next milestone
- `no_activity` -> Re-engagement action (value-add email or call)
- `sentiment_decline` -> Address objection or concern, introduce reference customer
- `no_meetings` -> Schedule discovery or check-in meeting

**Ghost risk consideration**: If primary contact has `is_ghost_risk: true` or `ghost_probability_percent > 50`, multi-threading becomes the #1 priority action regardless of other factors.

### The Impact-Urgency-Effort Matrix

Every potential action is scored on three dimensions:

**Impact (1-5):** How much does this action advance the deal toward close?
- 5: Directly creates a commitment or removes a blocker
- 4: Builds significant momentum (demo, reference call, business case)
- 3: Maintains engagement and advances understanding
- 2: Administrative or preparatory
- 1: Low-value activity

**Urgency (1-5):** What is the cost of delay?
- 5: Window closing within 48 hours
- 4: Overdue or time-sensitive (close date approaching, 14+ day gap)
- 3: Should happen this week
- 2: Important but not time-critical
- 1: Can wait without consequence

**Effort (inverted, 1-5):** How easy is it to execute?
- 5: Under 15 minutes
- 4: 15-30 minutes
- 3: 30-60 minutes
- 2: 1-3 hours
- 1: Half-day or more

**Priority Score = Impact x Urgency x Effort (inverted)**
- Score 75-125: **Urgent** -- do today
- Score 40-74: **High** -- do this week
- Score 15-39: **Medium** -- schedule for next week
- Score 1-14: **Low** -- batch with other work or delegate

### Capacity Adjustment

| Capacity | Max Actions | Focus |
|----------|-------------|-------|
| **busy** | 1 (minimum_viable_action only) | Highest-impact single action that takes <15 min |
| **normal** | 3-5 | Top actions across impact/urgency spectrum |
| **available** | 5-8 | Full action plan including preparation and optimization |

When capacity is "busy," the minimum_viable_action MUST be executable in under 15 minutes and have the highest combined impact + urgency score.

## Stage-Specific Action Playbooks

See `references/action-library.md` for the full action catalog and `references/stage-playbooks.md` for complete stage-by-stage playbooks with exit criteria, risk indicators, time limits, and worked examples.

### Stage 1-2: Discovery / Qualification
**Primary objective:** Validate the deal is worth pursuing and establish the buying process.
**Top actions:** Multi-thread into the account, quantify the pain, map the buying process, confirm BANT/MEDDIC criteria, send meeting recap with insights.
**Red flags:** No response after discovery (48h), single-threaded, no budget/timeline mention, "just exploring" language.

### Stage 3-4: Evaluation / Demo
**Primary objective:** Prove ${company_name}'s solution solves their specific problem better than alternatives.
**Top actions:** Deliver customized demo, introduce reference customer, create business case/ROI model, engage economic buyer, identify and address competitor.
**Red flags:** Demo keeps being postponed, no executive sponsor, evaluation criteria not shared.

### Stage 5-6: Negotiation / Proposal
**Primary objective:** Remove obstacles between "yes" and signature.
**Top actions:** Send proposal/contract, pre-wire negotiation, map procurement requirements, prepare concession strategy, create urgency with real constraint.
**Red flags:** "Let me think about it" without next step, new stakeholders appearing late, radio silence after proposal.

### Stage 7+: Closing
**Primary objective:** Get to signature and set up for successful implementation.
**Top actions:** Resolve final objection, make signing frictionless, preview implementation plan, align on success metrics.
**Red flags:** Contract sent but not opened, champion going quiet, close date pushed second time.

## Activity Pattern Analysis

Read `references/action-library.md` for the complete re-engagement action catalog with templates for each silence duration.

### Staleness Detection
- **7+ days**: Re-engage with value-add, NOT "just checking in."
- **14+ days**: Direct outreach to champion with specific question. If no response in 48h, call.
- **21+ days**: Breakup email. Paradoxically re-engages 15-20% of stalled deals (Gong).

### Ghosting Detection
- **2+ messages, no response**: Switch channels (call, LinkedIn, text) or go around to different stakeholder.
- **Meetings keep rescheduling**: Buyer is deprioritizing. Introduce constraint or new value.
- **"Let me get back to you" 3+ times**: Address directly -- "Are you still considering this, or has something changed?"

### Multithreading Analysis
- **1 contact**: Critical risk. Multi-threaded deals close at 3x the rate. Ask for introductions.
- **2-3 contacts**: Good but not safe. Identify who is missing (usually economic buyer or end-user champion).
- **4+ contacts**: Strong. Ensure stakeholder alignment on criteria and timeline.

## Confidence Level

Assess the data richness across all 5 layers and assign a confidence level to the overall recommendation:

| Level | Criteria | How It Affects Output |
|-------|----------|----------------------|
| **High** | CRM data complete + RAG transcripts found + web enrichment available. 3+ layers with rich data. | Actions are specific and grounded. Rationales cite transcript quotes, trigger events, and health signals. |
| **Medium** | CRM data available + at least one of RAG or web enrichment. 2 layers with data. | Actions are informed but some are stage-generic. Flag which layers are missing. |
| **Low** | CRM data only, or CRM data is sparse. Only 1 layer has meaningful data. | Actions default to stage playbook recommendations. Prominently flag: "Limited data -- these are playbook defaults, not deal-specific recommendations. Enrich this deal for better actions." |

Always include the confidence level in the output and explain what data informed the recommendation (and what was missing).

## Graceful Degradation

| Missing Data | Fallback Behavior | User-Facing Note |
|---|---|---|
| CRM deal record incomplete | Proceed with available fields; first action = "Update deal stage and close date in CRM" | "Deal record is missing [fields]. Recommendations are based on available data." |
| No activity history | Default to stage-appropriate actions from playbook | "No activity history available. Recommendations based on deal stage only." |
| RAG returns no transcripts | Proceed without transcript grounding; actions are stage-generic | "No meeting transcripts found. Actions are not grounded in conversation history." |
| Web search fails or returns nothing | Proceed without trigger events; skip Layer 2 | "External enrichment unavailable. No trigger events detected." |
| Contact not enriched | Skip stakeholder mapping; recommend enrichment | "Contact details are thin. Consider running enrichment before next outreach." |
| Health scores unavailable | Skip health-informed prioritization; use stage + activity only | "Health scoring unavailable. Prioritization based on stage and activity patterns." |
| Conflicting signals (verbal vs. behavioral) | Prioritize behavioral signals over verbal ones | "Buyer says [X] but activity shows [Y]. Behavioral data is more predictive." |
| 10+ open tasks already exist | Do not add more; prioritize existing tasks | "You have [X] open tasks. Complete or close the top 3 before adding new actions." |
| Deal appears dead (30+ days, past close date) | Honest assessment + single reactivation action | "This deal shows no activity in [X] days. Confirm viability before investing time." |

## Output Contract

Return a SkillResult with:
- `data.actions`: Array of action objects (ranked by priority score):
  - `action_type`: "email" | "call" | "meeting" | "task" | "crm_update" | "research" | "internal_alignment" | "reference_call" | "proposal" | "demo"
  - `title`: Action title (specific and actionable)
  - `description`: What to do (detailed enough to execute without follow-up questions)
  - `priority`: "urgent" | "high" | "medium" | "low"
  - `priority_score`: number (Impact x Urgency x Effort)
  - `roi_rationale`: Why this action matters -- connect to data, transcript quotes, or trigger events
  - `estimated_time`: Time estimate in minutes
  - `deadline`: Recommended deadline (ISO date)
  - `owner`: Suggested owner (user's name or role)
  - `dependencies`: Other actions this depends on (array of action titles or empty)
  - `source_layer`: Which intelligence layer informed this action (e.g., "RAG: Jan 15 call", "Web: funding round", "Health: ghost risk")
- `data.priorities`: Summary of priority distribution (how many urgent/high/medium/low)
- `data.roi_rationale`: Overall rationale for the action plan (2-3 sentences explaining the strategy)
- `data.minimum_viable_action`: The single most important action if user is busy (must be <15 min effort)
- `data.stage_insights`: Insights about deal stage and what typically works at this stage
- `data.rag_context_used`: Array of specific transcript findings that informed actions (quote, date, speaker, relevance)
- `data.confidence_level`: "high" | "medium" | "low" with explanation of data richness
- `data.trigger_events`: Array of external events creating action opportunities (event, source, recommended_action, urgency_impact)

## Quality Checklist

Before returning the action plan, verify:

- [ ] Actions are ranked by priority score, not alphabetically or randomly
- [ ] Every action has a specific ROI rationale tied to THIS deal's situation, not generic advice
- [ ] Time estimates are realistic (not everything is "5 minutes")
- [ ] The minimum_viable_action is genuinely the highest-impact thing the rep can do in under 15 minutes
- [ ] Actions account for existing open tasks (no duplicates)
- [ ] If activity gap is detected (7+ days), re-engagement is the #1 priority
- [ ] If only 1 contact is engaged, multi-threading is in the top 3 actions
- [ ] Actions match the deal stage (not recommending a discovery call for a deal in negotiation)
- [ ] At least one action involves the BUYER doing something (not all seller-side)
- [ ] Deadlines are specific dates, not "soon" or "next week"
- [ ] If the deal has a close date, actions are aligned to that timeline
- [ ] The overall rationale tells a coherent story about WHERE this deal is and WHAT moves it forward
- [ ] RAG transcript findings are cited in action rationales where available (quote + date)
- [ ] Trigger events from web search are connected to specific actions (not just listed)
- [ ] Confidence level accurately reflects data richness across the 5 layers
- [ ] Every data claim has a source (CRM field, transcript quote, web search result, health signal)

## Error Handling

### Deal not found or data incomplete
If the deal record is missing critical fields (stage, value, close date), return actions focused on data completion: "Update deal stage and close date in CRM" as the first action, then provide best-effort recommendations based on available data.

### No activity history available
Without activity data, you cannot detect staleness or ghosting. Default to stage-appropriate actions and flag: "No activity history available. These recommendations are based on deal stage only."

### Deal is in a very early stage with minimal data
If the deal is in Stage 1 with only a name and company, focus entirely on discovery: research the company, identify stakeholders, prepare discovery questions, schedule the first call.

### Deal appears to be dead (no activity 30+ days, past close date)
Be honest: "This deal shows no activity in [X] days and the close date has passed. Before investing time, confirm with the buyer that the opportunity is still active." Provide a single reactivation action, not a full plan.

### User capacity is "busy" but the deal is critical
Note the tension: "This is your most critical deal, but you indicated limited capacity. The minimum viable action is [X]. However, this deal is at risk if [Y] is not addressed this week. Consider delegating [Z] to free up 30 minutes."

## Tone and Presentation

- Be direct and specific. "Send a 3-bullet email to Sarah Chen addressing her data migration concern from the Jan 15 call" not "Consider reaching out to the prospect."
- Explain the WHY in plain language. Reps follow advice they understand and believe.
- Be honest about dead or dying deals. Saying "this deal may not be worth your time" is valuable advice.
- Frame actions as experiments. "Try this because the data shows..." not "You must do this."
- Acknowledge trade-offs. "This action takes 45 minutes, but it addresses the #1 blocker on your highest-value deal."
- Ground in specifics. Reference transcript quotes, trigger events, and health signals -- not generic playbook advice.
