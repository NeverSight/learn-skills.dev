---
name: franchisee-scoring
description: >
  Weighted franchisee selection scorecard generator. Builds recruitment criteria
  and scoring models parameterized by {target_franchisee} profile and
  {product_type} competency requirements. Use when designing franchisee
  selection criteria, building recruitment scorecards, evaluating franchise
  candidates, or comparing franchisee applicants for any franchise system.
---

# Franchisee Scoring

## Core Variables

| Variable | Examples | Impact on Scorecard |
|---|---|---|
| `{target_franchisee}` | operator, investor, corporate, hybrid | Determines weight distribution across criteria |
| `{product_type}` | software, food, education, healthcare, fitness | Determines domain expertise requirements |
| `{business_model}` | SaaS, physical_retail, service, hybrid | Determines operational competency requirements |
| `{franchise_model}` | single-unit, multi-unit, area_development, master_franchise | Determines scale of financial and management requirements |

## Required Inputs

- **Franchise System**: Description, maturity, current network size.
- **Target Franchisee Profile**: Operator vs. investor vs. corporate.
- **Territory Requirements**: What the franchisee needs to do in territory.
- **Financial Requirements**: Minimum investment, net worth, liquidity.

## Execution Steps

### 1. Ideal Franchisee Profile (IFP)

Build the IFP based on `{target_franchisee}` and `{product_type}`:

**Profile Archetypes**

| Dimension | Operator | Investor | Corporate | Hybrid |
|---|---|---|---|---|
| Day-to-day involvement | Full-time, hands-on | Part-time, oversight | Delegated to manager | Transition from operator to oversight |
| Financial profile | Moderate net worth, willing to work in business | High net worth, portfolio investor | Entity-backed, multi-unit capable | Growing net worth, reinvests |
| Management experience | May be first-time owner | Experienced manager of managers | Corporate operations team | Growing management skill |
| Domain expertise | Preferred but trainable | Not required (hires it) | Acquires or hires | Builds over time |
| Growth ambition | 1-3 units | 3-10+ units | 10+ units or master | 1 unit → multi-unit path |
| Risk tolerance | Moderate (personal investment) | Moderate-high (diversified) | Calculated (portfolio) | Moderate |

### 2. Scoring Criteria with Weights

**Financial Criteria**

| Criterion | Description | Weight by Archetype |
|---|---|---|
| Net worth | Total assets minus liabilities | Operator: 15% / Investor: 10% / Corporate: 10% |
| Liquid capital | Cash and easily convertible assets | Operator: 15% / Investor: 10% / Corporate: 10% |
| Credit score | Creditworthiness indicator | Operator: 10% / Investor: 5% / Corporate: 5% |
| Financing capability | Ability to secure additional capital | Operator: 5% / Investor: 10% / Corporate: 10% |

**Operational Criteria**

| Criterion | Description | Weight by Archetype |
|---|---|---|
| `{product_type}` domain experience | Direct experience in the industry | Operator: 15% / Investor: 5% / Corporate: 10% |
| Sales/business development ability | Track record of revenue generation | Operator: 15% / Investor: 5% / Corporate: 5% |
| People management experience | History of managing teams | Operator: 5% / Investor: 10% / Corporate: 10% |
| Multi-unit management | Experience operating multiple locations | Operator: 0% / Investor: 10% / Corporate: 15% |
| Local market knowledge | Familiarity with territory | Operator: 10% / Investor: 5% / Corporate: 5% |

**Cultural Fit Criteria**

| Criterion | Description | Weight by Archetype |
|---|---|---|
| Brand alignment | Values alignment with franchise brand | All: 5% |
| System compliance | Willingness to follow the system | Operator: 5% / Investor: 10% / Corporate: 5% |
| Community involvement | Local presence and engagement | Operator: 5% / Investor: 5% / Corporate: 0% |
| Growth mindset | Ambition and continuous improvement | All: 5% |
| Coachability | Receptiveness to training and feedback | Operator: 10% / Investor: 5% / Corporate: 5% |

### 3. Product-Type-Specific Criteria

Add criteria specific to `{product_type}`:

| Product Type | Additional Criteria | Why It Matters |
|---|---|---|
| Software/SaaS | Technical literacy, B2B sales experience, implementation project management | Must sell, implement, and support technology |
| Food/Restaurant | Food service experience, health code knowledge, hospitality orientation | Food safety and customer experience are critical |
| Education/Training | Education sector experience, local institution relationships, curriculum delivery | Credibility with educational decision-makers |
| Healthcare | Clinical background or healthcare management, regulatory knowledge | Compliance-heavy, trust-dependent |
| Fitness/Wellness | Personal training/fitness background, membership sales experience | Community-building and retention-driven |
| Professional Services | Professional credentials, client relationship management, team leadership | Quality delivered through people |
| Home Services | Trade experience or management, local market presence, fleet management | Execution-intensive, reputation-driven |

### 4. Scoring Methodology

**Scoring Scale (per criterion)**

| Score | Label | Definition |
|---|---|---|
| 5 | Exceptional | Exceeds requirements significantly — competitive advantage |
| 4 | Strong | Fully meets requirements with demonstrated evidence |
| 3 | Adequate | Meets minimum requirements — trainable on gaps |
| 2 | Below Standard | Gaps that require significant development |
| 1 | Disqualifying | Does not meet minimum threshold |

**Minimum Thresholds (Go/No-Go)**

| Category | Minimum Score | Rationale |
|---|---|---|
| Financial criteria | All items ≥ 3 | Cannot undercapitalize a franchise |
| `{product_type}` domain experience | ≥ 2 (trainable) or ≥ 4 (if no training program) | Must deliver competently |
| Brand alignment | ≥ 3 | Misaligned franchisees damage the brand |
| Overall weighted score | ≥ 3.5 | Below this correlates with franchisee failure |

**Decision Matrix**

| Weighted Score | Decision | Action |
|---|---|---|
| 4.5-5.0 | Strong Approve | Fast-track to discovery day |
| 3.5-4.4 | Approve | Proceed to discovery day, note development areas |
| 3.0-3.4 | Conditional | Address gaps before proceeding — specific plan required |
| 2.0-2.9 | Decline | Does not meet criteria — provide feedback |
| < 2.0 | Disqualify | Immediate decline |

### 5. Recruitment Funnel Benchmarks

Track conversion rates at each stage:

| Stage | Description | Benchmark Conversion |
|---|---|---|
| Lead | Initial inquiry or application | 100% (starting point) |
| Qualified Lead | Meets basic financial and background criteria | 30-40% |
| Application | Completes full application with financials | 50-60% of qualified |
| Interview | Phone/video screening with franchise development | 60-70% of applications |
| Discovery Day | In-person or virtual deep-dive | 50-60% of interviews |
| Awarded | Franchise agreement signed | 40-60% of discovery day |
| Opened | Unit operational | 85-95% of awarded |

**Overall funnel**: Expect 3-5% of initial leads to become operating franchisees.

## Output Template

```markdown
## Franchisee Scoring Model: [Franchise Name]

### Engagement Parameters
| Variable | Value |
|---|---|
| Target Franchisee | {target_franchisee} |
| Product Type | {product_type} |
| Business Model | {business_model} |
| Franchise Model | {franchise_model} |

### Ideal Franchisee Profile
[Narrative description of the ideal candidate]

### Weighted Scorecard
| Category | Criterion | Weight | Min Score | Candidate Score | Weighted |
|---|---|---|---|---|---|
| Financial | Net worth | X% | 3 | /5 | |
| Financial | Liquid capital | X% | 3 | /5 | |
| [Continue for all criteria] | | | | | |
| **TOTAL** | | **100%** | | | **/5.00** |

### Decision: [Approve / Conditional / Decline]
[Rationale with strengths and development areas]

### Recruitment Funnel Targets
[Conversion benchmarks for the franchise system]
```

## Quality Checks

- Weights sum to 100% across all criteria.
- `{target_franchisee}` archetype drives weight distribution (not one-size-fits-all).
- `{product_type}`-specific criteria included beyond generic business skills.
- Minimum thresholds defined as go/no-go gates (not just weighted into score).
- Decision matrix has clear action per score band.
- Recruitment funnel benchmarks included for pipeline planning.
