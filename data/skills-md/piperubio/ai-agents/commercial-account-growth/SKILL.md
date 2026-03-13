---
name: commercial-account-growth
description: >
  Manage account expansion for existing consulting clients through upselling
  (next phases, deeper engagements), cross-selling (new service lines —
  Software↔Data↔AI), and client advocacy (case studies, referrals). Analyze
  active and completed projects to identify growth signals and generate
  expansion proposals. Use when reviewing existing accounts for growth
  opportunities, when a project is completing and a follow-on engagement is
  possible, or when creating case studies from successful deliveries. Connects
  project-closure-and-learning output back into the commercial cycle.
---

# Commercial Account Growth

## Purpose

Maximize lifetime value of consulting client relationships by systematically
identifying and pursuing expansion opportunities. This skill closes the loop
between delivery (PM suite) and sales (Commercial suite), ensuring successful
projects naturally lead to more engagements.

## Key Insight — The Land & Expand Model for Consulting

- **Land**: Win an initial engagement (often Phase 0 assessment or a single workstream).
- **Expand**: Grow within the account through adjacent workstreams, new service lines, or deeper engagements.
- **Advocate**: Turn happy clients into references, case studies, and referral sources.
- The cost of expanding within an existing account is **5–7× lower** than acquiring a new client.

## Inputs

- `commercial-state.md` — pipeline and account intelligence.
- Project delivery artifacts (from PM suite): `project-state.md`, `lessons-learned.md`, `closure-report.md`.
- `user_input` — account context, relationship status, strategic goals.
- Optional: client satisfaction data, NPS feedback.

## Outputs (Contract)

### 1. `account-growth-plan.md` — Per Account

Generate a structured Markdown document with the following sections:

#### Account Health Assessment
- **Delivery satisfaction**: Based on project outcomes, lessons learned.
- **Relationship strength**: Champion engagement, exec access, trust level.
- **Revenue trajectory**: Current, historical, potential.
- **Strategic alignment**: Does this account align with our growth strategy?

#### Expansion Signals Detected
Scan project delivery data for:
- **Upsell signals**: Client asking for more scope, next phases mentioned, new pain discovered during delivery.
- **Cross-sell signals**: Adjacent needs identified (e.g., delivered Software, they need Data next).
- **Advocacy signals**: Client expressing satisfaction, willing to be referenced, internal champion promoting us.
- **Risk signals**: Champion leaving, budget cuts, competitor entering, delivery issues.

#### Expansion Opportunities (Prioritized)
For each opportunity include: description, service line, estimated value, probability, effort to pursue, recommended approach. Separate quick wins from strategic plays.

#### Recommended Actions (Next 90 Days)
- **Relationship actions**: Exec alignment, QBR, dinner, etc.
- **Technical actions**: Assessment of new area, POC, workshop.
- **Commercial actions**: Proposal for next phase, cross-sell pitch.

#### Account Revenue Projection
Current year, next 12 months, 3-year potential. Label all figures as estimates.

### 2. `case-study.md` — When Requested or Supported by Closure Data

Follow the STAR framework:
- **Situation**: Client context and challenge (anonymizable).
- **Task**: What we were engaged to do.
- **Action**: How we approached it (methodology, team, approach).
- **Result**: Quantified outcomes (metrics, improvements, ROI).

Include: client quote (if available), timeline, team size, technologies used.
Produce two versions: detailed (for sales use) and summary (for website/marketing).

### 3. Updated `commercial-state.md`

Enrich account intelligence and add new opportunities to pipeline.

## Expansion Signal Detection Framework

### During Active Projects
- "Can you also help with…" → immediate upsell opportunity.
- New stakeholders engaging → wider organizational interest.
- Client team struggling with adjacent area → cross-sell opportunity.
- Positive project reviews → advocacy opportunity.

### At Project Closure
- Lessons learned mention future needs → next engagement.
- Client requests extended support → retainer opportunity.
- High satisfaction scores → case study and referral opportunity.

### Between Engagements
- Industry changes affecting client → proactive outreach with insight.
- New leadership at client → re-engagement opportunity.
- Client mentioned in news (funding, M&A, expansion) → trigger event.

## Guardrails

1. Never push expansion on an unhappy client — fix delivery issues first.
2. Account growth must be genuinely in the client's interest, not just ours.
3. Case studies must be approved by the client before any external use.
4. Do not propose expansion if current project is at risk — focus on delivery.
5. Cross-sell must be supported by genuine capability, not aspiration.
6. Revenue projections must be clearly labeled as estimates, not commitments.
7. Relationship actions must respect the client's time and boundaries.
8. Always check for non-compete or exclusivity clauses before cross-selling.

## Example

**Scenario**: A 6-month data platform project is completing. During delivery the client's analytics lead mentioned: "We've got all this data now but nobody knows how to build ML models on it."

**Expansion signals detected**:
- **Cross-sell** (Data → AI): Client expressed need for ML capabilities adjacent to delivered data platform.
- **Upsell**: Potential Phase 2 for data platform enhancements (data quality, new sources).
- **Advocacy**: Project delivered on time, client sponsor praised the team in the retrospective.

**Recommended actions**:
1. Schedule a 1-hour ML readiness workshop (technical action — low effort, high signal).
2. Draft a Phase 2 proposal for data platform enhancements (commercial action).
3. Request a client quote for a case study on the data platform delivery (advocacy action).
4. Propose a QBR with the client CTO to discuss data & AI roadmap alignment (relationship action).

**Projected value**: Current engagement $400K → Phase 2 $200K + ML engagement $350K → 12-month potential $950K.

## Resources

### references/

- **`expansion-playbooks.md`**: Detailed playbooks for upselling, cross-selling, advocacy, QBRs, account planning, churn prevention, and revenue metrics. Read when executing any specific expansion activity.
