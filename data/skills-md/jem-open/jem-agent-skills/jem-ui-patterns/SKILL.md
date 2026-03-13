---
name: jem-ui-patterns
description: Guide for composing @jem-open/jem-ui components into app-level UI patterns — forms, data views, modals, navigation, and feedback.
---

# jem-ui-patterns

Guide for AI agents composing `@jem-open/jem-ui` components into app-level UI patterns. Covers how to combine components for forms, data views, modals, drawers, navigation, and feedback — with correct wiring, accessibility, and state management.

## Step 1 — Check prerequisites

Verify the consuming project is set up to use jem-ui.

**Check 1: Package installed**

Look for `@jem-open/jem-ui` in `package.json` dependencies or devDependencies.

If not found, install it:

```bash
npm install @jem-open/jem-ui
```

Peer dependencies required: `react@^18 | ^19`, `react-dom@^18 | ^19`, `tailwindcss@^3.4`.

**Check 2: Styles imported**

The app entry point (e.g. `layout.tsx`, `_app.tsx`, or `main.tsx`) must import jem-ui styles:

```typescript
import "@jem-open/jem-ui/styles.css"
```

If missing, add it.

**Check 3: Tailwind preset configured**

`tailwind.config.js` (or `.ts`) must include the jem-ui preset and content path:

```javascript
const jemPreset = require("@jem-open/jem-ui/tailwind-preset");

module.exports = {
  presets: [jemPreset],
  content: [
    "./src/**/*.{ts,tsx}",
    "./node_modules/@jem-open/jem-ui/dist/**/*.{js,mjs}",
  ],
};
```

If missing, add both the preset and the content path.

**Halt** if any check fails and cannot be auto-fixed.

---

## Step 2 — Identify the UI pattern needed

Use the table below to match the user's goal to a pattern, then follow the corresponding subsection in Step 3.

| Pattern | When to use | Key components |
|---|---|---|
| Form layout | Collecting user input with validation | InputField, Select, Checkbox, RadioGroup, Button, Label |
| Data view | Displaying searchable/filterable tabular data | DataTable, DataTableColumnHeader, SearchInput, Tag, Pagination, EmptyState |
| Modal workflow | Confirming actions, editing records, multi-step flows | Dialog, DialogContent, DialogHeader, DialogFooter, Button, form components |
| Drawer panel | Side panels for detail views, editing, or creation | Drawer, DrawerContent, DrawerHeader, DrawerBody, DrawerFooter, Button |
| Navigation structure | Page sections, hierarchical nav, collapsible content | Tabs, TabsList, TabsTrigger, TabsContent, Breadcrumb, Accordion |
| Feedback & notifications | Alerts, toasts, empty states, tooltips | Alert, Toaster, EmptyState, Tooltip, TooltipProvider |

---

## Step 3 — Apply the pattern

### Form layout

**Composition:**

- Wrap inputs in a `<form>` element
- Use `InputField` (not raw `Input`) for automatic label association
- Use `SelectField` (not raw `Select`) for labeled selects
- Stack fields vertically with `gap-md` (24px)
- Place actions (submit/cancel buttons) at the bottom with `gap-xs` between them
- Wire `error` prop on fields to validation state

**Accessibility:** Each input must have a label. InputField/SelectField/CheckboxWithLabel handle this automatically. For custom layouts, use `Label` with `htmlFor`.

```tsx
import { InputField, SelectField, Select, SelectTrigger, SelectContent, SelectItem, SelectValue, CheckboxWithLabel, Button } from "@jem-open/jem-ui"

function UserForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const [errors, setErrors] = useState<Record<string, string>>({})

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-md">
      <InputField
        label="Full name"
        name="name"
        placeholder="Enter your name"
        error={!!errors.name}
        helperText={errors.name}
      />
      <InputField
        label="Email"
        name="email"
        type="email"
        placeholder="name@example.com"
        error={!!errors.email}
        helperText={errors.email}
      />
      <SelectField label="Role" description="Determines permissions">
        <Select name="role">
          <SelectTrigger>
            <SelectValue placeholder="Select a role" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="admin">Admin</SelectItem>
            <SelectItem value="editor">Editor</SelectItem>
            <SelectItem value="viewer">Viewer</SelectItem>
          </SelectContent>
        </Select>
      </SelectField>
      <CheckboxWithLabel
        label="Send welcome email"
        description="User will receive an onboarding email"
      />
      <div className="flex gap-xs justify-end">
        <Button variant="outline" type="button">Cancel</Button>
        <Button variant="primary" type="submit">Create user</Button>
      </div>
    </form>
  )
}
```

### Data view

**Composition:**

- Use `DataTable` with typed `ColumnDef` array
- Use `DataTableColumnHeader` in sortable column headers
- Use `Tag` for status columns
- Use `SearchInput` for filtering (connect to DataTable's `filterColumn`)
- DataTable has built-in pagination — use `showPagination={true}` (default)
- Use `EmptyState` when data array is empty (check before rendering DataTable)

**Accessibility:** DataTable renders semantic `<table>` elements with proper headers. Column headers announce sort state.

```tsx
import { DataTable, DataTableColumnHeader, Tag, EmptyState } from "@jem-open/jem-ui"
import { ColumnDef } from "@tanstack/react-table"

type Order = {
  id: string
  customer: string
  status: "completed" | "pending" | "failed"
  total: number
}

const columns: ColumnDef<Order>[] = [
  {
    accessorKey: "id",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Order ID" />,
  },
  {
    accessorKey: "customer",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Customer" />,
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as string
      const variant = status === "completed" ? "success" : status === "pending" ? "pending" : "failed"
      return <Tag variant={variant}>{status}</Tag>
    },
  },
  {
    accessorKey: "total",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Total" />,
    cell: ({ row }) => `$${(row.getValue("total") as number).toFixed(2)}`,
  },
]

function OrdersPage({ orders }: { orders: Order[] }) {
  if (orders.length === 0) {
    return (
      <EmptyState
        icon="inbox"
        title="No orders yet"
        description="Orders will appear here once customers place them"
        variant="card"
      />
    )
  }

  return (
    <DataTable
      columns={columns}
      data={orders}
      filterColumn="customer"
      filterPlaceholder="Search customers..."
    />
  )
}
```

### Modal workflow

**Composition:**

- Use `Dialog` as the root
- `DialogTrigger` wraps the button that opens the modal (use `asChild`)
- `DialogContent` contains the modal body
- `DialogHeader` with `DialogTitle` (required for accessibility) and `DialogDescription`
- `DialogFooter` for action buttons
- `DialogClose` wraps the cancel button (use `asChild`)
- For destructive actions, use `DialogTitle variant="error"`

**Accessibility:** Dialog traps focus, `DialogTitle` is announced by screen readers, Escape key closes the dialog.

```tsx
import {
  Dialog, DialogTrigger, DialogContent, DialogHeader,
  DialogTitle, DialogDescription, DialogFooter, DialogClose
} from "@jem-open/jem-ui"
import { Button, InputField } from "@jem-open/jem-ui"

function EditProfileDialog() {
  const [name, setName] = useState("")

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Edit profile</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit profile</DialogTitle>
          <DialogDescription>Update your display name and preferences.</DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-md py-md">
          <InputField
            label="Display name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button variant="primary" onClick={handleSave}>Save changes</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Drawer panel

**Composition:**

- Use `Drawer` with `direction` prop (default: "right")
- `DrawerTrigger` opens the drawer (use `asChild`)
- `DrawerContent` is the panel container
- `DrawerHeader` has pink background, title, and close button
- `DrawerBody` is scrollable content area (padding included)
- `DrawerFooter` sticks to the bottom with a top border
- Use `DrawerSection` to group content blocks within DrawerBody

**Accessibility:** Drawer traps focus when open, close button in header, Escape key closes.

```tsx
import {
  Drawer, DrawerTrigger, DrawerContent, DrawerHeader,
  DrawerBody, DrawerFooter, DrawerTitle, DrawerClose
} from "@jem-open/jem-ui"
import { Button, Avatar, AvatarFallback, Tag, Divider } from "@jem-open/jem-ui"

function UserDetailDrawer({ user }: { user: User }) {
  return (
    <Drawer direction="right">
      <DrawerTrigger asChild>
        <Button variant="ghost">View details</Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>{user.name}</DrawerTitle>
        </DrawerHeader>
        <DrawerBody>
          <div className="flex items-center gap-md mb-md">
            <Avatar size="lg">
              <AvatarFallback size="lg">{user.initials}</AvatarFallback>
            </Avatar>
            <div>
              <p className="text-greyscale-text-title font-semibold">{user.name}</p>
              <p className="text-greyscale-text-caption">{user.email}</p>
            </div>
          </div>
          <Divider spacing="md" />
          <div className="flex flex-col gap-sm">
            <div className="flex justify-between">
              <span className="text-greyscale-text-subtitle">Status</span>
              <Tag variant="success">{user.status}</Tag>
            </div>
            <div className="flex justify-between">
              <span className="text-greyscale-text-subtitle">Role</span>
              <span className="text-greyscale-text-body">{user.role}</span>
            </div>
          </div>
        </DrawerBody>
        <DrawerFooter>
          <Button variant="primary">Edit user</Button>
          <DrawerClose asChild>
            <Button variant="outline">Close</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  )
}
```

### Navigation structure

**Composition:**

- Use `Tabs` for page sections (default variant for card-style, line variant for minimal)
- Use `Breadcrumb` for hierarchical page navigation
- Use `Accordion` for collapsible sections within a page
- Combine: Breadcrumb at top for location context, Tabs for section switching

**Accessibility:** Tabs use arrow keys for navigation, Accordion uses Enter/Space to toggle.

```tsx
import {
  Tabs, TabsList, TabsTrigger, TabsContent,
  Breadcrumb, BreadcrumbList, BreadcrumbItem, BreadcrumbLink,
  BreadcrumbPage, BreadcrumbSeparator
} from "@jem-open/jem-ui"

function SettingsPage() {
  return (
    <div className="flex flex-col gap-md">
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="/">Home</BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Settings</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>

      <Tabs defaultValue="general">
        <TabsList variant="line">
          <TabsTrigger variant="line" value="general">General</TabsTrigger>
          <TabsTrigger variant="line" value="security">Security</TabsTrigger>
          <TabsTrigger variant="line" value="notifications">Notifications</TabsTrigger>
        </TabsList>
        <TabsContent value="general">
          {/* General settings form */}
        </TabsContent>
        <TabsContent value="security">
          {/* Security settings form */}
        </TabsContent>
        <TabsContent value="notifications">
          {/* Notification preferences */}
        </TabsContent>
      </Tabs>
    </div>
  )
}
```

### Feedback & notifications

**Composition:**

- `Alert` for inline, persistent messages (validation summaries, warnings)
- `Toaster` + `toast()` for transient notifications (success confirmations, errors)
- `EmptyState` for no-data states (empty lists, no search results)
- `Tooltip` for supplementary info on icons/buttons

**Key rules:**

- Add `<Toaster />` once in root layout
- Wrap app in `<TooltipProvider>` once
- Match Alert variant to severity: `success`, `warning`, `destructive`, `note`
- Use `toast.success()`, `toast.error()`, `toast.info()`, `toast.warning()`

```tsx
import { Alert, AlertTitle, AlertDescription, EmptyState, Tooltip, TooltipTrigger, TooltipContent } from "@jem-open/jem-ui"
import { Button, IconButton } from "@jem-open/jem-ui"
import { toast } from "sonner"
import { Info } from "lucide-react"

// Inline alert for form validation
<Alert variant="destructive">
  <AlertTitle>Validation failed</AlertTitle>
  <AlertDescription>Please fix the errors below before submitting.</AlertDescription>
</Alert>

// Toast for async operation result
async function handleSave() {
  try {
    await saveData()
    toast.success("Changes saved successfully")
  } catch {
    toast.error("Failed to save changes")
  }
}

// Empty state when no data
<EmptyState
  icon="inbox"
  title="No messages"
  description="You're all caught up"
  primaryAction={{ label: "Compose", onClick: openCompose }}
/>

// Tooltip for icon button
<Tooltip>
  <TooltipTrigger asChild>
    <IconButton icon={<Info />} aria-label="More information" />
  </TooltipTrigger>
  <TooltipContent>Click to learn more about this feature</TooltipContent>
</Tooltip>
```

---

## Step 4 — Handle state and interactivity

### Form layout

- Use controlled components: `value` + `onChange` on each field
- Track errors in state: `const [errors, setErrors] = useState<Record<string, string>>({})`
- Show errors after submit attempt or on blur: wire `error={!!errors.fieldName}` and `helperText={errors.fieldName}`
- Use `loading` prop on submit Button during async operations
- Reset form state after successful submission

### Data view

- DataTable manages its own internal state (sorting, pagination, filtering)
- For server-side data, pass fresh `data` array — DataTable re-renders
- For empty state, check `data.length === 0` before rendering DataTable

### Modal workflow

- For controlled dialogs: use `open` and `onOpenChange` props on `Dialog`
- Close dialog after successful action: `setOpen(false)` in success callback
- Reset form state when dialog opens: use `onOpenChange` to clear state

### Drawer panel

- Same controlled pattern as Dialog: `open` + `onOpenChange` on `Drawer`
- DrawerBody scrolls automatically for overflow content

### Navigation

- Tabs: controlled with `value` + `onValueChange`, or uncontrolled with `defaultValue`
- Accordion: `type="single"` + `collapsible` for FAQ-style, `type="multiple"` for settings

### Feedback

- Toast is fire-and-forget: `toast.success("Message")` — no state management needed
- Alert is declarative: render based on state (e.g., `{showWarning && <Alert>...}`)

---

## Step 5 — Validate the composition

Run through this checklist before considering the UI complete:

- [ ] Every interactive component has an accessible label (InputField label, Button text, IconButton aria-label)
- [ ] Spacing between elements uses design tokens (`gap-md`, `p-sm`), not arbitrary values (`gap-6`, `p-4`)
- [ ] Loading states are handled (Button `loading` prop during async, Skeleton while data loads)
- [ ] Empty states are handled (EmptyState when no data, not a blank page)
- [ ] Error states are handled (InputField `error` + `helperText`, Alert for form-level errors, toast.error for async failures)
- [ ] Class composition uses `cn()` from `@jem-open/jem-ui`, not template literals
- [ ] No unnecessary wrapper elements (use `asChild` on Button/DialogTrigger/DrawerTrigger instead)
- [ ] `TooltipProvider` is present in the layout (if using Tooltip)
- [ ] `Toaster` is added once in the root layout (if using toast)
