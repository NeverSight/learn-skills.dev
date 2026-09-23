---
name: product-adoption
description: >-
  Diagnose and design product adoption for onboarding, activation, behavior change,
  feature discovery, rollout, and sustained use after launch. Covers consumer, B2B,
  internal-tool, and public-service contexts with evidence-based decision points and
  cohort segmentation. Does not own acquisition campaigns or marketing conversion (routes
  to go-to-market), product-analytics instrumentation (routes to
  product-analytics-and-measurement), or customer-success account management and health
  scoring (routes to conditional-customer-success). Do not use this skill for unrelated
  requests; route to the nearest named specialist.
license: MIT
metadata:
  tags: product-adoption, onboarding, activation, behavior-change, feature-discovery,
    rollout, sustained-use, time-to-value, cohort-segmentation, internal-tools,
    public-services, customer-education, adoption-evidence
---

# Product Adoption

Move people from aware to active, from active to habitual, and from habitual to
evangelical — across consumer, B2B, internal-tool, and public-service contexts.
This skill diagnoses adoption problems and designs adoption plans anchored in
evidence rather than marketing assumptions.

## When to Load

| Trigger | What's Needed |
|---|---|
| Diagnose low activation or time-to-value | `references/adoption-lifecycle-concepts.md` |
| Design an adoption or rollout plan | `templates/adoption-plan.md` |
| Diagnose a specific adoption problem | `templates/activation-time-to-value-diagnostic.md` |
| Segment users into rollout cohorts | `templates/segmentation-and-rollout-record.md` |
| Review sustained use after launch | `templates/sustained-use-review.md` |
| Handle non-SaaS contexts | `references/non-saas-adoption-contexts.md` |
| Design behavior change or education | `references/behavior-change-and-education.md` |

## When Not to Use

This skill does **not** own:

- **Acquisition campaigns, paid marketing, or conversion funnel optimization** — these belong to `go-to-market` (see [../go-to-market/SKILL.md](../go-to-market/SKILL.md)).
- **Product-analytics instrumentation** — belongs to `product-analytics-and-measurement` (prose reference only; skill not yet landed).
- **Customer-success account management, renewal management, or health scoring** — belongs to `conditional-customer-success` (prose reference only; skill not yet landed).

## File Map

| File | Purpose | Load when |
|---|---|---|
| [references/discovery-brief.md](references/discovery-brief.md) | Maps existing GTM/acquisition material, states ownership boundaries | Required context |
| [references/adoption-lifecycle-concepts.md](references/adoption-lifecycle-concepts.md) | Distinguishes acquisition, activation, adoption, retention, expansion | Diagnosing stage confusion |
| [references/non-saas-adoption-contexts.md](references/non-saas-adoption-contexts.md) | Internal-tool, public-service, consumer, and B2B patterns | Non-SaaS product |
| [references/behavior-change-and-education.md](references/behavior-change-and-education.md) | Behavior-change frameworks, in-product education, accessibility-first adoption | Designing onboarding, education |
| [templates/adoption-plan.md](templates/adoption-plan.md) | End-to-end adoption plan with evidence gates | Planning a launch |
| [templates/activation-time-to-value-diagnostic.md](templates/activation-time-to-value-diagnostic.md) | Structured activation diagnostic | Low activation signal |
| [templates/segmentation-and-rollout-record.md](templates/segmentation-and-rollout-record.md) | Cohort segmentation with evidence decision points | Rolling out to cohorts |
| [templates/sustained-use-review.md](templates/sustained-use-review.md) | Post-launch adoption review | Evaluating adoption health |

## Core Methodology

### The Adoption Pipeline (Five Distinct Stages)

```
ACQUISITION → ACTIVATION → ADOPTION → RETENTION → EXPANSION
```

| Stage | Definition | Owned by | This skill's role |
|---|---|---|---|
| **Acquisition** | User arrives at the product | `go-to-market` | Does NOT own. Consumes context. |
| **Activation** | User completes first meaningful outcome ("aha moment") | `product-adoption` | Owns. |
| **Adoption** | User forms a habit; product becomes regular workflow | `product-adoption` | Owns. |
| **Retention** | User stays and returns over time | Shared with `product-lifecycle-learning` | Consumes retention signals. |
| **Expansion** | User deepens engagement | `product-adoption` (feature-discovery) + `conditional-customer-success` (account-side) | Owns feature-discovery. |

### Evidence-Based Decision Points

| Decision | Evidence Signal | Rule |
|---|---|---|
| **Proceed** | Activation rate >= threshold, all cohorts | Green-light expansion |
| **Pause** | Activation rate < threshold in any cohort, or negative trend | Halt, diagnose, narrow |
| **Stop** | Sustained below-threshold, 2+ remediation attempts failed | Stop, route to lifecycle-learning |
| **Accelerate** | Activation > 2x threshold, sustained 2+ cycles | Increase cohort size |
| **Redesign onboarding** | Drop-off > 50% in first-run or TTV > 2x target | Redesign, re-test small cohort |

### Non-SaaS Support

Explicitly supports: internal tools, public services, consumer (non-subscription), B2B (non-SaaS).
Does not assume NPS, conversion rates, or MRR benchmarks are universal.
See [references/non-saas-adoption-contexts.md](references/non-saas-adoption-contexts.md).

### Connecting Adoption Evidence

- **Product analytics and measurement** — Consumes adoption evidence. `product-analytics-and-measurement` (prose) defines instrumentation.
- **Customer success** — Informs success playbooks. `conditional-customer-success` (prose) owns account-level response.
- **Lifecycle learning** — Sustained-use reviews feed `product-lifecycle-learning` (prose).
- **Product roadmapping and portfolio** — Pause/stop decisions feed `product-roadmapping-and-portfolio` (prose).

## Output Contract

1. Completed diagnostic or plan from relevant template
2. Evidence-gate decisions with cohort breakdowns
3. Explicit statement of which adoption stage(s) in scope and delegated

## Related Skills

- [../go-to-market/SKILL.md](../go-to-market/SKILL.md) — Owns acquisition, PLG metrics.
- `product-analytics-and-measurement` — Owns instrumentation (prose reference).
- `conditional-customer-success` — Owns account-level intervention (prose reference).
- `product-lifecycle-learning` — Receives sustained-use review records (prose reference).
- `product-roadmapping-and-portfolio` — Receives pause/stop evidence (prose reference).
