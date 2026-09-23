---
name: hugo-theme
description: >-
  Build, customize, and debug advanced Hugo CMS themes — template architecture, asset
  pipeline (CSS/JS/image processing), shortcodes and render hooks, page bundles, cover
  images, Hugo Modules, performance, SEO, and CI/CD. Use when working on a Hugo theme or
  site template layer. Do not use this skill for unrelated requests; route to the nearest
  named specialist.
license: MIT
compatibility: Works with any agent framework supporting the Agent Skills format.
metadata:
  source: >-
    Research compiled from official Hugo docs, major theme repositories, Hugo
    power user blogs, and community discussions.
  hugo-version: v0.154+
---

# Hugo Theme Development

Intermediate-to-advanced patterns for Hugo CMS theme development. Load the relevant reference file for your task.

## Reference Files

| Topic | Hugo Min | Load when... | File |
|-------|----------|-------------|------|
| **Template Architecture** | v0.120+ | You need to set up base templates with blocks, understand template lookup order (kind/layout/type/section), create partials, use partial decorators (v0.154+), or work with shortcode fundamentals | `references/template-architecture.md` |
| **Asset Pipeline** | v0.161+ | You're integrating Tailwind CSS v4 (`css.TailwindCSS`) or v3 (PostCSS), using Hugo Pipes for SCSS/JS bundling, setting up fingerprinting and SRI, building responsive images with srcset, or processing page/global/remote resources | `references/asset-pipeline.md` |
| **Shortcodes & Render Hooks** | v0.112+ | You need complex nested shortcodes, raw HTML shortcodes, markdown rendering inside shortcodes, custom render hooks for links/images/headings/code blocks, or language-specific code block rendering (Mermaid, etc.) | `references/shortcodes-and-hooks.md` |
| **Content Organization & i18n** | v0.126+ | You're working with leaf vs branch bundles, headless bundles, cover images, custom taxonomies, content adapters (v0.126+, dynamic pages), section-specific layouts, archetypes, or internationalization (translation tables, multilingual) | `references/content-and-i18n.md` |
| **Cover Images** | v0.120+ | You need to add cover/hero images to articles, support both page bundle resources and frontmatter paths, generate responsive srcsets, or handle the no-cover case gracefully | `references/cover-images.md` |
| **Modules & Performance** | v0.109+ | You're using Hugo Modules (init, import, vendor, workspace), building theme components with mount configuration, optimizing build speed with `partialCached`, configuring cache TTLs, or using configuration-driven theming (params, cascade) | `references/modules-and-performance.md` |
| **Design, UX & Accessibility** | v0.120+ | You need typography systems, accessible color palettes, design tokens, semantic HTML landmarks, ARIA patterns, keyboard navigation, accessible forms, content-first layouts, responsive navigation, engagement patterns (reading progress, dark mode toggle, sharing), Core Web Vitals optimization, container queries, `:has()` selectors, or testing/QA automation (axe-core, Lighthouse CI, visual regression) | `references/design-accessibility.md` |
| **SEO, Output Formats & CI/CD** | v0.120+ | You need JSON-LD structured data, Open Graph / Twitter Cards, custom output formats (JSON, AMP), sitemap customization, or CI/CD pipelines for themes (GitHub Actions, testing, deployment) | `references/seo-outputs-testing.md` |

## Quick Start

```go-html-template
{{/* Minimal theme baseof.html — start here */}}
<!DOCTYPE html>
<html lang="{{ .Site.Language.Lang }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ block "title" . }}{{ .Site.Title }}{{ end }}</title>
  {{ block "styles" . }}{{ end }}
</head>
<body>
  {{ block "header" . }}{{ partial "header.html" . }}{{ end }}
  <main>{{ block "main" . }}{{ end }}</main>
  {{ block "footer" . }}{{ partial "footer.html" . }}{{ end }}
  {{ block "scripts" . }}{{ end }}
</body>
</html>
```

### Step-by-Step: Bootstrap a New Theme

```bash
# 1. Create the theme directory
mkdir -p themes/my-theme/{layouts/{_default,_markup,partials,shortcodes},assets/{scss,css,js}}

# 2. Create baseof.html (use the template above) defining blocks:
#    title, styles, header, main, footer, scripts

# 3. Create partials for reusable components
#    layouts/partials/header.html, footer.html, css.html

# 4. Set up your asset pipeline
#    - SCSS  → assets/scss/main.scss + toCSS partial
#    - Tailwind  → assets/css/main.css + css.TailwindCSS partial
#    - JS  → assets/js/main.js + js.Build

# 5. Configure hugo.yaml
#    theme: my-theme
#    See the reference file for your chosen CSS approach.

# 6. Build and verify
hugo --gc
ls public/ | head
```

> **Tip:** Project-level `layouts/` overrides theme `layouts/`. If you want to test your theme in isolation, keep the project `layouts/` directory empty until you need overrides.

## Common Pitfalls

- **SCSS requires Hugo extended edition.** The default macOS/Homebrew Hugo build is NOT extended. Verify with `hugo version | grep extended`.
- **Tailwind v4 uses `css.TailwindCSS`, not PostCSS.** Don't install `postcss-cli` for v4 — use the native pipe directly. Tailwind v3 still needs the PostCSS pipeline.
- **`partialCached` stale with non-constant args.** Variant strings (`.Section`, `page.RelPermalink`) must be unique per caller. Repeated section names produce stale results.
- **`hugo new` respects archetype directory structure.** Place archetypes at `archetypes/<section>/index.md` to create page bundles instead of flat files.
- **`resources.Get` looks in `assets/`, not `static/`.** Files in `static/` are copied verbatim and not processed by Hugo Pipes. Use `assets/` for any file that goes through Pipes.
- **Content adapter templates MUST use `_content.gotmpl` naming.** Regular `.md` files in the same directory are ignored when a `_content.gotmpl` exists.
- **Render hook templates go in `_markup/` subdirectories.** Not in `_default/` directly — they need `layouts/_default/_markup/render-link.html` or section-specific `layouts/<type>/_markup/`.
- **`block` in partials conflicts with `define` in page templates.** `{{ block "title" . }}` inside a partial (e.g. `head.html`) uses the same Go template namespace as `{{ define "title" }}` in page templates (e.g. `single.html`). When both exist in the render tree, Hugo errors with `multiple definition of template "title"`. Fix: use direct page variables (`.Title`, `.Site.Title`) in partials instead of `block`. Reserve `block` exclusively for the `baseof.html` shell.
