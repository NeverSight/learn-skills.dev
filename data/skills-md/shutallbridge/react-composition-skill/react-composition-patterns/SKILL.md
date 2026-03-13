---
name: react-composition-patterns
description: >
  Guides coding agents to write React components using composition patterns
  (children, compound components, render props, slots) instead of monolithic,
  prop-heavy components. Apply when writing, reviewing, or refactoring React components.
license: MIT
metadata:
  author: shutallbridge
  version: "1.0.0"
---

# React Composition Patterns

## Core Philosophy

**Composition over configuration.** Instead of adding props to control every rendering variation, break components into smaller pieces that consumers assemble. This produces components that are easier to understand, test, and extend without modifying the original source.

**Inversion of control.** Let consumers decide _what_ renders. The component provides behavior, structure, and state — the consumer provides content. A `<Dialog>` shouldn't accept `title`, `body`, `footer` strings. It should accept children that the consumer composes.

**Stable Dependency Principle.** Encapsulate what changes (rendering decisions, content) and expose what's stable (behavior, state management, accessibility). When a component's public API is stable, consumers can change their rendering without modifying the component itself.

**Prefer many small components over one big configurable one.** A component with 15 props is harder to use than 5 components with 3 props each. Small components compose; large components configure. If you catch yourself adding a boolean prop to toggle between two rendering modes, split into two components instead.

## Pattern Overviews

### Children Composition

The simplest composition pattern. A component accepts `children` and wraps them with layout, styling, or behavior — without knowing or caring what the children are.

```tsx
function Card({ children }: { children: React.ReactNode }) {
  return <div className="rounded-lg border p-6 shadow-sm">{children}</div>;
}

// Consumer composes freely
<Card>
  <h2>Title</h2>
  <p>Any content the consumer wants.</p>
</Card>
```

Use when building layout wrappers, containers, or any component whose job is to _wrap_ rather than _render_ content.

For detailed examples and common mistakes, see [rules/children-composition.md](rules/children-composition.md).

### Compound Components

A set of related components that share implicit state via `createContext`/`useContext`. The parent manages state; children consume it. This keeps the API declarative while allowing flexible composition.

```tsx
<Select onValueChange={setColor}>
  <Select.Trigger>
    <Select.Value placeholder="Pick a color" />
  </Select.Trigger>
  <Select.Content>
    <Select.Item value="red">Red</Select.Item>
    <Select.Item value="blue">Blue</Select.Item>
  </Select.Content>
</Select>
```

**Important:** Always use Context for shared state between compound component parts. Never use `React.Children.map`, `React.cloneElement`, or child type inspection — these approaches are not type-safe, break when children are wrapped in other components, and fail with fragments.

Use when building components with multiple sub-parts that share state (Tabs, Accordion, Select, Menu, Dialog).

For detailed examples and common mistakes, see [rules/compound-components.md](rules/compound-components.md).

### Render Props

A function prop that gives the consumer access to internal state or data while letting them control what renders. Useful when the component manages logic (fetching, measuring, tracking) and the consumer decides presentation.

```tsx
<Combobox options={users} filterFn={fuzzyMatch}>
  {({ inputProps, results, highlighted }) => (
    <div>
      <input {...inputProps} />
      <ul>
        {results.map((user, i) => (
          <li key={user.id} data-active={i === highlighted}>
            {user.name}
          </li>
        ))}
      </ul>
    </div>
  )}
</Combobox>
```

Use when the consumer needs full rendering control over data or state your component manages. Often combined with custom hooks — if there's no JSX to wrap, a hook is simpler.

For detailed examples and common mistakes, see [rules/render-props.md](rules/render-props.md).

### Slots Pattern

Named content areas via typed props. Instead of inspecting children by type, accept explicit props like `header`, `footer`, `sidebar`, `icon`. Fully type-safe, no `React.Children` dependency.

```tsx
interface PageLayoutProps {
  header: React.ReactNode;
  sidebar: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

function PageLayout({ header, sidebar, children, footer }: PageLayoutProps) {
  return (
    <div className="grid grid-cols-[250px_1fr] grid-rows-[auto_1fr_auto]">
      <header className="col-span-2">{header}</header>
      <aside>{sidebar}</aside>
      <main>{children}</main>
      {footer && <footer className="col-span-2">{footer}</footer>}
    </div>
  );
}
```

Use when a component has multiple named content areas with a fixed layout structure. Use `children` for the primary content area and named props for secondary areas.

For detailed examples and common mistakes, see [rules/slots-pattern.md](rules/slots-pattern.md).

### Polymorphic Components

A component that can render as different HTML elements or other components. **Don't roll your own `as` prop with complex generics** — use an established library approach instead.

**Radix UI approach (`asChild` + `<Slot>`):**
```tsx
import { Slot } from "@radix-ui/react-slot";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
}

function Button({ asChild, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";
  return <Comp {...props} />;
}

// Renders as a link with Button's props merged
<Button asChild>
  <a href="/home">Home</a>
</Button>
```

**Base UI approach (`render` prop):**
```tsx
<Switch.Root render={<label />}>
  <Switch.Thumb />
</Switch.Root>
```

Both approaches are well-supported since shadcn/ui works with both Radix and Base UI as of 2026. Pick whichever matches your project's existing primitive library.

For detailed examples and common mistakes, see [rules/polymorphic-components.md](rules/polymorphic-components.md).

### Custom Hooks

Extract reusable logic (state, effects, subscriptions, calculations) into hooks when multiple components need the same behavior. Hooks compose logic without affecting the component tree.

```tsx
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mql = window.matchMedia(query);
    setMatches(mql.matches);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener("change", handler);
    return () => mql.removeEventListener("change", handler);
  }, [query]);

  return matches;
}

// Any component can use it
function Sidebar() {
  const isDesktop = useMediaQuery("(min-width: 768px)");
  return isDesktop ? <DesktopSidebar /> : <MobileSidebar />;
}
```

Use when you need to share logic (not JSX) between components. If a render prop component has no meaningful wrapper JSX, it should probably be a hook instead.

For detailed examples and common mistakes, see [rules/custom-hooks.md](rules/custom-hooks.md).

## Decision Guide

Use this to pick the right pattern for your situation:

| Situation | Pattern |
|---|---|
| Flexible layout wrapper (Card, Section, Container) | **Children** |
| Multiple sub-parts sharing state (Tabs, Select, Accordion) | **Compound components** (Context) |
| Consumer needs rendering control with provided data | **Render props** |
| Multiple named content areas with fixed layout | **Slots** (typed props) |
| Component must render as different elements/components | **Polymorphic** (use a library) |
| Reusable logic, no JSX output | **Custom hooks** |

**Never do this:**
- Add boolean/config props to toggle between rendering modes (`showIcon`, `variant="card" | "list"`, `mode="compact"`)
- Use `React.Children.map` or `React.cloneElement` for shared state — use Context instead
- Build your own `as` prop with complex TypeScript generics — use Radix Slot or Base UI `render`
- Accept a config array/object when composition would be clearer (`items={[{label, icon, onClick}]}`)

## Anti-Pattern Red Flags

Watch for these signals that a component needs refactoring toward composition:

- **>5 rendering-related props** — the component is trying to be everything to everyone
- **Conditional rendering via `variant`/`type`/`mode` props** — these are separate components pretending to be one
- **Copy-pasting a component for a slight variation** — extract the shared parts and compose
- **Deeply nested ternaries in JSX** — the rendering logic is too complex for a single component
- **Wrapper that just passes props through** — eliminate the wrapper or use composition
- **`React.Children.map`, `React.cloneElement`, or `typeof child.type` checks** — use Context for shared state, typed props for slots
- **Config arrays for renderable items** — `items={[{label, icon}]}` should be `<Item icon={X}>Label</Item>`

For detailed examples and refactoring walkthroughs, see [rules/anti-patterns.md](rules/anti-patterns.md).
