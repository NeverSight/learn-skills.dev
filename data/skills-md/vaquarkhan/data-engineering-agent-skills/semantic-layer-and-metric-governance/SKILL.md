---
name: semantic-layer-and-metric-governance
description: Guides agents through semantic layer and shared metric design. Use when defining business metrics, reusable dimensions, governed metric contracts, or shared semantic models consumed by dashboards, analytics tools, or other teams.
---

# Semantic Layer And Metric Governance

## Overview

Use this skill when the challenge is consistency of meaning, not just correctness of rows. It helps agents define shared metrics and dimensions so teams stop rebuilding conflicting logic in every downstream tool.

## When to Use

- defining or changing business metrics
- introducing a semantic or metric layer
- standardizing dimensions and filters across teams
- governing high-value shared KPIs

Do not rely on ad hoc BI formulas when a metric needs cross-team trust.

## Workflow

1. Define the metric contract.
   Include:
   - owner
   - exact business meaning
   - grain
   - numerator and denominator logic
   - filters and exclusions

2. Standardize shared dimensions and time logic.

3. Map consumers and expected use cases.
   A metric used in finance, product, and operations may need stronger governance than a local team report.

4. Keep metric logic centralized where possible.

5. Version or migrate breaking metric changes deliberately.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "Everyone already knows what revenue means." | Teams often carry different assumptions about refunds, timing, and exclusions. |
| "The BI layer can handle this locally." | Local formulas multiply inconsistency and make audits harder. |
| "Minor metric changes do not need change management." | Even small definition shifts can invalidate trend lines and stakeholder trust. |

## Red Flags

- no named metric owner
- filters and exclusions are implicit
- the same KPI exists in multiple incompatible forms
- definition changes are shipped without communication

## Verification

- [ ] Metric ownership and business meaning are explicit
- [ ] Shared dimensions and filters are standardized
- [ ] Consumer impact is considered for metric changes
- [ ] Breaking definition changes have a migration or communication path
