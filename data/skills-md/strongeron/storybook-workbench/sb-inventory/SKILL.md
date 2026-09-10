---
name: sb-inventory
description: "Audit a React+Vite app for real-vs-slop components (by actual imports), the dominant design system, and real prop-value usage at call sites. Use for 'what components do I have', 'which are dead', 'audit this vibe-coded app'."
compatibility: "Requires python3 and bash; the discovery scripts write JSON the agent reads (no jq needed at author time)."
allowed-tools: Bash Read Glob Grep Write
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    scripts: [inventory-project.sh, token-usage.py, scaffold-wrapper.sh, extract-component-usage.sh, scaffold-usage-mdx.py, build-component-pages.py, refresh-usage.sh]
    wrappers: [ProjectInventory, ComponentUsage]
    references: [field-learnings.md]
    templates: [usage-profile.mdx]
---

# sb-inventory — ground truth, not trust

Vibe-coded apps ship ~30% slop. This skill replaces "trust the AGENTS.md / CLAUDE.md / DESIGN.md" with
"see what's actually imported." Read `CONTEXT.md` for the real/vendor/dead/kind vocabulary.
(The dominant design system here comes from **code** signals, never from a doc. If a `DESIGN.md`
brief is present, `sb-health` cross-checks its claimed colors against the code — it drifts/lies the
same way an `AGENTS.md` does.)

## Run it

```bash
SKILL=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
"$SKILL/scripts/inventory-project.sh"   # writes .storybook/project-inventory.json (atomic)
```

The script is the ground truth — do NOT recompute by hand. Read the JSON and **cite its fields**.
For the known detector gotchas (what the discovery scripts get right vs. wrong across validation runs),
load `references/field-learnings.md` **only when a count looks surprising** (a 0, an outlier, a
suspected false orphan). **Do NOT load it** for a clean first-pass inventory whose numbers look right —
the JSON fields stand on their own.

## Report (read these fields, in this order)

1. **Stack** — `libraries` (react/vite/tailwind v4|v3/shadcn/radix/baseui/r3f).
2. **Dominant design system** — `designSystem.dominant` (one of tailwind-v4/shadcn/dtcg/css-vars/
   none) + `mixed` flag. If `mixed` → tell the user the project is in transition; suggest `sb-health`.
3. **The user's own components** — `components.realCount` / `deadCount` are **domain components
   only**. Cite `components.real[]` (most-imported first) as the priority list for stories.
4. **Vendor** — `components.vendorCount` + `byKind.vendor` = shadcn `components/ui/` primitives.
   Call these out *separately*: "you also have N installed shadcn primitives — not your code, not
   slop, don't write stories for them first."
5. **Modules / support / scaffold** — `moduleCount` (`byKind.module` = types/helpers/hooks/utils/
   lib/api — non-component source), `supportCount` (`byKind.scaffold|support` = test/factory/mock +
   SB init tutorial). All excluded from the headline AND the `real[]` most-imported list, so that
   list is your prod **components**, not a `types.ts` that's imported everywhere. Mention if non-zero.
6. **Tokens** — used vs orphan. **Stories** — `orphanStories` (stories importing a component that no longer
   exists) AND **`components.storyCoverage`** — own components written vs. needed: `{real, storyFiles,
   withColocatedStory, withStory, needsCount, needsStory[]}`. Read coverage from **`withColocatedStory`**
   (own components with their *own* `<name>.stories.*`) and **`storyFiles`** (distinct story files that
   exist) — those are the hard counts. **`withStory` is a loose upper bound**: it also counts a component
   as covered when *any* story merely imports it (e.g. a dialog story importing a form to mock it), so it
   over-reports — treat `withColocatedStory ≤ real_coverage ≤ withStory`. `needsStory[]` is the "stories
   needed" worklist (the inverse of orphanStories); `refresh-usage.sh` keeps it current so `sb-stories`
   can work down `needsStory[]`.

**The fix that matters here:** the "real" list and headline are the user's authored components —
NOT 40 shadcn primitives, types, or helpers. That was the #1 inventory complaint; the `vendor`/
`support`/`scaffold` buckets exist so the headline stays clean.

## Surface it as a story

Scaffold the `ProjectInventory` wrapper so the agent + designer share the view:

```bash
"$CORE/scripts/scaffold-wrapper.sh" ProjectInventory   # → .storybook/wrappers/ (+ icons.tsx)
```

Title `Foundations/Inventory`. The wrapper reads the same JSON; no emoji (uses the shared icon set).

## Real prop usage (not just real-vs-slop)

`importers` tells you a component is *used*; it does NOT tell you **which props/variants the app
actually renders**. A shadcn `Button` may declare 6 variants but prod only ships 2 — the rest are
catalog padding. Run the usage extractor after the inventory:

```bash
"$CORE/scripts/extract-component-usage.sh"   # → .storybook/component-usage.json (atomic)
```

Per component (own + shadcn primitives, keyed by PascalCase export) it records, from JSX call sites:
`props.<name>.{count, values{value:n}, exprCount}`, `callSites`, `files[]`, and **`declaredButUnused`** —
declared props / string-union values never passed (prop-level slop). Plus a `pages` rollup. Cite these
fields; never re-grep. `sb-stories` reads this to prioritize real states and tag never-used ones.

### The component worklist — audit the system by imports (`ComponentUsage`)

For the **whole-system view** — every real UI component ranked by call-sites, *what it's nested inside*
(`parents`) / *renders* (`children`), and *which routed pages it ends up on* (directly or transitively) —
generate the component↔page import graph. It **composes** the three discovery JSONs (no new scan):

```bash
"$CORE/scripts/build-component-pages.py"   # project-inventory + component-usage + flows → component-pages.json
# (or just run "$CORE/scripts/refresh-usage.sh" — it writes all four together)
```

`build-component-pages.py` reads `component-usage.json` (callSites/props/declaredButUnused + each
component's `files`), `project-inventory.json` (each component's `file`/`kind`), and `flows.json`
(route `path` + `access` role), then writes `.storybook/component-pages.json`:
per component `{callSites, props, declaredButUnused, parents[], children[], pages[{path, title, role, storyId}]}`,
plus, when the component's own file **is** a routed page surface, `isPage:true` + `route` (the path it
serves). A page is mounted by the router as a config value (`{ component: X }`), never as JSX, so it has 0
call sites / 0 props **by construction** (accurate, not missing) — `route` lets the docs read "serves
/scheduler" instead of a misleading "0". `route` is the route it *serves*, kept out of `pages[]` (a page
listed among "pages it appears on" reads circular).
This is paired with the **bidirectional usage edges** so one file answers "where is X used" in any direction:
`fileIndex` (`<src file> → {component, kind, pages[]}`), `tokens` (`<--token> → {category, count, components[], pages[]}` —
forward), and per component a `tokens[]` array (the reverse — what that component consumes). `tokens` lists
**every declared token** (used, primitive-only, or orphan) — a token consumed only by a design-system
primitive (`src/components/ui/*.tsx`, which the inventory buckets as `vendor`/`module`, not a tracked
component) still resolves to that primitive as its consumer instead of being silently dropped, so the
explorer shows the whole palette, not just tokens that reach an app component. The `usage-index`
helper (`resolveUsage` / `UsageDetail` / `UsageDisclosure`) reads `fileIndex` so `TokenMatrix` + the Foundations
swatches turn raw paths into clickable component/page names; the **`UsageExplorer`** wrapper reads the full graph
as the one searchable "where is this used?" surface (token ⇄ component ⇄ page). This makes the old per-app
`audit-map.json` (a parallel component↔page graph) redundant.
The **`ComponentUsage`** wrapper renders it as the worklist — scaffold it with
`"$CORE/scripts/scaffold-wrapper.sh" ComponentUsage`. Pages are resolved through the render graph
(a `Rating` nested in a `CourseCard` on `/dashboard` shows `/dashboard`), so it answers *"what do we have,
how heavily used, nested where, on which screens, and what still needs a story?"* It's a static draft —
barrel/dynamic/aliased imports can under-link; verify load-bearing edges against source.

### Presenting usage (the aligned flow — match this in Storybook)

**Usage lives where you look — embedded in each section's Docs, no separate "usage" pages/section.**

1. **One docs block, every Docs page (default, zero files).** Ship the `UsageSection` wrapper and add it
   to the **global autodocs layout** in `.storybook/preview.ts`. It adds a real-usage section to each
   section's Docs, reading the matching audit output file (so foundations need `tags: ['autodocs']`):
   - **Components** → `component-pages.json` — the `ComponentContext` "Where it's used" map (the pages it
     lands on, what nests it, what it renders, the tokens it pulls), plus the real component from `src/`
     rendered in isolation. **Collapsed by default** for fast scanning: a compact "where it's used" eyebrow
     + **adaptive meta** is always visible (only the non-zero counts — no redundant big `<h2>`, the Docs
     title already names the component); the map expands on demand (native `<details>`, open on the
     standalone audit page). The meta is **page-aware**: a real component reads "5 call sites · 2 props ·
     has a story", while a routed page (`isPage`) drops call-sites/props and leads with the route it serves
     — "serves /scheduler · 5 renders · has a story". A "what is this + where it's from" provenance band
     sits inside it but is **off by default** (demo-only; reach it with `setProvenance()`). Reuses the
     Usage-explorer stamp.
   - **Pages/*** → the real app page from `src/`, rendered through the provider/Inertia mocks (sb-setup) —
     the actual page, not a mockup. Its "what is this?" provenance band is **off by default** (the page
     story carries the content; the band only returns when provenance is switched on).
   - **Foundations** → nothing from `UsageSection`. Each Foundation renders its own self-contained story:
     `Colors` → `TokenMatrix` (value · mapping · adoption — NOT health; leave the `health` prop off, it
     defaults false), `Health` → `DesignSystemHealth` (full findings), `Icons` → `IconMatrix`,
     `Typography`/`Scales` → the token displays. The old per-foundation
     "Real usage in this app" bands were removed: Health duplicated the DesignSystemHealth story, and
     per-token "where used" doesn't resolve for type/scale (declared names ≠ referenced names) — that lives
     in the Usage explorer + the Colors adoption column.

   No sidebar clutter; no separate pages.
   ```ts
   import { Title, Subtitle, Description, Primary, Controls, Stories } from '@storybook/addon-docs/blocks';
   import { UsageSection } from './wrappers/UsageSection';
   // parameters.docs.page = () => (<><Title/><Subtitle/><UsageSection/><Description/><Primary/><Controls/><Stories/></>)
   // ↑ order is yours — UsageSection here puts the real-usage status band at the TOP; move it last for the bottom.
   ```
   `refresh-usage.sh` keeps the JSONs current; a Storybook rebuild reflects them. The generator stamps
   **nothing** by default — `scripts/scaffold-usage-mdx.py --per-component` is an opt-in escape hatch for
   standalone `<Name>.usage.mdx` pages rendered from `templates/usage-profile.mdx` (rarely needed).
2. **A visual usage grid is a FLAT story in the component's own CSF — never a separate file** (a new file =
   a new sidebar folder). Add an export next to the others using the `usage` prop:
   `<StateGrid component={X} usage={usageJson.components.X} states={…} />` (or `StateMatrix`); for tokens,
   `<TokenUsageGrid>`.

Limits: `{...spread}`/dynamic values are counted as `exprCount` ("set from a variable"), not resolved (static analysis).

## Full Setup sweep

This skill owns the inventory. For the rest of discovery, run the sibling skills (each owns its
script, writes atomic JSON, no sub-agent needed): **`sb-flows`** (routes/edges/nav → `flows.json`),
then **`sb-stories`** generates `component-states.json` + `prop-shapes.json` when it needs them.
Read the JSONs; never re-grep source.

## Never (and the non-obvious why)

- **NEVER decide the dominant design system from a doc** — read **code** signals (imports, call sites).
  A `DESIGN.md`/`AGENTS.md` is a *claim* that drifts; the imports are what actually ship.
- **NEVER recompute a count by hand or re-grep source** — the discovery scripts already wrote it to
  `.storybook/*.json`. Cite the field. Re-deriving by eye drifts from what the wrappers render and
  burns context the JSON already paid for.
- **NEVER trust an edge-case count blind** — a `0`, an outlier, or a suspected false orphan? *Then*
  load `references/field-learnings.md` (BSD-sed `\s`, Tailwind-utility token consumption, component-vs-page
  conflation). The static scan has known blind spots; the field notes name them.
- **NEVER put a usage grid in its own file** — it's a FLAT story in the component's own CSF. A new file
  is a new sidebar folder; the grid belongs beside the states it summarizes.

## Next

Append a one-line finding to `.storybook/audit/findings.md`, then ask the hub (`/sb-hub`) — usually
`sb-flows` (capture the app-map) or `sb-stories <TopComponent>`.
