---
name: shadcn-audit
description: "Trigger: shadcn audit, enforce shadcn usage, scoped UI audit. Audit React component adoption or full compliance without application changes."
license: Apache-2.0
metadata:
  author: Crystal-Desarrollo
  version: "1.0"
---

## Activation Contract

Audit shadcn usage across a React codebase or a selected section. Treat enforcement as reporting, not editing.

## Hard Rules

- Keep application files and dependencies unchanged. Perform read-only inspection; request permission before commands that write artifacts.
- Preserve behavior and intended appearance in every recommendation. Flag uncertain preservation as requiring design review.
- Report findings only inside the selected scope. Read shared dependencies for context without adding them to scope.
- Inspect every in-scope UI file, including owned primitives. Account for exclusions and blockers; sampling cannot establish completion.
- Respect evidenced project exceptions. Separate confirmed violations, adoption opportunities, and accepted exceptions.
- Use installed implementations and applicable documentation as evidence. Do not impose the newest preset or APIs on older source.

## Decision Gates

| Condition | Action |
| --- | --- |
| No shadcn configuration or verified equivalent | Return only `shadcn is not configured`. Stop. |
| Non-React implementation | Report unsupported framework. Stop. |
| Mode omitted | Use `full`. |
| `component-only` | Apply adoption checks C01–C03 only. |
| `full` | Apply adoption and full-compliance checks. |
| Tools or documentation unavailable | Perform supported checks; mark affected checks unverified. |
| Browser inspection requested | Inspect available UI without submitting forms or changing application state. |

## Execution Steps

1. Load [workflow](references/workflow.md). Resolve configuration, mode, scope, and the complete file inventory. Clarify ambiguous feature boundaries.
2. Load [rules](references/rules.md). Read each inventoried file and trace relevant imports, wrappers, styles, and primitive APIs. Search results are candidates, not completed inspection.
3. Evaluate every applicable rule in the selected mode. Record evidence, exact locations, exceptions, and verification limits. Preserve the inventory when inspection spans batches.
4. Load [report](references/report.md). Reconcile coverage and return its chat tables. Declare incomplete source coverage if any required file or applicable source check remains blocked or unverified.

## Output Contract

Return scope, mode, coverage, findings, exceptions, and verification tables. Include file/line, evidence, rule, severity, and preservation-aware recommendations. Create report files only when explicitly requested. Claim only the checks performed; source completion is not runtime or visual compliance.

## References

- [Workflow](references/workflow.md): discovery, scope, inventory, and tool fallback.
- [Rules](references/rules.md): adoption and full-compliance checks.
- [Report](references/report.md): classification, severity, and table format.
- [Scenarios](assets/scenarios.json): example inputs and expected audit decisions.
