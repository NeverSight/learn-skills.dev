---
name: nuxt-seo-best-practices
description: Nuxt SEO optimization guidelines for Cloudflare-deployed applications. Covers dynamic OG image generation on CF Workers, page SEO composables, JSON-LD structured data, SSR externals, and Nitro configuration. Triggers on tasks involving SEO, meta tags, OG images, Open Graph, Satori, social sharing, or Cloudflare Workers deployment.
license: MIT
metadata:
  author: vinayakkulkarni
  version: "1.0.0"
---

# Nuxt SEO Best Practices

Comprehensive SEO optimization guide for Nuxt 4 applications deployed to Cloudflare Pages/Workers. Contains 11 rules across 4 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Generating dynamic OG images on Cloudflare Workers
- Setting up page-level SEO meta tags and composables
- Adding JSON-LD structured data
- Configuring Nitro for Cloudflare Pages deployment
- Handling SSR-incompatible client-only libraries
- Setting up social sharing meta (Open Graph, Twitter Cards)
- Working with Satori for image generation (NEVER use React)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | OG Image Generation | CRITICAL | `og-` |
| 2 | Page SEO & Meta | HIGH | `meta-` |
| 3 | Structured Data | MEDIUM | `schema-` |
| 4 | Cloudflare & Nitro Config | HIGH | `cf-` |

## Quick Reference

### 1. OG Image Generation (CRITICAL)

- `og-cf-workers` - Generate dynamic OG images on Cloudflare Workers with @cf-wasm/og
- `og-no-react` - Use plain JS objects for Satori elements, NEVER React
- `og-cache-headers` - Cache OG images with immutable headers for CDN

### 2. Page SEO & Meta (HIGH)

- `meta-use-page-seo` - Reusable composable for consistent page-level SEO
- `meta-social-tags` - Proper Open Graph and Twitter Card meta tags
- `meta-canonical-url` - Canonical URLs and og:url for every page

### 3. Structured Data (MEDIUM)

- `schema-json-ld` - JSON-LD structured data in app.vue for Google Rich Results

### 4. Cloudflare & Nitro Config (HIGH)

- `cf-compatibility-date` - Pin compatibilityDate, never use 'latest'
- `cf-nitro-config` - Nitro config for CF Pages (nodeCompat, process.stdout, WASM)
- `cf-ssr-externals` - SSR external config for client-only libraries
- `cf-wasm-import` - WASM module configuration for Cloudflare Workers

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/og-cf-workers.md
rules/meta-use-page-seo.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and Nuxt/Cloudflare-specific notes

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
