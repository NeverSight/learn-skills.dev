---
name: localization-engineer
description: |
  Framework-agnostic internationalization (i18n) and localization (l10n) patterns for multilingual applications. Covers ICU message format, pluralization rules (CLDR), RTL layout with CSS logical properties, locale negotiation and detection strategies, SEO hreflang tags, cookie/header-based locale resolution, and translation workflow management.

  Use when adding multi-language support, choosing an i18n library, implementing pluralization or gender-aware messages, formatting dates/numbers/currencies by locale, handling RTL layouts, setting up locale detection, configuring hreflang SEO tags, or managing translation workflows.
license: MIT
metadata:
  author: oakoss
  version: '2.0'
---

# Localization Engineer

## Overview

Provides framework-agnostic patterns for building multilingual applications, covering the full i18n pipeline from locale detection through translation rendering. Addresses universal concerns like ICU message formatting, CLDR plural rules, RTL support, and SEO.

**When to use:** Adding multi-language support, locale-aware formatting, RTL layouts, pluralization, translation management, locale negotiation, multilingual SEO.

**When NOT to use:** Single-language apps with no internationalization plans, content that never changes locale, purely server-rendered static sites with no dynamic content.

**Key decision:** Choose Paraglide for compile-time type safety and minimal bundles in new projects. Choose i18next for broad ecosystem support and incremental adoption in existing projects. See the Library Selection table below.

## Library Selection

| Criteria          | Paraglide JS                                            | i18next                                           |
| ----------------- | ------------------------------------------------------- | ------------------------------------------------- |
| Architecture      | Compile-time, tree-shakable functions                   | Runtime, plugin-based ecosystem                   |
| Type safety       | Full (generated typed message functions)                | Partial (requires manual type setup)              |
| Bundle size       | Minimal (only used messages shipped)                    | Larger runtime (~40 kB base + plugins)            |
| Pluralization     | Via message format plugins                              | Built-in with CLDR plural categories              |
| Framework support | SvelteKit, TanStack Start, React Router, Astro, vanilla | React, Vue, Svelte, Angular, Node, vanilla        |
| ICU support       | Via `inlang-icu-messageformat-1` plugin                 | Via `i18next-icu` plugin                          |
| Translation tools | Fink editor, Sherlock VS Code extension                 | Locize, i18next-parser, many integrations         |
| Locale strategies | Built-in (cookie, URL, header, custom)                  | Via `i18next-browser-languagedetector` plugin     |
| SSR support       | AsyncLocalStorage-based per-request                     | Separate i18next instance per request             |
| Learning curve    | Low (compiler generates simple functions)               | Medium (large API surface, many plugins)          |
| Namespace support | Flat message files per locale                           | Multi-namespace with lazy loading per route       |
| Message format    | Inlang format or ICU via plugin                         | i18next JSON v4 or ICU via plugin                 |
| Community size    | Growing (inlang ecosystem)                              | Large (established since 2015)                    |
| Best for          | New projects prioritizing bundle size and type safety   | Existing projects needing broad ecosystem support |

## Quick Reference

| Pattern             | Approach                                                 | Key Points                                               |
| ------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| ICU pluralization   | `{count, plural, one {# item} other {# items}}`          | CLDR categories: zero, one, two, few, many, other        |
| ICU select (gender) | `{gender, select, male {He} female {She} other {They}}`  | Covers gender-aware and variant-based messages           |
| ICU selectordinal   | `{rank, selectordinal, one {#st} two {#nd} other {#th}}` | Ordinal suffixes vary by language                        |
| Number formatting   | `Intl.NumberFormat(locale, options)`                     | Currency, percent, unit formatting built into platform   |
| Date formatting     | `Intl.DateTimeFormat(locale, options)`                   | Avoid manual date string construction                    |
| Relative time       | `Intl.RelativeTimeFormat(locale, options)`               | "3 hours ago", "in 2 days" with locale-aware output      |
| List formatting     | `Intl.ListFormat(locale, { type: 'conjunction' })`       | "Alice, Bob, and Charlie" with locale-aware conjunctions |
| RTL layout          | CSS logical properties (`inline-start`, `inline-end`)    | Replace `left`/`right` with logical equivalents          |
| RTL detection       | `<html dir="rtl" lang="ar">`                             | Set `dir` attribute based on locale                      |
| Locale from URL     | `/en/about`, `/de/about`                                 | Most SEO-friendly, clear to users                        |
| Locale from cookie  | `locale=de` cookie                                       | Persists preference across sessions                      |
| Locale from header  | `Accept-Language: de-DE,de;q=0.9,en;q=0.8`               | Browser preference, use as fallback                      |
| Hreflang tags       | `<link rel="alternate" hreflang="de" href="...">`        | One per locale plus `x-default`                          |
| Namespace splitting | Group translations by feature or route                   | Reduces bundle size via lazy loading                     |
| Message extraction  | Automated tooling scans source for translation keys      | Prevents orphaned or missing translations                |
| Pseudolocalization  | Generate fake translations to test layout                | Catches truncation, overflow, hardcoded strings          |

## Common Mistakes

| Mistake                                           | Correct Pattern                                                             |
| ------------------------------------------------- | --------------------------------------------------------------------------- |
| Concatenating translated fragments into sentences | Use ICU message format with placeholders for proper grammar across locales  |
| Using `margin-left`/`padding-right` with RTL      | Use CSS logical properties (`margin-inline-start`, `padding-inline-end`)    |
| Hardcoding plural rules (`count === 1`)           | Use CLDR plural categories (some languages have zero, two, few, many forms) |
| Detecting locale only from IP geolocation         | Use `Accept-Language` header, then cookie, then geolocation as last resort  |
| Missing `x-default` in hreflang tags              | Always include `<link rel="alternate" hreflang="x-default">` for fallback   |
| One massive translation file per locale           | Split into namespaces by feature for lazy loading and maintainability       |
| Creating new i18next instance per component       | Create once at app initialization, share across components                  |
| Formatting dates with string concatenation        | Use `Intl.DateTimeFormat` for locale-aware date rendering                   |
| Storing locale in component state                 | Store in URL path or cookie for SSR compatibility and shareability          |
| Using different i18n keys in client and server    | Share translation files and key structure between client and server         |
| Assuming all languages expand equally             | Budget 30-40% extra space for German/Finnish translations vs English        |
| Embedding text in images                          | Use CSS/SVG text overlays so translations can be applied dynamically        |
| Using language codes without region variants      | Use `en-US` vs `en-GB` when formatting differences matter (dates, currency) |

## Delegation

- **Audit codebase for hardcoded strings**: Use `Explore` agent to scan components for untranslated user-facing text
- **Set up full i18n pipeline**: Use `Task` agent to configure locale detection, translation loading, and rendering
- **Plan localization architecture**: Use `Plan` agent to design namespace structure, locale strategy, and translation workflow
- **Review translation coverage**: Use `Task` agent to compare translation files and identify missing keys across locales
- **Code review for i18n compliance**: Delegate to `code-reviewer` agent

> If the `tanstack-start` skill is available, delegate server middleware and SSR locale patterns to it.
> If the `tanstack-router` skill is available, delegate URL-based locale routing patterns to it.
> If the `sveltekit` skill is available, delegate SvelteKit-specific routing and hooks patterns to it.
> If the `seo` skill is available, delegate advanced hreflang and sitemap patterns to it.

## References

- [Paraglide JS patterns](references/paraglide.md) -- compile-time i18n with typed message functions, SvelteKit/TanStack Start/React Router integration, locale strategies
- [i18next patterns](references/i18next.md) -- runtime i18n with plugin ecosystem, React/Vue/Svelte/vanilla integration, namespaces, language detection
- [ICU message format](references/icu-message-format.md) -- pluralization, select, number/date formatting, nested messages, RTL support, hreflang SEO
