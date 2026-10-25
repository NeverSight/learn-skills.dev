---
name: requirements-stakeholders
description: "Stakeholder analysis for BAs: build the list, maps (influence matrix, onion), RACI, personas, engagement and communication plans, and stakeholder risks; use at project start or when beginning a round of elicitation to know who to meet, how, and who decides."
---

# Requirements Stakeholders

Based on BABOK v3 section 3.2 (Plan Stakeholder Engagement), 10.43 (Stakeholder List, Map, or Personas) and Agile Extension v2 section 7.7 (Personas). Respond in the user's language. Stakeholder analysis is iterative; a stakeholder's position changes with scope and context (10.43.3).

## Hard rules
1. **Never invent people, roles, attitudes or authority.** Include in the list only people/groups that appear in the documents or in what the user says. Unknown attributes are written "?" with a way to find out (ask whom, which document to look at).
2. **Separate facts from guesses.** Every attribute carries a label: [Stated] (the user/document says so explicitly), [Inferred] (from role, job title, behaviour described), [Assumption]. Judgments about attitude and influence are opinions and are always [Inferred] unless the person themself or someone with authority confirms them.
3. **Political and privacy sensitivity** (BABOK 10.43.4 notes that assessing the influence and interest of each representative can be complex and politically risky). Analysis that includes assessments of individuals (attitude, influence) is for the BA team only; remind the user not to put a version with judgments about individuals into a widely shared document. By default assess by role/group, and do not comment on personality.
4. **Only one Accountable for each item** in the RACI (10.43.3.3). If an item has two A's: ask again, do not split.
5. **Personas must rest on research, not opinion** (10.43.3.4). A persona without research data must be labelled "Hypothesis, not validated" with a list of ways to validate it (interviews, surveys). Do not invent personal details such as age or family to make it feel real.
6. **Everything traces to a source**: the list carries sources (org chart, contract, sponsor, meeting). No source: "needs confirmation".

## Process
1. **Define the scope of the analysis**: which change/initiative, the in/out boundary (use the scope model if there is one).
2. **Build the list** (`references/analysis.md` section 1): look for internal sources (org chart, processes), external sources (contracts, suppliers, regulators, customers), and the standard BABOK roles to catch omissions.
3. **Analyze characteristics**: role, attitude, decision authority, level of influence/interest.
4. **Build the maps**: matrix (influence × interest/impact), onion, RACI for key activities (`references/maps-raci-persona.md`).
5. **Draft the engagement and communication plans** (`references/engagement-plans.md`).
6. **State stakeholder risks**: key people hard to engage, negative attitudes, a gap between the influence needed and the influence held; propose recording them in the risk register; hint to `business-case-strategy` if there is an overall risk assessment.
7. **Return**: list + maps + plans + open questions. If preparing for elicitation, link to `requirements-elicitation` (who to interview, who attends the workshop).

## Modes
- **Create new** from a project description/documents.
- **Update** from meeting notes or an organizational change (edit only the affected parts, keep a change history).
- **Review** an existing version: look for missed groups, missing attributes, RACI with 0 or 2 A's, plans that do not match the map.
- **Persona**: create a persona from user research data the user provides.

## Collaboration
From the list to the elicitation schedule: `requirements-elicitation`. RACI for UAT acceptance: `requirements-testcases`. System-level permission matrix (CRUD): `requirements-modelling`. Risk and change strategy: `business-case-strategy`.

## Reference files
- `references/analysis.md`: list, standard roles, characteristics to analyze, finding sources.
- `references/maps-raci-persona.md`: matrix, onion, RACI, persona.
- `references/engagement-plans.md`: engagement, communication, stakeholder risk.
- `templates/stakeholder-register.md`: register template with example.
