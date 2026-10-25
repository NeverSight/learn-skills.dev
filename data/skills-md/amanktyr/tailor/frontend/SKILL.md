---
name: frontend
description: Governs frontend development, UI components, React, Vue, Svelte, design system tokens, CSS, Tailwind, buttons, modals, forms, and responsive web performance optimization.
---

# Frontend Engineering Skill

Activate this skill when creating or modifying user interfaces, client components, styling systems, design tokens, hooks, or frontend state.

> **Operational Directive:** *Build responsive, accessible, resilient, and high-performance interfaces adhering strictly to the project's single design system with zero state-mutation bugs.*

---

## 1. Strict Negative Guardrail: Zero Unrequested Styling & Token Invariant

* **Zero Unrequested Styling Rule:** NEVER add, alter, or restyle CSS, classes, colors, gradients, dark-mode themes, or animations unless visual/styling changes are explicitly requested by the user.
* **Logic/State Isolation:** When implementing business logic, state management, API integration, or bugfixes, leave all styling attributes, classNames, and visual tags strictly untouched.
* **Inspect `.ai/UI.md` (or workspace manifests) first:** Identify the established styling framework (Tailwind CSS, CSS Modules, Styled Components, Vanilla CSS, shadcn/ui).
* **Strict Single Framework Rule:** Never import secondary styling frameworks (e.g. do not introduce Bootstrap, MUI, or Chakra if the project uses Tailwind CSS).
* **Zero Invented Tokens:** Never invent ad-hoc hex codes, magic margins/paddings, or arbitrary animations. Always reuse existing project theme tokens.
* **Unstyled Fallback:** If the project has no styling system and styling was not explicitly asked for, output clean, semantic, unstyled HTML. Never invent a custom CSS theme or inline styles unprompted.

---

## 2. Component Hierarchy & Separation of Concerns

Structure UI components using the **Smart Container vs Presentational Component** pattern:

```
┌────────────────────────────────────────────────────────┐
│ Smart / Container Component                            │
│ - Handles data fetching, URL query params, hooks       │
│ - Passes data and event callbacks to UI components     │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ Presentational / Dumb Component                        │
│ - Pure visual rendering, receives data via props       │
│ - Completely stateless or localized animation state    │
│ - High reusability across pages                        │
└────────────────────────────────────────────────────────┘
```

---

## 3. Performance & Core Web Vitals Optimization

* **Cumulative Layout Shift (CLS):** Always set explicit `width` and `height` (or aspect-ratio) on images, videos, and embed frames to eliminate visual jank.
* **Largest Contentful Paint (LCP):** Preload critical hero images and utilize modern formats (`.webp`, `.avif`).
* **Prevent Unnecessary Re-Renders:**
  - Avoid defining inline object literals or inline arrow functions inside hot loop renders.
  - Utilize `useMemo` and `useCallback` judiciously on computationally heavy operations.
* **Loading & Error State Ergonomics:** Every async component must gracefully handle 4 distinct states:
  1. Initial Loading (Skeleton placeholder, no layout shift)
  2. Data Rendered (Normal view)
  3. Empty State (Friendly message with actionable CTA)
  4. Error State (Clear feedback with retry button)

---

## 4. React Hook & State Lifecycle Invariants (Anti-Bug Guardrails)

### A. Immutable State Updates (Zero Direct Mutation)
* **Insecure / Buggy:**
  ```tsx
  // ❌ WRONG: Mutates state array directly; fails to trigger re-renders reliably
  items.push(newItem);
  setItems(items);
  ```
* **Correct Standard:**
  ```tsx
  // ✅ CORRECT: Return a brand new array reference
  setItems((prev) => [...prev, newItem]);
  ```

### B. No Redundant `useEffect` for Derived State
* **Anti-Pattern:** Syncing props to state or calculating filtered items inside `useEffect`:
  ```tsx
  // ❌ WRONG: Unnecessary state + extra render cycle
  const [filtered, setFiltered] = useState([]);
  useEffect(() => {
    setFiltered(items.filter((i) => i.active));
  }, [items]);
  ```
* **Correct Standard:** Calculate directly during rendering (or wrap with `useMemo` if expensive):
  ```tsx
  // ✅ CORRECT: Pure computation with zero extra render passes
  const filtered = useMemo(() => items.filter((i) => i.active), [items]);
  ```

### C. Strict List Key Invariant (Never Use Array Index for Dynamic Lists)
* **Anti-Pattern:** `<li key={index}>` on lists that can be reordered, deleted, or inserted dynamically (causes subtle input value corruption and rendering bugs).
* **Correct Standard:** Always use a stable, unique item identifier:
  ```tsx
  {items.map((item) => (
    <UserRow key={item.id} user={item} />
  ))}
  ```

### D. Memory Leak Prevention & Effect Cleanup
Every effect initiating an async network call, event listener, timer, or WebSocket must return an explicit cleanup function:
```tsx
useEffect(() => {
  const controller = new AbortController();

  async function loadData() {
    try {
      const res = await fetch(`/api/items?id=${id}`, { signal: controller.signal });
      const data = await res.json();
      setData(data);
    } catch (err: any) {
      if (err.name !== 'AbortError') setError(err);
    }
  }

  loadData();
  return () => controller.abort(); // Cancel in-flight request when component unmounts or ID changes
}, [id]);
```

---

## 5. Mandatory Frontend Pre-Commit Checklist

Before approving any UI or component change, verify:
* [ ] **Styling Isolation:** Did not alter existing visual styles unless requested.
* [ ] **Key Invariant:** No dynamic lists use array index as `key`.
* [ ] **Cleanup Invariant:** All `useEffect` listeners, intervals, and fetch subscriptions have cleanup handlers.
* [ ] **Derived State:** No redundant state variables synced via `useEffect`.
* [ ] **4-State UI Coverage:** Loading, Error, Empty, and Success states handled cleanly.
