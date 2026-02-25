---
name: shadcn-ui
description: Build production-ready React/Next.js UIs with shadcn/ui components. Full lifecycle - install, customize, compose, debug, optimize. Covers components, forms, tables, theming, animations, and hooks.
---

<essential_principles>

## How shadcn/ui Works

shadcn/ui is NOT a component library - it's a collection of re-usable components you copy into your project and own. This philosophy changes everything about how you work with it.

### 1. You Own the Code

Components are copied directly into your `components/ui/` directory. You can and should modify them. Don't wrap components - edit them directly. This is intentional.

```bash
# Install a component
npx shadcn@latest add button

# Components land in your project
# src/components/ui/button.tsx
```

### 2. Composition Over Monoliths

Build complex UIs by composing primitives. Every component follows consistent patterns:
- **Radix UI primitives** for accessibility
- **CVA (class-variance-authority)** for variants
- **cn() utility** for conditional classes
- **data-slot attributes** for styling hooks

```tsx
// Composition pattern - build from primitives
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    {/* Content */}
    <DialogFooter>
      <Button>Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### 3. The asChild Pattern

Use `asChild` prop to merge behavior onto a different element. Critical for navigation, forms, and custom triggers.

```tsx
// asChild merges Button behavior onto Link
<Button asChild>
  <Link href="/dashboard">Dashboard</Link>
</Button>

// asChild on DialogTrigger
<DialogTrigger asChild>
  <Button>Open Dialog</Button>
</DialogTrigger>
```

### 4. Variant-Driven Design

Use CVA for consistent variant APIs. Every button, badge, and alert follows this pattern:

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md...", // Base
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        destructive: "bg-destructive text-white",
        outline: "border bg-background",
        ghost: "hover:bg-accent",
      },
      size: {
        default: "h-9 px-4",
        sm: "h-8 px-3",
        lg: "h-10 px-6",
        icon: "size-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

### 5. CSS Variables for Theming

All colors use CSS variables. Theme by changing variables, not component code:

```css
/* Light mode */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
}

/* Dark mode */
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

### 6. React 19 Patterns

shadcn/ui uses modern React patterns - no forwardRef (React 19), data-slot attributes, and function components:

```tsx
// Modern pattern (no forwardRef in React 19)
function Button({ className, variant, size, asChild = false, ...props }) {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}
```

</essential_principles>

<intake>
**What would you like to do?**

1. Add a new shadcn component to the project
2. Build a form with validation
3. Build a data table with sorting/filtering
4. Customize an existing component
5. Create a compound component
6. Add animations/transitions
7. Set up or modify theming
8. Debug a component issue
9. Something else

**Then read the matching workflow from `workflows/` and follow it.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "add", "install", "component" | `workflows/add-component.md` |
| 2, "form", "validation", "input" | `workflows/build-form.md` |
| 3, "table", "data table", "sorting", "filtering" | `workflows/build-data-table.md` |
| 4, "customize", "modify", "change", "edit" | `workflows/customize-component.md` |
| 5, "compound", "create", "new component", "build component" | `workflows/build-compound-component.md` |
| 6, "animation", "motion", "transition", "animate" | `workflows/add-animations.md` |
| 7, "theme", "dark mode", "colors", "styling" | `workflows/setup-theming.md` |
| 8, "debug", "fix", "broken", "not working", "issue" | `workflows/debug-component.md` |
| 9, other | Clarify, then select workflow or references |

**After reading the workflow, follow it exactly.**
</routing>

<verification_loop>
## After Every Change

1. **TypeScript compiles?**
```bash
bunx tsc --noEmit
```

2. **Component renders?**
Check the dev server - no console errors

3. **Accessibility check:**
- Keyboard navigation works
- Focus states visible
- ARIA attributes present

4. **Visual check:**
- Matches design intent
- Works in light/dark mode
- Responsive on mobile

Report: "TypeScript: ✓ | Renders: ✓ | A11y: ✓ | Visual: ✓"
</verification_loop>

<reference_index>
## Domain Knowledge

All in `references/`:

**Core:**
- core-components.md - Button, Input, Label, Card, Badge, etc.
- composition-patterns.md - asChild, Slot, compound components

**Forms:**
- form-components.md - Form, Field, Input, Select, Combobox, etc.
- form-validation.md - Zod, React Hook Form, TanStack Form

**Data Display:**
- data-table.md - TanStack Table integration
- data-components.md - Kanban, Gantt, List, Calendar

**Navigation:**
- navigation-components.md - Sidebar, Tabs, Breadcrumb, Command

**Overlays:**
- overlay-components.md - Dialog, Sheet, Drawer, Popover, Tooltip

**Feedback:**
- feedback-components.md - Toast/Sonner, Alert, Progress, Skeleton

**Hooks:**
- hooks.md - useLocalStorage, useMediaQuery, useDebounce, etc.

**Animation:**
- animation-patterns.md - Framer Motion, micro-interactions

**Theming:**
- theming.md - CSS variables, dark mode, color system

**Advanced:**
- cli-registry.md - CLI commands, custom registries
- accessibility.md - WCAG compliance, keyboard navigation
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| add-component.md | Install and configure a shadcn component |
| build-form.md | Build forms with validation |
| build-data-table.md | Build tables with TanStack Table |
| customize-component.md | Modify existing components |
| build-compound-component.md | Create new compound components |
| add-animations.md | Add Framer Motion animations |
| setup-theming.md | Configure theming and dark mode |
| debug-component.md | Troubleshoot component issues |
</workflows_index>
