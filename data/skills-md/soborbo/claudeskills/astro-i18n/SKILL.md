---
name: astro-i18n
description: Internationalization patterns for Astro sites. Multi-language routing, content translation, locale switching, RTL support. Use for multi-market lead generation.
---

# Astro i18n Skill

## Purpose

Provides internationalization patterns for lead generation sites targeting multiple markets/languages. Implements URL-based routing (`/en/`, `/de/`, `/fr/`), translation management, SEO optimization with hreflang tags, and RTL support.

## Core Rules

1. **URL structure first** — `/en/`, `/de/`, `/fr/` prefixes for SEO and user clarity
2. **Fallback gracefully** — Missing translations default to primary language with console warning
3. **hreflang tags** — Required on every page for proper language alternates
4. **RTL support** — Use logical CSS properties (margin-inline-start) for Arabic/Hebrew
5. **Persist preference** — Store user's language choice in localStorage/cookie
6. **Type-safe translations** — Use TypeScript for language codes and translation keys
7. **No hardcoded text** — All user-facing strings must come from translation files
8. **SEO metadata** — Translate title, description, og:locale for each language
9. **Content parity** — Each language should have equivalent content structure
10. **Intl API formatting** — Use native Intl for dates, numbers, currency per locale

## Implementation Overview

| Component | Purpose | Location |
|-----------|---------|----------|
| `languages` config | Define supported locales + metadata | `src/i18n/config.ts` |
| Translation files | JSON with nested keys | `src/i18n/translations/{lang}.json` |
| `t()` function | Translation with fallback + params | `src/i18n/utils.ts` |
| `[lang]/` routes | Dynamic URL segments | `src/pages/[lang]/` |
| Language switcher | Dropdown component | Component in layout |
| hreflang tags | SEO language alternates | `<head>` in BaseLayout |
| Middleware | Optional browser detection | `src/middleware.ts` |

## Quick Start

### Minimal Config

```typescript
// src/i18n/config.ts
export const languages = {
  en: { name: 'English', code: 'en-GB', dir: 'ltr' },
  de: { name: 'Deutsch', code: 'de-DE', dir: 'ltr' },
} as const;
export const defaultLang = 'en';
export type Lang = keyof typeof languages;
```

### Translation Usage

```astro
---
import { t } from '@/i18n/utils';
const lang = getLangFromUrl(Astro.url);
---
<h1>{t(lang, 'hero.title')}</h1>
<p>{t(lang, 'hero.subtitle')}</p>
<button>{t(lang, 'hero.cta')}</button>
```

### Dynamic Route

```astro
---
// src/pages/[lang]/index.astro
export function getStaticPaths() {
  return Object.keys(languages).map(lang => ({ params: { lang } }));
}
---
```

## References

**Configuration & Setup:**
- [config.md](./references/config.md) - Language config, translation files, utilities

**Routing & URLs:**
- [routing.md](./references/routing.md) - Dynamic routes, redirects, middleware

**Components:**
- [components.md](./references/components.md) - Base layout, language switcher

**Content & Collections:**
- [content-collections.md](./references/content-collections.md) - Multi-language blog posts

**Formatting:**
- [formatters.md](./references/formatters.md) - Numbers, dates, currency per locale

**RTL Support:**
- [rtl-support.md](./references/rtl-support.md) - Arabic/Hebrew layout support

**SEO:**
- [seo.md](./references/seo.md) - hreflang, Open Graph, sitemaps

## Forbidden

- ❌ Hardcoded text in components (use `t()` function)
- ❌ Missing hreflang tags on pages
- ❌ Auto-translating without human review
- ❌ Different URLs for same content without hreflang links
- ❌ Ignoring RTL requirements for Arabic/Hebrew
- ❌ Locale in query params (`?lang=de`) instead of path (`/de/`)
- ❌ Using left/right CSS instead of logical properties
- ❌ Forgetting to translate meta descriptions and titles

## Definition of Done

- [ ] Language config with all supported locales defined
- [ ] Translation JSON files for each language with complete key coverage
- [ ] `t()` utility function with fallback to default language
- [ ] URL-based language routing using `[lang]/` dynamic segments
- [ ] hreflang tags on all pages pointing to language alternates
- [ ] Language switcher component in navigation
- [ ] Root `/` redirects to default language
- [ ] Browser language detection (optional, via middleware)
- [ ] RTL support implemented if targeting Arabic/Hebrew
- [ ] Date/number/currency formatting per locale using Intl API
- [ ] Content collections with language-specific entries
- [ ] All user-facing text extracted to translation files
- [ ] SEO meta tags translated (title, description, og:locale)
