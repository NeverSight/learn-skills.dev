---
name: sb-stories
description: "Write a CSF3 story for ONE React component, covering only its materially-different states (no Cartesian), with a factory when 3+ stories share a shape. Use for 'write a story for X', 'document this component', 'add a Storybook story'."
compatibility: "Requires bash, python3, and Node.js (Storybook; the --strict gate runs tsc + eslint via npx); git optional (--diff mode), jq optional (design-system hint in check-story-ready)."
allowed-tools: Bash Read Glob Grep Write Edit
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    # Skill-local files live in this skill's scripts/ + references/; shared ones (e.g. discover-runtime.py,
    # validate-stories.sh, anti-patterns.md, composition-patterns.md) resolve from shared/ ($CORE) in dev
    # and are copied into dist/ by build.sh on export.
    scripts: [validate-stories.sh, check-story-ready.sh, scaffold-factory.sh, extract-states.sh, extract-prop-shapes.sh, page-patterns.py, scaffold-page-story.py, discover-runtime.py]
    wrappers: false
    references: [with-mcp.md, without-mcp.md, anti-patterns.md, validate-workflow.md, factory-patterns.md, extraction-workflow.md, test-wiring.md, directory-structure.md, composition-patterns.md]
    templates: [controlled-component-story.tsx]
---

# sb-stories — one component, its real states

The default Build mode. The component exists in `src/components/`; you write its visible-states story.

## Before authoring (ask yourself)

- **Is it actually used?** Check `components.real[]` in `.storybook/project-inventory.json`. If it's
  in `dead[]`, remove it — don't write a story. If it's `vendor` (shadcn `ui/`), deprioritize.
- **Which states change behavior/appearance materially?** Refuse Cartesian combinations. Per-primitive
  minimum tables in `references/anti-patterns.md` (Button 8, Input 8, Modal 5, Form 6).
  Read `.storybook/component-states.json` instead of guessing — **if it's missing, generate it first:**
  `scripts/extract-states.sh`. (Bigger extraction context: `references/extraction-workflow.md`.)
  To render all those states on **one canvas**, use the `StateGrid` wrapper (variants × states →
  `StateMatrix`) from `sb-wrappers` — don't hand-roll the grid. These are the component-time wrappers;
  the data wrappers (ProjectInventory / DesignSystemHealth / AppFlowGraph …) come after their own steps.
- **Which states does THIS app actually ship?** Read `.storybook/component-usage.json` (`sb-inventory`'s
  `extract-component-usage.sh` — generate it if missing). Use `props.<prop>.values` to **prioritize** the
  variants real call sites pass; for anything in `declaredButUnused` (e.g. `variant=danger` never used),
  still author the state for completeness but **tag it `['usage:unused']`** and note "not used in this app"
  — don't pad the catalog with states prod never renders.
- **You don't author per-component docs by hand — they're composed once.** Every component's autodocs
  page already gains a **"Real usage in this app"** band: the `UsageSection` block (wired once into
  `preview.ts` `docs.page` by `sb-setup`) renders a **"Where it's used"** map per component — the pages it
  lands on, what nests it, what it renders, the tokens it pulls — read from the usage graph
  (`component-pages.json`). So when you add a story, **don't hand-add a usage block**; just run
  `refresh-usage.sh` so the graph is current and the band populates. To explore the whole graph
  interactively (any token / component / page → everywhere it's used, clickable), scaffold the
  **`UsageExplorer`** wrapper (`sb-wrappers`). Details + the docs.page composition live in `sb-inventory`
  (§ "Real usage in autodocs") and `sb-setup` (docs-page composition).
- **Factory?** YES if 3+ stories share a data shape. Read `.storybook/prop-shapes.json` (candidates
  flagged with `liveUsages`) — **if missing, run `scripts/extract-prop-shapes.sh` first.** Then
  `scripts/scaffold-factory.sh <Type> <import-path>` and fill the deterministic stub
  (`references/factory-patterns.md`); otherwise inline `args`.
- **Title taxonomy?** Match `storySort.order`; if the project has none, pick one via
  `references/directory-structure.md`.
- **Does a `play` actually earn its place?** Only write one for an interaction, async data,
  a portal, a CSS-driven state, or accessibility — never a bare `toBeVisible()` (anti-pattern 34).
  And the **project needs exactly one `CssCheck`** (anti-pattern 33): one story asserting a real
  `getComputedStyle` token value, the only proof the shared preview loaded the app's CSS. Both come
  from `npx storybook ai setup`'s prompt; `validate-stories.sh` check 13 + the project tally enforce them.
- **A "playground" / showcase story is Controls-driven, not click/hover.** If a reviewer asks "what is
  this playground story — can I click or hover it?": a playground is the **default story with its Controls
  panel** — you change `args` (variant, size, state) in the Controls tab and the canvas re-renders. It is
  NOT canvas interaction; hover/focus/active live in a `StateGrid` interaction matrix (addon-pseudo-states),
  and scripted click→assert flows live in a `play` function. So: Controls = try props · pseudo-states =
  hover/focus columns · `play` = a real interaction. Say which one the story is.
- **Is the Controls panel wired?** A component story must expose a usable Controls panel — it's the
  reviewer's prop sandbox and powers the autodocs ArgTypes table. The react-vite default
  (`react-docgen`) does NOT infer TS unions into selects, so declare `argTypes` for every enum/union
  prop (`control: 'select'|'inline-radio'` + `options`), group with `table.category`, hide
  escape-hatch / non-serializable props (`className`, refs, icon / callback / data props), and disable
  controls on render-only showcase stories (`parameters: { controls: { disable: true } }`). Full
  pattern + the docgen gotcha: `references/without-mcp.md` §13. (The panel itself must be *visible* —
  `sb-setup` writes a `manager.ts` with `showPanel: true`; `sb-audit`'s `audit-controls.sh` flags any
  component story missing this wiring.)

## Authoring source (mutually exclusive — load exactly one)

```bash
grep -q '@storybook/addon-mcp' package.json && test -f .mcp.json && echo WITH_MCP || echo WITHOUT_MCP
```

- `WITH_MCP` → `references/with-mcp.md` (MCP injects CSF3 conventions; you focus on judgment).
- `WITHOUT_MCP` → `references/without-mcp.md` (13 verification gaps + 4 critical SB10 patterns).
- Controlled components (Switch/Toggle/Checkbox/Tabs/Accordion/Select) start from
  `templates/controlled-component-story.tsx` — the `useArgs` sync is what AI gets wrong.

**Where the file goes (ASK first — don't scatter the repo).** Read `storiesLocation` from
`.storybook/audit/status.md` (the single rule lives in `CONTEXT.md` §STORIES LOCATION).

- **If it's unset** (e.g. the repo already had Storybook so `sb-setup` never asked), **STOP and ASK
  the user before writing any story** — never guess, never co-locate silently. Use `AskUserQuestion`
  (Claude) / `request_user_input` (Codex), or a numbered list where no blocking tool exists:
  > **Where should I save the stories? (everything else already lives under `.storybook/`.)**
  > 1. **`.storybook/stories/`** *(recommended — one place, isolated; `src/` untouched, one removable folder)*
  > 2. **Co-located** `src/**/<Name>.stories.tsx` *(for a project you own long-term)*
  > 3. **A custom folder** *(you name it — still kept to that one place)*
  Then record it in `.storybook/audit/status.md` as `storiesLocation: <isolated|colocated|PATH>`, make
  sure `main.ts` `stories` includes that path, and proceed. Recommend option 1.
- **`isolated` (or `.storybook/stories/`)** → write under `.storybook/stories/` mirroring the tree
  (`.storybook/stories/components/CourseCard.stories.tsx`), importing the component via the `@/` alias.
- **`colocated`** → `src/components/<X>/<X>.stories.tsx`.  **A custom path** → write there, every story.

Whatever the answer, **all stories go to that one location** — never a mix.

Title (the in-Storybook path, separate from the file path): match `.storybook/preview.ts`
`storySort.order`; else `Components/<Domain>/<Name>`. An **Overview / Spec / hub** story is an entry
point — pin it to the **top of its root** via `storySort.order` (a root-level hub first; a per-feature
`Overview`/`Spec` first in its group's sub-order with a `'*'` tail), never let it sort alphabetically into
the middle of the content it summarizes. See `references/directory-structure.md` → "Overview / spec / hub".

## Pages — real-page capture (Mode A)

For a **page** (a route/view under `pages/` · `app/` · `routes/` · `views/`) do NOT recreate it.
Run `scripts/page-patterns.py <root>` first — per page it reports `importable`, `component`,
`layout`, `dataHook` + **`dataType`** (the mock signal), `sections` (render order, `ui/` excluded),
`gridHint`; plus `sharedSections[]`. Then pick the mode off `importable`:

- **`importable: true`** (page has a default-export component) → **import the real page as-is and
  mock ONLY its data layer.** Scaffold with `scripts/scaffold-page-story.py <root> <page-suffix>`:
  it emits a `Pages/<Name>` story that imports the real page + wires the detected provider
  (Inertia `usePage` / router / store), with props **seeded from a factory keyed on `dataType`**
  (`scripts/scaffold-factory.sh <dataType> <import-path>`, per `references/factory-patterns.md`).
  Add one story per materially-different **data** state (empty / populated / error) — different
  factory inputs, never different markup. **Never re-author the page's JSX** (anti-pattern 27):
  the layout, columns, and components are the real page's, not yours.
- **`importable: false`** (assembled inline / no single component) → fall back to **Page Composition**
  (`references/composition-patterns.md` Pattern 4): assemble from the real `sections` —
  still factory-backed, still real components.

`sharedSections[]` (a section rendered by ≥2 pages) are the reusable page-pattern pieces — give each
its own `Components/*` story so pages **compose** them, not duplicate them.

## Overlays (Dialog / Modal / Sheet / Drawer / Popover) in autodocs

An open overlay portals a `position:fixed inset-0` overlay to `document.body`. Rendered **inline** on
the autodocs page (as the `Primary` block does), that overlay escapes over the *whole Docs page* —
Title, the "Real usage" section, Controls all vanish behind a blank backdrop. So for any overlay
component with `autodocs`, scope the story to its own iframe:

```ts
parameters: {
  layout: 'fullscreen',
  docs: { story: { inline: false, height: '640px' } },  // portal stays inside the frame; Docs prose stays readable
}
```

The story view (one story, full canvas) is unaffected — this is only for the Docs page. Don't reach
for it on non-overlay components (inline rendering is lighter).

**The page's own `dataHook` is just its data; the preview must also supply the provider TREE + root
CSS the page renders under.** Read those from `.storybook/runtime.json` (`scripts/discover-runtime.py`) —
`providers[]`, `rootCss`, `portals[]`, `network.needsMsw` — they're set up once in the shared preview
by `sb-setup`, so a page story rarely re-wires them. **Never re-derive by shell scan what a script
already wrote to `.storybook/*.json`** — cite the field.

## Batch (several components)

Write one story per component (each covering only its real states), then gate each with
`scripts/validate-stories.sh`. On Claude Code you can speed a batch up by writing components in
parallel with the Agent tool, but it's the same work — no special sub-agent needed.

## Gate before done

```bash
SKILL=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
"$CORE/scripts/validate-stories.sh" path/to/Foo.stories.tsx
# --strict adds tsc + eslint · --diff lints only changed stories
# For the "give me confidence" verdict (setup readiness preflight + conformance in one),
# run "$SKILL/scripts/check-story-ready.sh" path/to/Foo.stories.tsx instead — CONFIDENT when discovery JSONs are present.
```

Exits non-zero on any FAIL — fix before continuing. If you wrote a `play`, also dispatch the
judgment sub-agent (see `references/validate-workflow.md`); bash can't verify a `play`
is meaningful. To make stories an agent-runnable CLI gate (headless vitest + a11y), see
`references/test-wiring.md`.
