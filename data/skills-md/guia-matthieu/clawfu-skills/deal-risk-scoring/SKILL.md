---
name: deal-risk-scoring
description: Assess deal health and identify at-risk opportunities using engagement signals, stakeholder mapping, and velocity analysis
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Deal Risk Scoring

> Evaluate individual deal health through multi-signal analysis to prioritize coaching, intervention, and resource allocation.

## When to Use This Skill

- Weekly deal reviews and pipeline scrubs
- Before QBRs to identify problem deals
- When deals stall or push close dates
- Prioritizing manager coaching time
- Allocating SE/executive resources

## Methodology Foundation

Based on **Gong's Deal Intelligence research** and **Winning by Design's Revenue Architecture**, analyzing:
- Engagement velocity (email, meeting frequency)
- Stakeholder breadth (multi-threading)
- Competitive signals
- Timeline alignment
- Champion strength

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Scores deals on risk factors | Which deals to save vs. let go |
| Identifies missing elements | Resource allocation priorities |
| Suggests intervention actions | Executive sponsor assignments |
| Tracks velocity trends | Final stage/probability updates |
| Flags competitive threats | Win strategy adjustments |

## What This Skill Does

1. **Multi-signal analysis** - Engagement, stakeholders, timeline, competition
2. **Risk scoring** - Green/Yellow/Red health status with reasons
3. **Gap identification** - Missing stakeholders, stalled stages, unclear next steps
4. **Action recommendations** - Specific interventions to reduce risk
5. **Trend tracking** - Velocity changes over time

## How to Use

```
Assess the risk for this deal:

Deal: [Company Name]
Value: $X
Stage: [Current Stage]
Close Date: [Target Date]
Days in Stage: X

Recent Activity:
- [List emails, meetings, calls with dates]

Stakeholders:
- [Name, Title, Role in deal, Engagement level]

Competition: [Known competitors]
Champion: [Name and strength assessment]
```

## Instructions

### Step 1: Engagement Velocity Score (0-25 points)

| Criteria | Points |
|----------|--------|
| Meeting in last 7 days | +10 |
| Email response in last 3 days | +5 |
| Multiple contacts engaged | +5 |
| Prospect initiating contact | +5 |
| No activity 14+ days | -15 |

### Step 2: Stakeholder Coverage Score (0-25 points)

| Criteria | Points |
|----------|--------|
| Economic Buyer identified | +10 |
| Champion confirmed | +10 |
| Technical evaluator engaged | +5 |
| Only 1 contact | -10 |
| No C-level access | -5 |

### Step 3: Process Alignment Score (0-25 points)

| Criteria | Points |
|----------|--------|
| Clear next step scheduled | +10 |
| Mutual action plan agreed | +10 |
| Decision timeline confirmed | +5 |
| Close date pushed 2+ times | -15 |
| No defined process | -10 |

### Step 4: Competitive Position Score (0-25 points)

| Criteria | Points |
|----------|--------|
| No competition | +15 |
| Differentiation clear | +10 |
| Incumbent advantage | -10 |
| Price pressure | -5 |
| Unknown competitive status | -5 |

### Step 5: Calculate Total Risk Score

| Score | Health | Action |
|-------|--------|--------|
| 75-100 | 🟢 Green | Monitor, standard process |
| 50-74 | 🟡 Yellow | Intervention needed |
| 25-49 | 🟠 Orange | Escalate, major action |
| 0-24 | 🔴 Red | Rescue or disqualify |

## Examples

### Example 1: At-Risk Enterprise Deal

**Input:**
```
Deal: TechCorp Global
Value: $250K ARR
Stage: 3 - Proposal
Close Date: Feb 28 (pushed from Jan 31)
Days in Stage: 28

Recent Activity:
- Jan 15: Proposal sent to John (Dir of Ops)
- Jan 22: Follow-up email (no response)
- Jan 29: Called, voicemail
- Feb 5: Email asking for update (no response)

Stakeholders:
- John Smith, Director of Ops, Champion (was engaged)
- No other contacts

Competition: Competitor X mentioned in discovery
Champion: John - went silent
```

**Output:**
```
## Deal Risk Assessment: TechCorp Global

### Overall Score: 28/100 🔴 RED - HIGH RISK

### Score Breakdown

| Factor | Score | Issues |
|--------|-------|--------|
| Engagement | 0/25 | No response in 14+ days |
| Stakeholders | 5/25 | Single-threaded, no EB |
| Process | 5/25 | Pushed once, no clear next step |
| Competition | 18/25 | Competitor known but not blocking |
| **Total** | **28/100** | |

### Critical Risks

1. **🔴 Champion Gone Dark** - John hasn't responded in 14 days
   - Possible: Left company, lost internal support, chose competitor

2. **🔴 Single-Threaded** - No other relationships
   - If John is out, deal is dead

3. **🟠 No Economic Buyer** - Never met decision maker
   - John may not have authority to close

### Recommended Actions

**This Week:**
1. Research John on LinkedIn - still at company?
2. Find another contact via LinkedIn/referral
3. Send "breakup email" to force response
4. Check if Competitor X is in active eval

**If No Response by Friday:**
- Move to Stage 2 or Closed-Lost
- Free up forecast slot

### Red Flags to Watch
- If proposal was forwarded to competitor
- If budget was reallocated
- If project was deprioritized

### Save Probability: 25%
Without new contact access, this deal is likely lost.
```

### Example 2: Healthy Deal Review

**Input:**
```
Deal: GrowthCo Inc
Value: $85K ARR
Stage: 4 - Negotiation
Close Date: Feb 15
Days in Stage: 7

Recent Activity:
- Feb 1: Demo to full team (8 attendees)
- Feb 3: Pricing discussion with CFO
- Feb 5: Legal reviewing MSA
- Feb 7: Call scheduled for Feb 10

Stakeholders:
- Maria Lopez, VP Sales (Champion, highly engaged)
- Tom Chen, CFO (Economic Buyer, positive)
- Legal team (reviewing contract)
- 8 end users attended demo

Competition: None identified
Champion: Maria - actively selling internally
```

**Output:**
```
## Deal Risk Assessment: GrowthCo Inc

### Overall Score: 88/100 🟢 GREEN - HEALTHY

### Score Breakdown

| Factor | Score | Status |
|--------|-------|--------|
| Engagement | 25/25 | Daily activity, prospect-driven |
| Stakeholders | 23/25 | EB + Champion + Users confirmed |
| Process | 22/25 | Clear timeline, legal in motion |
| Competition | 18/25 | No competition identified |
| **Total** | **88/100** | |

### Strengths

1. **✅ Multi-threaded** - Champion, EB, and end users engaged
2. **✅ Process momentum** - Legal reviewing = serious intent
3. **✅ Executive access** - CFO in pricing discussions
4. **✅ Champion active** - Maria driving internally

### Minor Risks

1. **🟡 Legal review** - Could surface unexpected blockers
   - Mitigation: Pre-review common redlines

2. **🟡 No competition confirmed** - May be unknown
   - Mitigation: Ask directly in next call

### Recommended Actions

**Feb 10 Call Prep:**
1. Prepare redline responses for common legal issues
2. Confirm decision process post-legal
3. Ask: "Is anyone else in consideration?"
4. Get verbal commit from Maria

### Close Probability: 85%
Deal is on track. Focus on removing legal friction.
```

## Skill Boundaries

### What This Skill Does Well
- Objective risk scoring from available data
- Identifying gaps in deal coverage
- Prioritizing which deals need attention
- Suggesting specific interventions

### What This Skill Cannot Do
- Know information not provided (internal politics)
- Predict competitor moves
- Replace relationship judgment
- Guarantee score accuracy with incomplete data

### When to Escalate to Human
- Strategic accounts requiring executive judgment
- Deals involving partnerships or M&A
- Unusual contract structures
- Competitive intelligence gathering

## Iteration Guide

### Follow-up Prompts
- "What's the single most important action for this deal?"
- "Compare risk scores for my top 5 deals."
- "What questions should I ask in the next meeting?"
- "Draft a re-engagement email for the silent champion."

### Refinement Cycle
1. Initial assessment → Identify top risks
2. Take action → Update activity log
3. Re-score → Track improvement
4. Weekly review → Trend analysis

## Checklists & Templates

### Deal Health Checklist
- [ ] Champion identified and engaged this week
- [ ] Economic Buyer met at least once
- [ ] Next step scheduled within 7 days
- [ ] Competition status known
- [ ] Close date validated by prospect

### Risk Score Template
```markdown
## Deal: [Name] | Score: X/100 [Status Emoji]

### Quick Stats
- Value: $X | Stage: X | Days: X | Close: [Date]

### Scores
| Factor | Score | Key Issue |
|--------|-------|-----------|
| Engagement | /25 | |
| Stakeholders | /25 | |
| Process | /25 | |
| Competition | /25 | |

### Top 3 Actions
1.
2.
3.
```

## References

- Gong Deal Intelligence Research
- Winning by Design Revenue Architecture
- MEDDPICC Qualification Framework
- Force Management Command of the Message

## Related Skills

- `pipeline-forecasting` - Aggregate deal health into forecast
- `lead-qualification-meddic` - Deep qualification framework
- `account-health` - Post-sale relationship scoring

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 10 minutes per deal
- **Prerequisites**: Deal details, activity history, stakeholder map
