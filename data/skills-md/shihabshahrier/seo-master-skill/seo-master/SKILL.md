---
name: seo-master
description: >
  Complete SEO + GEO (Generative Engine Optimization) + AEO (Answer Engine
  Optimization) playbook for 2026. Covers traditional search ranking, how AI
  engines + coding agents (ChatGPT/Bing, Claude+Claude Code/Codex/OpenClaw/Brave,
  Gemini/Google, Perplexity) discover/rank/cite pages, framework-aware
  implementation (Next.js App Router Metadata API + React SPA prerender),
  structured data, technical SEO, titles/meta, content strategy, IndexNow,
  Google + Bing Search Console, competitor analysis, the 2026 I/O + core-update
  changes, and a prioritized checklist. Use when optimizing any website for
  search engines and AI answer engines, planning content/SEO strategy, adding
  structured data, fixing titles/meta, getting cited by AI chatbots/agents, or
  setting up Search Console. Also covers entity / personal-brand SEO across
  several owned domains, and small-site triage (when to prune rather than
  publish).
license: MIT
user-invocable: true
argument-hint: '[site path or URL to optimize]'
when_to_use: >
  Optimizing a website for search + AI answer engines; planning content/SEO
  strategy; implementing SEO in Next.js or React; adding structured data; fixing
  titles/meta; getting cited by ChatGPT/Claude/Gemini/coding agents; setting up
  Google/Bing Search Console + IndexNow.
---

# SEO Master Skill (SEO + GEO + AEO, 2026)

Battle-tested playbook distilled from optimizing a real SaaS (letx.app, a
collaborative LaTeX editor) against AI-native competitors. Everything here is
applied knowledge, not theory.

## The one-paragraph mental model

In 2026 there are **two audiences**: classic search crawlers (Google, Bing) and
**AI answer engines** (ChatGPT, Claude, Gemini, Perplexity, Copilot). They
overlap but differ. SEO ranks you in a list of links. **GEO/AEO gets you cited
inside an AI's generated answer.** A solid SEO foundation is required for both;
AEO/GEO adds: answer-first writing, dense structured data (especially FAQPage),
fact density, freshness, and being present where each AI grounds its search.
Critically — **each AI uses a different search index**, so "getting indexed" is
not one task but several.

## How to use this skill

1. **Detect the stack first** (`package.json` → Next.js App/Pages Router, React
   SPA, Astro, Remix…). Implementation differs by render model. See
   `references/framework-seo.md`.
2. Read `references/ai-engines-and-indexes.md` — determines *where* to optimize.
   Wrong index = invisible to that AI. (Coding agents like Claude Code / Codex /
   OpenClaw / Hermes mostly ground on **Brave**.)
3. Skim `references/whats-new-2026.md` for the I/O 2026 + May core-update context
   (AI Mode on Gemini 3.5 Flash; "AEO/GEO is still SEO"; llms.txt is optional).
4. Run the audit in `references/implementation-checklist.md` against the site.
5. Fix in priority order: indexing reach → structured data → answer-first
   content → titles/meta → content moat.
6. Use `references/search-console-setup.md` for Google + Bing + IndexNow, and
   `references/structured-data.md` / `references/content-and-aeo.md` as
   copy/paste references while implementing.

## Reference files (read as needed)

| File | What's in it |
|------|--------------|
| `references/ai-engines-and-indexes.md` | Which index each AI + coding agent uses (Brave/Bing/Google), how each cites, per-engine tactics |
| `references/framework-seo.md` | Detect the stack; Next.js App Router Metadata API (`metadata`/`generateMetadata`, sitemap/robots/OG conventions, render modes) + Pages Router + React SPA |
| `references/whats-new-2026.md` | Google I/O 2026, May 2026 core update, "AEO/GEO still SEO", llms.txt contested, AI-Mode query shift |
| `references/structured-data.md` | Every schema type with ready JSON-LD: FAQPage, HowTo, Course, SoftwareApplication, Article, Breadcrumb, ItemList, Product. Policy rules (fake ratings). |
| `references/titles-and-meta.md` | Title formula, the brand-suffix decision, meta description, OG/Twitter, canonical |
| `references/content-and-aeo.md` | Answer-first writing, fact density, FAQ pattern, content hubs, the "problems/errors" play, courses |
| `references/technical-seo.md` | Prerendering SPAs, sitemap, robots.txt + Content-Signals, llms.txt, code-splitting, Core Web Vitals, canonical/redirects |
| `references/search-console-setup.md` | Google Search Console, Bing Webmaster Tools + AI Performance, IndexNow (Cloudflare + script), submission steps |
| `references/competitor-and-positioning.md` | How to research competitors, find the open lane, off-site listicle strategy |
| `references/implementation-checklist.md` | Prioritized, copy-paste audit + execution checklist |
| `references/gsc-diagnostics-and-recovery.md` | Diagnose a site FROM Search Console data: brand/non-brand segmentation, striking-distance vs page-2 cohorts, slash-pair detection, the prerendered-SPA canonical trap + fix recipe, **the canonical-that-redirects check**, CTR surgery that still works in 2026, CLS quick wins, verification curl checks |
| `references/entity-and-personal-seo.md` | Optimising a *person* or a multi-domain owned network: one shared `@id` across domains, `sameAs` rules, Wikidata as the cheapest knowledge-graph entry, cross-domain product duplication, diagnosing entity fragmentation from GSC |

## Hard rules (learned the hard way)

- **Never fabricate `aggregateRating`/reviews in schema.** Google structured-data
  policy violation → manual action. Only use rating schema backed by visible,
  real on-page reviews. Use `featureList` / plain claims instead.
- **Never copy a competitor's stat.** ("20M users" belonged to Overleaf, not us —
  caught and removed.) Every claim must be true and yours.
- **Title ≤ 60 chars** or Google truncates. Long brand descriptors don't fit on
  content pages — use a short `| Brand` suffix there.
- **FAQ schema requires the FAQ to be visible on the page.** Schema-only FAQ =
  policy risk. Always render the questions AND emit JSON-LD.
- **Code-split heavy content** (course data, KaTeX, etc.) so the main JS bundle
  every visitor downloads stays small. Prerendered HTML keeps full content for
  SEO regardless.
- **IndexNow does NOT notify Google** — only Bing/Yandex/DuckDuckGo/etc. Google
  uses its own crawl + Search Console.
- **Detect the framework before implementing.** Next.js App Router uses the
  Metadata API (`metadata`/`generateMetadata`) — not helmet, not prerender. Only
  hand-rolled React SPAs need the Puppeteer prerender. Wrong tool = wasted work.
- **Don't over-optimize for AI citations.** The May 2026 core update appears to
  demote shallow answer-bait. Depth + real E-E-A-T + genuine fact density win;
  thin Q&A spam is now a risk, not a hack.
- **llms.txt is optional, low priority** — Google says it "isn't needed for AI
  Search." Add it only if cheap; never before content/schema/indexing.
- **Exactly ONE canonical per page, verified with curl on the deployed site.**
  Prerendered SPAs bake the static index.html canonical into every page and
  helmet adds a second — both wrong. The crawler reads baked HTML, not your
  DevTools. (Found live on a 500-user product; suppressed the whole site.)
- **Trailing slash: standardize on whatever the HOST redirects to** (Cloudflare
  Pages 308s to slash). Canonicals, sitemap, og:url, and internal hrefs must all
  use that one form, or GSC splits impressions across slash pairs.
- **Segment GSC before concluding anything.** Blended CTR/position lie: split
  brand vs non-brand, pos 4–15 (snippet problem) vs pos >15 (content-depth
  problem). New-content launches drop blended metrics mechanically — mix shift,
  not a penalty.
- **FAQ rich results no longer show for normal sites** (gov/health only since
  2023). Keep FAQPage for AI citation; for SERP CTR use title/meta rewrites and
  ItemList-with-images on collection pages instead.
- **Don't merge "duplicates" reflexively.** Two pages at pos 5–6 for one query =
  double SERP presence (keep + differentiate); and near-identical slugs may be
  genuinely different products — verify content before 301ing.
- **A single well-formed canonical can still be wrong.** Resolve it: if the URL
  the canonical names returns a 3xx, every page is pointing at a redirect. Found
  sitewide on a live site whose canonicals all omitted the trailing slash its
  host 308s to. `curl` the canonical target, don't just count the tags.
- **Audit built HTML with a parser, never `grep`.** A code comment mentioning a
  tag name in literal markup makes grep report duplicates that do not exist in
  the DOM. Parse, and require 100% of pages to pass — not "most".
- **Never append a brand suffix unconditionally.** `${title} | ${Brand}` pushed
  34 of 50 post titles past 60 chars, so every one rendered truncated. Append
  only when the result still fits; a bare title beats a clipped one.
- **Verify your CSS actually styles what your content emits.** A site had
  `@tailwindcss/typography` in `package.json` but never registered in
  `tailwind.config.ts` — `.prose` was six hand-written rules with no table or
  code styling, so a new comparison table would have rendered black-on-black.
  Publishing a format the stylesheet doesn't cover is a rendering bug, not a
  content win.
- **Check a list's inclusion criteria before planning an off-site PR.** A
  28k-star "free LLM API resources" list looked like the highest-leverage
  backlink available — but it indexes *providers that serve inference*, and the
  product was a *client that calls them*. The PR would have been rejected. The
  in-scope lists had 0–7 stars and no ranking power. Read the actual entries
  first; a rejected PR costs credibility.

## Small-site triage — read this BEFORE writing anything

The default instinct on a low-traffic site is to publish more. On three measured
properties that instinct was wrong every time:

| Site | Pages | Clicks / 91 days |
|---|---|---|
| letx.app | 604 | 1,293 — but **92% branded** |
| shahriarlabs.com | 48 posts | 73 |
| shihub.online | 79 posts | **13** (only 12 posts got a single impression) |

letX segmented: branded 543 clicks @ 13.4% CTR; **non-brand 44 clicks @ 0.48%**.
A content engine manufactures impressions, not visitors, until something
off-site makes the brand worth clicking. And since the **June 2026 spam update**,
a large zero-demand footprint is an active liability rather than dead weight.

So when a site is under ~100 clicks/quarter, in this order:

1. **Fix signal suppression first.** Canonicals (including the redirect check
   above), trailing slash, sitemap accuracy, title truncation. This is free
   ranking you already earned and are throwing away.
2. **Prune, don't publish.** Keep pages that earned impressions, belong to the
   one cluster that converts, or contain first-hand work nothing else can
   duplicate. `noindex` + drop-from-sitemap the rest — **do not delete**: keep
   them reachable and `follow`, so nothing 404s and the decision stays
   reversible. (Applied: 62 of 79 posts withdrawn, sitemap 112 → 30 URLs.)
3. **Deepen the one cluster already in striking distance.** Find the query group
   at position 4–15 with real impressions and put everything into it. One page
   that is genuinely the best on the internet beats twenty that are adequate.
4. **Then go off-site.** See the priority list below — this is the actual lever.

New pages are justified only where GSC already shows measured demand and no page
serves it. "This topic seems relevant" is not evidence; an impression count is.

## The priority order (highest ROI first)

1. **Indexing reach** — be in Google, Bing, and Brave indexes; wire IndexNow.
   (Feeds ChatGPT via Bing, Claude via Brave.)
2. **Structured data** — FAQPage on every page that can carry it (~3.2× AI
   Overview citation). Plus SoftwareApplication/Product/Article/HowTo.
3. **Answer-first content** — direct answer in first 40–60 words; 134–167-word
   self-contained passages.
4. **Titles/meta** — consistent, keyword-first, ≤60 chars.
5. **Content moat** — guides/tutorials/error-fix hub targeting the long-tail
   the competitor monetizes.
6. **Off-site** — get listed in the "alternatives" listicles AI engines cite.
