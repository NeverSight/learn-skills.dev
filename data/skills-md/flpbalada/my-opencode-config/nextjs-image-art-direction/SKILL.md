---
name: nextjs-image-art-direction
description:
  Implement art direction for Next.js images using getImageProps(). Use when
  showing different images for different viewport sizes, such as homepage carousels
  with mobile vs desktop assets, different cropping/composition, or when mobile
  and desktop images differ completely.
---

# Next.js Image: Art Direction

Art direction means showing **completely different images** based on viewport size — not just resizing the same image. Common use cases include homepage carousels with different assets for mobile vs desktop, switching from landscape (desktop) to portrait (mobile), or showing cropped vs full compositions.

## Art Direction vs Responsive Images

| Approach | Purpose | Implementation |
|----------|---------|----------------|
| **Art Direction** | Different image content/composition | `<picture>` with multiple `<source>` elements |
| **Responsive Images** | Same image, different sizes | `sizes` prop with `srcset` |

**Use Art Direction When:**
- Homepage carousels with different images for mobile and desktop (e.g., square images on mobile, wide banner on desktop)
- Mobile shows portrait crop, desktop shows landscape
- Different focal points for different screen sizes
- Completely different compositions are needed
- Content hierarchy changes between breakpoints
- Different image assets optimized for each viewport (e.g., mobile-optimized JPEGs vs desktop quality)

**Use Responsive Images When:**
- Same image works at all sizes
- Only the dimensions change
- Standard responsive behavior is sufficient

## Implementation with `getImageProps()`

The `getImageProps()` function (stable since Next.js 14.1.0) generates the necessary props without calling React `useState()`, making it ideal for art direction.

### Step-by-Step Implementation

```jsx
import { getImageProps } from 'next/image'

export default function ArtDirectedImage() {
  // Common props shared across all image versions
  const common = { 
    alt: 'Mountain landscape', 
    sizes: '100vw' 
  }
  
  // Desktop version (landscape, higher quality)
  const {
    props: { srcSet: desktop },
  } = getImageProps({
    ...common,
    src: '/hero-desktop.jpg',
    width: 1440,
    height: 875,
    quality: 80,
  })
  
  // Mobile version (portrait, smaller dimensions)
  const {
    props: { srcSet: mobile, ...rest },
  } = getImageProps({
    ...common,
    src: '/hero-mobile.jpg',
    width: 750,
    height: 1334,
    quality: 70,
  })
  
  return (
    <picture>
      {/* Desktop: min-width 1000px */}
      <source media="(min-width: 1000px)" srcSet={desktop} />
      
      {/* Mobile: min-width 500px */}
      <source media="(min-width: 500px)" srcSet={mobile} />
      
      {/* Fallback img element (rendered if no media query matches) */}
      <img {...rest} style={{ width: '100%', height: 'auto' }} />
    </picture>
  )
}
```

### Key Implementation Details

**Props to Vary by Breakpoint:**
- `src`: Different image file
- `width` / `height`: Different dimensions
- `quality`: Different compression levels

**Common Props (Shared):**
- `alt`: Accessibility text (must work for all versions)
- `sizes`: Responsive size hints for browser

**HTML Structure:**
- `<picture>` wrapper element
- `<source>` elements with `media` attribute for each breakpoint
- `<img>` element last as fallback (required)

## Breakpoint Strategy

Order matters! The browser uses the **first matching** `<source>`. List from largest to smallest (desktop-first) or smallest to largest (mobile-first).

### Desktop-First (Largest to Smallest)

```jsx
<picture>
  <source media="(min-width: 1000px)" srcSet={desktop} />
  <source media="(min-width: 500px)" srcSet={tablet} />
  <img {...rest} style={{ width: '100%', height: 'auto' }} />
</picture>
```

### Mobile-First (Smallest to Largest)

```jsx
<picture>
  <source media="(max-width: 499px)" srcSet={mobile} />
  <source media="(max-width: 999px)" srcSet={tablet} />
  <img {...rest} style={{ width: '100%', height: 'auto' }} />
</picture>
```

## Common Pitfalls

### ⚠️ Cannot Use `preload` or `loading="eager"`

These would cause **all images to load immediately**, defeating the purpose of art direction:

```jsx
// BAD: Would load both desktop and mobile
getImageProps({
  src: '/desktop.jpg',
  preload: true, // Don't do this!
})

// BAD: Same problem
getImageProps({
  src: '/desktop.jpg',
  loading: 'eager', // Don't do this!
})
```

**Solution:** Use `fetchPriority="high"` if you need to prioritize the LCP image:

```jsx
const common = { 
  alt: 'Hero image',
  fetchPriority: 'high', // Only load the matching image eagerly
}
```

### ⚠️ Alt Text Must Work for All Versions

The `alt` text is shared across all image versions. Make sure it accurately describes **all** possible images:

```jsx
// BAD: Only describes desktop version
const common = { alt: 'Wide panoramic mountain landscape' }

// GOOD: Describes both versions
const common = { alt: 'Mountain landscape with snow-capped peaks' }
```

### ⚠️ Cannot Use `placeholder` Prop

`getImageProps()` doesn't support the `placeholder` prop because the placeholder would never be removed. Handle loading states manually if needed.

### ⚠️ Ensure Images Exist for All Breakpoints

Missing images will cause broken image icons on certain devices. Always test on actual devices or browser dev tools with different viewport sizes.

## Complete Example: Hero Section

```jsx
import { getImageProps } from 'next/image'

export default function Hero() {
  const common = { 
    alt: 'Team collaboration in modern office',
    sizes: '100vw',
    fetchPriority: 'high',
  }
  
  // Large desktop: Full office scene
  const { props: { srcSet: desktop } } = getImageProps({
    ...common,
    src: '/hero-office-wide.jpg',
    width: 1920,
    height: 1080,
    quality: 85,
  })
  
  // Tablet: Focused team shot
  const { props: { srcSet: tablet } } = getImageProps({
    ...common,
    src: '/hero-team-focused.jpg',
    width: 1024,
    height: 768,
    quality: 80,
  })
  
  // Mobile: Single person portrait
  const { props: { srcSet: mobile, ...rest } } = getImageProps({
    ...common,
    src: '/hero-person-portrait.jpg',
    width: 750,
    height: 1334,
    quality: 75,
  })
  
  return (
    <section className="relative">
      <picture>
        <source media="(min-width: 1200px)" srcSet={desktop} />
        <source media="(min-width: 768px)" srcSet={tablet} />
        <source media="(min-width: 500px)" srcSet={mobile} />
        <img 
          {...rest} 
          className="w-full h-auto object-cover"
          style={{ maxHeight: '80vh' }}
        />
      </picture>
      <div className="absolute inset-0 flex items-center justify-center">
        <h1 className="text-white text-4xl font-bold drop-shadow-lg">
          Welcome to Our Platform
        </h1>
      </div>
    </section>
  )
}
```

## Advanced: CSS Background Images

You can use `getImageProps()` to optimize background images with `image-set()`:

```jsx
import { getImageProps } from 'next/image'

function getBackgroundImage(srcSet = '') {
  const imageSet = srcSet
    .split(', ')
    .map((str) => {
      const [url, dpi] = str.split(' ')
      return `url("${url}") ${dpi}`
    })
    .join(', ')
  return `image-set(${imageSet})`
}

export default function HeroBackground() {
  const {
    props: { srcSet },
  } = getImageProps({
    alt: '',
    width: 1920,
    height: 1080,
    src: '/hero-bg.jpg',
    quality: 80,
  })
  
  const backgroundImage = getBackgroundImage(srcSet)
  
  return (
    <main 
      style={{ 
        height: '100vh', 
        width: '100vw',
        backgroundImage,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <h1>Content Here</h1>
    </main>
  )
}
```

## Quick Reference

### DO

- Use `getImageProps()` for multiple image versions
- Share `alt` and `sizes` across all versions
- Order `<source>` elements correctly (first match wins)
- Use `fetchPriority="high"` for LCP images (not `preload`)
- Test on actual devices or responsive mode in dev tools
- Ensure all image files exist for defined breakpoints

### DON'T

- Use `preload` prop (loads all images)
- Use `loading="eager"` (loads all images)
- Use `placeholder` prop with `getImageProps()`
- Write alt text that only describes one version
- Forget to include the final `<img>` element
- Use art direction when simple responsive images suffice

## References

- [Next.js Image Component Docs - Art Direction](https://nextjs.org/docs/pages/api-reference/components/image#art-direction)
- [MDN - Responsive Images: Art Direction](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images#art_direction)
- [Next.js getImageProps() API](https://nextjs.org/docs/app/api-reference/components/image#getimageprops)
