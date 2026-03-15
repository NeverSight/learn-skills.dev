---
name: extract-saas-design
description: Use skill if you are forensically documenting the visual system of an existing SaaS dashboard or admin UI into structured design docs, not rebuilding or redesigning it.
---

# Extract SaaS Design

Extract the implemented visual system of an existing SaaS dashboard, admin panel, or internal tool into structured documentation. This is forensic work: document what exists, where it comes from, and how it behaves.

## Use this skill when

- The user wants the current visual system documented: tokens, component specs, layout patterns, dark mode, or dashboard-specific UI behavior.
- The user wants to recreate the current look in another codebase **through documentation**, not by copying source.
- The user wants scoped extraction: foundations only, named components, a navigation or data-display slice, or an evidence-based consistency audit.

## Do not use this skill when

- The real task is to build, port, or generate a working UI.
- The real task is redesign, restyling, “make it better,” or speculative UX advice.
- The target is mainly a marketing or brochure site instead of a SaaS/dashboard/admin product.
- There is no implemented UI evidence to inspect.

## Operating boundaries

1. **Document, don't rebuild.** Output documentation and evidence, not production UI code.
2. **Honor the requested scope.** Do not default to a full-system extraction unless the user asked for it.
3. **Work from evidence only.** Read actual source files and supporting artifacts; never infer unimplemented behavior.
4. **Resolve aliases.** Convert utilities, tokens, and variables to final values and explain their semantic role.
5. **Absence is evidence.** If a state or mode does not exist, write `not implemented`.
6. **Separate canon from noise.** Document the dominant system, then flag inconsistencies and exceptions explicitly.

## Scope routing

| If the user asks for... | Example requests | Deliver |
|---|---|---|
| Full extraction / "visual DNA" / "document the design system" | "Extract the full design system", "Document the visual DNA" | `system.md`, foundation docs, relevant component docs, and meta-docs (`INDEX.md`, `_summary.md`) |
| Foundations / tokens / theme only | "Extract the color tokens", "Document the spacing system" | `system.md` plus foundation docs only; skip component docs unless requested |
| Specific components or patterns | "Document the sidebar", "Extract button specs" | Minimal foundation context plus full docs for the named components or patterns only |
| Consistency / quality / accessibility audit | "Audit the color consistency", "Check accessibility" | Evidence-based findings grounded in extracted docs; do not drift into redesign proposals |

## Minimal workflow

1. **Frame the job**
   - Restate what is in scope, what is out of scope, and which artifacts count as ground truth.
   - Prefer the smallest extraction that satisfies the request.

2. **Build the evidence base**
   - **Detect the styling stack first** -- this determines everything else:
     - Tailwind v4 uses `@import "tailwindcss"` in CSS and `@theme` blocks instead of `tailwind.config.js`. Check for both.
     - shadcn/ui: look for `components/ui/` directory and `@/lib/utils` imports with `cn()`.
     - CSS entry point: find `globals.css` or `app.css` -- this is where tokens live.
   - Identify token sources: global CSS, theme files, Tailwind config (if v3), component source, Storybook.
   - **Resolve representative token chains end-to-end** before writing docs:
     ```
     Tailwind class -> CSS variable -> final value
     bg-primary -> var(--primary) -> oklch(0.21 0.006 285.88)
     ```
   - Detect the color space: modern shadcn uses `oklch()`, older uses `hsl()`.
   - Check for variant systems: CVA (`class-variance-authority`) defines variant/size matrices.
   - Capture recurring values, mode switching, state styling, and composition patterns.
3. **Extract foundations first when needed**
   - Spacing, colors, typography, shadows/depth, radius, animations, and shared state conventions.
   - For dashboard products, explicitly check sidebar overrides, chart palettes, density zones, and tabular/monospace usage.

4. **Extract components and patterns in scope**
   - For each component, document anatomy, variants, sizes, states, state transitions, dark-mode differences, and composition.
   - Treat sidebars, tables, command palettes, and form layouts as mega-components that must be decomposed.

5. **Verify before handoff**
   - Use `references/quality-checklist.md` as your verification checklist.
   - Every important value should be resolved to a final computed value, not just a class name or alias.
   - Every relevant state should be explicit, including `not implemented`.
   - Pay special attention to disabled, focus-visible, loading, error/invalid, empty, and dark-mode behavior.
   - Document opacity semantics and animation composition when they carry design meaning.
   - If a recreator would still need to guess, the extraction is incomplete.

6. **Package the output**
   - Create all extraction artifacts in the `.design-soul/` directory at the **codebase root** (not inside the skills repo).
   - Use the `.design-soul/` structure defined in `references/documentation/output-format.md`.
   - Follow the exact templates and file layout from the references instead of inventing new formats.

## Guardrails: do this, not that

| Do this | Not that |
|---|---|
| Resolve `bg-primary`, `rounded-md`, `p-3`, and similar aliases to actual values and meanings | Stop at class names or token aliases |
| Write `Hover: not implemented` / `Loading: not implemented` when absent | Invent expected states or “best practice” behavior |
| Scope to the user's request | Default to documenting the entire app |
| Document composition and context | Describe components only in isolation |
| Decompose mega-components into sub-parts and modes | Flatten sidebar, table, or form layout into one vague blob |
| Flag inconsistencies with file evidence | Smooth them over into a cleaner system than the product really has |
| Keep audits evidence-based | Turn the task into redesign or subjective critique |

## Recovery rules

- **Evidence is incomplete:** look for adjacent ground truth (global CSS, theme files, config, Storybook, screenshots). If still unresolved, document the gap explicitly.
- **The codebase is too large:** split into foundations plus the requested categories or components; do not widen scope silently.
- **Values conflict across files:** document the dominant pattern, then list exceptions with source references.
- **Dark mode or a state does not exist:** say so plainly; absence is part of the extraction.
- **The task starts drifting toward implementation:** stop generating build instructions and return to documentation deliverables.

## Output contract

When you are asked to produce extraction files, keep the structure predictable:

- `system.md` for foundations in scope
- numbered foundation docs when doing system-level extraction
- one numbered doc per extracted component
- `INDEX.md` and `_summary.md` for multi-document or full extractions

Use the exact structure, naming, and content expectations in `references/documentation/output-format.md`, `references/system-template.md`, and `references/component-template.md`.

## Reference routing

Start with the smallest relevant set. Only expand if the task genuinely needs more depth.

| Need | What it contains | Read |
|---|---|---|
| Foundation extraction method | Agent prompts for scanning tokens + grep commands + output templates | `references/foundations-agent.md`, `references/extraction/color-extraction.md`, `references/extraction/typography-extraction.md`, `references/extraction/spacing-extraction.md`, `references/system-template.md` |
| Component extraction method | Agent prompt for per-component visual specs + template with all required sections | `references/components-agent.md`, `references/component-template.md`, `references/extraction/icons-and-assets.md` |
| Dashboard/admin-specific patterns | Sidebar, metrics, tables, charts, cmdk, mega-component decomposition | `references/dashboard-patterns.md`, `references/layout/grid-and-responsive.md` |
| Token translation and naming | W3C DTCG, CSS custom properties, oklch format, shadcn naming pattern | `references/tokens/token-formats.md`, `references/tokens/naming-conventions.md` |
| Packaging the docs | `.design-soul/` directory structure, INDEX.md and _summary.md templates | `references/documentation/output-format.md`, `references/system-template.md`, `references/component-template.md` |
| Verification and audit | Extraction completeness checklist, token/component consistency matrix, WCAG contrast checks | `references/quality-checklist.md`, `references/audit/consistency-checklist.md`, `references/audit/accessibility-review.md` |

## Steering Notes for Agents

These notes prevent the most common extraction failures. Read the linked references for full detail.

### Tailwind v4 Detection

Grep for `@import "tailwindcss"` or `@theme` in CSS files — if found, the project uses Tailwind v4 (CSS-native config, no `tailwind.config.js`). If `tailwind.config.ts` exists with `theme.extend`, it uses Tailwind v3. Always check before extracting tokens. See `references/foundations-agent.md` for detection commands.

### oklch Color Space

Modern shadcn/ui (2024+) uses `oklch(L C H)` instead of `hsl()`. L=lightness (0-1), C=chroma (0-0.4), H=hue (0-360). Grays have C < 0.01. Always note lightness to distinguish dark/light colors. See `references/extraction/color-extraction.md` and `references/tokens/token-formats.md` for reading guides.

### CVA and cn() Patterns

The `cva()` call IS the component's visual spec — extract every variant/size key-value pair. The `cn()` utility merges classes via tailwind-merge where the last class wins. See `references/component-template.md` for the CVA extraction checklist and cn() merging guide.

### Token Chain Resolution

Never stop at the Tailwind class. Resolve the full chain: `bg-primary` → `var(--primary)` → `oklch(0.205 ...)`. Some tokens chain through multiple variables. Resolve ALL the way to the literal value. See `references/extraction/color-extraction.md` for variable chain resolution.

## Final reminder

This skill should feel like an orchestrator, not a template dump. Keep the main flow tight, use references for detail, and stay anchored to the implemented UI rather than rebuilding or redesigning it.
