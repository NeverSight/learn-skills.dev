---
name: react-composable-components
description: >
  Write and refactor React components to be small, composable, and customizable, doing one 
  thing well. Improve rendering performance, maintainability, and reusability by leveraging 
  compound components, prop spreading, and utility class merging. Apply these patterns when 
  authoring new components or breaking down large monolithic ones.
---

# React Composable Components

Patterns for authoring React components that are small, focused, and highly composable.

## Core idea

Large components that manage too much state and render multiple distinct UI areas suffer from poor readability, reusability, and render performance.

**Avoid:** Massive monolithic components that accept dozens of props (`hasHeader`, `showFooter`).  
**Prefer:** Breaking UI down into atomic, composable pieces (Compound Components) that transparently pass HTML attributes and merge utility classes for easy customization.

---

## 1. Extract Inline Render Methods

If a component has methods like `renderStoryScreen()`, extract them into independent child components. This prevents unnecessary re-renders of the entire monolith when small parts of the state change.

```tsx
// Prefer returning separate components instead of calling inline logic blocks
function App() {
  const [screen, setScreen] = useState('START');
  return (
    <main>
      {screen === 'START' && <StartScreen onStart={() => setScreen('STORY')} />}
      {screen === 'STORY' && <StoryScreen />}
    </main>
  );
}
```

---

## 2. Compound Components over Configuration Props

Instead of passing complex objects into a single component (`<MonolithCard footerButtons={<button>} />`), expose the sub-components. This allows the consumer to inject custom content or omit parts entirely.

```tsx
export function App() {
  return (
    <Card className="border-blue-500">
      <CardHeader>
        <CardTitle>Adventure Begins</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Consumer fully controls the layout and sub-components! */}
        <img src="/hero.png" alt="Hero" className="w-full h-auto" />
      </CardContent>
    </Card>
  );
}
```

---

## 3. Context for Shared State

When building complex compound components (like Tabs or Accordions), use a local React Context to share state internally, removing the need for consumers to manually drill props (`isOpen={isOpen} setIsOpen={setIsOpen}`).

```tsx
import { createContext, useContext, useState } from "react";

const TabsContext = createContext<{ activeTab: string; setActiveTab: (v: string) => void } | null>(null);

export function Tabs({ defaultValue, children }) {
  const [activeTab, setActiveTab] = useState(defaultValue);
  return <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>;
}

export function Tab({ value, children }) {
  const ctx = useContext(TabsContext);
  const isActive = ctx?.activeTab === value;
  return <button onClick={() => ctx?.setActiveTab(value)} className={isActive ? "font-bold" : ""}>{children}</button>;
}

export function TabContent({ value, children }) {
  const ctx = useContext(TabsContext);
  return ctx?.activeTab === value ? <div>{children}</div> : null;
}
```

**Usage:**

```tsx
<Tabs defaultValue="home">
  <Tab value="home">Home</Tab>
  <Tab value="settings">Settings</Tab>
  
  <TabContent value="home">Home Content!</TabContent>
  <TabContent value="settings">Settings Content!</TabContent>
</Tabs>
```

---

## 4. Transparent Props & ClassName Merging

Composable components should act like native HTML elements. Accept `className` and `...props` to give consumers full control without bloating the component API.

```tsx
import { forwardRef } from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs));

export const Button = forwardRef<HTMLButtonElement, React.ButtonHTMLAttributes<HTMLButtonElement>>(
  ({ className, variant = "primary", ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "rounded-md px-4 py-2 transition-colors",
        variant === "primary" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900",
        className
      )}
      {...props}
    />
  )
);
Button.displayName = "Button";
```

---

## 5. Concise Components with `react-twc`

Writing wrapper components with `forwardRef` and `className` merging can become boilerplate-heavy. When mapping styles to props, use [`react-twc`](https://react-twc.vercel.app/) for a styled-components-like API that automatically handles `forwardRef` and `className` merging.

```tsx
import { twc } from "react-twc";

export const Title = twc.h1`text-4xl font-extrabold tracking-tight`;

// Perfect for building Compound Components concisely:
export const Card = twc.div`rounded-xl border bg-card shadow`;
export const CardHeader = twc.div`flex flex-col space-y-1.5 p-6`;
export const CardTitle = twc.h3`font-semibold leading-none tracking-tight`;
export const CardContent = twc.div`p-6 pt-0`;
```

---

## Summary Checklist

- [ ] **Accept `className` and `...props`** in all reusable UI components.
- [ ] **Use a utility like `twMerge(clsx(...))`** or `react-twc` to merge default classes with consumer overrides naturally.
- [ ] **Expose structural pieces** (like `Header`, `Title`, `Content`) rather than relying on massive configuration prop objects.
- [ ] **Provide `ref` forwarding** (`React.forwardRef`) so parent components can interact directly with the underlying DOM elements.
- [ ] **Use local Context** for compound components that require shared internal state.
- [ ] **Break inline `renderSomething()` methods** into actual React components to optimize rendering.
