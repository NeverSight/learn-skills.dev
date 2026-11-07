---
name: ui-patterns
description: UI/UX patterns and guidelines derived from official Frappe apps (CRM, Helpdesk, HRMS). Use when designing interfaces for custom Frappe applications to ensure consistency with the ecosystem.
---

# Frappe UI Patterns

UI/UX patterns and design guidelines extracted from official Frappe applications.

## When to use

- Designing UI for a new Frappe app
- Building CRUD interfaces with Frappe UI
- Implementing list views, detail panels, or forms
- Ensuring consistent UX with CRM, Helpdesk, HRMS
- Choosing component patterns and layouts

## Inputs required

- App type (CRM-like, Helpdesk-like, data management)
- Key entities and their relationships
- Primary user workflows

## Reference apps

Study these official apps for patterns:

| App | Repo | Key Patterns |
|-----|------|--------------|
| Frappe CRM | [github.com/frappe/crm](https://github.com/frappe/crm) | Lead/Deal pipelines, Kanban, activity feeds |
| Frappe Helpdesk | [github.com/frappe/helpdesk](https://github.com/frappe/helpdesk) | Ticket queues, SLA indicators, agent views |
| Frappe HRMS | [github.com/frappe/hrms](https://github.com/frappe/hrms) | Employee self-service, approvals, dashboards |
| Frappe Insights | [github.com/frappe/insights](https://github.com/frappe/insights) | Query builders, visualizations, dashboards |
| Frappe Builder | [github.com/frappe/builder](https://github.com/frappe/builder) | Drag-drop interfaces, property panels |

## Procedure

### 0) App shell structure

All Frappe apps follow a consistent shell:

```
┌─────────────────────────────────────────────────────────────┐
│ Header (App title, search, user menu)                       │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│   Sidebar    │              Main Content                    │
│              │                                              │
│  - Nav items │  ┌─────────────────┬──────────────────────┐  │
│  - Filters   │  │   List View     │   Detail Panel       │  │
│  - Actions   │  │                 │                      │  │
│              │  │                 │                      │  │
│              │  └─────────────────┴──────────────────────┘  │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

**Implementation:**
```vue
<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <Sidebar />
    
    <!-- Main content with optional split view -->
    <div class="flex-1 flex">
      <ListView 
        :class="selectedDoc ? 'w-1/2' : 'w-full'"
        @select="selectDoc"
      />
      <DetailPanel 
        v-if="selectedDoc" 
        :doc="selectedDoc"
        class="w-1/2 border-l"
      />
    </div>
  </div>
</template>
```

### 1) Sidebar patterns

**Standard structure:**
```vue
<template>
  <aside class="w-56 border-r bg-gray-50 flex flex-col">
    <!-- App logo/title -->
    <div class="p-4 border-b">
      <h1 class="font-semibold">My App</h1>
    </div>
    
    <!-- Primary navigation -->
    <nav class="flex-1 p-2">
      <SidebarLink 
        v-for="item in navItems" 
        :key="item.name"
        :label="item.label"
        :icon="item.icon"
        :to="item.route"
        :count="item.count"
      />
    </nav>
    
    <!-- Quick filters (context-dependent) -->
    <div v-if="filters.length" class="p-2 border-t">
      <p class="text-xs text-gray-500 px-2 mb-1">Filters</p>
      <SidebarLink 
        v-for="filter in filters"
        :key="filter.name"
        :label="filter.label"
        :count="filter.count"
        @click="applyFilter(filter)"
      />
    </div>
    
    <!-- User/settings at bottom -->
    <div class="p-2 border-t">
      <UserMenu />
    </div>
  </aside>
</template>
```

**CRM example nav items:**
- Leads (with count badge)
- Deals (with count badge)
- Contacts
- Organizations
- Activities
- ---
- Settings

### 2) List view patterns

**Standard list with filters:**
```vue
<template>
  <div class="flex-1 flex flex-col">
    <!-- Toolbar -->
    <div class="flex items-center justify-between p-4 border-b">
      <div class="flex items-center gap-2">
        <Input 
          type="search" 
          placeholder="Search..." 
          v-model="searchQuery"
          :debounce="300"
        />
        <FilterDropdown :filters="availableFilters" v-model="activeFilters" />
      </div>
      <div class="flex items-center gap-2">
        <ViewToggle v-model="viewMode" :options="['list', 'kanban', 'grid']" />
        <Button variant="solid" @click="createNew">
          <template #prefix><FeatherIcon name="plus" /></template>
          New
        </Button>
      </div>
    </div>
    
    <!-- View modes -->
    <ListView v-if="viewMode === 'list'" :data="items" @row-click="select" />
    <KanbanView v-else-if="viewMode === 'kanban'" :data="items" :columns="stages" />
    <GridView v-else :data="items" @card-click="select" />
  </div>
</template>
```

**List row structure:**
```vue
<template>
  <div class="flex items-center p-3 hover:bg-gray-50 cursor-pointer border-b">
    <!-- Selection checkbox (for bulk actions) -->
    <Checkbox v-if="selectable" v-model="selected" class="mr-3" />
    
    <!-- Avatar/icon -->
    <Avatar :label="row.name" :image="row.image" class="mr-3" />
    
    <!-- Primary content -->
    <div class="flex-1 min-w-0">
      <p class="font-medium truncate">{{ row.title }}</p>
      <p class="text-sm text-gray-500 truncate">{{ row.subtitle }}</p>
    </div>
    
    <!-- Status badge -->
    <Badge :variant="statusVariant">{{ row.status }}</Badge>
    
    <!-- Metadata -->
    <span class="text-sm text-gray-500 ml-4">{{ timeAgo(row.modified) }}</span>
    
    <!-- Actions dropdown -->
    <Dropdown :options="rowActions" class="ml-2">
      <Button variant="ghost" icon="more-horizontal" />
    </Dropdown>
  </div>
</template>
```

### 3) Kanban view patterns

**Used in:** CRM (Deals), Helpdesk (Tickets by status)

```vue
<template>
  <div class="flex overflow-x-auto p-4 gap-4">
    <div 
      v-for="column in columns" 
      :key="column.name"
      class="flex-shrink-0 w-72 bg-gray-100 rounded-lg"
    >
      <!-- Column header -->
      <div class="p-3 font-medium flex items-center justify-between">
        <span>{{ column.label }}</span>
        <Badge>{{ column.items.length }}</Badge>
      </div>
      
      <!-- Cards -->
      <div class="p-2 space-y-2 min-h-[200px]">
        <KanbanCard 
          v-for="item in column.items"
          :key="item.name"
          :data="item"
          @click="select(item)"
          draggable
          @dragend="handleDrop"
        />
      </div>
      
      <!-- Add new in column -->
      <Button variant="ghost" class="w-full" @click="addTo(column)">
        + Add {{ column.singular }}
      </Button>
    </div>
  </div>
</template>
```

**Kanban card structure:**
```vue
<template>
  <div class="bg-white rounded-lg p-3 shadow-sm border cursor-pointer hover:shadow">
    <p class="font-medium mb-1">{{ data.title }}</p>
    <p class="text-sm text-gray-500 mb-2">{{ data.subtitle }}</p>
    <div class="flex items-center justify-between">
      <Avatar :label="data.assigned_to" size="sm" />
      <span class="text-xs text-gray-400">{{ data.due_date }}</span>
    </div>
  </div>
</template>
```

### 4) Detail panel / side panel

**Split view pattern (CRM/Helpdesk style):**
```vue
<template>
  <aside class="w-[480px] border-l bg-white flex flex-col">
    <!-- Header with close -->
    <div class="flex items-center justify-between p-4 border-b">
      <h2 class="font-semibold">{{ doc.name }}</h2>
      <Button variant="ghost" icon="x" @click="$emit('close')" />
    </div>
    
    <!-- Tabs -->
    <Tabs v-model="activeTab">
      <Tab name="details" label="Details" />
      <Tab name="activity" label="Activity" />
      <Tab name="notes" label="Notes" />
    </Tabs>
    
    <!-- Tab content -->
    <div class="flex-1 overflow-auto p-4">
      <DetailsTab v-if="activeTab === 'details'" :doc="doc" />
      <ActivityFeed v-else-if="activeTab === 'activity'" :doctype="doctype" :name="doc.name" />
      <NotesTab v-else :doctype="doctype" :name="doc.name" />
    </div>
    
    <!-- Footer actions -->
    <div class="p-4 border-t flex justify-end gap-2">
      <Button @click="edit">Edit</Button>
      <Button variant="solid" @click="primaryAction">{{ primaryActionLabel }}</Button>
    </div>
  </aside>
</template>
```

### 5) Form patterns

**Standard form layout:**
```vue
<template>
  <div class="max-w-2xl mx-auto p-6">
    <!-- Form header -->
    <div class="mb-6">
      <h1 class="text-xl font-semibold">{{ isNew ? 'New' : 'Edit' }} {{ doctype }}</h1>
    </div>
    
    <!-- Sections -->
    <FormSection title="Basic Information">
      <div class="grid grid-cols-2 gap-4">
        <FormControl label="Name" v-model="doc.name" :required="true" />
        <FormControl label="Status" type="select" v-model="doc.status" :options="statusOptions" />
      </div>
      <FormControl label="Description" type="textarea" v-model="doc.description" class="mt-4" />
    </FormSection>
    
    <FormSection title="Details" collapsible>
      <!-- More fields -->
    </FormSection>
    
    <!-- Actions -->
    <div class="flex justify-end gap-2 mt-6 pt-4 border-t">
      <Button @click="cancel">Cancel</Button>
      <Button variant="solid" @click="save" :loading="saving">Save</Button>
    </div>
  </div>
</template>
```

**FormSection component:**
```vue
<template>
  <div class="mb-6">
    <div 
      class="flex items-center justify-between mb-3 cursor-pointer"
      @click="collapsible && (collapsed = !collapsed)"
    >
      <h3 class="font-medium text-gray-700">{{ title }}</h3>
      <FeatherIcon v-if="collapsible" :name="collapsed ? 'chevron-down' : 'chevron-up'" />
    </div>
    <div v-show="!collapsed">
      <slot />
    </div>
  </div>
</template>
```

### 6) Activity feed pattern

**Used across all apps for tracking changes:**
```vue
<template>
  <div class="space-y-4">
    <!-- Add comment -->
    <div class="flex gap-3">
      <Avatar :label="$user.name" />
      <div class="flex-1">
        <Textarea v-model="newComment" placeholder="Add a comment..." rows="2" />
        <Button class="mt-2" @click="addComment" :disabled="!newComment">Comment</Button>
      </div>
    </div>
    
    <!-- Activity items -->
    <div v-for="item in activities" :key="item.name" class="flex gap-3">
      <Avatar :label="item.owner" size="sm" />
      <div class="flex-1">
        <div class="flex items-baseline gap-2">
          <span class="font-medium text-sm">{{ item.owner }}</span>
          <span class="text-xs text-gray-400">{{ timeAgo(item.creation) }}</span>
        </div>
        <!-- Different activity types -->
        <CommentContent v-if="item.type === 'comment'" :content="item.content" />
        <StatusChange v-else-if="item.type === 'status'" :from="item.from" :to="item.to" />
        <FieldChange v-else-if="item.type === 'change'" :field="item.field" :value="item.value" />
      </div>
    </div>
  </div>
</template>
```

### 7) Empty states

**Always provide helpful empty states:**
```vue
<template>
  <div class="flex flex-col items-center justify-center h-64 text-center">
    <FeatherIcon name="inbox" class="w-12 h-12 text-gray-300 mb-4" />
    <h3 class="font-medium text-gray-700 mb-1">{{ title }}</h3>
    <p class="text-sm text-gray-500 mb-4">{{ description }}</p>
    <Button v-if="action" variant="solid" @click="action.handler">
      {{ action.label }}
    </Button>
  </div>
</template>

<!-- Usage -->
<EmptyState 
  title="No leads yet"
  description="Create your first lead to get started"
  :action="{ label: 'Create Lead', handler: createLead }"
/>
```

### 8) Loading states

**Skeleton loaders for perceived performance:**
```vue
<!-- List skeleton -->
<template>
  <div v-if="loading" class="space-y-2 p-4">
    <div v-for="i in 5" :key="i" class="flex items-center gap-3 p-3">
      <Skeleton class="w-10 h-10 rounded-full" />
      <div class="flex-1">
        <Skeleton class="h-4 w-1/3 mb-2" />
        <Skeleton class="h-3 w-1/2" />
      </div>
    </div>
  </div>
  <ListView v-else :data="data" />
</template>
```

### 9) Color and status conventions

| Status Type | Color | Usage |
|-------------|-------|-------|
| Success/Active | Green (`bg-green-100 text-green-700`) | Completed, Active, Resolved |
| Warning/Pending | Yellow (`bg-yellow-100 text-yellow-700`) | Pending, In Progress, Due Soon |
| Error/Blocked | Red (`bg-red-100 text-red-700`) | Failed, Blocked, Overdue |
| Info/Default | Blue (`bg-blue-100 text-blue-700`) | New, Open, Info |
| Neutral | Gray (`bg-gray-100 text-gray-700`) | Draft, Cancelled, Closed |

**Badge component usage:**
```vue
<Badge variant="success">Active</Badge>
<Badge variant="warning">Pending</Badge>
<Badge variant="error">Overdue</Badge>
<Badge variant="info">New</Badge>
<Badge variant="subtle">Draft</Badge>
```

### 10) Responsive patterns

**Mobile-first considerations:**
```vue
<template>
  <!-- Hide sidebar on mobile, show as drawer -->
  <Sidebar v-if="!isMobile" />
  <Drawer v-else v-model="sidebarOpen">
    <Sidebar />
  </Drawer>
  
  <!-- Stack list and detail on mobile -->
  <div :class="isMobile ? 'flex-col' : 'flex'">
    <ListView v-show="!isMobile || !selectedDoc" />
    <DetailPanel v-if="selectedDoc" :fullScreen="isMobile" />
  </div>
</template>
```

## Component reference

Use these Frappe UI components consistently:

| Component | Usage |
|-----------|-------|
| `<Button>` | All actions, with variants: solid, subtle, ghost |
| `<Input>` | Text inputs, search fields |
| `<FormControl>` | Form fields with labels, validation |
| `<Select>` | Dropdowns, status selectors |
| `<Checkbox>` | Boolean inputs, bulk selection |
| `<Avatar>` | User images, entity icons |
| `<Badge>` | Status indicators, counts |
| `<Dropdown>` | Action menus, context menus |
| `<Dialog>` | Modal confirmations, forms |
| `<Tabs>` | Content organization |
| `<Tooltip>` | Helpful hints, truncated text |

## Verification

- [ ] App shell matches standard layout (sidebar + main + optional detail)
- [ ] List views have search, filters, view toggle, create button
- [ ] Detail panel has tabs (Details, Activity, Notes)
- [ ] Empty states are helpful with actions
- [ ] Loading states use skeletons, not spinners
- [ ] Status colors follow conventions
- [ ] Forms are sectioned and consistent
- [ ] Mobile experience is considered

## Failure modes / debugging

- **Inconsistent spacing**: Use TailwindCSS spacing scale (p-2, p-4, gap-2, gap-4)
- **Wrong component**: Check Frappe UI docs for correct component and props
- **Broken responsiveness**: Test at mobile breakpoints; use `sm:`, `md:`, `lg:` prefixes
- **Missing states**: Ensure loading, empty, and error states are handled

## Escalation

- For component implementation → `frontend-development`
- For backend API integration → `api-development`
- For enterprise workflows → `enterprise-patterns`

## References

- [references/app-shell-patterns.md](references/app-shell-patterns.md) — Detailed shell layouts
- [references/component-patterns.md](references/component-patterns.md) — Component usage guide
- [references/mobile-patterns.md](references/mobile-patterns.md) — Responsive design

## Guardrails

- **Study official apps first**: Before designing UI, review CRM, Helpdesk, or relevant official app for patterns
- **Use Frappe UI components**: Never create custom components when Frappe UI has an equivalent
- **Follow spacing conventions**: Use consistent padding/margins (4px increments)
- **Provide all states**: Every view needs loading, empty, and error states
- **Keep navigation consistent**: Sidebar structure should match official apps
- **Test responsively**: Ensure mobile experience works

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Custom app shell design | Unfamiliar UX for users | Copy CRM/Helpdesk shell structure |
| Missing empty states | Users confused when no data | Add EmptyState component with action |
| Spinner instead of skeleton | Jarring loading experience | Use Skeleton components for loading |
| Inconsistent status colors | User confusion | Follow color conventions table |
| Deep nesting without breadcrumbs | Users get lost | Add breadcrumb navigation |
| Modal overuse | Disruptive workflow | Prefer side panels for detail views |
| No keyboard navigation | Accessibility issues | Ensure Tab/Enter work for key flows |
