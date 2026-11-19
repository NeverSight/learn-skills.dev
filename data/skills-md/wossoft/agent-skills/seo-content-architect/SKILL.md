---
name: seo-content-architect
description: Plan an SEO-first website content architecture before UI design or frontend implementation. Use when defining site identity, topics, search intents, Google/Bing SERP-backed page types, sitemap, URL preservation and redirects for a reworked site, Markdown content sources, internal links, and page metadata for a new or reworked website. Not for isolated copy edits or technical SEO audits.
---

# SEO Content Architect

Define what the website is, what it should cover, and how its pages relate before designing or building the interface.

## Work content first

- Complete the content architecture before UI design or frontend implementation. If the request also includes design or development, finish and expose the architecture artifacts first, then use them as the design input.
- Start from the user's business, product, audience, market, language, and conversion goals. Inspect an existing site's pages and content when available.
- Separate confirmed facts, research findings, and assumptions. Ask only when a missing choice would materially change the site's identity or scope; otherwise proceed with a clearly marked assumption.
- Keep the output proportional to the site. Prefer a small, coherent architecture over a large speculative sitemap.

Use this order:

`Business -> Site Identity -> Existing Site Inventory -> Search Research -> SERP -> Topic Cluster -> Sitemap -> Review Checkpoint -> Markdown Content -> Internal Links -> SEO Metadata -> Design`

Skip the inventory step for a new site.

## 1. Define the site identity

Create `site-identity.md` before planning pages. State:

- who the site or organization is;
- what it offers;
- whom it serves;
- which problems it solves;
- its primary conversion or business outcomes;
- the core topics it can credibly own;
- topics it should not cover;
- its useful differentiation and evidence, without inventing claims;
- target markets and languages. For more than one language or region, decide the URL strategy (subdirectories such as `/en/` and `/de/` by default; subdomains or separate domains only with a stated reason) and that each localized page declares `hreflang` alternates. Settle this before the sitemap, because it shapes every path.

Use the topic exclusions to prevent adjacent high-volume queries from expanding the site beyond its purpose.

## 2. Inventory an existing site

When reworking a site, existing URLs that already rank or earn links are assets. Losing them loses traffic.

- List current indexable URLs from the live sitemap, a crawl, or the codebase.
- When the user can provide Google Search Console or Bing Webmaster Tools data, record clicks, impressions, and main queries per URL. Without that data, mark traffic as unknown rather than estimating it.
- Default to keeping a URL that has traffic, impressions, or external links. Change it only when the new architecture clearly requires it.
- For every URL that is removed, merged, or moved, record a 301 target in `url-migration.md`: old URL, new URL or `410` with reason, traffic evidence, and decision. Redirect to the closest equivalent page, never blanket-redirect to the homepage.
- Treat existing pages that already own a search intent as the canonical owner unless there is a reason to move ownership.

## 3. Research search intent and the live SERP

Target search engines are **Google** (primary) and **Bing**. Do not research other engines.

Before defining an important page, search the current results for its likely primary query and meaningful variants. Important pages include the homepage, core product, service, or tool pages, cluster hubs, and pages expected to drive material acquisition or conversion.

- Inspect the top 10 organic results on Google plus visible SERP features (AI Overview, featured snippet, People Also Ask, video, shopping, local pack) for the target locale and language.
- Check Bing for important pages, and note where it differs materially from Google. Bing results also feed Microsoft Copilot and other AI search experiences, so differences there matter.

For each important intent, record:

- **Search Intent:** the job the searcher is trying to complete;
- **Content Type:** product page, tool, tutorial, comparison, documentation, category, landing page, or another type actually represented in the SERP;
- **Content Format:** guide, list, calculator, template, reference, interactive workflow, and so on;
- **Content Angle:** the dominant promise or framing;
- **Competing Pages:** the main relevant results and their URLs;
- **SERP Gaps:** what existing results omit, obscure, or handle poorly;
- **Information Gain:** specific data, expertise, tool capability, workflow, examples, or perspective this site can uniquely add.

Record the research date, engine, locale, and language. Treat rankings and SERP features as time-sensitive observations, not permanent facts. Cite the pages used as evidence.

Let the observed intent and SERP determine the page type. Do not force every query into an article. If live search is unavailable or the user disallows it, do not fabricate SERP findings; mark the page `serp: unverified` and provide the queries that still need research.

## 4. Build topics and intent clusters

- Derive a limited set of core topics from the site identity, then group supporting topics beneath them.
- Model one primary page for one search intent. Map close keyword variants to that page instead of generating one page per keyword.
- Before adding a page, compare it with existing and planned pages for audience, intent, promised outcome, likely SERP overlap, and content scope. Merge, retarget, or defer pages that would compete with one another.
- Prioritize business relevance, conversion potential, product fit, credibility, and achievable information gain over raw search volume. Use search-volume or Search Console data when available; otherwise state that priorities are judgment-based.
- Do not create an important page unless it has a clear information gain. If the site cannot add something useful, exclude or defer the page.
- Use programmatic SEO only when every generated page is grounded in real data, a useful tool capability, or genuinely distinct content. Query permutations and AI-filled templates are not sufficient differentiation.

## 5. Create the sitemap

Each planned page gets one Markdown source file under `content/` whose path maps clearly to its URL. Its front matter is the **single source of truth** for that page's plan:

```yaml
---
title: ""
path: ""
core_topic: ""
topic_cluster: ""
goal: ""                 # what the page must help the visitor or business accomplish
search_intent: ""        # the single primary intent owned by the page
primary_query: ""        # representative query, not a reason to create variants
page_type: ""            # supported by SERP evidence and user need
cta: ""                  # the next meaningful action
parent: ""               # structural parent page
related_pages: []        # semantic relations outside the parent-child path
information_gain: ""     # why this page deserves to exist
previous_url: ""         # existing sites only, when the URL changes
serp: unverified         # verified | unverified | n/a
status: planned          # planned | brief | draft | ready
---
```

`serp` records whether the intent and page type are backed by live research; `status` records how far the content has progressed. Keep them independent.

Generate `sitemap.md` from the front matter as a hierarchy plus a table (path, page type, primary query, parent, `serp`, `status`). Do not hand-edit it; regenerate it whenever pages change. Keep the hierarchy shallow enough to understand and specific enough to guide implementation.

Maintain one canonical owner for each primary intent. Identify conflicts explicitly rather than hiding duplicates under different URLs.

## 6. Review checkpoint

Stop after the sitemap and present a review summary before writing content, unless the user has explicitly asked for an end-to-end run. Identity and page ownership mistakes are cheap to fix here and expensive after content exists.

The summary contains, without YAML:

1. site identity in three to five lines, including excluded topics;
2. the page hierarchy with each page's primary query, page type, and `serp` state;
3. intent conflicts and how they were resolved (merged, retargeted, deferred);
4. for an existing site, URL changes and redirects, with the traffic evidence behind each;
5. numbered open questions and assumptions, structure-changing ones first, so the user can answer by number.

Apply the user's answers, regenerate `sitemap.md`, then continue.

## 7. Write Markdown content

After the front matter, write the actual page content or a content brief at the depth authorized by the user. Mark briefs as briefs (`status: brief`); do not present outlines as finished content. Include only sections needed to satisfy the intent and deliver the claimed information gain. Do not put multiple independently indexable intents into one source file.

Write so both readers and AI search can use the page:

- answer the primary question near the top, then elaborate;
- make key passages self-contained, so a definition, step, or comparison still makes sense when quoted alone;
- prefer specific facts, numbers, examples, and first-hand experience over general statements, and cite sources for factual claims;
- use descriptive headings that match the questions the section answers.

Do not impose a minimum word count. Remove repetition, generic introductions, and AI filler rather than expanding copy to reach an arbitrary length.

## 8. Design internal links

Create `internal-links.md` with a concise link map containing source page, destination page, relationship, reader reason, and suggested anchor concept.

- Use links to express both hierarchy and semantic relationships.
- Link hubs to children and children back to their relevant hub.
- Add cross-cluster links only when they help the reader continue a related task.
- Ensure every indexable page has a discoverable path and at least one intentional internal inbound link; flag orphan pages.
- Prefer descriptive, natural anchors. Do not force exact-match anchors or add links solely for keyword repetition.

## 9. Add metadata after the content structure

Once intent, page purpose, and content are stable, add page titles, meta descriptions, canonical paths, `hreflang` alternates for localized pages, and sharing metadata where useful. Keep them aligned with the actual page promise and avoid inventing claims that the content does not support.

Recommend structured data (JSON-LD) only for types the visible content actually supports, such as `Organization`, `Product`, `Article`, `BreadcrumbList`, `FAQPage`, or `HowTo`. Never mark up content that is not on the page.

Do not use metadata work as a substitute for resolving duplicate intent, weak content, or an unclear site identity.

## Deliverables

Scale the deliverables to the site:

- **Small site (about five pages or fewer):** one `seo-plan.md` with identity, SERP notes, sitemap, and link map as sections, plus `content/`.
- **Larger site:**

```text
site-identity.md
sitemap.md               # generated from content/ front matter
internal-links.md
serp-research.md         # or linked research sections within page sources
url-migration.md         # existing sites only
content/
  index.md
  ...one Markdown source per SEO page
```

Keep SERP evidence concise and actionable.

End with unresolved decisions and explicitly unverified SERPs, if any. The architecture is ready for design only when the site's identity, page ownership, hierarchy, content source, URL preservation, and important internal relationships are clear. When the `page-blueprint` skill is available, it takes the sitemap and `content/` as input: each page's `page_type` selects a website pattern (`landing`, `article`, `hub`, `comparison`), and layouts reference content sections by heading. Keep `page_type` values and section headings stable enough for that mapping.
