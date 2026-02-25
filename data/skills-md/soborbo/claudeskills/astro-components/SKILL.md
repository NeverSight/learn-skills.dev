---
name: astro-components
description: UI component library for Astro lead generation sites. Buttons, forms, cards, badges. Requires design-tokens skill.
---

# Astro Components Skill

## Purpose

Provides reusable UI components. Does NOT handle sections, layouts, or business logic.

## Scope

| ✅ Use For | ❌ NOT For |
|-----------|-----------|
| Marketing sites | Web apps |
| Lead gen pages | Dashboards |
| Service websites | E-commerce carts |

## Core Rules

1. **All styling via design-tokens** — No hardcoded colors/spacing
2. **Token missing = build error** — Never fallback to arbitrary values
3. **Mobile-first** — Base styles for mobile, `md:` for larger
4. **44px minimum touch targets** — All interactive elements
5. **Zero external dependencies** — Pure Astro + Tailwind only

## Semantic HTML Rules

| Element | Use | Never |
|---------|-----|-------|
| `<button>` | Actions, toggles | `<div onclick>` |
| `<a>` | Navigation | `<span onclick>` |
| `<input>` | Form data | Contenteditable div |

**Rule:** If it does something → `<button>`. If it goes somewhere → `<a>`.

## Component Variants

**Fixed variants only.** Claude cannot invent new variants.

| Component | Allowed Variants |
|-----------|-----------------|
| Button | `primary`, `secondary`, `outline`, `ghost` |
| Card | `default`, `elevated`, `outlined` |
| Badge | `default`, `success`, `warning`, `error`, `info` |
| Alert | `info`, `success`, `warning`, `error` |

**New variant needed?** → Update this skill first, then use.

## Props Pattern (All Components)

```typescript
interface Props {
  variant?: 'primary' | 'secondary';  // Explicit union, no string
  size?: 'sm' | 'md' | 'lg';          // Fixed sizes only
  class?: string;                      // Allow extension
  // ... component-specific
}

const { variant = 'primary', size = 'md' } = Astro.props;
```

## JavaScript Rules

| Allowed | Forbidden |
|---------|-----------|
| `client:visible` islands | Inline `onclick` |
| Astro actions | `<script>` in component |
| Separate `.ts` files | Any DOM manipulation |

**Exception:** None. If JS needed, use island architecture.

## Icon Handling

```typescript
// If icon name not found → render nothing + console.warn
const path = icons[name];
if (!path) {
  console.warn(`Icon "${name}" not found`);
  return null;
}
```

**No silent failures.** Missing icon = visible warning in dev.

## Form Components

| Rule | Requirement |
|------|-------------|
| Label | Always visible, linked via `for` |
| Placeholder | Hint only, never replaces label |
| Error | Below input, `role="alert"` |
| Required | Visual indicator (`*`) + `required` attr |

## Component Boundaries

Components must NOT:
- Fetch data
- Format/transform data
- Access global state
- Import other components (except Icon)
- Contain business logic

**Rule:** Component receives props → renders UI. Nothing else.

## File Structure

```
src/components/ui/
├── Button.astro
├── Input.astro
├── Card.astro
├── Badge.astro
├── Alert.astro
├── Icon.astro
└── index.ts
```

## Forbidden

- ❌ External UI libraries
- ❌ Hardcoded colors/spacing
- ❌ Touch targets under 44px
- ❌ Missing focus states
- ❌ Inline JavaScript
- ❌ Inventing new variants
- ❌ Silent failures

## References

- [button.md](references/button.md) — Button component code
- [input.md](references/input.md) — Input component code
- [card.md](references/card.md) — Card component code
- [icon.md](references/icon.md) — Icon component + full icon list

## Definition of Done

- [ ] Uses design-tokens only
- [ ] All interactive: focus states + 44px touch
- [ ] TypeScript Props interface
- [ ] No inline JavaScript
- [ ] Tested on mobile 375px
