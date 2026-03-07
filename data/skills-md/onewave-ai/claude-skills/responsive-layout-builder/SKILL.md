---
name: responsive-layout-builder
description: Build responsive layouts with CSS Grid, Flexbox, and container queries. Use when creating responsive designs, fixing layout issues, or building mobile-first layouts.
---

# Responsive Layout Builder

## Instructions

When building responsive layouts:

1. **Identify the layout pattern** (grid, sidebar, cards, etc.)
2. **Start mobile-first**
3. **Use appropriate CSS technique** (Grid vs Flexbox)
4. **Add breakpoints** for larger screens
5. **Test across viewports**

## Breakpoints

```css
/* Tailwind defaults */
sm: 640px   /* Small devices */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Large screens */

/* Custom CSS */
@media (min-width: 640px) { }
@media (min-width: 768px) { }
@media (min-width: 1024px) { }
```

## Common Layout Patterns

### 1. Holy Grail Layout

```tsx
// Tailwind CSS
<div className="min-h-screen flex flex-col">
  <header className="h-16 bg-white border-b">Header</header>

  <div className="flex-1 flex">
    <aside className="hidden md:block w-64 bg-gray-50 border-r">
      Sidebar
    </aside>
    <main className="flex-1 p-6">
      Main Content
    </main>
  </div>

  <footer className="h-16 bg-white border-t">Footer</footer>
</div>
```

```css
/* Plain CSS */
.layout {
  display: grid;
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 1fr;
  min-height: 100vh;
}

@media (min-width: 768px) {
  .layout {
    grid-template-columns: 250px 1fr;
  }

  .header, .footer {
    grid-column: 1 / -1;
  }
}
```

### 2. Responsive Card Grid

```tsx
// Tailwind - Auto-fit cards
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  {items.map(item => (
    <Card key={item.id} {...item} />
  ))}
</div>

// Auto-fill with minimum width
<div className="grid grid-cols-[repeat(auto-fill,minmax(280px,1fr))] gap-6">
  {items.map(item => (
    <Card key={item.id} {...item} />
  ))}
</div>
```

```css
/* Plain CSS */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

### 3. Sidebar Layout

```tsx
// Fixed sidebar, scrollable content
<div className="flex h-screen">
  <aside className="w-64 flex-shrink-0 overflow-y-auto border-r bg-gray-50">
    <nav className="p-4">Sidebar Nav</nav>
  </aside>

  <main className="flex-1 overflow-y-auto">
    <div className="p-6">Main Content</div>
  </main>
</div>

// Collapsible sidebar
<div className="flex h-screen">
  <aside className={cn(
    "flex-shrink-0 overflow-y-auto border-r bg-gray-50 transition-all",
    isOpen ? "w-64" : "w-16"
  )}>
    <nav className="p-4">...</nav>
  </aside>
  <main className="flex-1 overflow-y-auto p-6">...</main>
</div>
```

### 4. Hero Section

```tsx
<section className="relative min-h-[60vh] flex items-center justify-center px-4">
  {/* Background */}
  <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-purple-700" />

  {/* Content */}
  <div className="relative z-10 max-w-4xl mx-auto text-center text-white">
    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold">
      Headline Here
    </h1>
    <p className="mt-6 text-lg md:text-xl opacity-90 max-w-2xl mx-auto">
      Subheadline text goes here with more details.
    </p>
    <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
      <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold">
        Primary CTA
      </button>
      <button className="px-8 py-3 border-2 border-white rounded-lg font-semibold">
        Secondary CTA
      </button>
    </div>
  </div>
</section>
```

### 5. Masonry Grid

```tsx
// CSS Columns approach
<div className="columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6">
  {items.map(item => (
    <div key={item.id} className="break-inside-avoid">
      <Card {...item} />
    </div>
  ))}
</div>
```

### 6. Sticky Header

```tsx
<header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b">
  <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
    <Logo />
    <NavLinks className="hidden md:flex" />
    <MobileMenuButton className="md:hidden" />
  </nav>
</header>
```

## Container Queries (Modern)

```css
/* Define container */
.card-container {
  container-type: inline-size;
}

/* Query the container */
@container (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
  }
}
```

```tsx
// Tailwind v3.2+
<div className="@container">
  <div className="flex flex-col @md:flex-row">
    <img className="w-full @md:w-48" />
    <div className="p-4">Content</div>
  </div>
</div>
```

## Flexbox vs Grid Decision

| Use Flexbox | Use Grid |
|-------------|----------|
| Navigation bars | Page layouts |
| Card content alignment | Card grids |
| Centering content | Complex 2D layouts |
| Space distribution | Overlapping elements |
| Unknown item count | Defined structure |

## Responsive Typography

```tsx
// Fluid typography with clamp
<h1 className="text-[clamp(2rem,5vw,4rem)]">
  Responsive Heading
</h1>

// Tailwind responsive
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">
  Responsive Heading
</h1>
```

## Testing Checklist

- [ ] 320px (small phones)
- [ ] 375px (iPhone)
- [ ] 768px (tablet portrait)
- [ ] 1024px (tablet landscape / laptop)
- [ ] 1280px+ (desktop)
- [ ] Test with actual content (not lorem ipsum)
- [ ] Test with long/short content variations
