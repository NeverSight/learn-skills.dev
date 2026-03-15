---
name: build-daisyui-mcp
description: Use skill if you are building UI with daisyUI components, converting Figma designs or screenshots to daisyUI code, or generating themes using the daisyui-blueprint MCP server.
---

# build-daisyui-mcp

Use this skill as the operating layer for daisyUI 5 work with the `daisyui-blueprint` MCP tools. Keep `SKILL.md` lean: choose the correct workflow, fetch only the references you need, and keep bulky detail in `references/`.

## Use this skill for

- Building or refactoring UI with daisyUI 5 + Tailwind v4
- Converting a Figma frame or screenshot into daisyUI code
- Choosing the right snippet category: `components`, `component-examples`, `layouts`, `templates`, or `themes`
- Generating or adapting a custom daisyUI theme from brand colors, images, or existing UI

## Do not use this skill for

- Pure Tailwind work with no daisyUI goal
- UI libraries other than daisyUI
- Generic design discussion that does not need daisyUI code, snippets, or themes

## Non-negotiable rules

1. **Nested object syntax only** for `daisyui-blueprint-daisyUI-Snippets`. Arrays fail silently.
2. **Fetch before guessing.** If you do not know a valid class or example key, fetch the component reference first. Guessing class names is the #1 source of broken output.
3. **Batch requests, max ~8 items per call.** Get all needed snippets in one call; do not fetch one component at a time. But keep each call under ~8 items — larger batches produce 15–26 KB responses that can overflow context.
4. **Use the right category.** `components` is reference data (class names, parts, modifiers), not copy-paste HTML. `component-examples` is working markup. `themes` returns CSS, not HTML.
5. **Start page work from `templates` (preferred) or `layouts`.** Templates give a complete starting point; layouts give a shell. Do not assemble full pages from many isolated component guesses.
6. **For Figma, always follow** `FETCH → ANALYZE → GET SNIPPETS → BUILD`. Never skip analysis.
7. **Use semantic daisyUI colors** (`primary`, `secondary`, `accent`, `neutral`, `base-*`, `info`, `success`, `warning`, `error`) and `*-content` variants on themed surfaces.
8. **Do not use `dark:` for daisyUI semantic colors.** Themes already adapt them. Only use `dark:` for custom Tailwind utility classes outside daisyUI's theme system.
9. **Prefer CSS-only daisyUI interaction patterns** unless app-specific behavior truly requires custom JS:
   - drawer → checkbox toggle (use `is-drawer-open:` / `is-drawer-close:` variants for visibility)
   - modal → `<dialog>` with `.modal-open` or JS `.showModal()`
   - dropdown → `<details>` or popover API
   - tabs/steppers → daisyUI radio/tab patterns
10. **Stay on daisyUI v5 syntax** (`fieldset`, `dock`, `tabs-lift`, `card-border`, no `input-bordered`, no `form-control`).
11. **Load only the 1–3 references needed for the active task.** Do not dump the entire skill into context.
12. **Adapt output to the target framework.** For React/Next.js: `class` → `className`, self-close void elements (`<img />`, `<input />`), `for` → `htmlFor`, `tabindex` → `tabIndex`. For Vue: use `:class` bindings. For Svelte: use `class:` directives.

```jsonc
// ✅ Correct
{
  "components": { "button": true, "card": true },
  "component-examples": { "card.card": true }
}

// ❌ Wrong — arrays fail silently with no error
{ "components": ["button", "card"] }
{ "snippets": ["components/button"] }
```

## Choose the right tool or snippet category first

| Need | Use | Key rule |
|---|---|---|
| Validate classes, parts, modifiers, or discover example names | `components` | Start here when unsure |
| Copy-paste markup for a known pattern | `component-examples` | Fetch only the 1–3 best matches |
| Get a page shell with placeholders | `layouts` | Best starting point for dashboards, sidebars, app shells |
| Start from a full page | `templates` | Use for login/dashboard/full-page acceleration |
| Get theme variables or color-system reference | `themes` | Returns CSS/config, not component HTML |
| Extract structure from a Figma design | `daisyui-blueprint-Figma-to-daisyUI` | Returns a node tree only; always follow with snippets |

**Mix categories in one call** when you already know what you need:

```json
{
  "layouts": { "responsive-collapsible-drawer-sidebar": true },
  "components": { "navbar": true, "card": true, "table": true },
  "component-examples": {
    "navbar.responsive-dropdown-menu-on-small-screen-center-menu-on-large-screen": true,
    "table.table-with-visual-elements": true
  },
  "themes": { "colors": true }
}
```

## Route to the correct workflow

> **Priority rule — first match wins.** Walk the table top to bottom; stop at the first row that matches the request. If the request spans multiple rows (e.g., "Figma design with forms"), handle the primary workflow first, then load secondary references.

| Request shape | Do this first | Then load |
|---|---|---|
| Setup or install daisyUI / Tailwind v4 | Read setup docs | `references/integration/tailwind-v4-setup.md` |
| MCP server missing or Figma auth/setup issue | Fix tool setup before composing UI | `references/tool-api-reference.md` |
| Migrating from daisyUI v4 | Read migration docs before writing code | `references/integration/v4-to-v5-migration.md` |
| Single component or section | Fetch `components` first, then targeted `component-examples` | `references/common-mistakes.md` |
| Full page, dashboard, auth screen, landing page | Start from `templates` (preferred) or `layouts` | `references/workflows/component-composition.md`, `references/workflows/responsive-layouts.md` |
| Figma URL present | Run the Figma workflow below | `references/workflows/figma-to-code.md`, `references/tool-api-reference.md` |
| Screenshot or image mockup | Run the screenshot workflow below | `references/workflows/screenshot-to-code.md`, `references/common-mistakes.md`, `references/prompts/screenshot-prompt.md` |
| Brand colors, image-to-theme, dark mode, theme request | Run the theme workflow below | `references/workflows/theme-generation.md`, `references/theming/custom-themes.md`, `references/theme-and-colors.md`, `references/prompts/image-to-theme-prompt.md` |
| Form-heavy UI | Load form patterns before composing | `references/patterns/form-patterns.md` |
| Navbar, menu, drawer, tabs, dock, breadcrumbs | Load navigation patterns before composing | `references/patterns/navigation-patterns.md` |
| Bootstrap or raw Tailwind conversion | Use the relevant conversion workflow | `references/workflows/bootstrap-conversion.md`, `references/workflows/tailwind-optimization.md`, `references/prompts/bootstrap-prompt.md`, `references/prompts/tailwind-prompt.md` |
| Prompt crafting or multi-step chaining | Load prompt guides | `references/prompts/prompt-engineering.md`, `references/prompts/prompt-chaining.md` |

## Workflow — component or page composition

1. **Decide scope and starting point.**
   - Single component/section → fetch `components` reference, then targeted `component-examples`.
   - Full page/app shell → fetch a `template` (preferred) or `layout` first. Never build a full page from scratch when a template exists.
2. **Fetch reference data before writing any markup.**
   - For each component you plan to use, verify its valid classes via `components` category.
   - Batch related components in one MCP call (~8 items max).
   - If you need exact example keys, fetch `components` first to discover names, then fetch `component-examples`.
3. **Fetch only targeted examples** for complex pieces: responsive navbars, drawers with icon-only collapsed state, data tables, pricing cards, multi-step forms.
4. **Compose from the outside in** — this is the assembly order, not optional:
   1. Page shell (template or layout)
   2. Navigation (navbar, sidebar/drawer, breadcrumbs)
   3. Main content blocks (hero, stat grids, card grids, tables)
   4. Detail components (badges, tooltips, modals, toasts)
5. **Apply semantic colors and responsive utilities** after structure is correct. Use `sm:`, `md:`, `lg:` breakpoint prefixes for responsive behavior.
6. **If the page is branded**, do theme work before final polish so semantic colors resolve correctly.

> **Steering — page composition pitfalls from real usage:**
> - Dashboard stat grids: use CSS grid (`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4`) not flexbox for even columns.
> - Drawer checkbox toggle: the `<input type="checkbox">` must be a sibling of `.drawer-side`, not nested inside content. Use `is-drawer-open:` and `is-drawer-close:` variants for show/hide behavior.
> - If a UI element has no daisyUI equivalent (charts, maps, code editors, media players), wrap it in a `card` or `card-body` container with semantic colors applied to the wrapper only. Do not force non-UI elements into daisyUI components.

Load only what you need:

- `references/workflows/component-composition.md` — dashboard, landing page, and e-commerce patterns
- `references/workflows/responsive-layouts.md` — breakpoint strategies, grid patterns
- `references/common-mistakes.md` — "do this, not that" quick reference

## Workflow — Figma to daisyUI

This sequence is mandatory.

1. **FETCH**
   - Call `daisyui-blueprint-Figma-to-daisyUI`
   - Prefer a node-specific Figma URL (`?node-id=X-Y`)
   - Start with `depth: 3-5`; increase only if the tree is too shallow
   - Use `includeImages: false` unless image references are required
2. **ANALYZE**
   - layout direction and alignment
   - spacing and padding
   - component candidates
   - typography scale
   - corner radius, shadows, and color roles
3. **GET SNIPPETS**
   - Batch all identified components in one call (~8 items max)
   - If example names are unknown, fetch `components` first, then the exact `component-examples`
4. **BUILD**
   - Map Figma structure to daisyUI components + Tailwind layout classes
   - Use semantic colors instead of hardcoded hex on UI surfaces
   - Add responsive breakpoints explicitly
5. **RECOVER IF NEEDED**
   - If the node tree is too shallow, re-fetch with higher depth
   - If the file is large/noisy, switch to a more specific node URL
   - If a Figma element has no daisyUI equivalent, use raw Tailwind wrapped in a semantic container (see recovery rules)

Load only what you need:

- `references/workflows/figma-to-code.md` — step-by-step Figma extraction guide
- `references/tool-api-reference.md` — MCP tool parameters and auth setup
- `references/component-catalog.md` — full class/modifier reference when lookup is needed

## Workflow — screenshot or mockup to daisyUI

1. **Scan top-to-bottom**: navbar/header, hero, sidebar, main content, footer/dock.
2. **Identify the page shell first** before individual components. Check if a `template` or `layout` matches the overall structure.
3. **Catalog visible patterns**:
   - component type
   - likely variant
   - size
   - semantic color role
   - visible state
4. **Fetch components and only the best-matching examples** (~8 items max per call).
5. **Assemble the shell first**, then fill details and tune spacing/color.
6. **For non-daisyUI elements** (charts, graphs, maps, video players): note them as `<!-- TODO: integrate [chart library] here -->` inside a `card` wrapper with appropriate sizing. Do not attempt to recreate them with daisyUI components.
7. **If an interaction is not visible**, choose the most likely CSS-only daisyUI pattern and state the assumption.

Load only what you need:

- `references/workflows/screenshot-to-code.md` — full screenshot conversion workflow
- `references/prompts/screenshot-prompt.md` — agent prompt for screenshot analysis
- `references/component-catalog.md` — class validation when uncertain
- `references/common-mistakes.md` — avoid frequent errors

## Workflow — theme generation

1. **Determine the source**: brand palette, image, existing website, or Figma tokens.
2. **Map source colors to daisyUI semantics**:
   - `primary`, `secondary`, `accent`
   - `neutral`
   - `base-100`, `base-200`, `base-300`, `base-content`
   - `info`, `success`, `warning`, `error`
3. **Generate matching `*-content` colors** with accessible contrast.
4. **Output `@plugin "daisyui/theme"` CSS in OKLCH.**
5. **Validate with semantic component usage**; do not leave UI surfaces on raw Tailwind colors.
6. **If building branded UI**, theme first, then fetch templates/components so the markup stays semantic.

Load only what you need:

- `references/workflows/theme-generation.md` — end-to-end theme workflow
- `references/theming/custom-themes.md` — variable reference and design presets
- `references/theme-and-colors.md` — color system architecture
- `references/prompts/image-to-theme-prompt.md` — image-to-OKLCH extraction prompt
- `references/tool-api-reference.md` for `themes` category usage

## Recovery rules — if the agent starts drifting

- **Snippets tool returns nothing or empty** → check nested object syntax first; arrays fail silently.
- **You do not know an example key** → fetch the `components` category for that component; example keys are listed in the response.
- **Generated classes look plausible but unverified** → validate via `components` category or `references/component-catalog.md`.
- **You are making too many MCP calls** → batch them (~8 items max) and mix categories in one call.
- **A full page is forming from unrelated snippets** → stop and restart from a `template` or `layout`.
- **The MCP server or Figma tool errors on setup/auth** → check `references/tool-api-reference.md`, especially MCP config and `FIGMA` requirements.
- **Markup uses `bg-blue-500`, `text-white`, or `dark:` on themed UI** → replace with semantic color classes (`bg-primary`, `text-primary-content`) or a custom theme.
- **You added JS for a standard drawer/modal/dropdown** → switch back to the CSS-only daisyUI mechanism.
- **You see v4 terms** like `form-control`, `input-bordered`, `label-text`, `tabs-lifted`, or `btm-nav` → convert to v5 equivalents and load `references/integration/v4-to-v5-migration.md`.
- **You start copying bulky examples into this skill** → stop and route to the relevant reference instead.
- **A UI element has no daisyUI equivalent** (chart, map, code editor, media player) → wrap it in a semantic container (`card`, `card-body`) with a TODO comment. Do not invent daisyUI classes.
- **Output is for React/Next.js but uses HTML attributes** → apply rule 12 (framework adaptation).
- **MCP response is huge (>10 KB)** → you fetched too many items. Reduce batch size and be more targeted.

## Minimal reference packs

| Task | Load |
|---|---|
| Single component/section | `references/common-mistakes.md` |
| Full page/layout | `references/workflows/component-composition.md`, `references/workflows/responsive-layouts.md` |
| Figma conversion | `references/workflows/figma-to-code.md`, `references/tool-api-reference.md` |
| Screenshot conversion | `references/workflows/screenshot-to-code.md`, `references/common-mistakes.md` |
| Theme generation | `references/workflows/theme-generation.md`, `references/theming/custom-themes.md` |
| Forms | `references/patterns/form-patterns.md` |
| Navigation | `references/patterns/navigation-patterns.md` |
| Setup or migration | `references/integration/tailwind-v4-setup.md`, `references/integration/v4-to-v5-migration.md` |
| Bootstrap/Tailwind conversion | `references/workflows/bootstrap-conversion.md`, `references/workflows/tailwind-optimization.md`, `references/prompts/bootstrap-prompt.md`, `references/prompts/tailwind-prompt.md` |
| Prompt crafting / chaining | `references/prompts/prompt-engineering.md`, `references/prompts/prompt-chaining.md` |
| Class/modifier validation | `references/component-catalog.md` |
| Color system deep dive | `references/theme-and-colors.md`, `references/theming/custom-themes.md` |
| Image to theme | `references/prompts/image-to-theme-prompt.md`, `references/theme-and-colors.md` |
| Screenshot analysis prompts | `references/prompts/screenshot-prompt.md` |

## Exit checklist

Before finishing, verify each item passes:

| Check | Pass criteria |
|---|---|
| Snippet syntax | Every `daisyui-blueprint-daisyUI-Snippets` call uses `{ "category": { "name": true } }` — no arrays, no string values |
| Category choice | `components` used for class lookup; `component-examples` for markup; `templates`/`layouts` for page shells; not mixed up |
| Batch efficiency | All needed snippets fetched in ≤3 MCP calls total (not one call per component) |
| daisyUI v5 classes | Zero occurrences of `form-control`, `input-bordered`, `label-text`, `tabs-lifted`, `btm-nav`, or other v4-only classes |
| Semantic colors | All themed surfaces use `bg-base-*`, `text-base-content`, `bg-primary`, etc. — no raw Tailwind colors (`bg-blue-500`) on daisyUI components |
| `dark:` usage | Zero `dark:` prefixes on daisyUI semantic colors; `dark:` only used for custom non-theme utilities |
| Layout starting point | Page-level work started from a `template` or `layout`, not assembled from individual components |
| Figma sequence | If Figma was involved: FETCH → ANALYZE → GET SNIPPETS → BUILD sequence was followed in order |
| Framework adaptation | If target is React/Next.js/Vue/Svelte: `class`→`className`, `for`→`htmlFor`, self-closing tags, etc. |
| Reference efficiency | Only 1–3 reference files were loaded for this task, not the full set |
