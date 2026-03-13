---
name: mobile-ux-improver
description: Mobile-first UX best practices enforcer for web applications. Covers touch targets, responsive design, mobile gestures, performance optimization, and accessibility. Use when creating or editing mobile UI components, implementing responsive layouts, handling touch interactions, optimizing for mobile devices, or working with viewport configurations, breakpoints, and mobile-specific patterns.
---

# Mobile UX Improver

## Purpose

Enforce mobile-first UX best practices to ensure exceptional mobile web experiences. This skill prevents common mobile UX mistakes and guides implementation of touch-friendly, responsive, performant interfaces.

## When to Use

Auto-triggers when:
- Editing mobile UI components
- Working with responsive layouts
- Implementing touch interactions
- Optimizing mobile performance
- Using Tailwind responsive classes (sm:, md:, lg:)
- Handling mobile gestures

Manual trigger when:
- Reviewing mobile UX
- Implementing new mobile features
- Debugging mobile-specific issues

---

## Quick Reference

### Touch Targets

**Minimum Sizes:**
- ✅ **48px × 48px** (recommended)
- ⚠️ **44px × 44px** (absolute minimum)
- ❌ **< 44px** (too small, avoid)

**Spacing:**
- 8px minimum between interactive elements
- 12px+ recommended for frequently used controls

### Responsive Breakpoints (Tailwind)

```typescript
// Mobile-first approach
<div className="w-full md:w-1/2 lg:w-1/3">

// Breakpoints
sm: 640px   // Small tablets
md: 768px   // Tablets
lg: 1024px  // Small desktops
xl: 1280px  // Large desktops
2xl: 1536px // Extra large
```

### Performance Targets

- **First Contentful Paint**: < 1.8s
- **Time to Interactive**: < 3.8s
- **Cumulative Layout Shift**: < 0.1
- **Largest Contentful Paint**: < 2.5s

---

## Core Principles

### 1. Mobile-First Design

**Always start with mobile layout:**

```typescript
// ✅ CORRECT - Mobile first, then desktop
<button className="w-full px-4 py-3 md:w-auto md:px-6">
  Tap Me
</button>

// ❌ WRONG - Desktop first
<button className="w-auto px-6 sm:w-full sm:px-4">
  Tap Me
</button>
```

**Why:** Mobile constraints force better UX decisions, easier to scale up than down.

### 2. Touch-Friendly Targets

**Minimum interactive area:**

```typescript
// ✅ CORRECT - 48px touch target
<button className="min-h-[48px] min-w-[48px] p-3">
  <Icon className="w-6 h-6" />
</button>

// ❌ WRONG - Too small
<button className="p-1">
  <Icon className="w-4 h-4" />
</button>
```

**Spacing between targets:**

```typescript
// ✅ CORRECT - Adequate spacing
<div className="flex gap-3">
  <button className="p-3">A</button>
  <button className="p-3">B</button>
</div>

// ❌ WRONG - Targets too close
<div className="flex gap-1">
  <button className="p-1">A</button>
  <button className="p-1">B</button>
</div>
```

### 3. Responsive Typography

**Use relative units for mobile:**

```typescript
// ✅ CORRECT - Scales with viewport
<h1 className="text-2xl md:text-4xl lg:text-5xl">
  Heading
</h1>

// ✅ CORRECT - Clamp for fluid scaling
<p className="text-base leading-relaxed">
  Body text
</p>

// ⚠️ AVOID - Fixed pixel sizes
<h1 style={{ fontSize: '60px' }}>
  Heading
</h1>
```

### 4. Viewport Configuration

**Required meta tag:**

```html
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
```

**Why maximum-scale=5:** Allows zoom for accessibility while preventing excessive zoom accidents.

---

## Touch Targets & Spacing

### Target Sizing Chart

| Element Type | Minimum Size | Recommended Size | Spacing |
|--------------|--------------|------------------|---------|
| Primary Button | 44px | 48px | 12px |
| Icon Button | 44px | 48px | 8px |
| Link in Text | 44px height | 48px height | 8px vertical |
| Checkbox/Radio | 44px | 48px | 12px |
| Slider Thumb | 44px | 48px | N/A |

### Common Patterns

**Primary Action Button:**

```typescript
<button className="w-full px-6 py-4 text-lg font-semibold rounded-lg bg-brand-blue text-white hover:bg-blue-600 active:bg-blue-700 transition-colors min-h-[48px]">
  Continue
</button>
```

**Icon Button:**

```typescript
<button
  className="p-3 rounded-full hover:bg-gray-100 active:bg-gray-200 transition-colors min-h-[48px] min-w-[48px] flex items-center justify-center"
  aria-label="Close"
>
  <XIcon className="w-6 h-6" />
</button>
```

**List of Links:**

```typescript
<nav className="space-y-2">
  {links.map(link => (
    <a
      key={link.id}
      href={link.url}
      className="block px-4 py-3 text-base hover:bg-gray-50 active:bg-gray-100 rounded-lg min-h-[48px]"
    >
      {link.label}
    </a>
  ))}
</nav>
```

**[📖 Complete Guide: resources/touch-targets-guide.md](resources/touch-targets-guide.md)**

---

## Responsive Design

### Mobile-First Approach

**Start with mobile, enhance for larger screens:**

```typescript
// Layout structure
<div className="
  flex flex-col gap-4          /* Mobile: stack vertically */
  md:flex-row md:gap-6         /* Tablet: horizontal */
  lg:gap-8                     /* Desktop: more spacing */
">
  <aside className="w-full md:w-64 lg:w-80">
    Sidebar
  </aside>
  <main className="flex-1">
    Content
  </main>
</div>
```

### Container Patterns

**Responsive containers:**

```typescript
// Full-width on mobile, constrained on desktop
<div className="
  w-full px-4                  /* Mobile: full width, padding */
  md:px-6                      /* Tablet: more padding */
  lg:max-w-7xl lg:mx-auto lg:px-8  /* Desktop: centered, max width */
">
  {children}
</div>
```

### Grid Layouts

**Responsive grid:**

```typescript
<div className="
  grid grid-cols-1 gap-4       /* Mobile: 1 column */
  sm:grid-cols-2 sm:gap-6      /* Small tablet: 2 columns */
  lg:grid-cols-3 lg:gap-8      /* Desktop: 3 columns */
">
  {items.map(item => (
    <Card key={item.id} {...item} />
  ))}
</div>
```

### Hiding/Showing Elements

**Conditional visibility:**

```typescript
// Mobile menu vs desktop nav
<>
  {/* Mobile menu button */}
  <button className="md:hidden p-3">
    <MenuIcon />
  </button>

  {/* Desktop navigation */}
  <nav className="hidden md:flex gap-6">
    <NavLink href="/about">About</NavLink>
    <NavLink href="/contact">Contact</NavLink>
  </nav>
</>
```

**[📖 Complete Guide: resources/responsive-patterns.md](resources/responsive-patterns.md)**

---

## Mobile Gestures

### Horizontal Scrolling

**Swipeable container:**

```typescript
<div className="
  flex gap-4 overflow-x-auto snap-x snap-mandatory
  scrollbar-hide              /* Hide scrollbar on mobile */
  pb-4                        /* Padding for scroll indicator */
  -mx-4 px-4                  /* Edge-to-edge on mobile */
  md:mx-0 md:px-0             /* Contained on desktop */
">
  {items.map(item => (
    <div
      key={item.id}
      className="flex-shrink-0 w-72 snap-center"
    >
      <Card {...item} />
    </div>
  ))}
</div>
```

### Pull-to-Refresh

**Implement with overscroll-behavior:**

```typescript
<main className="
  overscroll-contain          /* Prevent chain scrolling */
  overflow-y-auto
  h-screen
">
  {content}
</main>
```

### Scroll Behavior

**Smooth scrolling:**

```typescript
// Global CSS or Tailwind
<html className="scroll-smooth">

// Component-level
<div className="overflow-y-auto scroll-smooth">
  {longContent}
</div>
```

**[📖 Complete Guide: resources/mobile-gestures.md](resources/mobile-gestures.md)**

---

## Performance Optimization

### Image Optimization

**Responsive images:**

```typescript
<img
  src="/hero-mobile.jpg"
  srcSet="
    /hero-mobile.jpg 640w,
    /hero-tablet.jpg 1024w,
    /hero-desktop.jpg 1920w
  "
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1024px) 50vw,
    33vw
  "
  alt="Hero image"
  loading="lazy"
  className="w-full h-auto"
/>
```

### Lazy Loading

**Component lazy loading:**

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function Page() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Font Loading

**Optimize web fonts:**

```html
<link
  rel="preload"
  href="/fonts/custom-font.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

**[📖 Complete Guide: resources/mobile-performance.md](resources/mobile-performance.md)**

---

## Accessibility for Mobile

### Screen Reader Support

**Proper labeling:**

```typescript
<button
  aria-label="Close dialog"
  className="p-3"
>
  <XIcon className="w-6 h-6" />
</button>
```

### Focus Management

**Keyboard + touch support:**

```typescript
<button className="
  p-3 rounded-lg
  focus:outline-none focus:ring-2 focus:ring-brand-blue focus:ring-offset-2
  active:bg-gray-100
">
  Action
</button>
```

### Color Contrast

**WCAG AA minimum:**
- Normal text: 4.5:1
- Large text: 3:1
- Interactive elements: 3:1

---

## Common Anti-Patterns to Avoid

### ❌ Don't: Hover-Only Interactions

```typescript
// ❌ WRONG - No hover on touch devices
<div className="hover:visible">
  Hidden content
</div>

// ✅ CORRECT - Click/tap to reveal
<button onClick={() => setVisible(true)}>
  Show content
</button>
```

### ❌ Don't: Fixed Positioning That Blocks Content

```typescript
// ❌ WRONG - Header blocks content
<header className="fixed top-0 w-full h-16 bg-white">

<main className="pt-0">  /* Content hidden behind header */

// ✅ CORRECT - Account for header
<header className="fixed top-0 w-full h-16 bg-white z-10">

<main className="pt-16">  /* Content starts below header */
```

### ❌ Don't: Tiny Text

```typescript
// ❌ WRONG - Unreadable on mobile
<p className="text-xs">
  Important information
</p>

// ✅ CORRECT - Readable base size
<p className="text-base md:text-sm">
  Important information
</p>
```

### ❌ Don't: Disable Zoom

```html
<!-- ❌ WRONG - Prevents accessibility -->
<meta name="viewport" content="user-scalable=no, maximum-scale=1">

<!-- ✅ CORRECT - Allow zoom for accessibility -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
```

---

## Example: Mobile-Optimized Component

**Complete touch-friendly card:**

```typescript
import React from 'react';

interface ProductCardProps {
  title: string;
  price: number;
  image: string;
  onAddToCart: () => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  title,
  price,
  image,
  onAddToCart
}) => {
  return (
    <div className="
      bg-white rounded-lg shadow-sm overflow-hidden
      hover:shadow-md transition-shadow
      w-full                          /* Mobile: full width */
      sm:w-64                         /* Tablet: fixed width */
    ">
      <img
        src={image}
        alt={title}
        loading="lazy"
        className="w-full h-48 object-cover"
      />

      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2 line-clamp-2">
          {title}
        </h3>

        <p className="text-2xl font-bold text-brand-blue mb-4">
          ${price.toFixed(2)}
        </p>

        <button
          onClick={onAddToCart}
          className="
            w-full px-6 py-3 rounded-lg
            bg-brand-blue text-white font-semibold
            hover:bg-blue-600 active:bg-blue-700
            transition-colors
            min-h-[48px]              /* Touch-friendly height */
            focus:outline-none focus:ring-2 focus:ring-brand-blue focus:ring-offset-2
          "
          aria-label={`Add ${title} to cart`}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
```

---

## Testing Mobile UX

### Manual Testing Checklist

- [ ] Test on real mobile devices (iOS, Android)
- [ ] Verify touch targets are 44px+ minimum
- [ ] Check text is readable without zoom
- [ ] Test horizontal scrolling with touch
- [ ] Verify forms work with mobile keyboards
- [ ] Test landscape + portrait orientations
- [ ] Check performance on slow connections
- [ ] Verify hover states have touch alternatives
- [ ] Test with screen reader (VoiceOver, TalkBack)
- [ ] Check color contrast meets WCAG AA

### Browser DevTools

**Chrome DevTools Mobile Emulation:**
1. Open DevTools (F12)
2. Toggle device toolbar (Cmd+Shift+M / Ctrl+Shift+M)
3. Select device or custom dimensions
4. Enable touch emulation
5. Test throttling (3G, 4G networks)

---

## Reference Existing Components

**Good examples in your codebase:**

- `FilterPill.tsx` - Touch-friendly pill buttons with proper spacing
- `TeamCard.tsx` - Responsive card layout with touch interactions
- `Fab.tsx` - Floating action button with proper touch target

---

## Related Skills

- **frontend-dev-guidelines**: React/TypeScript best practices
- **seo-specialist**: Mobile SEO optimization
- **error-tracking**: Performance monitoring

---

**Skill Status**: Active guardrail - Enforces mobile UX quality
**Line Count**: < 500 (following 500-line rule) ✅
**Progressive Disclosure**: Reference files for detailed guides ✅
