---
name: frontend-shadcn
description: DEFAULT foundation component library for all React/Next.js UI needs. Use as the starting point for any project needing buttons, inputs, dialogs, forms, tables, navigation, modals, dropdowns, and other standard UI elements. Built on Radix UI + Tailwind CSS. Check shadcn FIRST before reaching for other libraries.
allowed-tools: Read, Edit, Write, Bash (*)
---

# shadcn/ui Component Library

## Overview

shadcn/ui is NOT a component library you install via npm. It's a collection of re-usable components that you copy and paste into your project. You OWN the code.

**Philosophy:** Copy-paste → Own the code → Customize freely

**Built on:** Radix UI (accessibility) + Tailwind CSS (styling) + CVA (variants)

## When to Use This Skill

- Starting ANY new React/Next.js project
- Need standard UI components (buttons, inputs, dialogs, etc.)
- Building forms, tables, navigation
- Need accessible, production-ready components
- User asks for "basic UI", "form", "modal", "dropdown", etc.

**This is your DEFAULT starting point. Always check shadcn/ui first.**

---

## Quick Start

### Project Setup

```bash
# Initialize shadcn/ui in your project
npx shadcn@latest init

# Answer prompts:
# - Style: Default or New York
# - Base color: Slate, Gray, Zinc, Neutral, Stone
# - CSS variables: Yes (recommended)
```

### Add Components

```bash
# Add single component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add button card dialog

# Add ALL components
npx shadcn@latest add --all
```

---

## Complete Component Reference

### Forms & Inputs

| Component | Command | Use Case |
|-----------|---------|----------|
| **Button** | `add button` | Primary actions, CTAs |
| **Input** | `add input` | Text fields |
| **Textarea** | `add textarea` | Multi-line text |
| **Select** | `add select` | Dropdown selection |
| **Native Select** | `add native-select` | Native HTML select |
| **Checkbox** | `add checkbox` | Boolean options |
| **Radio Group** | `add radio-group` | Single choice from options |
| **Switch** | `add switch` | Toggle on/off |
| **Slider** | `add slider` | Range selection |
| **Input OTP** | `add input-otp` | One-time password input |
| **Form** | `add form` | Form with react-hook-form + zod |
| **Label** | `add label` | Form field labels |
| **Field** | `add field` | Form field wrapper |

```tsx
// Button variants
<Button>Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>
```

```tsx
// Form example with validation
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(schema),
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Login</Button>
      </form>
    </Form>
  )
}
```

### Overlays & Modals

| Component | Command | Use Case |
|-----------|---------|----------|
| **Dialog** | `add dialog` | Modal windows, confirmations |
| **Alert Dialog** | `add alert-dialog` | Destructive action confirmations |
| **Sheet** | `add sheet` | Side panels (mobile nav, filters) |
| **Drawer** | `add drawer` | Bottom sheets (mobile) |
| **Popover** | `add popover` | Floating content, pickers |
| **Tooltip** | `add tooltip` | Hover hints |
| **Hover Card** | `add hover-card` | Rich hover previews |
| **Context Menu** | `add context-menu` | Right-click menus |
| **Dropdown Menu** | `add dropdown-menu` | Action menus |

```tsx
// Dialog example
<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogDescription>
        Make changes to your profile here.
      </DialogDescription>
    </DialogHeader>
    {/* content */}
    <DialogFooter>
      <Button type="submit">Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

```tsx
// Sheet (side panel)
<Sheet>
  <SheetTrigger asChild>
    <Button variant="outline">Open Menu</Button>
  </SheetTrigger>
  <SheetContent side="left"> {/* left | right | top | bottom */}
    <SheetHeader>
      <SheetTitle>Menu</SheetTitle>
    </SheetHeader>
    {/* navigation links */}
  </SheetContent>
</Sheet>
```

### Navigation

| Component | Command | Use Case |
|-----------|---------|----------|
| **Navigation Menu** | `add navigation-menu` | Main site navigation |
| **Menubar** | `add menubar` | App menubar (File, Edit, View) |
| **Breadcrumb** | `add breadcrumb` | Page hierarchy |
| **Pagination** | `add pagination` | Page navigation |
| **Tabs** | `add tabs` | Content sections |
| **Command** | `add command` | Command palette (⌘K) |
| **Sidebar** | `add sidebar` | App sidebar navigation |

```tsx
// Tabs example
<Tabs defaultValue="account">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>
  <TabsContent value="account">Account settings...</TabsContent>
  <TabsContent value="password">Password settings...</TabsContent>
</Tabs>
```

```tsx
// Command palette (cmdk)
<Command>
  <CommandInput placeholder="Type a command..." />
  <CommandList>
    <CommandEmpty>No results found.</CommandEmpty>
    <CommandGroup heading="Suggestions">
      <CommandItem>Calendar</CommandItem>
      <CommandItem>Search</CommandItem>
      <CommandItem>Settings</CommandItem>
    </CommandGroup>
  </CommandList>
</Command>
```

### Layout & Structure

| Component | Command | Use Case |
|-----------|---------|----------|
| **Card** | `add card` | Content containers |
| **Accordion** | `add accordion` | Collapsible sections |
| **Collapsible** | `add collapsible` | Toggle content visibility |
| **Separator** | `add separator` | Visual dividers |
| **Aspect Ratio** | `add aspect-ratio` | Fixed aspect containers |
| **Scroll Area** | `add scroll-area` | Custom scrollbars |
| **Resizable** | `add resizable` | Resizable panels |

```tsx
// Card example
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content here</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

```tsx
// Accordion
<Accordion type="single" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Is it accessible?</AccordionTrigger>
    <AccordionContent>
      Yes. It follows WAI-ARIA patterns.
    </AccordionContent>
  </AccordionItem>
</Accordion>
```

### Data Display

| Component | Command | Use Case |
|-----------|---------|----------|
| **Table** | `add table` | Basic tables |
| **Data Table** | `add data-table` | Advanced tables (sorting, filtering) |
| **Avatar** | `add avatar` | User images |
| **Badge** | `add badge` | Status labels, tags |
| **Calendar** | `add calendar` | Date picker calendar |
| **Date Picker** | `add date-picker` | Date selection |
| **Carousel** | `add carousel` | Image/content sliders |
| **Chart** | `add chart` | Data visualization (Recharts) |

```tsx
// Table
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Email</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>John Doe</TableCell>
      <TableCell>john@example.com</TableCell>
      <TableCell><Badge>Active</Badge></TableCell>
    </TableRow>
  </TableBody>
</Table>
```

```tsx
// Badge variants
<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

### Feedback

| Component | Command | Use Case |
|-----------|---------|----------|
| **Alert** | `add alert` | Inline messages |
| **Toast** | `add toast` | Brief notifications |
| **Sonner** | `add sonner` | Better toast notifications |
| **Progress** | `add progress` | Loading progress |
| **Skeleton** | `add skeleton` | Loading placeholders |
| **Spinner** | `add spinner` | Loading indicator |
| **Empty** | `add empty` | Empty state placeholder |

```tsx
// Alert
<Alert>
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    You can add components to your app.
  </AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Something went wrong.</AlertDescription>
</Alert>
```

```tsx
// Toast (using Sonner - recommended)
import { toast } from "sonner"

// Trigger toast
toast.success("Profile updated!")
toast.error("Something went wrong")
toast.loading("Saving...")
```

```tsx
// Skeleton loading
<div className="space-y-2">
  <Skeleton className="h-4 w-[250px]" />
  <Skeleton className="h-4 w-[200px]" />
</div>
```

### Utility

| Component | Command | Use Case |
|-----------|---------|----------|
| **Toggle** | `add toggle` | On/off button |
| **Toggle Group** | `add toggle-group` | Multiple toggles |
| **Combobox** | `add combobox` | Searchable select |
| **Typography** | `add typography` | Text styles |
| **Kbd** | `add kbd` | Keyboard shortcut hints |
| **Button Group** | `add button-group` | Grouped buttons |
| **Input Group** | `add input-group` | Input with addons |
| **Item** | `add item` | List item component |

```tsx
// Combobox (searchable select)
<Popover open={open} onOpenChange={setOpen}>
  <PopoverTrigger asChild>
    <Button variant="outline" role="combobox">
      {value || "Select framework..."}
    </Button>
  </PopoverTrigger>
  <PopoverContent>
    <Command>
      <CommandInput placeholder="Search..." />
      <CommandList>
        <CommandEmpty>No results.</CommandEmpty>
        <CommandGroup>
          {frameworks.map((framework) => (
            <CommandItem
              key={framework.value}
              onSelect={() => setValue(framework.value)}
            >
              {framework.label}
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </Command>
  </PopoverContent>
</Popover>
```

---

## Common Patterns

### Loading Button

```tsx
import { Loader2 } from "lucide-react"

<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  {isLoading ? "Loading..." : "Submit"}
</Button>
```

### Confirmation Dialog

```tsx
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={handleDelete}>
        Delete
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Search with Command

```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline" className="w-[200px] justify-start">
      <Search className="mr-2 h-4 w-4" />
      Search...
      <Kbd className="ml-auto">⌘K</Kbd>
    </Button>
  </DialogTrigger>
  <DialogContent className="p-0">
    <Command>
      <CommandInput placeholder="Search..." />
      <CommandList>
        <CommandEmpty>No results.</CommandEmpty>
        <CommandGroup heading="Pages">
          <CommandItem>Dashboard</CommandItem>
          <CommandItem>Settings</CommandItem>
        </CommandGroup>
      </CommandList>
    </Command>
  </DialogContent>
</Dialog>
```

### Responsive Mobile Menu

```tsx
// Desktop: Navigation Menu
// Mobile: Sheet with menu

<div className="hidden md:block">
  <NavigationMenu>{/* desktop nav */}</NavigationMenu>
</div>

<div className="md:hidden">
  <Sheet>
    <SheetTrigger asChild>
      <Button variant="ghost" size="icon">
        <Menu />
      </Button>
    </SheetTrigger>
    <SheetContent side="left">
      {/* mobile nav links */}
    </SheetContent>
  </Sheet>
</div>
```

---

## Theming

### CSS Variables (globals.css)

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 5.9% 10%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    /* ... dark mode values */
  }
}
```

### Using Theme Colors

```tsx
// In Tailwind classes
<div className="bg-background text-foreground" />
<div className="bg-primary text-primary-foreground" />
<div className="bg-muted text-muted-foreground" />
<div className="border-border" />
```

---

## Component Customization

### Extending Variants (CVA)

```tsx
// components/ui/button.tsx
import { cva } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input bg-background hover:bg-accent",
        secondary: "bg-secondary text-secondary-foreground",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        // Add custom variants
        success: "bg-green-600 text-white hover:bg-green-700",
        warning: "bg-yellow-500 text-black hover:bg-yellow-600",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
        // Add custom sizes
        xl: "h-14 rounded-lg px-10 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

---

## Decision Guide

```
Need a component?
       │
       ▼
┌──────────────────────────┐
│ Is it a STANDARD UI      │
│ element? (button, input, │
│ modal, table, form...)   │
└──────────────────────────┘
       │
  YES ─┴─ NO
   │       │
   ▼       ▼
shadcn   Check Aceternity
 /ui     or Magic UI
```

---

## Troubleshooting

```yaml
"Component not found":
  → npx shadcn@latest add [component] --overwrite
  → Check components.json exists

"Styles not applying":
  → Check tailwind.config.ts content paths
  → Check globals.css has CSS variables

"Hydration mismatch (Dialog/Sheet)":
  → Add suppressHydrationWarning to <html>
  → Use dynamic(() => import(...), { ssr: false })

"Dark mode not working":
  → npm install next-themes
  → Add darkMode: ['class'] to tailwind.config.ts
  → Wrap app with ThemeProvider

"Form errors not showing":
  → Include <FormMessage /> in FormField
  → Check zodResolver(schema) is set
```

---

## References

- **[patterns.md](references/patterns.md)** — Dark mode toggle, multi-step forms, data tables, file upload

## External Resources

- https://ui.shadcn.com/docs — Documentation
- https://ui.shadcn.com/docs/components — Components list
- https://ui.shadcn.com/themes — Theme generator
- https://ui.shadcn.com/blocks — Example blocks
