---
name: responsive-images
description: |
  Implement performant responsive images with srcset, sizes, lazy loading, and modern formats (WebP, AVIF). Covers aspect-ratio for CLS prevention, picture element for art direction, and fetchpriority for LCP optimization.

  Use when adding images to pages, optimizing Core Web Vitals, preventing layout shift, implementing art direction, or converting to modern formats.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Responsive Images

## Overview

Responsive images serve the right image size and format based on viewport, device pixel ratio, and browser capabilities. Proper implementation prevents layout shift (CLS), optimizes Largest Contentful Paint (LCP), and reduces bandwidth by 50-70% with modern formats.

**When to use:** Any page with images, especially content images, hero images, product photos, and gallery layouts.

**When NOT to use:** Inline SVG icons, CSS background patterns, or canvas-rendered graphics.

## Quick Reference

| Pattern           | Approach                                      | Key Points                                         |
| ----------------- | --------------------------------------------- | -------------------------------------------------- |
| Responsive sizing | `srcset` with width descriptors (w) + `sizes` | Browser selects optimal image for viewport and DPR |
| Modern formats    | `<picture>` with AVIF, WebP, JPEG sources     | AVIF saves 70%, WebP saves 50% vs JPEG             |
| Art direction     | `<picture>` with `media` queries              | Different crops per viewport                       |
| LCP hero image    | `loading="eager"` + `fetchpriority="high"`    | Prioritize download for Core Web Vitals            |
| Below-fold images | `loading="lazy"`                              | Defer until near viewport                          |
| Prevent CLS       | `width` + `height` attributes                 | Browser reserves space before load                 |
| Fixed containers  | `object-fit: cover` or `contain`              | Maintain aspect ratio in constrained space         |
| Format fallback   | AVIF, WebP, JPEG source order                 | Best compression first, universal fallback last    |

## Recommended Image Sizes

| Use Case           | Widths to Generate        | Sizes Attribute                   |
| ------------------ | ------------------------- | --------------------------------- |
| Full-width hero    | 800w, 1200w, 1600w, 2400w | `100vw`                           |
| Content width      | 400w, 800w, 1200w         | `(max-width: 768px) 100vw, 800px` |
| Grid cards (3-col) | 300w, 600w, 900w          | `(max-width: 768px) 100vw, 33vw`  |
| Sidebar thumbnail  | 150w, 300w                | `150px`                           |

## Loading Strategy

| Image Position       | loading | fetchpriority | Why                               |
| -------------------- | ------- | ------------- | --------------------------------- |
| Hero/LCP             | `eager` | `high`        | Optimize LCP, prioritize download |
| Above fold (not LCP) | `eager` | omit          | Load normally                     |
| Below fold           | `lazy`  | omit          | Defer until near viewport         |
| Off-screen carousel  | `lazy`  | omit          | Defer until interaction           |

## Format Comparison

| Format | Quality   | File Size | Browser Support | Use Case                         |
| ------ | --------- | --------- | --------------- | -------------------------------- |
| JPEG   | Good      | Medium    | 100%            | Photos, complex images           |
| PNG    | Lossless  | Large     | 100%            | Logos, transparency              |
| WebP   | Excellent | Small     | 96%+            | Modern browsers, photos          |
| AVIF   | Excellent | Smallest  | 93%+            | Newest format, fallback required |

## Common Mistakes

| Mistake                                                      | Correct Pattern                                                       |
| ------------------------------------------------------------ | --------------------------------------------------------------------- |
| Omitting width and height attributes on img elements         | Always include `width` and `height` to prevent CLS layout shift       |
| Lazy loading the LCP hero image                              | Use `loading="eager"` and `fetchpriority="high"` for LCP images       |
| Using density descriptors (1x, 2x) for variable-width images | Use width descriptors (400w, 800w) with a `sizes` attribute           |
| Missing alt text on content images                           | Provide descriptive alt text; use `alt=""` only for decorative images |
| Serving only JPEG without modern format fallbacks            | Use `<picture>` with AVIF and WebP sources falling back to JPEG       |

## Delegation

- **Audit a page for responsive image issues and CLS problems**: Use `Explore` agent to scan HTML for missing attributes, incorrect loading strategies, and format gaps
- **Convert all images on a page to use picture element with modern formats**: Use `Task` agent to rewrite img tags with AVIF/WebP/JPEG fallback chain
- **Plan an image optimization pipeline for a multi-page site**: Use `Plan` agent to design srcset breakpoints, format conversion workflow, and CDN integration

## References

- [srcset, sizes, and width descriptor patterns](references/srcset-sizes.md)
- [Picture element and art direction](references/picture-element.md)
- [Modern image formats: WebP, AVIF, and conversion tools](references/modern-formats.md)
- [Lazy loading, fetchpriority, and LCP optimization](references/lazy-loading.md)
- [Aspect ratio, object-fit, and CLS prevention](references/aspect-ratio.md)
