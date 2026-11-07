---
name: image-media-patterns
description: "Image, video, and media UI patterns: hero and product imagery, galleries, carousels, video and audio players, avatars, thumbnails, aspect ratios, cropping, lazy loading, responsive images, and media accessibility. Use when placing media on a page or building a gallery or player."
---

# Image & Media Patterns — Complete Visual Media System

## Mental model

Media is where performance and craft collide. An unoptimised hero image costs
more than every font, script and stylesheet on the page combined, and a
correctly-sized one is invisible.

- **Reserve the space.** Width and height attributes or `aspect-ratio` on every
  image. Layout shift is the single most common Core Web Vitals failure and the
  easiest to prevent.
- **The hero is never lazy.** `loading="lazy"` on the largest contentful paint
  element delays the thing the score is measuring. Lazy-load everything below
  the fold and nothing above it.
- **Aspect ratio is a design decision.** 16:9 for video, 4:3 for editorial, 1:1
  for avatars and grids, 3:2 for photography. Mixing ratios inside one grid
  reads as an accident.
- **Autoplay needs muting, a pause control, and a reduced-motion escape.** All
  three, not two.
- **Alt text describes function, not appearance.** A decorative image takes
  `alt=""`; a linked image describes the destination.

## Constants

```
16:9  video, embeds            4:3  editorial, product photography
1:1   avatars, grid thumbnails 3:2  photography
21:9  cinematic banners        golden 1.618:1  hero art
```

## Index

| Need | Reference |
|---|---|
| Masonry, justified, uniform, mosaic grid | `gallery-carousel-patterns.md` |
| Lightbox, filter animation, infinite scroll | `gallery-carousel-patterns.md` |
| Scroll-snap or autoplay carousel, filmstrip | `gallery-carousel-patterns.md` |
| Before/after comparison slider | `gallery-carousel-patterns.md` |
| Custom video player, picture-in-picture | `media-player-patterns.md` |
| Audio player, podcast player, voice message | `media-player-patterns.md` |
| Avatars, upload UI, upload progress | `media-player-patterns.md` |
| `srcset` by width or DPR, `<picture>` art direction | `responsive-image-recipes.md` |
| Native and IntersectionObserver lazy loading | `responsive-image-recipes.md` |
| LQIP, BlurHash, ThumbHash, dominant colour | `responsive-image-recipes.md` |
| Choosing AVIF vs WebP vs JPEG; Core Web Vitals | `media-formats-performance.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/media-player-patterns.md` | players, avatars, upload | 1283 |
| `references/gallery-carousel-patterns.md` | 13 gallery and carousel patterns | 1244 |
| `references/responsive-image-recipes.md` | srcset, lazy loading, placeholders | 655 |
| `references/media-formats-performance.md` | format choice, CWV | 97 |

## What every reference file contains

1. When the pattern applies, and the simpler thing to try first
2. Complete HTML/CSS/TSX with the loading strategy included
3. Accessibility: alt text rules, controls, keyboard, reduced motion
4. The performance cost and how to measure it
5. The mobile form of the pattern

## Routing

For **galleries and carousels** — masonry (both CSS-columns and grid), justified,
uniform and mosaic grids, lightboxes, scroll-snap and autoplay carousels,
filmstrips, infinite scroll and comparison sliders: read
`references/gallery-carousel-patterns.md`.

For **players** — a complete custom video player spec, scroll-triggered
picture-in-picture, full audio player, podcast player, and voice-message UI:
read `references/media-player-patterns.md`.

For **shipping images well** — width- and DPR-based `srcset`, art direction with
`<picture>`, native and IntersectionObserver lazy loading, LQIP, BlurHash,
ThumbHash and dominant-color placeholders: read
`references/responsive-image-recipes.md`.

For **odds and ends** — the patterns that had no home in the files above when this skill was converted to a router: read `references/media-supplementary.md`.

## Cross-References

- **layout-block-intelligence** — Hero sections, feature blocks containing images
- **component-patterns-code** — React/SwiftUI/CSS implementations of image components
- **accessibility-inclusive-design** — WCAG media requirements, screen reader patterns
- **performance-states-patterns** — Loading skeletons, error states, empty states
- **responsive-block-patterns** — Container queries, breakpoint transformations
- **animation-recipe-library** — Entrance animations, Ken Burns, parallax recipes
- **form-design-encyclopedia** — File upload form patterns
- **platform-visual-standards** — iOS/Android/web image handling conventions
- **design-systems-architecture** — Token-driven image component APIs
