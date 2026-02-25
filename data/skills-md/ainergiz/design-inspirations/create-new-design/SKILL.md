---
name: create-new-design
description: Scaffolds a new design in the design-inspirations repo with preview component, detail page, and main page entry. Use when creating a new design, adding a design inspiration, or scaffolding design files.
---

# Create New Design

Scaffold a new design inspiration with the correct file structure, ViewTransition naming, and component patterns.

## Required Information

Before creating files, gather:

1. **Design ID** (kebab-case): e.g., `pricing-table`, `user-profile`
2. **Title**: e.g., "Pricing Table", "User Profile Card"
3. **Description**: One-line description for the main page
4. **Tags**: 2-4 category tags (e.g., "Card", "Form", "Dashboard")
5. **Attribution** (optional): Twitter handle of original designer

## File Structure

```
src/
├── app/
│   ├── designs/
│   │   └── [design-id]/
│   │       └── page.tsx          # Detail page
│   └── page.tsx                   # Update designs array
└── components/
    └── previews/
        └── [Name]Preview.tsx      # Preview component
```

## Step 1: Create Preview Component

Create `src/components/previews/[Name]Preview.tsx`.

See [examples/preview-template.tsx](examples/preview-template.tsx) for the full template.

Key conventions:
- Export named function: `export function [Name]Preview()`
- ViewTransition names: `[design-id]-light`, `[design-id]-dark`, `[design-id]-light-panel`, `[design-id]-dark-panel`
- Side-by-side layout with dot grid backgrounds
- Light panel: `bg-[#f5f5f5]` with `#d4d4d4` dots
- Dark panel: `bg-zinc-950` with `#3f3f46` dots

## Step 2: Create Detail Page

Create `src/app/designs/[design-id]/page.tsx`.

See [examples/page-template.tsx](examples/page-template.tsx) for the full template.

Key conventions:
- Use DM Sans font for design pages
- Split layout: 50/50 light/dark
- Header with back arrow, Code button, and attribution
- Code button links to the component file on GitHub
- Attribution format: "Inspired from @username" with profile photo via `unavatar.io`

## Step 3: Update Main Page

Add entry to `src/app/page.tsx`:

```tsx
import { [Name]Preview } from "@/components/previews/[Name]Preview";

const designs = [
  // ... existing designs
  {
    id: "[design-id]",
    number: "XX",  // Increment from last
    title: "[Title]",
    description: "[Description]",
    tags: ["Tag1", "Tag2"],
    PreviewComponent: [Name]Preview,
  },
];
```

## Step 4: Update globals.css

Add ViewTransition CSS for new design in `src/app/globals.css`:

```css
/* Add to existing shared element transitions section */
::view-transition-old([design-id]-light),
::view-transition-new([design-id]-light),
::view-transition-old([design-id]-dark),
::view-transition-new([design-id]-dark),
::view-transition-old([design-id]-light-panel),
::view-transition-new([design-id]-light-panel),
::view-transition-old([design-id]-dark-panel),
::view-transition-new([design-id]-dark-panel) {
  animation-duration: 300ms;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Add to reduced motion section */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old([design-id]-light),
  ::view-transition-new([design-id]-light),
  ::view-transition-old([design-id]-dark),
  ::view-transition-new([design-id]-dark),
  ::view-transition-old([design-id]-light-panel),
  ::view-transition-new([design-id]-light-panel),
  ::view-transition-old([design-id]-dark-panel),
  ::view-transition-new([design-id]-dark-panel) {
    animation: none;
  }
}
```

## ViewTransition Naming Convention

| Element | Pattern | Example |
|---------|---------|---------|
| Light card | `[design-id]-light` | `pricing-table-light` |
| Dark card | `[design-id]-dark` | `pricing-table-dark` |
| Light panel | `[design-id]-light-panel` | `pricing-table-light-panel` |
| Dark panel | `[design-id]-dark-panel` | `pricing-table-dark-panel` |

## Code Button Format

```tsx
<a
  href="https://github.com/ainergiz/design-inspirations/blob/main/src/app/designs/[design-id]/page.tsx"
  target="_blank"
  rel="noopener noreferrer"
  className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-zinc-500 hover:text-zinc-700 hover:bg-zinc-100 rounded-lg transition-colors"
>
  <Code className="w-4 h-4" />
  <span className="hidden sm:inline">Code</span>
</a>
```

## Attribution Format

```tsx
<a
  href="https://x.com/[username]"
  target="_blank"
  rel="noopener noreferrer"
  className="flex items-center gap-2 text-sm text-zinc-500 hover:text-zinc-700"
>
  <span className="hidden sm:inline text-zinc-400">Inspired from</span>
  <Image
    src="https://unavatar.io/x/[username]"
    alt="[Name]"
    width={24}
    height={24}
    className="w-6 h-6 rounded-full"
  />
  <span className="font-medium text-zinc-700">@[username]</span>
  <ExternalLink className="w-3.5 h-3.5" />
</a>
```

## Step 5: Custom Animations (if needed)

If your component has custom animations (e.g., carousels, progress bars), add keyframes to `src/app/globals.css`:

```css
/* Example: Carousel progress animation */
@keyframes carousel-progress {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

.animate-carousel-progress {
  animation: carousel-progress linear forwards;
}
```

Common animation patterns:
- **Progress bars**: `scaleX(0)` to `scaleX(1)` with `origin-left`
- **Fade in**: `opacity: 0` to `opacity: 1`
- **Slide up**: `translateY(10px)` to `translateY(0)`

## Related Skills

Consider using these patterns in your design:
- **component-variants**: Color token mapping for light/dark modes
- **expandable-card**: Smooth expand/collapse with grid-rows
- **image-carousel**: Auto-advance carousel with touch support
- **glassmorphism**: Frosted glass overlay effects
- **nested-card**: Outer gradient with inner content card
- **stacked-cards**: Fanned/cascading card stacks with hover lift
- **dropdown-menu**: Click-outside detection and z-index stacking

## Checklist

- [ ] Preview component created with correct ViewTransition names
- [ ] Detail page created with split layout
- [ ] Code button links to component file on GitHub
- [ ] Design entry added to main page designs array
- [ ] globals.css updated with ViewTransition CSS
- [ ] Custom keyframes added to globals.css (if needed)
- [ ] Attribution included (if available)
- [ ] Both light and dark variants implemented
- [ ] Components follow existing code style
- [ ] Touch interactions considered for mobile
