---
name: technical-program-management
description: >-
  Manage technical programs made of multiple related projects, products, teams, or
  vendors: establish the program mandate and benefits, align component work, manage
  cross-project dependencies and shared capacity, govern risks and decisions,
  coordinate transformation and adoption, and communicate program health to executives,
  delivery teams, and partners. Use when the work is a coordinated change larger than
  one project or when component projects are locally green but the combined outcome is
  at risk. Do not use for single-project control, detailed implementation planning,
  product portfolio or capital-allocation decisions, enterprise architecture design,
  release approval, or live incident command; route those to the named specialists.
license: MIT
compatibility: >-
  Platform-agnostic methodology and Markdown templates. No runtime dependency.
metadata:
  tags: technical-program-management, program-governance, benefits-realization,
    dependency-management, transformation, stakeholder-communication
---

# Technical Program Management

Program-level control can fail even when every component is on its own track. Use this skill to see and manage the seams, not to replace project managers or product governance.

## First move: prove the program boundary

A program is not a larger project: it exists because coordination, shared constraints, or benefits across components require decisions that no component owner can make alone.

Read existing strategy, business case, component plans, dependency records, benefits
assumptions, and recent status evidence before creating ceremony. Establish:

- the shared outcome and why the components belong together;
- the senior accountable owner and program decision rights;
- component projects/workstreams, owners, interfaces, and operational recipients;
- expected benefits, benefit owners, measures, baselines, timing, and disbenefits;
- shared capacity, funding, architecture, vendors, environments, and policy constraints;
- the current phase, critical decision, evidence gaps, and stop/revisit conditions.

If the work is one bounded project, route to [technical-project-management](../technical-project-management/SKILL.md).
If the work is only a collection of unrelated investments, route to
[product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md) or
[strategy-frameworks](../strategy-frameworks/SKILL.md).

## Reference routing

Read only what the current decision requires:

| Situation | Read |
|---|---|
| Program mandate, component map, or shared constraints | [Program brief template](templates/program-brief.md) |
| Integrated status, dependency, risk, or recovery problem | [Program control and troubleshooting](references/program-control.md) |
| Benefits, governance, or evidence boundary | [Research ledger](references/research-ledger.md) |
| Benefits dependency mapping, tranche decisions, or disbenefits | [Benefits dependency and tranche control](references/benefits-dependency-and-tranches.md) |
| Adoption, operating-model change, or benefit drift | [Benefits and transformation](references/benefits-and-transformation.md) |
| Integrated control record needs filling | [Integrated control template](templates/integrated-control.md) |
| Audience-specific status or decision update | [Stakeholder update template](templates/stakeholder-update.md) |
| Independent assurance or troubled-program intervention | [Assurance and intervention](references/assurance-and-intervention.md) |
| One project needs detailed control | [technical-project-management](../technical-project-management/SKILL.md) |
| Product portfolio or capital-allocation choice | [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md) or [strategy-frameworks](../strategy-frameworks/SKILL.md) |

## Routing to adjacent skills

- For a single bounded project's milestones, forecasts, dependencies, recovery, or closure, use [technical-project-management](../technical-project-management/SKILL.md).
- For product roadmap and portfolio sequencing, use [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md).
- For recurring product decision rights and product governance, use [product-operations-and-governance](../product-operations-and-governance/SKILL.md).
- For enterprise target-state architecture or architecture governance, use [enterprise-architecture](../enterprise-architecture/SKILL.md).
- For approved work breakdown and detailed rollout planning, use [implementation-planning](../implementation-planning/SKILL.md).

## Program operating loop

1. **Mandate.** Confirm the outcome, component boundaries, authority, funding horizon,
   success measures, and assumptions. Do not convert a strategic aspiration into an
   approved program without an accountable sponsor.
2. **Shape the architecture of work.** Define component charters, interfaces, shared
   milestones, integration evidence, decision rights, and escalation paths. Preserve
   each component's appropriate delivery method; coordinate outcomes, not ceremonies.
3. **Build the integrated view.** Maintain one program control record containing
   dependency health, integrated milestones, shared-capacity conflicts, benefits,
   risks/issues, decisions, forecasts, and changes. Link to component records rather
   than copying them.
4. **Manage the seams.** Review cross-project dependencies by provider, receiver,
   definition of ready, acceptance evidence, needed-by date, fallback, and escalation
   owner. A component marked green does not make an unmet program dependency green.
5. **Steer by evidence.** Compare actuals and forecasts with the program baseline and
   benefits hypothesis. Surface variance, confidence loss, benefit drift, and
   emerging disbenefits immediately. Missing evidence is unknown, not green.
6. **Make trade-offs.** Present options across scope, sequence, capacity, funding,
   quality, risk, adoption, and benefits. A local optimization that harms the shared
   outcome is a program issue. Preserve history when the mandate or baseline changes.
7. **Realize and transition.** Coordinate adoption, operating-model change, capability
   transfer, and benefits measurement. Use [Benefits dependency and tranche control](references/benefits-dependency-and-tranches.md)
   when components must produce a shared benefit in stages. Use [Assurance and intervention](references/assurance-and-intervention.md)
   when evidence, governance, or the integrated outcome is materially disputed or off track.
   Close or reshape the program only when the outcome decision, residual ownership,
   operational handoff, and benefits follow-up are explicit.

## Method selection

Use the smallest adequate program model. Keep governance separate from component
cadence.

| Conditions | Program pattern | First test |
|---|---|---|
| Stable outcome, fixed external gates, staged component delivery | Predictive/stage-governed program | Are component interfaces and decision gates feasible with real capacity? |
| Uncertain solution or benefits, learning must change the roadmap | Iterative/adaptive program | Is there an evidence checkpoint that can change funding or scope? |
| Many products or teams release increments into one capability | Incremental/release-train coordination | Is each increment usable and does integration evidence accumulate? |
| High dependency density and shared specialists | Flow/network coordination | Are dependency aging, capacity contention, and escalation visible? |
| Mixed hardware, software, vendor, regulatory, or organizational change | Hybrid program | Is one integrated decision view connecting the different cadences? |

Do not prescribe a branded method because the program uses multiple teams. Explain the
trade-off, authority, cadence, evidence, and revisit trigger. A program manager
coordinates; they do not acquire component owners' architecture, product, engineering,
or risk-acceptance authority by tracking their work.

## Communication contract

Tailor the same evidence to the stakeholder's decision:

- **Sponsor/executive:** outcome confidence, material variance, options, recommendation,
  decision required, latest useful decision date, and consequence of waiting.
- **Component leads:** dependency changes, interface acceptance, shared-capacity trade-
  offs, decisions needed, and what remains within their authority.
- **Operations/adoption owners:** capability readiness, training/process change,
  support model, adoption evidence, residual risk, and handoff date.
- **Vendor/partner:** provider and receiver obligations, definition of ready, evidence,
  commercial/technical constraint, escalation route, and next checkpoint.
- **Affected users or customers:** what changes, when, impact, support, uncertainty,
  and how feedback changes the plan. Do not publish internal risk detail that is not
  appropriate for the audience.

Never make a component dashboard, meeting count, or percentage complete stand in for
program health. Report health by dimension: outcome, schedule, dependency, capacity,
quality, adoption, benefits, and risk.

## Troubleshooting patterns

- **All projects green, program red:** inspect integration, shared capacity, benefit
  ownership, and adoption; do not average component status.
- **Dependency dispute:** reconstruct the provider/receiver contract and evidence,
  then escalate the decision the local owners cannot make.
- **Benefits are slipping while outputs ship:** test the benefit hypothesis, adoption
  and operating assumptions, and disbenefits; re-scope or stop rather than declaring
  output delivery equal to value.
- **Program has become a project list:** restate the shared outcome, remove unrelated
  components, and route independent investments to portfolio governance.
- **Sponsor changes direction midstream:** preserve the original mandate and variance,
  record the new decision, assess component and benefit impacts, and rebaseline only
  with authority.
- **Shared team is the bottleneck:** show competing demand and consequences; do not
  promise that adding work or meetings creates capacity.
- **Transformation resistance:** identify affected roles, decision rights, incentives,
  training, feedback channels, and adoption signals. Route organizational design to
  [org-design](../org-design/SKILL.md); keep program coordination here.
- **No evidence after repeated reviews:** stop after three non-converging diagnostic
  passes, name the missing evidence and decision owner, and escalate or pause.

## Routing table

| Need | Route |
|---|---|
| One project's milestones, vendor handoff, forecast, recovery, or closure | [technical-project-management](../technical-project-management/SKILL.md) |
| Approved requirement into work breakdown and rollout plan | [implementation-planning](../implementation-planning/SKILL.md) |
| Product bets, roadmap sequencing, or portfolio allocation | [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md) |
| Product decision rights and recurring product governance | [product-operations-and-governance](../product-operations-and-governance/SKILL.md) |
| Enterprise capabilities, target/transition architecture, or architecture authority | [enterprise-architecture](../enterprise-architecture/SKILL.md) |
| Technology adoption posture or standards governance | [technology-radar](../technology-radar/SKILL.md) |
| Release mechanics or launch authorization | [release-engineering](../release-engineering/SKILL.md) and [production-readiness](../production-readiness/SKILL.md) |
| Live outage or responder command | [site-reliability-engineering](../site-reliability-engineering/SKILL.md) |
| Capital allocation, corporate strategy, or M&A | [strategy-frameworks](../strategy-frameworks/SKILL.md) |
| Organizational structure and talent design | [org-design](../org-design/SKILL.md) |
| Independent assurance or troubled-program intervention | [Assurance and intervention](references/assurance-and-intervention.md) |
| Post-delivery adoption evidence or benefits learning | [product-adoption](../product-adoption/SKILL.md) and [product-lifecycle-learning](../product-lifecycle-learning/SKILL.md) |

## Output contract and completion

Produce the smallest useful artifact: program brief, integrated dependency/control
record, benefits map, governance decision, escalation brief, stakeholder update,
recovery options, or transition/closure record. Separate evidence, inference,
assumptions, commitments, options, and unknowns. Link to component sources and name
owners rather than inventing agreement.

Complete when the requested program decision or artifact is delivered, the shared
outcome and component boundaries are explicit, material dependencies and benefits have
owners and review triggers, unresolved authority is escalated, and no claim exceeds
the evidence. Do not imply ongoing monitoring without an authorized mechanism.

## Research basis and limitations

This synthesis is informed by a deep, source-grounded research artifact retained
with the development record, including PMI's *The Standard for Program Management,
Fifth Edition* (2024), UK Government Project Delivery guidance, Local Government
Association dependency guidance, and NASA risk management guidance. The deep run
confirmed the value of benefits dependency mapping, tranches, disbenefits, enterprise
risk categories, and independent assurance. It directly consulted three sources; the
NASA handbook PDF and some UK pages remained inaccessible to the scraper, so claims
requiring those exact documents are not presented as verified here. The sources provide
principles and jurisdiction-specific requirements, not a universal operating model or
proof that any method guarantees success. Use formal organizational or regulatory
standards when they govern the actual program.
