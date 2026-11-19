---
name: ux-audit-skill
description: Audit existing UI screens, URLs, screenshots, Figma frames, HTML/CSS/React code, dashboards, mobile flows, and landing pages for UX, accessibility, responsive behavior, visual hierarchy, conversion blockers, state coverage, and regression risk. Use this skill whenever the user asks for a UI/UX review, severity matrix, evidence-backed findings, before/after check, or actionable refactor brief. Never claim DOM, Lighthouse, axe, or screenshot evidence unless it exists.
---

# UX Audit Skill

Use this specialist for evidence-backed review of existing UI artifacts. The output is a severity matrix and actionable refactor brief, not a generic design essay.

## Operating Modes

- `review-live-url`: audit a reachable URL with available browser/static evidence.
- `review-screenshot`: audit image-only context without DOM claims.
- `review-code`: audit source files and templates.
- `refactor-brief`: convert findings into implementation tasks for another skill.
- `regression-check`: compare before/after evidence and remaining risks.

## Required Workflow

1. Classify available evidence using [references/audit-evidence-model.md](references/audit-evidence-model.md).
2. Apply [references/severity-model.md](references/severity-model.md) before ranking findings.
3. Use [assets/audit-report.template.md](assets/audit-report.template.md) for audit output.
4. Use [assets/regression-report.template.md](assets/regression-report.template.md) for before/after checks.
5. Apply `../../shared/privacy-policy.md` before screenshots, Figma, or authenticated state.
6. If a URL is available, reuse local scripts listed in `../../shared/tool_inventory.json`.
7. Label every finding by evidence type: `DOM`, `screenshot`, `source`, `automated`, or `Manual`.

## Evidence Boundaries

- Screenshot-only input cannot support DOM, Lighthouse, axe, or runtime claims.
- Source-only input cannot prove rendered layout unless run or screenshot evidence exists.
- Manual findings are allowed but must be labeled `Manual`.
- Planned tools are not evidence.

## Validation

```bash
python3 $CODEX_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py $CODEX_SKILLS_DIR/ux-audit-skill
python3 $CODEX_SKILLS_DIR/senior-skill-architect/scripts/lint_production_skill.py $CODEX_SKILLS_DIR/ux-audit-skill
```

## Output Shape

```text
Audit target:
Evidence available:
Ran:
Skipped:
Severity matrix:
Top fixes:
Verification plan:
Privacy notes:
Residual risk:
```
