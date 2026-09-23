---
name: technical-project-management
description: >-
  Manage technical projects from initiation through delivery and closure: choose
  and tailor predictive, iterative, Scrum, flow-based, or hybrid approaches;
  coordinate teams and vendors; track milestones, risks, issues, dependencies,
  forecasts, scope changes, and recovery. Use when a team has no project manager,
  a TPM needs decision-ready analysis, a project is slipping, or commitments and
  handoffs need coordination. Use `technical-program-management` instead when
  multiple related projects, teams, vendors, shared capacity, or benefits must be
  coordinated toward one outcome. Adapt depth to the user's expertise. Do not use for
  a standalone coding task, product discovery or strategy, only writing an
  implementation plan, only diagnosing Kanban flow, operating a ticket tool,
  incident command, or a release go/no-go decision; route those to specialists.
license: MIT
compatibility: >-
  Host-neutral methodology and Markdown templates. Optional read-only schedule
  analysis requires Python 3.10+ standard library; no credentials or network.
---

# Technical Project Management

Help a team make and maintain credible delivery commitments. Start at the user's
current decision; do not restart a healthy project or impose a new methodology.

## First move

Read existing project artifacts before asking questions. Identify the outcome,
current phase, immediate decision, decision-maker, constraints, and evidence gaps.
Infer experience from the request and artifacts; ask about preference only if it
matters. For teams without a PM, provide a small usable working system and explain
unfamiliar concepts in context. For experienced TPMs, lead with the delta, options,
recommendation, and decision needed; omit introductory lessons.

### Choose the entry point

| Starting condition | First action | Primary output |
|---|---|---|
| New or inherited project with unclear mandate | Read [Engagement and initiation](references/engagement-and-initiation.md) | Proposed brief with authority and evidence gaps |
| Approved work with a delivery method but weak control | Read [Control and communication](references/control-and-communication.md) | Current control record and decision brief |
| Slipping date, cost, scope, or dependency | Read [Forecasting and schedule analysis](references/forecasting.md) and [Change and recovery](references/change-and-recovery.md) | Conditional forecast and recovery options |
| Cross-team, supplier, or mixed-method handoff | Read [Hybrid and dependencies](references/hybrid-and-dependencies.md) | Dependency agreement and acceptance evidence |
| Delivered work, retirement, or decommissioning with unresolved ownership or benefits | Read [Closure and transition](references/closure-and-transition.md) | Conditional closure, accepted transition, or decommissioning record |
| Technical uncertainty needs staged learning | Read [Adaptive delivery](references/adaptive-delivery.md) | Evidence-backed decision among PoC, prototype, pilot, or stop; none alone proves production readiness |
| Forecast, deadline, or resource-feasibility question | Read [Forecasting and schedule analysis](references/forecasting.md) | Conditional forecast stating model, assumptions, capacity, and feasibility limits |
| Material risk, issue, assumption, or decision needs control | Read [Control and communication](references/control-and-communication.md) | Record with owner, signal/trigger, response, authority, and next review |
| A supplier or team handoff lacks readiness or acceptance evidence | Read [Hybrid and dependencies](references/hybrid-and-dependencies.md) | Agreement with provider, receiver, definition of ready, evidence, fallback, and escalation |

Do not call a desired date a commitment, a forecast an acceptance, or a diagnostic brief an approved plan.

> Before proposing a commitment, identify who can authorize scope, dates, capacity, acceptance, and external communication. Mark each as accepted, proposed, unknown, or disputed. Read-only diagnosis may proceed; external updates require authorization.

## Operating loop

1. Establish mandate and authority; separate approved commitments, forecasts,
   assumptions, and unknowns. A diagnostic or options brief can precede approval;
   do not turn it into an approved implementation plan.
2. Select the smallest adequate management approach. Preserve effective existing
   practices and specify any changed decision rights, cadence, and handoffs.
3. Reuse the implementation plan and maintain milestones, dependency commitments,
   remaining work, resource availability, risks, issues, and decisions.
4. Compare evidence with the baseline and tolerances. Investigate contradictions;
   missing evidence means unknown, not green. Surface forecast changes immediately
   when material; do not wait for a scheduled report.
5. Present feasible options when scope, capacity, cost, or dates conflict. Keep the
   baseline history; an authorized change is not permission to hide prior variance.
6. Close only on acceptance and explicit residual ownership. Distinguish project
   closure, release readiness, service operation, and later benefit realization.

## Reference routing

Read only what the current task requires. Each reference includes applicability,
procedures, failure signals, and an observable exit.

A multi-project initiative with a shared outcome, cross-project dependencies, or
program-level benefits belongs to `technical-program-management`; a single bounded
project remains here.

| Decision phase / situation | Read | Exit artifact or evidence |
|---|---|---|
| New or inherited project, no PM, expert collaboration | [Engagement and initiation](references/engagement-and-initiation.md) | Proposed brief with mandate, authority, and evidence gaps |
| Choosing or questioning a methodology | [Method selection](references/method-selection.md) | Approach decision with adaptations and revisit trigger |
| Predictive planning, stages, tolerances, fixed constraints | [Predictive and stage governance](references/predictive-and-stages.md) | Baseline, tolerances, and gate evidence |
| Scrum, iteration, incremental delivery, discovery uncertainty | [Adaptive delivery](references/adaptive-delivery.md) | Learning/increment evidence and inspect/adapt decision |
| Flow, shared specialists, critical chain, appetite-based work | [Flow and constrained capacity](references/flow-and-capacity.md) | Capacity/WIP or appetite decision with owner |
| Mixed methods, cross-team or vendor interfaces | [Hybrid and dependencies](references/hybrid-and-dependencies.md) | Dependency agreement and interface acceptance evidence |
| Estimates, forecasts, budgets, schedule model | [Forecasting and schedule analysis](references/forecasting.md) | Conditional forecast with assumptions and feasibility limits |
| Weekly control, stakeholder disagreement, escalations | [Control and communication](references/control-and-communication.md) | Status/update or decision brief with next checkpoint |
| Scope changes, troubled projects, recovery | [Change and recovery](references/change-and-recovery.md) | Change/recovery record preserving the baseline |
| Acceptance, cancellation, operational handoff | [Closure and transition](references/closure-and-transition.md) | Closure or transition record with residual owners |
| Real examples or transferability checks | [Case studies](references/case-studies.md) | Source-limited analogy, not a guarantee |
| Research provenance, edition, evidence limits | [Source index](references/source-index.md) | Traceable evidence ledger |
| Skill purpose, coverage, research decisions | [Research brief](references/research-brief.md) | Coverage and limitation record |
| Validation scope and behavioral evaluation protocol | [Evaluation guide](references/evaluation-guide.md) | Reproducible evaluation record |

## Templates and calculation

Adapt existing project documents rather than creating parallel sources of truth.
Use only artifacts that answer a current decision.

| Need | Artifact |
|---|---|
| Establish mandate and working agreements | [Project brief](templates/project-brief.md) |
| Explain method choice and adaptation | [Approach decision](templates/approach-decision.md) |
| Maintain milestones and evidence | [Project control record](templates/project-control.md) |
| Coordinate a supplier or receiving team | [Dependency agreement](templates/dependency-agreement.md) |
| Report a change and ask for a decision | [Status and decision brief](templates/status-and-decision.md) |
| Assess scope changes or recovery options | [Change and recovery record](templates/change-and-recovery.md) |
| Accept, cancel, or transfer ownership | [Closure record](templates/closure-record.md) |
| Calculate a small dependency network | [Example schedule](templates/schedule-example.json) |

Run `python3 scripts/schedule.py --input templates/schedule-example.json --json`
from this skill's directory when dependency arithmetic helps. Read forecasting
first: the result is an unconstrained earliest schedule, not a commitment or a
resource-leveled plan. The script only reads input and writes stdout/stderr.
Run `python3 -m unittest discover -s scripts -p 'test_*.py'` for its tests.

## When not to use

- A coding fix or architecture design: use the applicable engineering skill.
- Validating needs or choosing product investments: use
  [product-discovery](../product-discovery/SKILL.md) or
  [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md).
- Only decomposing an approved requirement: use
  [implementation-planning](../implementation-planning/SKILL.md).
- Detailed board, WIP, or service-flow diagnosis: use
  [kanban-guru](../kanban-guru/SKILL.md).
- Shaping a bounded product bet: use [product-shaping](../product-shaping/SKILL.md).
- Product-wide decision rights: use
  [product-operations-and-governance](../product-operations-and-governance/SKILL.md).
- Executive-office support: use
  [chief-of-staff-methodology](../chief-of-staff-methodology/SKILL.md).
- Release mechanics or launch approval: use
  [release-engineering](../release-engineering/SKILL.md) and
  [production-readiness](../production-readiness/SKILL.md). This skill may track project implications after that decision, but does not approve the release.
- Live incident command: use
  [site-reliability-engineering](../site-reliability-engineering/SKILL.md).
- Ticket operations alone: use [jira](../jira/SKILL.md) or
  [linear](../linear/SKILL.md). Use [financial-modeling](../financial-modeling/SKILL.md)
  for financial model construction, and [legal-strategy](../legal-strategy/SKILL.md)
  for contract interpretation.

## Authority and completion

This methodology prepares decisions. It does not invent stakeholder consent,
assign accepted commitments on someone else's behalf, or approve risk. Updating
external project systems or sending communications changes external state:

> Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

Apply existing session authorization; do not ask repeatedly for the same scope.
Destructive actions need an explicit directive. Keep prepared drafts visibly distinct
from issued communications. Do not monitor people or turn activity counts into
individual performance judgments.

Complete a requested management cycle when the artifact or update is delivered,
claims have evidence or explicit uncertainty, and unresolved decisions have an
accountable route and next review trigger. Do not imply ongoing monitoring without
an authorized mechanism. If three diagnostic passes yield no new evidence, stop
with the missing input and affected decision; do not manufacture certainty.
