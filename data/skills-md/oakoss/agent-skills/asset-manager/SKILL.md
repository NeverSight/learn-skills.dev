---
name: asset-manager
description: 'Organize design assets, optimize images and fonts, maintain brand asset libraries, implement version control for assets, and enforce naming conventions. Use when optimizing images for web, converting fonts to WOFF2, organizing asset directories, setting up responsive image pipelines, or managing logo variants.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Asset Manager

Manages design assets across projects: directory organization, naming conventions, image/font optimization, brand libraries, and version control. Use when assets need to be organized, compressed, converted to modern formats, or tracked across releases. Not for runtime image transformations or CDN configuration beyond path prefixing.

## Quick Reference

| Task               | Tool / Approach               | Key Points                                                   |
| ------------------ | ----------------------------- | ------------------------------------------------------------ |
| Image optimization | Sharp                         | Resize, compress, convert to WebP/AVIF/JPEG/PNG              |
| SVG optimization   | SVGO (v4+)                    | `removeViewBox` and `removeTitle` off by default in v4       |
| Font conversion    | `woff2_compress`, `sfnt2woff` | TTF/OTF to WOFF2 (primary) + WOFF (fallback)                 |
| Font subsetting    | Glyphhanger                   | Remove unused glyphs, auto-detect from crawled pages         |
| Responsive images  | Sharp breakpoints             | Generate mobile (640), tablet (768), desktop (1920) variants |
| Asset versioning   | SHA-256 hash tracking         | `asset-versions.json` manifest with change detection         |
| Large files in git | Git LFS                       | Track PSD, AI, Sketch, Figma, MP4, MOV files                 |
| Brand assets       | Typed manifest                | `BrandAssets` interface with logos, colors, typography       |

## Directory Structure

| Directory                                | Contents                                 |
| ---------------------------------------- | ---------------------------------------- |
| `assets/images/{category}/`              | Products, team, marketing, UI images     |
| `assets/icons/svg/`                      | SVG icon files                           |
| `assets/fonts/{family}/`                 | WOFF2 + WOFF font files                  |
| `assets/videos/`                         | Video assets                             |
| `assets/logos/svg/`, `png/`, `variants/` | Logo formats and color variants          |
| `brand/`                                 | Colors JSON, typography JSON, guidelines |

## Naming Conventions

| Asset Type | Pattern                                    | Example                           |
| ---------- | ------------------------------------------ | --------------------------------- |
| Images     | `{category}-{description}-{size}.{format}` | `product-hero-1920x1080.jpg`      |
| Icons      | `{icon-name}-{variant}.svg`                | `home-outline.svg`                |
| Fonts      | `{font-family}-{weight}.{format}`          | `Inter-Regular.woff2`             |
| Logos      | `logo-{variant}.{format}`                  | `logo-full.svg`, `logo-white.svg` |

## Optimization Targets

| Format | Tool             | Use Case                          |
| ------ | ---------------- | --------------------------------- |
| WebP   | Sharp            | Primary web images                |
| AVIF   | Sharp            | Modern browsers, best compression |
| JPEG   | Sharp (mozjpeg)  | Fallback photos                   |
| PNG    | Sharp            | UI elements with transparency     |
| SVG    | SVGO             | Icons and logos                   |
| WOFF2  | `woff2_compress` | Primary web fonts                 |
| WOFF   | `sfnt2woff`      | Font fallback                     |

## Pipeline Steps

| Step              | Action                                                |
| ----------------- | ----------------------------------------------------- |
| Organize          | Sort unsorted assets by naming rules into directories |
| Optimize images   | Resize, compress, generate WebP/AVIF variants         |
| Responsive images | Generate mobile/tablet/desktop breakpoint sizes       |
| Optimize fonts    | Convert TTF/OTF to WOFF2 + WOFF                       |
| Version           | Hash-based tracking with `asset-versions.json`        |

## Common Mistakes

| Mistake                             | Fix                                                        |
| ----------------------------------- | ---------------------------------------------------------- |
| Committing raw design files to git  | Use Git LFS for PSD, AI, Sketch, Figma, video files        |
| Serving original-size images        | Generate responsive variants at breakpoints                |
| Using only JPEG/PNG                 | Generate WebP + AVIF with fallbacks                        |
| No font subsetting                  | Use Glyphhanger to subset unused glyphs                    |
| Missing `font-display: swap`        | Always set on `@font-face` to avoid FOIT                   |
| No CDN for assets                   | Prefix asset paths with `CDN_URL` env variable             |
| Using imagemin for new projects     | Use Sharp directly; imagemin is unmaintained               |
| Using SVGO v3 plugin config with v4 | `removeViewBox` and `removeTitle` are off by default in v4 |

## Delegation

- **Discover asset organization patterns in a codebase**: Use `Explore` agent to find existing asset directories, naming conventions, and optimization scripts
- **Optimize a batch of images or fonts**: Use `Task` agent to run Sharp pipelines, font conversions, and responsive image generation
- **Plan a complete asset pipeline**: Use `Plan` agent to design directory structure, naming conventions, optimization steps, and CI integration

## References

- [Organization](references/organization.md)
- [Image Optimization](references/image-optimization.md)
- [Font Management](references/font-management.md)
- [Version Control](references/version-control.md)
- [Brand Library](references/brand-library.md)
- [Best Practices](references/best-practices.md)
