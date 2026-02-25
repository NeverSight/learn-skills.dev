---
name: search-filtering
description: Search UX, filter patterns, sort options, and empty states. Use when building search interfaces or filterable lists.
version: 1.0.0
---

# Search & Filtering

This skill covers search and filter patterns — search UX, filter types, sort options, and empty states for filtered results.

## Use-When

This skill activates when:
- Agent builds search interfaces
- Agent creates filterable lists or tables
- Agent designs sort functionality
- Agent handles empty search/filter results

## Core Rules

- ALWAYS show results count or "no results" message
- ALWAYS allow clearing filters
- ALWAYS maintain filter state during session
- PREFER instant search for small datasets
- PREFER URL params for shareable filtered views

## Common Agent Mistakes

- No feedback for empty results
- Filters that can't be cleared
- No indication of active filters
- Search that only triggers on submit (when instant is better)

## Examples

### ✅ Correct

```tsx
<SearchInput 
  value={query} 
  onChange={setQuery}
  placeholder="Search items..."
/>

<div className="flex gap-2">
  <FilterChip active={filter === 'all'} onClick={() => setFilter('all')}>
    All
  </FilterChip>
  <FilterChip active={filter === 'active'} onClick={() => setFilter('active')}>
    Active
  </FilterChip>
</div>

{results.length === 0 && (
  <EmptyState message="No results found" />
)}
```

### ❌ Wrong

```tsx
<input placeholder="Search" />
{/* No feedback when empty */}
```

## References

- [Search UX](https://www.nngroup.com/articles/search/)
