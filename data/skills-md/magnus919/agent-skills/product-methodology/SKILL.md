---
name: product-methodology
description: >-
  Translate validated product evidence into tactical backlog decisions, prioritization,
  specifications, and stakeholder communications. Do not use this skill for CPO-level
  vision, positioning, or market strategy; use `product-strategy` for strategic direction.
license: MIT
metadata:
  source_repo: https://github.com/magnus919/hermes-profiles
  source_commit: 867a555
---

# Product Methodology

This skill begins where discovery ends. When you have validated evidence from stakeholder conversations, competitive research, or usage data, it guides you through prioritization, decision-making, specification, and communication.

## Pipeline

```
VALIDATED EVIDENCE → [PRIORITIZE] → [DECIDE] → [SPECIFY] → [COMMUNICATE]
                         |              |           |              |
                    RICE + MoSCoW   Decision log   Spec        Stakeholder
                                     template    template       briefs
```

## Reference Guide

Load only the reference relevant to the task:

| Reference | Load when |
|---|---|
| [RICE scoring](references/rice-framework.md) | You need to compare unrelated feature proposals by Reach × Impact × Confidence / Effort |
| [MoSCoW prioritization](references/moscow-prioritization.md) | Scope is tight for a time-boxed release and you need crisp Must/Should/Could/Won't boundaries |
| [Opportunity solution trees](references/opportunity-solution-trees.md) | The problem space is messy and you need to connect customer needs to build decisions without jumping to solutions |
| [Decision log](references/decision-log.md) | You've made a decision with tradeoffs that will be questioned later — log the context and expected outcome |
| [Spec template](references/spec-template.md) | You need a requirements document that engineers, designers, and stakeholders can all work from |
| [Stakeholder communication](references/stakeholder-communication.md) | You're preparing a message for execs, engineers, designers, or customers — each audience needs a different format |
| [Source index](references/source-index.md) | Reviewing provenance, porting scope, and authoritative source links |

## Templates

| Template | Load when |
|---|---|
| [Decision log template](templates/DECISION_LOG.md) | You need a fillable decision log entry with frontmatter |
| [Spec template](templates/SPEC.md) | You need a fillable spec document with the sections provided by this methodology |

## Trigger Conditions

Load this skill when:

- Prioritizing a backlog of feature proposals or initiatives
- Making a product decision that needs a documented rationale
- Writing a specification for a feature or integration
- Communicating a product decision to different audiences (executives, engineers, designers, customers)
- Mapping customer opportunities to potential solutions
- Scoping a time-boxed release with clear boundaries
- A stakeholder asks "why did we decide this?" and there's no record

## When Not to Use

- **Stakeholder discovery and interviews** — load `product-discovery` first. This skill starts from validated evidence, not raw stakeholder conversations.
- **Shaping an unbounded idea into a bet** (appetite, pitch, circuit breaker) — load [product-shaping](../product-shaping/SKILL.md) before prioritization frameworks apply; this skill consumes a won bet, it does not create one.
- **Interaction design, task flows, state/recovery models, or usability-study planning** — use [product-design-and-ux](../product-design-and-ux/SKILL.md) after this skill has chosen scope. This skill decides what to build and why; design-and-ux defines user-facing behavior.

## Working Method

1. Confirm you have validated evidence (interview notes, usage data, competitive analysis). If not, route to `product-discovery`. If the validated problem has no appetite or bounded solution yet, shape it via `product-shaping` first — do not pre-shred a pitch into tasks before its bet is placed.
2. Prioritize with RICE when comparing unrelated proposals; use MoSCoW when scoping a time-boxed delivery.
3. Log decisions as structured records with context, options, rationale, and expected outcomes.
4. Write specs that define the problem, success metrics, scope boundaries, open questions, and edge cases.
5. Communicate decisions in the format each audience needs — recommendation-first for executives, context-first for engineers, listening-first for customers.

## Routing Boundary

Use `product-strategy` for CPO-level vision, positioning, market strategy, and portfolio direction. Route tactical prioritization, specifications, decision logs, and backlog sequencing back here once strategic direction and validated evidence are available; do not make portfolio strategy decisions in this skill.

## Portability

This skill is intentionally host-neutral. It requires no profile system, output format, scripts, or external services. Load references directly by path — use the host agent's normal file-loading mechanism.

## Provenance

| Framework | Origin | Source |
|---|---|---|
| RICE | Intercom (Sean McBride, 2016) | [intercom.com/blog/rice-simple-prioritization-for-product-managers](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) |
| MoSCoW | Dai Clegg, Oracle UK (1994); later adopted by DSDM | [Agile Business Consortium: MoSCoW prioritisation](https://www.agilebusiness.org/dsdm-project-framework/moscow-prioritisation.html) |
| Opportunity Solution Trees | Teresa Torres (Product Talk) | [producttalk.org/opportunity-solution-tree](https://www.producttalk.org/opportunity-solution-tree/) |
| Decision log | Synthesized from ADR practice and product management conventions | — |
| Spec template | Synthesized from common PRD practice | — |
| Stakeholder communication | Synthesized from product management communication practice | — |

This skill was ported from [`magnus919/hermes-profiles`](https://github.com/magnus919/hermes-profiles) at commit [`867a555`](https://github.com/magnus919/hermes-profiles/commit/867a555). See [`references/source-index.md`](references/source-index.md) for the portability boundary.
