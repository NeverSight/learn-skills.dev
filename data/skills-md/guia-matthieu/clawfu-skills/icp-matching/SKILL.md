---
name: icp-matching
description: Score and qualify prospects against your Ideal Customer Profile using firmographic, technographic, and behavioral criteria
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# ICP Matching

> Systematically evaluate prospects against your Ideal Customer Profile to prioritize high-fit accounts and improve SDR efficiency.

## When to Use This Skill

- Building lead scoring models
- Qualifying inbound leads
- Prioritizing outbound target accounts
- Refining ICP definitions
- Training SDRs on qualification

## Methodology Foundation

Based on **TOPO ICP Framework** and **Gartner B2B Buying Research**, combining:
- Firmographic fit (company attributes)
- Technographic fit (tech stack)
- Behavioral signals (intent data)
- Persona fit (contact attributes)

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures ICP framework | ICP criteria values |
| Scores prospects against ICP | Pass/fail thresholds |
| Identifies fit gaps | Prioritization rules |
| Suggests disqualification | Exception handling |
| Ranks prospect lists | Territory assignments |

## Instructions

### Step 1: Define ICP Dimensions

**Firmographic Criteria:**
| Attribute | Ideal | Acceptable | Disqualify |
|-----------|-------|------------|------------|
| Company Size | 100-1000 | 50-2000 | <25 or >5000 |
| Revenue | $10M-$500M | $5M-$1B | <$2M |
| Industry | SaaS, Tech | Professional Services | Government |
| Geography | US, Canada | UK, EU | APAC |
| Growth Stage | Series A-C | Seed, Series D+ | Pre-seed |

**Technographic Criteria:**
| Attribute | Ideal | Acceptable | Disqualify |
|-----------|-------|------------|------------|
| CRM | Salesforce | HubSpot | None |
| Tech Stack | Modern | Mixed | Legacy only |
| Competitors | None installed | Evaluating | Locked in |

**Persona Criteria:**
| Attribute | Ideal | Acceptable | Disqualify |
|-----------|-------|------------|------------|
| Title | VP/Director | Manager | Coordinator |
| Department | Sales, Marketing | RevOps | IT |
| Decision Power | Budget authority | Influencer | User only |

### Step 2: Weight and Score

**Scoring Model:**
```
ICP Score =
  (Firmographic × 40%) +
  (Technographic × 30%) +
  (Persona × 30%)

Each dimension: 0-100 points
```

**Score Interpretation:**
| Score | Fit | Action |
|-------|-----|--------|
| 80-100 | Excellent | Prioritize immediately |
| 60-79 | Good | Standard outreach |
| 40-59 | Fair | Nurture, low priority |
| <40 | Poor | Disqualify |

### Step 3: Apply to Prospects

For each prospect:
1. Gather available data
2. Score each dimension
3. Calculate weighted score
4. Classify and prioritize

## Examples

### Example 1: ICP Definition

**Output:**
```
## Ideal Customer Profile: B2B Sales Tech Company

### Tier 1 (Excellent Fit - 80-100)
**These are your ideal targets. Prioritize always.**

**Company:**
- Size: 100-500 employees
- Revenue: $20M-$200M ARR
- Stage: Series B or C funded
- Industry: B2B SaaS
- Growth: 30%+ YoY
- Location: US/Canada

**Technology:**
- CRM: Salesforce
- Stack: Modern (cloud-native)
- Current solution: None or legacy competitor

**Buyer:**
- Title: VP Sales, CRO, Head of Sales
- Reports to: CEO/COO
- Budget: >$50K annually

---

### Tier 2 (Good Fit - 60-79)
**Worth pursuing with standard effort.**

**Company:**
- Size: 50-100 OR 500-1000 employees
- Revenue: $10M-$20M OR $200M-$500M
- Stage: Series A or D
- Industry: B2B Tech (not pure SaaS)
- Location: UK, EU

**Technology:**
- CRM: HubSpot
- Stack: Mix of modern/legacy
- Current solution: Considering change

**Buyer:**
- Title: Director of Sales Ops
- Reports to: VP Sales
- Budget: $25K-$50K annually

---

### Tier 3 (Fair Fit - 40-59)
**Nurture only. Don't prioritize.**

**Company:**
- Size: 25-50 OR 1000-2000 employees
- Revenue: $5M-$10M
- Stage: Seed
- Industry: Professional services

**Buyer:**
- Title: Sales Manager
- Budget: <$25K

---

### Disqualified (Score <40)
**Do not pursue. Auto-reject.**

- Company size <25 employees
- Revenue <$2M
- Industry: Government, Education, Non-profit
- Geography: APAC, LATAM (no support)
- Competitor locked in (multi-year contract)
- No CRM in use
- Title: Individual contributor
```

### Example 2: Prospect Scoring

**Input:**
```
Score this prospect:

Company: GrowthTech Inc
Employees: 280
Revenue: $45M (estimated)
Industry: B2B SaaS
Founded: 2019
Location: Austin, TX
Recent news: Series B ($30M) in January

Tech Stack:
- CRM: Salesforce Enterprise
- Marketing: Marketo
- No sales engagement tool

Contact: Jennifer Wu
Title: VP of Revenue Operations
LinkedIn: Active, posts about sales productivity
Previous company: Used our competitor
```

**Output:**
```
## ICP Match: GrowthTech Inc

### Overall Score: 92/100 ⭐ EXCELLENT FIT

---

### Firmographic Score: 95/100

| Criteria | Finding | Points |
|----------|---------|--------|
| Size (280 emp) | ✅ Ideal (100-500) | 20/20 |
| Revenue ($45M) | ✅ Ideal ($20-200M) | 20/20 |
| Industry (B2B SaaS) | ✅ Ideal | 20/20 |
| Stage (Series B) | ✅ Ideal | 20/20 |
| Location (US) | ✅ Ideal | 15/15 |
| **Subtotal** | | **95/100** |

### Technographic Score: 90/100

| Criteria | Finding | Points |
|----------|---------|--------|
| CRM (Salesforce) | ✅ Ideal | 35/35 |
| Stack (Modern) | ✅ Marketo + SF | 25/25 |
| Competition | ✅ None installed | 30/30 |
| **Subtotal** | | **90/100** |

### Persona Score: 92/100

| Criteria | Finding | Points |
|----------|---------|--------|
| Title (VP RevOps) | ✅ Decision maker | 35/35 |
| Department | ✅ Revenue Operations | 25/25 |
| Activity | ✅ Active on LinkedIn | 15/20 |
| Previous | ✅ Knows competitor | 15/15 |
| **Subtotal** | | **92/100** |

---

### Weighted Total
```
(95 × 0.40) + (90 × 0.30) + (92 × 0.30)
= 38 + 27 + 27.6
= 92.6 → 92/100
```

---

### Match Summary

**🎯 Tier 1: Excellent Fit**

**Strengths:**
1. Perfect company size/stage/industry
2. Salesforce user (easy integration story)
3. VP RevOps = ideal buyer persona
4. Recent funding = budget available
5. No competitor installed = greenfield

**Conversation Angles:**
1. "Congrats on Series B! How is that affecting your sales team scale?"
2. "I noticed you're not using a sales engagement tool yet—most RevOps leaders at your stage are building that out now."
3. "Given your Salesforce/Marketo stack, our integration would be seamless."

**Risk Factors:**
- None identified

**Priority: Immediate outreach**
Add to top of SDR queue. High-value, high-probability.
```

## Skill Boundaries

### What This Skill Does Well
- Structuring ICP frameworks
- Scoring prospects systematically
- Identifying fit gaps
- Prioritizing outreach

### What This Skill Cannot Do
- Access company databases
- Verify data accuracy
- Know internal buying dynamics
- Predict conversion likelihood

### When to Escalate to Human
- ICP definition changes
- Borderline accounts
- Strategic target accounts
- Exception requests

## References

- TOPO ICP Framework
- Gartner B2B Buying Research
- SalesLoft ICP Best Practices
- Outreach.io Target Account Model

## Related Skills

- `lead-scoring` - RevOps scoring model
- `signal-monitoring` - Intent data
- `prospecting-research` - Deep account research

## Skill Metadata

- **Domain**: SDR Automation
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 2 hours for ICP, 5 min per prospect
- **Prerequisites**: ICP criteria definition
