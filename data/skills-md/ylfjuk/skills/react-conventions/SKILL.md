---
name: react-conventions
description: Standards for writing React code — props, JSX, component structure, effects. Use when writing or reviewing any component or hook, even if conventions aren't mentioned. Targets React 19.
---

# React Conventions

Standards for how React is written here. Assumes the `typescript-conventions` skill for enums, mappers, schemas, casts, control flow, and exports, and the `project-structure` skill for file naming and placement.

**Precedence.** Existing standards supersede this guide — the organization's, the language's, the framework's, and the repo's own, in that order. See the precedence rule in `project-structure`. Refactor existing code toward these standards only when asked to.

## Props

Name the props type `Props`:

```tsx
type Props = {
	title: string;
};
```

If the type must be exported, or the file contains multiple components (discouraged — prefer one per file), name it for its component: `CardProps`.

When a component takes children, use `PropsWithChildren`:

```tsx
import type { PropsWithChildren } from "react";

type Props = { title: string };

export function Card(props: PropsWithChildren<Props>) {
	/* ... */
}
```

**Do not use `React.FC`.** TypeScript's inference is simpler, safer, and avoids implicit `children`.

### Destructure in the body, not the signature

```tsx
// ✅ Preferred
export function Card(props: Props) {
	const { title, children } = props;

	return <div>{title}</div>;
}

// ⚠️ Acceptable for very simple components
export function Card({ title, children }: Props) {
	return <div>{title}</div>;
}
```

Body destructuring is clearer when debugging and makes it easy to add defaults, logging, or a spread without reshaping the signature.

### Destructure order

1. Variables — `{ isEnabled }`
2. Variables with defaults — `{ isEnabled = false }`
3. Functions — `{ onClick }`
4. Functions with defaults — `{ onClose = noop }`
5. Ref — `{ ref }`
6. Children — `{ children }`
7. Rest — `{ ...rest }`

```tsx
export function Button(props: Props) {
	const { title, isDisabled = false, onClick, onClose = noop, ref, children, ...rest } = props;
}
```

## JSX prop order

1. `key`
2. `ref`
3. Truthy booleans, shorthand — `isEnabled`, never `isEnabled={true}`
4. Constants and literals — `prop={"value"}`, `prop={42}`
5. Variables and state — `prop={variable}`
6. Functions and handlers — `onClick={handleClick}`

```tsx
<Component key={key} ref={ref} isEnabled prop={"value"} label={label} onClick={handleClick} />
```

**Braces on string props**, including literals: `prop={"value"}`, not `prop="value"`. Every other value needs the braces anyway, so this keeps one shape at every call site. This applies to props only — plain text children stay unwrapped: `<div>text</div>`.

Most configs set `react/jsx-curly-brace-presence` to `never` for props, which will strip these on `--fix`. Configure it to match:

```jsonc
"react/jsx-curly-brace-presence": ["error", { "props": "always" }]
```

**Note the two orders differ deliberately.** `ref` is second at the call site and fifth in the destructure. At the call site `key` and `ref` are identity and meta, so they surface where a reader scans first; in the body they're passthrough plumbing you rarely touch, so they sink next to `children` and `...rest`.

## Component declaration

Use **function declarations**. Arrow functions are for small one-liner components, or components declared inside another component or method.

```tsx
// ✅
export function Card(props: Props) {
	/* ... */
}

// ✅ one-liner
const Divider = () => <hr />;
```

### Compound components

Use the compound pattern for elements meant to be used together:

```tsx
export function Dropdown(props: PropsWithChildren) {
	const { children } = props;

	return <div>{children}</div>;
}

Dropdown.Item = DropdownItem;
```

The sub-component can be inline or imported from its own file — `./dropdown-item.tsx`, kebab-case like any other file.

## Component body order

1. **Props destructure**
2. **Hooks and constants** the hooks or effects depend on
3. **Effects**
4. **Other constants** — derived values and handlers used only by the JSX
5. **Early returns**
6. **JSX**

```tsx
export function UserPanel(props: Props) {
	const { userId, onSelect } = props;

	const containerRef = useRef<HTMLDivElement>(null);
	const { data, isLoading } = useUser(userId);
	const sortedItems = useMemo(() => sort(data), [data]);

	useEffect(() => {
		/* ... */
	}, [userId]);

	const label = formatLabel(sortedItems);

	function handleSelect() {
		setIsOpen(false);
		onSelect?.();
	}

	if (isLoading) return <Spinner />;
	if (!data) return null;

	return <div ref={containerRef}>{label}</div>;
}
```

**What separates band 2 from band 4:** anything a hook or effect needs goes above the effects; anything only the JSX needs goes below.

Within band 2, prefer `useRef` → `useMemo` → `useCallback`. This is a soft preference — dependencies between hooks, or on non-hook values, override it.

Early returns over a top-level ternary, and over nesting generally — see the control flow section of `typescript-conventions`.

## Event handlers

**`onX` for props, `handleX` for internal wrappers.** A `handleX` wrapper should do something beyond forwarding — its name tells the reader there's extra logic to find.

```tsx
// ❌ pointless wrapper
function handleClick() {
  onClick();
}
<button onClick={handleClick} />

// ✅ pass it straight through
<button onClick={onClick} />

// ✅ the wrapper earns its name
function handleClick() {
  setIsOpen(false);
  onClick?.();
}
<button onClick={handleClick} />
```

Call an optional handler with `onClick?.()`. When the destructure supplied a default (`onClose = noop`), call it directly.

## Hooks and effects

Follow React's [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) — **avoid unnecessary effects.**

When an effect genuinely must handle an event, pair it with [`useEffectEvent`](https://react.dev/reference/react/useEffectEvent).

Place effects after all other hooks, per the body order above.

Custom hooks return an object once there are more than two values; a tuple is fine for one or two.

When a hook takes an options object, name the type `Options`, paralleling `Props`:

```ts
type Options = { userId: string; isEnabled?: boolean };

export function useUser(options: Options) {}
```

A hook taking a single bare value needs no type at all — don't wrap one argument in an object to have somewhere to put the name.

## Keys

Never use an array index as `key`. React reuses the wrong component instance on reorder, insert, or delete, which corrupts state silently.

```tsx
{
	items.map((item) => <Row key={item.id} />);
} // ✅
{
	items.map((item, index) => <Row key={index} />);
} // ❌
```

Enforced by `react/no-array-index-key`. A constant, predefined array that never reorders is the harmless case, but enable the rule and disable it inline there rather than relying on judgment.

## React 18

React 19 is the target. On 18, two things change:

- **`ref` is not a prop.** Use `forwardRef`, taking `ref` as the second argument. Such a component is a `const`, not a function declaration, and `ref` drops out of the props destructure order.

    ```tsx
    export const Input = forwardRef<HTMLInputElement, Props>((props, ref) => {
    	const { value, onChange, ...rest } = props;
    });
    ```

- **`useEffectEvent` doesn't exist** — it shipped stable in 19.2. Use a local equivalent or the `useRef` pattern.

Everything else applies unchanged.
