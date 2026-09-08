---
name: ui-ux
description: "Use as the UI/UX quality gate for frontend work that materially affects web product surfaces: design/build/redesign/review/polish/refactor pages or component systems, screenshot/UX critiques, rescue of GPT/Codex-looking UI, stack or UI-foundation choices, shadcn/Tailwind/table/form patterns, loading/empty/error/mobile/accessibility states, or installing frontend governance docs such as DESIGN.md, FRONTEND_CONTRACT.md, PAGE_BRIEF.md, and visual QA norms. Trigger lightly for small UI-sensitive tweaks using the Tiny change gate. Coordinate with visual implementation skills when asked to build a polished interface; this skill supplies product cognition, UX judgment, guardrails, and verification. Skip for pure backend/API/data/model changes, tests with no UI surface, mechanical renames, dependency chores, or edits that do not affect layout, interaction, copy, visual behavior, accessibility, or frontend rules."
---

# UI/UX Quality

This skill turns Codex from a free-form UI generator into a frontend design-and-development agent. It must understand the project first, recommend suitable choices, and create enforceable project-level norms during implementation.

## Core stance

Frontend quality is not a fixed style guide or a pile of rules. Good frontend work requires project cognition, task-flow judgment, product temperament, page-type judgment, human-language copy, component reuse, visual verification, and iterative polishing.

Do not constrain the agent's creative range by banning colors, gradients, density, unusual layouts, or expressive visual direction by default. Creative freedom is welcome when it fits the product. But every frontend surface has a baseline craft floor: alignment, spacing rhythm, hierarchy, semantic grouping, state clarity, and target/action proximity must be coherent before visual experimentation counts as polish.

The goal is not "avoid shadcn" or "ban gradients." The real goal is:

```
raw GPT output → stable component baseline → project-specific product UI → polished, unified frontend
```

Do not optimize only the visible screen. Optimize the user's journey: entry → decision → action → feedback → recovery → completion.

Think of this as:

```text
freedom in style, discipline in structure
```

## Non-negotiable first step: project cognition

Before writing or changing frontend code, answer briefly:

```text
Project in human words:
Core users:
Core business objects:
Current page/surface type:
Primary user task:
Entry point / previous step:
First decision user must make:
Success criterion:
Recovery path:
Mobile primary action:
Product temperament:
User-facing vocabulary:
Internal terms that should not appear in main UI:
Known frontend risks:
```

If you cannot answer these from the existing code, docs, or screenshots, investigate first. Do not start implementation on an unknown project.

## Trigger tiers

Use the smallest tier that fits the request:

- **Full** — page creation, redesign, UI review, visual polish, component-system work, stack/library choice, screenshot critique, rescue/refactor, or project governance.
- **Light** — a small UI-sensitive tweak that can affect layout, copy, visual hierarchy, accessibility, or interaction. Use only the Tiny change gate from `references/workflow.md`.
- **Skip** — purely backend/API/data/model work, tests with no UI surface, mechanical renames, dependency chores, or code edits with no user-visible frontend effect.

## Adjacent skill boundaries

Use this skill as the product-cognition, UX-judgment, frontend-governance, and verification layer. It does not replace more specialized build or visual skills.

- If a task asks for a high-fidelity web page, polished visual implementation, or prototype, apply this skill's cognition gate first, then coordinate with the relevant frontend or product-design implementation skill when available.
- If a task is specifically about shadcn component installation, registry usage, or component API wiring, use the shadcn-specific guidance after the UX gate when the change is user-visible.
- If a product-design workflow has its own mandatory design-brief gate, satisfy that gate too; do not duplicate the same questions at length.
- If there is no user-visible frontend impact, skip this skill even if the repository is a frontend repository.

## Repository instructions and AGENTS.md

Before changing a project's frontend, read repository-level agent instructions when they exist, such as `AGENTS.md`, `CLAUDE.md`, or `CODEX.md`. Treat those files as operating constraints.

Do not rewrite `AGENTS.md` for ordinary frontend tasks. Keep detailed design rules in project docs such as `docs/frontend/DESIGN.md` and `docs/frontend/FRONTEND_CONTRACT.md`.

When the user asks to install or codify frontend governance for a repository:

1. Copy or update the frontend governance docs first.
2. Add only a short pointer in `AGENTS.md` telling future agents which frontend docs to read before broad UI changes.
3. Do not duplicate long checklists, product strategy, screenshots, or secrets in `AGENTS.md`.
4. If `AGENTS.md` already points to an equivalent project rule file, update that file instead of adding another rule block.

## Frontend Thinking Gate

Output this before every substantive frontend task:

```text
Project stage:       new / half-built / finished / rescue
Surface type:        marketing / docs / API console / admin / ops workbench /
                     CRUD list / object detail / setup wizard / mobile task / other
Primary user task:
Entry / journey:
First decision:
Information priority:
Friction / recovery:
Mobile primary action:
Recommended UI foundation:
Reference design systems:
What must not appear on screen:
Key anti-pattern risks:
Baseline craft risks:
Verification plan:
```

Keep it short. This is a thinking checkpoint, not a planning essay.

## Project-stage modes

### 1. New project — recommend, preview, choose

Recommend proactively; the user may not know frontend tradeoffs.

- App framework: Next.js, Vite/React, Remix, Astro, etc.
- UI foundation: shadcn registry, Radix/Base UI/React Aria/Ark UI, Ant/MUI/Mantine/Chakra/HeroUI, or custom.
- Data/UI engines: TanStack Query, TanStack Table, charts, form libraries.
- Design reference pack: 2–4 systems that match the product temperament.
- Verification: Storybook, Playwright screenshots, accessibility checks.
- First-page patterns and prototype approach.

Give options with tradeoffs, not a single dogma. See `references/tool-selection.md`.

### 2. Half-built project — assess before refactor

Do not automatically rewrite. Assess first:

```text
Keep:
Replace:
Refactor depth:    polish / local page / component-layer / page-IA restart
Risks of continuing current UI:
Risks of rebuilding:
Smallest useful next step:
```

### 3. Finished project — polish and unify

Avoid architecture churn. Focus on:

- Visual hierarchy and copy clarity.
- Task success, decision clarity, and recovery paths.
- Status and error translation.
- Loading / empty / error / long-text states.
- Dangerous-operation safety.
- Responsive and mobile task layout.
- Component consistency and screenshot regression.

### 4. Rescue — AI output already degraded

When existing UI shows clear GPT/Codex flavor, diagnose before patching:

1. Run the anti-pattern self-check (`references/anti-patterns.md`).
2. Run the UX evaluation checklist (`references/ux-evaluation.md`).
3. Identify which failure modes are present.
4. Classify: cosmetic fix / page-level refactor / component-layer refactor / restart.
5. Fix the deepest root cause first — patching symptoms on a structurally wrong flow wastes effort.

## Human-language cognition

Translate all project and UI copy into words users understand. Do not paste README, architecture, protocol, or internal terms onto operational pages.

Separate what the agent needs to know from what the user needs to act on:

```text
Agent context / implementation understanding → keep in code, docs, comments, tooltips, diagnostics, or project governance.
User task / current state / next action      → show in the primary UI.
```

Do not let the interface narrate itself. This is a placement and intent test, not a string blacklist:

- A phrase is acceptable when it directly helps the current user decide, act, or recover on this surface.
- The same phrase is a problem when it is prominent primary UI copy that explains the agent's design intent, implementation contract, or component semantics.
- Developer tools and API consoles may expose protocol names, JSON, and diagnostic language when those are part of the user's task; keep them secondary to the current result and next action unless the page is explicitly a raw diagnostic view.

Examples below illustrate a failure pattern. They are not forbidden literal strings:

```text
"This panel is only for diagnostics."
"JSON is not the main operation entry."
"This page validates the search → resources → resolve protocol."
```

Turn those into user-facing state and action copy instead:

```text
"搜索已完成，未找到匹配资源。"
"换一个关键词，或切换书源后再试。"
"原始响应"
```

Use this hierarchy:

1. **Human-facing conclusion** — what happened and what to do.
2. **Operational detail** — enough for an admin or operator.
3. **Technical diagnostics** — error codes, IDs, raw JSON; place in expandable details, developer mode, or raw inspectors.

```
First human words, then terminology.
First conclusion, then detail.
First action, then raw data.
```

Developer-focused pages may surface more technical terms, but hierarchy still applies.

If the product's primary user language is known, use that language for primary UI labels, states, and actions. API names, protocol steps, JSON fields, and internal object names may appear as secondary labels, badges, tooltips, or raw diagnostic content — not as the dominant interface language.

## Product temperament before style

Choose style by product intent, not by default library aesthetics:

| Temperament | Characteristics |
|---|---|
| AI-native / creative | Futuristic, fluid, expressive; avoid generic purple-glass AI clichés |
| Developer tool / API console | Compact, precise, trustworthy, code-friendly; no hero on tool pages |
| Enterprise ops / diagnostics | Dense, reliable, state-first, safe |
| Commerce / licensing / billing | Calm, precise, high-trust, auditable |
| Content ops / library / CMS | Readable, searchable, workflow-oriented, warmer |
| Marketing / landing | Expressive, conversion-oriented; more visual freedom |

## Tool and component selection

Use tools for fit, not fashion. See `references/tool-selection.md` for full guidance.

Quick stance:

- **shadcn/ui**: strong safety baseline, project-owned components. Mature it into project-specific components; do not treat default shadcn look as final.
- **Radix / Base UI / React Aria / Ark UI**: accessible behavior without locking visual style.
- **Ant Design / MUI / Mantine / Chakra / HeroUI**: useful for speed or ecosystem; they bring a visual face — use deliberately.
- **TanStack Table**: prefer for serious data tables; style separately.
- **Storybook**: use when component states need to stop drifting.
- **Playwright**: use for visual checks, responsive screenshots, and interaction verification.
- **Design galleries and curated UI inspiration libraries**: exploration references, not final authority.

## Development guardrails

### Hard red lines

- Secrets, tokens, private URLs, or sensitive identifiers exposed by default.
- Dangerous / destructive actions without confirmation or undo.
- Technical status shown as the primary user-facing copy with no translation.
- Long text, IDs, paths, or JSON breaking layout.
- Mobile / compact view unusable for its primary task.
- Raw JSON as the primary interface for non-developer tasks.
- README / architecture / product manifesto pasted into normal operational UI.

### Default guidance (explainable exceptions allowed)

- Tool pages prioritize task efficiency over hero or atmosphere.
- Admin / ops pages prioritize state, issues, and next action over decoration.
- Tables browse and select; complex editing belongs in detail panels, drawers, flows, or dedicated screens.
- Page copy is short; deep explanation belongs in help / docs / tooltips / details.
- State and errors include reason, impact, and next step.

### Creative freedom zone

If the product is novel, AI-native, marketing-led, or consumer-facing, allow stronger visual identity. Explain why the style fits the product and how it preserves usability.

Creative freedom does not waive the craft floor. Before delivery, check that:

- alignment and spacing follow a clear rhythm;
- primary, secondary, and utility actions are visually distinct;
- read-only status, navigation, controls, and diagnostics do not share confusing styles;
- user-facing labels dominate technical identifiers;
- actions sit near the content they operate on;
- empty leftover space is intentional, not unfinished layout residue.

## Anti-pattern self-check

Before delivery, verify the output does not contain:

- Screen-only thinking with no user journey.
- README pasted on screen.
- Landing-page treatment on a tool page.
- Card wall with no task hierarchy.
- Business-object soup on a flat surface.
- Everything visible at once instead of progressive disclosure.
- No recovery path after error, permission denial, or destructive action.
- Giant all-in-one form instead of progressive disclosure.
- Table stuffed with complex configuration.
- Raw technical states as primary copy.
- Fake-premium styling that does not serve the task.
- Mechanical mobile stacking without task reordering.
- Default component-library look with no project-specific adaptation.
- Missing loading / empty / error / long-text states.
- Local consistency drift: components look reasonable alone but misalign across spacing, tag styles, numeric precision, state indicators, separators, or button hierarchy.

If present, fix or explicitly justify. See `references/anti-patterns.md`.

## Workflow

```
Project cognition → recommend → preview → choose → polish → optimize → judge → codify → unify
```

Full workflow with gates: `references/workflow.md`.

## Reference files

Read only what is needed:

- `references/workflow.md` — full workflow, phase guides, and thinking gates.
- `references/project-cognition.md` — project recognition and human-language copy.
- `references/tool-selection.md` — component libraries, frameworks, verification tools.
- `references/design-reference-packs.md` — design-system references by product temperament.
- `references/anti-patterns.md` — Codex / GPT frontend failure modes.
- `references/ux-evaluation.md` — task flow, friction, IA, recovery, mobile UX, and GPT UX weakness review.
- `references/development-guardrails.md` — rules, constraints, and delivery checks.

Templates (copy into project with `scripts/init_frontend_quality.py`; use `--update-agents` only when the user wants a repository-level `AGENTS.md` pointer):

- `templates/DESIGN.md`
- `templates/FRONTEND_CONTRACT.md`
- `templates/PAGE_BRIEF.md`
- `templates/FRONTEND_REVIEW.md`

## Delivery format

When advising or reviewing:

```text
判断：
推荐：
理由：
风险：
下一步：
需要沉淀到规范的点：
```

When implementing:

```text
已遵守的项目认知：
关键设计取舍：
验证结果：
后续可沉淀：
```
