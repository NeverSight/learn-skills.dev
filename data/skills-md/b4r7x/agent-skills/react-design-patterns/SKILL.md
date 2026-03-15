---
name: react-design-patterns
description: Use when choosing a React component pattern — custom hooks, control props, compound components, headless components, render props, container/presentational, or other architectural patterns. Includes 13 patterns with decision guide and 2025 popularity ranking.
metadata:
  author: b4r7x
  version: "1.0.0"
---

# React Design Patterns

## Overview

13 patterns ranked by 2025 popularity. Golden rule: **start with a Custom Hook — upgrade to Compound Components only if structural sharing is needed**.

## Pattern Decision Guide

| Need | Pattern |
|------|---------|
| Reusable logic, no UI opinion | Custom Hook |
| Controlled vs uncontrolled component behavior | Control Props |
| Tightly coupled UI subcomponents (Tabs, Modal, Accordion) | Compound Components |
| Logic without imposed styling | Headless Component |
| Separate data fetching from rendering | Container / Presentational |
| Global stable state (auth, theme) | Provider (Context) |
| Reverse data flow (child → parent) | Render Props |
| Full render control via children | Children as Function |
| Flexible API with pre-built props | Props Getters |
| Crash isolation | Error Boundary |
| Render outside DOM parent (modals, tooltips) | Portal |
| Design system hierarchy | Atomic Design |

## 1. Custom Hook ⭐⭐⭐⭐⭐

Extract stateful logic into a reusable function. Most popular pattern in 2025.

```jsx
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try { return JSON.parse(localStorage.getItem(key)) ?? initialValue; }
    catch { return initialValue; }
  });
  const set = useCallback((v) => {
    setValue(prev => {
      const next = v instanceof Function ? v(prev) : v;
      localStorage.setItem(key, JSON.stringify(next));
      return next;
    });
  }, [key]);
  return [value, set];
}
```

## 2. Control Props ⭐⭐⭐⭐

Component supports both **controlled** (parent owns state via props) and **uncontrolled** (manages own state) modes. Every form input and component library uses this.

```jsx
// Controlled — parent manages state
<EditableTitle title={title} onChange={setTitle} />

// Uncontrolled — component manages own state, parent can reset via key
<EditableTitle key={userId} defaultTitle="Untitled" />

// Implementation supporting both modes
function EditableTitle({ title, defaultTitle = '', onChange }) {
  const [internal, setInternal] = useState(defaultTitle);
  const isControlled = title !== undefined;
  const value = isControlled ? title : internal;

  const handleChange = (e) => {
    if (!isControlled) setInternal(e.target.value);
    onChange?.(e.target.value);
  };

  return <input value={value} onChange={handleChange} />;
}
```

## 3. Compound Components ⭐⭐⭐⭐

Family of subcomponents sharing state via local context. Used by Radix UI, Headless UI, React Aria.

```jsx
const TabsContext = createContext(null);
function Tabs({ children, defaultTab }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  const value = useMemo(() => ({ activeTab, setActiveTab }), [activeTab]);
  return <TabsContext.Provider value={value}>{children}</TabsContext.Provider>;
}
Tabs.Tab = function({ id, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return <button className={activeTab === id ? 'active' : ''} onClick={() => setActiveTab(id)}>{children}</button>;
};
Tabs.Panel = function({ id, children }) {
  const { activeTab } = useContext(TabsContext);
  return activeTab === id ? <div>{children}</div> : null;
};
```

Always guard with a custom hook:
```jsx
function useTabs() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tabs.* must be used inside <Tabs>');
  return ctx;
}
```

## 4. Headless Component ⭐⭐⭐⭐

Hook provides logic only — zero HTML, zero CSS. You own the UI completely.

```jsx
function useAccordion() {
  const [openIndex, setOpenIndex] = useState(null);
  const toggle = useCallback((i) => setOpenIndex(prev => prev === i ? null : i), []);
  const isOpen = useCallback((i) => openIndex === i, [openIndex]);
  return { toggle, isOpen };
}
// Two completely different UIs can use the same hook
```

## 5. Container / Presentational ⭐⭐⭐

Split into: **Container** (logic, fetch, navigation) and **Presentational** (receives data via props, renders only).

```jsx
// Presentational — pure UI, easy to test
const UserCard = ({ user, onFollow }) => (
  <div><h2>{user.name}</h2><button onClick={onFollow}>Follow</button></div>
);
// Container — logic and data
const UserCardContainer = ({ userId }) => {
  const { user, follow } = useUser(userId);
  if (!user) return <Skeleton />;
  return <UserCard user={user} onFollow={follow} />;
};
```

## 6. Provider (Context) ⭐⭐⭐⭐

`createContext` + `useContext` for global/local state. See `react-usecontext` skill for full details.

## 7. Render Props ⭐⭐

Pass a **function as prop** — component calls it with data:

```jsx
<WindowSize render={({ width }) => (
  width < 768 ? <MobileMenu /> : <DesktopMenu />
)} />
```

Useful for reverse data flow (child → parent). Mostly replaced by custom hooks in 2025.

## 8. Children as Function ⭐⭐

Variant of render props — function passed as `children`. Popularized by Formik, Downshift:

```jsx
<Toggle>
  {({ on, toggle }) => (
    <button onClick={toggle}>{on ? 'ON' : 'OFF'}</button>
  )}
</Toggle>
```

## 9. Props Getters ⭐⭐

Hook returns pre-built prop objects to spread on elements. Used by React Hook Form (`register`), react-table:

```jsx
function useToggle() {
  const [on, setOn] = useState(false);
  const getTogglerProps = (overrides = {}) => ({
    onClick: () => setOn(prev => !prev),
    'aria-pressed': on,
    ...overrides,
  });
  return { on, getTogglerProps };
}
// Usage: <button {...getTogglerProps({ className: 'my-btn' })}>
```

## 10. Error Boundary ⭐⭐

Catches JS errors in the component tree, shows fallback UI. Requires class component or `react-error-boundary` library:

```jsx
import { ErrorBoundary } from 'react-error-boundary';
<ErrorBoundary FallbackComponent={ErrorFallback} onReset={() => { /* reset state */ }}>
  <Dashboard />
</ErrorBoundary>
```

Underused — most apps should have granular error boundaries per section.

## 11. Portal ⭐⭐⭐

Renders outside the DOM parent tree. Solves z-index, overflow: hidden, clipping:

```jsx
import { createPortal } from 'react-dom';
function Modal({ isOpen, children }) {
  if (!isOpen) return null;
  return createPortal(
    <div className="modal-overlay">{children}</div>,
    document.body
  );
}
```

## 12. HOC (Higher-Order Component) ⭐ — Legacy

Function that takes a component, returns a new component. **Replaced by custom hooks in modern code.**

```jsx
// Legacy
const ProtectedDashboard = withAuth(Dashboard);
// Modern equivalent
function ProtectedRoute({ children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  return children;
}
```

## 13. Atomic Design ⭐⭐⭐

Hierarchy: **Atoms** (Button) → **Molecules** (SearchBox = Input + Button) → **Organisms** (Header) → **Templates** (layout without data) → **Pages** (template with data). Great for design systems and large team projects.

## References
- [Compound Pattern — patterns.dev](https://www.patterns.dev/react/compound-pattern/) — visual guide to compound components with context
- [Compound Components with React Hooks](https://kentcdodds.com/blog/compound-components-with-react-hooks) — Kent C. Dodds' canonical tutorial
- [React Design Patterns — Telerik](https://www.telerik.com/blogs/react-design-patterns-best-practices) — survey of modern patterns with best practices
