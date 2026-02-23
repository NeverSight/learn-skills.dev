---
name: docyrus-app-ui-design
description: Design and build production-grade UI components for Docyrus React applications using preferred component libraries. Use when creating dashboards, forms, data tables, layouts, or any UI elements. Triggers on tasks involving component selection, UI design, dashboard creation, layout design, shadcn, diceui, animate-ui, docyrus-ui, reui components, or requests to build user interfaces.
---

# Docyrus App UI Design

Build polished, accessible UI components for Docyrus React applications using a curated set of 127+ pre-built components from shadcn, diceui, animate-ui, docyrus-ui, and reui libraries.

## Component Library Preferences

**Primary component libraries (in order of preference):**

1. **shadcn** — 43 core components (buttons, forms, dialogs, tables, charts)
2. **diceui** — 42 advanced components (data grids, kanban, file upload, color picker)
3. **animate-ui** — 21 animated components (sidebar, dialogs, cards, menus)
4. **docyrus** — 19 Docyrus-specific components (data grid, form fields, value renderers)
5. **reui** — 2 utility components (file upload, sortable)

**Total available**: 127 components

## Critical Design Rules

1. **Always check preferred components first** — Before implementing any new component, search the preferred components reference to find an existing match.
2. **Use AwesomeCard for dashboards** — Unless the user specifically requests a different card design, use `@docyrus/ui-awesome-card` for dashboard stat cards and metrics.
3. **Use animate-ui Sidebar for layouts** — Unless the user requests a different layout, use `@animate-ui/sidebar` for app navigation.
4. **Prefer Recharts for charting** — Use Recharts as the first choice for all data visualization needs. shadcn Chart components are built on Recharts.
5. **Icon library preference order**:
   - **First choice**: hugeicons
   - **Second choice**: fontawesome light
   - **Third choice**: lucide-icons

## Quick Start Patterns

### Dashboard with AwesomeCard

```tsx
import { AwesomeCard } from '@/components/ui/awesome-card'
import { HugeIcon } from '@/components/ui/icons'

<AwesomeCard
  title="Total Revenue"
  value="$124,500"
  icon={<HugeIcon name="dollar-circle" />}
  trend={{ value: 12.5, direction: 'up' }}
/>
```

### App Layout with animate-ui Sidebar

```tsx
import { Sidebar, SidebarContent, SidebarHeader } from '@/components/ui/sidebar'

<Sidebar>
  <SidebarHeader>
    <AppLogo />
  </SidebarHeader>
  <SidebarContent>
    <NavItems />
  </SidebarContent>
</Sidebar>
```

### Data Table with diceui

```tsx
import { DataTable } from '@/components/ui/data-table'

<DataTable
  columns={columns}
  data={projects}
  enableFiltering
  enableSorting
  enablePagination
/>
```

### Charts with shadcn + Recharts

```tsx
import { ChartContainer, ChartTooltip } from '@/components/ui/chart'
import { LineChart, Line, XAxis, YAxis } from 'recharts'

<ChartContainer>
  <LineChart data={chartData}>
    <XAxis dataKey="month" />
    <YAxis />
    <ChartTooltip />
    <Line type="monotone" dataKey="revenue" />
  </LineChart>
</ChartContainer>
```

## Component Selection Strategy

When the user requests a UI component:

1. **Search the reference** — Check `references/preferred-components-catalog.md` for existing components by name, category, or functionality
2. **Match by use case** — If multiple options exist, prefer:
   - shadcn for basic/common components
   - diceui for advanced/specialized components
   - animate-ui for components requiring animation/transitions
   - docyrus for Docyrus-specific data handling
3. **Install the component** — Use the registry install command from the catalog
4. **Reference the docs** — Point to the component's doc file for detailed usage

## Installation Pattern

All components follow the shadcn registry pattern:

```bash
# shadcn components
pnpm dlx shadcn@latest add button

# diceui components
pnpm dlx shadcn@latest add @diceui/data-table

# animate-ui components
pnpm dlx shadcn@latest add @animate-ui/sidebar

# docyrus components
pnpm dlx shadcn@latest add @docyrus/ui-awesome-card

# reui components
pnpm dlx shadcn@latest add @reui/file-upload-default
```

## Common Use Cases

| Use Case | Preferred Component | Library |
|----------|-------------------|---------|
| Dashboard cards | AwesomeCard | docyrus |
| App navigation | Sidebar | animate-ui |
| Data tables | DataTable | diceui |
| Editable grids | Data Grid | docyrus |
| Forms | Form Fields | docyrus |
| File upload | File Upload | diceui |
| Charts | Chart + Recharts | shadcn |
| Dialogs | Responsive Dialog | diceui |
| Date picker | Date Time Picker | docyrus |
| Color picker | Color Picker | diceui |
| Kanban board | Kanban | diceui |
| Timeline | Timeline | diceui |
| Rating | Rating | diceui |

## References

Read these files for detailed component information:

- **`references/preferred-components-catalog.md`** — Complete catalog of all 127 components with descriptions, install commands, and doc paths
- **`references/component-selection-guide.md`** — Decision trees and guidelines for choosing the right component for each use case
- **`references/icon-usage-guide.md`** — Icon library integration patterns and usage examples for hugeicons, fontawesome, and lucide

## Integration with docyrus-app-dev

This skill works alongside `docyrus-app-dev` for full-stack app development:

- **docyrus-app-dev** handles data fetching, collections, queries, auth
- **docyrus-app-ui-design** handles component selection, UI design, layout

When building a feature:
1. Use `docyrus-app-dev` to set up data queries and mutations
2. Use `docyrus-app-ui-design` to select and implement UI components
3. Combine them for complete, polished features
