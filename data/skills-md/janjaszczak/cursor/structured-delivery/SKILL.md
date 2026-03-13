---
name: structured-delivery
description: Provide structured outputs (plan/report/checklist/table) optimized for readability and reuse. Use when user requests a plan, report, checklist, template, or when high-risk requires explicit verification steps.
compatibility: None.
metadata:
  intent: Default answers remain concise; structure only on request or risk.
---

# structured-delivery

## Activation gate (anti-noise)
Activate if:
- The user asks for plan/raport/checklista/tabela/template.
- Or high-risk-review is active.

Skip if:
- Simple Q&A where brevity is desired.

## Output formats (choose one)
- Plan: Objective → Steps → Verify
- Report: Findings → Evidence → Recommendation → Next steps
- Checklist: grouped by phase
- Table: exportable (CSV-like) when helpful
