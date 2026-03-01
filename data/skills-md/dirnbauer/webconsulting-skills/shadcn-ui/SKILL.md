---
name: shadcn-ui
description: >-
  Expert guide for building accessible, customizable UI components with shadcn/ui,
  Radix UI, and Tailwind CSS. Covers installation, core components (Button, Input, Form,
  Card, Dialog, Select, Sheet, Table, Toast, Charts), forms with React Hook Form + Zod
  validation, theming with CSS variables, Next.js integration, and advanced patterns.
metadata:
  version: "1.0.0"
  source: "https://github.com/giuseppe-trisciuoglio/developer-kit"
  related_skills:
    - react-best-practices
    - frontend-design
    - web-design-guidelines
---

# shadcn/ui Component Patterns

## Overview

Expert guide for building accessible, customizable UI components with shadcn/ui, Radix UI, and Tailwind CSS. This skill provides comprehensive patterns for implementing production-ready components with full accessibility support.

## Table of Contents

- When to Use
- Quick Start
- Installation & Setup
- Project Configuration
- Core Components
  - Button
  - Input & Form Fields
  - Forms with Validation
  - Card
  - Dialog (Modal)
  - Select (Dropdown)
  - Sheet (Slide-over)
  - Menubar & Navigation
  - Table
  - Toast Notifications
  - Charts
- Advanced Patterns
- Customization
- Next.js Integration
- Best Practices
- Common Component Combinations

## When to Use

- Setting up a new project with shadcn/ui
- Installing or configuring individual components
- Building forms with React Hook Form and Zod validation
- Creating accessible UI components (buttons, dialogs, dropdowns, sheets)
- Customizing component styling with Tailwind CSS
- Implementing design systems with shadcn/ui
- Building Next.js applications with TypeScript
- Creating complex layouts and data displays

## Instructions

1. **Initialize Project**: Run `npx shadcn@latest init` to configure shadcn/ui
2. **Install Components**: Add components with `npx shadcn@latest add <component>`
3. **Configure Theme**: Customize CSS variables in globals.css for theming
4. **Import Components**: Use components from `@/components/ui/` directory
5. **Customize as Needed**: Modify component code directly in your project
6. **Add Form Validation**: Integrate React Hook Form with Zod schemas
7. **Test Accessibility**: Verify ARIA attributes and keyboard navigation

## Quick Start

For new projects, use the automated setup:

```bash
# Create Next.js project with shadcn/ui
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app
npx shadcn@latest init

# Install essential components
npx shadcn@latest add button input form card dialog select
```

For existing projects:

```bash
# Install dependencies
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge lucide-react

# Initialize shadcn/ui
npx shadcn@latest init
```

## What is shadcn/ui?

shadcn/ui is **not** a traditional component library or npm package. Instead:

- It's a **collection of reusable components** that you can copy into your project
- Components are **yours to customize** - you own the code
- Built with **Radix UI** primitives for accessibility
- Styled with **Tailwind CSS** utilities
- Includes CLI tool for easy component installation

## Installation & Setup

### Initial Setup

```bash
# Initialize shadcn/ui in your project
npx shadcn@latest init
```

During setup, you'll configure:

- TypeScript or JavaScript
- Style (Default, New York, etc.)
- Base color theme
- CSS variables or Tailwind CSS classes
- Component installation path

### Installing Individual Components

```bash
# Install a single component
npx shadcn@latest add button

# Install multiple components
npx shadcn@latest add button input form

# Install all components
npx shadcn@latest add --all
```

## Core Components

### Button Component

```bash
npx shadcn@latest add button
```

```tsx
import { Button } from "@/components/ui/button";

// Variants
<Button variant="default">Default</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Sizes
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon className="h-4 w-4" /></Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Please wait
</Button>
```

### Input & Form Fields

```bash
npx shadcn@latest add input label
```

```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

<div className="grid w-full max-w-sm items-center gap-1.5">
  <Label htmlFor="email">Email</Label>
  <Input type="email" id="email" placeholder="Email" />
</div>
```

### Forms with Validation

```bash
npx shadcn@latest add form
```

This installs React Hook Form, Zod, and form components.

```tsx
"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import {
  Form, FormControl, FormDescription, FormField,
  FormItem, FormLabel, FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  username: z.string().min(2, {
    message: "Username must be at least 2 characters.",
  }),
  email: z.string().email({
    message: "Please enter a valid email address.",
  }),
})

export function ProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { username: "", email: "" },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>Your public display name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### Card Component

```bash
npx shadcn@latest add card
```

```tsx
import {
  Card, CardContent, CardDescription,
  CardFooter, CardHeader, CardTitle,
} from "@/components/ui/card"

<Card className="w-[350px]">
  <CardHeader>
    <CardTitle>Create project</CardTitle>
    <CardDescription>Deploy your new project in one-click.</CardDescription>
  </CardHeader>
  <CardContent>
    <form>
      <div className="grid w-full items-center gap-4">
        <div className="flex flex-col space-y-1.5">
          <Label htmlFor="name">Name</Label>
          <Input id="name" placeholder="Name of your project" />
        </div>
      </div>
    </form>
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button>Deploy</Button>
  </CardFooter>
</Card>
```

### Dialog (Modal)

```bash
npx shadcn@latest add dialog
```

```tsx
import {
  Dialog, DialogContent, DialogDescription,
  DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open Dialog</Button>
  </DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit profile</DialogTitle>
      <DialogDescription>
        Make changes to your profile here.
      </DialogDescription>
    </DialogHeader>
    <div className="grid gap-4 py-4">
      <Input id="name" value="Pedro Duarte" />
    </div>
    <DialogFooter>
      <Button type="submit">Save changes</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Select (Dropdown)

```bash
npx shadcn@latest add select
```

```tsx
import {
  Select, SelectContent, SelectItem,
  SelectTrigger, SelectValue,
} from "@/components/ui/select"

<Select>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Select a fruit" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="apple">Apple</SelectItem>
    <SelectItem value="banana">Banana</SelectItem>
    <SelectItem value="orange">Orange</SelectItem>
  </SelectContent>
</Select>
```

### Sheet (Slide-over)

```bash
npx shadcn@latest add sheet
```

```tsx
import {
  Sheet, SheetContent, SheetDescription,
  SheetHeader, SheetTitle, SheetTrigger,
} from "@/components/ui/sheet"

<Sheet>
  <SheetTrigger asChild>
    <Button variant="outline">Open Sheet</Button>
  </SheetTrigger>
  <SheetContent side="right">
    <SheetHeader>
      <SheetTitle>Settings</SheetTitle>
      <SheetDescription>Configure your application.</SheetDescription>
    </SheetHeader>
    {/* Settings content */}
  </SheetContent>
</Sheet>
```

### Table

```bash
npx shadcn@latest add table
```

```tsx
import {
  Table, TableBody, TableCaption, TableCell,
  TableHead, TableHeader, TableRow,
} from "@/components/ui/table"

<Table>
  <TableCaption>A list of recent invoices.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell className="font-medium">INV001</TableCell>
      <TableCell>Paid</TableCell>
      <TableCell className="text-right">$250.00</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Toast Notifications

```bash
npx shadcn@latest add toast
```

Setup in root layout:

```tsx
import { Toaster } from "@/components/ui/toaster"

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  )
}
```

Usage:

```tsx
import { useToast } from "@/components/ui/use-toast"

const { toast } = useToast()

// Success
toast({ title: "Success", description: "Changes saved." })

// Error
toast({ variant: "destructive", title: "Error", description: "Something went wrong." })

// With action
toast({
  title: "Uh oh!",
  description: "Something went wrong.",
  action: <ToastAction altText="Try again">Try again</ToastAction>,
})
```

### Charts

```bash
npx shadcn@latest add chart
```

Built on **Recharts** with consistent theming:

```tsx
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { ChartContainer, ChartTooltipContent } from "@/components/ui/chart"

const chartConfig = {
  desktop: { label: "Desktop", color: "var(--chart-1)" },
  mobile: { label: "Mobile", color: "var(--chart-2)" },
} satisfies import("@/components/ui/chart").ChartConfig

<ChartContainer config={chartConfig} className="min-h-[200px] w-full">
  <BarChart data={chartData}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" tickLine={false} axisLine={false} />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} />
    <ChartTooltip content={<ChartTooltipContent />} />
  </BarChart>
</ChartContainer>
```

## Theming with CSS Variables

Configure in `globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    /* ... other dark mode variables */
  }
}
```

## Customizing Components

Since you own the code, customize directly with `cva`:

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        // Add custom variant
        custom: "bg-gradient-to-r from-purple-500 to-pink-500 text-white",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        // Add custom size
        xl: "h-14 rounded-md px-10 text-lg",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)
```

## Next.js Integration

### App Router

Ensure interactive components use `"use client"` directive. Add Toaster to root layout.

### Server Components

Wrap interactive shadcn/ui components in Client Components when used in Server Components.

### Server Actions with Forms

```tsx
"use client"

async function onSubmit(values: z.infer<typeof formSchema>) {
  const response = await fetch("/api/contact", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(values),
  })
  if (!response.ok) throw new Error("Failed to submit")
  toast({ title: "Success!", description: "Message sent." })
}
```

## Constraints and Warnings

- **Not an NPM Package**: Components are copied to your project; you own the code
- **Client Components**: Most components require `"use client"` directive
- **Radix Dependencies**: Ensure all `@radix-ui` packages are installed
- **Tailwind Required**: Components rely on Tailwind CSS utilities
- **TypeScript**: Designed for TypeScript projects; type definitions included
- **Path Aliases**: Configure `@` alias in tsconfig.json for imports
- **Dark Mode**: Set up dark mode with CSS variables or class strategy

## Best Practices

1. **Accessibility**: Components use Radix UI primitives for ARIA compliance
2. **Customization**: Modify components directly in your codebase
3. **Type Safety**: Use TypeScript for type-safe props and state
4. **Validation**: Use Zod schemas for form validation
5. **Styling**: Leverage Tailwind utilities and CSS variables
6. **Consistency**: Use the same component patterns across your app
7. **Testing**: Components are testable with React Testing Library
8. **Performance**: Components are optimized and tree-shakeable

## References

- Official Docs: https://ui.shadcn.com
- Radix UI: https://www.radix-ui.com
- React Hook Form: https://react-hook-form.com
- Zod: https://zod.dev
- Tailwind CSS: https://tailwindcss.com
- Examples: https://ui.shadcn.com/examples
