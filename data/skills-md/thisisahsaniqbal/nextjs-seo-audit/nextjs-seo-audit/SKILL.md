---
name: nextjs-seo-audit
description: >
  Comprehensive SEO audit skill for Next.js and HTML pages. Covers on-page optimisation,
  JSON-LD schema validation, meta tags, Open Graph, semantic HTML, site speed, mobile
  responsiveness, and backlink analysis. Use when a user asks to audit, optimise, or fix
  SEO issues on a webpage or website.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# nextjs-seo-audit

A comprehensive SEO audit skill that teaches you how to analyse HTML pages and provide actionable recommendations across 10 skill areas.

## When to activate

Use this skill when the user asks you to:

- Run an SEO audit on a page, component, or full website
- Fix specific SEO issues (headings, meta tags, schema, speed, etc.)
- Optimise a Next.js or HTML page for search engines
- Validate structured data (JSON-LD), Open Graph, or Twitter Cards
- Check page performance, semantic HTML, or mobile-friendliness
- Analyse outbound links or backlink strategy

## How to run a full audit

When performing a full SEO audit, run **all 10 sub-skills** in order on the provided HTML. Read each sub-skill's `SKILL.md` for the detailed checklist:

| # | Skill | SKILL.md | Focus area |
|---|---|---|---|
| 1 | On-Page Optimization | [skills/onpage-optimization/SKILL.md](skills/onpage-optimization/SKILL.md) | Headings, keywords, internal links |
| 2 | Schema JSON Optimization | [skills/schema-json-optimization/SKILL.md](skills/schema-json-optimization/SKILL.md) | JSON-LD structured data |
| 3 | Meta Data Optimization | [skills/meta-data-optimization/SKILL.md](skills/meta-data-optimization/SKILL.md) | Title, description, OG, Twitter Cards |
| 4 | Semantic Layout | [skills/semantic-layout/SKILL.md](skills/semantic-layout/SKILL.md) | HTML5 semantic elements, accessibility |
| 5 | Site Speed Optimization | [skills/site-speed-optimization/SKILL.md](skills/site-speed-optimization/SKILL.md) | Scripts, stylesheets, images |
| 6 | Mobile Optimization | [skills/mobile-optimization/SKILL.md](skills/mobile-optimization/SKILL.md) | Viewport, responsive design, touch targets |
| 7 | Backlink Monitoring | [skills/backlink-monitoring/SKILL.md](skills/backlink-monitoring/SKILL.md) | External links, dofollow/nofollow strategy |
| 8 | International SEO | [skills/international-seo/SKILL.md](skills/international-seo/SKILL.md) | Hreflang, multi-language, regional targeting |
| 9 | Technical SEO | [skills/technical-seo/SKILL.md](skills/technical-seo/SKILL.md) | Sitemap, robots.txt, canonical, crawlability |
| 10 | Core Web Vitals | [skills/core-web-vitals/SKILL.md](skills/core-web-vitals/SKILL.md) | LCP, CLS, INP, performance scoring |

## Output format

For each check, report:

- **Status**: `✅ PASS`, `⚠️ WARN`, or `❌ FAIL`
- **Message**: Clear, actionable description of the finding

At the end, provide a summary:

```
SEO Audit Summary
─────────────────
✅ Pass:  X
⚠️ Warn:  Y
❌ Fail:  Z
──────────────
Score: XX%
```

## Global thresholds reference

These thresholds are used across all sub-skills:

| Parameter | Value |
|---|---|
| Title length | 30–60 characters |
| Meta description length | 120–160 characters |
| Keyword density (ideal) | 1.0–3.0% |
| Internal links (min per page) | 3 |
| Max fixed-width before warning | 500px |
| Min touch target size | 48px × 48px |
| Max inline CSS length | 5000 characters |
| Max external scripts | 10 |
| Required OG tags | `og:title`, `og:description`, `og:image`, `og:url`, `og:type` |
| Required Twitter Card tags | `twitter:card`, `twitter:title`, `twitter:description` |
| Required semantic elements | `header`, `main`, `footer`, `nav` |
| Recommended semantic elements | `article`, `section`, `aside`, `figure` |
