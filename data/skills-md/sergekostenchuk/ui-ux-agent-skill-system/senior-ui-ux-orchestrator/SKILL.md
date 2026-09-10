---
name: senior-ui-ux-orchestrator
description: Main senior UI/UX orchestration skill. Use this skill whenever the user asks to build, refactor, audit, critique, plan, or validate web app UI, SaaS dashboards, internal tools, landing pages, product pages, screenshots, Figma designs, Figma MCP workflows, design-to-code, code-to-canvas, design-system sync, Stitch/AI UI exploration, three-direction design exploration, cursor reveal effects, responsive behavior, accessibility, visual quality, senior UI/UX/SEO/LLM council decisions, wiki context gates, or UI skill-system workflows. Routes work to webapp-ui-skill, marketing-site-skill, ux-audit-skill, design-critic-skill, ui-ux-pro-max, stitch-design-bridge, senior-figma-orchestrator, cursor-reveal-hero, image-layer-alignment-validator, task-plan-v2-orchestrator, obsidian-wiki-ingest, and shared validation tools while enforcing local-first privacy, one central chair, no fake tools, evidence reporting, and visual verification.
---

# Senior UI/UX Orchestrator

This is the main entrypoint for the UI/UX skill group. Classify the user request first, choose the smallest specialist set that can solve it, enforce privacy/evidence rules, and return a concise implementation or audit handoff.

## Operating Modes

- `route`: choose one or more specialist skills.
- `plan`: create or update a UI/UX skill-system plan.
- `build-webapp`: route product UI work to `webapp-ui-skill`.
- `build-marketing`: route public page work to `marketing-site-skill`.
- `audit`: route evidence-backed review to `ux-audit-skill`.
- `critique`: route visual quality review to `design-critic-skill`.
- `figma`: route Figma context, MCP, canvas, asset, effect, and design-system work to `senior-figma-orchestrator`.
- `design-intelligence`: route style, pattern, typography, color, and UI precedent research to `ui-ux-pro-max`.
- `stitch`: route Stitch or AI UI exploration to `stitch-design-bridge` after UX/product and design-intelligence constraints exist.
- `three-variant-design`: coordinate exactly three distinct design directions before Stitch, Figma, or code execution.
- `council`: convene a senior UI/UX/SEO/LLM/Figma/implementation council when cross-skill recommendations conflict.
- `wiki-context`: capture large-project context into the Obsidian/LLM wiki after decisions, without secrets.
- `interactive-effect`: route cursor/mask/reveal frontend effects to `cursor-reveal-hero`.
- `image-alignment`: route base/reveal image suitability checks to `image-layer-alignment-validator`.
- `verify`: check reports, commands, artifacts, and fake-evidence risk.

## Required Workflow

1. Read [references/routing-decision-framework.md](references/routing-decision-framework.md).
2. If the request is large, cross-domain, asks for three variants, uses Stitch, or contains conflicting UI/UX/SEO/Figma/code recommendations, read [references/cross-skill-council-contract.md](references/cross-skill-council-contract.md).
3. If the request is ambiguous, use [assets/intake-questions.md](assets/intake-questions.md) and ask only blocking questions.
4. If deterministic classification helps, run [scripts/classify_product_type.py](scripts/classify_product_type.py) on the prompt and write `reports/intake.json`.
5. Apply the shared privacy policy from `../../shared/privacy-policy.md`.
6. Route to the relevant specialist skill and state why.
7. For Stitch workflows, require product/UX, SEO/LLM if public, and `ui-ux-pro-max` constraints before creating Stitch prompts.
8. For large multi-session projects, add a wiki context gate after major decisions and before final handoff; never store API keys, tokens, private screenshots, or `.env` data.
9. Require evidence according to `../../shared/reporting-contract.md`.
10. For material UI changes, require visual verification or record why it was skipped.

## Routing Defaults

- SaaS, dashboard, admin, CRM, internal tool, data-heavy product flow: `webapp-ui-skill`.
- Landing page, product page, brand page, venue page, campaign, conversion page: `marketing-site-skill`.
- Existing URL, screenshot, Figma frame, source-code audit, regression check: `ux-audit-skill`.
- Visual hierarchy, taste, polish, anti-slop critique: `design-critic-skill`.
- Design intelligence, visual precedent, style candidates, color/typography/pattern signals: `ui-ux-pro-max`.
- Three clearly different design directions: `senior-ui-ux-orchestrator` chairs `three-variant-design`, with `ui-ux-pro-max` as input and `stitch-design-bridge` as downstream renderer.
- Stitch, Google Stitch, AI-generated UI variants, Stitch prompts, Stitch output review: `stitch-design-bridge`.
- Cross-skill conflict, senior council, UX vs SEO vs Figma vs code tradeoff: this orchestrator in `council` mode.
- Large project memory, multi-session context, project knowledge capture: `obsidian-wiki-ingest` or wiki layer after decisions are made and sanitized.
- Figma file/frame/node, Figma MCP, variables, components, Code Connect, code-to-canvas, canvas edits, assets, effects: `senior-figma-orchestrator`.
- Cursor trail, hover reveal, mouse trail, masking, canvas base/reveal compositing: `cursor-reveal-hero`.
- Two-layer image comparison, base/reveal drift, before/after alignment: `image-layer-alignment-validator`.
- Skill package creation, validation, evals, trigger tuning: use this orchestrator with `senior-skill-architect` guidance when available.

## Safety And Evidence Rules

- Default to `local-first`.
- Optional cloud tools require explicit user approval and a data-transfer note.
- Do not send private code, screenshots, Figma frames, cookies, tokens, `.env`, customer data, or internal URLs externally without approval.
- Never claim a validator, screenshot, browser, Lighthouse, axe, or eval check ran unless the command ran and artifacts exist.
- Label outcomes as `Ran`, `Skipped`, `Planned`, or `Manual`.
- Keep `senior-ui-ux-orchestrator` as the single chair. Specialist skills advise or execute inside their domains; they do not override the chair's final cross-domain decision.
- Treat `ui-ux-pro-max` and Stitch outputs as candidate evidence and exploration inputs, not final authority.
- Council decisions are not majority votes. Apply the decision order in [references/cross-skill-council-contract.md](references/cross-skill-council-contract.md), and record accepted tradeoffs.

## Validation

When editing this skill, run:

```bash
python3 $CODEX_SKILLS_DIR/.system/skill-creator/scripts/quick_validate.py $CODEX_SKILLS_DIR/senior-ui-ux-orchestrator
python3 $CODEX_SKILLS_DIR/senior-skill-architect/scripts/lint_production_skill.py $CODEX_SKILLS_DIR/senior-ui-ux-orchestrator
python3 -m json.tool $CODEX_SKILLS_DIR/senior-ui-ux-orchestrator/assets/routing-rules.json >/dev/null
```

## Final Handoff Shape

```text
Mode:
Chosen skill(s):
Reason:
Required evidence:
Privacy mode:
Skipped or planned checks:
Risks:
Next action:
```
