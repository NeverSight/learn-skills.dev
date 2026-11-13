---
name: refactor
description: "Code refactoring. Use for 'refactor', 'cleanup', 'improve' requests"
allowed-tools: Read, Write, Edit, Grep, Glob, Task
---

# Refactor Skill

## Role

Refactorer who improves code quality and maintainability

## Refactoring Principles

### Behavior Preservation
- Keep existing functionality intact
- Minimize external interface (API, props) changes
- Make incremental changes

### Step-by-step Approach
1. Understand current code
2. Write tests if possible
3. Refactor in small units
4. Verify behavior at each step

## Refactoring Patterns

### Component Separation
**Before**
```tsx
function BigComponent() {
  // 200 lines of code...
}
```

**After**
```tsx
function BigComponent() {
  return (
    <>
      <Header />
      <Content />
      <Footer />
    </>
  );
}
```

### Custom Hook Extraction
**Before**
```tsx
function Component() {
  const [data, setData] = useState();
  useEffect(() => { /* complex logic */ }, []);
  // ...
}
```

**After**
```tsx
function useComplexLogic() {
  const [data, setData] = useState();
  useEffect(() => { /* complex logic */ }, []);
  return { data };
}

function Component() {
  const { data } = useComplexLogic();
}
```

### Type Consolidation
**Before**
```typescript
// Duplicate types in multiple files
type Session = { id: string; title: string; }
```

**After**
```typescript
// packages/shared/src/index.ts
export type Session = { id: string; title: string; }
```

### Service Layer Separation
**Before**
```typescript
router.get('/', async (req, res) => {
  // Complex business logic in route...
});
```

**After**
```typescript
// services/feature.service.ts
export async function getFeatures() { /* logic */ }

// routes/feature.ts
router.get('/', async (req, res) => {
  const result = await getFeatures();
  res.json(result);
});
```

## Project-specific Refactoring Points

### apps/web
- Large components → Split into smaller components
- Repeated logic → Extract to custom hooks
- Inline styles → Tailwind classes

### apps/server
- Logic in routes → Separate to services
- Duplicate validation → Extract to middleware
- Hardcoded values → Constants/environment variables

### packages/shared
- Duplicate types → Consolidate
- Share utility functions
