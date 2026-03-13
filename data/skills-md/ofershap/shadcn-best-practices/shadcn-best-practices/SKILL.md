---
name: shadcn-best-practices
description:
  shadcn/ui done right. Component customization, form patterns, theming, accessibility, and
  composition patterns.
metadata:
  tags: shadcn, react, ui, best-practices
---

## When to use

Use this skill when working with shadcn/ui. Agents often treat it as a conventional npm package,
suggest wrong imports, skip the form patterns, and ignore the copy-paste architecture. This skill
anchors correct component sourcing, form patterns with React Hook Form + Zod, theming via CSS
variables, and composition patterns.

## Critical Rules

### 1. Components live in your project, not a package

**Wrong:**

```tsx
import { Button } from "@shadcn/ui";
import { Button } from "shadcn-ui";
```

**Correct:**

```tsx
import { Button } from "@/components/ui/button";
```

**Why:** shadcn/ui is a collection of copy-paste components. You copy them into your project and own
the source. There is no @shadcn/ui package to import from.

### 2. Use cn() for conditional classes

**Wrong:**

```tsx
<div className={`flex ${variant === "primary" ? "bg-blue-500" : "bg-gray-500"} ${className}`}>
```

**Correct:**

```tsx
import { cn } from "@/lib/utils"
<div className={cn("flex", variant === "primary" && "bg-blue-500", className)}>
```

**Why:** cn() from @/lib/utils merges Tailwind classes correctly and resolves conflicts. Template
literals produce invalid combinations and unpredictable specificity.

### 3. Forms: React Hook Form + Zod + shadcn Form

**Wrong:**

```tsx
<form
  onSubmit={(e) => {
    e.preventDefault(); /* manual validation */
  }}
>
  <input onChange={(e) => setValue(e.target.value)} />
</form>
```

**Correct:**

```tsx
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Form, FormField, FormItem, FormControl, FormMessage } from "@/components/ui/form"

const schema = z.object({ username: z.string().min(2) })
const form = useForm({ resolver: zodResolver(schema), defaultValues: { username: "" } })

<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField control={form.control} name="username" render={({ field }) => (
      <FormItem>
        <FormControl><Input {...field} /></FormControl>
        <FormMessage />
      </FormItem>
    )} />
  </form>
</Form>
```

**Why:** shadcn Form is built for React Hook Form with Zod. Manual validation and uncontrolled
inputs bypass validation, a11y, and error display.

### 4. Build custom components with Radix primitives

**Wrong:**

```tsx
<div onClick={() => setOpen(!open)} role="button">
  ...
</div>
```

**Correct:**

```tsx
import * as Dialog from "@radix-ui/react-dialog";
<Dialog.Root>
  <Dialog.Trigger>...</Dialog.Trigger>...
</Dialog.Root>;
```

**Why:** Radix provides accessibility, keyboard handling, and focus management. Rebuilding from divs
duplicates bugs and a11y gaps.

### 5. Theming via CSS variables

**Wrong:**

```tsx
<Button className="bg-blue-500 text-white hover:bg-blue-600">
```

**Correct:**

```css
/* globals.css */
:root {
  --primary: 222.2 84% 4.9%;
  --primary-foreground: 210 40% 98%;
}
```

```tsx
<Button>
```

**Why:** shadcn components read from CSS variables. Hardcoding colors breaks theming and dark mode.

### 6. Accessibility

**Wrong:**

```tsx
<div onClick={handleClick}>Click me</div>
<button>Submit</button>
```

**Correct:**

```tsx
<button onClick={handleClick} aria-label="Open menu">Open</button>
<button type="submit">Submit</button>
```

**Why:** Buttons need proper roles, labels, and keyboard support. Use semantic elements and aria
attributes.

### 7. Use cva for component variants

**Wrong:**

```tsx
className={cn("base", size === "sm" && "text-sm", size === "lg" && "text-lg", variant === "outline" && "border", ...)}
```

**Correct:**

```tsx
import { cva } from "class-variance-authority"
const variants = cva("base", { variants: { size: { sm: "text-sm", lg: "text-lg" }, variant: { outline: "border" } } })
className={variants({ size, variant })}
```

**Why:** cva keeps variant logic declarative and type-safe. Conditional chains are hard to maintain
and error-prone.

### 8. Dialog/Sheet/Popover: controlled state and navigation

**Wrong:**

```tsx
<Dialog open={open} onOpenChange={() => {}}>
```

**Correct:**

```tsx
<Dialog open={open} onOpenChange={setOpen}>
```

**Why:** Always pass controlled state and handle close. Close on route change or escape via
onOpenChange so state stays in sync.

### 9. Data tables with TanStack Table

**Wrong:**

```tsx
<table>{data.map(row => <tr>...)}</table>
```

**Correct:**

```tsx
import { useReactTable, getCoreRowModel } from "@tanstack/react-table";
import { Table, TableHeader, TableBody, TableRow } from "@/components/ui/table";
const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() });
```

**Why:** shadcn Table is designed to work with @tanstack/react-table for sorting, filtering, and
virtualization.

### 10. Toast: use sonner integration

**Wrong:**

```tsx
import { toast } from "custom-toast-library";
toast("Done");
```

**Correct:**

```tsx
import { toast } from "sonner";
toast.success("Done");
```

**Why:** shadcn uses sonner for Toaster. Use the configured sonner instance to match app styling and
placement.

### 11. Never import from @shadcn/ui

**Wrong:**

```tsx
import { Component } from "@shadcn/ui";
```

**Correct:**

```tsx
import { Component } from "@/components/ui/component";
```

**Why:** Components live in your repo at @/components/ui/. Add new ones with the CLI.

### 12. Add components with the CLI

**Wrong:**

```bash
npm install @shadcn/button
```

**Correct:**

```bash
npx shadcn@latest add button
```

**Why:** The CLI copies component source and configures your project. Install adds nothing useful.

## Patterns

- Keep component source in @/components/ui/ and customize it directly
- Use FormField, FormItem, FormControl, FormMessage for every form field
- Define theme in globals.css with --\* CSS variables
- Use Radix primitives when extending beyond existing shadcn components
- Prefer cn() for any conditional or composed class names

## Anti-Patterns

- Importing from @shadcn/ui or any shadcn package
- Wrapping shadcn components instead of editing source
- Template literals for conditional Tailwind classes
- Uncontrolled forms or manual validation instead of React Hook Form + Zod
- Hardcoding hex/rgb colors in components
- Building dialogs or dropdowns from divs instead of Radix
- Custom toast implementations instead of sonner
- Adding components via npm install instead of shadcn CLI
