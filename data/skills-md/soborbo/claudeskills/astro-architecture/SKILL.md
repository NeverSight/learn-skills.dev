---
name: astro-architecture
description: Technical architecture for Astro lead generation websites. Use when setting up new projects, configuring build tools, or establishing project foundations. For images use astro-images skill. For SEO use astro-seo skill.
---

# Astro Architecture Skill

Technical foundation for high-performance, accessible, translation-ready lead gen sites.

## Core Rules (Non-Negotiable)

1. **Astro static or hybrid only** — No SPA routing, no client-side frameworks
2. **TypeScript strict mode** — Always enabled, no `any`
3. **All text from i18n** — No hardcoded strings in components
4. **Mobile-first CSS** — Base styles for mobile, `md:` and up for larger
5. **Performance is build-time** — No runtime optimization hacks
6. **One source of truth** — All site data in `site.ts`
7. **Skill boundaries** — Images via `astro-images`, SEO via `astro-seo`, forms via `astro-forms`

## Forbidden (STOP)

STOP and reassess if any of these occur:

- ❌ Client-side routing framework (React Router, etc.)
- ❌ UI component library (shadcn, DaisyUI, Chakra)
- ❌ Inline business logic in `<script>` tags
- ❌ Hardcoded translations in components
- ❌ Images not using `astro-images` skill
- ❌ SEO markup not using `astro-seo` skill
- ❌ Missing required pages (404, Privacy Policy)
- ❌ `client:load` without explicit justification
- ❌ External fonts via Google Fonts API (self-host instead)
- ❌ PageSpeed score below 90

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Astro (latest stable) |
| Styling | Tailwind CSS (latest stable) |
| Language | TypeScript (strict) |
| Deploy | Cloudflare Pages |
| Forms | `astro-forms` skill |
| Calculator | `lead-gen-calculator` skill |
| Images | `astro-images` skill |
| SEO | `astro-seo` skill |
| UX | `astro-ux` skill |

## Performance Targets

| Metric | Target | FAIL if |
|--------|--------|---------|
| PageSpeed (mobile) | ≥ 95 | < 90 |
| PageSpeed (desktop) | ≥ 95 | < 90 |
| Load time (desktop) | < 0.8s | > 1.5s |
| Load time (mobile) | < 1.4s | > 1.9s |
| LCP | < 1.5s | > 3s |
| CLS | < 0.1 | > 0.25 |
| Total JS | < 50KB | > 100KB |

## Browser Compatibility

Must work on:
- Chrome, Firefox, Safari, Edge, Opera, Brave
- iOS Safari (all versions), Android Chrome, Samsung Internet
- **Old devices:** iOS 12+, Android 7+

FAIL if site breaks on any of these.

## File Structure

```
src/
├── config/
│   └── site.ts              # ALL site data
├── i18n/
│   ├── ui.ts                # UI strings
│   ├── en.json              # English
│   └── [lang].json          # Other languages
├── layouts/
│   ├── BaseLayout.astro     # HTML shell
│   └── LandingLayout.astro
├── pages/
│   ├── index.astro
│   ├── thank-you.astro
│   ├── privacy-policy.astro # REQUIRED
│   ├── 404.astro            # REQUIRED
│   ├── 410.astro            # REQUIRED
│   └── [lang]/              # Translated pages
│       └── index.astro
├── components/
│   ├── sections/            # From astro-ux
│   ├── ui/
│   ├── layout/
│   │   ├── Header.astro
│   │   ├── Footer.astro     # Must have business data
│   │   └── MobileMenu.astro
│   └── common/
│       └── LanguageSwitcher.astro
├── actions/                 # From astro-forms
├── lib/
│   ├── i18n.ts              # Translation helpers
│   └── gtm.ts               # GTM/GA4 helpers
├── styles/
│   └── global.css
└── assets/
    ├── fonts/               # Self-hosted fonts
    └── images/
```

## Central Config

```typescript
// src/config/site.ts
export const site = {
  name: "Business Name",
  phone: "+44 XXX XXX XXXX",
  email: "info@example.com",
  address: "123 Street, City, Postcode",
  
  colors: {
    primary: "#1C202F",
    secondary: "#E5F2FF",
    accent: "#FF6B35",
  },
  
  defaultLocale: 'en',
  locales: ['en', 'hu', 'es'] as const,
  
  gtm: {
    id: "GTM-XXXXXXX",
    cookieYesId: "XXXXXXXX",
  },
  
  social: {
    google: { rating: 4.9, count: 270 },
  },
};
```

## References

### Required (Always Read)

- [pages.md](references/pages.md) — 404, 410, Privacy Policy (MUST exist)
- [a11y.md](references/a11y.md) — Accessibility requirements
- [config.md](references/config.md) — Config file templates

### Required if Multi-Language

- [i18n.md](references/i18n.md) — Translation setup, hreflang

### Conditional

- [gtm.md](references/gtm.md) — Only if GTM/GA4 tracking enabled
- [fonts.md](references/fonts.md) — Only if custom fonts used

## Definition of Done

Architecture is complete when ALL are true:

- [ ] All pages render without JavaScript enabled
- [ ] PageSpeed ≥ 90 on both mobile and desktop
- [ ] No CLS on page load (test with throttled connection)
- [ ] All visible text comes from i18n dictionaries
- [ ] Required pages exist: 404, Privacy Policy
- [ ] Footer contains business data (name, address, phone, email)
- [ ] hreflang tags present if multi-language
- [ ] GTM fires correctly (test in GTM Preview)
- [ ] Cookie consent blocks tracking until accepted
- [ ] Site works on iOS Safari and Android Chrome
- [ ] Keyboard navigation works throughout
- [ ] Skip link present and functional
