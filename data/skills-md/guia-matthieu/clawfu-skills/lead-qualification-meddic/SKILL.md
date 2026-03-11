---
name: lead-qualification-meddic
description: Qualify enterprise opportunities using MEDDIC/MEDDPICC framework for complex B2B sales cycles
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Lead Qualification: MEDDIC

> Qualify complex enterprise opportunities using the MEDDIC framework to ensure deal viability and improve forecast accuracy.

## When to Use This Skill

- Enterprise deal qualification
- Complex sales cycles (60+ days)
- Multiple stakeholder deals
- High ACV opportunities ($50K+)
- Improving forecast accuracy

## Methodology Foundation

Based on **PTC's MEDDIC methodology** (developed by Dick Dunkel), extended to MEDDPICC:
- **M**etrics - Quantified value
- **E**conomic Buyer - Decision authority
- **D**ecision Criteria - How they'll choose
- **D**ecision Process - How they'll buy
- **I**dentify Pain - Business problem
- **C**hampion - Internal advocate
- **C**ompetition - Competitive landscape
- **P**aper Process - Legal/procurement

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures MEDDIC questions | Deal prioritization |
| Scores each component | Resource investment |
| Identifies gaps | Coaching focus |
| Creates deal summaries | Forecast commit |
| Suggests next actions | Win strategy |

## Instructions

### Step 1: Define MEDDIC Components

| Component | Definition | Key Question |
|-----------|------------|--------------|
| **Metrics** | Quantified outcomes | "What numbers will improve?" |
| **Economic Buyer** | Person with budget authority | "Who can say yes and write the check?" |
| **Decision Criteria** | How they evaluate | "What criteria will you use to decide?" |
| **Decision Process** | Steps to purchase | "What happens between now and signed contract?" |
| **Identify Pain** | Business problem | "What happens if this doesn't get solved?" |
| **Champion** | Internal advocate | "Who's fighting for this internally?" |
| **Competition** | Alternatives | "What else are you considering?" |
| **Paper Process** | Procurement/legal | "What's involved in getting contracts signed?" |

### Step 2: Discovery Questions by Component

**Metrics:**
- "If this project succeeds, what numbers will change?"
- "How will you measure ROI?"
- "What's the cost of the current problem?"
- "What KPIs are you trying to impact?"

**Economic Buyer:**
- "Who ultimately approves the budget for this?"
- "Have you worked with them on similar initiatives?"
- "Can I meet them before we finalize a proposal?"

**Decision Criteria:**
- "What are the must-haves vs nice-to-haves?"
- "How will you compare solutions?"
- "Who developed these criteria?"
- "How important is [your differentiator]?"

**Decision Process:**
- "Walk me through the steps from here to signed contract."
- "Who else needs to evaluate this?"
- "Are there approval committees or board reviews?"
- "What could delay or derail this process?"

**Identify Pain:**
- "What's driving this initiative now?"
- "What happens if you do nothing?"
- "How is this affecting your team/business/customers?"
- "Have you tried to solve this before?"

**Champion:**
- "Who's the biggest advocate for this project?"
- "What happens to them if this succeeds/fails?"
- "Can they get us access to [stakeholder]?"
- "How much influence do they have?"

**Competition:**
- "What alternatives are you considering?"
- "How far along are you with other vendors?"
- "What do you like about what you've seen?"
- "How does that compare to what we've shown you?"

**Paper Process:**
- "What's your typical procurement timeline?"
- "Are there security or legal reviews required?"
- "Have you worked with vendors like us before?"
- "What can we do to expedite the process?"

### Step 3: Score Each Component

| Score | Criteria |
|-------|----------|
| 🟢 3 | Confirmed, documented, verified |
| 🟡 2 | Identified but not confirmed |
| 🟠 1 | Weak or incomplete |
| 🔴 0 | Unknown or missing |

**Deal Qualification Levels:**
| Score | Status | Action |
|-------|--------|--------|
| 21-24 | Strong | Commit to forecast |
| 16-20 | Developing | Address gaps |
| 11-15 | Early | More discovery needed |
| <11 | Weak | Qualify out or restart |

## Examples

### Example 1: Full MEDDIC Analysis

**Output:**
```
## MEDDIC Deal Scorecard: GlobalTech ($250K)

### Deal Overview
- **Account:** GlobalTech Inc
- **Value:** $250,000 ARR
- **Stage:** Proposal
- **Close Date:** March 15
- **Sales Cycle:** 90 days (Day 60)

---

### MEDDIC Score: 18/24 🟡 Developing

| Component | Score | Status |
|-----------|-------|--------|
| Metrics | 3/3 | 🟢 |
| Economic Buyer | 2/3 | 🟡 |
| Decision Criteria | 3/3 | 🟢 |
| Decision Process | 2/3 | 🟡 |
| Identify Pain | 3/3 | 🟢 |
| Champion | 3/3 | 🟢 |
| Competition | 1/3 | 🟠 |
| Paper Process | 1/3 | 🟠 |

---

### Component Details

#### Metrics: 3/3 🟢
**Status:** Strong - Quantified and agreed

**Evidence:**
- ROI target: 3x in Year 1
- Specific KPIs: Reduce CAC by 20%, increase pipeline by 40%
- CFO signed off on business case
- Baseline metrics documented

**Quote:** "If we can hit these numbers, this pays for itself in 6 months."

---

#### Economic Buyer: 2/3 🟡
**Status:** Identified but not met

**Evidence:**
- EB: CFO Jennifer Walsh
- Champion confirmed she has budget authority
- Haven't had direct meeting yet
- Email correspondence only

**Gap:** Need face-to-face with CFO before proposal review

**Action:** Request 15-min executive alignment call

---

#### Decision Criteria: 3/3 🟢
**Status:** Strong - Criteria aligned with our strengths

**Evidence:**
- Formal RFP with weighted criteria
- Our top differentiators match their priorities:
  - Integration depth (30% weight) - ✅ Our strength
  - Time to value (25% weight) - ✅ Our strength
  - Price (20% weight) - ⚠️ Neutral
  - Support (15% weight) - ✅ Our strength
  - References (10% weight) - ✅ Have 3 ready

**Quote:** "Integration is non-negotiable for us."

---

#### Decision Process: 2/3 🟡
**Status:** Mapped but timeline fuzzy

**Evidence:**
- Step 1: Technical evaluation ✅ Complete
- Step 2: Business review ✅ Complete
- Step 3: Proposal review ⏳ This week
- Step 4: CFO approval ⏳ Pending
- Step 5: Legal/Procurement ⏳ Unknown timeline
- Step 6: Contract signed ⏳ Target March 15

**Gap:** Steps 4-6 timeline not confirmed

**Action:** Get specific dates for approval meeting and legal review

---

#### Identify Pain: 3/3 🟢
**Status:** Strong - Urgent, quantified pain

**Evidence:**
- Current problem: 40% of leads fall through cracks
- Business impact: $2M estimated lost revenue
- Trigger: Missed Q3 target, board pressure
- Previous attempts: Tried 2 solutions, both failed

**Quote:** "This is keeping our CEO up at night."

---

#### Champion: 3/3 🟢
**Status:** Strong - Active, influential champion

**Champion Profile:**
- Name: Marcus Chen, VP Revenue Operations
- Motivation: His initiative, career impact
- Influence: Direct report to CFO
- Actions taken:
  - Built internal business case
  - Scheduled all meetings
  - Defended us vs. competitor
  - Sharing our content internally

**Quote:** "I'm putting my reputation on this."

---

#### Competition: 1/3 🟠
**Status:** Weak - Incomplete intel

**Evidence:**
- Know they evaluated CompetitorX
- Don't know current status
- Champion said "we've narrowed to two"
- No details on competitor proposal

**Gap:** Critical blind spot

**Action:**
- Ask champion directly about competitor status
- Understand their proposal/pricing
- Prepare competitive battle card response

---

#### Paper Process: 1/3 🟠
**Status:** Weak - Unknown

**Evidence:**
- They have a procurement team
- Security review likely required
- No timeline documented
- Haven't met procurement

**Gap:** Could add 2-4 weeks we haven't planned for

**Action:**
- Ask champion about typical procurement timeline
- Offer to start security questionnaire early
- Get intro to procurement contact

---

### Gap Summary

| Gap | Priority | Owner | Action | Due |
|-----|----------|-------|--------|-----|
| Meet CFO | High | AE | Request exec call | Day 62 |
| Competition intel | High | AE | Discovery with champion | Day 63 |
| Paper process | Medium | SE | Start security review | Day 65 |
| Decision timeline | Medium | AE | Confirm dates | Day 65 |

---

### Forecast Recommendation

**Current:** In forecast at 50% probability
**Recommendation:** Keep in forecast, but address gaps before increasing commit

**Path to 80%:**
1. Meet CFO (Economic Buyer confirmed)
2. Confirm competitor status (know we're preferred)
3. Map procurement timeline (no surprises)

**Risks:**
- Competition could have better pricing
- Procurement could delay past March 15
- CFO hasn't engaged directly
```

### Example 2: Champion Assessment

**Output:**
```
## Champion Evaluation: Marcus Chen

### Champion Scorecard

| Criteria | Score | Evidence |
|----------|-------|----------|
| Access | 🟢 High | Direct report to EB |
| Influence | 🟢 High | Owns budget recommendation |
| Motivation | 🟢 High | Career tied to outcome |
| Credibility | 🟢 High | 8 years at company |
| Engagement | 🟢 High | Weekly calls, sharing content |
| **Overall** | **Strong Champion** | |

---

### Champion Profile

**Name:** Marcus Chen
**Title:** VP Revenue Operations
**Reports to:** Jennifer Walsh (CFO)
**Tenure:** 8 years
**Role in Deal:** Project owner and recommender

---

### Why They're Championing

1. **Personal Win:** This is his initiative; success = promotion
2. **Pain Owner:** Responsible for the problem we solve
3. **Budget Influence:** Makes recommendation to CFO
4. **Trusted:** Long tenure, respected internally

---

### Champion Actions Taken

✅ Built internal business case
✅ Scheduled all meetings
✅ Shared our ROI calculator with CFO
✅ Defended us when competitor name dropped
✅ Gave us competitive intel
✅ Proactively updated us on internal discussions

---

### Champion Test Questions

**Question: Can they sell when you're not in the room?**
Answer: Yes - built business case, defends us

**Question: Will they give you bad news?**
Answer: Yes - warned us about CFO concerns

**Question: Can they get you to the Economic Buyer?**
Answer: Partially - email intros yes, meeting not yet

---

### Champion Gaps

| Gap | Risk | Mitigation |
|-----|------|------------|
| Hasn't secured CFO meeting | Medium | Help champion prepare ask |
| Single-threaded | Medium | Build relationships with IT Director |

---

### Champion Coaching Plan

**Help Marcus succeed by:**
1. Provide leave-behind for his CFO conversation
2. Share competitor objection responses
3. Arm with 3 references he can share
4. Prepare him for likely CFO questions:
   - "Why not build this ourselves?"
   - "What's the implementation risk?"
   - "Can we get better pricing?"
```

## Skill Boundaries

### What This Skill Does Well
- Structuring complex deal qualification
- Identifying deal gaps systematically
- Creating deal coaching plans
- Improving forecast accuracy

### What This Skill Cannot Do
- Replace relationship skills
- Guarantee deal outcomes
- Know competitor strategies
- Handle negotiation tactics

## References

- PTC MEDDIC Framework (Dick Dunkel)
- Force Management MEDDICC
- Salesforce Enterprise Selling
- Winning by Design MEDDIC

## Related Skills

- `lead-qualification-bant` - Simpler qualification
- `deal-risk-scoring` - Risk assessment
- `pipeline-forecasting` - Commit based on MEDDIC

## Skill Metadata

- **Domain**: SDR Automation / Sales
- **Complexity**: Advanced
- **Mode**: centaur
- **Time to Value**: 45-60 min per deal
- **Prerequisites**: Enterprise sales experience
