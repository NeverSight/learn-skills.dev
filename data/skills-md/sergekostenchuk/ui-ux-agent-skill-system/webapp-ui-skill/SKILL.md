---
name: webapp-ui-skill
description: Build, refactor, audit, and validate dense web application UI. Use this skill whenever the user asks for SaaS dashboards, admin panels, CRM screens, internal tools, tables, filters, settings flows, data-heavy workflows, empty/loading/error states, responsive app screens, accessibility fixes, or product UI implementation where hierarchy, state coverage, keyboard behavior, and visual verification matter. Do not use for landing pages unless the task is actually an app surface.
---

# Web App UI Skill

Use this specialist for product UI surfaces: dashboards, admin tools, internal workflows, CRM screens, settings, data tables, and state-heavy app screens.

## Operating Modes

- `build`: create or refactor app UI.
- `audit`: review an existing app screen and produce a fix brief.
- `state-coverage`: inspect loading, empty, error, disabled, focus, selected, submitting, and success states.
- `verify`: run available local evidence checks and report gaps.

## Required Workflow

1. Read [references/dashboard-patterns.md](references/dashboard-patterns.md) for product UI layout decisions.
2. Read [references/state-model.md](references/state-model.md) before changing app flows or components.
3. Use [assets/state-matrix.template.md](assets/state-matrix.template.md) and [assets/implementation-report.template.md](assets/implementation-report.template.md) when a stable output artifact is useful.
4. Use `../../shared/privacy-policy.md` before any external service or screenshot handling.
5. Use `../../shared/visual-verification.md` for material UI changes.
6. If source files are available, run [scripts/check_state_coverage.ts](scripts/check_state_coverage.ts) or report why it was skipped.
7. If a URL is available, run [scripts/visual_smoke_test.mjs](scripts/visual_smoke_test.mjs) or report why it was skipped.
8. Return concise implementation notes with `Ran`, `Skipped`, `Planned`, and `Manual`.

## Design Doctrine

- Prioritize scanning, comparison, and repeated action over marketing composition.
- Use compact headings, stable grids, predictable navigation, and explicit state handling.
- Keep cards for repeated items, modals, and genuinely framed tools.
- Do not add decorative hero sections, nested cards, one-note palettes, or viewport-scaled typography.
- Buttons, controls, and tables must have stable dimensions and readable labels.

## Tool Contracts

- State coverage: `node scripts/check_state_coverage.ts --root "$PROJECT_ROOT" --out reports/state-coverage.json`.
- Visual smoke: `node scripts/visual_smoke_test.mjs --url "$URL" --out reports/visual-smoke`.
- Optional cloud generation is never default. It requires explicit approval and a data-transfer note.

## Validation

```bash
python3 $CODEX_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py $CODEX_SKILLS_DIR/webapp-ui-skill
python3 $CODEX_SKILLS_DIR/senior-skill-architect/scripts/lint_production_skill.py $CODEX_SKILLS_DIR/webapp-ui-skill
```

## Output Shape

```text
Surface:
Primary workflow:
State coverage:
Ran:
Skipped:
Manual findings:
Files changed or proposed:
Verification required:
Risks:
```
