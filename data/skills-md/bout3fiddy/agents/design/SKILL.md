---
name: design
description: Frontend design curation skill for UI critique, motion storyboarding, and DialKit tuning. Use when the user asks for interface feedback, animation sequencing, or interactive design-control setup.
---

# Design (Curated Frontend Design Skill)

Use this skill for design-focused frontend tasks without routing into `coding`.

## Operating rules
- Keep responses design-first: clarity, hierarchy, interaction quality, and user context.
- Use progressive disclosure: open only the reference module needed for the active request.
- If a task mixes critique and implementation, start with critique, then provide concrete implementation guidance.
- Prefer actionable outputs: prioritized issues, concrete edits, and copy-paste-ready snippets when requested.
- If the request is ambiguous across modules, ask one brief clarifying question.

## Workflow
1) Detect the lane: critique, animation storyboarding, or DialKit tuning.
2) Open the matching reference file and follow that workflow.
3) Produce structured output with concrete observations and next actions.
4) For follow-up requests, switch modules only if user intent changes.

## Reference triggers (open when clearly relevant)
- UI critique/review/feedback/audit/polish/refine/redesign -> `skills/design/references/design-critique.md`
- Animation/storyboard/motion/transition/entrance/timing/stagger/spring -> `skills/design/references/storyboard-animation.md`
- DialKit/sliders/controls/tuning panel/live params -> `skills/design/references/dialkit.md`

## References
- `skills/design/references/index.md` - References index for this skill
- `skills/design/references/design-critique.md` - Structured UI critique workflow and output format
- `skills/design/references/storyboard-animation.md` - Stage-driven animation authoring/refactor pattern
- `skills/design/references/dialkit.md` - DialKit control-generation workflow and defaults
