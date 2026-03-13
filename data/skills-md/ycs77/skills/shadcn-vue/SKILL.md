---
name: shadcn-vue
description: Component usage patterns for shadcn-vue — a Vue component distribution system built on Reka UI and Tailwind CSS. Covers component APIs, forms with VeeValidate/TanStack Form, data tables, sidebar, charts, theming, and custom registries.
metadata:
  author: Lucas Yang
  version: "2026.02.14"
  source: Generated from https://github.com/unovue/shadcn-vue, scripts located at https://github.com/ycs77/skills
---

> The skill is based on shadcn-vue (latest, Reka UI v2 + Tailwind CSS v4), generated at 2026-02-14.

shadcn-vue is a code distribution system for Vue components. Instead of installing a package, you copy component source code into your project for full control. Components are built on Reka UI (headless primitives) and styled with Tailwind CSS.

Key conventions:
- Install components via `npx shadcn-vue@latest add <component>`
- Components live in `@/components/ui/<component>`
- Utilities in `@/lib/utils` (provides `cn` class merge helper)
- Composables in `@/composables/`
- Uses `new-york` style (default style is deprecated)
- Reka UI provides the headless primitive layer

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Project Setup & CLI | CLI commands, components.json config, project initialization | [core-setup](references/core-setup.md) |
| Theming & Dark Mode | CSS variables, color conventions, dark mode setup | [core-theming](references/core-theming.md) |

## Components

### Data Entry

| Topic | Description | Reference |
|-------|-------------|-----------|
| Button & ButtonGroup | Button variants, ButtonGroup, split buttons | [components-button](references/components-button.md) |
| Input Components | Input, InputGroup, Textarea, NumberField, InputOTP, PinInput, TagsInput | [components-input](references/components-input.md) |
| Selection Controls | Checkbox, RadioGroup, Switch, Toggle, ToggleGroup, Slider | [components-selection-controls](references/components-selection-controls.md) |
| Select & Command | Select, NativeSelect, Combobox, Command palette | [components-select](references/components-select.md) |
| Date Components | Calendar, DatePicker, RangeCalendar | [components-date-picker](references/components-date-picker.md) |

### Data Display

| Topic | Description | Reference |
|-------|-------------|-----------|
| Display Components | Card, Table, Avatar, Item, Empty, Badge, Kbd, Label, Spinner, Skeleton, Progress | [components-data-display](references/components-data-display.md) |

### Overlays

| Topic | Description | Reference |
|-------|-------------|-----------|
| Dialog & Panels | Dialog, AlertDialog, Sheet, Drawer, Popover, HoverCard, Tooltip | [components-overlay](references/components-overlay.md) |
| Menus | DropdownMenu, ContextMenu, Menubar | [components-menu](references/components-menu.md) |

### Navigation & Layout

| Topic | Description | Reference |
|-------|-------------|-----------|
| Navigation | Breadcrumb, NavigationMenu, Tabs, Pagination, Stepper | [components-navigation](references/components-navigation.md) |
| Layout & Feedback | Accordion, Collapsible, Separator, AspectRatio, Resizable, ScrollArea, Carousel, Alert, Toast/Sonner | [components-layout](references/components-layout.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Field Component | Accessible form field system with labels, descriptions, errors, groups | [features-field](references/features-field.md) |
| Forms: VeeValidate | Form validation with VeeValidate + Zod + Field component | [features-form-vee-validate](references/features-form-vee-validate.md) |
| Forms: TanStack Form | Form validation with TanStack Form + Zod + Field component | [features-form-tanstack](references/features-form-tanstack.md) |
| Data Table | TanStack Table with sorting, filtering, pagination, selection, expanding | [features-data-table](references/features-data-table.md) |
| Sidebar | Composable sidebar with menus, collapsible groups, theming | [features-sidebar](references/features-sidebar.md) |
| Charts | Unovis-based charts with ChartConfig, tooltips, legends | [features-charts](references/features-charts.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Custom Registry | Building and distributing custom component registries | [advanced-registry](references/advanced-registry.md) |
