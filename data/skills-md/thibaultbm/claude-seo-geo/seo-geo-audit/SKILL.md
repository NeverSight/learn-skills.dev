---
name: seo-geo-audit
description: "Get a prioritized SEO + GEO action plan for any website. Input: a URL (and optional competitors). Output: ranked fixes across technical health, content, keywords, e-commerce, local, backlinks, and AI visibility (ChatGPT, Perplexity, Google AI Overviews), or a plain-language summary. Use to audit or review a site, find why it does not rank or is not cited by AI, compare against competitors, or set a baseline before a bigger SEO project."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Full SEO + GEO site audit

Audit a website the way a senior practitioner does: collect verifiable facts first, judge them against a field-tested checklist, benchmark against the competitors that actually rank, and deliver a short list of fixes ordered by impact. The methodology was distilled from 115+ real agency audit calls and updated with sourced 2025-2026 evidence on AI search.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed.

## Why this audit is different

1. Facts before judgment. Every claim in the final report must trace back to something measured (by the bundled script, a browser check, or data the owner provided). Never guess a title length or assume a sitemap exists.
2. Competitors over abstract thresholds. "Your page has 400 words" means nothing alone. "The three sites outranking you average 1200 words on this query" is a finding. When competitors are known, benchmark page versus page.
3. Two search worlds at once. Every category is checked twice: does it help Google rankings, and does it help the site get retrieved and cited by ChatGPT, Perplexity and Google AI Overviews. These overlap but do not coincide (AI Mode answers show only about 32 percent URL overlap with the top 10 organic results).
4. The audit is a pricing tool for agencies. The counted error volume doubles as a quote: "500 errors on this site, that is roughly 3000 euros of work" scopes the project the prospect is buying. The score is a ratio of errors to pages, so one template-level error repeats across every page using that template and a single fix corrects it everywhere, which is why a low score is rarely a catastrophe. Frame both up front so the owner reads the report as a plan, not a verdict (field heuristic from 115+ agency audits).

## When to use

- The user provides a URL and wants improvement points, an audit, a review, or a "check".
- A site does not rank, never gained traction, or is invisible in AI assistant answers.
- Not for a sudden loss: when traffic or rankings fell from a known level, use the seo-traffic-drop skill first. An audit lists everything imperfect on a site, which is the wrong instrument for finding the one thing that changed.
- The user wants a comparison against one or more competitors.
- A baseline is needed before content production, a migration, or a redesign.

## Inputs to gather

Ask only for what is missing; proceed with what exists:

| Input | Required | Note |
|---|---|---|
| Homepage URL | yes | The script also discovers robots.txt, sitemap, llms.txt |
| 1-2 key pages | recommended | Top service, product or article page |
| Competitor URLs | recommended | Enables page-versus-page benchmarking |
| Goals and market | helpful | Local vs national, language, business model |
| GSC / GA4 access | optional | Indexation ratio and traffic facts; otherwise ask the owner for screenshots |

## Phase 1: collect the facts

Run the bundled collector on the homepage plus key pages, and on each competitor page cited later in the report:

```
python3 scripts/seo_audit.py https://example.com /services /blog/top-article
```

It returns, per page: a page kind (homepage, article, blog hub, product, page), an SEO score and a GEO score out of 100 with a ranked FINDINGS list (same thresholds and weights as the Sorank SEO Analyzer extension, codes explained in checklist section 15), and the facts behind them: HTTP status, HTTPS, platform fingerprint, title (with generic-title flag), meta description length, full heading hierarchy with level jumps, image alt coverage and weight sample, internal versus external link counts, Open Graph, canonical, JSON-LD types, visible word count, meta robots, an em dash and en dash count with samples (checklist 6.4: an AI-writing tell to find-and-replace with commas), a `likely_js_rendered` flag, bold count and samples, top terms with density and two-word phrases, the keyword placement matrix (title and H1 terms across title, H1, H2-H6, meta, URL, intro, bold, alt), readability (sentence-length buckets, Flesch), citability counts (statistics, definitions, quotes, question headings, snippable paragraphs), link quality (nofollow, sponsored, ugc, empty and generic anchors), social profiles and placeholder links, head tags (charset, favicon, Twitter card, Open Graph keys, meta refresh, hreflang validation), URL hygiene, mixed content, text-to-HTML ratio, DOM size, image format, dimensions and LCP lazy-loading, JSON-LD parse errors and missing or empty required properties per type, and template detection (table of contents, author block and author page link, dates, breadcrumb, commercial links in the body, blog hub card images). Site-wide: robots.txt rules for AI search bots, AI user-fetch agents, and AI training bots (three separate groups), sitemap declaration and URL count, llms.txt presence.

For the site-level view a page audit cannot give (orphans, click depth, weak inbound links, broken links and redirects, duplicate titles and H1, cannibalization candidates, stale pages), crawl the site:

```
python3 ../seo-internal-linking/scripts/site_crawl.py https://example.com --max-pages 500 --out crawl.json
```

With Search Console exports for two consecutive periods (and the same period a year earlier), `../seo-traffic-drop/scripts/content_decay.py` lists the pages losing traffic and why (ranking, CTR, demand, seasonal), stale pages first.

To compare one page with the pages that outrank it, run the benchmark on the client page and 3-5 competitor pages of the same type:

```
python3 scripts/page_benchmark.py --type service https://example.com/service https://rival-a.com/service https://rival-b.com/service
```

It prints one table (scores, words, bold, headings, tables, statistics, placement, schema, template blocks, social profiles, and every block `section_audit.py` detects), the blocks half or more of the competitors have and the client does not, the schema types they use, the metrics where the client sits below the competitor median, and the vocabulary gap (terms and phrases half the competitors use and the client never does, with the competitor headings that carry them). The page skills (homepage, service, product, collection, comparison, blog, local, page sections) run it as their Phase 3; the 27 requirements every page shares are in `references/common-page-spec.md`.

It also collects the measurement tags on every page (GA4, GTM, other analytics, Search Console verification meta) and ends with a measurement coverage summary that names the pages where the GA4 tag is missing.

Measurement is collected on EVERY page, not once for the domain: the usual failure is a tag pasted into one template and never into the others, which no site-wide check can see. Three outcomes, and they are not the same finding:

| Report says | What it means | What to do |
|---|---|---|
| `GA4: G-XXXXXXXX` | the tag is in the raw HTML | nothing |
| `GA4: unknown (a GTM container can load it)` | GTM is there, no G- id in the HTML | open the container or the browser Tag Assistant before writing anything; a GTM-loaded GA4 leaves no trace in the source |
| `NO MEASUREMENT AT ALL` | no GA4, no GTM, no other analytics | real finding, and it blocks every later recommendation |

The Search Console line reads the `google-site-verification` meta tag only. Its absence proves nothing: DNS records, an HTML file, GA4 and GTM verify a property just as well and leave nothing in the page. Ask the owner instead of declaring the property unverified.

Known limits, and what to do about each:

| Limit | Fallback |
|---|---|
| `likely_js_rendered: true` (client-side site) | Open the page in a browser to read the real content, and report that AI crawlers cannot see it (they do not execute JavaScript, see seo-technical) |
| Images loaded as CSS backgrounds | Invisible to the parser (total may read 0); verify visually |
| Real-world speed | Ask the user to run https://pagespeed.web.dev (free, no key) on mobile and desktop and share scores |
| Backlink profile | Use GSC Links report or Bing Webmaster Tools if available; paid indexes (Ahrefs, Semrush, Moz) only as an option |
| GSC indexation ratio, Google Business Profile | Ask the owner; never invent these numbers |
| Tags injected by a consent manager or a server-side container | Invisible in raw HTML; confirm in the browser before reporting a missing GA4 |

## Phase 2: analyze against the checklist

Read `references/audit-checklist.md` now. It contains the full 15-category checklist with thresholds, detection methods, and the reason behind each rule. Work through it in this order, skipping categories that do not apply to the site type:

| # | Category | Applies to |
|---|---|---|
| 1 | Method and framing | all |
| 2 | Tags (title, meta, headings, slugs) | all |
| 3 | Images | all |
| 4 | Performance and indexation | all |
| 5 | Architecture (one intent = one page) | all |
| 6 | Content volume | all |
| 7 | Keywords and intent | all |
| 8 | Blog and articles | sites with a blog (or that need one) |
| 9 | GEO (AI visibility) | all |
| 10 | Conversion signals | all |
| 11 | E-commerce (products, collections) | stores |
| 12 | Backlinks and mentions | all |
| 13 | Local (Google Business Profile) | local businesses |
| 14 | Migration risks | sites about to change domain, CMS or structure |
| 15 | Measured page checks (the script's FINDINGS codes and scores) | all |

While analyzing:

- Classify each finding as OK, Fix, or Blocking. A Blocking finding (noindex on the whole site, client-rendered content, hacked pages) invalidates work on everything downstream; say so plainly.
- Count what can be counted ("23 of 31 images have no alt text"), because numbers make the report credible and actionable.
- Separate the two altitudes. This audit judges site health (crawl, speed, indexation, tags, schema). When a page is technically clean and still underperforms, the gap is usually a missing block rather than a broken attribute: hand that page to seo-page-sections for a block-by-block audit instead of stretching this checklist to cover it.
- Identify the 3 highest-impact fixes. Resist listing 40 equal-weight items: the owner will do nothing with that. The philosophy is that SEO compounds many small gains (roughly "1 percent per action", a field heuristic), but the report must still rank them.

## Phase 3: the GEO layer

For the same pages, evaluate AI visibility specifically:

1. Crawler access: from the script output, report blocked AI search bots (these remove the site from AI answers) separately from blocked training bots (a brand-visibility tradeoff, see the canonical table in seo-technical references/ai-crawlers.md).
2. Rendering: if content only exists after JavaScript runs, ChatGPT, Claude and Perplexity cannot read it. This single finding outranks everything else in the GEO section.
3. Citability: score the key pages against the 5-pillar rubric in geo-visibility (answer-first passages, stats and quotes with sources, tables and lists, question headings, E-E-A-T signals, structured data, descriptive slugs).
4. Entity: search the brand name; check that name, one-line description and key facts match across the site, LinkedIn, review platforms and directories.
5. Measurement baseline: note whether the site can even see its AI traffic today (GA4 channel setup), and point to geo-tracking.

## Phase 4: deliver

Read `references/output-templates.md` and pick the format:

- Template A, full audit report: for practitioners; verdict line, what is good, top 3 priorities, findings by category with OK / Fix / Blocking status, ordered action plan.
- Template B, plain-language email: for non-technical owners; no acronyms, every term explained in everyday words, progress acknowledged, honest verdict.

Rules for both: no em dash (U+2014) and no en dash (U+2013) anywhere in the deliverable, commas instead (a colon, a period or parentheses when a comma loses the sense); the em dash is the most recognizable tell of AI-written text and an audit that reads as machine output loses the authority its findings need. Flag the same thing as a finding when the audited pages carry em dashes: it is a live AI-writing tell on the client's own site, and the fix is a find-and-replace to commas. Then: write in the language of the site, open with what is genuinely good (credibility, and most sites do several things right), keep the verdict honest even when it is "rebuild before investing in content", and state explicitly what was not verified and why.

Reassure before you criticize: lead with honest numbered reference points ("this is already better than 90 percent of the sites I see", "I am very demanding on the score, above 80 percent is very good") so the owner trusts the findings instead of bracing for them. Explain the score as a ratio of errors to pages, where a template-level error repeats across all pages built on that template and one fix corrects it everywhere, so a low number does not warrant panic or a misread comparison against another tool (field heuristic from 115+ agency audits).

## Handoffs after the audit

| Finding | Skill to apply the fix |
|---|---|
| A dated loss of traffic or rankings, rather than a site that never performed | seo-traffic-drop |
| Crawl, speed, indexation, JS rendering, AI bot access | seo-technical |
| Wrong or missing keywords, cannibalization | seo-keyword-research |
| Weak or thin articles | seo-content-blog |
| Product page issues | seo-content-product-page |
| Thin homepage or sales page (no bold, no proof numbers, generic FAQ, no Organization or Course schema) | seo-content-homepage |
| Article template gaps (no table of contents, author box, dates, CTA) or a blog hub without cover images | seo-content-blog (references/blog-templates.md) |
| Service pages missing or merged | seo-content-service-page |
| Category pages with no content | seo-content-collection-page |
| Whole blocks absent from a page (no FAQ, no breadcrumb, no price in text) | seo-page-sections |
| No comparison or alternatives pages, so competitors own those queries | seo-content-comparison-page |
| Orphan pages, weak internal links | seo-internal-linking |
| Missing or invalid structured data | seo-schema-markup |
| Weak link profile, no brand mentions | seo-backlinks |
| Local visibility, reviews, GBP | seo-local |
| Low AI citation rate | geo-visibility |
| No AI traffic measurement | geo-tracking |

## Common mistakes

- Auditing only the homepage. Money pages and one article reveal more than the homepage alone.
- Reporting thresholds without competitors. The gap is the finding, not the absolute number.
- Treating GEO as a separate mystical discipline. Most GEO failures found in audits are SEO failures (not indexed, client-rendered, thin content) wearing a new name.
- Inventing data. If speed, backlinks or indexation were not measured, write "not verified" instead of guessing.
- Burying the verdict. The first line of the deliverable answers: is this site ready to grow, does it need a short fix list, or does it need a rebuild first.

## Sources

- AI Mode versus top 10 organic overlap (32 percent URL overlap): https://www.semrush.com/blog/ai-mode-comparison-study/
- AI crawlers do not execute JavaScript (500M+ fetch analysis): https://vercel.com/blog/the-rise-of-the-ai-crawler
- Why ChatGPT cites pages (1.4M prompt study): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Generative Engine Optimization (controlled study, KDD 2024): https://arxiv.org/abs/2311.09735
- Google guidance on AI features and structured data: https://developers.google.com/search/docs/appearance/ai-features
