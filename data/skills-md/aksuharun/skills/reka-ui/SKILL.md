---
name: reka-ui
description: Use when building accessible Vue.js interfaces with Reka UI (Radix Vue).
---

# Reka UI

Unstyled, accessibility-first Vue.js component library. Zero styles, WAI-ARIA compliant, keyboard navigation, and focus management built in.

```bash
npm install reka-ui
```

## Core Patterns

**Anatomy**: Root → Trigger → Portal → Content. Import named parts from `reka-ui`. Namespaced: `import { Dialog } from 'reka-ui/namespaced'` → `<Dialog.Root>`, `<Dialog.Trigger>`, etc.

**Styling**: Target `data-state`, `data-side`, `data-align`, `data-disabled`, `data-highlighted`. CSS: `.Item[data-state="open"] {}`. Tailwind: `data-[state=open]:border-b-2`. Teleported elements (portals) need `:deep()` in scoped styles.

**asChild**: Merges behavior onto the child element instead of rendering the default element. Use to render a custom element or compose multiple primitives.

**State**: Uncontrolled = `default-value` prop. Controlled = `v-model` (or `:model-value` + `@update:model-value`).

**Animation**: CSS keyframes on `data-state` (Reka suspends unmount during exit), Vue `<Transition>`, or Motion Vue (`motion-v`) with `AnimatePresence`.

**Nuxt**: `modules: ['reka-ui/nuxt']` — auto-imports all components.

**RTL**: `<ConfigProvider dir="rtl">` wraps the app.

**Dates**: Install `@internationalized/date`. `v-model` on calendar/date components accepts `DateValue` objects.

**Virtualization**: `*Virtualizer` components for large lists. Requires fixed-height parent, `estimateSize`, `textContent` props. Filter items manually before passing.

## References

Read only the file relevant to the current task.

- **[references/components-a-l.md](references/components-a-l.md)** — Anatomy, data attributes, CSS variables, and key notes for components Accordion through Listbox.

- **[references/components-m-z.md](references/components-m-z.md)** — Anatomy, data attributes, CSS variables, and key notes for components Menubar through Tree.

- **[references/guides.md](references/guides.md)** — Styling, composition (asChild), animation, controlled state, dates, i18n/RTL, SSR, virtualization, namespaced imports, inject context, migration guide.

- **[references/utilities.md](references/utilities.md)** — Primitive, Slot, ConfigProvider, VisuallyHidden, Presence, FocusScope, and composables (useForwardPropsEmits, useFilter, useDateFormatter, etc.).
