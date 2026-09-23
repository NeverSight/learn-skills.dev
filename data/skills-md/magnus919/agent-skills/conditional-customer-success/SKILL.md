---
name: conditional-customer-success
description: >-
  Guide recurring human-relationship practices — success plans, health
  evidence, renewal and expansion signals, QBRs, handoffs, escalation, and
  closed-loop Voice of Customer. Do not use this skill for products without
  accounts, renewals, QBRs, or a customer-success team, including some
  internal tools, pure transactional products without recurring relationships,
  and public services without account-based engagement. Load only when the
  product context includes a recurring human relationship; decline or route
  away otherwise.
license: MIT
metadata:
  tags: customer-success, success-plan, health-evidence, renewal, expansion,
    QBR, escalation, handoff, voice-of-customer, feedback-closure, account-management,
    B2B, transactional, public-service, internal-product, conditional-skill
---

# Conditional Customer Success

A CONDITIONAL skill for products with recurring human relationships. This
skill must **never** be loaded for every product context. It loads only when
the product has accounts, renewals, QBRs, or a dedicated customer-success
team. When those conditions are absent — for internal tools, pure transactional
products, or public services without account-based engagement — this skill
declines and routes the caller away.

## When to Load (Should-Trigger Examples)

| Example | What makes it a match |
|---|---|
| B2B subscription product with named account managers | Accounts, renewals, dedicated CS team |
| Enterprise SaaS with quarterly business reviews | QBR cadence, account-tier engagement |
| Renewal-risk analysis needed for a contract portfolio | Renewal evidence, churn-risk signals |
| Product with an assigned customer-success team managing health plans | Success plans, health tracking |
| Account-expansion opportunity identified but adoption signals are mixed | Expansion with relationship context |
| Customer feedback loop — insight surfaced, product change made, customer communication needed | Closed-loop Voice of Customer |

## When not to use

This skill must not be loaded for products without accounts, renewals,
QBRs, or a customer-success team. See the should-not-trigger examples below.

## When NOT to Load (Should-Not-Trigger Examples)

This skill must **not** load when the product context lacks the required
preconditions. The skill must decline and route the caller away.

| Example | Why it does not apply |
|---|---|
| Internal developer tool with no accounts, no renewals, no QBRs | No recurring human relationship; no CS team |
| Pure transactional e-commerce product — one-time purchases, no account management | No accounts, no renewals, no QBRs, no CS team |
| Public-service benefit-application portal — no account-tier engagement, no CS team | No accounts (in the CS sense), no renewals, no QBRs |
| Consumer mobile game with subscription billing but no human CS relationship | Subscription alone is insufficient; no human CS relationship |
| Open-source project with community support but no paid accounts | No accounts, no renewals, no CS team |
| Internal analytics dashboard for a single team | No recurring relationship outside the team; no CS team |

**Decline rule**: If none of the should-trigger conditions are present — that is,
the product has no accounts, no renewals, no QBRs, and no customer-success
team — this skill must decline with an applicability assessment that records
which preconditions were absent and routes the caller to the nearest
appropriate skill (product-analytics-and-measurement, product-adoption, or
product-lifecycle-learning).

## Product/Relationship Models

This skill defines when customer-success practice applies and what adaptations
are needed for four distinct models. None assumes SaaS.

### 1. B2B Subscription

**Applies fully.** Accounts, renewals, QBRs, expansion tiers, and a dedicated
customer-success team are the canonical fit. All artifacts apply: success plans,
health/risk records, escalation paths, handoff protocols, and closed-loop
feedback.

### 2. Transactional (Non-Subscription)

**Partial application — adapted.** The product may have repeat customers and
account relationships without formal subscriptions. CS adaptations:

- Success plans focus on repeat-purchase patterns and re-order outcomes, not
  subscription renewal dates.
- Health evidence uses purchase frequency, order-value trends, and account
  engagement signals — not MRR or churn metrics.
- QBRs become periodic business reviews triggered by purchase milestones or
  account tier, not calendar dates.
- Escalation triggers on declining purchase frequency or account dormancy.

### 3. Public Service

**Minimal application — routing preferred.** Public-service products often
have citizens or beneficiaries, not "accounts." CS applies only when there
is explicit account-based engagement (e.g., a case-management portal).

- Success plans become service-outcome plans, not commercial plans.
- Health evidence uses service-access equity, completion-rate gaps across
  cohorts, and accessibility barriers — never commercial metrics.
- Escalation routes to program governance, not commercial leadership.
- Privacy boundaries are stricter: citizen data must not be repurposed.
  See [references/privacy-and-human-judgment.md](references/privacy-and-human-judgment.md).

When no account-based engagement exists, **decline** and route to
product-adoption (for service-adoption diagnostics) and
product-analytics-and-measurement (for service-outcome measurement).

### 4. Internal Product

**Conditional — strong routing preference.** Internal products may have
"internal customers" (other teams, business units), but CS applies only
when there is a recurring human relationship with structured engagement.

- Success plans become internal service-level agreements, not commercial plans.
- Health evidence uses internal adoption, workflow-completion, and
  time-saved metrics — never revenue or MRR.
- QBRs become internal service reviews, structured around team outcomes.
- Escalation routes to internal governance, not commercial leadership.

When the internal product has no recurring human relationship (e.g., a
single-team analytics dashboard), **decline** and route to product-adoption
or product-lifecycle-learning.

## Core Artifacts

Every artifact is a decision-support tool, never an automated decision.

### 1. Applicability Decision

Before applying any customer-success method, produce an applicability
assessment. If the product context lacks accounts, renewals, QBRs, or a CS
team, **decline** and route the caller away. Record which preconditions
were absent.

Template: [templates/applicability-decision.md](templates/applicability-decision.md)

### 2. Success Plan

A structured record of the customer's desired outcomes, aligned product
capabilities, measurable milestones, and assigned relationship owner.
Not a sales plan; not a support ticket; not a project plan. The success
plan is the living artifact that connects customer intent to product
evidence.

Template: [templates/success-plan.md](templates/success-plan.md)

### 3. Health / Risk Record

An **evidence-based** record — never an automated score. For each health
dimension, capture:

- The signal (observable evidence, not a proxy metric).
- The source (analytics, adoption, direct observation).
- The trend (direction and recency).
- The confidence (how reliable the evidence is).
- Conflicting signals (surface disagreement, not a forced consensus).

Template: [templates/health-risk-record.md](templates/health-risk-record.md)

### 4. Escalation Path

A defined path from signal to decision-maker, with explicit human-judgment
gates. Every escalation requires a human decision before action. The path
defines:

- The trigger signal and its threshold.
- The escalation owner (named role, not a system).
- The review cadence.
- The decision options (and who makes each).
- The fallback if no decision is reached.

Template: [templates/escalation-and-feedback-closure.md](templates/escalation-and-feedback-closure.md)

### 5. Handoff Protocols

Defined handoffs to product, support, and engineering teams with clear
ownership boundaries:

| Handoff | Trigger | Receiving Team | Artifact |
|---|---|---|---|
| Feature request from customer evidence | Validated pattern across ≥3 accounts | Product | Success-plan extract + health evidence |
| Support escalation | Blocking issue with account impact | Support | Escalation record with account context |
| Technical defect with account risk | Reproducible bug affecting ≥1 account | Engineering | Defect record + account-impact assessment |
| Churn risk requiring lifecycle action | Sustained health decline, 2+ remediation attempts failed | Product-lifecycle-learning | Health/risk record + remediation history |

### 6. Closed-Loop Feedback Closure

The path from customer insight to product change to customer communication:

```
Customer Insight → Validate (pattern? isolated?) →
  Product Decision (build / defer / decline) →
    Implementation → Communication Back to Customer →
      Close Loop (record evidence)
```

Every step is recorded. "Communication Back to Customer" is mandatory —
closing the loop means the customer knows what happened with their feedback.
See [templates/escalation-and-feedback-closure.md](templates/escalation-and-feedback-closure.md).

## Privacy and Human Judgment Boundaries

These boundaries are non-negotiable.

### Customer Feedback Must Not Become Surveillance

- Feedback is collected with consent and a stated purpose.
- Usage is limited to the stated purpose.
- Aggregation is permitted for pattern detection; individual-level
  behavior tracking beyond the stated purpose is not.
- Customer data shared across teams is scoped to the minimum necessary.

### Health Scores Are Decision-Support, Not Automated Decisions

- A health signal is evidence; it never becomes an automated action
  (no auto-churn, no auto-escalation without human review).
- Conflicting signals must be surfaced, not averaged into a single score.
- The health/risk record includes confidence and provenance for every signal.

### Human Judgment Is Required for Escalation Decisions

- Every escalation trigger requires a human decision before any action.
- The escalation path defines who decides, on what evidence, with what
  options.
- A "no decision" state has a defined fallback — escalate further, not
  auto-act.

### Privacy Boundaries Around Customer Data

- Customer-identifiable data is never embedded in templates shared outside
  the CS team.
- Health evidence uses anonymized or aggregated signals when shared across
  teams.
- Data retention and access are governed by the product's privacy policy,
  not the CS practice.

See [references/privacy-and-human-judgment.md](references/privacy-and-human-judgment.md) for the full boundaries reference.

## Routing and Related Skills

This skill routes to specialist skills rather than re-deriving their
methodology. All routing references use relative paths to existing
directories, or prose references for skills not yet landed.

### Routes to (existing skills)

| Skill | What it owns | How this skill consumes it |
|---|---|---|
| [../product-analytics-and-measurement/SKILL.md](../product-analytics-and-measurement/SKILL.md) | Metric trees, tracking plans, instrumentation QA, measurement governance | Provides health evidence and metric definitions for health/risk records |
| [../product-adoption/SKILL.md](../product-adoption/SKILL.md) | Onboarding, activation, behavior change, feature discovery, sustained use | Provides adoption signals (activation, feature adoption, sustained use) as health dimensions |
| [../product-experimentation/SKILL.md](../product-experimentation/SKILL.md) | Experiment design, readout, ship/no-ship decisions | Consumed when CS evidence suggests an experiment (e.g., intervention test for at-risk accounts) |
| [../go-to-market/SKILL.md](../go-to-market/SKILL.md) | Acquisition campaigns, marketing conversion | Does NOT own. CS consumes acquisition context only. |
| [../crm/SKILL.md](../crm/SKILL.md) | HubSpot CRM operations — contact records, deal pipeline views, confirmed deal stage changes | Provides account records and pipeline/health context for health/risk records and QBR preparation |

### Routes to (prose references — skills not yet landed)

| Skill | What it owns | How this skill routes to it |
|---|---|---|
| product-lifecycle-learning | Retirement communication plans, customer treatment during sunset, migration-support coordination, churn-pattern learning across the portfolio | Escalates sustained health decline (2+ remediation attempts failed) for lifecycle action. Routes churn and sunset signals for portfolio-level learning. |

### Does NOT own

- **Statistical inference or experiment design** — belongs to `data-scientist` and `product-experimentation`.
- **Product-analytics instrumentation** — belongs to `product-analytics-and-measurement`.
- **Acquisition, marketing conversion, or campaign design** — belongs to `go-to-market`.
- **Product roadmapping or portfolio prioritization** — belongs to `product-roadmapping-and-portfolio`.
- **Customer support operations or ticket management** — belongs to support-tooling skills.
- **Contract negotiation, pricing, or legal terms** — belongs to `go-to-market` and legal-strategy skills.

## File Map

| File | Purpose | Load when |
|---|---|---|
| [references/discovery-brief.md](references/discovery-brief.md) | Maps existing related content, ownership boundaries, and routing decisions | First load — required context |
| [references/privacy-and-human-judgment.md](references/privacy-and-human-judgment.md) | Full privacy and human-judgment boundaries, surveillance-risk guidance, consent framework | Privacy or judgment question arises |
| [templates/applicability-decision.md](templates/applicability-decision.md) | Structured applicability assessment — decline or proceed with evidence | Customer-success method considered for any product |
| [templates/success-plan.md](templates/success-plan.md) | Customer success plan with desired outcomes, milestones, evidence gates | Building or reviewing a success plan |
| [templates/health-risk-record.md](templates/health-risk-record.md) | Evidence-based health/risk record with signal, source, trend, confidence, and conflicting-signal tracking | Health review, QBR prep, renewal-risk analysis |
| [templates/escalation-and-feedback-closure.md](templates/escalation-and-feedback-closure.md) | Escalation path definition and closed-loop feedback closure record | Escalation design or feedback-loop operation |

## QBR and Engagement Cadence

### Quarterly Business Review (QBR) Structure

A QBR is an evidence review, not a sales presentation. The structure:

1. **Success-plan review** — progress against desired outcomes, milestone
   achievement.
2. **Health evidence** — each dimension, its signal, trend, and confidence.
   Conflicting signals presented, not averaged.
3. **Adoption evidence** — feature adoption, activation trends, sustained-use
   patterns (from product-adoption evidence).
4. **Risk review** — open risks, mitigation status, escalation history.
5. **Forward plan** — next-period success-plan adjustments, expansion
   opportunities (routed to go-to-market for commercial motion), and
   risk-mitigation actions.
6. **Feedback loop status** — open feedback items, product decisions made,
   communication-back status.

### Triggering QBRs Outside B2B Subscription

For non-subscription models, QBRs are triggered by events, not calendar dates:

| Model | QBR Trigger |
|---|---|
| Transactional | Purchase-milestone threshold, account-tier change, or 6-month dormancy |
| Public Service | Service-review cycle, equity-gap detection, or accessibility-audit result |
| Internal Product | Internal service-review cycle, team-reorg, or adoption decline |

## Output Contract

1. An **applicability decision** recorded before any CS method is applied.
2. A **success plan** with desired outcomes, milestones, evidence gates, and
   a named relationship owner.
3. A **health/risk record** with evidence per dimension, not a score.
4. An **escalation path** with explicit human-judgment gates.
5. A **closed-loop record** tracing customer insight → product decision →
   customer communication.
6. **Handoff records** to product, support, or engineering with account
   context and evidence.
