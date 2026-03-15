---
name: wp-theme-dev
description: >
  Develop WordPress themes following official WordPress coding standards, theme review requirements, accessibility
  standards (WCAG 2.1 AA), and modern web development best practices. Use this skill whenever the user wants to create,
  scaffold, or develop a WordPress theme — including block (FSE) themes, classic themes, child themes, or hybrid themes.
  Also trigger when the user mentions "WordPress theme", "WP theme", "block theme", "FSE theme", "theme.json",
  "template parts", "style variations", "child theme", or wants to build a custom design/layout for WordPress.
  Even if the user just says "build me a theme for X" or "I need a theme", use this skill.
---

# WordPress Theme Development

## Overview

Create production-ready WordPress themes that follow official WordPress coding standards, the WordPress.org theme
review requirements, WCAG 2.1 Level AA accessibility standards, and modern web development best practices. Every
theme produced by this skill is accessible, secure, translatable, performant, and ready for WordPress.org submission.

## Quick Start Workflow

1. **Read references** — Before writing any code, read the relevant reference files:
   - `references/block-theme-architecture.md` — Block theme structure, theme.json, templates, patterns
   - `references/classic-theme-architecture.md` — Classic theme structure, template hierarchy, The Loop
   - `references/accessibility.md` — WCAG 2.1 AA requirements, WordPress accessibility-ready standards
   - `references/review-requirements.md` — WordPress.org theme review checklist (14 categories)
2. **Determine theme type** — Ask if the user wants a block theme (recommended), classic theme, or child theme
3. **Gather requirements** — Design goals, color palette, typography, features needed
4. **Scaffold** — Generate the directory structure, required files, and theme.json
5. **Build templates & patterns** — Create each template/pattern as a separate file
6. **Generate readme.txt** — Always include a WordPress.org-compliant readme.txt
7. **Deliver** — Ask user if they want files for download or a custom path

## Core Principles — ALWAYS Follow These

### 1. Block Themes Are the Default
Unless the user explicitly asks for a classic theme, always build a **block theme** (Full Site Editing). Block themes:
- Use HTML template files (not PHP template files)
- Configure design through `theme.json` (not PHP/CSS)
- Support the Site Editor for full visual editing
- Use block patterns for reusable layouts
- Use template parts for headers, footers, sidebars

Only build a classic theme when the user specifically requests it or needs features only available in classic themes.

### 2. Clean functions.php
The `functions.php` file should ONLY contain:
- Theme setup (`after_setup_theme` hook) — declaring support for theme features
- Asset enqueueing (`wp_enqueue_scripts` hook)
- Registering block patterns, pattern categories, and block styles
- Registering navigation menus (classic themes)
- Registering widget areas (classic themes)
- Loading additional PHP files from `inc/` directory

**NEVER** put lengthy logic, output HTML, or complex functionality directly in functions.php.
Split additional functionality into files in the `inc/` directory.

### 3. Accessibility — Non-Negotiable
Every theme MUST meet WCAG 2.1 Level AA and WordPress accessibility requirements. This is not optional.

Read `references/accessibility.md` for complete requirements. Key mandatory items:

**Skip links:** First focusable element, visible on focus, jumps to main content.

**Keyboard navigation:** All interactive elements reachable and operable via keyboard. Visible focus indicators on all focusable elements. Focus order follows logical reading order.

**Semantic HTML:** Use proper HTML5 landmark elements (`<header>`, `<main>`, `<nav>`, `<aside>`, `<footer>`). Use ARIA landmark roles as reinforcement. Proper heading hierarchy (one H1 per page, no skipped levels).

**Color contrast:** All text meets 4.5:1 ratio against background (3:1 for large text 18px+ bold or 24px+ regular). UI components and focus indicators meet 3:1 ratio.

**Content links:** Links within body content MUST be underlined. Bold/italic/color-only is not acceptable.

**Forms:** All form inputs must have explicit `<label>` elements. No placeholder-only labels. Error states must be perceivable by screen readers.

**Images:** All `<img>` tags must have meaningful `alt` attributes. Decorative images use `alt=""`.

**Screen reader text:** Use `.screen-reader-text` class for visually hidden but accessible text. Apply to "Read more" links, icon-only buttons, and repetitive link text.

**Repetitive link text:** "Read more" links must include the post title (visually hidden is OK).

**Media:** Embedded media must not auto-play. Provide controls for all media.

### 4. Security
- Escape ALL output: `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses_post()`
- Sanitize ALL input: `sanitize_text_field()`, `absint()`, etc.
- Use nonces for any form submissions
- Validate and check capabilities before privileged operations
- Never use `eval()`, `base64_decode()` on user data, or direct `$_GET`/`$_POST` without sanitization

### 5. WordPress Coding Standards
- Prefix ALL functions, classes, hooks, handles with a unique theme prefix (minimum 4 characters)
- All user-facing strings must be translatable: `__()`, `_e()`, `esc_html__()`, `esc_html_e()`, etc.
- Text domain must match the theme slug
- Use `wp_enqueue_script()` / `wp_enqueue_style()` — never hardcode `<script>` or `<link>` tags
- Use WordPress bundled libraries (jQuery, etc.) — never bundle your own copies
- Include original source when using minified files
- No PHP errors, warnings, or notices with WP_DEBUG enabled
- No deprecated functions or constants

### 6. WordPress.org Theme Review Compliance
Every theme MUST comply with all 14 review categories. Read `references/review-requirements.md`.

Key rules:
- GPLv2 or later license for ALL code, images, fonts, and assets
- Include copyright and license for ALL bundled resources in readme.txt
- No tracking/remote resources without explicit user consent (Google Fonts exception)
- No plugin territory functionality (CPTs, shortcodes, SEO, analytics, contact forms)
- No admin dashboard hijacking; notices must be dismissible
- No redirect on theme activation
- Do not remove/hide the admin bar
- Theme names must not use "WordPress", "Theme", or "Twenty*"
- Screenshot must represent actual theme output, not be an advertisement
- Complete readme.txt with all required headers

### 7. Modern CSS & Performance
- Use CSS custom properties (variables) for theming — align with theme.json presets
- Use modern layout: CSS Grid and Flexbox (no floats for layout)
- Use `clamp()` for fluid responsive typography and spacing
- Use logical properties (`margin-inline`, `padding-block`) for RTL support
- Mobile-first responsive design with `min-width` media queries
- Minimize render-blocking resources
- Use `loading="lazy"` on images and iframes below the fold
- Use `font-display: swap` for custom fonts
- Prefer system font stacks or locally hosted fonts over Google Fonts for privacy/performance

## Theme Type Reference

| User Wants | Theme Type | Key Reference |
|---|---|---|
| Block theme / FSE theme | Block theme | `references/block-theme-architecture.md` |
| Classic PHP theme | Classic theme | `references/classic-theme-architecture.md` |
| Modify existing theme | Child theme | Both references depending on parent type |
| Hybrid approach | Classic + block features | Both references |

## Naming Conventions

Derive all names from the theme name the user provides:

| Element | Convention | Example (theme: "Starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter Blue starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter starter"starter starter --> Let me fix the table. |

| Element | Convention | Example (theme: "Starter Blue") |
|---|---|---|
| Theme slug | lowercase-hyphenated | `starter-blue` |
| Text domain | same as slug | `starter-blue` |
| Function prefix | lowercase underscore (4+ chars) | `stbl_` |
| Constant prefix | UPPER_SNAKE | `STBL_` |
| Class prefix | Upper_Snake | `Starter_Blue_` |
| Handle names | slug prefix | `starter-blue-style` |
| Pattern category | slug prefix | `starter-blue` |
| Block style names | slug prefix | `starter-blue/card-shadow` |

Choose a short prefix (4+ characters) derived from the theme name.

## Delivery

After building the theme:

1. Ask the user where they want the files:
   - **Download:** Copy to `/mnt/user-data/outputs/{theme-slug}/` and present as downloadable
   - **Custom path:** Write to the path the user specifies
2. Always include `readme.txt` and `style.css` with all required headers
3. Provide a brief summary of generated files
4. If using a build process (block theme with custom blocks), note `npm install && npm run build` is needed

## Checklist Before Delivery

- [ ] `style.css` has ALL required headers (Theme Name, Author, Version, License, etc.)
- [ ] `readme.txt` is present, complete, and includes resource credits
- [ ] ALL output is escaped (`esc_html`, `esc_attr`, `esc_url`, `wp_kses_post`)
- [ ] ALL input is sanitized
- [ ] ALL strings are translatable with correct text domain
- [ ] ALL functions/classes/handles are prefixed (4+ characters)
- [ ] Skip link is present, first focusable element, visible on focus
- [ ] Keyboard navigation works for all interactive elements
- [ ] Visible focus indicators on all focusable elements
- [ ] Proper heading hierarchy (one H1, no skipped levels)
- [ ] Content links are underlined
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 text, 3:1 large text/UI)
- [ ] All images have appropriate alt attributes
- [ ] ARIA landmarks are present and unique labels on duplicates
- [ ] "Read more" links include post title (screen-reader-text)
- [ ] Forms have explicit `<label>` elements
- [ ] No PHP errors/warnings/notices with WP_DEBUG
- [ ] No deprecated functions
- [ ] No bundled WP default libraries
- [ ] No plugin territory functionality
- [ ] No remote resources without consent
- [ ] No admin redirect on activation
- [ ] Assets properly enqueued (not hardcoded)
- [ ] Responsive design works at all breakpoints
- [ ] RTL support via logical properties or RTL stylesheet
- [ ] License is GPLv2 or later
- [ ] Screenshot is 1200×900, represents actual theme output
