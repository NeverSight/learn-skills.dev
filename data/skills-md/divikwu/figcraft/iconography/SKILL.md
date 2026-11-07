---
name: iconography
description: "Icon rules: ordering in auto-layout (children array order = visual order), tool chain (icon_search -> icon_create with index), sizing, spacing, style consistency. Use when: icon/icons + create/place/add/order/position/wrong/layout, or when icons appear in wrong position."
---

# Iconography

## Skill Boundaries

- Use this skill for **icon placement, ordering, sizing, and tool chain** (`icon_search` → `icon_create`).
- General icon design rules (single set, no text placeholders) are in [ui-ux-fundamentals](../ui-ux-fundamentals/SKILL.md).
- Library-specific icon discovery (search_design_system for icon components) is handled by [design-guardian](../design-guardian/SKILL.md) workflow.

## Ordering — children order = visual order (CRITICAL)

In auto-layout, the children array index directly controls visual position:
- **Index 0** = leftmost (HORIZONTAL) / topmost (VERTICAL)
- **Last index** = rightmost / bottommost

`icon_create` with `parentId` **appends to END** by default. Use `index` to control position:
- `index: 0` — icon appears FIRST (left of text in HORIZONTAL)
- Omit index — icon appears LAST (right of text)

### Common Patterns

| UI Pattern | Correct children order | icon_create index |
|------------|----------------------|-------------------|
| Search input | [search-icon, text-input] | `index: 0` |
| Password input | [lock-icon, text-input, eye-icon] | lock: `index: 0`, eye: omit |
| Nav menu item | [icon, label, chevron-right] | icon: `index: 0`, chevron: omit |
| Button with leading icon | [icon, label] | `index: 0` |
| Button with trailing icon | [label, icon] | omit (default append) |
| Settings row | [icon, label, toggle/chevron] | icon: `index: 0` |
| List item | [thumbnail, content, trailing-action] | thumbnail: `index: 0` |
| Tab bar item | [icon, label] (VERTICAL) | `index: 0` |
| Notification badge | [bell-icon, red-dot] | bell: `index: 0` |
| Back navigation | [arrow-left, title] | `index: 0` |

### Inline Children vs icon_create

Two approaches for placing icons in create_frame:

1. **Inline children** (preferred for structured layouts): Include icon as a `type: "frame"` placeholder in the children array at the correct position, then use `icon_create(parentId: "<placeholder-id>")` to fill it. Array position controls visual order directly.

2. **Post-creation icon_create** (simpler): Create the frame first, then call `icon_create(parentId: "<frame-id>", index: 0)` to insert at the correct position.

Note: `create_frame` children `type: "svg"` requires raw SVG markup string, NOT icon names like "lucide:home". Use `icon_create` for named icons.

## Tool Chain

### Library Mode (Design Guardian)
1. `search_design_system(query: "icon chevron")` — find library icon components
2. If found: use `type: "instance"` in children or component insert
3. If not found: fall back to Iconify flow below

### No-Library Mode (Design Creator)
1. `icon_search(query: "search", prefix: "lucide")` — find icon name
2. `icon_create(icon: "lucide:search", parentId: "...", index: 0, size: 20)` — create + place

### Key Constraints
- `icon_create` accepts icon name ("prefix:name") — fetches SVG automatically
- `create_frame` children `type: "svg"` requires raw SVG markup, NOT icon name
- These are different mechanisms — don't mix them

## Sizing

| Context | Icon Size | itemSpacing to text | Notes |
|---------|----------|--------------------|----|
| Inline (body text) | 16px | 4-6px | Match text line height |
| Input field | 20px | 8px | Vertically centered |
| Navigation / toolbar | 24px | 8-12px | Default icon_create size |
| Button with icon | 20px | 8px | Match button text size |
| Feature / empty state | 32-64px | 12-16px | Prominent, muted color |
| Tab bar | 24px | 4px | Above label (VERTICAL layout) |
| Avatar placeholder | 40-80px | — | Inside circular frame |

## Alignment

- Parent frame needs `counterAxisAlignItems: "CENTER"` to vertically center icon with text
- Icon containers: use `type: "frame"` with `layoutMode`, `primaryAxisAlignItems: "CENTER"`, `counterAxisAlignItems: "CENTER"`
- Touch targets: icon buttons need minimum 44x44px tap area — add padding to reach 44x44 even if icon is 24px

## Color

- Use `colorVariableName` in `icon_create` to bind icon color to design token
- `icon_create` auto-detects fill vs stroke icons and binds accordingly
- Without binding, icon won't respond to theme changes (light/dark mode)

## Style Consistency

- Single icon set per design (all `lucide:`, or all `mdi:`, etc.) — never mix sets
- Single style: outline, filled, or duotone — never mix styles
- Icon stroke weight should match typography weight (light type -> thin icons)
- NEVER use decorative icons without functional meaning

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Icon placed after text (wrong order) | Use `icon_create` with `index: 0` for leading icons |
| Text as icon (">" for chevron, "..." for more) | Runtime detection warns; use `icon_create` instead |
| Rectangle as icon container | Use `type: "frame"` — rectangles can't have children |
| Forgot icon entirely (search bar without search icon) | Plan ALL icons before create_frame |
| Icon name in SVG child | `type: "svg"` needs raw SVG markup; use `icon_create` for named icons |
| Icon too small / too large | Follow sizing table above per context |
| No color binding | Pass `colorVariableName` when design system has tokens |
| Mixed icon sets (lucide + mdi) | Pick one prefix and use it consistently |
| Mixed icon styles (outline + filled) | Choose one style for the entire design |
| Touch target too small | Icon buttons need 44x44px minimum via padding |
| Icon-text vertical misalignment | Set `counterAxisAlignItems: "CENTER"` on parent |
| Icon spacing inconsistent | Use sizing table itemSpacing values per context |
