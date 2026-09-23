---
name: technology-radar
description: Build and maintain technology radars for adoption, trial, assessment, and hold decisions, and choose proportionate architecture-governance paths for technology portfolios. Use when governing technology choices, build-versus-buy decisions, architecture standards, exceptions, or engineering portfolio risk. Do not use for enterprise capability or target-state architecture, writing ADRs, implementing systems, security engineering, or operational incident/runbook work.
license: MIT
compatibility: No runtime dependency.
metadata:
  source_repo: https://github.com/magnus919/hermes-profiles
  source_commit: 867a555
---


# Technology Radar

CTO methodology for making technology decisions, governing architecture, measuring engineering effectiveness, managing technical debt, and operating an innovation pipeline. These frameworks help a CTO balance short-term delivery velocity with long-term platform health.

## When Not to Use

- Route enterprise capability maps, operating-model design, and current/target-state roadmaps to [`enterprise-architecture`](../enterprise-architecture/SKILL.md). This skill stays focused on technology portfolio posture and governance mechanics; use [`software-architecture`](../software-architecture/SKILL.md) for system-level target design.
- Route the durable record of one consequential decision to `adr-authoring`; use this skill to choose the governance path and connect the decision to standards or radar feedback.
- Route system design and code changes to the relevant engineering skill, security requirements and threat modeling to `secure-software-engineering`, and live operations or SLO work to `site-reliability-engineering`.

## Domain Model

| Domain | Covers | Artifact |
|--------|--------|----------|
| **Technology Radar** | Adopt/Trial/Assess/Hold quadrants, tool selection criteria, deprecation policy | Technology radar document |
| **Build vs Buy** | TCO analysis, decision matrices, vendor evaluation, integration cost | Build-vs-buy recommendation |
| **Architecture Governance** | Automated policy, federated decisions, advice processes, centralized review, standards, exceptions, and feedback | Governance decision record, standard, exception, radar update |
| **Engineering Metrics** | DORA (deploy frequency, lead time, MTTR, change failure rate), SPACE, DevEx | Engineering dashboard, health report |
| **Technical Debt** | Interest calculation, remediation prioritization, principal estimation | Technical debt register |
| **Innovation Pipeline** | Horizon scanning, POC criteria, production readiness gates | Innovation funnel, POC report |

## When to Load

Load this skill when the task involves:

- Evaluating a new technology or tool for adoption
- Making a build-vs-buy decision with TCO analysis
- Designing or auditing architecture governance processes
- Setting up engineering metrics dashboards (DORA, SPACE)
- Quantifying and prioritizing technical debt remediation
- Running an innovation pipeline with POC-to-production gates
- Deprecating or retiring legacy technology
- Selecting or auditing automated policy, federated decisions, advice processes, or centralized review


## Governance Workflow

For architecture or technology-governance work, read `references/architecture-governance.md` and:

1. Establish the decision, intended outcome, affected systems and teams, evidence available, and the decision owner.
2. Assess reversibility, scope, risk, blast radius, regulatory exposure, and cross-team impact. Record uncertainty instead of converting it into a false score.
3. Select the lightest governance mode that still controls the credible downside: automated policy, federated decision, advice process, or centralized review. Escalate when evidence shows that the decision is less reversible, broader, riskier, or more regulated than first assumed.
4. Define the decision record, implementation checks, exception path, and signals that will cause reconsideration.
5. Feed implementation and operational evidence back into the decision, standards, exceptions, and radar posture. Treat feedback as a reason to learn, not as retroactive blame.

## Reference Files

| Reference | Load When | File |
|-----------|-----------|------|
| Technology Radar | You need to evaluate and categorize a technology or tool for adoption, trial, assessment, or hold | `references/technology-radar.md` |
| Build vs Buy | You're comparing build vs buy options with TCO analysis and decision criteria | `references/build-vs-buy.md` |
| Architecture Governance | You're choosing or auditing proportional governance modes, standards, exceptions, escalation, or feedback | `references/architecture-governance.md` |
| Engineering Metrics | You need to measure engineering effectiveness with DORA, SPACE, or DevEx frameworks | `references/engineering-metrics.md` |

## Design Principles

1. **Technology is a means, not an end.** Every technology decision must trace back to a business outcome. "Because it's new" is not a reason to adopt. "Because it solves X faster/safer/cheaper" is.
2. **Radar is a living document.** A technology radar should be refreshed when evidence, strategy, risk, or usage changes materially. Set a cadence that fits the portfolio, and make significant adoption, hold, promotion, or retirement decisions trigger an update rather than waiting for a calendar event.
3. **Build vs buy is never just cost.** Total Cost of Ownership includes maintenance, hiring, training, integration, migration, and opportunity cost. A cheaper build today may be vastly more expensive over 3 years.
4. **Engineering metrics measure the system, not the people.** DORA metrics measure the delivery capability of the org. SPACE measures developer satisfaction. Neither is a performance review tool for individuals.
5. **Technical debt has a principal and an interest payment.** The principal is the cost to fix it properly. The interest is the recurring drag on velocity. Prioritize debt where interest/principal ratio is highest.
6. **Production readiness gates exist to prevent crisis.** Every gate that is skipped in the name of speed will be paid for in incident response time later.
7. **Governance should follow consequence.** Local and reversible decisions should stay local; irreversible, regulated, high-blast-radius, or materially cross-team decisions need stronger coordination or authority.

## Portability

This skill is intentionally host-neutral. Use your agent's normal mechanisms to load the references, templates, and scripts listed here. Do not assume a particular profile system, task orchestrator, memory service, or response-handoff format.
