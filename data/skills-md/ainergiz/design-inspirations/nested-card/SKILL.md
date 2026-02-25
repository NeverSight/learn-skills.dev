---
name: nested-card
description: Creates cards with an outer gradient container and inner content card. Use when building premium card designs with depth, layered card layouts, or cards with image sections and content sections.
---

# Nested Card Pattern

Build premium card designs with an outer gradient container wrapping an inner content card, creating visual depth and separation between media and content areas.

## Structure Overview

```
┌─────────────────────────────┐  ← Outer card (gradient bg, padding)
│  ┌───────────────────────┐  │
│  │      Image/Media      │  │  ← Media section (rounded)
│  └───────────────────────┘  │
│  ┌───────────────────────┐  │
│  │      Content Card     │  │  ← Inner card (solid bg)
│  └───────────────────────┘  │
└─────────────────────────────┘
```

## Core Implementation

### Light Mode

```tsx
<div className="bg-gradient-to-b from-[#e8e8ea] to-[#dcdce0] rounded-3xl p-2 shadow-xl shadow-zinc-400/30 border border-white/60">
  {/* Media section */}
  <div className="relative h-[240px] w-full rounded-2xl overflow-hidden mb-2 border border-white/40">
    {/* Image, carousel, or media content */}
  </div>

  {/* Inner content card */}
  <div className="bg-white rounded-2xl px-5 py-4">
    {/* Card content */}
  </div>
</div>
```

### Dark Mode

```tsx
<div className="bg-gradient-to-b from-zinc-700 to-zinc-800 rounded-3xl p-2 shadow-xl shadow-black/50 border border-zinc-600/40">
  {/* Media section */}
  <div className="relative h-[240px] w-full rounded-2xl overflow-hidden mb-2 border border-zinc-600/30">
    {/* Image, carousel, or media content */}
  </div>

  {/* Inner content card */}
  <div className="bg-zinc-900 rounded-2xl px-5 py-4">
    {/* Card content */}
  </div>
</div>
```

## Token Reference

| Element | Light Mode | Dark Mode |
|---------|------------|-----------|
| **Outer card** | | |
| Background | `bg-gradient-to-b from-[#e8e8ea] to-[#dcdce0]` | `bg-gradient-to-b from-zinc-700 to-zinc-800` |
| Border | `border-white/60` | `border-zinc-600/40` |
| Shadow | `shadow-xl shadow-zinc-400/30` | `shadow-xl shadow-black/50` |
| Border radius | `rounded-3xl` | `rounded-3xl` |
| Padding | `p-2` | `p-2` |
| **Media section** | | |
| Border | `border-white/40` | `border-zinc-600/30` |
| Border radius | `rounded-2xl` | `rounded-2xl` |
| **Inner card** | | |
| Background | `bg-white` | `bg-zinc-900` |
| Border radius | `rounded-2xl` | `rounded-2xl` |
| Padding | `px-5 py-4` | `px-5 py-4` |

## Sizing Variations

### Preview (compact)

```tsx
// Outer
<div className="rounded-2xl p-1.5 w-[300px]">
  {/* Media: h-[140px], rounded-xl */}
  {/* Inner: rounded-xl, px-3.5 py-3 */}
</div>
```

### Detail Page (full)

```tsx
// Outer
<div className="rounded-3xl p-2 max-w-[420px]">
  {/* Media: h-[240px], rounded-2xl */}
  {/* Inner: rounded-2xl, px-5 py-4 */}
</div>
```

| Context | Outer Radius | Inner Radius | Padding | Media Height |
|---------|-------------|--------------|---------|--------------|
| Preview | `rounded-2xl` | `rounded-xl` | `p-1.5` | `h-[140px]` |
| Detail | `rounded-3xl` | `rounded-2xl` | `p-2` | `h-[240px]` |

## Full Example

```tsx
function ProductCardLight() {
  return (
    <div className="bg-gradient-to-b from-[#e8e8ea] to-[#dcdce0] rounded-3xl p-2 w-full max-w-[420px] shadow-xl shadow-zinc-400/30 border border-white/60">
      {/* Image section */}
      <div className="relative h-[240px] w-full rounded-2xl overflow-hidden mb-2 border border-white/40">
        <Image
          src="/images/product.jpg"
          alt="Product"
          fill
          className="object-cover"
        />
      </div>

      {/* Content section */}
      <div className="bg-white rounded-2xl px-5 py-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-1.5">
          <h3 className="text-lg font-semibold text-zinc-900">
            Product Title
          </h3>
          <span className="text-sm font-medium text-zinc-700">$99</span>
        </div>

        {/* Description */}
        <p className="text-sm text-zinc-500 mb-4">
          Product description goes here.
        </p>

        {/* Tags or features */}
        <div className="flex items-center gap-2 text-xs text-zinc-500">
          <span>Feature 1</span>
          <span className="text-zinc-300">•</span>
          <span>Feature 2</span>
        </div>
      </div>
    </div>
  );
}
```

## Variations

### Without Media Section

```tsx
<div className="bg-gradient-to-b from-[#e8e8ea] to-[#dcdce0] rounded-2xl p-1.5 border border-white/60">
  <div className="bg-white rounded-xl px-4 py-4">
    {/* Content only */}
  </div>
</div>
```

### Multiple Inner Sections

```tsx
<div className="bg-gradient-to-b from-[#e8e8ea] to-[#dcdce0] rounded-3xl p-2 border border-white/60">
  {/* Media */}
  <div className="h-[200px] rounded-2xl overflow-hidden mb-2">...</div>

  {/* Stats bar */}
  <div className="bg-zinc-100 rounded-xl px-4 py-2 mb-2">...</div>

  {/* Main content */}
  <div className="bg-white rounded-2xl px-5 py-4">...</div>
</div>
```

## Checklist

- [ ] Outer card uses gradient background
- [ ] Border radius decreases inward (3xl → 2xl → xl)
- [ ] Inner sections have consistent gap (`mb-2` or `gap-2`)
- [ ] Media section has `overflow-hidden`
- [ ] Shadow appropriate for theme
- [ ] Border opacity creates subtle depth
