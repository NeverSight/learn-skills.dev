---
name: bulk-select-actions
description: Build world-class table bulk selection with floating action toolbar. Linear/Notion-quality UX with proper checkbox states, smooth animations, and confirmation dialogs
---

## When to Use This Skill

Use when:
- Building a table/list with multi-select functionality
- Implementing bulk actions (delete, archive, export, status change)
- Need a floating action toolbar that appears on selection
- Want consistent selection UX across multiple tables

## Tech Stack

| Package | Version | Purpose |
|---------|---------|---------|
| `@radix-ui/react-checkbox` | ^1.x | Checkbox with indeterminate state |
| `tailwindcss-animate` | ^1.x | Entrance animations |
| `shadcn/ui` | latest | AlertDialog, Button, DropdownMenu |
| `lucide-react` | ^0.x | Icons |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Page Component (selection state owner)                     │
│  ├── selectedIds: Set<string>                               │
│  ├── onSelectionChange: (ids: Set<string>) => void          │
│  └── bulk action handlers                                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Table Component                                      │    │
│  │ ┌─────┬─────────────────────────────────────────┐   │    │
│  │ │ ☑️  │ Header row with select-all checkbox      │   │    │
│  │ ├─────┼─────────────────────────────────────────┤   │    │
│  │ │ ☐  │ Row 1                                    │   │    │
│  │ │ ☑️  │ Row 2 (selected)                         │   │    │
│  │ │ ☑️  │ Row 3 (selected)                         │   │    │
│  │ │ ☐  │ Row 4                                    │   │    │
│  │ └─────┴─────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Floating Toolbar (fixed bottom center, z-50)        │    │
│  │ ┌──────────────┬────────────┬────────────┬───────┐  │    │
│  │ │ 2 selected ✕ │  Action 1  │  Action 2  │ Delete│  │    │
│  │ └──────────────┴────────────┴────────────┴───────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Critical Patterns

### 1. Selection State Management (Page Level)

Selection state MUST live in the page component, not the table:

```typescript
// page.tsx
"use client";

import { useState } from "react";

export default function ItemsPage() {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  // Clear selection when filters change
  const handleFilterChange = (value: string) => {
    setFilter(value);
    setSelectedIds(new Set());
  };

  return (
    <>
      <ItemsTable
        items={items}
        selectedIds={selectedIds}
        onSelectionChange={setSelectedIds}
      />
      <BulkActionsToolbar
        selectedIds={selectedIds}
        onClearSelection={() => setSelectedIds(new Set())}
        // ... action handlers
      />
    </>
  );
}
```

### 2. Checkbox Indeterminate State (CRITICAL)

Use the built-in `checked` prop with `"indeterminate"` value:

```typescript
// ✅ CORRECT - Use built-in indeterminate prop
<Checkbox
  checked={allSelected ? true : someSelected ? "indeterminate" : false}
  onCheckedChange={handleSelectAll}
  aria-label="Select all"
/>

// ❌ WRONG - Manual ref approach (gets overwritten by Radix)
<Checkbox
  checked={allSelected}
  ref={(el) => {
    if (el) {
      (el as HTMLButtonElement).dataset.state = someSelected
        ? "indeterminate"
        : "checked";
    }
  }}
/>
```

### 3. Selection Logic

```typescript
// Table component
const allSelected = items.length > 0 && items.every((item) => selectedIds.has(item.id));
const someSelected = items.some((item) => selectedIds.has(item.id)) && !allSelected;

const handleSelectAll = () => {
  if (allSelected) {
    onSelectionChange(new Set()); // Deselect all
  } else {
    onSelectionChange(new Set(items.map((item) => item.id))); // Select all
  }
};

const handleSelectOne = (id: string, checked: boolean) => {
  const newSet = new Set(selectedIds);
  if (checked) {
    newSet.add(id);
  } else {
    newSet.delete(id);
  }
  onSelectionChange(newSet);
};
```

### 4. Floating Toolbar Position & Animation

```typescript
// CRITICAL: These exact classes for consistent UX
<div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 animate-in fade-in slide-in-from-bottom-4 duration-200">
  <div className="flex items-center gap-2 bg-background border rounded-lg shadow-lg px-4 py-3">
    {/* Toolbar content */}
  </div>
</div>
```

### 5. Toolbar Structure

```typescript
export function BulkActionsToolbar({
  selectedIds,
  onClearSelection,
  onAction1,
  onAction2,
  onDelete,
  isLoading = false,
}: BulkActionsToolbarProps) {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const selectedCount = selectedIds.size;

  // Hide when nothing selected
  if (selectedCount === 0) {
    return null;
  }

  return (
    <>
      <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 animate-in fade-in slide-in-from-bottom-4 duration-200">
        <div className="flex items-center gap-2 bg-background border rounded-lg shadow-lg px-4 py-3">
          {/* Selected count with clear button */}
          <div className="flex items-center gap-2 pr-3 border-r">
            <span className="text-sm font-medium">
              {selectedCount} selected
            </span>
            <Button
              variant="ghost"
              size="sm"
              className="h-6 w-6 p-0"
              onClick={onClearSelection}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Action buttons */}
          <Button variant="outline" size="sm" onClick={onAction1} disabled={isLoading}>
            <Icon className="h-4 w-4 mr-2" />
            Action 1
          </Button>

          {/* Destructive action - always last, with confirmation */}
          <Button
            variant="outline"
            size="sm"
            onClick={() => setDeleteDialogOpen(true)}
            disabled={isLoading}
            className="text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Delete
          </Button>
        </div>
      </div>

      {/* Confirmation dialog for destructive actions */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Items</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete {selectedCount} item
              {selectedCount === 1 ? "" : "s"}? This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => { onDelete(); setDeleteDialogOpen(false); }}
              className="bg-red-600 hover:bg-red-700"
            >
              Delete {selectedCount} Item{selectedCount === 1 ? "" : "s"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
```

### 6. Row Checkbox - Prevent Row Click

```typescript
<TableRow
  className="cursor-pointer"
  onClick={() => onRowClick(item.id)}
>
  <TableCell onClick={(e) => e.stopPropagation()}>
    <Checkbox
      checked={selectedIds.has(item.id)}
      onCheckedChange={(checked) => handleSelectOne(item.id, !!checked)}
      aria-label={`Select ${item.name}`}
    />
  </TableCell>
  {/* ... other cells */}
</TableRow>
```

### 7. Conditional Actions Based on Item State

```typescript
// Check selected items' states for conditional actions
const selectedItems = items.filter((item) => selectedIds.has(item.id));
const allDraft = selectedItems.every((item) => item.status === "DRAFT");
const allPublished = selectedItems.every((item) => item.status === "PUBLISHED");

// Only show "Publish" if all selected are DRAFT
{allDraft && (
  <Button variant="outline" size="sm" onClick={onPublish}>
    <Globe className="h-4 w-4 mr-2" />
    Publish
  </Button>
)}

// Only show "Close" if all selected are PUBLISHED
{allPublished && (
  <Button variant="outline" size="sm" onClick={onClose}>
    <XCircle className="h-4 w-4 mr-2" />
    Close
  </Button>
)}
```

## Table Component Props Interface

```typescript
interface SelectableTableProps<T extends { id: string }> {
  items: T[];
  isLoading?: boolean;
  selectedIds: Set<string>;
  onSelectionChange: (ids: Set<string>) => void;
  onRowClick?: (id: string) => void;
}
```

## Toolbar Component Props Interface

```typescript
interface BulkActionsToolbarProps {
  selectedIds: Set<string>;
  onClearSelection: () => void;
  isLoading?: boolean;
  // Add specific action handlers as needed
}
```

## Styling Patterns

### Checkbox Column Width

```typescript
<TableHead className="w-12">
  <Checkbox ... />
</TableHead>
```

### Clear Selection Button

```typescript
<Button
  variant="ghost"
  size="sm"
  className="h-6 w-6 p-0"  // Compact square button
  onClick={onClearSelection}
>
  <X className="h-4 w-4" />
</Button>
```

### Destructive Action Button

```typescript
<Button
  variant="outline"
  size="sm"
  className="text-red-600 hover:text-red-700 hover:bg-red-50"
>
  <Trash2 className="h-4 w-4 mr-2" />
  Delete
</Button>
```

### Confirmation Dialog Action

```typescript
<AlertDialogAction className="bg-red-600 hover:bg-red-700">
  Delete {count} Item{count === 1 ? "" : "s"}
</AlertDialogAction>
```

### Selected Count Section (with separator)

```typescript
<div className="flex items-center gap-2 pr-3 border-r">
  <span className="text-sm font-medium">{count} selected</span>
  <ClearButton />
</div>
```

## Common Mistakes to Avoid

### ❌ Using useEffect to clear selection on filter change

```typescript
// WRONG - ESLint error, causes cascading renders
useEffect(() => {
  setSelectedIds(new Set());
}, [filter]);
```

### ✅ Clear selection in the filter handler

```typescript
// CORRECT - Clear inline when filter changes
const handleFilterChange = (value: string) => {
  setFilter(value);
  setSelectedIds(new Set());
};
```

### ❌ Selection state in table component

```typescript
// WRONG - State should be lifted to page
function Table() {
  const [selectedIds, setSelectedIds] = useState(new Set());
  // ...
}
```

### ✅ Selection state in page component

```typescript
// CORRECT - Page owns state, passes to children
function Page() {
  const [selectedIds, setSelectedIds] = useState(new Set());
  return (
    <>
      <Table selectedIds={selectedIds} onSelectionChange={setSelectedIds} />
      <Toolbar selectedIds={selectedIds} onClearSelection={() => setSelectedIds(new Set())} />
    </>
  );
}
```

### ❌ Missing stopPropagation on row checkbox

```typescript
// WRONG - Clicking checkbox also triggers row click
<TableRow onClick={onRowClick}>
  <TableCell>
    <Checkbox onCheckedChange={handleSelect} />
  </TableCell>
</TableRow>
```

### ✅ Stop propagation on checkbox cell

```typescript
// CORRECT - Checkbox click doesn't bubble to row
<TableRow onClick={onRowClick}>
  <TableCell onClick={(e) => e.stopPropagation()}>
    <Checkbox onCheckedChange={handleSelect} />
  </TableCell>
</TableRow>
```

### ❌ No confirmation for destructive bulk actions

```typescript
// WRONG - Dangerous actions need confirmation
<Button onClick={onBulkDelete}>Delete All</Button>
```

### ✅ Always confirm destructive actions

```typescript
// CORRECT - AlertDialog for confirmation
<Button onClick={() => setDeleteDialogOpen(true)}>Delete</Button>
<AlertDialog open={deleteDialogOpen}>
  {/* Confirmation content */}
</AlertDialog>
```

## File Structure

```
src/
├── app/
│   └── (dashboard)/
│       └── dashboard/
│           └── items/
│               └── page.tsx           # Selection state owner
├── components/
│   └── items/
│       ├── items-table.tsx            # Table with checkboxes
│       ├── items-bulk-actions-toolbar.tsx  # Floating toolbar
│       └── index.ts                   # Exports
└── hooks/
    └── use-items.ts                   # Include bulk mutation hooks
```

## Bulk Mutation Hooks Pattern

```typescript
// hooks/use-items.ts
export function useBulkDeleteItems(teamId?: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (ids: string[]) => {
      const response = await fetch(`/api/teams/${teamId}/items/bulk-delete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ids }),
      });
      if (!response.ok) throw new Error("Failed to delete items");
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["items", teamId] });
    },
  });
}
```

## Related Asset Files

| Asset | Description |
|-------|-------------|
| `assets/components/bulk-actions-toolbar.tsx` | Generic toolbar template |
| `assets/components/selectable-table.tsx` | Table with checkbox selection |
| `assets/hooks/use-bulk-selection.ts` | Reusable selection hook |

## Checklist

- [ ] Selection state lives in page component (not table)
- [ ] Checkbox uses `checked={allSelected ? true : someSelected ? "indeterminate" : false}`
- [ ] Floating toolbar has `fixed bottom-6 left-1/2 -translate-x-1/2 z-50`
- [ ] Toolbar has `animate-in fade-in slide-in-from-bottom-4 duration-200`
- [ ] Toolbar returns `null` when `selectedCount === 0`
- [ ] Row checkbox cell has `onClick={(e) => e.stopPropagation()}`
- [ ] Selected count section has `border-r` separator
- [ ] Destructive action has confirmation dialog
- [ ] Destructive button has `text-red-600 hover:text-red-700 hover:bg-red-50`
- [ ] Confirmation action has `bg-red-600 hover:bg-red-700`
- [ ] Selection clears when filters change (in handler, not useEffect)
- [ ] Bulk mutation hooks invalidate queries on success
