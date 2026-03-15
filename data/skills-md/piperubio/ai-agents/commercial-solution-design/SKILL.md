---
name: commercial-solution-design
description: >
  Translate discovered client pain points into high-level technology solution
  architectures for consulting engagements in Software Engineering, Data Platforms,
  and AI/ML. Produce solution briefs with phased roadmaps, effort estimations,
  team composition, and technology recommendations. Use when designing a pre-sale
  technical solution, creating a solution brief for a proposal, or when a prospect
  needs to understand what the engagement would look like before committing. This
  is the preventa técnica / solution engineering step.
---

# Commercial Solution Design

## Purpose

Bridge the gap between discovery (understanding the problem) and proposal (presenting the offer). Create a credible, high-level solution architecture that demonstrates technical competence and gives the prospect confidence that we understand their problem AND know how to solve it.

This is NOT a detailed project plan — it is a pre-sale solution sketch at the right level of detail to win trust and inform pricing.

## Key Distinction

- This is a **PRE-SALE** artifact, not a project plan.
- Level of detail: enough to be credible and priceable, not enough to execute.
- The detailed project plan comes AFTER the deal closes, via `project-planning` skill.
- Think of this as the "lite version" of `project-intake-and-charter` + `project-planning`, designed to win the deal.

## Scope

- This skill WILL:
  - Map discovered pain points to consulting service categories and solution patterns
  - Design a high-level solution architecture with technology recommendations
  - Define a phased delivery roadmap with effort ranges per phase
  - Specify team composition and seniority mix
  - Identify risks, dependencies, assumptions, and success criteria
  - Recommend an engagement model (T&M / Fixed-Price / Outcome-Based / Hybrid)
  - Produce a `solution-brief.md` per opportunity

- This skill WILL NOT:
  - Produce detailed technical designs or implementation specs
  - Create detailed project plans, WBS, or schedules (that is `project-planning`)
  - Make pricing decisions (that is `commercial-proposal-writer`)
  - Execute technical work

## Inputs

- **`discovery-notes.md`** — from `commercial-discovery` (primary source of pain points and context)
- **`qualification-scorecard.md`** — from `commercial-qualification` (validates opportunity quality, fit, and branch)
- **`discovery-proposal-deliverables.md`** *(Branch B only)* — outputs from a completed Strategic Discovery engagement. When present, this is the PRIMARY input and overrides discovery-notes as the source of truth for architecture, risks, and estimation. Estimation accuracy improves to +/- 20% or better.
- **`commercial-state.md`** — current pipeline context
- **`user_input`** — technical constraints, preferences, capacity, or additional context

**Branch context note**: When the qualification scorecard shows `branch: B` and a linked Discovery opportunity is `closed_won`, the solution-design is for the **implementation opportunity** following the Discovery. In this case, estimation carries lower uncertainty — target +/- 20% instead of the standard +/- 30%, and Phase 0 (Assessment) may be shortened or skipped if Discovery already covered it.

## Solution Design Principles

1. Start with business outcomes, map backward to technical requirements.
2. Phase 0 (Assessment/Quick Wins) is mandatory — it reduces risk for both sides and demonstrates value early.
3. Prefer proven technologies over cutting-edge unless the client specifically needs innovation.
4. Always include knowledge transfer — consulting should make the client MORE capable, not dependent.
5. Right-size the team — resist the urge to over-staff for revenue; a lean, senior team builds more trust.
6. Make assumptions explicit — every uncertain element must be stated as an assumption, not a fact.

## Workflow

### 1. Analyze Inputs

Review discovery notes, qualification scorecard, and pipeline context. Identify:
- Primary pain points and their business impact
- Client's technical maturity level
- Constraints (timeline, budget, team, compliance)
- Decision criteria and stakeholder concerns

### 2. Map Pain Points to Solution Patterns

For each pain point from discovery, identify the applicable consulting solution pattern. Consult `references/solution-patterns.md` for common patterns across Software Engineering, Data Platforms, and AI/ML domains. Each pattern includes typical phases, team composition, risks, and engagement model guidance.

### 3. Design Solution Architecture

For each solution component, document:
- **Current State**: where the prospect is today (from discovery)
- **Target State**: where they need to be (derived from pain + objectives)
- **Key Components**: major architectural elements (described in text/ASCII, not visual)
- **Technology Recommendations**: suggested stack with rationale (not vendor-locked unless required)
- **Integration Points**: connections to existing client systems
- **Risks & Assumptions**: technical risks specific to this component

### 4. Define Phased Roadmap

Structure delivery in consulting-appropriate phases:

- **Phase 0 — Assessment / Quick Wins (2-4 weeks)**: Mandatory. Detailed technical discovery, stakeholder interviews, current state documentation, quick wins to demonstrate value. Clear deliverable: assessment report + detailed recommendation.
- **Phase 1 — Foundation / MVP (duration varies)**: Core infrastructure or architecture setup, visible early wins, working foundation.
- **Phase 2 — Build-out / Scale (duration varies)**: Main solution delivery, iterative development with regular demos.
- **Phase 3 — Optimization / Handoff (duration varies)**: Performance optimization, documentation, team training, transition to internal team or support model.

Each phase must include: objectives, key deliverables, dependencies, and estimated effort (person-weeks range).

Every phase must have a clear "done" criteria that could serve as a natural exit point.

Not all phases apply to every engagement. Adjust based on scope and complexity.

### 5. Specify Team Composition

Define the consulting team:
- Roles needed (Tech Lead, Sr. Engineer, Data Engineer, ML Engineer, PM, etc.)
- Seniority mix (% senior vs. mid vs. junior)
- Client-side resources needed (data access owners, subject matter experts, decision-makers)
- Knowledge transfer plan (how the client team ramps up)

### 6. Estimate Effort

Produce preliminary estimates as ranges using the three-point method:
- **Per phase**: person-weeks expressed as optimistic-realistic-pessimistic range
- **Total engagement**: aggregate range
- **Key assumptions**: factors that drive the estimate up or down

Consult `references/estimation-guide.md` for benchmarks by service type and estimation methodology.

**Estimation accuracy by context**:
- Standard (discovery notes only): estimates carry +/- 30% accuracy. Communicate this explicitly.
- Post-Discovery (Branch B, Discovery deliverables available): estimates carry +/- 20% accuracy. Note that a completed Discovery is the source of the improved confidence.

### 7. Assess Risks & Dependencies

Identify:
- Technical risks specific to this solution
- Client dependencies (data access, environments, stakeholder availability)
- Assumptions that could change the scope
- Capability gaps requiring partnering or subcontracting

### 8. Recommend Engagement Model

Select and justify: T&M / Fixed-Price / Outcome-Based / Hybrid.

General guidance:
- **T&M**: when scope is exploratory or likely to evolve
- **Fixed-Price**: when scope is well-defined and bounded
- **Outcome-Based**: when measurable business KPIs can be tied to delivery
- **Hybrid**: Phase 0 T&M + subsequent phases fixed or outcome-based

## Outputs (Contract)

### Output 1: `solution-brief.md`

Per opportunity. Structure:

```markdown
# Solution Brief: {Company Name} — {Opportunity Name}

## Executive Summary
[2-3 paragraphs, business-language, no jargon. State the problem, proposed approach,
expected outcomes, and engagement scope.]

## Current State Assessment
[From discovery, structured as problems + impacts]

| # | Problem | Business Impact | Priority |
|---|---------|----------------|----------|
| 1 |         |                | High/Med/Low |

## Proposed Solution Architecture

### Architecture Overview
[High-level architecture described in text/ASCII — components, data flows, integrations]

### Technology Recommendations
| Component | Recommended Technology | Rationale |
|-----------|----------------------|-----------|
|           |                      |           |

### Integration Points
- [Integration with existing client system 1]
- [Integration with existing client system 2]

## Phased Roadmap

### Phase 0: Assessment / Quick Wins (X weeks)
- **Objectives**: [what this phase achieves]
- **Key Deliverables**: [tangible outputs]
- **Dependencies**: [what must be true or available]
- **Estimated Effort**: X-Y person-weeks (optimistic-realistic-pessimistic)
- **Done Criteria**: [clear exit point]

### Phase 1: Foundation / MVP (X weeks)
[same structure]

### Phase 2: Build-out / Scale (X weeks)
[same structure]

### Phase 3: Optimization / Handoff (X weeks)
[same structure]

## Team Composition

| Role | Seniority | Allocation | Phases | Responsibilities |
|------|-----------|-----------|--------|-----------------|
|      |           |           |        |                 |

**Seniority Mix**: X% Senior / Y% Mid / Z% Junior
**Client-Side Resources Needed**: [roles, availability]
**Knowledge Transfer Plan**: [approach]

## Preliminary Effort Estimation

| Phase | Duration | Effort (person-weeks) | Confidence |
|-------|----------|----------------------|------------|
| Phase 0 | X weeks | O / R / P | Medium |
| Phase 1 | X weeks | O / R / P | Low |
| Phase 2 | X weeks | O / R / P | Low |
| Phase 3 | X weeks | O / R / P | Low |
| **Total** | **X weeks** | **O / R / P** | |

**Key Assumptions Driving the Estimate**:
1. [Assumption 1]
2. [Assumption 2]

## Risks & Dependencies

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
|      |            |        |            |

### Client Dependencies
- [Data access / environments / stakeholder availability]

### Scope-Changing Assumptions
- [Assumptions that, if wrong, materially change the engagement]

## Success Criteria
[Measurable, tied back to discovery pain points]
- Criterion 1
- Criterion 2

## Recommended Engagement Model
[T&M / Fixed-Price / Outcome-Based / Hybrid — with rationale]

---
*Pre-sale artifact — subject to detailed discovery post-engagement. Estimates ±30%.*
```

### Output 2: Updated `commercial-state.md`

Move opportunity to `solution` stage. Update with:
- Reference to the solution brief
- Estimated engagement value based on effort sizing
- Next action: review solution brief with prospect

## Guardrails

1. Never present as a final design — clearly label as "pre-sale, subject to detailed discovery post-engagement."
2. Effort estimates must be ranges (±30% is acceptable at this stage), never point estimates.
3. Technology recommendations must include rationale, not just preference.
4. Always identify what the CLIENT must provide (data, access, people, decisions).
5. If the solution requires capabilities outside our expertise, flag it and suggest partnering/subcontracting.
6. Do not over-engineer — match solution complexity to client maturity level.
7. Every phase must have a clear "done" criteria that could serve as a natural exit point.

## Example

**Scenario**: MedTech Corp, mid-size healthcare company. Discovery revealed: legacy SQL Server data warehouse (10+ years old) struggling with performance, no self-service analytics, reports take days to produce manually, data quality issues causing compliance risk. Qualification score: 4.2/5 — Pursue.

**Solution Brief Executive Summary** (excerpt):

> MedTech Corp's reporting infrastructure, built on a legacy SQL Server data warehouse over a decade ago, no longer meets the organization's growing analytics and compliance needs. Manual report generation consumes significant analyst time, data quality gaps create compliance exposure, and the current architecture cannot scale to support self-service analytics demanded by business units.
>
> We propose a phased data platform modernization engagement that migrates MedTech's analytical workloads to a cloud-based data platform with a modern analytics layer. The approach prioritizes quick wins in data quality and automated reporting (Phase 0-1) before tackling the full platform migration (Phase 2), ensuring early value delivery while managing risk.
>
> The engagement spans approximately 20-28 weeks with a team of 3-4 consultants, producing a modern, governed data platform with self-service analytics capabilities and a fully enabled internal team.

**Phase 0: Assessment / Quick Wins** (excerpt):

> - **Objectives**: Validate data landscape, identify critical data quality issues, deliver 2-3 automated reports to replace highest-pain manual processes.
> - **Key Deliverables**: Data landscape assessment report, data quality audit, 2-3 automated reports, detailed Phase 1-3 plan.
> - **Dependencies**: Access to SQL Server environment, availability of lead data analyst for interviews, sample compliance reporting requirements.
> - **Estimated Effort**: 2-3 person-weeks (optimistic: 2 / realistic: 2.5 / pessimistic: 3).
> - **Done Criteria**: Assessment report delivered and reviewed, automated reports operational, Phase 1 plan approved.
