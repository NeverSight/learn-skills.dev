---
name: commercial-discovery
description: >
  Prepare and conduct B2B discovery meetings for technology consulting
  engagements. Generate pre-meeting research briefs, SPIN-based question guides
  adapted for consulting, stakeholder/buying committee mapping, and structured
  discovery notes. Use when preparing for a first discovery call, conducting
  needs analysis for consulting projects, or mapping the decision-making unit
  within a prospect organization.
---

# Commercial Discovery (B2B Consulting Sales)

Purpose
- Enable thorough, structured discovery for B2B consulting sales.
- Unlike SaaS discovery (which demos a product), consulting discovery must
  deeply understand the client's current state, desired future state,
  organizational dynamics, and constraints to later design a custom solution.
- Prepare the seller and capture structured notes.

Key Differentiation from SaaS Discovery
- No product to demo — discovery IS the product sample.
- Must assess organizational readiness, not just feature fit.
- Need to understand current tech stack, team capabilities, and culture.
- Must map multiple stakeholders (not just a single buyer).
- Consulting discovery often spans 2-3 meetings, not one.

Scope
- This skill WILL:
  - Generate pre-meeting research briefs with tailored SPIN questions
  - Map buying committees and stakeholder dynamics
  - Produce structured post-meeting discovery notes
  - Run mini tech-maturity assessments during discovery
  - Update pipeline state with discovery insights

- This skill WILL NOT:
  - Propose solutions (defer to solution-design phase)
  - Generate proposals or SOWs
  - Conduct qualification scoring (see commercial-qualification)

Inputs
- **prospect-profile.md** — from commercial-prospecting
- **commercial-state.md** — pipeline context
- **user_input** — meeting details, known contacts, specific areas to explore

Outputs (contract)

# Output 1: Pre-Meeting Brief (`discovery-prep.md`)

- **Company research summary** — key facts, recent news, strategic context
- **Known pain points and hypotheses** — from prospecting or prior interactions
- **Stakeholder map** — known contacts, roles, likely agenda
- **SPIN question guide** — 15-20 questions tailored to this prospect, organized by S/P/I/N (see `references/discovery-frameworks.md`)
- **Meeting agenda suggestion** — 45-60 min structure
- **Red flags to watch for** — signals this opportunity may not be real
- **Success criteria for the meeting** — what "good" looks like

# Output 2: Post-Meeting Discovery Notes (`discovery-notes.md`)

- **Meeting metadata** — date, attendees, duration
- **Current State summary** — tech stack, processes, team, pain points
- **Desired Future State** — what success looks like for them
- **Gap Analysis** — current → desired, organized by Software / Data / AI
- **Buying Committee Map** — Champion, Economic Buyer, Technical Buyer, Coach, Blocker — with names
- **Budget signals** — explicit mentions, inferred range
- **Timeline signals** — urgency drivers, deadlines, fiscal year
- **Competition signals** — other vendors mentioned, internal alternatives
- **Next steps agreed**
- **Open questions requiring follow-up**

# Output 3: Updated `commercial-state.md`

Update the opportunity with discovery insights: stage, champion, key pain points, next action.

---

SPIN Framework Adapted for Tech Consulting

- **Situation**: Current tech landscape, team structure, processes, recent initiatives
- **Problem**: Pain points, inefficiencies, failed past initiatives, technical debt
- **Implication**: Business impact of not solving (revenue loss, competitive risk, team attrition, compliance risk)
- **Need-payoff**: Value of solving (ROI, speed, capability unlock, market advantage)

For the full SPIN question bank organized by service line (Software, Data, AI) with 10 questions per category, see `references/discovery-frameworks.md`.

Mini Tech Maturity Assessment (during discovery)

- Run a quick 5-question assessment per axis (Software / Data / AI) to validate or update prospecting scores.
- Compare self-reported maturity vs. observed indicators.
- Full questionnaire available in `references/discovery-frameworks.md`.

---

Guardrails (must follow)
1. Discovery is about listening, not pitching — question-to-statement ratio should be 3:1 minimum.
2. Never propose a solution during discovery — note the urge, defer to solution-design phase.
3. Always map at least Champion + Economic Buyer — if you cannot identify both, flag as risk.
4. Capture exact quotes when possible — client's own words are gold for proposals.
5. Never assume budget — probe with indirect questions.
6. If discovery reveals the prospect is not a fit, say so honestly rather than forcing it.
7. Flag when a single discovery meeting is insufficient and recommend follow-up.

---

Example

**Context**: Logistics company (Acme Logistics) exploring data platform modernization. Legacy SQL Server data warehouse, 15-person IT team, $40M revenue.

**Sample SPIN Questions**:

Situation:
- "Walk me through how data currently flows from your TMS and WMS into the SQL Server warehouse."
- "How many people on the team write queries or reports against the warehouse today?"

Problem:
- "What happens when leadership asks for a report that crosses multiple source systems?"
- "How long does it take to onboard a new data source into the warehouse?"

Implication:
- "When route optimization decisions are delayed because data isn't ready, what's the cost per day in fuel and driver hours?"
- "If the warehouse goes down during peak shipping season, what's the operational impact?"

Need-payoff:
- "If your operations team had real-time visibility into shipment status across all carriers, how would that change your customer SLA performance?"
- "What would it mean for the business if you could add a new data source in days instead of months?"
