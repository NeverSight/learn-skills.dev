---
name: design-critic-skill
description: Critique UI visual quality with observable design criteria. Use this skill whenever the user asks for visual critique, design review, polish, hierarchy, spacing, typography, contrast risk, consistency, brand fit, anti-slop review, screenshot critique, Figma frame critique, or a fix brief for a weak interface. Keep findings actionable and evidence-labeled. Do not require Attention Insight, Khroma, or external screenshot upload for normal local critique.
---

# Design Critic Skill

Use this specialist when the main need is visual quality judgment and actionable polish, not full implementation or automated audit.

## Operating Modes

- `screenshot-critique`: review a screenshot or image.
- `figma-critique`: review a provided Figma frame/context.
- `code-context-critique`: critique likely visual issues from source and local screenshots.
- `fix-brief`: convert critique into implementation instructions for webapp or marketing skills.

## Required Workflow

1. Read [references/hierarchy-rubric.md](references/hierarchy-rubric.md).
2. Read [references/anti-slop-patterns.md](references/anti-slop-patterns.md) before calling a design "polished".
3. Use [references/taste-constraints.md](references/taste-constraints.md) to keep critique observable.
4. Apply `../../shared/privacy-policy.md` before Figma/screenshots/external tools.
5. Use [assets/critique-report.template.md](assets/critique-report.template.md) for structured output.
6. Mark evidence type: screenshot, Figma, source, browser, or `Manual`.

## Critique Rules

- Findings must map to observable issues: hierarchy, grouping, scan path, contrast risk, spacing, type scale, affordance, consistency, content density, or action priority.
- Avoid vague taste claims without fix direction.
- Do not invent accessibility, DOM, performance, or analytics evidence.
- Optional cloud tools can support ideation only after approval and cannot replace local judgment.

## Validation

```bash
python3 $CODEX_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py $CODEX_SKILLS_DIR/design-critic-skill
python3 $CODEX_SKILLS_DIR/senior-skill-architect/scripts/lint_production_skill.py $CODEX_SKILLS_DIR/design-critic-skill
```

## Output Shape

```text
Input:
Evidence type:
Top findings:
Fix brief:
What not to change:
Verification:
Privacy notes:
```
