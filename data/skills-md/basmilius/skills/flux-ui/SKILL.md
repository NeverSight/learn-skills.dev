---
name: flux-ui
description: >-
  Use when building, editing, or reviewing Vue 3 UI with Flux (by Bas Milius):
  @flux-ui/components (docs at flux-ui.dev) and its siblings @flux-ui/application
  (app shell / dashboards) and @flux-ui/statistics (KPIs/charts). Trigger on
  Flux-prefixed components (FluxPrimaryButton, FluxFormField, FluxPane), on
  FluxRoot / showConfirm / showSnackbar / showPrompt / showAlert, on its
  composables (useBreakpoints, useFluxStore, use*Injection), or any import from
  @flux-ui/*. This is the Vue 3 Flux (basmilius), NOT the Livewire/Blade Flux
  from fluxui.dev and NOT the Flux web-components library; never mix their
  syntaxes.
license: MIT (skill content); Flux itself is MIT, by Bas Milius
---

# Flux UI (Vue 3)

Flux is an opinionated **Vue 3** component library by Bas Milius: **named exports**
from `@flux-ui/components` (SFCs, `<script lang="ts" setup>`), documented at
**flux-ui.dev**, which is the source of truth for exact props/emits/slots. Real apps
also use the siblings **`@flux-ui/application`** (app shell) and
**`@flux-ui/statistics`** (KPIs/charts).

**This skill is a router.** It encodes the durable judgment (which component, how to
compose, the naming traps) and defers prop tables to the docs. Pick the right
reference file below; do not work from memory for exact props.

## 1. Disambiguation (read first)

"Flux UI" is overloaded. This skill is ONLY **basmilius/flux**: Vue 3, npm
`@flux-ui/components`, docs at flux-ui.dev. Do NOT apply it to, or mix syntax with:

- **livewire/flux** (fluxui.dev): a Laravel/Livewire/Blade kit using `flux:button`
  style tags. Different project.
- The **Flux web-components** library (`j-flex`, `j-box`, ...). Different again.

Emitting a `flux:button` Blade tag or a `j-` element for a Vue Flux task means you
mixed libraries: stop and use the `Flux`-prefixed Vue component.

## 2. Setup (the three that silently break builds)

Full install, Vite preset, FluxRoot, icons and tokens: `references/conventions.md`.
The traps worth knowing up front:

- **Vue 3.6 pre-release peer.** Flux 3.x does not accept `vue@latest` (3.5.x fails
  the peer). The accepted range moves as 3.6 approaches stable, so read it from the
  package itself (`npm view @flux-ui/components peerDependencies`) instead of a
  build named here. Install Flux and `@basmilius/vite-preset` with the `@latest`
  dist-tag, not a guessed caret range.
- **One Vite plugin per Flux package** (`flux()`, `fluxApplication()`,
  `fluxStatistics()`). A missing plugin resolves that package to dist with unimported
  CSS, giving an **unstyled shell / charts**.
- **FluxRoot is required.** Mount one as the app wrapper, or `showAlert` /
  `showConfirm` / `showPrompt` / `showSnackbar`, `FluxOverlay` and `FluxTooltip`
  throw.

## 3. The naming rule (most common trap)

Names are `Flux`-prefixed PascalCase. **Most** are just the doc path PascalCased
(`form/field` → `FluxFormField`), but several groups deviate, and guessing those is
the single most common mistake. Three patterns to distrust:

- **Variant moves to the front:** `button/primary` → `FluxPrimaryButton`,
  `pane/clickable` → `FluxClickablePane`.
- **A path segment is dropped:** `layout/flex` → `FluxFlex`, `form/toggle` →
  `FluxToggle`.
- **Reordered / resuffixed:** `form/slider/ranged` → `FluxFormRangeSlider`,
  `filter/async-option` → `FluxFilterOptionAsync`.

Treat anything under `button/*`, `form/*` (controls), `layout/*`, `pane/*` and
`filter/*` as suspect and look it up. The base button is `FluxButton`; grouping
wrappers have their own names (`FluxButtonStack`, `FluxFormRadioGroup`, ...). The
complete build-verified list with every trap is `references/component-index.md`
(start there).

## 4. Choosing a component (selection map)

Match the need to a component; confirm exact names in `references/component-index.md`.

- **Buttons** → `FluxPrimaryButton` / `FluxSecondaryButton` /
  `FluxDestructiveButton`, `FluxSplitButton` (action+menu), `FluxButtonStack` (row).
  Not bare `FluxButton`. Plain link → `FluxLink`.
- **Forms** → wrap each control in a `FluxFormField` inside a `FluxForm`. Trap names:
  toggle is `FluxToggle`, stepper `FluxQuantitySelector`, range `FluxFormRangeSlider`,
  dates `FluxFormDateInput`. Composition: `references/forms.md`.
- **Dialogs & feedback** → programmatic `showConfirm` / `showPrompt` / `showAlert` /
  `showSnackbar`; rich or deep-linkable `FluxOverlay` / `FluxSlideOver`; inline
  `FluxNotice` / `FluxBadge` / `FluxTooltip`. `references/dialogs-and-feedback.md`.
- **Layout, tables & navigation** → `FluxFlex` / `FluxGrid` / `FluxContainer`,
  `FluxPane` (the card surface), `FluxSplitView`; `FluxDataTable` / `FluxTable`,
  `FluxKanban`, `FluxTreeView`, `FluxCalendar`; `FluxMenu`, `FluxTabs`, `FluxStepper`,
  `FluxCommandPalette`, `FluxSegmentedControl`. `references/components.md`.
- **Dashboard / multi-page app** → the **`@flux-ui/application`** shell +
  **`@flux-ui/statistics`** for KPIs/charts, not hand-rolled layout.
  `references/patterns.md` §6, `references/ecosystem.md`.
- **Typography / text** → `FluxText` (Flux type scale: size/weight/color, tabular
  figures, truncate), not raw HTML + custom CSS.
- **Composables** → `useBreakpoints` (responsive), `useFluxStore` (global store),
  `use*Injection` (custom controls). `references/conventions.md`.

## 5. Composition & conventions (the load-bearing rules)

Copy-ready skeletons (app shell, CRUD form, data table, dashboard, dialogs) live in
`references/patterns.md`; the cross-cutting rules in `references/conventions.md`.
Getting the wrapper nesting right matters more than props. Know these before opening
a file:

- **Form:** `FluxForm` › `FluxPaneBody` › `FluxFormField` (label/hint/error) ›
  control; submit is a `FluxPrimaryButton is-submit`. **Pane:** `FluxPane` ›
  `FluxPaneHeader` / `FluxPaneBody` / `FluxPaneFooter`.
- **Split button:** both halves must be the **same** variant (the dropdown arrow is a
  `FluxSecondaryButton` internally, so the `#button` slot holds a
  `FluxSecondaryButton` too). `references/patterns.md` §5.
- **Overlay / slide-over `v-if`:** put it on the pane **inside**, never on the surface
  itself (keep `@close` there), or it unmounts instantly and skips its leave
  transition. `references/dialogs-and-feedback.md`.
- **Icons** are registered Font Awesome name strings; also register each component's
  "Required icons" from its doc page. **Trap:** `FluxIcon` / `FluxBoxedIcon` take the
  icon via `name`, not `icon`.
- **`gap` / spacing** = a number in pixels; **colors** = `FluxColor` tokens
  (`gray | primary | danger | info | success | warning`); dark mode is built in.
- **Types** (`FluxIconName`, `FluxColor`, `FluxTo`, ...) import from
  **`@flux-ui/types`**, NOT `@flux-ui/components` (type error otherwise).
- **Every component must be imported** or Vue renders the unknown tag literally and
  lowercased (silent, not a build error).

Depth for all of these: `references/conventions.md`.

## 6. When you need exact props

Never assume a prop exists: open the component's doc page (every URL is in
`references/component-index.md`) for its Props / Emits / Slots and the exact import.

## Reference files

- `references/component-index.md` - the complete, build-verified list of every
  component and transition, with doc URLs and the naming traps. **Start here.**
- `references/conventions.md` - install, Vite preset, FluxRoot, Font Awesome
  registration, routing/Nuxt, design tokens, colors, dark mode, types, prop-vs-slot,
  and the composables / global API.
- `references/patterns.md` - idiomatic end-to-end skeletons from a production app: app
  shell, CRUD form, data table + filters, the confirm→act→snackbar loop, pane
  composition, and the dashboard.
- `references/components.md` - choosing and composing the layout, table, and
  navigation components (which one, and how the pieces fit).
- `references/forms.md` - the form group, the Field composition, controls, and the
  CRUD-form pattern.
- `references/dialogs-and-feedback.md` - overlay vs programmatic, the show* functions
  and their real return types, notices and inline feedback.
- `references/ecosystem.md` - the sibling packages `@flux-ui/application` (app shell)
  and `@flux-ui/statistics` (KPIs/charts), with their export surface.
