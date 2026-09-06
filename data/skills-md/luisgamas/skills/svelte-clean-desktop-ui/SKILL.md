---
name: svelte-clean-desktop-ui
description: Token-driven clean desktop UI/UX system for redesigning or creating Svelte 5 application interfaces with shadcn-svelte, Bits UI, Tailwind v4, and lucide icons. Use for desktop app visual systems, component styling, shell layouts, sidebars, settings screens, cards, menus, tabs, forms, dialogs, terminal/editor panes, compact density, neutral surface layering, Geist (humanist variable sans) typography, softened hairlines, and making an interface feel polished, modern, precise, soft, and less robotic without changing UI libraries.
---

# Svelte Clean Desktop UI

## Purpose

Use this skill to create a clean, professional desktop application interface while preserving a Svelte 5 stack built on Tailwind v4, shadcn-svelte, Bits UI, and lucide icons.

Do not change UI libraries just to improve visual quality. The target style is achieved through design tokens, component recipes, density rules, semantic surfaces, state behavior, and typography.

## First Reads

Load only the references needed for the task:

- For global visual direction and feasibility: read `references/visual-direction.md`.
- For tokens, spacing, typography, color, elevation, and motion: read `references/core-style-system.md`.
- For Svelte component implementation patterns: read `references/svelte-component-patterns.md`.
- For screens such as sidebars, settings, worktree cards, terminal/editor shells: read `references/screen-patterns.md`.
- For migration sequencing and acceptance checks: read `references/migration-and-validation.md`.

Reusable starter assets:

- `assets/desktop-clean-tokens.css`: CSS variable layer to adapt an app-level stylesheet.
- `assets/desktop-clean-design.ts`: role-based design token module for Svelte components.
- `assets/component-class-recipes.yaml`: compact class recipes for common primitives.

## Core Workflow

1. Inspect the target Svelte files before editing. Prefer existing UI primitives and local token modules before adding new abstractions.
2. Identify the UI role: shell, sidebar, list row, card, settings section, toolbar, menu, form, dialog, editor, terminal, or status area.
3. Apply the style system by role, not by decoration. The clean look comes from hierarchy, density, and state behavior.
4. Keep Svelte components idiomatic. Use snippets, `$props`, `$derived`, `cn`, `tailwind-variants`, Bits UI wrappers, and lucide icons where the project already uses them.
5. Prefer token changes when many components share the issue. Use local classes only when a component has a unique layout responsibility.
6. Verify desktop widths and narrow panel states. Check text truncation, hover/focus/active states, sidebar resizing, scrollbars, dialogs/popovers, and dark mode.

## Visual Direction

Aim for this result:

- calm neutral canvas with small luminance differences between background, sidebars, cards, and active rows;
- strong information hierarchy without oversized type;
- dense but breathable rows, using 6-12px internal spacing and consistent line-height;
- active/hover states that feel tactile but not loud;
- borders that separate only where necessary, usually `border-border/50` or foreground-mixed equivalents;
- rounded corners mostly `6px` to `10px`, with `12px` reserved for larger settings/content surfaces;
- icons as functional controls, usually 12-16px, with stroke weight and opacity adjusted by state;
- menus, popovers, and dialogs that feel like desktop tools: compact, aligned, with clear focus rings;
- Geist (Geist Variable, weight range 100-900) for primary UI text — a humanist, low-contrast variable sans that renders light and soft at dense UI sizes — with a strong monospace stack for code and terminal surfaces.

The single biggest lever for a soft, light, non-robotic texture is the **typeface**: prefer a humanist low-contrast variable sans (Geist) over a rigid geometric one (DM Sans, Poppins, Montserrat). Geometric faces have uniform strokes and round, tightly-spaced bowls that read heavy and "mechanical" at 12-13px; a humanist face opens the rhythm and lightens the texture. Pair it with grayscale font-smoothing and a touch of tracking (see `references/core-style-system.md`).

Avoid:

- heavy primary tint across large cards;
- nested card stacks;
- one-hue themed UI;
- thick dividers and resize handles that read louder than content;
- body text below 12px for meaningful reading;
- uppercase labels except short section headers or tiny badges;
- visible explanatory copy that describes UI mechanics instead of helping the workflow.

## Implementation Rules

### Tokens First

Before touching many components, update the token layer:

- app stylesheet: global colors, font family, scrollbar classes, theme variables.
- design token module: role-based class strings for text, icon, surfaces, rows, controls, panels.
- UI primitives: button, card, input, select, tabs, dropdown-menu, dialog, popover, badge.

### Svelte Component Rules

- Keep components accessible: preserve labels, `aria-*`, keyboard behavior, focus-visible rings, disabled states.
- Use `cn(...)` for conditional classes and keep state classes close to the element they affect.
- Use lucide icons in icon buttons, with `title` or tooltip for ambiguous actions.
- Keep stable dimensions on rows and controls: explicit `h-*`, `size-*`, `min-w-0`, `truncate`, and predictable gaps.
- Use hover-reveal only for secondary actions; make primary actions visible.

### Desktop Layout Rules

- Reserve the main canvas for work. Avoid marketing-page spacing.
- Sidebars should feel like navigation surfaces, not card galleries.
- Settings screens should use a two-column app-shell pattern with a focused content pane and section surfaces.
- Terminal/editor panes should prioritize contrast, scroll performance, and predictable chrome.

## Decision Guide

Use these quick choices:

- If a component feels robotic or noisy: in order of impact — (1) switch the UI face to a humanist variable sans (Geist) if it isn't already; (2) soften every structural hairline to `border-border/50`-`/60` or a `color-mix` border instead of full-strength `border-border`; (3) lower chrome-text contrast (muted/60 instead of full foreground); (4) remove redundant dividers; (5) soften surface contrast and add precise hover/focus states.
- If a component feels cramped: add vertical rhythm by grouping rows, not by inflating every control.
- If a component feels empty: improve alignment, surface layering, and metadata placement before adding decoration.
- If a component lacks polish: check font, sidebar surface variables, hover opacity, rounded corners, and active-state strength first.
- If Radix-like polish is requested: map to Bits UI/shadcn-svelte primitive behavior; do not introduce React-only primitives into a Svelte app.

## Validation Checklist

Before finishing UI work:

- Run the project's typecheck command when code changed.
- Run relevant tests if behavior changed.
- Start the dev server for visual work and inspect the actual UI when feasible.
- Confirm light and dark modes.
- Confirm no text overflow in sidebars, cards, buttons, nav rows, select triggers, tabs, and dialog headers.
- Confirm hover, active, disabled, focus-visible, expanded, selected, and loading states.
- Confirm panels can resize without breaking row layout.
