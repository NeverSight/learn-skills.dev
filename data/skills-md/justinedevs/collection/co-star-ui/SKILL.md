---
name: co-star-ui
description: "CO-STAR UI Creator for React/Next.js: structured prompting to build or integrate UI (components, pages, design systems) or to create custom CO-STAR prompts. Use when the user wants to add hero sections, dashboards, design tokens, shadcn/Magic UI/Aceternity integration, Newsprint design system, or to draft their own CO-STAR prompt (Context, Objective, Style, Tone, Audience, Response). Always run discovery questions first, then plan, then implementation."
license: See repository LICENSE
---

# CO STAR UI Skill

Structured CO-STAR prompting for UI work: **Context, Objective, Style, Tone, Audience, Response**. The skill supports two modes and requires choosing one before proceeding.

---

## Decision: Which Mode to Use

| If the user wants to… | Use | Action |
|----------------------|-----|--------|
| **Build or change UI** — components, pages, design system, shadcn/Magic UI/Aceternity, refactors, hero/dashboard/landing | **UI build mode** | Follow [references/co-star-prompt.md](references/co-star-prompt.md). Discovery questions first, then integration plan and code. |
| **Create a custom CO-STAR prompt** — their own prompt, design system doc, or CO-STAR template from scratch | **Prompt creator mode** | Follow [references/co-star-creator.md](references/co-star-creator.md). Guide them through Context, Objective, Style, Tone, Audience, Response. |
| **Unclear or mixed** | **Weigh main ask.** Implementation → prompt first; "create my prompt" → creator first. |

**Signals for UI build:** build, implement, add, refactor, component, page, design system, shadcn, Tailwind, React, Next.js, hero, dashboard, landing, integrate.

**Signals for prompt creator:** create my prompt, custom prompt, my own CO STAR, design system doc, template for our product.

---

## Non-Negotiable Pre-Actions

1. **Locate** the correct resource (co-star-prompt vs co-star-creator) from the decision table above.
2. **Do not** suggest code or libraries until you have run **scoped discovery questions** (tech stack, existing UI lib, design direction, target page/feature). Keep to 5–10 questions.
3. **After** answers, respond with: integration strategy, token/primitive definitions, component patterns, negative constraints (anti-patterns), and a **critique loop** (2–4 risks, one small first slice, and "which component or page first?").

---

## Flow (UI Build Mode)

1. **Scoped questions first** — Framework, styling, existing tokens/components, constraints, goal (re-skin vs new theme vs one page).
2. **Integration strategy** — Which base (e.g. shadcn + Radix), which registries (Tailark, Magic UI, Aceternity), which animation (React Bits, Anime.js) if any. Keep the set minimal.
3. **Concrete plan** — Tokens, core components, then marketing/dashboard layers. Code sketches in the user’s stack (Tailwind, CSS modules, etc.).
4. **Negative constraints** — No multiple full UI suites, no mixing incompatible design languages, no heavy animation everywhere. Normalize tokens when copy-pasting.
5. **Critique loop** — List trade-offs, suggest one small first slice, ask what to tackle first.

---

## Flow (Prompt Creator Mode)

1. Guide the user through **Context** (existing codebase, stack, target design system).
2. Then **Objective** (mental model, minimal abstractions, migration plan, implementation guidance, critique).
3. Then **Style**, **Tone**, **Audience**, **Response format** (two phases: scoped questions first, then implementation plan + code sketches).
4. Include **negative constraints** and **edge cases** in the resulting prompt.

---

## Resources

- **references/co-star-prompt.md** — Full CO-STAR prompt for building/integrating UI (modern React ecosystem, registries, copy-paste vs npm). Read when the user is in UI build mode.
- **references/co-star-creator.md** — Full CO-STAR prompt for Newsprint UI Creator (design system integration, tokens, primitives). Use for prompt-creator mode or for Newsprint-specific builds.
