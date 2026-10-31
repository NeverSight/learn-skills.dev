---
name: component-patterns-code
description: "Production UI component code in React/TypeScript, SwiftUI, and modern CSS with full state matrices, ARIA attributes, keyboard handling, and design token consumption. Use when building or reviewing a button, modal, form, input, table, or any component that needs all of its states covered."
---

# Component Patterns & Code — Production-Ready UI Engineering

## The Component Mindset

"A component is not a visual artifact. It is a state machine with a visual output." Every button, input, modal, and card exists in a matrix of states that must be designed, implemented, and tested. Developers and designers who treat components as static visual elements inevitably ship incomplete interfaces that break under real-world conditions — when the network is slow, when the user tabs instead of clicks, when the content is unexpectedly long, when the screen is 320px wide.

Production-quality component engineering demands three disciplines simultaneously: visual fidelity (the component looks correct across every state), behavioral completeness (the component responds correctly to every interaction), and semantic correctness (the component communicates its purpose and state to all users, including those using assistive technology).

## Component State Matrix Methodology

Every component exists in far more states than the typical design file represents. The State Matrix is a systematic enumeration of every possible visual and behavioral state a component can occupy. Before writing a single line of code, enumerate the full matrix.

### The Universal State Set

These states apply to virtually every interactive component:

1. **Default** — the resting state, no user interaction, content loaded normally
2. **Hover** — pointer device is over the component, visual feedback indicates interactivity
3. **Focus** — the component has keyboard focus, visible focus ring is mandatory (WCAG 2.4.7)
4. **Active/Pressed** — the component is being activated (mousedown, touch start)
5. **Disabled** — the component is non-interactive, visually muted, removed from tab order
6. **Loading** — the component or its content is being fetched, skeleton or spinner is shown
7. **Error** — something went wrong, the error is communicated visually and to screen readers
8. **Success** — an operation completed successfully, confirmation feedback is shown
9. **Skeleton** — content has not yet loaded, a placeholder shape indicates the forthcoming layout
10. **Empty** — no data to display, guidance or action is offered to the user
11. **Read-only** — content is visible but not editable, visually distinct from disabled
12. **Selected** — the component is chosen within a selection group (checkbox checked, row highlighted)
13. **Dragging** — the component is being repositioned, visual affordance communicates movability
14. **Overflow** — content exceeds bounds, truncation or scroll behavior activates

### Compound States

States combine. A text input can be simultaneously focused and in an error state. A button can be loading and disabled. A table row can be selected and hovered. Your component API must handle compound states gracefully without combinatorial explosion. The recommended pattern is to model each state dimension independently:

- **Interaction state:** default, hover, focus, active (mutually exclusive for pointer, but focus persists alongside hover)
- **Validation state:** none, error, warning, success (one at a time)
- **Content state:** loaded, loading, skeleton, empty, error (one at a time)
- **Selection state:** selected, unselected
- **Availability state:** enabled, disabled, read-only

This dimensional model yields a manageable API surface rather than an unwieldy union of every possible combination.

### State Matrix Audit Checklist

Before any component ships:

- Are all 14 universal states accounted for in design and code?
- Do compound states resolve without visual conflicts?
- Is every state transition animated appropriately (not jarring, not distracting)?
- Does every state have a screen reader equivalent (aria-busy, aria-invalid, aria-disabled, aria-selected)?
- Has every state been tested on mobile (touch) and desktop (pointer + keyboard)?

## Component Taxonomy

Organizing components into functional categories creates a shared vocabulary for the team and ensures coverage. The taxonomy below covers the foundational set that virtually every product needs.

### Action Components

Components that trigger operations. The user clicks, taps, or activates them to cause something to happen.

- **Button** — the primary action trigger; variants include primary, secondary, ghost, danger, icon-only
- **IconButton** — a button with only an icon and an accessible label; used where space is constrained
- **FAB (Floating Action Button)** — a persistent action button layered over content, common on mobile
- **SegmentedControl** — a group of buttons where exactly one is selected, acting as a toggle between views

### Input Components

Components that accept user data.

- **TextField** — single-line text entry with optional label, helper text, validation, and character count
- **TextArea** — multi-line text entry with auto-resize and character limit
- **Select** — a dropdown menu for choosing one option from a predefined list
- **Combobox** — a searchable select that combines text input with option filtering
- **Checkbox** — a binary or indeterminate toggle for non-exclusive options
- **RadioGroup** — a set of mutually exclusive options
- **Toggle/Switch** — an on/off binary control with immediate effect
- **Slider** — a draggable track for selecting a numeric value within a range
- **DatePicker** — a calendar-based date selection with keyboard support

### Feedback Components

Components that communicate status, results, or system state to the user.

- **Toast/Snackbar** — a temporary, non-blocking notification that auto-dismisses
- **Banner** — a persistent message pinned to a region of the interface
- **Dialog/Modal** — a focused overlay requiring user attention and response
- **ProgressBar** — a visual indicator of completion percentage for a known-duration operation
- **Skeleton** — a placeholder shape indicating content is loading

### Navigation Components

Components that move the user between views, sections, or pages.

- **Tabs** — horizontal or vertical tab strips for switching between panels of content
- **Breadcrumb** — a hierarchical trail showing the user's location within a navigation structure
- **Sidebar/Drawer** — a vertical navigation panel, collapsible on smaller screens
- **Pagination** — page controls for navigating multi-page data sets
- **BottomNav** — a mobile navigation bar anchored to the screen bottom

### Content Components

Components that present or contain information.

- **Card** — a bounded container for a cohesive unit of content and related actions
- **Avatar** — a circular or rounded image representing a user, entity, or placeholder
- **Badge** — a small indicator attached to another element showing count or status
- **Chip/Tag** — a compact element representing an attribute, filter, or selection
- **Tooltip** — a small overlay providing supplementary text on hover or focus
- **Accordion** — a vertically stacked set of collapsible sections

### Data Components

Components optimized for displaying structured datasets.

- **Table** — a two-dimensional grid of rows and columns with sortable headers, pagination, and row selection
- **List** — a vertical sequence of related items with optional actions
- **Grid** — a responsive multi-column layout of repeated content items
- **Chart** — a visual representation of data (bar, line, pie, scatter)

## Design Token Integration

Every component must consume design tokens rather than hardcoded values. Tokens are the contract between design and code. They ensure that when the design system changes a color, spacing value, or font, every component updates automatically.

### Token Categories in Components

- **Color tokens:** `--color-primary`, `--color-surface`, `--color-on-surface`, `--color-error`, `--color-border`
- **Spacing tokens:** `--space-xs`, `--space-sm`, `--space-md`, `--space-lg`, `--space-xl`
- **Typography tokens:** `--font-family-body`, `--font-size-sm`, `--line-height-normal`, `--font-weight-medium`
- **Radius tokens:** `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-full`
- **Shadow tokens:** `--shadow-sm`, `--shadow-md`, `--shadow-lg`
- **Motion tokens:** `--duration-fast`, `--duration-normal`, `--easing-standard`, `--easing-decelerate`
- **Size tokens:** `--size-touch-target` (44px minimum), `--size-icon-sm`, `--size-icon-md`

### Token Usage Rules

1. Never use raw hex colors, pixel values, or font stacks in component CSS.
2. Component-level tokens alias global tokens: `--button-bg: var(--color-primary)`.
3. State variations reference the token system: `--button-bg-hover: var(--color-primary-hover)`.
4. Dark mode is a token swap, not a component rewrite.
5. Token overrides via CSS custom properties enable theming without code changes.

## Accessibility-First Component Engineering

Accessibility is not an enhancement. It is a baseline requirement. Components built with accessibility from the start are cheaper to maintain, more robust, and usable by everyone.

### Keyboard Navigation

- Every interactive component must be reachable via Tab key.
- Custom widgets must implement the expected keyboard pattern from WAI-ARIA Authoring Practices: arrow keys for menus, tabs, and radio groups; Enter/Space for activation; Escape for dismissal.
- Focus order must match the visual order. If CSS reorders elements visually, ensure `tabindex` or DOM order reflects the intended sequence.
- Focus must never become trapped (except intentionally in modals, where a focus trap is required).
- The visible focus indicator must meet 3:1 contrast and should not rely solely on browser defaults.

### ARIA Roles and States

- Use semantic HTML first (`<button>`, `<input>`, `<dialog>`, `<nav>`). ARIA is a supplement, not a replacement.
- Dynamic state changes require ARIA state updates: `aria-expanded`, `aria-selected`, `aria-checked`, `aria-busy`, `aria-invalid`, `aria-disabled`.
- Live regions (`aria-live="polite"` or `aria-live="assertive"`) announce dynamic content changes (toast notifications, form validation messages, loading completions).
- Every icon-only button requires `aria-label`. Every image requires `alt` text or `aria-hidden="true"` if decorative.

### Screen Reader Announcements

- Toast notifications must use `role="status"` or `aria-live="polite"` so screen readers announce them without interrupting the current task.
- Error messages should be linked to their inputs via `aria-describedby`.
- Loading states should use `aria-busy="true"` on the loading region.
- Route changes in SPAs should announce the new page title via a live region or focus management.

## Responsive Component Patterns

### Container Queries Over Media Queries

Media queries respond to the viewport. Container queries respond to the component's container. Since components are reused in different layout contexts (sidebar, main content, modal), container queries produce correct results where media queries fail.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { flex-direction: row; }
}

@container card (max-width: 399px) {
  .card { flex-direction: column; }
}
```

### Fluid Sizing

Use `clamp()` for typography and spacing that scales smoothly between breakpoints without abrupt jumps:

```css
font-size: clamp(1rem, 0.5rem + 1.5vw, 1.5rem);
padding: clamp(0.75rem, 2vw, 2rem);
```

### Touch Target Minimums

Per WCAG 2.5.8 (Target Size), interactive elements must be at least 24x24 CSS pixels, with a recommendation of 44x44 pixels. Apple HIG specifies 44pt minimum. Material Design specifies 48dp. Always err on the side of larger targets on touch devices.

This is directly informed by Fitts's Law (see `cognitive-psychology-ux`): the time to reach a target is a function of distance and target size. Smaller targets increase error rates and frustration, especially under mobile conditions (one-handed use, walking, glare).

## Routing

For **React** — the `cn()` utility, then Button, TextInput, Select, Dialog,
Toast, Card, Badge, Avatar and the rest as complete CVA + Tailwind + Radix
implementations with every state and full ARIA: read
`references/react-component-cookbook.md`.

For **SwiftUI** — the EnvironmentKey-based theme system, then PrimaryButton,
ValidatedTextField, AdaptiveSheet, SwipeableListRow, AdaptiveNavigationStack,
DynamicForm, BadgedTabView and CachedAsyncImage: read
`references/swiftui-component-cookbook.md`.

For **modern CSS** — container queries, `:has()`, subgrid, `@layer`, and the
patterns that replace what used to need JavaScript: read
`references/css-modern-patterns.md`.

## Cross-References

- **Cognitive psychology foundations** — `cognitive-psychology-ux` covers Fitts's Law (touch target sizing), Hick's Law (reducing choice overload in selects and menus), Miller's Law (chunking in data tables and forms), and the gestalt principles that inform component grouping and layout.
- **Accessibility compliance** — `accessibility-inclusive-design` provides the full WCAG 2.2 checklist, assistive technology testing procedures, and inclusive design patterns that component code must satisfy.
- **Design token architecture** — `ui-visual-design-system` details the token naming conventions, scale generation, and semantic mapping that components consume.
- **Animation and interaction** — `interaction-motion-design` covers easing curves, duration scales, reduced-motion handling, and spring physics that component transitions use.
- **Design-to-code workflow** — `figma-design-tool-workflows` describes how component designs in Figma translate to code, including auto-layout to flexbox mapping, variant properties to component props, and design token export.
- **System governance** — `design-systems-architecture` explains how components are documented, versioned, tested, and distributed across teams.

## Key Sources

- WAI-ARIA Authoring Practices 1.2 — W3C component keyboard and ARIA patterns
- Inclusive Components — Heydon Pickering (component accessibility patterns)
- Material Design 3 Component Guidelines — Google
- Apple Human Interface Guidelines — Components
- React Aria (Adobe) — accessible React component primitives
- Radix UI — unstyled, accessible component primitives
- Open UI — web platform component standards research
