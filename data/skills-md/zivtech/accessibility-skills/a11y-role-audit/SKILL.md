---
name: a11y-role-audit
description: "ARRM-based accessibility role audit — responsibility-based review lenses"
compatibility: Codex CLI mirror of .claude/skills/a11y-role-audit/SKILL.md
---

# Accessibility Role Audit (Codex Mirror)

Review a component, page, or design from the responsibility perspective of team roles derived from the W3C WAI ARRM framework.

## Roles

1. **Visual Design** — Contrast, zoom, focus indicators, target sizes, motion
2. **UX Design** — Interaction patterns, focus order, error flows, state communication
3. **Front-End Development** — Semantic HTML, ARIA, keyboard, live regions
4. **Content Authoring** — Alt text, headings, link text, captions, plain language
5. **Business Analysis** — CAPTCHA, time limits, requirements, metrics
6. **Testing** — AT validation, regression, coverage

## Usage

```
Review this component from the visual design role perspective:
[component code or description]
```

## Reference Files

- `roles/README.md` — overview and integration
- `roles/<role-name>.md` — per-role definition with checklist
- `roles/arrm-task-mapping.yaml` — WCAG SC → role mapping

## Output

Each role produces:
- Findings with severity, WCAG citation, evidence, and role ownership
- Blind spot escalations (areas needing other roles)
- Cross-role synthesis when multiple roles reviewed
