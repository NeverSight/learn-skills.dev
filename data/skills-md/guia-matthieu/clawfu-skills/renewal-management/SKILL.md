---
name: renewal-management
description: Manage the customer renewal process with health-based playbooks, timeline tracking, and risk mitigation strategies
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Renewal Management

> Execute systematic renewal processes using health-based segmentation, proactive outreach, and risk mitigation to maximize retention.

## When to Use This Skill

- Building renewal playbooks by segment
- Managing renewal pipeline
- Handling at-risk renewals
- Forecasting renewal revenue
- Optimizing renewal timing

## Methodology Foundation

Based on **Gainsight Renewal Management** and **SaaS Renewal Best Practices**, focusing on:
- Health-based renewal approach
- Timeline-driven playbooks
- Risk mitigation strategies
- Expansion during renewal

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Creates renewal timelines | Discount authority |
| Builds health-based playbooks | Pricing decisions |
| Identifies renewal risks | Save vs. let go |
| Suggests save strategies | Contract terms |
| Calculates renewal forecast | Executive involvement |

## Instructions

### Step 1: Segment by Health + Contract

**Renewal Matrix:**

| Health | Contract Value | Approach |
|--------|----------------|----------|
| 🟢 High + High | Expand + Multi-year |
| 🟢 High + Low | Upsell |
| 🟡 Medium + Any | Standard renewal |
| 🟠 Low + High | Save priority |
| 🔴 Critical + Any | Executive save |

### Step 2: Define Renewal Timeline

**Standard Timeline (90-Day):**

| Days Out | Activity | Owner |
|----------|----------|-------|
| 120 | Health check, flag risks | CSM |
| 90 | Renewal kickoff | CSM |
| 75 | Value review call | CSM |
| 60 | Proposal sent | CSM/Sales |
| 45 | Negotiation | Sales |
| 30 | Final terms | Sales |
| 14 | Signature push | Sales |
| 0 | Renewal close | Sales |

### Step 3: Build Health-Based Playbooks

**Green Playbook (Healthy):**
- Light touch, focus on expansion
- Lead with value summary
- Propose multi-year

**Yellow Playbook (Monitor):**
- Standard engagement
- Address any concerns early
- Secure commitment before term end

**Orange/Red Playbook (At-Risk):**
- Heavy engagement
- Executive involvement
- Save plan execution

### Step 4: Calculate Renewal Forecast

```
Renewal Forecast =
  (Green × 95%) +
  (Yellow × 80%) +
  (Orange × 50%) +
  (Red × 25%)
```

## Examples

### Example 1: Renewal Playbook

**Output:**
```
## Renewal Playbook: 90-Day Process

### Healthy Customer (Health Score >75)

**Goal:** Renew with expansion or multi-year

**Day 120: Pre-Renewal Check**
- [ ] Review health score and trends
- [ ] Check expansion opportunities
- [ ] Prepare value summary

**Day 90: Renewal Kickoff**
- [ ] Send renewal notice email
- [ ] Schedule value review call
- [ ] Prepare ROI documentation

**Day 75: Value Review Call (45 min)**
Agenda:
1. Relationship check (5 min)
2. Value delivered review (15 min)
3. 2026 priorities (10 min)
4. Renewal discussion (10 min)
5. Next steps (5 min)

Script: "Based on [X value delivered], we'd love to continue our partnership. I'd like to discuss options for next year, including a multi-year agreement that could give you better terms."

**Day 60: Proposal**
- Standard or upgrade proposal
- Multi-year option (5-10% discount)
- Expansion options

**Day 45-14: Light Follow-Up**
- Procurement coordination
- Answer questions
- Minimal negotiation

**Day 0: Close**
- Expected close rate: 95%
- Expected expansion: 10-20%

---

### At-Risk Customer (Health Score <50)

**Goal:** Save the account, then renew

**Day 120: Risk Assessment**
- [ ] Deep dive on health issues
- [ ] Identify root cause
- [ ] Develop save plan
- [ ] Alert leadership

**Day 90: Save Plan Activation**
- [ ] Executive sponsor outreach
- [ ] Service recovery actions
- [ ] Address root causes

**Day 75: Executive Check-In**
- [ ] VP/Director involvement
- [ ] Commitment to resolution
- [ ] Timeline for improvement

**Day 60: Renewal Conversation**
Only if health improving:
- Acknowledge challenges
- Show commitment to success
- Flexible terms if needed

**Day 45: Negotiation**
Options to consider:
- Short-term renewal (6 months)
- Reduced scope/price
- Success-based terms

**Day 30: Decision Point**
If not improving:
- Prepare for potential churn
- Discuss graceful exit options
- Maintain relationship

**Expected Outcomes:**
- Save rate: 40-50%
- Full renewal: 25%
- Reduced renewal: 15%
- Churn: 50-60%
```

### Example 2: Renewal Forecast

**Input:**
```
Q2 Renewals:
- 10 accounts, $1.2M ARR total

Health distribution:
- Green: 4 accounts ($500K)
- Yellow: 3 accounts ($400K)
- Orange: 2 accounts ($200K)
- Red: 1 account ($100K)
```

**Output:**
```
## Q2 Renewal Forecast

### By Health Segment

| Health | Accounts | ARR | Prob | Forecast |
|--------|----------|-----|------|----------|
| 🟢 Green | 4 | $500K | 95% | $475K |
| 🟡 Yellow | 3 | $400K | 80% | $320K |
| 🟠 Orange | 2 | $200K | 50% | $100K |
| 🔴 Red | 1 | $100K | 25% | $25K |
| **Total** | **10** | **$1.2M** | | **$920K** |

### Forecast Summary
- **Base Forecast:** $920K (77% of total)
- **At Risk:** $280K (23% of total)
- **Expected Churn:** $280K

### Scenario Analysis

| Scenario | Retention | ARR |
|----------|-----------|-----|
| Best Case | 90% | $1.08M |
| Base Case | 77% | $920K |
| Worst Case | 60% | $720K |

### Actions to Improve

**To reach 85% retention ($1.02M):**
1. Convert 1 Yellow → Green (+$20K)
2. Save 1 Orange account (+$100K)
3. Maintain Green at 95%

**Priority Actions:**
| Account | Health | ARR | Action |
|---------|--------|-----|--------|
| OrangeCo #1 | 🟠 | $120K | Executive save plan |
| OrangeCo #2 | 🟠 | $80K | Success intervention |
| RedCorp | 🔴 | $100K | Last-resort save or exit |
```

## Skill Boundaries

### What This Skill Does Well
- Building renewal timelines
- Creating health-based playbooks
- Forecasting renewal revenue
- Identifying save strategies

### What This Skill Cannot Do
- Access your CRM data
- Make pricing decisions
- Execute renewal conversations
- Know specific customer dynamics

### When to Escalate to Human
- Discount approvals
- Contract modifications
- Executive relationships
- Legal/procurement issues

## References

- Gainsight Renewal Management
- SaaStr Renewal Best Practices
- ChurnZero Renewal Playbooks
- Totango Renewal Automation

## Related Skills

- `churn-prediction` - Risk identification
- `account-health` - Health scoring
- `expansion-signals` - Expand at renewal
- `qbr-preparation` - Pre-renewal QBR

## Skill Metadata

- **Domain**: Customer Success
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 30 min per renewal, 2-4 hours for playbook
- **Prerequisites**: Health scores, contract data
