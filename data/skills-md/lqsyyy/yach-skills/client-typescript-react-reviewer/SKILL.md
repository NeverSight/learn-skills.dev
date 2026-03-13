---
name: client-typescript-react-reviewer
description: "Expert code reviewer for TypeScript + React 17 applications. Use when reviewing React code, identifying anti-patterns, evaluating Redux + Saga state management, or assessing code maintainability. Triggers: code review requests, PR reviews, React architecture evaluation, identifying code smells, TypeScript type safety checks, useEffect abuse detection, Redux/Saga pattern review."
---

# TypeScript + React 17 Code Review Expert

Expert code reviewer with deep knowledge of React 17, Redux, Redux-Saga, Ant Design 4, and TypeScript best practices.

## Review Priority Levels

### Critical (Block Merge)

These issues cause bugs, memory leaks, or architectural problems:

| Issue | Why It's Critical |
|-------|-------------------|
| `useEffect` for derived state | Extra render cycle, sync bugs |
| Missing cleanup in `useEffect` | Memory leaks (timers, event listeners) |
| Direct state mutation (`.push()`, `.splice()`) | Silent update failures (React/Redux) |
| Conditional hook calls | Breaks Rules of Hooks |
| `key={index}` in dynamic lists | State corruption on reorder |
| `any` type without justification | Type safety bypass |
| Missing `yield` in Sagas | Saga won't wait for effect, logic breaks |
| Blocking effects in Sagas | `call` or `take` blocking other loops unnecessarily |
| Illegal dependency | `_public`, `pages`, `plugins` importing from `im` |
| Missing `try-catch` | Critical in Sagas, JSON parsing, and async IO |

### High Priority

| Issue | Impact |
|-------|--------|
| Incomplete dependency arrays | Stale closures, missing updates |
| Props typed as `any` | Runtime errors |
| Unjustified `useMemo`/`useCallback` | Unnecessary complexity |
| Missing Error Boundaries | Poor error UX |
| Controlled input initialized with `undefined` | React warning |
| Missing error handling in Sagas | Crashes the generator/application |

### Architecture/Style

| Issue | Recommendation |
|-------|----------------|
| Component > 300 lines | Split into smaller components |
| Prop drilling > 2-3 levels | Use composition or Redux |
| State far from usage | Colocate state |
| Custom hooks without `use` prefix | Follow naming convention |
| Hardcoded constants | Use config files or constants.ts |

## Quick Detection Patterns

### useEffect Abuse (Most Common Anti-Pattern)

```typescript
// WRONG: Derived state in useEffect
const [firstName, setFirstName] = useState('');
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(firstName + ' ' + lastName);
}, [firstName, lastName]);

// CORRECT: Compute during render
const fullName = firstName + ' ' + lastName;
```

```typescript
// WRONG: Event logic in useEffect
useEffect(() => {
  if (product.isInCart) showNotification('Added!');
}, [product]);

// CORRECT: Logic in event handler
function handleAddToCart() {
  addToCart(product);
  showNotification('Added!');
}
```

### Redux + Saga Patterns

```typescript
// WRONG: Missing error handling in Saga (Critical)
function* fetchDataSaga(action) {
  const data = yield call(api.fetchData, action.payload);
  yield put(actions.fetchSuccess(data));
}

// CORRECT (Mandatory): Try-catch in Saga
function* fetchDataSaga(action) {
  try {
    const data = yield call(api.fetchData, action.payload);
    yield put(actions.fetchSuccess(data));
  } catch (error) {
    yield put(actions.fetchFailure(error));
  }
}
```

### TypeScript Red Flags

```typescript
// Red flags to catch
const data: any = response;           // Unsafe any
const items = arr[10];                // Missing undefined check
const App: React.FC<Props> = () => {}; // Discouraged pattern

// Preferred patterns
const data: ResponseType = response;
const items = arr[10]; // with noUncheckedIndexedAccess
const App = ({ prop }: Props) => {};  // Explicit props
```

## Review Workflow

1. **Scan for critical issues first** - Check for the patterns in "Critical (Block Merge)" section
2. **Evaluate Redux/Saga usage** - Check for proper effect usage and error handling in Sagas
3. **Assess ahooks usage** - Check if `ahooks` (useMount, useUnmount, etc.) are used for readability
4. **Assess TypeScript safety** - Generic components, discriminated unions, strict config
5. **Review for maintainability** - Component size, hook design, folder structure

## Reference Documents

For detailed patterns and examples:

- **[redux-saga-patterns.md](references/redux-saga-patterns.md)** - Best practices for Redux-Saga effects and flows
- **[antd-v4-patterns.md](references/antd-v4-patterns.md)** - Ant Design 4 component usage and Form/Table best practices
- **[electron-patterns.md](references/electron-patterns.md)** - Electron IPC, cleanup, and native integration
- **[antipatterns.md](references/antipatterns.md)** - Comprehensive anti-pattern catalog with fixes
- **[checklist.md](references/checklist.md)** - Full code review checklist for thorough reviews

## State Management Quick Guide

| Data Type | Solution |
|-----------|----------|
| Persistent Server Data | Redux + Redux-Saga |
| Cache/Fetching | TanStack Query (v4) |
| UI/Complex Global State | Redux |
| Component-local state | useState/useReducer |
| Performance Helpers | ahooks (useLatest, useUpdateEffect) |

## Specialized Review Rules

### 1. Localization (i18n)
Avoid hardcoded Chinese/English strings in JSX.
- **Wrong:** `<span>确定</span>`
- **Correct:** `<span>{util.locale('common_ok')}</span>`

### 2. Electron Cleanup
Always verify that IPC listeners and DOM event listeners have corresponding cleanup logic.

### Redux Mutation Anti-Pattern

```typescript
// NEVER mutate state in Reducers
case 'ADD_TODO':
  state.todos.push(action.payload);
  return state;

// Redux Toolkit or Immutable updates
case 'ADD_TODO':
  return { ...state, todos: [...state.todos, action.payload] };
```

## TypeScript Config Recommendations

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true
  }
}
```

`noUncheckedIndexedAccess` is critical - it catches `arr[i]` returning undefined.

## Immediate Red Flags

When reviewing, flag these immediately:

| Pattern | Problem | Fix |
|---------|---------|-----|
| `eslint-disable react-hooks/exhaustive-deps` | Hides stale closure bugs | Refactor logic |
| Component defined inside component | Remounts every render | Move outside |
| `useState(undefined)` for inputs | Uncontrolled warning | Use empty string |
| `React.FC` with generics | Generic inference breaks | Use explicit props |
| Large Saga without `takeLatest` | Race conditions / Performance | Use `takeLatest` or `takeEvery` correctly |