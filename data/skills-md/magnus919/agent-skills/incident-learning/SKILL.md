---
name: incident-learning
description: >-
  Convert operational incident and near-miss evidence into durable product,
  engineering, test, evaluation, and governance improvements with verified
  closure. Separate observed facts from causal hypotheses and unresolved
  uncertainty; map follow-up work across code, tests, skills, operations,
  product, and governance; track ownership, verification, and closure for
  every finding. Do not use to assign blame or produce a generic postmortem
  template; do not close learning because tickets were created — require
  evidence the intended change occurred.
license: MIT
compatibility: Platform-agnostic methodology. No runtime dependency.
---

# Incident Learning

Convert operational incidents, near misses, and exercise findings into verified, owned improvements across product, engineering, test, evaluation, and governance domains. This skill owns the learning pipeline — the structured method that takes raw incident evidence and produces durable follow-up work with closure evidence. It does not own incident response, postmortem facilitation, or implementation of follow-up work; it owns the conversion from evidence to verified change.

## When to use

| Trigger | What it covers |
|---|---|
| "Convert this incident into follow-up work" | Evidence separation, causal ledger, follow-up work map, ownership assignment |
| "What did we learn from this incident?" | Learning record with facts, hypotheses, uncertainty, escaped-from mapping |
| "Track this finding to closure" | Verification record, closure evidence, follow-up work status |
| "Link this incident to a missing requirement" | Escaped-from gap mapping: requirements, monitoring, authority, migration, adoption |
| "Review our incident follow-up closure rate" | Learning pipeline audit, unverified closures, stale follow-up work |
| "Process this near-miss" | Near-miss learning record, contributing conditions, risk reduction follow-up |
| "Build an incident learning record" | Structured record with evidence/inference/uncertainty separation and escaped-from analysis |

## When not to use

- **Assigning blame or conducting a blame-based review.** This skill is explicitly blameless. It converts evidence into improvements, not fault into consequences. It contains no blame-assignment process, no "who to blame" field, and no "blameworthy" classification. If you need a postmortem that identifies responsible individuals, this skill will not serve that purpose.
- **Producing a generic postmortem template as the sole output.** This skill's artifacts — the incident-learning record, causal/evidence ledger, follow-up work map, and verification and closure record — are the primary deliverables. A postmortem, timeline, or five-whys analysis may inform the learning record but is never the terminal output.
- **Live incident command or incident response.** Route to [site-reliability-engineering](../site-reliability-engineering/SKILL.md) for the incident command system, on-call operations, and real-time incident management.
- **Facilitating a blameless postmortem session.** Route to [site-reliability-engineering](../site-reliability-engineering/SKILL.md) for postmortem culture, timeline construction, and facilitation methods. This skill consumes postmortem output; it does not produce it.
- **Closing learning because tickets were created.** Ticket creation is an action, not an outcome. This skill requires verification that the intended change occurred and had the intended effect. A ticket alone is not closure.
- **Root-cause debugging of a specific failure.** Route to [systematic-debugging](../systematic-debugging/SKILL.md) for failure investigation. This skill consumes debugging findings as input to the learning pipeline.

## Core principles

**Evidence, not inference, is the foundation.** Every incident learning record separates three categories: observed facts (what happened, backed by telemetry, logs, or direct observation), causal hypotheses (inferences about why it happened, labeled with confidence and alternative explanations), and unresolved uncertainty (what remains unknown, including open questions and competing hypotheses). Conflating these categories produces false confidence. See the evidence/inference/uncertainty taxonomy in the learning record template.

**Learning closes with verification, not tickets.** Creating a ticket, a task, or a story is a process step — not evidence of improvement. Closure requires: (1) the follow-up work was implemented, (2) the implementation was verified against the intended change, and (3) the intended effect was observed (or a revised hypothesis was recorded). The verification and closure record template enforces this standard. Tickets alone are explicitly not sufficient; the closure record must reference evidence of the implemented change.

**Follow-up work spans domains, not only code.** An incident can expose gaps in any of six domains: product (requirements, design, user experience), code (implementation, logic, dependencies), tests (regression coverage, integration tests, assertions), evals (evaluation cases, grader coverage, dataset gaps), operations (monitoring, alerting, runbooks, capacity), and governance (authority boundaries, policy, compliance, access control). The follow-up work map uses this six-domain taxonomy; every finding maps to at least one domain.

**Every incident escaped from something.** The "escaped from" analysis maps the originating gap to one or more of: an escaped requirement (a needed requirement that was absent or incomplete), missing monitoring or observability (no signal existed to detect the condition), unsafe authority or access (insufficient guardrails on who could act), a migration gap (a transition that introduced the condition), or an adoption consequence (user or operator behavior that contributed). This mapping drives the follow-up work: a monitoring gap produces an observability follow-up, not a code patch.

**Uncertainty is recorded, not hidden.** Competing causal hypotheses, incomplete data, and open questions are explicit fields in the learning record — not footnotes. Unresolved uncertainty drives investigation follow-up work: what needs to be instrumented, what data needs to be collected, what hypothesis needs to be tested. An incident learning record with no unresolved uncertainty is either trivial or premature.

**Blame is absent by design.** The learning record has no field for "who caused this," "responsible individual," or "blameworthy action." The method treats incidents as system outcomes — products of interacting components, processes, assumptions, and conditions — not individual failures. This is not a stylistic preference; it is a structural constraint of the templates and the record format.

## The incident learning record

The incident learning record is the primary artifact. It contains these structured fields:

| Field | Content | Requirement |
|---|---|---|
| **Incident identifier** | Unique ID, date, duration, severity, systems affected | Required |
| **Observed facts** | What happened — backed by telemetry, logs, direct observation, timeline events | Required; no inference here |
| **Causal hypotheses** | Inferences about why it happened, each labeled with confidence level and alternative explanations | Required; must be separated from facts |
| **Contributing conditions** | System states, process gaps, environmental factors that enabled or amplified the incident | Required |
| **Unresolved uncertainty** | Open questions, competing hypotheses, missing data, unknowns | Required; drives investigation follow-up |
| **Escaped-from mapping** | Originating gap: escaped requirement, missing monitoring/observability, unsafe authority/access, migration gap, adoption consequence | Required; at least one category |
| **Follow-up work map** | Findings mapped to domains (product, code, tests, evals, operations, governance) with ownership and verification method | Required; at least one follow-up per significant finding |
| **Verification and closure record** | For each follow-up: implementation evidence, verification evidence, effect evidence, closure date, closure authority | Required for closure; tickets alone are not sufficient |

## Loading guide

| File | Load when |
|---|---|
| [references/discovery-brief.md](references/discovery-brief.md) | Understanding ownership boundaries with adjacent skills and routing decisions |
| [references/evidence-inference-taxonomy.md](references/evidence-inference-taxonomy.md) | Separating observed facts from causal hypotheses and unresolved uncertainty in an incident record |
| [references/escaped-from-analysis.md](references/escaped-from-analysis.md) | Mapping incidents to originating gaps: requirements, monitoring, authority, migration, adoption |
| [references/follow-up-domains.md](references/follow-up-domains.md) | Mapping findings to the six follow-up domains (product, code, tests, evals, operations, governance) with ownership patterns |
| [references/verification-and-closure.md](references/verification-and-closure.md) | Defining what constitutes verified closure, rejecting ticket-only closure, and recording closure evidence |

## Templates

| Template | File | Purpose |
|---|---|---|
| Incident-learning record | [templates/incident-learning-record.md](templates/incident-learning-record.md) | Structured record with facts/hypotheses/uncertainty separation and escaped-from mapping |
| Causal/evidence ledger | [templates/causal-evidence-ledger.md](templates/causal-evidence-ledger.md) | Ledger tracking each causal claim with supporting evidence, confidence, and alternatives |
| Follow-up work map | [templates/follow-up-work-map.md](templates/follow-up-work-map.md) | Six-domain follow-up work map with ownership, verification method, and status tracking |
| Verification and closure record | [templates/verification-and-closure-record.md](templates/verification-and-closure-record.md) | Per-follow-up closure record requiring implementation evidence, verification evidence, and effect evidence |

## Routing and related skills

This skill composes capabilities from and routes to:

- **[site-reliability-engineering](../site-reliability-engineering/SKILL.md)** — Incident command, on-call operations, SLO/SLI framework, blameless postmortems, monitoring and alerting. SRE owns the live incident response and postmortem facilitation; incident-learning consumes postmortem output and converts it into verified follow-up work.
- **[qa-methodology](../qa-methodology/SKILL.md)** — Test strategy, regression testing, quality gates. Incident findings that reveal test gaps (missing regression coverage, weak assertions, untested paths) produce follow-up work routed to QA methodology for test design and implementation.
- **[verification-methodology](../verification-methodology/SKILL.md)** — Pass/fail assessment against explicit criteria. Incident-learning's closure standard requires verification evidence; verification-methodology provides the protocol for producing that evidence against the intended change.
- **[agent-evals-and-observability](../agent-evals-and-observability/SKILL.md)** — Agent evaluation design, dataset management, grading, trajectory review. Incidents involving agent behavior produce eval-gap follow-up work (missing eval cases, inadequate grader coverage, unobserved failure modes) routed to agent-evals-and-observability.
- **[product-lifecycle-learning](../product-lifecycle-learning/SKILL.md)** — Post-launch outcome review, assumption updating, feature retirement. Incidents that reveal product-assumption failures (a feature used differently than intended, an assumption that didn't hold) produce product follow-up work routed to product-lifecycle-learning for assumption-update and feature-health decisions.
- **[implementation-planning](../implementation-planning/SKILL.md)** — Delivery planning, work breakdown, dependency mapping, rollout strategy. Cross-domain follow-up work that spans multiple teams or repositories is routed to implementation-planning for coordinated delivery planning.
- **[resilience-and-recovery](../resilience-and-recovery/SKILL.md)** — Resilience design, exercise evidence, game days, restore testing. Exercise and DR test findings feed into incident-learning for cross-incident pattern analysis and verified follow-up closure. Incident-learning consumes exercise findings as input; resilience-and-recovery owns the exercise design.
- **[production-readiness](../production-readiness/SKILL.md)** — Launch evidence packet, go/no-go decisions. Incident-learning findings that reveal systemic production gaps feed into production-readiness evidence packets for future launch decisions.

This skill feeds the **production-excellence** bundle (not yet landed) and the **agent-production-operations** bundle (not yet landed) as a component capability: incident learning records, causal ledgers, follow-up work maps, and closure records flow into production-excellence for cross-incident pattern analysis and into agent-production-operations for agent-specific operational learning.

## What incident-learning does NOT own

- **Incident command and live response**: owned by site-reliability-engineering. Incident-learning does not manage live incidents or run incident response.
- **Postmortem facilitation**: owned by site-reliability-engineering. Incident-learning consumes postmortem output; it does not facilitate postmortem sessions.
- **Root-cause debugging**: owned by systematic-debugging. Incident-learning consumes debugging findings as input.
- **Test design and implementation**: owned by qa-methodology. Incident-learning identifies test gaps; QA methodology designs and implements the tests.
- **Eval framework implementation**: owned by agent-evals-and-observability. Incident-learning identifies eval gaps; agent-evals-and-observability designs the evals.
- **Implementation of follow-up work**: owned by the relevant specialist skill per domain. Incident-learning owns the learning record, follow-up map, and closure verification — not the implementation itself.
- **Release decisions**: owned by production-readiness. Incident-learning feeds evidence into production-readiness; it does not make go/no-go calls.
