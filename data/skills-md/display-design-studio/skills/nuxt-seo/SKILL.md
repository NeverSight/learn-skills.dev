---
name: nuxt-seo
description: >-
  Full @nuxtjs/seo suite best practices for Nuxt 3 — covers @nuxtjs/sitemap,
  nuxt-og-image, nuxt-schema-org, nuxt-seo-utils, nuxt-link-checker,
  @nuxtjs/robots, useSeoMeta, useHead, breadcrumbs, canonical URLs, favicon,
  og:image, structured data, and llms.txt. Use when the user mentions sitemap,
  og image, schema.org, useSeoMeta, useHead, breadcrumbs, canonical, link
  checker, robots.txt, noindex, blockAiBots, llms.txt, or any @nuxtjs/seo
  module in a Nuxt project.
---

# Nuxt SEO — Full Suite

Best-practices guide for the `@nuxtjs/seo` meta-package and all six modules:
`@nuxtjs/sitemap`, `nuxt-og-image`, `nuxt-schema-org`, `nuxt-seo-utils`,
`nuxt-link-checker`, and `@nuxtjs/robots`.

> Also load the `nuxt` skill for Nuxt core patterns.

## ROUTING: Which rule file to load

**IF installing @nuxtjs/seo or configuring shared site.url / site.name:**
→ Read `rules/core-site-config.md`

**IF working with useHead, useSeoMeta, titleTemplate, or global meta defaults:**
→ Read `rules/core-meta-tags.md`

**IF setting up @nuxtjs/robots or configuring robots.txt for the first time:**
→ Read `rules/core-robots-setup.md`

**IF generating or customizing a sitemap.xml:**
→ Read `rules/features-sitemap.md`

**IF generating Open Graph images (og:image) dynamically:**
→ Read `rules/features-og-image.md`

**IF adding structured data / JSON-LD / Schema.org to pages:**
→ Read `rules/features-schema-org.md`

**IF working with breadcrumbs, canonical URLs, favicon, or automatic OG tags:**
→ Read `rules/features-seo-utils.md`

**IF checking for broken links in dev or CI:**
→ Read `rules/features-link-checker.md`

**IF controlling crawling per page, route, or dynamically at runtime:**
→ Read `rules/features-page-control.md`

**IF adding or referencing llms.txt for AI tool documentation access:**
→ Read `rules/features-llms-txt.md`

## Rule index

| Topic | Description | File |
|-------|-------------|------|
| Sections overview | Categories and reading order | [rules/_sections.md](rules/_sections.md) |
| Site config | @nuxtjs/seo install, shared site.url/name/description, env config | [rules/core-site-config.md](rules/core-site-config.md) |
| Meta tags | useSeoMeta, useHead, app.head defaults, titleTemplate | [rules/core-meta-tags.md](rules/core-meta-tags.md) |
| Robots setup | Installation, nuxt.config.ts, disallow, blockNonSeoBots, blockAiBots | [rules/core-robots-setup.md](rules/core-robots-setup.md) |
| Sitemap | Auto-generation, dynamic URLs, i18n, multi-sitemap, debug | [rules/features-sitemap.md](rules/features-sitemap.md) |
| OG Image | nuxt-og-image, templates, renderers, prerendering | [rules/features-og-image.md](rules/features-og-image.md) |
| Schema.org | nuxt-schema-org, identity, useSchemaOrg, schema types | [rules/features-schema-org.md](rules/features-schema-org.md) |
| SEO Utils | Breadcrumbs, canonical, favicon, automatic OG tags | [rules/features-seo-utils.md](rules/features-seo-utils.md) |
| Link Checker | Dev/CI broken link detection, rules, reporting, exclusions | [rules/features-link-checker.md](rules/features-link-checker.md) |
| Page control | definePageMeta robots, route rules, useRobotsRule, X-Robots-Tag | [rules/features-page-control.md](rules/features-page-control.md) |
| llms.txt | Standard, manual public/ file, nuxtseo.com docs for AI tools | [rules/features-llms-txt.md](rules/features-llms-txt.md) |

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Suite setup & shared config | CRITICAL | `core-` |
| 1 | Meta tags & head management | CRITICAL | `core-` |
| 1 | Robots module setup | CRITICAL | `core-` |
| 2 | Sitemap generation | HIGH | `features-` |
| 2 | OG Image generation | HIGH | `features-` |
| 2 | Schema.org / structured data | HIGH | `features-` |
| 2 | SEO utils (breadcrumbs, canonical) | HIGH | `features-` |
| 3 | Link checker | MEDIUM | `features-` |
| 3 | Per-page crawl control | MEDIUM | `features-` |
| 3 | llms.txt | LOW | `features-` |

## Coverage and maintenance

- Coverage map: `rules/_coverage-map.md`
- Suite source: https://github.com/harlan-zw/nuxt-seo
- Docs: https://nuxtseo.com
- Update when `@nuxtjs/seo` releases a new major version.
