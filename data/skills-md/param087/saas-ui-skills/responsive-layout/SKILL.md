---
name: responsive-layout
description: Use when building the app shell or any responsive screen — sidebar + topbar layouts, Tailwind breakpoints, container queries, and fluid grids that hold up from mobile to ultrawide.
---

# Responsive Layout

## Overview

Most SaaS apps share one shell: a collapsible sidebar, a sticky topbar, and a scrollable content area. Get the shell right with Flexbox/Grid and a mobile-first approach, and every page inside inherits good behavior. Reach for **container queries** when a component must adapt to *its container*, not the viewport.

## When to use

- Building the application frame (sidebar + topbar + content).
- A layout breaks on mobile or wastes space on wide screens.
- A component needs to reflow based on available width, not screen size.

## App shell pattern

```tsx
export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {/* Sidebar: hidden on mobile, fixed width on desktop */}
      <aside className="hidden w-64 shrink-0 border-r md:block">
        <Sidebar />
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b bg-background/95 px-4 backdrop-blur">
          <MobileNavTrigger className="md:hidden" />
          <Topbar />
        </header>

        <main className="flex-1 overflow-y-auto p-4 md:p-6">
          <div className="mx-auto w-full max-w-6xl">{children}</div>
        </main>
      </div>
    </div>
  );
}
```

`min-w-0` on the flex child is the unsung hero — without it, long content (tables, code) forces horizontal overflow instead of wrapping.

## Mobile-first breakpoints

Write the base style for mobile, then layer `sm: md: lg:` for larger screens:

```tsx
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
```

Tailwind breakpoints: `sm 640 · md 768 · lg 1024 · xl 1280 · 2xl 1536`. On mobile the sidebar becomes a `Sheet` (see modals-and-dialogs).

## Container queries (component-level responsiveness)

A card in a 3-column grid and the same card full-width should look different — based on *its* width:

```tsx
<div className="@container">
  <article className="flex flex-col gap-4 @md:flex-row @md:items-center">
    <img className="aspect-video w-full rounded-lg @md:w-48" />
    <div>…</div>
  </article>
</div>
```

Enable with the `@tailwindcss/container-queries` plugin. Prefer container queries for reusable components; viewport breakpoints for page structure.

## Fluid sizing

- `clamp()` for fluid type/space: `text-[clamp(1.5rem,4vw,2.5rem)]`.
- `min-h-screen` not `h-screen` for content that can grow.
- `max-w-*` + `mx-auto` to cap line length on wide screens (readability tops out ~75ch).

## Pitfalls

- **Forgetting `min-w-0`** on flex children → page-wide horizontal scrollbars.
- **`h-screen` with growing content** clips overflow; use `min-h-screen`.
- **Desktop-first** (`lg:` everywhere, overriding down) is harder than mobile-first.
- **No max width** on huge monitors → 200-character lines nobody can read.
- **Viewport queries for components** that get reused at different widths.

## Hand-off

A responsive shell that hosts `navigation-patterns` (the sidebar), `dashboard-layout`, and every product page.
