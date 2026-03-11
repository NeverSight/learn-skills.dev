---
name: qbr-preparation
description: Automate QBR preparation with account summaries, success metrics, challenges, and strategic recommendations
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# QBR Preparation

> Generate comprehensive Quarterly Business Review materials including account history, success metrics, challenges, and strategic recommendations.

## When to Use This Skill

- Preparing quarterly customer reviews
- Executive business reviews (EBRs)
- Annual planning sessions with customers
- Renewal discussions
- Strategic account planning

## Methodology Foundation

Based on **Gainsight QBR Best Practices** and **Strategic Account Management**, structuring reviews around:
- Value delivered (backward-looking)
- Current health and engagement
- Future opportunities and risks
- Strategic recommendations

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Compiles account history | Strategic positioning |
| Calculates success metrics | Recommendations to present |
| Identifies risks and opportunities | Pricing and terms |
| Drafts talking points | Relationship dynamics |
| Creates presentation structure | Meeting facilitation |

## What This Skill Does

1. **Account summary** - Key facts and history
2. **Value documentation** - Metrics and achievements
3. **Health assessment** - Current status and trends
4. **Risk/opportunity analysis** - What to watch and pursue
5. **Strategic recommendations** - Next quarter priorities

## How to Use

```
Prepare QBR materials for:

Account: [Company Name]
Contract: $[ARR], Started: [Date], Renewal: [Date]
Primary Contact: [Name, Title]
CSM: [Your name]

Account History:
- [Major milestones, implementations, expansions]
- [Key wins and challenges]

Usage/Success Metrics:
- [Key metrics with current values and trends]
- [Goals they set vs. achieved]

Recent Activity:
- [Support tickets, calls, meetings last quarter]
- [Any escalations or issues]

Relationship Status:
- Champion: [Name, engagement level]
- Exec Sponsor: [Status]
- Other stakeholders: [List]

Known Opportunities/Risks:
- [Expansion potential, concerns mentioned, competitors]
```

## Instructions

### Step 1: Compile Account Overview

**Key Facts Section:**
```
Account Snapshot
- Company: [Name]
- Industry: [Sector]
- Size: [Employees/Revenue]
- Product: [What they bought]
- Contract: $X ARR | Since [Date] | Renews [Date]
- Health: [Score] | [Status]
```

### Step 2: Document Value Delivered

**The Win Section (Critical):**

| Category | Format |
|----------|--------|
| Quantified ROI | "Saved X hours, $Y dollars, Z%" |
| Goals achieved | Their stated goals → our impact |
| Milestones | Major accomplishments |
| Testimonial-worthy | Quote-able successes |

**Structure:**
```
"When you started with us, you wanted to [GOAL].
In Q[X], you achieved [RESULT]."
```

### Step 3: Assess Current Health

**Health Dashboard:**
```
| Dimension | Score | Trend | Notes |
|-----------|-------|-------|-------|
| Product | X/25 | ↗️↘️→ | Key metric |
| Support | X/25 | ↗️↘️→ | CSAT, tickets |
| Financial | X/25 | ↗️↘️→ | Payment, growth |
| Relationship | X/25 | ↗️↘️→ | Engagement |
| **Overall** | **X/100** | | |
```

### Step 4: Identify Risks and Opportunities

**Risk Assessment:**
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Action] |

**Opportunity Assessment:**
| Opportunity | Value | Timeline | Next Step |
|-------------|-------|----------|-----------|
| [Opp] | $X | Q1/Q2 | [Action] |

### Step 5: Develop Recommendations

**Strategic Recommendations Framework:**
1. **Continue** - What's working, keep doing
2. **Start** - New initiatives for next quarter
3. **Stop** - What should we change or deprioritize

## Examples

### Example 1: Full QBR Prep

**Input:**
```
Prepare QBR for CloudTech Industries:

Account: CloudTech Industries (Manufacturing)
Contract: $180K ARR, Started: Jan 2024, Renewal: Jan 2027
Primary: Sarah Chen, VP Operations
CSM: Alex

History:
- Implemented in 60 days (target was 90)
- Added 50 seats in Q2 ($30K expansion)
- Had a major support escalation in Q3 (resolved)
- Reduced production downtime by 35%

Metrics:
- DAU: 145/200 seats (73%)
- Key feature (alerts): 89% adoption
- CSAT: 4.3 (was 3.8 during escalation)
- NPS: 8

Recent Activity:
- 3 support tickets (minor)
- Monthly check-in calls
- Sarah attended user conference

Relationship:
- Champion: Sarah Chen (strong)
- Exec Sponsor: COO Mike Johnson (met once)
- Also engaged: IT Director, 3 plant managers

Opportunities/Risks:
- They're opening 2 new plants (expansion?)
- Competitor demo'd to IT last month
- Sarah mentioned "budget review" for next year
```

**Output:**
```
## QBR Preparation: CloudTech Industries
### Q4 2025 Business Review

---

## 📋 Executive Summary

**Account Health: 78/100 🟢 Healthy**

CloudTech has achieved significant operational improvements, including **35% reduction in production downtime**. The Q3 support escalation was resolved and CSAT has recovered. Two key opportunities: **new plant expansion** and **deepening executive relationship**. One risk to monitor: competitor activity and budget review timing.

**Recommended QBR Focus:**
1. Celebrate the 35% downtime reduction (ROI story)
2. Discuss new plant rollout plan
3. Secure executive sponsor re-engagement

---

## 🏢 Account Snapshot

| Attribute | Value |
|-----------|-------|
| Company | CloudTech Industries |
| Industry | Manufacturing |
| Contract Value | $180,000 ARR |
| Customer Since | January 2024 (11 months) |
| Renewal Date | January 2027 |
| Health Score | 78/100 🟢 |
| CSM | Alex |

**Key Contacts:**
| Name | Title | Role | Engagement |
|------|-------|------|------------|
| Sarah Chen | VP Operations | Champion | High |
| Mike Johnson | COO | Exec Sponsor | Low (1 meeting) |
| [IT Director] | IT Director | Technical | Medium |
| 3 Plant Managers | Operations | Users | High |

---

## 📈 Value Delivered

### Headline Metric
> **35% reduction in production downtime**
> *"Before [Product], we were losing 12 hours/month to unplanned downtime. Now it's under 8 hours."*

### Quarterly Achievements

| Goal | Target | Achieved | Status |
|------|--------|----------|--------|
| Reduce downtime | 25% | 35% | ✅ Exceeded |
| Implementation | 90 days | 60 days | ✅ Exceeded |
| User adoption | 70% | 73% | ✅ Met |
| Alert response time | <15 min | 11 min avg | ✅ Exceeded |

### ROI Calculation (Talking Point)
```
Downtime cost: ~$5,000/hour
Hours saved: 4 hours/month × 11 months = 44 hours
Value delivered: 44 × $5,000 = $220,000
Contract value: $180,000
ROI: 122% (already paid for itself)
```

### Journey Milestones
- ✅ Jan 2024: Implementation (30 days early!)
- ✅ Q2 2024: Added 50 seats ($30K expansion)
- ⚠️ Q3 2024: Support escalation (resolved)
- ✅ Q4 2024: 35% downtime reduction achieved

---

## 🎯 Current Health

### Score Breakdown

| Dimension | Score | Trend | Notes |
|-----------|-------|-------|-------|
| Product | 29/40 | → | 73% DAU, strong adoption |
| Support | 12/15 | ↗️ | Recovered from escalation |
| Financial | 20/25 | → | Current, expanded once |
| Relationship | 17/20 | → | Strong champion, weak exec |
| **Total** | **78/100** | | 🟢 Healthy |

### Engagement Metrics

| Metric | Q3 | Q4 | Trend |
|--------|----|----|-------|
| DAU | 140 | 145 | ↗️ +4% |
| Feature adoption | 85% | 89% | ↗️ |
| CSAT | 3.8 | 4.3 | ↗️ Recovering |
| Support tickets | 8 | 3 | ↗️ Improved |
| NPS | 6 | 8 | ↗️ |

---

## ⚠️ Risks & Opportunities

### Risks to Discuss

| Risk | Level | Details | Mitigation |
|------|-------|---------|------------|
| Competitor | 🟡 Medium | Demo'd to IT last month | Competitive defense, exec engagement |
| Budget review | 🟡 Medium | Sarah mentioned "budget discussions" | Reinforce ROI before budget cycle |
| Exec relationship | 🟡 Medium | COO met only once | Request exec-to-exec call |

### Opportunities to Pursue

| Opportunity | Value | Probability | Next Step |
|-------------|-------|-------------|-----------|
| 2 new plants | $60-90K | 60% | Discuss rollout timeline |
| Additional modules | $40K | 40% | Demo predictive features |
| Case study | N/A | 80% | Request with 35% stat |

---

## 💬 QBR Agenda (Suggested)

**Duration: 60 minutes**

| Time | Topic | Lead |
|------|-------|------|
| 0:00 | Welcome, agenda | CSM |
| 0:05 | Their priorities for 2026 | Sarah |
| 0:15 | Value recap: 35% downtime story | CSM |
| 0:25 | Health dashboard review | CSM |
| 0:35 | New plant expansion discussion | Both |
| 0:45 | Product roadmap preview | CSM |
| 0:55 | Next steps and actions | Both |

---

## 📝 Talking Points

### Opening
"Sarah, before we dive in, I want to acknowledge the incredible progress your team has made. A 35% reduction in downtime is exceptional—most customers see 20-25% in their first year."

### Competitive Defense (if needed)
"I heard [Competitor] came by. Happy to do a side-by-side comparison, but I'd also point out: you've already achieved ROI with us. Switching has real costs—time, retraining, risk. Let's talk about what's driving the evaluation."

### Budget Concern
"You mentioned budget reviews coming up. Would it help if I prepared a one-page ROI summary your team could use internally? The 35% downtime number plus the $220K in savings is a strong story."

### Expansion Ask
"With two new plants opening, I want to make sure we're ahead of the curve. What's the timeline? We could do a phased rollout to minimize disruption."

### Executive Engagement
"I'd love to get Mike more involved. Would it make sense to schedule a brief executive update—maybe 20 minutes—where we share the ROI story and get his input on strategic priorities?"

---

## ✅ Pre-QBR Checklist

- [ ] Confirm attendees (Sarah + who else?)
- [ ] Send agenda 3 days before
- [ ] Prepare one-page health summary
- [ ] Update ROI calculation with latest numbers
- [ ] Review competitor battle card
- [ ] Prepare new plant rollout options
- [ ] Draft follow-up email template

---

## 📊 Supporting Materials

### Attachment 1: Health Score Trend
[Include chart showing Q1-Q4 trend]

### Attachment 2: ROI One-Pager
[One-page summary of 35% stat + dollar value]

### Attachment 3: Product Roadmap Preview
[2-3 upcoming features relevant to their use case]
```

## Skill Boundaries

### What This Skill Does Well
- Structuring QBR content
- Calculating ROI and metrics
- Identifying risks and opportunities
- Drafting talking points

### What This Skill Cannot Do
- Know internal customer politics
- Access your CRM/analytics directly
- Facilitate the actual meeting
- Make pricing decisions

### When to Escalate to Human
- Pricing/contract negotiations
- Escalation-level issues
- Executive relationship strategy
- Competitive positioning

## Iteration Guide

### Follow-up Prompts
- "Draft the one-page ROI summary for their CFO."
- "Create a competitive defense script for this QBR."
- "What questions should I ask about the new plants?"
- "Write the follow-up email after this QBR."

## Checklists & Templates

### QBR Prep Checklist
- [ ] Account overview verified
- [ ] Metrics pulled and validated
- [ ] ROI calculated
- [ ] Risks/opportunities identified
- [ ] Agenda drafted
- [ ] Talking points prepared
- [ ] Materials attached
- [ ] Calendar confirmed

## References

- Gainsight QBR Best Practices
- Miller Heiman Strategic Selling
- Customer Success QBR Templates
- Executive Business Review Guide

## Related Skills

- `account-health` - Health scoring input
- `expansion-signals` - Opportunity identification
- `churn-prediction` - Risk assessment

## Skill Metadata

- **Domain**: Customer Success
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 30-60 min per QBR
- **Prerequisites**: Account history, metrics, relationship context
