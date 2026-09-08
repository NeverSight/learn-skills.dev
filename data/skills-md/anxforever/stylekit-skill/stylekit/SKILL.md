---
name: stylekit
description: Apply a specific, consistent visual style to frontend UI you are generating. Use when building or styling web UI (pages, components, dashboards, landing pages) and you want a named aesthetic — Glassmorphism, Neo-Brutalist, Cyberpunk, Bauhaus, Apple, Stripe, Linear, and many more — instead of generic AI defaults. StyleKit gives you design tokens, component recipes, and AI rules for each style, with themes installable through the shadcn registry.
---

# StyleKit

Apply StyleKit's 146 curated visual styles to generated UI. Use the catalog, fetch the exact spec, install the theme, and honor the style's rules.

## Workflow

1. **Detect project context** — know the target project's stack before generating.
2. **Pick a style** — match the user's intent to a catalog slug.
3. **Fetch the full spec** — pull tokens, recipes, and AI rules for that slug.
4. **Install the theme** (optional) — drop the shadcn registry theme into the project.
5. **Generate with the rules** — use the style's exact tokens and do/don't lists.

## Task routing

Route by what the user actually asked for:

- **New UI** (page, component, dashboard, landing page) → full workflow below.
- **Restyle / fix existing UI** ("this looks generic", "make it feel more Stripe") → Steps 0, 2, 3, then edit only the parts that violate the style's tokens and rules; keep the existing structure and states unless asked otherwise. See [references/design-principles.md](references/design-principles.md) iteration modes.
- **Migrate from one style to another** → fetch both specs, diff their tokens and forbidden lists, then update classes style-by-style. Never mix tokens from both styles.
- **Review / audit style consistency** → fetch the style spec, then check every component against doList/dontList and the token table. Report violations concretely (file, element, class).

## Step 0 — Detect project context

Before generating, run the detector in the target project directory:

```bash
python3 scripts/detect-project.py   # run from the project root, or pass a path
```

Use the output to adapt generation:

- **framework** (`next`/`react`/`vue`/`svelte`/`vanilla`) — match component style to the framework (client/server components for Next, etc.).
- **tailwind.version** — v4 uses CSS-first config (`@theme` in CSS, no `tailwind.config.js`); v3 uses the config file. The shadcn registry install requires Tailwind v4; if the project is v3, install the theme manually from the spec's `cssVars` instead.
- **shadcn.installedComponents** — prefer reusing installed components over generating new ones; match the project's alias paths.
- **reactVersion** — target the project's React version; do not use APIs the version doesn't support.

If the detector reports a stack you did not expect (e.g. the user said "React" but the project is Vue), stop and confirm with the user before generating.

## Step 1 — Pick a style

Match the user's request to a slug from the catalog:

- **Human catalog**: https://www.stylekit.top/styles
- **By theme**: https://www.stylekit.top/collections (dark-mode, retro-vintage, anime-manga, game-ui, colorful-bold, hand-drawn)
- **Colors / hex codes**: https://www.stylekit.top/colors
- **Machine-readable list**: `GET https://www.stylekit.top/api/styles` → `{ total, styles: [{ slug, nameEn, description, styleType, keywords, colors }] }`
- **Common style signatures**: see [references/style-signatures.md](references/style-signatures.md) for the visual traits of popular styles

For an ambiguous request, scan the `/api/styles` list keywords and pick the closest slug. When in doubt, ask the user between two candidates.

## Step 2 — Fetch the full spec

Fetch the machine-readable spec for the chosen slug — do not guess tokens or rules from memory (styles get updated):

```bash
python3 scripts/fetch-style.py <slug>            # full spec: tokens, recipes, rules
python3 scripts/fetch-style.py <slug> --tokens   # tokens only
python3 scripts/fetch-style.py <slug> --recipes  # recipes only
```

The script prints a compact spec for code generation. Raw endpoints are also available:

- Full pack: `GET https://www.stylekit.top/api/styles/{slug}`
- Markdown: `GET https://www.stylekit.top/api/styles/{slug}/md`
- Tokens: `GET https://www.stylekit.top/api/styles/{slug}/tokens`
- Recipes: `GET https://www.stylekit.top/api/styles/{slug}/recipes`
- Human page: https://www.stylekit.top/styles/{slug}

### Process the spec in priority order

1. **aiRules** — instruction string written for AI. Highest priority; overrides general patterns when they conflict.
2. **doList / dontList** — hard constraints. Every generated component must satisfy all items.
3. **philosophy** — the "why" behind the style. Determines ambiguous decisions (visual hierarchy, spacing, mood).
4. **colors** — `{ primary, secondary, accent[] }`. Source of truth for the palette.
5. **tokens** — semantic categories mapped to exact Tailwind classes. Use instead of inventing classes.
6. **components** — code templates for button, card, input (and optionally nav, hero, footer). Starting points.
7. **globalCss** — base CSS that must be included in the page/layout when using this style.

## Step 3 — Install the theme (optional)

Drop the theme into an existing shadcn/ui project (Tailwind v4):

```bash
npx shadcn add https://www.stylekit.top/r/<slug>.json
```

Requires a `tsconfig.json` in the target project. Injects the style's light + dark `cssVars` into `globals.css`. Full guide: https://www.stylekit.top/developers

If the project is not Tailwind v4 (per Step 0), do not run the registry install; apply the spec's `cssVars` and token classes manually.

## Step 4 — Generate with the style's rules

1. Use the style's **design tokens** (colors, spacing, typography, shadows, radii) — do not invent your own values.
2. Follow the **AI rules** and **doList/dontList** — they encode what makes the style read as intentional (e.g. Neo-Brutalist: thick borders, hard shadows, no rounded corners; Glassmorphism: high blur, translucency, inner glow).
3. Use **component templates** and **recipes** as starting points; adapt to the user's content and to the project's detected stack (Step 0).
4. Keep the style consistent across every component in the session, including responsive breakpoints (mobile-first).

### Good — uses exact token classes

```tsx
// Neo-Brutalist button — token classes from the fetched spec
<button className="
  px-6 py-3
  bg-[#ff006e] text-white font-black
  border-2 md:border-4 border-black rounded-none
  shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]
  hover:shadow-none hover:translate-x-[2px] hover:translate-y-[2px]
  active:translate-x-[4px] active:translate-y-[4px]
  transition-all duration-200
">
  Click Me
</button>
```

### Bad — guessing classes, ignoring tokens

```tsx
// WRONG: rounded-lg violates neo-brutalist (must be rounded-none)
// WRONG: shadow-lg violates neo-brutalist (must use hard-edge shadow)
// WRONG: bg-blue-500 is not in the style's color palette
<button className="px-6 py-3 bg-blue-500 rounded-lg shadow-lg">Click Me</button>
```

## Anti-patterns

- **Don't mix tokens from different styles.** Each style's tokens are internally consistent; mixing produces incoherent UI.
- **Don't ignore aiRules.** They override general patterns and may contradict common Tailwind conventions.
- **Don't use generic Tailwind when style-specific tokens exist.** Use `shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]` for neo-brutalist, not `shadow-md`.
- **Don't skip the philosophy.** It determines visual hierarchy decisions.
- **Don't generate without checking doList/dontList.** A glassmorphism component without `backdrop-blur` is broken; a neo-brutalist component with `rounded-lg` is wrong.
- **Don't hardcode hex values.** Use the style's `colors` object and token classes.
- **Don't rely on memory — always fetch the spec.** Styles get updated; stale data leads to violations.

## Don't skip these — and why

| "I can skip this because…" | Why you can't |
|----------------------------|---------------|
| "I already know neo-brutalist's tokens." | The spec changes with every release; your memory is a snapshot. Fetch it. |
| "This is a tiny button, tokens don't matter." | One off-token class breaks the whole style read. Every component must pass doList/dontList. |
| "The project looks like plain React, no need to detect." | Framework, Tailwind version, and existing shadcn components change how you generate. Run Step 0. |
| "I'll just use `bg-white` for glassmorphism, close enough." | `bg-white` is on glassmorphism's forbidden list. Exact tokens or it's not the style. |
| "The user asked for a quick tweak, no spec needed." | A tweak that ignores the spec silently drifts the UI away from the style. Fetch it. |

## Quality gate

Before delivering generated UI, apply the checks in
[references/design-principles.md](references/design-principles.md): swap test, squint test,
signature test, and token test. Keep the style identity strong, meet the accessibility baseline,
and avoid the anti-pattern blacklist.

Run the evaluator on the generated code to catch rule violations mechanically:

```bash
python3 scripts/eval-check.py <slug> <file>                  # check a file
python3 scripts/eval-check.py <slug> <file> --component button   # also enforce required classes for a declared component
```

`eval-check.py` reports forbidden classes, off-palette colors, and (with `--component`) missing
required classes. It treats the style's own component templates as the reference implementation:
a required entry is only enforced when the matching template uses it, so a spec-data inconsistency
does not produce false failures on generated code.

## Pre-delivery checklist

Confirm each item with concrete evidence before presenting the result:

- [ ] Style spec was fetched (not guessed) — cite the slug and that `fetch-style.py` ran.
- [ ] Project context was detected (Step 0) — cite the detected framework/Tailwind version.
- [ ] Every generated class comes from the style's tokens or explicit allowed values.
- [ ] No class from the style's `forbidden` list is present in the output.
- [ ] doList items are all satisfied; dontList items are all absent.
- [ ] `prefers-reduced-motion` is respected if the style animates.
- [ ] Colors are the style's palette (primary/secondary/accent), not invented hexes.
- [ ] Swap test passed — replacing the signature classes with defaults would visibly change the identity.
- [ ] Responsive behavior is mobile-first and consistent across breakpoints.
- [ ] `eval-check.py` reported no violations for the delivered files.

## Spec data health

The catalog is community-curated; occasionally a style's required table or a component template
contains an internal contradiction (e.g. a template uses a class the style forbids, or a template
carries a hex not in the palette). When you hit one:

- **Trust the component template** over the required table — the template is the verified
  reference implementation.
- **Report the inconsistency** rather than silently working around it: run
  `python3 scripts/verify-spec.py <slug>` to enumerate the exact contradictions, and tell the
  user (or open an issue on github.com/AnxForever/stylekit) so the catalog can be fixed.

## Resources

- `references/style-signatures.md` — visual traits, forbidden, and required classes for popular styles
- `references/design-principles.md` — quality bar: intent-first generation, token hierarchy, accessibility baseline, pre-delivery validation
- `scripts/fetch-style.py` — fetch a style's spec from the API and print a compact code-generation reference
- `scripts/detect-project.py` — detect the target project's framework, Tailwind version, and shadcn setup
- `scripts/eval-check.py` — mechanical compliance gate for generated code (forbidden, palette, required)
- `scripts/verify-spec.py` — audit a style's spec for internal contradictions (data health)
- `scripts/benchmark.py` — with/without-skill pass-rate comparison (regression suite)
