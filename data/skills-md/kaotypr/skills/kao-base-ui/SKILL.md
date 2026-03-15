---
name: kao-base-ui
description: >
  Guide for building UI with Base UI React (@base-ui/react), a headless, accessible component
  library using compound component patterns. Use this skill whenever the user is building or
  modifying any user interface in React, including forms and validation, navigation and menus,
  modals and overlays, selection controls, toast notifications, accordions, tabs, or any
  interactive UI component. Also trigger when the user mentions @base-ui/react, Base UI,
  headless components, migrating from Radix UI, or asks about accessible component patterns.
  Even if the user does not explicitly mention Base UI, use this skill whenever they are
  creating React UI components, building a design system, or working on frontend user
  experience.
license: MIT
metadata:
  author: kaotypr
  version: "1.1.0"
---

# Base UI React

**Package**: `@base-ui/react` v1.2.0
**Status**: Stable (production-ready)
**React**: 19+
**Components**: 36+

## Installation

```bash
pnpm add @base-ui/react
```

**Required CSS** — add to your app root to create a stacking context for portaled components:

```css
#root {
  isolation: isolate;
}
```

## Architecture

Base UI implements a **compound component** pattern where each component is a namespace with sub-parts. All imports use sub-path format:

```tsx
import { Select } from '@base-ui/react/select';
import { Dialog } from '@base-ui/react/dialog';
import { Tooltip } from '@base-ui/react/tooltip';
```

### Three Render Patterns

Every component supports three ways to control its rendered output:

**1. Direct Children (Default)** — component renders its default HTML element:
```tsx
<Dialog.Trigger>Open</Dialog.Trigger>
```

**2. Render Element** — pass a JSX element to the `render` prop:
```tsx
<Dialog.Trigger render={<a href="#">Open</a>} />
```

**3. Render Function** — full control via callback receiving `(props, state)`:
```tsx
<Dialog.Trigger render={(props, state) => <MyButton {...props} active={state.open} />} />
```

> **Important**: Base UI uses the `render` prop. Never use `asChild` — that is a Radix UI concept and does not exist in Base UI.

## Floating Components: Portal > Positioner > Popup

Components like Select, Popover, Tooltip, Menu, Combobox all use the same three-layer nesting pattern for positioned overlays:

```tsx
<Component.Portal>        {/* Renders into document.body */}
  <Component.Positioner>  {/* Handles positioning relative to anchor */}
    <Component.Popup>     {/* The visible floating element */}
      {/* content */}
    </Component.Popup>
  </Component.Positioner>
</Component.Portal>
```

Never skip `Portal` or `Positioner` — the positioning system depends on this structure.

**Positioner props**: `side`, `align`, `sideOffset`, `alignOffset`, `collisionAvoidance`, `collisionPadding`

**CSS variables** available on Positioner for sizing:
- `--anchor-width`, `--anchor-height`
- `--available-width`, `--available-height`
- `--transform-origin`

## Styling with Data Attributes

Base UI exposes component state via data attributes instead of className toggles:

| Attribute | Meaning |
|---|---|
| `[data-popup-open]` | Floating element is visible |
| `[data-active]` | Tab/item is active |
| `[data-highlighted]` | Item has keyboard/mouse focus |
| `[data-checked]` | Checkbox/radio/switch is checked |
| `[data-unchecked]` | Checkbox/radio/switch is unchecked |
| `[data-disabled]` | Component is disabled |
| `[data-required]` | Field is required |
| `[data-valid]` | Field passes validation |
| `[data-invalid]` | Field fails validation |
| `[data-dirty]` | Field value has changed |
| `[data-touched]` | Field has been focused and blurred |
| `[data-side="top|right|bottom|left"]` | Floating element side |
| `[data-align="start|center|end"]` | Floating element alignment |

### Animations

Use `[data-starting-style]` and `[data-ending-style]` for enter/exit transitions:

```css
.popup {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 200ms, transform 200ms;
}

.popup[data-starting-style],
.popup[data-ending-style] {
  opacity: 0;
  transform: translateY(-8px);
}
```

## Component Categories

Components are organized into four categories. For detailed API, props, and examples, see the corresponding reference file.

### Floating Components
→ See `references/floating-components.md`

Select, Popover, Tooltip, Menu, Menubar, ContextMenu, Combobox, PreviewCard

### Overlay Components
→ See `references/overlay-components.md`

Dialog, AlertDialog, Drawer

### Form Components
→ See `references/form-components.md`

Field, Fieldset, Form, Input, Checkbox, Radio, NumberField, Slider, Switch, Toggle

### Display Components
→ See `references/display-components.md`

Accordion, Avatar, Button, Tabs, Toast, Toolbar, Progress, ScrollArea, Separator, ToggleGroup, Collapsible

### Utilities
→ See `references/utilities.md`

mergeProps, useRender, CSPProvider, DirectionProvider

## Critical Rules

### Always
- Use `Portal > Positioner > Popup` for floating components
- Add `isolation: isolate` to root CSS
- Use `align` prop (not `alignment`)
- Use `Select.Item` + `Select.ItemText` (not `Option`)
- Use `[data-active]` for Tabs (not `[data-selected]`)
- Use `mergeProps` when combining multiple prop objects
- Import from sub-paths: `'@base-ui/react/component-name'`
- Place `delay`/`closeDelay` on `Tooltip.Trigger`, not `Tooltip.Root`
- Wrap app in `Tooltip.Provider` for shared tooltip defaults

### Never
- Use `asChild` — Base UI uses `render` prop instead
- Skip `Portal` or `Positioner` for floating components
- Use Radix UI naming conventions (they differ)
- Assume Accordion allows multiple panels by default (`multiple` defaults to `false`)
- Place tooltip timing props on Root instead of Trigger
