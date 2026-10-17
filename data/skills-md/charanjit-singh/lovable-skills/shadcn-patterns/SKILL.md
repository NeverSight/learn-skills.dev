---
name: shadcn-patterns
description: >-
  Use when adding UI with shadcn/ui: dialogs, sheets, data tables, forms,
  command palette, dropdowns, or layout components. Not for non-shadcn design
  systems or backend-only work.
---

# shadcn/ui patterns

Use existing shadcn components from `@/components/ui`. Do not reinvent primitives.

## Dialog vs Sheet

| Use | Component |
|-----|-----------|
| Desktop modal, short forms | `Dialog` |
| Mobile-first, filters, long forms | `Sheet` (side or bottom) |

Always include `DialogTitle` / `SheetTitle` for accessibility.

## Data tables

- Use `@tanstack/react-table` with shadcn `Table`, `DataTable` pattern.
- Column headers sortable when list is large.
- Row actions in `DropdownMenu`, not 5 inline buttons.
- Empty/error states via `error-states-and-empty-ui` skill.

## Forms

- `Form`, `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormMessage`.
- Pair with Zod + react-hook-form (`typed-api-hooks-forms` skill).

## Buttons and actions

- One **primary** action per section; destructive uses `variant="destructive"`.
- `Button` + `disabled={isPending}` during mutations.

## Command palette

- `Command`, `CommandInput`, `CommandList`, `CommandItem` for search/navigation.
- Keyboard: Cmd/Ctrl+K when spec asks for it.

## Toasts and notifications

- Use **Sonner** (`<Toaster />` once at the root) for transient feedback.
- One toast per action; don't stack 5 success toasts.
- Errors: short message + optional retry; never raw `error.message` from Supabase.

```ts
import { toast } from "sonner";

toast.success("Project created");
toast.error("Could not save changes", { description: "Please try again." });
```

## Navigation patterns

- Persistent left `Sidebar` for app shell; `Tabs` inside a route for sub-views.
- `Breadcrumb` once routes go ≥ 3 levels deep.
- Mobile: bottom nav or `Sheet` drawer — never desktop sidebar squeezed onto phones.

## Responsive

- Stack filters in `Sheet` on mobile; inline on `md+`.
- Touch targets ≥ 44px where possible.
- Test at 375px width.

## Theming

- Use CSS variables from shadcn (`bg-background`, `text-foreground`) — never hardcoded `#fff`.
- Dark mode: see `dark-mode-and-theming` skill.

## Avoid

- Raw HTML `<button>` styled ad hoc when shadcn exists.
- Nested dialogs without clear close path.
- Missing `aria` labels on icon-only buttons.
- Multiple toast libraries (Sonner + react-hot-toast + custom) in one app.
