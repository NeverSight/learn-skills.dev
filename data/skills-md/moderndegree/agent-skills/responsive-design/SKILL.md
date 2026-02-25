---
name: responsive-design
description: Mobile-first responsive design, breakpoints, touch targets, and adaptive layouts. Use when building layouts, creating responsive components, or optimizing for mobile.
version: 1.0.0
---

# Responsive Design

This skill covers responsive design principles — mobile-first development, appropriate breakpoints, touch-friendly targets, and adaptive layout patterns.

## Use-When

This skill activates when:
- Agent builds page layouts or components
- Agent adds responsive breakpoints
- Agent designs for mobile devices
- Agent creates touch-friendly interactions
- Agent converts desktop-only designs to responsive

## Core Rules

- ALWAYS use mobile-first approach (base styles for mobile, media queries for larger)
- ALWAYS ensure touch targets are at least 44x44px
- ALWAYS design for smallest screen first, then enhance
- NEVER rely solely on device detection (use feature detection)
- ALWAYS test at actual breakpoints, not just resize the browser

## Common Agent Mistakes

- Desktop-first approach leading to mobile afterthought
- Touch targets too small (buttons, links under 44px)
- Fixed widths that break on smaller screens
- Not considering landscape orientation on mobile
- Hiding content instead of adapting it

## Examples

### ✅ Correct

```tsx
// Mobile-first: base styles for mobile, enhance for larger
<div className="w-full md:w-1/2 lg:w-1/3">
  <Button className="w-full md:w-auto h-11">
    Submit
  </Button>
</div>

// Touch-friendly targets (min 44px)
<button className="min-h-[44px] min-w-[44px] px-4 py-3">
  Tap Here
</button>
```

### ❌ Wrong

```tsx
// Desktop-first
<div className="w-1/2">
  <button className="p-1">Click</button>
</div>

// Touch target too small
<button className="p-2 text-sm">
  Too small
</button>
```

## References

- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox)
- [Google Mobile-Friendly](https://developers.google.com/web/fundamentals/design-and-ux/responsive)
- [Apple Human Interface Guidelines - Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
