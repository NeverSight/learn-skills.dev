---
name: component-library
description: Builds reusable, accessible UI components with consistent APIs for variants, sizes, states, slots and controlled or uncontrolled use, a complete state matrix, WAI-ARIA keyboard patterns for buttons, dialogs, menus and tabs, token-based styling and stories. Use when asked to create a button, modal, dropdown or tabs component, or to start or clean up a component library. Not for writing system documentation (use design-system-docs).
---

# Component Library

Produces components with predictable APIs, complete interaction states, built-in accessibility, and token-based styling, plus examples that show every variant and state.

## When to use
- "Create a Button / Modal / Dropdown / Tabs component."
- "Our components are inconsistent; clean up the library."
- Starting a shared UI package used by several apps.
- Turning repeated one-off UI into reusable components.
- Auditing components for keyboard and screen reader support.

## Workflow
1. Inventory existing components and tokens in the repo and reuse their naming and patterns. If no tokens exist, set them up with design-tokens.
2. Write the API before the code: props, variants, sizes, slots, events, controlled and uncontrolled behavior, ref forwarding.
3. Fill the state matrix (variant × size × state) and mark invalid combinations.
4. Look up the matching WAI-ARIA Authoring Practices (APG) pattern and list its roles, states, and keyboard interactions.
5. Implement with native elements first (`button`, `dialog`, `input`), adding ARIA only where native semantics fall short.
6. Style only with semantic tokens, as CSS custom properties or Tailwind theme values mapped to them.
7. Write stories or examples for every variant and state, with keyboard and automated accessibility checks.
8. Add brief usage notes; hand fuller documentation to design-system-docs.

## Rules
**API**
- Reuse prop names across components: `variant`, `size`, `disabled`, `value`/`defaultValue`/`onValueChange`, `open`/`defaultOpen`/`onOpenChange`. Stateful components support controlled and uncontrolled use.
- Forward refs, spread remaining props onto the root element, and merge `className` instead of replacing it.
- Composition over configuration: prefer `children` and sub-components (`Dialog.Title`, `Card.Footer`) to long lists of boolean props.
- Variants name intent (`primary`, `secondary`, `ghost`, `destructive`), not appearance (`blue`, `rounded`).

**States**
- Interactive components define default, hover, focus-visible, active, and disabled, plus loading, invalid, and selected or checked where they apply.
- Focus ring via `:focus-visible`, at least 2px thick with ≥3:1 contrast against adjacent colors; never removed without a replacement.
- Use the native `disabled` attribute; switch to `aria-disabled="true"` only when the control must stay focusable, such as a loading button or one that explains why it is unavailable.
- Interactive targets are at least 24×24px, and 44×44px for primary touch controls.

**Accessibility patterns (WAI-ARIA APG)**
- Button: native `button` with `type="button"` unless it submits; icon-only buttons get `aria-label`.
- Dialog: `role="dialog"`, `aria-modal="true"`, `aria-labelledby`; focus moves in on open, Tab stays inside, Escape closes, focus returns to the trigger. Native `dialog` with `showModal()` provides most of this.
- Menu button: trigger has `aria-haspopup="menu"` and `aria-expanded`; arrow keys move between items, Enter or Space activates, Escape closes and returns focus. Only for actions, never for site navigation.
- Tabs: `tablist`, `tab`, `tabpanel`, `aria-selected`, `aria-controls`; one tab in the Tab sequence (roving tabindex), Left and Right arrows move between tabs, Home and End jump to the ends.
- Tooltips show on hover and focus, dismiss with Escape, stay open while hovered, and never hold essential information.

**Tokens**
- No raw hex, px, or ms values inside components; use semantic tokens (`--color-action-primary-bg`, `--radius-control`, `--duration-fast`) from design-tokens.

## Output
- An API table per component: prop, type, default, description.
- Component code in React + Tailwind when the project uses it, otherwise semantic HTML with CSS custom properties and `data-variant` and `data-size` attributes. Use `cva` for variant maps only if it is already installed; plain objects work the same way:

```tsx
import * as React from "react";
// Theme keys (action-primary, surface, focus, danger) map to semantic CSS custom properties.
const base = "inline-flex items-center justify-center gap-2 rounded-control font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 disabled:opacity-50";
const variants = {
  primary: "bg-action-primary text-on-action-primary hover:bg-action-primary-hover",
  secondary: "border border-default bg-surface text-default hover:bg-surface-hover",
  ghost: "text-default hover:bg-surface-hover",
  destructive: "bg-danger text-on-danger hover:bg-danger-hover",
} as const;
const sizes = { sm: "h-8 px-3 text-sm", md: "h-10 px-4 text-sm", lg: "h-12 px-5 text-base" } as const;

type ButtonProps = React.ComponentPropsWithoutRef<"button"> & {
  variant?: keyof typeof variants; size?: keyof typeof sizes; loading?: boolean;
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { variant = "primary", size = "md", loading = false, type = "button", className = "", onClick, ...rest }, ref) {
  return (
    <button ref={ref} type={type} aria-busy={loading || undefined} aria-disabled={loading || undefined}
      onClick={(e) => { if (loading) { e.preventDefault(); return; } onClick?.(e); }}
      className={[base, variants[variant], sizes[size], className].join(" ")} {...rest} />
  );
});
```

- Stories or examples: one per variant, one per state, and a full matrix view; keyboard interaction tests and an axe check where the test setup already exists.

## Avoid
- Boolean prop explosions (`isPrimary`, `isLarge`, `isRounded`, `hasIcon`).
- `div` or `span` with click handlers instead of `button`.
- `outline: none` without a visible `:focus-visible` replacement.
- Hard-coded colors, spacing, and durations that bypass tokens.
- `role="menu"` on navigation links, or ARIA that contradicts native semantics.
- Dialogs that do not trap focus or do not return it on close.
- Components that swallow `className`, `ref`, or `aria-*` props.

## Final check
- [ ] The API uses the library's shared prop names and supports controlled and uncontrolled use where stateful.
- [ ] Every state in the matrix is styled and visible in a story.
- [ ] Keyboard behavior matches the APG pattern and works without a mouse.
- [ ] Focus-visible ring is at least 2px with ≥3:1 contrast; focus is never lost on open or close.
- [ ] Only semantic tokens are used; no raw hex values or magic numbers.
- [ ] `ref`, `className`, and remaining props are forwarded.
