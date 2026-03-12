---
name: ahooks
description: Comprehensive ahooks React hooks library specialist. Expert in all 76+ ahooks hooks including state management, effects, data fetching, performance optimization, DOM utilities, and advanced patterns. Use when working with ahooks library, need React hooks utilities or want to learn best practices.
---

# Ahooks React Hooks Library

This skill provides comprehensive expertise for the ahooks React hooks library, covering all 76+ hooks with detailed documentation, examples, and best practices.

## Quick Start

### Basic Usage
```jsx
import { useRequest, useMount, useSetState } from 'ahooks';

const MyComponent = () => {
  const { data, loading, error } = useRequest('/api/data');
  const [state, setState] = useSetState({ count: 0 });

  useMount(() => {
    console.log('Component mounted');
  });

  return <div>{data}</div>;
};
```

### Common Patterns
- **State Management**: `useSetState`, `useToggle`, `useBoolean` for complex state
- **Data Fetching**: `useRequest` for API calls with caching, retry, polling
- **Performance**: `useDebounce`, `useThrottle` for optimization
- **Lifecycle**: `useMount`, `useUnmount`, `useUpdateEffect` for component lifecycle

## Hook Categories

This skill organizes hooks into 9 main categories:

### 📊 State Management (12 hooks)
State utilities for complex state handling.
**See:** [state-hooks.md](references/state-hooks.md)

### 🔄 Lifecycle Effects (9 hooks)
Component lifecycle and effect management.
**See:** [effect-hooks.md](references/effect-hooks.md)

### 🌐 Data Fetching (6 hooks)
API calls, pagination, infinite scroll, and data caching.
**See:** [request-hooks.md](references/request-hooks.md)

### ⚡ Performance Optimization (9 hooks)
Debounce, throttle, memoization, and RAF optimizations.
**See:** [performance-hooks.md](references/performance-hooks.md)

### 🎨 DOM & UI (12 hooks)
Event listeners, sizing, scrolling, and UI interactions.
**See:** [dom-hooks.md](references/dom-hooks.md)

### 💾 Storage (4 hooks)
Local storage, session storage, cookies, and URL state.
**See:** [dom-hooks.md](references/dom-hooks.md)

### 🌍 Browser APIs (8 hooks)
Network status, visibility, keyboard events, and browser features.
**See:** [dom-hooks.md](references/dom-hooks.md)

### ⏰ Timers (4 hooks)
Intervals, timeouts, and countdown utilities.
**See:** [advanced-hooks.md](references/advanced-hooks.md)

### 🚀 Advanced Utilities (12 hooks)
WebSockets, history management, reactive data, and complex patterns.
**See:** [advanced-hooks.md](references/advanced-hooks.md)

## Getting Help

### Ask About:
- **Hook Usage**: "How to use useRequest with pagination?"
- **Migration**: "How to migrate from useState to useSetState?"
- **Best Practices**: "Performance tips for React hooks?"
- **Integration**: "How to combine useRequest with useAntdTable?"
- **Troubleshooting**: "Why is my useDebounce not working?"
- **TypeScript**: "Type definitions for useBoolean?"

### Comprehensive Guides
- [Migration Guide](references/migration-guide.md) - From React built-ins
- [Best Practices](references/best-practices.md) - Performance and patterns

## Quick Reference

```javascript
// Most commonly used hooks
import {
  useRequest,      // Data fetching
  useMount,        // Component mount
  useUnmount,      // Component unmount
  useSetState,     // State management
  useDebounce,     // Performance
  useThrottle,     // Performance
  useEventListener // DOM events
} from 'ahooks';
```