---
name: kanban-dnd
description: Build world-class kanban board drag-and-drop with @dnd-kit. Linear-quality UX with proper collision detection, smooth animations, and visual feedback
---

## When to Use This Skill

Use when:
- Building a kanban/pipeline board with drag-and-drop
- Implementing card movement between columns
- Need proper collision detection that prioritizes columns over cards
- Want Linear/Notion-style drag UX with cursor-following overlay

## Tech Stack

| Package | Version | Purpose |
|---------|---------|---------|
| `@dnd-kit/core` | ^6.x | Core DnD context and hooks |
| `@dnd-kit/modifiers` | ^9.x | Cursor snapping modifiers |
| `@dnd-kit/utilities` | ^3.x | CSS transform utilities |

## Installation

```bash
bun add @dnd-kit/core @dnd-kit/modifiers @dnd-kit/utilities
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  DndContext (sensors, collision detection, event handlers) │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Column  │  │ Column  │  │ Column  │  │ Column  │        │
│  │(droppa- │  │(droppa- │  │(droppa- │  │(droppa- │        │
│  │  ble)   │  │  ble)   │  │  ble)   │  │  ble)   │        │
│  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │  │         │        │
│  │ │Card │ │  │ │Card │ │  │ │Card │ │  │  Empty  │        │
│  │ │drag │ │  │ │drag │ │  │ │drag │ │  │         │        │
│  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │  │         │        │
│  │ ┌─────┐ │  │ ┌─────┐ │  │         │  │         │        │
│  │ │Card │ │  │ │Card │ │  │         │  │         │        │
│  │ └─────┘ │  │ └─────┘ │  │         │  │         │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
├─────────────────────────────────────────────────────────────┤
│  DragOverlay (follows cursor with snapCenterToCursor)       │
└─────────────────────────────────────────────────────────────┘
```

## Critical Patterns

### 1. Custom Collision Detection (MOST IMPORTANT)

**Problem:** Default collision detection can return card IDs when dropping on a card instead of the column ID.

**Solution:** Custom collision detection that prioritizes column droppables:

```typescript
// lib/dnd/collision-detection.ts
import {
  pointerWithin,
  rectIntersection,
  type CollisionDetection,
} from "@dnd-kit/core";

export const columnPriorityCollision: CollisionDetection = (args) => {
  // First, check pointer intersections
  const pointerCollisions = pointerWithin(args);
  
  // Filter to only column collisions (columns have data.type === 'column')
  const columnCollisions = pointerCollisions.filter(
    (collision) => collision.data?.droppableContainer?.data?.current?.type === "column"
  );

  if (columnCollisions.length > 0) {
    return columnCollisions;
  }

  // Fallback to rect intersection
  const rectCollisions = rectIntersection(args);
  const columnRectCollisions = rectCollisions.filter(
    (collision) => collision.data?.droppableContainer?.data?.current?.type === "column"
  );

  if (columnRectCollisions.length > 0) {
    return columnRectCollisions;
  }

  return rectCollisions;
};
```

### 2. Column Setup with Data Type

Columns must include `data.type` for collision detection filtering:

```typescript
const { setNodeRef } = useDroppable({
  id: column.id,
  data: {
    type: "column",  // CRITICAL: Enables collision filtering
    columnId: column.id,
  },
});
```

### 3. Card Setup with useDraggable (NOT useSortable)

For cross-column moves without within-column reordering, use `useDraggable`:

```typescript
const {
  attributes,
  listeners,
  setNodeRef,
  isDragging,
} = useDraggable({
  id: card.id,
  data: {
    type: "card",
    card,
  },
});

// Apply to entire card for drag-anywhere behavior
<Card
  ref={setNodeRef}
  {...attributes}
  {...listeners}
  className="cursor-grab active:cursor-grabbing touch-none select-none"
>
```

### 4. Resolving Drop Target to Column ID

Handle both column drops and card drops:

```typescript
const findTargetColumnId = useCallback(
  (overId: UniqueIdentifier | undefined): string | null => {
    if (!overId) return null;
    
    const overIdStr = String(overId);
    
    // Check if it's a column ID directly
    if (columnIds.has(overIdStr)) {
      return overIdStr;
    }
    
    // Otherwise it's a card ID - find which column that card is in
    const columnId = cardColumnMap.get(overIdStr);
    return columnId || null;
  },
  [columnIds, cardColumnMap]
);
```

### 5. DragOverlay with Cursor Snapping

**Problem:** Default DragOverlay appears offset from cursor.

**Solution:** Use `snapCenterToCursor` modifier and disable drop animation:

```typescript
import { snapCenterToCursor } from "@dnd-kit/modifiers";

<DragOverlay
  modifiers={[snapCenterToCursor]}
  dropAnimation={null}  // Prevents fly-out effect on drop
>
  {activeCard ? (
    <div className="w-[272px] pointer-events-none">
      <Card card={activeCard} isDragging />
    </div>
  ) : null}
</DragOverlay>
```

### 6. Sensor Configuration

```typescript
const sensors = useSensors(
  useSensor(PointerSensor, {
    activationConstraint: {
      distance: 5,  // 5px movement before drag activates
    },
  }),
  useSensor(KeyboardSensor, {
    coordinateGetter: sortableKeyboardCoordinates,
  })
);
```

### 7. Visual Feedback States

```typescript
// Board tracks active states
const [activeCard, setActiveCard] = useState<Card | null>(null);
const [activeOverColumn, setActiveOverColumn] = useState<string | null>(null);

// Pass to columns for visual feedback
<Column
  isOver={activeOverColumn === column.id}
  isDragging={!!activeCard}
/>
```

## Complete Event Handlers

```typescript
const handleDragStart = useCallback((event: DragStartEvent) => {
  const { active } = event;
  const card = cards?.find((c) => c.id === active.id);
  if (card) {
    setActiveCard(card);
    setActiveOverColumn(card.columnId);
  }
}, [cards]);

const handleDragOver = useCallback((event: DragOverEvent) => {
  const { over } = event;
  if (!over) {
    setActiveOverColumn(null);
    return;
  }
  const targetColumnId = findTargetColumnId(over.id);
  setActiveOverColumn(targetColumnId);
}, [findTargetColumnId]);

const handleDragEnd = useCallback((event: DragEndEvent) => {
  const { active, over } = event;
  
  setActiveCard(null);
  setActiveOverColumn(null);

  if (!over) return;

  const cardId = String(active.id);
  const targetColumnId = findTargetColumnId(over.id);

  if (!targetColumnId) return;

  const card = cards?.find((c) => c.id === cardId);
  if (!card || card.columnId === targetColumnId) return;

  // Optimistic update via mutation
  updateCard.mutate({
    cardId,
    data: { columnId: targetColumnId },
  });
}, [cards, findTargetColumnId, updateCard]);

const handleDragCancel = useCallback(() => {
  setActiveCard(null);
  setActiveOverColumn(null);
}, []);
```

## Styling Patterns

### Card States

```typescript
// Original card being dragged
isCurrentlyDragging && "opacity-30"

// DragOverlay card
isDragging && "shadow-xl ring-2 ring-primary/20 rotate-[1deg] cursor-grabbing"

// Entire card is draggable
"cursor-grab active:cursor-grabbing touch-none select-none"
```

### Column States

```typescript
// Column during any drag
isDragging && "bg-muted/30"

// Column being hovered
isOver && "bg-primary/5 ring-2 ring-primary/20 ring-inset"
```

### Empty Column State

```typescript
<div className={cn(
  "border-2 border-dashed rounded-lg",
  isOver ? "border-primary/40 bg-primary/5" : "border-border/50"
)}>
  <p>{isDragging ? "Drop here" : "Drag items here"}</p>
</div>
```

## Common Mistakes to Avoid

### ❌ Using useSortable for cross-column moves

```typescript
// WRONG - useSortable is for within-list reordering
import { useSortable } from "@dnd-kit/sortable";
const { ... } = useSortable({ id: card.id });
```

### ✅ Use useDraggable for cross-column moves

```typescript
// CORRECT - useDraggable for simple drag to droppable
import { useDraggable } from "@dnd-kit/core";
const { ... } = useDraggable({ id: card.id });
```

### ❌ Assuming over.id is always a column ID

```typescript
// WRONG - over.id could be a card ID if you drop on a card
const handleDragEnd = (event) => {
  const newColumnId = over.id as string;  // Might be a card ID!
};
```

### ✅ Resolve over.id to column ID

```typescript
// CORRECT - Handle both column and card drop targets
const targetColumnId = findTargetColumnId(over.id);
```

### ❌ Using drop animation with snapCenterToCursor

```typescript
// WRONG - Causes fly-out effect on drop
<DragOverlay
  modifiers={[snapCenterToCursor]}
  dropAnimation={{ duration: 200, easing: "ease-out" }}
>
```

### ✅ Disable drop animation

```typescript
// CORRECT - Instant disappear on drop
<DragOverlay
  modifiers={[snapCenterToCursor]}
  dropAnimation={null}
>
```

### ❌ Separate drag handle

```typescript
// WRONG - Creates offset issues, worse UX
<Card>
  <div {...listeners}>
    <GripIcon /> {/* Only this area is draggable */}
  </div>
  <Content />
</Card>
```

### ✅ Entire card draggable

```typescript
// CORRECT - Linear-style drag anywhere
<Card {...listeners} {...attributes} className="cursor-grab">
  <Content />
</Card>
```

## Optimistic Updates with React Query

```typescript
export function useUpdateCard(teamId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ cardId, data }) => updateCard(teamId, cardId, data),

    // Optimistic update
    onMutate: async ({ cardId, data }) => {
      await queryClient.cancelQueries({ queryKey: cardKeys.lists() });

      const previousCards = queryClient.getQueriesData<Card[]>({
        queryKey: cardKeys.lists(),
      });

      queryClient.setQueriesData<Card[]>(
        { queryKey: cardKeys.lists() },
        (old) => old?.map((card) =>
          card.id === cardId ? { ...card, ...data } : card
        )
      );

      return { previousCards };
    },

    // Rollback on error
    onError: (_err, _variables, context) => {
      context?.previousCards?.forEach(([queryKey, data]) => {
        queryClient.setQueryData(queryKey, data);
      });
    },

    // Refetch after settle
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: cardKeys.all });
    },
  });
}
```

## File Structure

```
src/
├── components/
│   └── kanban/
│       ├── kanban-board.tsx       # DndContext wrapper
│       ├── kanban-column.tsx      # Droppable column
│       ├── kanban-card.tsx        # Draggable card
│       └── kanban-skeleton.tsx    # Loading state
├── lib/
│   └── dnd/
│       └── collision-detection.ts # Custom collision detection
└── hooks/
    └── use-cards.ts               # React Query with optimistic updates
```

## Related Asset Files

| Asset | Description |
|-------|-------------|
| `assets/lib/collision-detection.ts` | Column-priority collision detection |
| `assets/components/kanban-board.tsx` | Complete board implementation |
| `assets/components/kanban-column.tsx` | Droppable column with visual feedback |
| `assets/components/kanban-card.tsx` | Draggable card component |

## Checklist

- [ ] Installed `@dnd-kit/core`, `@dnd-kit/modifiers`, `@dnd-kit/utilities`
- [ ] Custom collision detection prioritizes columns
- [ ] Columns use `useDroppable` with `data.type: "column"`
- [ ] Cards use `useDraggable` (NOT `useSortable`)
- [ ] `findTargetColumnId` resolves both column and card drop targets
- [ ] DragOverlay uses `snapCenterToCursor` modifier
- [ ] DragOverlay has `dropAnimation={null}`
- [ ] DragOverlay wrapper has fixed width matching card width
- [ ] Cards have `touch-none select-none cursor-grab` classes
- [ ] Visual feedback for `isOver` and `isDragging` states
- [ ] Optimistic updates with rollback on error
