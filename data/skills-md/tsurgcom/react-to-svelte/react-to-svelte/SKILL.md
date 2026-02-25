---
name: react-to-svelte
description: Convert React components to Svelte 5 using runes syntax. Handles hooks, pure components, JSX, effects, context, refs, events, and accessibility.
license: MIT
metadata:
  author: tsurg
  version: "1.0.0"
---

# React to Svelte 5 Converter

Convert React components to Svelte 5 components using modern runes syntax.

## When to Use

- Converting React components to Svelte
- Migrating React projects to Svelte
- Understanding React-to-Svelte patterns

## Core Conversions

### 1. Component Structure

**React:**

```jsx
import React from "react";

function MyComponent() {
  return <div>Hello</div>;
}

export default MyComponent;
```

**Svelte 5:**

```svelte
<div>Hello</div>
```

### 2. State Management

**React useState:**

```jsx
const [count, setCount] = useState(0);
setCount(count + 1);
```

**Svelte $state:**

```svelte
<script>
  let count = $state(0);
  count++; // Direct mutation works
</script>
```

**React useReducer:**

```jsx
const [state, dispatch] = useReducer(reducer, initialState);
```

**Svelte:**

```svelte
<script>
  let state = $state(initialState);

  function dispatch(action) {
    state = reducer(state, action);
  }
</script>
```

### 3. Derived Values

**React useMemo:**

```jsx
const doubled = useMemo(() => count * 2, [count]);
```

**Svelte $derived:**

```svelte
<script>
  let doubled = $derived(count * 2);
</script>
```

**React useCallback:**

```jsx
const handleClick = useCallback(() => {}, []);
```

**Svelte:**

```svelte
<script>
  // Just a regular function - no need for useCallback
  function handleClick() {}
</script>
```

### 4. Side Effects

**React useEffect:**

```jsx
useEffect(() => {
  console.log("mounted or updated");
  return () => console.log("cleanup");
}, [dep]);
```

**Svelte $effect:**

```svelte
<script>
  $effect(() => {
    console.log('mounted or updated');
    return () => console.log('cleanup');
  });
</script>
```

**React useLayoutEffect:**

```jsx
useLayoutEffect(() => {}, []);
```

**Svelte $effect.pre:**

```svelte
<script>
  $effect.pre(() => {});
</script>
```

### 5. Props

**React:**

```jsx
function Button({ label, onClick, disabled = false }) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}
```

**Svelte $props:**

```svelte
<script>
  let { label, onclick, disabled = false } = $props();
</script>

<button {onclick} {disabled}>{label}</button>
```

**With TypeScript:**

```svelte
<script lang="ts">
  interface Props {
    label: string;
    onclick: () => void;
    disabled?: boolean;
  }

  let { label, onclick, disabled = false }: Props = $props();
</script>
```

### 6. Pure Components

**React memo:**

```jsx
const MemoizedComponent = React.memo(Component);
```

**Svelte:**

```svelte
<!-- No equivalent needed - Svelte components are pure by default -->
```

### 7. Event Handling

**React:**

```jsx
<button onClick={handleClick} onMouseEnter={handleHover}>
```

**Svelte:**

```svelte
<button onclick={handleClick} onmouseenter={handleHover}>
```

**Event object:**

```svelte
<button onclick={(e) => handleClick(e)}>
```

### 8. Conditional Rendering

**React:**

```jsx
{
  isVisible && <Modal />;
}
{
  isLoading ? <Spinner /> : <Content />;
}
```

**Svelte:**

```svelte
{#if isVisible}
  <Modal />
{/if}

{#if isLoading}
  <Spinner />
{:else}
  <Content />
{/if}
```

**React ternary with null:**

```jsx
{
  condition ? <A /> : null;
}
```

**Svelte:**

```svelte
{#if condition}
  <A />
{/if}
```

### 9. List Rendering

**React:**

```jsx
{
  items.map((item, index) => <li key={item.id}>{item.name}</li>);
}
```

**Svelte:**

```svelte
{#each items as item, index (item.id)}
  <li>{item.name}</li>
{/each}
```

**With index only:**

```svelte
{#each items as item, i}
  <li>{i}: {item.name}</li>
{/each}
```

### 10. Context

**React:**

```jsx
const ThemeContext = createContext("light");
const theme = useContext(ThemeContext);
```

**Svelte:**

```svelte
<!-- Provider.svelte -->
<script>
  import { setContext } from 'svelte';
  setContext('theme', 'light');
</script>

<!-- Consumer.svelte -->
<script>
  import { getContext } from 'svelte';
  const theme = getContext('theme');
</script>
```

### 11. Refs

**React:**

```jsx
const inputRef = useRef(null);
<input ref={inputRef} />;
```

**Svelte:**

```svelte
<script>
  let inputRef = $state<HTMLInputElement | null>(null);
</script>

<input bind:this={inputRef} />
```

### 12. Forms and Two-Way Binding

**React:**

```jsx
const [value, setValue] = useState("");
<input value={value} onChange={(e) => setValue(e.target.value)} />;
```

**Svelte bind:**

```svelte
<script>
  let value = $state('');
</script>

<input bind:value />
```

**Checkbox:**

```svelte
<input type="checkbox" bind:checked={isChecked} />
```

### 13. Slots vs Children

**React:**

```jsx
function Card({ children, header }) {
  return (
    <div>
      <header>{header}</header>
      {children}
    </div>
  );
}
```

**Svelte:**

```svelte
<!-- Card.svelte -->
<div>
  <header>{@render header?.()}</header>
  {@render children?.()}
</div>

<!-- Usage -->
<Card>
  {#snippet header()}
    <h1>Title</h1>
  {/snippet}
  <p>Content</p>
</Card>
```

### 14. Styles

**React (CSS-in-JS):**

```jsx
<div style={{ color: 'red', fontSize: 14 }}>
```

**Svelte (scoped styles):**

```svelte
<div class="red-text">Content</div>

<style>
  .red-text {
    color: red;
    font-size: 14px;
  }
</style>
```

**Dynamic styles:**

```svelte
<div style:color={dynamicColor} style:font-size="{size}px">
```

## Advanced Patterns

### Custom Hooks to Functions

**React custom hook:**

```jsx
function useCounter(initial = 0) {
  const [count, setCount] = useState(initial);
  const increment = () => setCount((c) => c + 1);
  return { count, increment };
}
```

**Svelte:**

```javascript
// counter.svelte.js
export function createCounter(initial = 0) {
  let count = $state(initial);
  return {
    get count() {
      return count;
    },
    increment: () => count++,
  };
}
```

```svelte
<script>
  import { createCounter } from './counter.svelte.js';
  const counter = createCounter(0);
</script>

<button onclick={counter.increment}>
  Count: {counter.count}
</button>
```

### Higher-Order Components

**React HOC:**

```jsx
function withAuth(Component) {
  return function Wrapped(props) {
    const isAuth = useAuth();
    return isAuth ? <Component {...props} /> : <Login />;
  };
}
```

**Svelte (use wrapper component):**

```svelte
<!-- WithAuth.svelte -->
<script>
  let { component: Component, ...props } = $props();
  const isAuth = $derived(checkAuth());
</script>

{#if isAuth}
  <Component {...props} />
{:else}
  <Login />
{/if}
```

## Accessibility (a11y)

### ARIA Attributes

**React:**

```jsx
<div aria-label="Close dialog" aria-expanded={isOpen}>
```

**Svelte:**

```svelte
<div aria-label="Close dialog" aria-expanded={isOpen}>
```

### Keyboard Events

**React:**

```jsx
<div onKeyDown={handleKeyDown} tabIndex={0} role="button">
```

**Svelte:**

```svelte
<div onkeydown={handleKeyDown} tabindex="0" role="button">
```

### Focus Management

**React:**

```jsx
const buttonRef = useRef(null);
useEffect(() => {
  buttonRef.current?.focus();
}, []);
```

**Svelte:**

```svelte
<script>
  let buttonRef = $state<HTMLButtonElement | null>(null);

  $effect(() => {
    buttonRef?.focus();
  });
</script>

<button bind:this={buttonRef}>Focus me</button>
```

### Screen Reader Announcements

**React:**

```jsx
<div aria-live="polite" aria-atomic="true">
  {announcement}
</div>
```

**Svelte:**

```svelte
<div aria-live="polite" aria-atomic="true">
  {announcement}
</div>
```

### Svelte a11y Warnings

Svelte provides compile-time accessibility warnings:

- Missing alt attributes on images
- Invalid ARIA attributes
- Missing keyboard handlers on interactive elements
- Form elements without labels

### Reduced Motion

**React:**

```jsx
const prefersReducedMotion = useMediaQuery("(prefers-reduced-motion: reduce)");
```

**Svelte (using CSS):**

```svelte
<style>
  @media (prefers-reduced-motion: reduce) {
    * {
      animation: none !important;
      transition: none !important;
    }
  }
</style>
```

## Migration Checklist

1. [ ] Rename file from `.jsx/.tsx` to `.svelte`
2. [ ] Remove React imports
3. [ ] Convert function to Svelte structure (script/template/style)
4. [ ] Convert `useState` to `$state`
5. [ ] Convert `useEffect` to `$effect`
6. [ ] Convert `useMemo` to `$derived`
7. [ ] Convert props to `$props()`
8. [ ] Convert event handlers (camelCase to lowercase)
9. [ ] Convert conditional rendering to `{#if}` blocks
10. [ ] Convert `.map()` to `{#each}` blocks
11. [ ] Convert `useContext` to `getContext`
12. [ ] Convert `useRef` to `bind:this`
13. [ ] Add scoped styles
14. [ ] Review accessibility attributes
15. [ ] Test component behavior

## Common Pitfalls

1. **Direct mutation in Svelte works** - Don't try to maintain immutability habits from React
2. **Effects run immediately** - Unlike React's delayed effects, `$effect` runs synchronously
3. **Props are read-only** - Use callbacks for child-to-parent communication
4. **No virtual DOM** - Don't rely on React's reconciliation behavior
5. **Scoped styles by default** - Use `:global()` for global styles

## Examples

### Counter Component

**React:**

```jsx
import { useState } from "react";

function Counter({ initial = 0, step = 1 }) {
  const [count, setCount] = useState(initial);

  return (
    <button onClick={() => setCount((c) => c + step)}>Count: {count}</button>
  );
}
```

**Svelte:**

```svelte
<script>
  let { initial = 0, step = 1 } = $props();
  let count = $state(initial);
</script>

<button onclick={() => count += step}>
  Count: {count}
</button>
```

### Fetch Data Component

**React:**

```jsx
import { useState, useEffect } from "react";

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then((r) => r.json())
      .then((data) => {
        setUser(data);
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  return <div>{user?.name}</div>;
}
```

**Svelte:**

```svelte
<script>
  let { userId } = $props();

  let user = $state(null);
  let loading = $state(true);

  $effect(() => {
    loading = true;
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        user = data;
        loading = false;
      });
  });
</script>

{#if loading}
  <div>Loading...</div>
{:else}
  <div>{user?.name}</div>
{/if}
```

## Success Criteria

- Component renders correctly in Svelte
- All state updates work as expected
- Props are properly typed (if using TypeScript)
- Accessibility attributes are preserved
- Component follows Svelte 5 idioms and best practices
