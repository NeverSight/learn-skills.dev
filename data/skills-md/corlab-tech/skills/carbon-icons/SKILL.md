---
name: carbon-icons
description: Carbon Design System icon usage for React components. MANDATORY when any component includes an icon. Use when implementing UI components that need icons, building atoms/molecules/organisms with icon elements, or adding icons to buttons, inputs, navigation, or any other UI element. Covers icon imports, sizing, color, alignment, touch targets, and the V-Shield Design System icon labeling system.
---

# Carbon Icons

Use `@carbon/icons-react` for all icons. Never create inline SVGs or extract icons from Figma.

## Import & Usage

```tsx
import { Search, ChevronDown, Close, View, ViewOff, Information, Add } from '@carbon/icons-react';

<Search size={20} />
<Close size={16} />
```

Icons render as inline SVGs with `currentColor` fill — they inherit the parent's text color.

## Sizing

| Size | Context | Pairs with |
|------|---------|------------|
| `16` | Inputs, badges, compact buttons, inline indicators | `text-body-md` (14px) |
| `20` | Default — buttons, form fields, nav items | `text-body-lg` (16px) |
| `24` | Section headers, cards, medium emphasis | `text-heading-md`–`text-heading-lg` |
| `32` | Hero sections, empty states, pictograms | `text-heading-xl`+ |

Keep icon size consistent within a component. Do not mix sizes arbitrarily.

## Color

- Icons are **monochromatic** — always a single solid color
- Color comes from `currentColor` — set via Tailwind text color on parent or icon
- **Match icon color with adjacent text** — never use a different color for the icon vs its label
- Must pass **4.5:1** contrast ratio (same rule as typography)
- Use semantic tokens: `text-icon`, `text-icon-hover`, `text-icon-disabled`, `text-text`, `text-gray-600`, etc.

```tsx
// ✅ Icon inherits parent color
<span className="text-gray-600 flex items-center gap-1">
  <Search size={16} /> Search
</span>

// ❌ WRONG — icon has different color than text
<span className="text-gray-600">
  <Search size={16} className="text-primary-600" /> Search
</span>
```

## Alignment

- Always **center-align** icons next to text: `items-center`
- Never baseline-align icons to text

```tsx
// ✅ Correct
<div className="flex items-center gap-2">
  <Information size={16} />
  <span>Help text</span>
</div>
```

## Touch Targets

Interactive icons need **minimum 44px** touch target. Add padding if the icon is smaller:

```tsx
<button className="p-3 flex items-center justify-center" aria-label="Close">
  <Close size={16} />
</button>
```

## Icon Types (V-Shield Design System Labeling)

The Figma Design System (node `2377:25170`) labels icons into 3 categories:

1. **"used"** — Standard Carbon icons. Import from `@carbon/icons-react`.
2. **"custom"** — Not in Carbon. Only these may use inline SVG or a custom component.
3. **"both"** — Exists in Carbon but customized. Prefer Carbon version unless customization is essential.

## Finding Icons

Browse: https://carbondesignsystem.com/elements/icons/library/

Import names use PascalCase. Examples:
- `chevron-down` → `ChevronDown`
- `view` / `view-off` → `View` / `ViewOff`
- `close` → `Close`
- `checkmark` → `Checkmark`
- `warning` → `Warning`
- `information` → `Information`
- `add` → `Add`
- `subtract` → `Subtract`
- `edit` → `Edit`
- `trash-can` → `TrashCan`
- `overflow-menu-vertical` → `OverflowMenuVertical`

## Pictograms & Flags

- Large illustrative icons (32px+): use `@carbon/pictograms-react`
- Country flags: custom assets (not in Carbon)

## Rules Summary

1. Always import from `@carbon/icons-react`
2. Never create `<svg>` manually for standard UI icons
3. Never extract SVGs from Figma
4. Use `currentColor` — set color via Tailwind text classes
5. Center-align next to text (`items-center`)
6. 44px minimum touch target for interactive icons
7. Match icon color with adjacent text color
