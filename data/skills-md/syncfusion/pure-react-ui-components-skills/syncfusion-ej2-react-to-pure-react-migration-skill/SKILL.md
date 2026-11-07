---
name: syncfusion-ej2-react-to-pure-react-migration-skill
description: Migrate Syncfusion EJ2 React components to Syncfusion Pure React components. Use when a user has EJ2 React reference files (e.g. `@syncfusion/ej2-react-buttons`, `ButtonComponent`, `cssClass`, unprefixed event props, `<Inject services=[...]/>`, `<XxxDirective>` patterns, class-component lifecycle methods, or `enableRtl`/`enableMask`/`e-flat`/`e-success` style props) and wants to convert them to the new `@syncfusion/react-*` packages. Apply this skill whenever user code references these patterns, even if the destination component lives in a different package or keeps the same display name.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion EJ2 React → Pure React Migration

Global migration workflow and shared conventions for moving an app from
Syncfusion EJ2 React to Syncfusion Pure React.

> **Where to look for specifics:**
> - **Component props / events / methods / enums / templates:**
>   `references/<componentName>.md`
> - **EJ2-side API surface that the migration is moving away from:** the
>   Syncfusion EJ2 React documentation.
> - **Per-component feature configuration** (filtering, paging, sorting,
>   virtualization, custom templates, sub-component composition, axis
>   options, etc.): `references/<componentName>.md`.
>
> SKILL.md is intentionally **not** a component API catalog. It only
> documents rules that apply across multiple components or that govern how
> migration work is performed.

> **Availability:** Pure React components are available from
> Syncfusion v29.2.4. Only a subset of EJ2 components has been published
> in Pure React — if a target component is not listed in the
> [component naming table](#component-naming) below, it has not been
> published yet and cannot be migrated with Pure React alone.

---

## Source hierarchy

When migrating a code surface, load information in this order:

1. `SKILL.md` — global migration workflow, package transformations,
   naming transformations, shared conventions, repository-wide patterns.
2. `references/<componentName>.md` — the component's own props / events /
   methods / enums / templates / interfaces / rendering behavior /
   feature configuration / component-specific limitations.

`references/<componentName>.md` is the **primary source** for component
migration — for any prop, method, union, enum, event, or other detail,
consult that file, never SKILL.md. If guidance lives in both places,
prefer the reference; only cross-cutting behavior belongs here.

---

## Component naming

Drop the `Component` suffix on the EJ2 class to derive the Pure React
identifier. A handful of components also change their root name:

| EJ2 React | Pure React | EJ2 package area |
| --- | --- | --- |
| `AutoCompleteComponent` | `<Autocomplete>` | `ej2-react-dropdowns` |
| `ButtonComponent` | `<Button>` | `ej2-react-buttons` |
| `CalendarComponent` | `<Calendar>` | `ej2-react-calendars` |
| `ChartComponent` | `<Chart>` | `ej2-react-charts` |
| `CheckBoxComponent` | `<Checkbox>` | `ej2-react-buttons` |
| `ChipListComponent` | `<Chip>` / `<ChipList>` (see reference file) | `ej2-react-buttons` |
| `ComboBoxComponent` | `<ComboBox>` | `ej2-react-dropdowns` |
| `ContextMenuComponent` | `<ContextMenu>` | `ej2-react-navigations` |
| `DatePickerComponent` | `<DatePicker>` | `ej2-react-calendars` |
| `DateRangePickerComponent` | `<DateRangePicker>` | `ej2-react-calendars` |
| `DateTimePickerComponent` | `<DateTimePicker>` | `ej2-react-calendars` |
| `DialogComponent` | `<Dialog>` | `ej2-react-popups` |
| `DropDownButtonComponent` | `<DropDownButton>` | `ej2-react-splitbuttons` |
| `DropDownListComponent` | `<DropDownList>` | `ej2-react-dropdowns` |
| `FabComponent` | `<Fab>` | `ej2-react-buttons` |
| `FormValidator` (class instance) | `<Form>` | `ej2-react-inputs` |
| `GridComponent` | `<Grid>` | `ej2-react-grids` |
| `ListViewComponent` | `<ListView>` | `ej2-react-lists` |
| `MenuComponent` | `<Menu>` | `ej2-react-navigations` |
| `MessageComponent` | `<Message>` | `ej2-react-notifications` |
| `MultiSelectComponent` | `<MultiSelect>` | `ej2-react-dropdowns` |
| `NumericTextBoxComponent` | `<NumericTextBox>` | `ej2-react-inputs` |
| `RadioButtonComponent` | `<RadioButton>` | `ej2-react-buttons` |
| `ScheduleComponent` | `<Scheduler>` | `ej2-react-schedule` |
| `SkeletonComponent` | `<Skeleton>` | `ej2-react-notifications` |
| `SplitButtonComponent` | `<SplitButton>` | `ej2-react-splitbuttons` |
| `SwitchComponent` | `<Switch>` | `ej2-react-buttons` |
| `TextAreaComponent` | `<TextArea>` | `ej2-react-inputs` |
| `TextBoxComponent` | `<TextBox>` | `ej2-react-inputs` |
| `TimePickerComponent` | `<TimePicker>` | `ej2-react-calendars` |
| `ToastComponent` | `<Toast>` | `ej2-react-notifications` |
| `ToolbarComponent` | `<Toolbar>` | `ej2-react-navigations` |
| `TooltipComponent` | `<Tooltip>` | `ej2-react-popups` |
| `AccumulationChartComponent` | `<PieChart>` | `ej2-react-charts` |

> Components that already lack the suffix (e.g. `<Form>`, `<Menu>`) keep
> their name. When in doubt, consult `references/<componentName>.md`.

### Collection directives → composite components

EJ2 React uses framework-style `<XDirective>` / `<XCollectionDirective>`
pairs. Pure React replaces these with dedicated sub-component compositions:

- `<XDirective>` / `<XCollectionDirective>` patterns → read the
  per-component reference for the exact replacement component family.
- `<Inject services={[Service]} />` — **drop entirely**. The feature is
  re-enabled in Pure React via the appropriate `*Settings` / `*Settings={{
  enabled }}` prop on the root component — see the reference file for
  the component that owned the Inject.

---

## Package transformations

EJ2 React packages share `@syncfusion/ej2-react-<area>`. Pure React
packages drop the `ej2-` prefix; some areas also change their final
segment:

| EJ2 package | Pure React package |
| --- | --- |
| `@syncfusion/ej2-react-buttons` | `@syncfusion/react-buttons` |
| `@syncfusion/ej2-react-calendars` | `@syncfusion/react-calendars` |
| `@syncfusion/ej2-react-charts` | `@syncfusion/react-charts` |
| `@syncfusion/ej2-react-dropdowns` | `@syncfusion/react-dropdowns` |
| `@syncfusion/ej2-react-grids` | `@syncfusion/react-grid` |
| `@syncfusion/ej2-react-inputs` | `@syncfusion/react-inputs` |
| `@syncfusion/ej2-react-lists` | `@syncfusion/react-lists` |
| `@syncfusion/ej2-react-navigations` | `@syncfusion/react-navigations` |
| `@syncfusion/ej2-react-notifications` | `@syncfusion/react-notifications` |
| `@syncfusion/ej2-react-popups` | `@syncfusion/react-popups` |
| `@syncfusion/ej2-react-schedule` | `@syncfusion/react-scheduler` |
| `@syncfusion/ej2-react-splitbuttons` | `@syncfusion/react-splitbuttons` |

Areas not listed above have not yet been published as Pure React packages —
do not attempt migration for those.

---

## License migration

When migrating, update the license registration as shown below.

### Code-based registration

**Before (EJ2 React):**

```tsx
import { registerLicense } from '@syncfusion/ej2-base';

registerLicense('YOUR_LICENSE_KEY');
```

**After (Pure React):**

```tsx
import { registerLicense } from '@syncfusion/react-base';

registerLicense('YOUR_LICENSE_KEY');
```

Register the license once during application startup (for example, in
`main.tsx`) before rendering any Syncfusion components.

### CLI-based registration

**Before (EJ2 React):** `npx syncfusion-license activate`

**After (Pure React):** `npx syncfusion-react-license activate`

The existing `syncfusion-license.txt` file and `SYNCFUSION_LICENSE`
environment variable continue to work without changes.

### Summary

| EJ2 React | Pure React |
| --- | --- |
| `@syncfusion/ej2-base` | `@syncfusion/react-base` |
| `npx syncfusion-license activate` | `npx syncfusion-react-license activate` |
| `syncfusion-license.txt` | No change |
| `SYNCFUSION_LICENSE` | No change |

---

## Theming

EJ2 React themes are CSS packages; Pure React theming replaces them with
imports of themed CSS files. The Pure React side supports only
`material`, `tailwind`, and `bootstrap`. Older EJ2 themes (Fabric,
Fluent, Fluent 2, High Contrast, Tailwind 3, Bootstrap 4, Bootstrap 5,
Bootstrap 5.3, Material 3) have no Pure React counterpart — the app
must switch to one of the three supported themes.

### Theme import patterns

Pick **one** of the two patterns in the migration target, using the
appropriate theme package name as the value for `<themeName>`:

```css
/* Component-scoped: ship styles for one component only. */
@import "@syncfusion/react-<themeName>-theme/styles/<componentName>/index.css";

/* Theme-global: ship styles for every component in the theme. */
@import "@syncfusion/react-<themeName>-theme/styles/<themeName>.css";
```

`<themeName>` is one of `material`, `tailwind`, `bootstrap`.
`<componentName>` is the Pure React component name — see the
[component naming table](#component-naming).

### Theme migration workflow

1. Strip every `@syncfusion/ej2-*-theme` import from the codebase.
2. If the EJ2 theme is not `material`, `tailwind`, or `bootstrap`,
   switch to one of those three and remove the EJ2-only theme references.
3. Add the chosen Pure React theme import at the application root using
   either the component-scoped or theme-global pattern above.
4. Eyeball-test the app — Pure React CSS hooks are a visual redraw of
   the EJ2 themes and are not byte-identical.

---

## Version

Pure React components are available from Syncfusion **v29.2.4**; the
standalone Pure React theme packages require **v34.1.29** or later.
See the [Version check](#version-check) subsection in the migration
workflow for the major-version rule and the `node_modules` inspection
rule.

---

## Icons

EJ2 React icons come from `@syncfusion/ej2-icons` as CSS class strings
(e.g. `e-icons e-add`). Pure React icons ship from
`@syncfusion/react-icons` as React modules that you import and render
as components. The specific icon names available, the way they accept
color/size props, and any per-component `icon`/`iconCss` semantics are
documented in each component's reference file.

---

## Shared migration conventions

The conventions below are shared by multiple components. For the exact
prop / event / method / enum / template names involved in a given
component, read `references/<componentName>.md`.

- **Drop `Component`/`Directive`/`CollectionDirective` suffixes** — see [Component naming](#component-naming).
- **Strip `<Inject services={[...]} />`** — replaced by Settings props on the root component; details are per-component.
- **Prefix event handlers with `on`** (e.g. `change` → `onChange`); any specific rename is in the per-component reference.
- **Move locale and RTL off the component onto `<Provider>`** — see [Provider usage](#provider-usage). Same applies to `currencyCode`, `ripple`, and `animate` when they would otherwise repeat across components.
- **Replace class refs with `useRef<T>(null)`** — see [Refs & imperative APIs](#refs--imperative-apis).
- **Replace lifecycle props (`created`/`destroyed`) and imperative `destroy()` with React `useEffect`** — see [Lifecycle translation](#lifecycle-events--react-hooks).

When a convention is mentioned in a reference file too, the reference
file is authoritative for that component.

### Provider usage

`<Provider>` is the Context-API wrapper for shared Syncfusion Pure
React settings. It distributes direction, locale, currency code,
ripple, and animation values to every Syncfusion Pure React component
inside its subtree, so the application can configure shared behaviour
once instead of repeating it on each component tag. The component is
imported from `@syncfusion/react-base`.

Migration for `enableRtl`, `Animation` from `@syncfusion/ej2-base` is hanlded like below in React with additional features.

#### When it is required

`<Provider>` is required whenever the migrated app needs any of the
following to apply to more than one component at once:

- The EJ2 `enableRtl` prop — must be lifted off individual components
  onto `<Provider dir="rtl">`.
- The EJ2 `locale` prop — must be lifted off individual components
  onto `<Provider locale="…">`.
- A default currency for components that render currency-formatted
  values — set `<Provider currencyCode="…">`.
- A global ripple toggle — set `<Provider ripple={…}>`.
- A global animation toggle — set `<Provider animate={…}>`.

A single component that needs only one of these can still set the prop
directly on its own tag. `<Provider>` is the mechanism for sharing a
value across multiple components in the same scope.

#### Context-sharing behavior

`<Provider>` exposes its settings through React context. Every
Syncfusion Pure React component inside the subtree automatically reads
`dir`, `locale`, `currencyCode`, `ripple`, and `animate` from the
nearest enclosing `<Provider>`. A component-level prop (when one
exists) still overrides the Provider context for that single
component; nested `<Provider>` scopes override the outer Provider.

#### Migration patterns

Prop renames when lifting from per-component to `<Provider>`:

| EJ2 React prop | Pure React Provider prop |
| --- | --- |
| `enableRtl` | `dir="rtl"` |
| `locale` | `locale` |
| `currencyCode` | `currencyCode` |
| `ripple` | `ripple` |
| `animate` | `animate` |

- Move `enableRtl` and `locale` off every component instance onto the
  enclosing `<Provider>` scope.
- Use `<Provider>` for `currencyCode`, `ripple`, and `animate` when
  those values would otherwise repeat across components.
- Nest `<Provider>` scopes when subtrees need different settings — the
  inner Provider wins for the props it sets.

#### Provider props

The full prop list (defaults shown):

| Prop | Type | Default | Description |
| --- | --- | --- | --- |
| `animate` | `boolean` | `true` | Enables transition animations on wrapped components. |
| `children` | `node` | — | The subtree that will inherit the Provider context. |
| `currencyCode` | `string` | `"USD"` | Default currency code for components that format currency. |
| `dir` | `string` | `"ltr"` | Text direction. Use `"rtl"` for right-to-left layouts. Replaces the EJ2 `enableRtl` prop. |
| `locale` | `string` | `"en-US"` | Locale identifier. Replaces the EJ2 `locale` prop. |
| `ripple` | `boolean` | `false` | Enables the ripple interaction on wrapped components. |


#### Application-level setup

Place `<Provider>` at the highest level that needs the settings —
typically the application root, immediately inside
`ReactDOM.createRoot`:

```tsx
import { Provider } from "@syncfusion/react-base";

<Provider locale="en-US" currencyCode="USD" dir="ltr" ripple={false} animate={true}>
  {/* the application tree */}
</Provider>
```

#### Cross-component usage patterns

Wrap a page — or any subtree — once rather than passing the same
`dir`, `locale`, `currencyCode`, `ripple`, or `animate` props to
every component tag. When two subtrees need different settings — for
example, an RTL sidebar inside an LTR application — nest `<Provider>`
scopes:

```tsx
<Provider locale="en-US" dir="ltr">
  {/* LTR subtree */}
  <Provider dir="rtl">
    {/* RTL subtree */}
  </Provider>
</Provider>
```

### Refs & imperative APIs

EJ2 React uses class refs that bind the entire component instance and
allow imperative method calls (`addRecord`, `showSpinner`, …). Pure
React uses typed refs (`useRef<T>(null)`) that expose only the methods
the new component exposes.

- The shape and naming of imperative methods are component-specific —
  see `references/<componentName>.md`.
- Some methods change name or return type when migrating; the
  per-component reference is the source of truth for that.
- Where the EJ2 method took row/column indexes, the Pure React method
  typically takes the primary key and field name — see the Grid
  reference for the worked example pattern.

### Lifecycle events → React hooks

EJ2's `created` / `destroyed` callback props and imperative `destroy()`
are gone. Pure React equivalents:

| EJ2 React | Pure React |
| --- | --- |
| `created={fn}` | `useEffect(() => { fn(); }, [])` |
| `destroyed={fn}` | `useEffect(() => { return () => fn(); }, [])` |
| `instance.destroy()` | `useEffect` cleanup |

Some lifecycle *event names* are renamed rather than dropped (e.g.
`beforeOpen` may become `onOpen` in some components). Check the
reference file for the specific component.

---

## Migration workflow

Run this loop for every EJ2 React file or folder you migrate to Pure
React. Treat the compile step as the gate — if it fails, reopen the
loop and pick the fix branch before moving on.

```
Migration Spec (references/*.md)
        ↓
Apply mappings
        ↓
Generate code
        ↓
Compile
        ↓
Success?
├─ Yes → Stop
└─ No
        ↓
Is mapping available in MD?
├─ Yes → Fix
└─ No
        ↓
Inspect node_modules
```

### Steps

1. **Read the migration spec.** Open every
   `references/<componentName>.md` covering the components in scope —
   the references are the only source of truth for component-specific
   renames; SKILL.md deliberately does not duplicate those tokens.
   Cross-check the [component naming table](#component-naming); if any
   component is missing, stop and surface that to the user.
2. **Apply the mappings.** Translate the source to Pure React using
   only the tokens documented in the references plus the cross-cutting
   conventions in this file (package renames, `<Inject>` removal, event
   `on` prefix, `<Provider>` lifting, refs, lifecycle, themes).
3. **Generate code.** Emit the migrated file, scoped strictly to what
   the references justify — do not invent unmapped renames.
4. **Compile.** Run the project's typecheck / build. Treat compile
   success as the stop signal.
5. **Failure branch.** When the compile fails, check whether the
   mapping for the failing token is in `references/*.md`:
   - **Yes — fix it.** Apply the documented mapping, regenerate, and
     return to step 4.
   - **No — inspect `node_modules`.** Open the installed package
     source only when the references are silent, then add the
     discovered mapping back to the relevant
     `references/<componentName>.md` so the next run can fix without
     leaving the spec.

### Version check

When confirming whether the target project can host Pure React
components, compare **major versions only**:

- Pure React components require Syncfusion **v29** or later.
- Pure React standalone theme packages require **v34** or later.

A minor-version mismatch (for example, `29.2.4` vs. `29.6.0`) is
acceptable and must not trigger a `node_modules` inspection. Inspect
`node_modules` only when the compile step fails — never as part of the
upfront version check. EJ2 themes other than `material`, `tailwind`,
or `bootstrap` still cannot be carried over.

---

## Quick-reference checklist

Use this checklist when reviewing a migrated file. SKILL.md intentionally
limits itself to migration behavior — every concrete prop / event /
method / enum token to scrub or replace lives in
`references/<componentName>.md` (consult that file for the exact strings).

- [ ] Every imported `@syncfusion/ej2-react-*` and `@syncfusion/ej2-*` package has been swapped
      for its Pure React counterpart.
- [ ] No `<…Component>` / `<…Directive>` / `<…CollectionDirective>`
      identifier remains on a component tag.
- [ ] No `<Inject services={[…]}/>` block remains.
- [ ] All EJ2 prop tokens covered by a per-component reference have
      been replaced — see the corresponding `references/<componentName>.md`
      for the per-prop rename.
- [ ] All EJ2 event handler tokens covered by a per-component
      reference have the `on` prefix — see the same reference.
- [ ] All EJ2 enums and value-string tokens (calendar types, sort
      directions, color/size/variant class strings, etc.) have been
      replaced by their typed Pure React equivalents — see the same
      reference.
- [ ] `enableRtl` / `locale` props are no longer on any component
      instance; the relevant scope is wrapped in `<Provider dir=… locale=…>`.
      Shared `currencyCode` / `ripple` / `animate` values are also
      scoped through `<Provider>` rather than repeated on individual
      components.
- [ ] Lifecycle props (`created` / `destroyed`) and any imperative
      `destroy()` call have been replaced by `useEffect`.
- [ ] Class refs have been replaced by `useRef<T>(null)` with the
      typed reference shape documented in the per-component reference.
- [ ] EJ2 theme CSS imports are gone; the Pure React theme import is in
      place at the appropriate scope and uses one of the three
      supported themes.
- [ ] Target Syncfusion version is >= v29.2.4 (and >= v34.1.29 if using
      the new theme packages).
