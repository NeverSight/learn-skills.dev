---
name: Daily Focus Planner
description: |
  Generate a prioritized daily action plan with top deals, contacts needing attention,
  next best actions, and a task pack. Use when a user asks "what should I focus on today",
  "plan my day", "prioritize my tasks", or wants to know what needs their attention most.
  Returns ranked priorities, concrete actions, and ready-to-create tasks.
metadata:
  author: sixty-ai
  version: "2"
  category: sales-ai
  skill_type: atomic
  is_active: true
  context_profile: full
  agent_affinity:
    - pipeline
  triggers:
    - pattern: "what should I focus on today"
      intent: "daily_focus"
      confidence: 0.90
      examples:
        - "what should I focus on"
        - "what are my priorities today"
        - "plan my day"
        - "daily focus"
    - pattern: "prioritize my tasks"
      intent: "task_prioritization"
      confidence: 0.85
      examples:
        - "help me prioritize"
        - "what needs my attention"
        - "what's most important today"
    - pattern: "create a plan for today"
      intent: "daily_planning"
      confidence: 0.80
      examples:
        - "make a plan"
        - "daily plan"
        - "organize my day"
  keywords:
    - "focus"
    - "priorities"
    - "plan"
    - "today"
    - "attention"
    - "important"
    - "organize"
    - "tasks"
    - "action plan"
  requires_capabilities:
    - crm
    - tasks
  requires_context:
    - company_name
    - pipeline_deals
    - contacts_needing_attention
    - open_tasks
  inputs:
    - name: date
      type: string
      description: "The date to generate the focus plan for in ISO format"
      required: false
      default: "today"
      example: "2025-01-15"
    - name: time_of_day
      type: string
      description: "Current time context for prioritization weighting"
      required: false
      example: "morning"
    - name: user_capacity
      type: string
      description: "User's current workload level affecting task volume"
      required: false
      default: "normal"
      example: "busy"
  outputs:
    - name: priorities
      type: array
      description: "5-8 priority items ranked by urgency with type, reason, and context"
    - name: actions
      type: array
      description: "5-8 concrete next best actions with priority, time estimate, and ROI rationale"
    - name: task_pack
      type: array
      description: "Top 3 task previews ready to create, targeting fastest pipeline movement"
  priority: critical
---

## Available Context & Tools
@_platform-references/org-variables.md
@_platform-references/capabilities.md

# Daily Focus Planner

## Goal
Create a **prioritized daily action plan** that tells the rep exactly what to do today and why. This is not a briefing (that is the Daily Brief Planner's job). A briefing answers "What's happening?" A focus plan answers **"What should I DO?"**

The difference is critical. A briefing is a newspaper; a focus plan is a battle plan. It ranks, selects, and commits the rep to specific actions that maximize pipeline movement given their available time.

## The Briefing vs. Focus Plan Distinction

| Dimension | Daily Briefing | Daily Focus Plan |
|-----------|---------------|-----------------|
| **Question answered** | "What's going on?" | "What should I do?" |
| **Orientation** | Informational | Prescriptive |
| **Output** | Status summary | Ranked action list + task pack |
| **Decision required** | None (read and absorb) | Yes (commit to top actions) |
| **Time to consume** | 30 seconds (scan) | 2 minutes (review and commit) |
| **Updates during day** | Can re-run for latest status | Should be set once in the morning |

## Why Prioritized Planning Beats Reactive Selling

Research consistently shows that disciplined daily planning drives quota attainment:

- **Reps with a written daily plan** close 27% more pipeline than those who "wing it" (CSO Insights)
- **The top 20% of reps** spend 33% less time on low-value activities because they plan before they act (Gartner)
- **Decision fatigue** costs the average rep 2.5 hours per day in context-switching and task-selection overhead (McKinsey)
- **The Zeigarnik Effect**: Unfinished tasks occupy mental bandwidth. A clear plan with defined scope frees cognitive resources for selling.

The focus plan eliminates the "what should I do next?" question. Every minute spent deciding is a minute not spent selling.

## Priority Ranking Methodology

### The CVHS Score (Close date x Value x Health x Staleness)

Every deal and action is scored using four weighted factors. Consult `references/focus-frameworks.md` for the CVHS deep dive with worked scoring examples and override rules.

```
PRIORITY_SCORE = (Close_Urgency x 0.35) + (Value_Weight x 0.25) + (Health_Risk x 0.25) + (Staleness x 0.15)
```

#### Close Urgency (35% weight)
The single strongest signal. Deals closing soon need action NOW.

| Close Date | Score | Label |
|-----------|-------|-------|
| Today or overdue | 100 | CRITICAL |
| This week | 85 | Urgent |
| Next week | 60 | High |
| This month | 40 | Medium |
| Next month+ | 15 | Low |
| No close date | 30 | Medium (penalized for missing data) |

#### Value Weight (25% weight)
Higher-value deals justify more time investment.

| Deal Value vs. Average | Score |
|----------------------|-------|
| 3x+ average | 100 |
| 2-3x average | 80 |
| 1-2x average | 50 |
| Below average | 25 |
| Unknown value | 40 |

#### Health Risk (25% weight)
At-risk deals need intervention before they die.

| Health Score | Score | Interpretation |
|-------------|-------|---------------|
| 0-30 | 100 | Critical -- likely to lose without immediate action |
| 31-50 | 80 | At risk -- needs attention this week |
| 51-70 | 50 | Needs monitoring |
| 71-90 | 20 | Healthy |
| 91-100 | 5 | Strong -- minimal attention needed |
| No health score | 50 | Unknown = assume moderate risk |

#### Staleness (15% weight)
Days since last meaningful activity on the deal.

| Days Stale | Score |
|-----------|-------|
| 14+ days | 100 |
| 10-13 days | 80 |
| 7-9 days | 60 |
| 4-6 days | 30 |
| 0-3 days | 5 |

### The "One Thing" Principle

After scoring all actions, identify the single highest-impact action. See `references/focus-frameworks.md` for the "One Thing" selection criteria, scenario-specific patterns, and the Focusing Question framework. This becomes the **headline recommendation**:

> "If you could only do ONE thing today, do this: [action]"

The one thing is the action with the highest CVHS score AND the clearest path to completion today. A high-score action that requires a 3-day process does not qualify as the "one thing."

Selection criteria for the "one thing":
1. Highest CVHS score among completable-today actions
2. Has a clear, concrete next step (not "research" or "think about")
3. Directly moves a deal forward (advances stage, unblocks decision, re-engages champion)
4. Can be done in under 30 minutes

## Capacity-Aware Planning

The number of recommended actions scales to the rep's available bandwidth. See `references/capacity-guide.md` for the full available hours calculation, overcommitment detection algorithm, and capacity templates by day type.

| Capacity Level | Actions | Task Pack | Signal |
|---------------|---------|-----------|--------|
| **Busy** (back-to-back meetings, travel day) | 1-2 | 1 task | Focus only on the "one thing" |
| **Normal** (typical day, some meetings) | 3-5 | 3 tasks | Balanced action set |
| **Available** (light meeting day, focused time) | 5-8 | 3-5 tasks | Expand to include nurture and prospecting |

**Auto-detection heuristics** (when `user_capacity` is not provided):
- 5+ meetings today = "busy"
- 10+ open overdue tasks = "busy" (they're already overwhelmed)
- 2-4 meetings = "normal"
- 0-1 meetings = "available"

**Never exceed 8 actions** regardless of capacity. Research on cognitive load shows that action lists beyond 7 items cause decision paralysis and reduce completion rates.

## Action Concreteness Standard

Every recommended action MUST meet the **SMART-A standard** (Specific, Measurable, Achievable, Relevant, Time-bound, Assigned):

### Bad Actions (too vague)
- "Follow up on deal" -- Follow up how? With whom? About what?
- "Check in with contact" -- What's the purpose? What outcome do you want?
- "Work on pipeline" -- This is a category, not an action.
- "Review proposal" -- Review for what? What's the decision point?

### Good Actions (concrete and completable)
- "Send revised pricing proposal to Sarah Chen at Acme Corp, addressing the 15% discount request from Tuesday's call"
- "Call Mike Ross at TechFlow to re-engage -- he hasn't responded in 9 days. Ask about the budget committee meeting."
- "Email David Kim the case study he requested (FinServ vertical, 30% efficiency gain) and propose Thursday for a technical demo"
- "Update the Acme deal stage from Proposal to Negotiation and log the pricing discussion from today's call"

### The Concreteness Test
For each action, ask: "Could a colleague execute this action with zero additional context?" If not, add more specifics.

Required elements for every action:
1. **Verb** -- What to do (send, call, email, schedule, update, create)
2. **Target** -- Who it's directed at (person name and company)
3. **Content** -- What the communication/action contains
4. **Context** -- Why now (linked to a deal event, timeline, or risk signal)

## ROI Rationale Framework

Every action must include a one-sentence rationale explaining **why this action matters more than alternatives**:

### Rationale Templates by Category

**Revenue protection**: "This $[X] deal closes [when] and [risk signal] -- acting today prevents [consequence]."
- Example: "This $45K deal closes Friday and Sarah hasn't replied since Tuesday -- acting today prevents the deal slipping to next month."

**Revenue acceleration**: "[Deal] is at [stage] and [positive signal] -- [action] could advance it to [next stage] this week."
- Example: "TechFlow is at Demo stage and Mike confirmed budget approval -- sending the proposal today could advance to Negotiation this week."

**Relationship recovery**: "[Contact] has been dark for [X days] on a [value] deal -- re-engagement now has a [Y%] higher success rate than waiting."
- Example: "James Park has been dark for 9 days on a $28K deal -- re-engagement now has a 60% higher success rate than waiting another week."

**Pipeline hygiene**: "[X deals] are stale/outdated -- cleaning the pipeline improves forecast accuracy and frees mental bandwidth."

## Task Pack Design

The task pack converts the top 3 recommended actions into ready-to-create tasks. These are designed to be accepted with one click.

### Task Pack Requirements

Each task in the pack must include:

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Action-oriented, starts with verb, under 80 chars | "Send revised pricing to Sarah Chen (Acme)" |
| `description` | 2-3 sentences with context and a mini-checklist | See below |
| `due_date` | ISO date, prefer "today" or "tomorrow" | "2025-01-15" |
| `priority` | Derived from CVHS score: >70 = high, 40-70 = medium, <40 = low | "high" |
| `deal_id` | Linked deal if applicable | "deal_abc123" |
| `contact_id` | Linked contact if applicable | "contact_xyz789" |

### Description Template
```
Context: [Why this task exists -- the deal situation and trigger]
Action: [Exactly what to do]
Checklist:
- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3 -- log the outcome]
```

### Example Task Pack Entry
```json
{
  "title": "Send revised pricing to Sarah Chen (Acme Corp)",
  "description": "Context: Acme Corp ($45K) is in Proposal stage, closing Friday. Sarah requested a 15% volume discount on Tuesday's call.\nAction: Send the revised pricing sheet with the approved discount tier.\nChecklist:\n- [ ] Pull the approved discount matrix from the pricing doc\n- [ ] Customize the proposal PDF with Acme's volumes\n- [ ] Send via email with a suggested call for Thursday to review\n- [ ] Log the email in CRM and set a 24-hour follow-up reminder",
  "due_date": "2025-01-15",
  "priority": "high",
  "deal_id": "deal_abc123",
  "contact_id": "contact_sarah_chen"
}
```

## Time Estimation Methodology

Each action receives a time estimate to help the rep plan their day:

| Action Type | Typical Duration | Notes |
|------------|-----------------|-------|
| Send email (with customization) | 10-15 min | Includes writing, reviewing, personalizing |
| Phone call (with prep) | 15-20 min | Includes reviewing notes, making the call, logging |
| Schedule a meeting | 5-10 min | Finding availability, sending invite |
| Update CRM records | 5-10 min | Stage changes, notes, next steps |
| Prepare proposal/deck | 30-60 min | Customization, review, formatting |
| Research / account review | 15-30 min | Reviewing history, news, preparing talking points |
| Internal sync (manager, SE) | 15 min | Quick alignment before external action |

**Total time budget**: Sum all recommended actions. If total exceeds available hours (based on meeting gaps), reduce the action list until it fits. A plan the rep cannot complete is worse than no plan.

## Pipeline Velocity Impact

Connect each action to its pipeline impact using this framework:

| Action | Pipeline Metric Affected | Expected Impact |
|--------|------------------------|-----------------|
| Re-engage stale contact | Cycle time (reduces stall) | Prevents 15-30 day deal extension |
| Send proposal | Conversion rate (stage advancement) | Advances deal to Negotiation |
| Book next meeting | Velocity (keeps momentum) | Maintains 3-5 day cadence |
| Handle objection | Win rate | Addresses #1 reason deals stall |
| Multi-thread (new contact) | Win rate (+15-25% with 3+ contacts) | De-risks single-champion dependency |
| Update forecast | Pipeline accuracy | Improves commit reliability |

## Inputs

- `pipeline_deals`: from `execute_action("get_pipeline_deals", { filter: "closing_soon", period: "this_week", include_health: true, limit: 10 })`
- `contacts_needing_attention`: from `execute_action("get_contacts_needing_attention", { days_since_contact: 7, filter: "at_risk", limit: 10 })`
- `open_tasks`: from `execute_action("list_tasks", { status: "pending", limit: 20 })`

## Output Contract

Return a SkillResult with:

- `data.one_thing`: object -- The single most important action today
  - `title`: string
  - `description`: string
  - `entity_type`: "deal" | "contact"
  - `entity_id`: string
  - `rationale`: string
  - `estimated_time`: number (minutes)

- `data.priorities`: array of 5-8 priority items
  - `type`: "deal" | "contact" | "task"
  - `id`: string
  - `name`: string
  - `reason`: string (why it needs attention now)
  - `urgency`: "critical" | "high" | "medium"
  - `context`: string (deal stage, days stale, value, etc.)
  - `cvhs_score`: number (0-100, for transparency)

- `data.actions`: array of 3-8 next best actions (adjusted by capacity)
  - `title`: string (verb-first, under 80 characters)
  - `description`: string (concrete, passes the colleague test)
  - `priority`: "urgent" | "high" | "medium" | "low"
  - `entity_type`: "deal" | "contact" | "task"
  - `entity_id`: string | null
  - `estimated_time`: number (minutes)
  - `roi_rationale`: string (why this matters more than alternatives)
  - `pipeline_impact`: string (which metric this action affects)

- `data.task_pack`: array of 3 task previews (top actions, ready to create)
  - `title`: string
  - `description`: string (include context and checklist)
  - `due_date`: string (ISO date, prefer "today" or "tomorrow")
  - `priority`: "high" | "medium" | "low"
  - `deal_id`: string | null
  - `contact_id`: string | null

- `data.time_budget`: object
  - `total_action_minutes`: number
  - `available_minutes`: number (estimated from meeting gaps)
  - `capacity_assessment`: "busy" | "normal" | "available"

## Quality Checklist

Before returning the focus plan, verify:

- [ ] "One thing" is identified and meets the completable-today criteria
- [ ] All actions pass the concreteness test (verb + target + content + context)
- [ ] Action count matches capacity level (busy: 1-2, normal: 3-5, available: 5-8)
- [ ] Every action has an ROI rationale (not just "needs follow-up")
- [ ] Task pack has exactly 3 items (or fewer if capacity is "busy")
- [ ] Task pack descriptions include checklists
- [ ] Time estimates are realistic and total fits available time
- [ ] CVHS scores are calculated, not arbitrary
- [ ] No duplicate actions (e.g., two actions targeting the same contact for the same reason)
- [ ] Priorities are ranked, not just listed
- [ ] Actions cover different deal stages (not all focused on one deal)
- [ ] No fabricated deal data or contact names
- [ ] Entity IDs included for all linked deals and contacts

## Error Handling

### Empty pipeline (no deals)
Shift focus entirely to tasks and prospecting. Actions should center on:
- Completing overdue tasks
- Prospecting new leads
- Nurturing existing contacts
- Administrative pipeline hygiene
Message: "Your pipeline is empty. Today's focus: building pipeline through prospecting and outreach."

### No contacts needing attention
This is a healthy signal. Note it positively: "All contacts are recently engaged -- nice work." Focus actions on deal advancement and tasks instead.

### No tasks
Generate actions purely from deal and contact data. Every deal or stale contact implies a natural next action. Include a note: "No pending tasks found. The actions below are generated from your pipeline status."

### All deals healthy
When no deals are at risk, shift from defensive to offensive actions:
- Advance deals to next stage
- Multi-thread into additional contacts
- Prepare for upcoming close dates
- Prospect for new pipeline
Message: "Pipeline looks strong. Focus on acceleration and prospecting today."

### Conflicting priorities (too many critical items)
When more than 3 items score as "critical," apply tiebreakers in order:
1. Highest deal value wins
2. Nearest close date wins
3. Longest stale period wins
Cap critical items at 3 and downgrade the rest to "high."

### Capacity mismatch (too many actions for available time)
If total estimated time exceeds available hours by more than 25%, trim from the bottom of the priority list. Add note: "Your day is packed. I've trimmed to the top [X] actions that fit your available time."

### Missing health scores
When health data is unavailable, increase the weight of staleness and close date in the CVHS calculation. Note: "Deal health scores unavailable -- prioritizing by close date and activity recency."

### Afternoon/evening request
If the focus plan is requested after 2pm, adjust:
- Remove actions that require morning energy (cold calls, major proposals)
- Focus on quick wins completable before end of day
- Include a "tomorrow's top priority" preview
- Reduce action count by 50% (half the day is gone)
