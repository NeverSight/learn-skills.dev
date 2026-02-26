---
name: commercial-proposal-writer
description: >
  Write comprehensive commercial proposals for B2B technology consulting
  engagements. Integrate solution briefs, ROI/business cases, consulting pricing
  models (T&M, Fixed, Outcome-based, Retainer, Blended), team structure,
  governance, timeline, and terms. Output includes commercial-proposal.md and
  preliminary workplan-and-estimate.md that feeds into the PM suite's
  project-intake-and-charter skill. Use when creating proposals, writing SOWs,
  pricing engagements, or preparing commercial offers. Triggers on: proposal,
  commercial proposal, SOW, pricing, quote, engagement offer, commercial offer,
  statement of work.
---

# Commercial Proposal Writer

## Purpose
- Write compelling, complete commercial proposals for consulting engagements.
- Integrate solution architecture, business case, pricing, and commercial terms into a cohesive document.
- Produce the bridge artifact that connects the commercial pipeline to the PM delivery pipeline.
- Apply the Proposal Pyramid framework (Executive Summary → Solution → Investment → Proof).

## Critical Bridge
The preliminary `workplan-and-estimate.md` produced by this skill is the EXACT input for `project-intake-and-charter` in the PM suite. This is how commercial handoff to delivery works.

## Inputs
- **solution-brief-{slug}.md**: Output from `commercial-solution-design` (required).
- **discovery-notes-{slug}.md**: Output from `commercial-discovery` (for context).
- **qualification-scorecard-{slug}.md**: Output from `commercial-qualification` (validates pursuit decision and branch).
- **prospect-profile-{slug}.md**: Output from `commercial-prospecting` (company/contact context).
- **discovery-proposal-deliverables.md** *(Branch B post-Discovery only)*: When this opportunity follows a completed Discovery engagement, include the Discovery deliverables as context. Reference the Discovery in the proposal — it demonstrates prior investment and reduces client skepticism about scope.
- **commercial-state.md**: Current pipeline state.
- **user_input**: Pricing parameters, team rates, specific terms, client preferences, competitive context.

**Branch context**: Check the opportunity `branch` in `commercial-state.md`:
- **Branch A**: Standard implementation proposal. No prior Discovery. Estimation carries +/- 30% caveat if relevant.
- **Branch B (post-Discovery)**: Implementation proposal following a completed Discovery engagement. The proposal should reference the Discovery outputs as the basis for scope and estimation. Estimation carries +/- 20% confidence. Optionally include a brief "What the Discovery Revealed" section to reinforce the value of the prior investment and justify the proposed approach.

## Proposal Pyramid Framework (CLOSE)

Structure every proposal using the CLOSE framework. See `references/proposal-frameworks.md` for detailed structure, writing guidelines, anti-patterns, and review checklist.

**C — Context**: Demonstrate deep understanding of the client's situation and challenges.
**L — Loss**: Quantify what they lose by NOT acting (cost of inaction).
**O — Outcome**: Paint the picture of the desired future state and its business value.
**S — Solution**: Present the specific approach, phases, and deliverables.
**E — Evidence**: Provide proof through case studies, methodologies, team credentials.

## Win Factor Awareness

Research shows proposal win factors weight as follows:
- 40% Relationship & Trust
- 25% Solution Fit
- 20% Presentation Quality
- 15% Pricing

Invest most effort in demonstrating understanding and trust. The "Understanding Your Situation" and "Executive Summary" sections carry the most weight.

## Pricing Models for Consulting

Select the appropriate model (or combine) based on engagement characteristics. See `references/pricing-models.md` for detailed guidance on each model, rate card structures, discount strategy, ROI templates, objection handling, and margin considerations.

| Model | Best For | Risk Distribution |
|-------|---------|------------------|
| **Time & Materials (T&M)** | Uncertain scope, evolving requirements, advisory | Client bears scope risk |
| **Fixed Price** | Well-defined scope, clear deliverables, short engagements | Consultant bears scope risk |
| **Outcome-Based** | Measurable business outcomes, performance improvement | Shared risk, high reward potential |
| **Retainer** | Ongoing advisory, fractional CTO/architect, continuous support | Predictable for both sides |
| **Blended / Hybrid** | Phased engagements mixing discovery (T&M) + delivery (fixed) | Risk distributed by phase |

## Workflow

1. **Compile Inputs**: Gather solution brief, discovery notes, qualification scorecard.
2. **Determine Pricing Strategy**: Select pricing model(s), calculate total investment, structure payment milestones.
3. **Build Proposal Pyramid**: Structure content following CLOSE framework.
4. **Write Proposal Sections**: Draft each section (see output template below).
5. **Generate Workplan & Estimate**: Create the preliminary WBS + hours + cost document.
6. **Internal Review Checklist**: Verify all sections are complete and consistent.

## Outputs (contract)

### Output 1: `commercial-proposal-{company-slug}.md`

```markdown
# Commercial Proposal: {Opportunity Name}
## {Company Name}

**Prepared by**: {Consulting Firm}
**Date**: YYYY-MM-DD
**Valid until**: YYYY-MM-DD (typically 30 days)
**Version**: 1.0

---

## 1. Executive Summary
[CLOSE framework: Context → Loss → Outcome → Solution → Evidence in condensed form. Max 1 page / 400 words. This section must stand alone — a busy executive should understand the entire proposal from this section.]

## 2. Understanding Your Situation (Context)
### Current State
[Demonstrate deep understanding of the client's situation — drawn from discovery notes]
### Challenges
[Specific pain points, quantified where possible]
### Cost of Inaction
[What happens if they don't address these challenges — the "Loss" element]

## 3. Proposed Approach (Solution)
### Solution Overview
[High-level approach, drawn from solution brief]
### Delivery Phases

#### Phase 0: {Name} — {Duration}
- **Objective**: 
- **Key Activities**:
  - Activity 1
  - Activity 2
- **Deliverables**:
  - Deliverable 1
  - Deliverable 2
- **Success Criteria**:
  - Criterion 1

[Repeat for each phase]

### Methodology
[Brief description of how the team works: Agile, iterative, regular demos, weekly syncs, etc.]

## 4. Expected Outcomes (Outcome)
- Outcome 1: [quantified business value]
- Outcome 2: [quantified business value]
- Outcome 3: [quantified business value]

### ROI Projection
[If quantifiable: estimated ROI calculation. If not: qualitative value statement]

## 5. Team & Governance
### Proposed Team

| Role | Name (if known) | Allocation | Rate Category |
|------|----------------|-----------|--------------|
| | | | |

### Governance Model
- **Steering Committee**: [frequency, attendees]
- **Progress Reports**: [frequency, format]
- **Escalation Path**: [how issues are escalated]
- **Change Management**: [how scope changes are handled]

## 6. Investment

### Pricing Model: {T&M / Fixed / Outcome-Based / Retainer / Blended}

### Fee Summary

| Phase | Hours | Rate | Amount |
|-------|-------|------|--------|
| | | | |
| **Subtotal** | | | |
| Discount (if any) | | | |
| **Net Total** | | | **$XXX** |

### Payment Schedule

| Milestone | Trigger | Amount | Due Date |
|-----------|---------|--------|----------|
| | | | |

### What's Included
- Item 1
- Item 2

### What's Not Included
- Item 1
- Item 2

## 7. Why Us (Evidence)
### Relevant Experience
[1-2 brief case studies or project summaries showing similar work]
### Methodology & Quality
[Key differentiators: approach, tools, certifications]
### Client References
[Available upon request, or list if permitted]

## 8. Terms & Conditions
### Engagement Terms
- **Start Date**: Proposed YYYY-MM-DD (subject to SOW execution)
- **Duration**: X months
- **Location**: Remote / On-site / Hybrid
- **Travel & Expenses**: [included / billed at cost / not applicable]

### Key Terms
- Intellectual property: [work product ownership]
- Confidentiality: [mutual NDA reference]
- Termination: [notice period, typically 30 days]
- Change requests: [process for scope changes]

## 9. Next Steps
1. Review proposal and provide feedback by YYYY-MM-DD
2. Schedule proposal walkthrough meeting
3. Finalize SOW and commercial terms
4. Target engagement start: YYYY-MM-DD

---

**Contact**: {Name}, {Title}, {Email}, {Phone}
```

### Output 2: `workplan-and-estimate-{company-slug}.md`

Follow the format from the existing PM suite's workplan template:

```markdown
# Workplan and Estimate — {Project Name}

PM: {Name}
Date: YYYY-MM-DD
Summary: {Brief summary of scope and objective}

## WBS / Activity Details
- 1. {Activity} — Hours: X — Rate: $X — Subtotal: $X
- 2. {Activity} — Hours: X — Rate: $X — Subtotal: $X
[continue for all WBS items]

Total hours: X
Hourly rate / Blended rate: $X
Subtotal: $X
Discount: X% (-$X)
Net before VAT: $X
VAT (if applicable): $X
Total: $X

## Approval Required
- Owners: {names}
- Deadline: 48 business hours from submission

Suggested decision-log entry:
| D-XX | YYYY-MM-DD | Workplan and Estimate Approval | Approver: {name} |
```

This workplan-and-estimate IS the input artifact for `project-intake-and-charter` in the PM suite, creating the bridge between commercial and delivery.

**Updated**: `commercial-state.md` — Move opportunity to `proposal` stage, update `value`, `probability`, `next_action`.

## Guardrails
1. **Never send a proposal without prior discovery** — proposals built on assumptions lose.
2. **Proposal must tell a story**: CLOSE framework must flow naturally, not feel like a checklist.
3. **Never include rates or pricing without user validation** — always ask for confirmation of rate cards.
4. **Investment section must be crystal clear** — no ambiguity about what's included and excluded.
5. **Always include a "What's Not Included" section** — prevent scope disputes from day one.
6. **Workplan must be consistent with proposal** — hours, phases, and amounts must match exactly.
7. **Validity period is mandatory** — proposals expire (default 30 days).
8. **Terms are commercial, not legal** — always flag that legal review is recommended for actual contracts.
9. **Never badmouth competitors** — differentiate positively.
10. **Proposals must be self-contained** — readable without external context.
11. **Win factors awareness**: 40% relationship, 25% solution fit, 20% presentation quality, 15% pricing. Write accordingly.
12. **Anti-patterns to avoid**: Feature-dumping without connecting to pain, burying the price, vague scope, no clear next steps, no exec summary.

## Example: Executive Summary using CLOSE Framework

**Scenario**: Data Platform Modernization proposal for Acme Corp.

> ## Executive Summary
>
> **Acme Corp** has built a strong analytics culture over the past five years, but the on-premise data warehouse that powers your reporting is reaching capacity limits — query times have tripled in the past 12 months, and the data engineering team spends 60% of its time on maintenance rather than new insights. *(Context)*
>
> Without intervention, this trajectory means: $2.4M/year in analyst idle time, 3-month delays for new data products, and growing risk of a production outage that could blind executive decision-making for days. *(Loss)*
>
> The target state is a cloud-native data platform that delivers sub-second query performance, self-service analytics for 200+ business users, and 80% reduction in maintenance overhead — freeing the data team to focus on strategic initiatives. *(Outcome)*
>
> We propose a 4-phase modernization program over 6 months: Assessment & Design (4 weeks), Core Platform Build (8 weeks), Migration & Integration (8 weeks), and Optimization & Enablement (4 weeks). Our approach prioritizes zero-downtime migration and parallel running to eliminate business risk. *(Solution)*
>
> Our team has delivered 12 similar migrations in the past 3 years, including a $3M program for a Fortune 500 retailer that achieved 94% query performance improvement and full ROI within 9 months. *(Evidence)*

## Example Scenario
**Input**: Solution brief for Acme Corp (architecture modernization, L-size, 850h, $150/hr blended, 4-person team). User says: "Use T&M for Phase 0 and Fixed for Phases 1-4. Offer 5% discount for full program commitment."

**Output**: Complete commercial proposal with CLOSE-structured narrative + workplan-and-estimate showing:
- Phase 0: T&M, 120h × $150 = $18,000
- Phases 1-4: Fixed at $110,250 (730h × $150 = $109,500, rounded)
- Total: $127,500 - 5% discount = $121,125
- Payment: 30% on SOW, 30% at Phase 2 start, 30% at Phase 3 complete, 10% on final delivery
