---
name: linear-design
description: Build and audit Linear/Vercel/Notion-quality UI. Covers color systems, motion, progressive disclosure, keyboard-first design, layout architecture, surface elevation, information density, micro-interactions, and state handling. Use when building UI components, reviewing design quality, creating pages, or when the user asks for a design review.
---

# Linear-Quality Design System

Build UI with the craft of Linear, Vercel, and Resend. Great UI is restraint, not addition.
The best details are invisible — felt, not seen.

## Color System

Design a **derived color system**, not a palette of hardcoded values.

- Define 3 foundation variables: **base color**, **accent color**, **contrast level**.
- Derive all surfaces, text, icons, borders from these via opacity operations.
- Use perceptually uniform color space (LCH/OKLCH) so colors at same lightness look equally light.
- Hierarchy through **opacity and weight**, not hue. Monochrome-first.
- Color ONLY for semantic meaning: error (red), success (green), active/selected, brand accent.
- No decorative color. No habitual colored icons — make them `muted-foreground`.
- Limit brand color leakage into chrome. The frame should feel neutral and timeless.
- No hardcoded hex anywhere. CSS variables / design tokens only.

## Surface & Elevation

Layer surfaces with subtle background shifts, not heavy shadows.

- Define clear elevation hierarchy: `background` → `card/raised` → `popover` → `dialog/modal`.
- Each level is a slight shade shift (via opacity on base), not a different color.
- **Dark mode**: shadows become subtle borders or glows. Replace `shadow-md` with `border border-border/50`.
- **Borders**: semi-transparent at low opacity (`border-border/40`), never solid opaque lines.
- **Backdrop blur** on floating elements: `backdrop-blur-sm` on overlays, popovers, command palette.
- Support high-contrast mode via the contrast variable — accessibility built into the system.
- `-webkit-font-smoothing: antialiased` globally.

## Motion & Animation

Motion is ~30% of why premium UI feels premium. `transition-colors duration-150` is the floor.

- **Micro-transitions**: color/opacity changes use `duration-150 ease-out`.
- **Layout transitions**: panels, drawers, sidebars use `duration-200 ease-in-out`.
- **Entrances**: modals/dialogs use spring-based easing — slight overshoot, then settle.
  Framer Motion: `type: "spring", stiffness: 400, damping: 30`. CSS: `cubic-bezier(0.34, 1.56, 0.64, 1)`.
- **List stagger**: items entering a list animate in with 30-50ms stagger between each.
- **Skeleton shimmer**: animated gradient sweep matching content shape, not a static gray box.
- **Toasts**: slide in from consistent anchor (bottom-right), slide out on dismiss.
- **Number animations**: counters animate between values, don't jump.
- **Exit animations**: elements leaving should animate out (opacity + slight translate), not vanish.
- Never add artificial delays. Motion should feel instant-but-smooth, not slow.

## Layout Architecture

The structural patterns that make an app feel like a tool, not a website.

- **Three-column layout**: collapsible sidebar (240-280px) + main content + optional detail panel.
- **Resizable panels**: drag handles between columns. Show handle on hover, store width preference.
- **Sticky headers**: compress or transform on scroll. Never duplicate content in header and body.
- **Sheet/drawer vs modal**: use sheets for contextual detail (stays in flow), modals for focused tasks
  (blocks flow). Sheets slide from right, modals center with backdrop.
- **Command palette**: `Cmd+K` overlay that floats above layout. Fuzzy search, categorized results,
  recent items, keyboard-navigable. This is primary navigation for power users.
- **Split views**: side-by-side content for comparison or detail-alongside-list.

## Keyboard-First Design

A Linear-quality app is faster with keyboard than mouse.

- **Command palette** (`Cmd+K`): search commands, navigate, execute actions. Must exist.
- **Single-key shortcuts**: `C` to create, `S` for status, etc. Show in tooltips and context menus.
- **List navigation**: `j/k` or arrow keys to move through items, `Enter` to open.
- **Multi-select**: `Shift+Click` range select, `Cmd+Click` toggle individual.
- **Focus management**: after dialog close, focus returns to trigger. After create, focus new item.
- **Shortcuts in UI**: display keyboard shortcut hints in tooltips, context menus, and command palette
  results. This teaches users the shortcuts naturally.
- **Escape to dismiss**: every overlay, modal, popover, command palette closes on `Escape`.

## Progressive Disclosure

Resting state is minimal. Complexity reveals on interaction.

- **Row actions**: edit, delete, options menu — visible only on row `:hover`.
- **Metadata**: timestamps, secondary badges — shown on hover where non-essential at rest.
- **Toolbars**: bulk action bars appear on selection, not permanently.
- **Contextual menus**: right-click surfaces full action set. Include keyboard shortcuts in menu items.
- **Sub-menu safe areas**: triangle hit area between cursor and sub-menu so diagonal mouse movement
  doesn't close the menu (the Linear pattern — ~40 lines of code, invisible to user, felt as smoothness).
- If it's not primary content or primary action, it should not be visible at rest.

## Information Density

Dense yet clean. Chrome is sparse, content is dense.

- **Tight line-heights** in lists and tables (1.25-1.4, not Tailwind default 1.5).
- **Compact inline metadata**: status dot + avatar + priority icon + label, all in one row.
- **Tabular numbers**: `font-variant-numeric: tabular-nums` on all number columns so digits align.
- **Monospace**: IDs, branch names, code, technical strings in `font-mono text-xs`.
- **Right-align numbers** in table columns.
- **Density trade-off**: reduce chrome spacing (sidebar padding, header height) to give content room.
  Content area can be dense; navigation frame stays spacious.

## Buttons & Actions

- AT MOST one `variant="default"` (primary) button per page/modal/card.
- All other actions: secondary, outline, or ghost — pick by visual weight.
- Destructive: `variant="destructive"` + confirmation dialog before execution.
- Consistent button height per context. Never mix sizes in the same view.
- Cursor `pointer` on everything clickable.

## Interactivity & Micro-interactions

- Every clickable element: distinct `hover:` state (color/opacity) + `active:` state (pressed).
- No bare `<div onClick>` without visual hover feedback.
- Focusable elements: `focus-visible:ring-2 ring-ring`.
- **Drag handles**: appear on hover, hidden at rest.
- **Copy-to-clipboard**: brief "Copied!" feedback (tooltip or inline text swap, 1.5s).
- **Optimistic updates**: UI changes instantly on action, server catches up async.
- **Smart menu positioning**: menus stay in viewport, flip direction when near edges.
- **Input debounce**: search/filter inputs debounce 200-300ms, show subtle loading indicator.

## Typography

- Each view: one dominant heading, one focal point. No competing visual weights.
- Chrome recedes, content advances — high-contrast text against quieter frame.
- Design system tokens only. No arbitrary font sizes or weights.
- **Display font for headings** (e.g. Inter Display, Geist) for expression. Regular weight for body.
- **Letter-spacing**: slightly tighter on large headings (`tracking-tight`), default on body.

## Truncation

- Single-line: `truncate` + `min-w-0` on flex parent and span.
- Multi-line: `line-clamp-{n}` with deliberate max.
- Text never overflows. Every string is bounded. Never `break-all`.

## States

- **Loading**: `<Skeleton>` matching real layout shape + shimmer animation. Never spinner in content.
- **Empty**: title + one-line description + single CTA. Never blank.
- **Error**: human-readable message + what to do next.
- **Disabled**: `opacity-50 cursor-not-allowed`. Never remove the element.

## Tables & Data Display

- Full row highlight on hover (subtle background change).
- Right-aligned numbers, left-aligned text.
- Sortable columns with subtle indicator (chevron icon).
- Horizontally scrollable with frozen first column on overflow.
- Row actions on hover (progressive disclosure).
- Alternating row backgrounds at very low opacity (optional, `even:bg-muted/30`).

## Components

- shadcn/ui only. Never reimplement Dialog, Tooltip, Dropdown, Select, Tabs, Badge, Card, Skeleton.
- Lucide icons only. No emojis. No decorative AI icons (sparkles, wands, stars).
- Icon-only buttons: MUST wrap in `<Tooltip>` with short label. No exceptions.
- Consistent icon size per density (16px dense, 18-20px standard). Don't mix arbitrarily.
- Consistent border radius throughout — never deviate from system radius.

## Spacing

- 4px base scale. No arbitrary values (`mt-[13px]` is a violation).
- No orphaned elements. Everything on a layout grid.
- Remove borders/dividers replaceable by spacing alone.
- Generous whitespace — empty space IS the design.

## Polish

- No `console.log` in UI components.
- No `z-[9999]` — use defined z-index scale.
- No `!important` overrides.
- No hardcoded colors — all through CSS variables.
- `Escape` closes every overlay.
- URL updates on tab/section change for shareability.
- Responsive: sidebar collapses to icon-only or drawer on mobile. Panels stack vertically.

## Audit Output Format

For each issue:
1. File path + line
2. What's wrong (one sentence)
3. The fix

Group by: **Color/Surface** → **Motion** → **Layout** → **Keyboard** → **Progressive Disclosure** →
**Density** → **Interactivity** → **Typography** → **States** → **Tables** → **Polish**

Rank: broken interactions > missing keyboard support > missing states > motion gaps > visual inconsistency > polish.

End with: what still needs human design judgment that code alone cannot fix.
