---
name: site-reliability-engineering
description: >-
  Design, operate, and improve reliable production systems with SLOs, incident command,
  observability, error budgets, and operational practices. Do not use this skill for
  unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Python 3.9+ is required only for the bundled calculation and summary scripts.
metadata:
  source_repo: https://github.com/magnus919/hermes-profiles
  source_commit: 867a555
  enrichment_sources: "Seeking SRE; The Site Reliability Workbook"
---


# Site Reliability Engineering

A comprehensive methodology for designing, operating, and improving reliable production systems. Rooted in Google SRE principles and extended with modern practices for incident command, observability engineering, error budget governance, and operational excellence.

## When to Load This Skill

| Trigger | What It Means |
|---|---|
| "Design reliability into this system" | SLO/SLI framework, error budget policy, resilience architecture |
| "Run an incident postmortem" | Blameless postmortem with timeline, 5 Whys, action tracking |
| "Improve our on-call" | Rotation design, alert tuning, toil reduction, escalation policy |
| "Build observability" | The Four Golden Signals, dashboard design, alert rule patterns |
| "Do a reliability review" | Architecture review against SRE principles, risk assessment |
| "I need an incident commander" | Incident command framework, role cards, communication templates |
| "Automate this operational task" | Toil assessment, automation decision tree, runbook pattern |
| "Adopt SRE in this organization" | Engagement boundaries, maturity, team model, and change adoption |
| "Review this reliability design" | User journeys, dependencies, overload, configuration, canary, durability |
| "Our SRE team is overloaded" | Operational-load diagnosis, protected engineering time, recovery plan |
| "Improve incident learning or sustainable on-call" | Cognitive load, psychological safety, documentation, exercises |
## When not to use

Use [release-engineering](../release-engineering/SKILL.md) to plan releases, compose promotion and rollback gates, or coordinate a release train. Use [systematic-debugging](../systematic-debugging/SKILL.md) to find the cause of a specific failure. Operating the telemetry stack itself — Prometheus scrape configs, OpenTelemetry Collector pipelines, Loki ingest and retention, Prometheus rules files — belongs to [telemetry](../telemetry/SKILL.md); this skill owns the SLI/SLO and alert *design* those rules implement. Grafana product work — dashboards, panels, Grafana-side alert rules, contact points, notification policies — belongs to [grafana](../grafana/SKILL.md).

## Operational closure gate

For any automated mitigation, rollback, recovery action, or incident closeout:

1. **Bound the action before it starts.** Record the target, affected population, maximum blast radius, success criterion, abort/rollback criteria, rollback target and procedure, and who may stop or reverse it. Prefer the smallest reversible scope and staged expansion.
2. **Verify recovery at the user boundary.** After the action, follow the [R-01 closure evidence sequence](templates/runbook-template.md#r-01-post-incident-steps): check the user-facing SLOs, critical user journey, relevant dependency health, and data/state correctness. Observe a defined stability window and check secondary effects such as backlog recovery.
3. **Do not equate alert resolution with recovery.** A cleared alert or passing health endpoint is evidence, not a resolution verdict. If required evidence is missing, retain the `MITIGATING` or `MONITORING` state, name the unverified boundary, and escalate rather than declare `RESOLVED`.
4. **Record the evidence.** Capture the action, scope, thresholds, observed recovery evidence, remaining uncertainty, and rollback/follow-up trigger in the incident or change record.

"Pre-authorized" means a human service owner, incident commander, or other designated change authority has explicitly approved the specific action and scope in the current incident or change record, with an approval action or confirmation independently attributable to that human. A request to investigate or diagnose, an approved standing policy/runbook without current human confirmation, an agent-authored note or self-claimed role, or the agent's own judgment is not production-mutation authorization. Automation may execute only after that authorization is verified and the action is bounded. It must stop and hand off when authorization, blast radius, rollback path, or recovery evidence cannot be established.

## Reference Files

| Topic | File | When to Load |
|---|---|---|
| SRE Book Chapter Summaries | `references/sre-book-chapters.md` | Design engagement, first principles review |
| SLO/SLI Framework | `references/slo-sli-framework.md` | Defining reliability targets |
| SLO Implementation Recipe | `references/slo-implementation-recipe.md` | Agent-executable SLO adoption sequence and stakeholder review |
| Error Budget Governance | `templates/error-budget-policy.md` and `references/slo-sli-framework.md` | Policy design, burn rate alerts |
| Incident Command System | `references/incident-command-system.md` | During/after incident, training |
| Blameless Postmortems | `references/postmortem-culture.md` | After incident, process design |
| Monitoring & Alerting | `references/monitoring-alerting.md` | Observability design, alert rules |
| On-Call Best Practices | `references/oncall-best-practices.md` | Rotation design, team sizing |
| Toil Elimination | `references/toil-elimination.md` | Automation prioritization, ops review |
| Release Engineering | [release-engineering](../release-engineering/SKILL.md) | Release planning, promotion, progressive delivery, and rollback design; use the local reference only for SRE-specific integration context |
| Effective Troubleshooting | `references/troubleshooting.md` | Debugging methodology |
| Senior SRE Role Blueprint | `references/senior-sre-blueprint.md` | Role definition, KPI framework |
| SRE Communication Guide | `references/sre-communication-guide.md` | Stakeholder updates, incident communication |
| Guiding Principles | `references/guiding-principles.md` | First principles, philosophy |
| Product-Focused Reliability | `references/product-focused-reliability.md` | Product-centric SRE, CUJ-based SLOs, JTBD model |
| Twenty Years of Lessons | `references/twenty-years-lessons.md` | Incident-derived tactical lessons, Prodverbs |
| SRE Ecosystem Guide | `references/sre-ecosystem-guide.md` | Curated guide to all SRE resources (Workbook, Secure Systems, Classroom, Prodcast, STPA, Video Gallery, Mobaa, fundamentals, AI ops) |
| Adoption and Engagement | `references/sre-adoption-and-engagement.md` | Starting SRE, dedicated and non-dedicated team models, maturity, change adoption |
| Reliability Design and Change | `references/reliability-design-and-change.md` | Capacity, overload, configuration, canaries, data durability, dependencies, design review |
| Human Systems and Learning | `references/human-systems-and-learning.md` | Cognitive work, sustainable on-call, psychological safety, documentation, exercises |
| Third-Party Dependency Reliability | `references/third-party-dependency-reliability.md` | Vendor boundaries, failure modes, fallbacks, and provider evidence |
| Operational Documentation | `references/operational-documentation.md` | Functional quality, ownership, testing, and staleness lifecycle |

## Templates

| Template | File | Purpose |
|---|---|---|
| Incident Commander Checklist | `templates/incident-command-checklist.md` | Step-by-step IC response |
| Postmortem Template | `templates/postmortem-template.md` | Blameless postmortem document |
| Runbook Template | `templates/runbook-template.md` | Operational runbook standard |
| SLO Declaration Template | `templates/slo-declaration-template.md` | Service-level objective specification |
| Error Budget Policy | `templates/error-budget-policy.md` | Team-level error budget governance |
| On-Call Rotation Template | `templates/oncall-rotation.md` | Rotation schedule and escalation |
| Service Review Checklist | `templates/service-review-checklist.md` | Pre-launch reliability review |
| Incident Communication Template | `templates/incident-communication.md` | Status updates during incidents |
| Reliability Design Review | `templates/reliability-design-review.md` | Evidence-based review of user impact, failure modes, capacity, change, and operations |
| Operational Overload Recovery | `templates/operational-overload-recovery.md` | Declare, protect, reduce, and verify recovery from unsustainable operational load |
| Reliability Ownership Charter | `templates/reliability-ownership-charter.md` | Make service, pager, dependency, and engagement boundaries explicit |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/slo-burn-rate.py` | Calculate error budget burn rate from SLI data |

## Portability

This skill is intentionally host-neutral. Use your agent's normal mechanisms to load the references, templates, and scripts listed here. Do not assume a particular profile system, task orchestrator, memory service, or response-handoff format.
