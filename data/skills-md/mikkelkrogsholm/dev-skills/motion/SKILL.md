---
name: motion
description: "Motion (formerly Framer Motion) — React and JavaScript animation library. Use when animating with Motion or Framer Motion: page transitions, hover/tap/drag gestures, scroll-triggered animations, exit animations, layout animations, spring physics, variants, AnimatePresence, useAnimate, useMotionValue, or migrating from framer-motion to the motion package. Fetch live documentation for up-to-date details."
---

# Motion

> **CRITICAL: Your training data for Motion is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs. Motion's docs are organized by topic — fetch the specific page for what you're implementing:
>
> - Animations: **`WebFetch("https://motion.dev/docs/animate")`**
> - React components: **`WebFetch("https://motion.dev/docs/react-quick-start")`**
> - Gestures: **`WebFetch("https://motion.dev/docs/react-gestures")`**
> - Scroll animations: **`WebFetch("https://motion.dev/docs/react-use-scroll")`**
> - Layout animations: **`WebFetch("https://motion.dev/docs/react-layout-animations")`**
>
> Do not proceed without fetching the relevant URL first. Never assume an API exists — verify against current docs.

Motion is a production-grade animation library for React and JavaScript — formerly known as Framer Motion, now independent and expanded to support vanilla JS and other frameworks.

## Key Capabilities

- **Declarative animations**: `motion` components animate via `initial`, `animate`, and `exit` props — no manual DOM manipulation
- **Variants**: Named animation states shared across component trees, with automatic stagger and orchestration
- **Exit animations**: `AnimatePresence` keeps unmounting components in the DOM until their `exit` animation completes
- **Layout animations**: `layout` prop uses FLIP technique to animate any CSS layout change automatically
- **Gestures**: Built-in `whileHover`, `whileTap`, `whileDrag`, and `whileFocus` props with full event callbacks
- **Motion values**: `useMotionValue` and `useTransform` create composable, signal-like values that update outside React's render cycle
- **Imperative API**: `animate()` function and `useAnimate` hook for programmatic control, usable outside React
- **Spring physics**: Default transition is spring-based; configure with `type: "spring"`, `stiffness`, `damping`, `mass`
- **Scroll animations**: `useScroll` and `useTransform` for scroll-linked animations without scroll event listeners

## Best Practices

- **Package is now `motion`, import from `motion/react` for React** — the old `framer-motion` package still works as a compatibility shim, but new projects should install `motion` and import from `motion/react`. Never mix imports from both packages in the same project.

  ```tsx
  // Correct (new)
  import { motion, AnimatePresence } from "motion/react"

  // Old (still works but deprecated)
  import { motion, AnimatePresence } from "framer-motion"
  ```

- **`AnimatePresence` requires a changing `key` prop on the child — missing key means exit animations never fire** — `AnimatePresence` tracks children by their `key`. If the key stays the same, Motion sees no unmount and the `exit` animation is skipped entirely. Always give the animated child a key tied to what changes.

  ```tsx
  // Wrong — key never changes, exit animation skipped
  <AnimatePresence>
    {show && <motion.div exit={{ opacity: 0 }}>Hello</motion.div>}
  </AnimatePresence>

  // Correct — key changes when content changes
  <AnimatePresence>
    {show && <motion.div key="hello" exit={{ opacity: 0 }}>Hello</motion.div>}
  </AnimatePresence>
  ```

- **Conditional rendering with `&&` bypasses `AnimatePresence`** — when you write `{condition && component}`, React removes the element from the tree immediately when `condition` is false. `AnimatePresence` never gets a chance to play the exit animation. Always place the condition inside `AnimatePresence` as a child, not outside it.

  ```tsx
  // Wrong — component removed before exit animation can play
  {isVisible && (
    <AnimatePresence>
      <motion.div key="box" exit={{ opacity: 0 }} />
    </AnimatePresence>
  )}

  // Correct — AnimatePresence controls the unmount
  <AnimatePresence>
    {isVisible && <motion.div key="box" exit={{ opacity: 0 }} />}
  </AnimatePresence>
  ```

- **Layout animations across separate components require `LayoutGroup`** — the `layout` prop animates an element's own position/size changes. When a layout change in one component should trigger layout animations in sibling or unrelated components, wrap them all in `LayoutGroup`. Without it, each component animates independently and the effect looks disconnected.

  ```tsx
  import { LayoutGroup } from "motion/react"

  <LayoutGroup>
    <Sidebar />   {/* layout prop inside */}
    <MainContent /> {/* layout prop inside — will coordinate with Sidebar */}
  </LayoutGroup>
  ```

- **`useMotionValue` and `useTransform` values do not trigger re-renders — do not read them in render logic** — motion values update synchronously and bypass React's reconciler for performance. Reading a motion value with `.get()` inside a render returns a snapshot that will not cause the component to re-render when it changes. Use `useMotionValueEvent` or `useTransform` to react to changes, or `motion` component props to bind them to the DOM.

  ```tsx
  const x = useMotionValue(0)

  // Wrong — x.get() won't trigger re-renders, displayed value will be stale
  return <div>Position: {x.get()}</div>

  // Correct — bind to a motion component prop; Motion updates the DOM directly
  return <motion.div style={{ x }} />

  // Correct — subscribe to changes with useMotionValueEvent
  useMotionValueEvent(x, "change", (latest) => console.log(latest))
  ```

- **`motion` components are React-only; `animate()` is the framework-agnostic imperative API** — use `motion.div`, `motion.span`, etc. only in React component trees. For animations in utility functions, vanilla JS, or outside JSX, use the `animate()` function imported from `motion` (not `motion/react`). `useAnimate` is a React hook that provides a scoped imperative API for complex sequences inside components.

  ```tsx
  // React component — use motion components
  import { motion } from "motion/react"
  const Card = () => <motion.div animate={{ opacity: 1 }} />

  // Vanilla JS / utility — use animate() from "motion"
  import { animate } from "motion"
  animate("#box", { opacity: 1 }, { duration: 0.3 })

  // Complex sequences inside React — use useAnimate
  import { useAnimate } from "motion/react"
  const [scope, animate] = useAnimate()
  ```
