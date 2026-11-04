---
name: bascik-seo
description: Search, social sharing, and AI discoverability for Bascik sites. Use when adding page titles, meta descriptions, canonical URLs, Open Graph or Twitter cards, JSON-LD structured data (Article, BreadcrumbList, Organization, FAQ), noindex, sitemap.xml, robots.txt, llms.txt, or social images; when fixing Lighthouse SEO findings or duplicate titles; or when generating meta tags for dynamic routes. Includes an SEO audit script for the built site.
license: MIT
metadata:
  author: bascik
  homepage: https://bascik.dev
---

# SEO, Social Cards, and Discoverability

Bascik outputs static HTML, so search engines and AI crawlers read every word without running JavaScript. The work is correct head tags on every page plus the files crawlers look for. Requires the `bascik` skill; `bascik-scripts` covers build scripts and dynamic routes.

## Every page needs

| Tag                                               | Rule                                                                                |
| ------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `<html lang>` and `<meta name="viewport">`        | On every page, usually from a shared head component                                 |
| `<title>`                                         | Unique, accurate, concise, and aligned with the visible page heading                |
| `<meta name="description">`                       | Unique, useful summary of the specific page; Google may select visible text instead |
| `<link rel="canonical">`                          | Absolute URL of this page, including the base, only when the site URL is known      |
| `og:title`, `og:description`, `og:url`, `og:type` | Social previews; an absolute `og:image` (1200x630) for a large card                 |
| One `<h1>`                                        | Matches the title's intent                                                          |

## Rules (must follow)

1. **Build tags in the context of the page that uses them.** A build script inside a component runs for each use, with that page's environment variables; no page-aware marker is needed.
2. **Never hard-code the domain.** URLs come from `BASCIK_SITE_URL` (CI variable or `.env`), `BASCIK_BASE`, and `BASCIK_PAGE_PATH`. `bascik --build` fails without the site URL because it writes the sitemap and robots.txt.
3. **Build head tags with `html` from `@bascik/bascik/html`**, which escapes every value you interpolate, and write JSON-LD as `` html`<script type="application/ld+json">${json(data)}</script>` ``: `json()` escapes `<`, `>` and `&` so data can never close the script tag. Never write an escaper of your own. Describe only what is visible on the page.
4. **Dynamic routes** read the item from `BASCIK_ROUTE` in the head build script and pass its fields to the tag helper.
5. **A noindex page also needs `<meta name="bascik-sitemap" content="exclude" />` written literally in its source.** Bascik reads the source file, not script output, to decide what `sitemap.xml` lists. 404 and 500 pages are excluded automatically.
6. **Keep authored `robots.txt` and `sitemap.xml` only for custom rules**, and turn off the matching `generate` flag. Otherwise let Bascik generate them.
7. **For branded search results and sitelinks, make the home page's identity and site hierarchy clear:** use a descriptive home-page title and heading, link to key pages from the home page and shared navigation, and use concise descriptive anchor text. Google chooses sitelinks and rankings automatically; no tag, JSON-LD, sitemap, or Bascik setting can require a particular result layout.
8. **Treat lengths as editorial targets, not Google rules.** The SEO audit warns outside its 10–65 title and 50–160 description ranges, but Google has no fixed character limit for either. Google may rewrite title links and generate query-specific snippets from visible page text; a meta description is only one possible snippet source.
9. **Keep site identity consistent.** For Google site-name guidance, use the same recognizable brand in the home page's visible content, title, and `og:site_name`. You may provide one `WebSite` structured-data item on the home page with the canonical home-page URL and site name; Google selects the displayed name automatically, and `alternateName` is optional.
10. **Use structured data only when it accurately describes visible page content and fits a Google-supported feature.** Follow the general and feature-specific policies, keep markup current and complete, and validate the deployed page. Valid markup can make a page eligible for a rich result, but never guarantees one or improves ordinary ranking by itself. A JavaScript-injected JSON-LD block can be processed after rendering; Bascik's build-time output avoids needing that client-side step.
11. **Do not promise a ranking or treat Preferred Sources as an SEO control.** Google uses many signals; no title, schema, sitemap, or domain name can guarantee first place. Preferred Sources is a separate feature for eligible publications and specific Search experiences, not a way to control ordinary rankings or sitelinks.

Copy a tested helper instead of writing one: `add-example.mjs starter-site/src/lib/seo.ts` gives `seo({ title, description, image, type, noindex, ... })`, `jsonLd()`, `breadcrumbList()`, and `article()`. `add-example.mjs starter-site/scripts/llms-txt.ts` adds a post-phase exec script that writes `llms.txt` from every indexable page's title and description; `bascik-refactor/scripts/llms-txt.mjs`, from the opt-in `bascik-refactor` skill (`npx skills add bascikdev/bascik --skill bascik-refactor`), does the same with sections per first path segment and canonical URLs.

## Audit the build

```sh
BASCIK_SITE_URL=https://example.com npx bascik --build
node <skills-dir>/bascik-seo/scripts/audit-seo.mjs            # reads the site URL from the environment or .env
node <skills-dir>/bascik-seo/scripts/audit-seo.mjs --strict   # fail on warnings too (CI)
```

- **error**: missing title, description, `lang`, or viewport; invalid JSON-LD; relative canonical or `og:image`.
- **warn**: lengths outside the audit's editorial targets, duplicate titles or descriptions, not exactly one `<h1>`, images without `alt`, missing canonical or Open Graph tags, a canonical that points at another page, a noindex page still in `sitemap.xml`, missing `sitemap.xml` or `robots.txt`.
- **info**: noindex pages and pages without `og:image`.

Also run `node <skills-dir>/bascik/scripts/check-links.mjs` for broken links and `#fragments`.

## Look it up

| How do I...                                                        | Read                                                                                |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Write the essential head tags and JSON-LD                          | `/lighthouse/seo`                                                                   |
| Follow Google's guidance for site names, title links, and snippets | `/lighthouse/seo#site-names-titles-and-snippets`                                    |
| Help Google understand the home page and choose sitelinks          | `/lighthouse/seo#help-google-choose-sitelinks`                                      |
| Use structured data for an eligible rich result                    | `/lighthouse/seo#structured-data-with-json-ld`                                      |
| Understand ranking limits and Preferred Sources                    | `/lighthouse/seo#ranking-and-publisher-features`                                    |
| Control `sitemap.xml`, `robots.txt`, and lastmod dates             | `/sitemap`                                                                          |
| Publish `llms.txt` and support AI agents                           | `/lighthouse/agentic-browsing`                                                      |
| Generate per-page canonical URLs and titles                        | `/how-to/page-aware-scripts`                                                        |
| See the helper in a working site                                   | `add-example.mjs starter-site/src/lib/seo.ts`, or the starter site README on GitHub |
| Serve files under `/.well-known/`                                  | `/deployment#well-known-uris`                                                       |

`node <skills-dir>/bascik/scripts/read-doc.mjs <path>` prints any of these.
