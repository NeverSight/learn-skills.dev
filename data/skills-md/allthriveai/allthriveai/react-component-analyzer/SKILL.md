---
name: react-component-analyzer
description: Debug React component issues including TypeScript types, props, state management, hooks, and rendering problems. Use when troubleshooting component not rendering, prop errors, state not updating, hook issues, or TypeScript type mismatches.
allowed-tools: Read, Grep, Glob
---

# React Component Analyzer

Analyzes and debugs React/TypeScript component issues in this project.

## Project Context

- Frontend: React 18 with TypeScript
- Build tool: Vite
- State management: React Query (TanStack Query)
- Routing: React Router v6
- Styling: Tailwind CSS
- Components: `frontend/src/components/`
- Pages: `frontend/src/pages/`
- Types: `frontend/src/types/`
- Services: `frontend/src/services/`

## When to Use

- "Component not rendering"
- "Props not being passed"
- "State not updating"
- "useEffect not firing"
- "TypeScript error on component"
- "React Query not fetching"
- "Infinite re-renders"

## Debugging Approach

### 1. Component Structure
- Check component file exists and exports correctly
- Verify import paths are correct
- Check for TypeScript errors in props interface

### 2. Props and Types
- Verify prop types match between parent and child
- Check for optional vs required props
- Look for type mismatches with API responses

### 3. State and Hooks
- Check useState/useReducer initial values
- Verify useEffect dependencies
- Look for missing dependencies causing stale closures
- Check useMemo/useCallback usage

### 4. React Query Issues
- Verify query keys are correct
- Check enabled/refetch conditions
- Look for stale time and cache settings
- Verify mutation invalidations

## Common Issues

**Component not rendering:**
```typescript
// Check: Is it exported correctly?
export default ComponentName;  // or
export { ComponentName };

// Check: Is the route configured?
<Route path="/page" element={<ComponentName />} />
```

**Props type mismatch:**
```typescript
// Check: Does interface match API response?
interface Project {
  id: number;
  title: string;  // API might return 'name' not 'title'
}
```

**useEffect not firing:**
```typescript
// Check: Dependencies array
useEffect(() => {
  // This only runs when `id` changes
}, [id]);  // Missing dependency?
```

**React Query stale data:**
```typescript
// Check: Query invalidation after mutation
const mutation = useMutation({
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['projects'] });
  }
});
```

## Key Files to Check

```
frontend/src/
├── components/
│   ├── common/          # Shared components
│   ├── projects/        # Project-specific components
│   └── ui/              # UI primitives
├── pages/
│   ├── ExplorePage.tsx  # Explore/discovery page
│   ├── ProjectPage.tsx  # Single project view
│   └── DashboardPage.tsx
├── types/
│   ├── models.ts        # Data model types
│   └── api.ts           # API response types
├── services/
│   ├── api.ts           # Axios instance
│   └── projects.ts      # Project API calls
└── hooks/
    └── useProjects.ts   # Custom hooks
```

## Type Checking Tips

```bash
# Run TypeScript check
cd frontend && npx tsc --noEmit

# Check specific file
npx tsc --noEmit src/components/MyComponent.tsx
```

## Browser DevTools

- React DevTools: Inspect component tree, props, state
- Network tab: Verify API requests/responses
- Console: Check for React warnings/errors
