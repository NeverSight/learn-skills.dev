---
name: system-selection
description: >
  Structured system and vendor selection methodology using weighted scoring with
  stakeholder-aligned criteria. USE THIS SKILL when the user asks about vendor
  evaluation, RFP creation, build vs buy decisions, system selection, ERP selection,
  CRM selection, platform evaluation, software procurement, or technology vendor
  comparison. Covers the full lifecycle from requirements gathering through contract
  negotiation with TCO modeling and decision presentation frameworks.
---

# System Selection

## Required Inputs

- **System Type**: Category of system being selected (ERP, CRM, HRIS, data platform, etc.).
- **Business Context**: Why this selection is happening (new implementation, replacement, consolidation).
- **Stakeholder Map**: Key decision-makers, influencers, and end users.
- **Budget Range**: Capital and operating budget constraints.
- **Timeline**: Decision timeline and target go-live date.
- **Constraints**: Mandatory requirements, regulatory needs, integration dependencies, preferred vendors.

## Execution Steps

### 1. Requirements Gathering

Gather requirements across four categories. Each requirement is rated by priority and assigned a stakeholder owner.

**Requirement Priority Classification:**

| Priority | Label | Definition | Scoring Impact |
|---|---|---|---|
| P1 | **Must Have** | Non-negotiable; vendor fails without it | Eliminatory -- vendor disqualified if unmet |
| P2 | **Should Have** | Important; significant impact on success | High weight in scoring (3x multiplier) |
| P3 | **Nice to Have** | Desirable; adds value but not essential | Standard weight in scoring (1x multiplier) |
| P4 | **Future** | Not needed now but anticipated within 2 years | Low weight (0.5x multiplier) |

**Functional Requirements Template:**

| ID | Requirement | Description | Priority | Stakeholder | Source |
|---|---|---|---|---|---|
| FR-001 | | | P1/P2/P3/P4 | | |

**Categories to cover:**
- **Functional**: Business capabilities, workflows, reporting, user experience
- **Technical**: Architecture, APIs, security, performance, scalability, data model
- **Integration**: Systems to connect, data flows, real-time vs batch, middleware
- **Non-Functional**: Availability SLA, response time, data residency, accessibility, compliance

**Requirements Discovery Methods:**
1. Stakeholder interviews (1:1 with decision-makers and power users)
2. Process mapping workshops (current state and desired future state)
3. Pain point analysis (top 10 issues with current system)
4. Data flow analysis (what data moves between systems)
5. Regulatory review (compliance requirements that constrain selection)

### 2. Build vs. Buy vs. Configure Decision

Before evaluating vendors, determine if buying is the right approach.

**Decision Scorecard:**

| Factor | Weight | Build (Custom) | Buy (SaaS/License) | Configure (Low-Code/Platform) | Score |
|---|---|---|---|---|---|
| Strategic differentiation | 15% | 5: Full control, unique IP | 1: Same as competitors | 3: Moderate customization | |
| Time to value | 15% | 1: 12-24 months | 5: 1-6 months | 4: 3-9 months | |
| Total cost (5 year) | 15% | Variable, often underestimated | Predictable licensing | Moderate, platform fees | |
| Maintenance burden | 10% | 5: Full ownership | 1: Vendor managed | 3: Shared responsibility | |
| Talent availability | 10% | Specialized skills required | Lower barrier | Platform-specific skills | |
| Vendor/platform risk | 10% | None | Lock-in, viability risk | Platform dependency | |
| Scalability | 10% | Depends on architecture | Vendor-managed scaling | Platform-dependent | |
| Integration flexibility | 10% | Full control | API-dependent | Platform ecosystem | |
| Regulatory compliance | 5% | Full control | Vendor certification | Platform certification | |
| **Weighted Total** | **100%** | | | | |

**Decision Threshold:**
- Build score > Buy by 20%+: Proceed with build (validate with CTO/CIO)
- Scores within 20%: Default to buy unless strong strategic differentiation argument
- Buy score > Build: Proceed with vendor evaluation (below)

### 3. Market Landscape Analysis

**Vendor Universe Mapping:**

| Tier | Description | Example Criteria | Typical Count |
|---|---|---|---|
| **Leaders** | Established, broad capability, large customer base | Gartner MQ leaders, >$1B revenue | 3-5 |
| **Challengers** | Strong product, growing market share | Strong product reviews, fast growth | 3-5 |
| **Niche Players** | Specialized by industry, size, or function | Deep domain fit, innovative features | 5-10 |
| **Emerging** | New entrants, modern architecture, disruptive pricing | Cloud-native, AI-first, <3 years in market | 3-5 |

**Research Sources:**
- Analyst reports: Gartner Magic Quadrant, Forrester Wave, IDC MarketScape
- Peer reviews: G2, Capterra, TrustRadius (filter for similar company size/industry)
- Industry references: Peer company implementations, conference case studies
- Vendor briefings: Analyst inquiry, vendor-provided materials

### 4. Long List to Short List Reduction

**Stage Gate Process:**

| Stage | Input | Criteria | Output |
|---|---|---|---|
| **Universe** | All known vendors | Market presence in category | 15-25 vendors |
| **Long List** | Universe filtered | Meets P1 requirements (desk research) | 8-12 vendors |
| **RFI Response** | Long list vendors | Detailed capability match, pricing range | 5-8 vendors |
| **Short List** | RFI respondents | Weighted scoring threshold (>70%) | 3-5 vendors |
| **Final Demo** | Short list vendors | Full evaluation with stakeholders | 2-3 vendors |
| **Selection** | Finalists | Final scoring, negotiation, reference checks | 1 vendor |

**Long List Elimination Criteria (any = disqualify):**
- Does not meet any P1 requirement
- No presence in target geography/market
- Company size mismatch (too small = risk, too large = priority risk)
- No relevant industry references
- Technology architecture fundamentally incompatible
- Pricing model misaligned with budget range

### 5. RFP/RFI Template Structure

**RFP Document Outline:**

| Section | Content | Page Guidance |
|---|---|---|
| 1. Company Overview | About the buying organization, strategic context | 1-2 pages |
| 2. Project Scope | System scope, users, geographies, timeline | 2-3 pages |
| 3. Current State | Existing systems, integrations, pain points | 1-2 pages |
| 4. Requirements | Functional, technical, integration, non-functional (reference matrix) | 10-20 pages |
| 5. Vendor Information | Company background, financials, references, roadmap | 2-3 pages |
| 6. Implementation Approach | Methodology, team, timeline, change management | 3-5 pages |
| 7. Pricing | License/subscription, implementation, ongoing costs (use TCO template) | 2-3 pages |
| 8. Security & Compliance | Certifications, data handling, audit reports | 2-3 pages |
| 9. SLA & Support | Uptime SLA, support tiers, escalation, maintenance windows | 1-2 pages |
| 10. Evaluation Criteria | Scoring methodology (transparent to vendors) | 1 page |
| 11. Response Instructions | Format, deadline, Q&A process, contact | 1 page |

**RFP Requirements Response Format:**

| Req ID | Requirement | Priority | Response Options |
|---|---|---|---|
| FR-001 | [Description] | P1 | Fully Supported / Supported with Configuration / Supported with Customization / Roadmap (date) / Not Supported |

### 6. Weighted Scoring Framework

**Scoring Category Weights (adjustable by stakeholder priorities):**

| Category | Default Weight | Range | Key Stakeholder |
|---|---|---|---|
| **Functional Fit** | 30% | 25-40% | Business owners, end users |
| **Technical Fit** | 20% | 15-25% | IT/Engineering |
| **Vendor Viability** | 15% | 10-20% | Procurement, executive sponsor |
| **Cost (TCO)** | 15% | 10-20% | Finance, procurement |
| **Implementation Risk** | 10% | 5-15% | PMO, IT |
| **Innovation & Roadmap** | 10% | 5-15% | CTO/CIO, product |
| **Total** | **100%** | | |

**Detailed Scoring Rubric (apply consistently across all vendors):**

| Score | Label | Definition |
|---|---|---|
| 5 | **Exceptional** | Exceeds requirement; best-in-class capability demonstrated |
| 4 | **Strong** | Fully meets requirement with proven capability |
| 3 | **Adequate** | Meets requirement with minor gaps or workarounds |
| 2 | **Partial** | Partially meets requirement; significant customization needed |
| 1 | **Weak** | Barely addresses requirement; major gaps |
| 0 | **Fail** | Does not meet requirement (eliminatory for P1 items) |

**Scoring Matrix Template:**

| Category | Sub-Criteria | Weight | Vendor A | Vendor B | Vendor C |
|---|---|---|---|---|---|
| **Functional Fit (30%)** | | | | | |
| | Core functionality coverage | 10% | | | |
| | Workflow/process alignment | 8% | | | |
| | Reporting & analytics | 6% | | | |
| | User experience | 6% | | | |
| **Technical Fit (20%)** | | | | | |
| | Architecture & scalability | 6% | | | |
| | Security & compliance | 6% | | | |
| | Integration capabilities | 5% | | | |
| | Performance | 3% | | | |
| **Vendor Viability (15%)** | | | | | |
| | Financial stability | 5% | | | |
| | Market position & trajectory | 4% | | | |
| | Customer references | 3% | | | |
| | Partner ecosystem | 3% | | | |
| **Cost / TCO (15%)** | | | | | |
| | 5-year TCO | 10% | | | |
| | Pricing model flexibility | 5% | | | |
| **Implementation Risk (10%)** | | | | | |
| | Implementation complexity | 4% | | | |
| | Vendor implementation capability | 3% | | | |
| | Data migration risk | 3% | | | |
| **Innovation (10%)** | | | | | |
| | Product roadmap alignment | 5% | | | |
| | AI/automation capabilities | 3% | | | |
| | Technology modernity | 2% | | | |
| **TOTAL** | | **100%** | **/5.0** | **/5.0** | **/5.0** |

### 7. Vendor Demo Evaluation Scorecard

**Demo Structure (require from all vendors):**

| Segment | Duration | Content | Evaluators |
|---|---|---|---|
| Company & vision | 15 min | Vendor strategy, roadmap, relevant experience | Executive sponsor |
| Core scenario 1 | 30 min | Primary business workflow (scripted) | Business users |
| Core scenario 2 | 30 min | Secondary business workflow (scripted) | Business users |
| Integration demo | 15 min | Live integration with key systems | IT/Engineering |
| Administration | 15 min | Configuration, security, user management | IT/Engineering |
| Q&A | 15 min | Open questions from evaluation team | All |

**Demo Evaluation Form (per evaluator):**

| Criteria | Weight | Score (1-5) | Notes |
|---|---|---|---|
| Scenario completion (did it work?) | 25% | | |
| Ease of use / UX quality | 20% | | |
| Data handling and reporting | 15% | | |
| Configurability (no custom code) | 15% | | |
| Integration capability demonstrated | 10% | | |
| Presenter knowledge and credibility | 10% | | |
| Innovation / "wow factor" | 5% | | |
| **Weighted Score** | **100%** | **/5.0** | |

### 8. Reference Check Methodology

**Reference Selection Rules:**
- Require 3-5 references per short-listed vendor
- At least 1 reference in same industry
- At least 1 reference of similar company size
- At least 1 reference that went live within last 18 months
- Request references the vendor did NOT pre-select (ask for full customer list)

**Reference Check Question Bank:**

| Category | Questions |
|---|---|
| **Implementation** | How long did implementation take vs. plan? What was the biggest surprise? Would you use the same implementation partner again? |
| **Functionality** | What works well? What are the top 3 gaps or workarounds? How does reporting meet your needs? |
| **Performance** | Any performance issues at scale? Uptime experience vs. SLA? |
| **Support** | How responsive is vendor support? How are bugs and enhancement requests handled? |
| **Cost** | Did total cost match proposal? Any unexpected costs? How have renewal negotiations gone? |
| **Integration** | How well does the system integrate? API quality and documentation? |
| **Satisfaction** | Net Promoter Score (0-10)? Would you choose this vendor again? What would you do differently? |

### 9. Total Cost of Ownership (TCO) Model

**5-Year TCO Template:**

| Cost Category | Year 0 (Impl) | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | Total |
|---|---|---|---|---|---|---|---|
| **Software Costs** | | | | | | | |
| License / subscription fees | | | | | | | |
| User licenses (per seat) | | | | | | | |
| Module / add-on fees | | | | | | | |
| API / integration fees | | | | | | | |
| Storage / compute overage | | | | | | | |
| **Implementation Costs** | | | | | | | |
| Vendor professional services | | | | | | | |
| SI / implementation partner | | | | | | | |
| Data migration | | | | | | | |
| Custom development | | | | | | | |
| Testing and QA | | | | | | | |
| **Internal Costs** | | | | | | | |
| Internal project team (FTE x months) | | | | | | | |
| Business user time (training, UAT) | | | | | | | |
| IT support team allocation | | | | | | | |
| **Change Management** | | | | | | | |
| Training development and delivery | | | | | | | |
| Change management program | | | | | | | |
| Productivity loss during transition | | | | | | | |
| **Ongoing Costs** | | | | | | | |
| Annual maintenance / support | | | | | | | |
| Managed services / admin | | | | | | | |
| Enhancements / releases | | | | | | | |
| Infrastructure (if on-prem) | | | | | | | |
| **Risk Contingency (10-20%)** | | | | | | | |
| **TOTAL** | | | | | | | **$[X]** |

**TCO Comparison Normalization:**
- Convert all pricing to same term (monthly/annual)
- Normalize user counts to same projected growth
- Include contractual escalators (annual price increases)
- NPV calculation at company's discount rate for multi-year comparison

```
NPV of TCO = Sum of (Annual Cost_t / (1 + discount_rate)^t) for t = 0 to 5
Cost per User per Month = 5-Year TCO / (Average User Count x 60 months)
```

### 10. Implementation Risk Assessment

**Risk Assessment per Vendor:**

| Risk Factor | Weight | Assessment Criteria | Vendor A | Vendor B | Vendor C |
|---|---|---|---|---|---|
| Implementation complexity | 20% | # of integrations, data migration volume, customizations | | | |
| Vendor implementation track record | 20% | On-time %, reference satisfaction, methodology maturity | | | |
| Data migration risk | 15% | Data volume, quality, mapping complexity, downtime tolerance | | | |
| Organizational readiness | 15% | Change magnitude, executive support, user buy-in | | | |
| Integration risk | 15% | API maturity, middleware needs, real-time requirements | | | |
| Timeline feasibility | 15% | Vendor capacity, internal resource availability, dependencies | | | |
| **Weighted Risk Score** | **100%** | Lower = less risky | **/5.0** | **/5.0** | **/5.0** |

### 11. Contract Negotiation Key Terms

**Critical Contract Terms Checklist:**

| Term | What to Negotiate | Acceptable / Watch Out |
|---|---|---|
| **Pricing protections** | Annual increase cap, volume discount tiers, MFN clause | Cap at 3-5%; avoid uncapped CPI adjustments |
| **SLA and penalties** | Uptime guarantee, response times, credit mechanism | 99.9%+ uptime; meaningful credits (5-10% of monthly fee) |
| **Data ownership** | Data portability, export formats, deletion on termination | You own all data; vendor provides full export at no cost |
| **Termination rights** | Convenience termination, cause termination, transition period | 90-day notice; 6-12 month transition assistance |
| **Liability cap** | Vendor liability for data breach, downtime, errors | Minimum 2x annual fees; carve-outs for IP infringement, data breach |
| **Implementation guarantees** | Fixed price or cap, milestone payments, warranty period | Milestone-based payments; 90-day warranty post go-live |
| **IP rights** | Ownership of customizations, configurations, integrations | You own all custom code; vendor retains core product IP |
| **Escrow** | Source code escrow for vendor insolvency | Required for critical systems; annual verification |
| **Compliance** | Audit rights, certification maintenance, breach notification | Annual SOC 2; 24-hour breach notification |
| **Renewal terms** | Auto-renewal notice period, renewal pricing | 90-day opt-out; renewal at current published rates or negotiated cap |

### 12. Decision Presentation Template

**Steering Committee Decision Pack Structure:**

| Section | Content | Slides |
|---|---|---|
| Executive Summary | Recommendation, key rationale, investment required | 1 |
| Process Overview | Methodology, timeline, participants, vendors evaluated | 1 |
| Requirements Summary | Key requirements, prioritization, stakeholder alignment | 1 |
| Vendor Comparison | Scoring summary, strengths/weaknesses, key differentiators | 2-3 |
| TCO Comparison | 5-year cost comparison, NPV, cost per user | 1 |
| Risk Assessment | Implementation risk by vendor, mitigation plans | 1 |
| Reference Insights | Key findings from reference checks | 1 |
| Recommendation | Recommended vendor with top 3 reasons, second choice | 1 |
| Implementation Plan | High-level timeline, resource needs, key milestones | 1 |
| Decision Required | Specific ask, approval needed, next steps | 1 |

## Output Template

```markdown
# System Selection: [System Type] for [Organization]

**Prepared for**: [Steering Committee] | **Date**: [Date] | **Decision Required By**: [Date]

## Executive Summary

**Recommendation**: [Vendor Name]
**Confidence Level**: [High / Medium / Low]

[3-5 sentence summary: why this system is being selected, the recommended vendor,
key differentiators, and total investment required.]

### Selection at a Glance
| Criterion | Vendor A | Vendor B | Vendor C |
|---|---|---|---|
| Weighted Score | X.X/5.0 | X.X/5.0 | X.X/5.0 |
| 5-Year TCO | $[X]M | $[X]M | $[X]M |
| Implementation Risk | Low/Med/High | Low/Med/High | Low/Med/High |
| Go-Live Timeline | X months | X months | X months |

## 1. Requirements Summary
**Total Requirements**: [X] (P1: [X] | P2: [X] | P3: [X] | P4: [X])
[Key requirements highlights]

## 2. Build vs. Buy Decision
**Decision**: [Build / Buy / Configure]
[Scoring summary and rationale]

## 3. Market Landscape
[Vendor universe, long list, and short list progression]

## 4. Detailed Vendor Scoring

### Scoring Summary
| Category (Weight) | Vendor A | Vendor B | Vendor C |
|---|---|---|---|
| Functional Fit (30%) | X.X | X.X | X.X |
| Technical Fit (20%) | X.X | X.X | X.X |
| Vendor Viability (15%) | X.X | X.X | X.X |
| Cost / TCO (15%) | X.X | X.X | X.X |
| Implementation Risk (10%) | X.X | X.X | X.X |
| Innovation (10%) | X.X | X.X | X.X |
| **Weighted Total** | **X.X** | **X.X** | **X.X** |

### Vendor Profiles
**[Vendor A]**: [2-3 sentence summary of strengths and weaknesses]
**[Vendor B]**: [2-3 sentence summary of strengths and weaknesses]
**[Vendor C]**: [2-3 sentence summary of strengths and weaknesses]

## 5. TCO Comparison (5-Year)
| Cost Category | Vendor A | Vendor B | Vendor C |
|---|---|---|---|
| Software | $[X] | $[X] | $[X] |
| Implementation | $[X] | $[X] | $[X] |
| Ongoing (annual) | $[X] | $[X] | $[X] |
| Internal costs | $[X] | $[X] | $[X] |
| **5-Year Total** | **$[X]** | **$[X]** | **$[X]** |
| NPV @ [X]% | $[X] | $[X] | $[X] |
| Cost/user/month | $[X] | $[X] | $[X] |

## 6. Reference Check Summary
| Vendor | NPS (avg) | On-Time Implementation | Top Concern |
|---|---|---|---|
| [Vendor A] | [X]/10 | [X]% | [Concern] |

## 7. Implementation Risk Assessment
[Risk comparison by vendor with mitigation strategies]

## 8. Recommendation and Rationale

**Recommended**: [Vendor Name]
**Second Choice**: [Vendor Name] (if primary negotiation fails)

**Top 3 Reasons:**
1. [Reason with supporting evidence]
2. [Reason with supporting evidence]
3. [Reason with supporting evidence]

**Key Risks of Recommended Vendor:**
1. [Risk with mitigation plan]

## 9. Implementation Plan (High Level)
| Phase | Timeline | Key Activities | Investment |
|---|---|---|---|
| Contract & Kickoff | Weeks 1-4 | Contract signing, project setup, team mobilization | $[X] |
| Design & Configure | Weeks 5-16 | Requirements validation, configuration, integrations | $[X] |
| Test & Train | Weeks 17-24 | UAT, performance testing, training delivery | $[X] |
| Go-Live & Stabilize | Weeks 25-30 | Cutover, hypercare, issue resolution | $[X] |

## 10. Decision Required
- [ ] Approve recommended vendor: [Vendor Name]
- [ ] Approve budget: $[X]M (implementation) + $[X]M/year (ongoing)
- [ ] Authorize contract negotiation to proceed
- [ ] Confirm go-live target: [Date]
```

## Quality Checks

- [ ] Requirements gathered across all four categories (functional, technical, integration, non-functional).
- [ ] Build vs. buy analysis completed before vendor evaluation.
- [ ] All vendors scored using identical weighted criteria with consistent rubric.
- [ ] Category weights validated with stakeholders before scoring begins.
- [ ] At least 3 vendors on final short list for meaningful comparison.
- [ ] Demo evaluation uses scripted scenarios consistent across all vendors.
- [ ] Reference checks completed with at least 3 references per finalist.
- [ ] 5-year TCO model includes all cost categories with consistent assumptions.
- [ ] NPV calculation applied for multi-year cost comparison.
- [ ] Implementation risk assessed per vendor with mitigation strategies.
- [ ] Contract negotiation checklist covers all critical terms.
- [ ] Decision presentation structured for steering committee approval.
- [ ] Scoring methodology is transparent and defensible.
- [ ] All estimates carry confidence levels (High/Medium/Low).
