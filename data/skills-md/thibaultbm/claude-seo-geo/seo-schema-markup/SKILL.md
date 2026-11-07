---
name: seo-schema-markup
description: "Get valid Schema.org JSON-LD that still earns surfaces in 2026. Input: a page and its type (article, product, local business, person, and so on). Output: ready-to-adapt JSON-LD (Organization with sameAs, Article, Product, Offer, AggregateRating, LocalBusiness, BreadcrumbList, Person, WebSite, VideoObject, Event), entity graph linking with @id, a what-Google-dropped status table, and a two-validator routine. Use for schema, structured data, JSON-LD, rich results, review stars, breadcrumbs, sameAs, knowledge panel, or Rich Results Test errors."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Schema markup that still pays in 2026

Structured data is the most machine-readable layer of a page: prices, ratings, dates, authors, and entity relationships declared in a format engines parse without guessing. Google reads it for rich results and Merchant listings; LLM grounding pipelines read it as a fact source. Between 2023 and 2026 Google removed several rich result types, so effort that used to pay (FAQ, HowTo) now buys nothing in the SERP. This skill implements what still earns surfaces, skips what is dead, and keeps every claim inside Google's guidelines.

One principle governs everything: markup describes the visible page. It never adds facts the user cannot see.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed.

## When to use this skill

Use it for:

- Implementing JSON-LD on any page type (home, blog post, product, location, author, video, event)
- Auditing existing markup for validity, eligibility, and honesty
- Rich result work: review stars, prices, availability, breadcrumbs, video
- Entity work: Organization, sameAs, author Person graphs for E-E-A-T
- Deciding which schema types deserve effort in 2026 (status table below)
- Debugging Rich Results Test errors or rich results that disappeared

When schema is NOT the answer:

- "Our FAQ dropdowns vanished from Google": that is Google removing the feature (May 2026), not a markup bug. Check the status table before debugging.
- "Make us rank higher with schema": structured data disambiguates and unlocks result features; it is not a ranking lever on its own. Set that expectation early.
- "The page is not indexed at all": fix crawl and indexation first with the seo-technical skill; schema on an unindexed page is decoration.

Hand off neighboring problems:

- Crawlability, JavaScript rendering, AI crawler access: use the seo-technical skill (its references/ai-crawlers.md is the canonical crawler reference)
- Writing content that AI engines quote: use the geo-visibility skill
- Google Business Profile and local rankings: use the seo-local skill
- Page structure and copy for products, services, collections: use the seo-content-product-page, seo-content-service-page, and seo-content-collection-page skills

## Workflow

### Step 1: Inventory what is already there

Fetch the raw served HTML and check for structured data blocks:

    # How many JSON-LD blocks does the server actually send
    curl -sL https://example.com/page/ | grep -c 'application/ld+json'

    # Legacy microdata that may conflict with JSON-LD
    curl -sL https://example.com/page/ | grep -c 'itemscope'

Why raw HTML: JSON-LD injected client-side (Google Tag Manager, SPA hydration) is unreliable. Googlebot usually picks it up after rendering, but AI crawlers never execute JavaScript (see the seo-technical skill), and any validator pointed at the source misses it. Structured data belongs in the server response. For a quick automated sweep of on-page basics alongside schema, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py), which checks robots.txt AI bot rules, sitemap, and on-page basics.

Record per page type: which schema types exist, whether they validate, and whether the values match the visible page. The third question catches the violations that matter; the first two are mechanical.

### Step 2: Map page types to schema types

| Page type | Implement | Skip |
|---|---|---|
| Every page | Organization reference (@id), BreadcrumbList | FAQPage for rich results |
| Homepage | Organization (full node) plus WebSite | |
| Blog post | Article or BlogPosting, author Person, BreadcrumbList | HowTo |
| Product page | Product, Offer, AggregateRating and Review when real reviews are displayed | Invented ratings |
| Service page | Service or WebPage, Organization reference | Self-serving review stars |
| Location page | LocalBusiness, most specific subtype available (pair with the seo-local skill) | LocalBusiness on a business with no physical premises |
| Author page | ProfilePage with mainEntity Person (same @id as every article byline, sameAs to the real profiles) | |
| Training, coaching or course program page | Course (name, description, provider, offers when the price is public, hasCourseInstance with courseMode and courseWorkload); or Service when it is one-to-one coaching with no syllabus | Self-collected review stars on the program |
| Video page | VideoObject | |
| Event page | Event | |
| SaaS pricing page | Product or Service with Offer when prices are public | "From" prices not shown on the page |
| Careers page | JobPosting (active Google jobs surface) | |

### Step 3: Check what the CMS already outputs (field notes)

Most schema problems in real audits are duplication problems, not absence problems. Check before adding anything:

| Platform | What you typically find | What to do |
|---|---|---|
| WordPress with Yoast or Rank Math | A complete @graph already output: Organization, WebSite, Article, BreadcrumbList | Configure the plugin (logo, sameAs, author pages) instead of pasting a second block; two diverging Organizations is the classic self-inflicted wound |
| Shopify | Theme ships Product JSON-LD by default | Verify values against the visible page (sale price versus compare-at price, missing brand or sku); fix the theme markup rather than adding a duplicate Product |
| Webflow | No automatic schema | Add per-template embeds bound to CMS fields so values update with content |
| Headless or SPA builds | Markup present in the repo, absent from the served HTML | Move it into the server response; confirm with the curl check from Step 1 |

### Step 4: Apply the 2026 status table

Spend implementation effort top-down by verdict. The full table is in Rules and thresholds; the two headline facts: FAQPage rich results no longer exist for anyone (removed May 7, 2026), and HowTo has had no surface since 2023. Do not let a client pay for either expecting SERP features.

### Step 5: Build one entity graph, not isolated blocks

Engines reconcile entities; help them by linking nodes with stable @id values:

- Organization: @id {{SITE_URL}}/#organization, declared fully once (homepage or sitewide), referenced everywhere else
- Each author: @id {{SITE_URL}}/team/{{slug}}/#person
- Each Article: author points to the Person @id, publisher points to the Organization @id

The shape of a wired blog post, abbreviated (full templates in references/jsonld-templates.md):

    {
      "@context": "https://schema.org",
      "@graph": [
        { "@type": "Organization", "@id": "https://example.com/#organization", "name": "Example Co" },
        { "@type": "Person", "@id": "https://example.com/team/jane/#person", "name": "Jane Doe",
          "worksFor": { "@id": "https://example.com/#organization" } },
        { "@type": "Article", "headline": "Example headline",
          "datePublished": "2026-04-02", "dateModified": "2026-05-28",
          "author": { "@id": "https://example.com/team/jane/#person" },
          "publisher": { "@id": "https://example.com/#organization" } }
      ]
    }

Why it matters: three pages each declaring a slightly different Organization (name variants, different logos) fragment the entity. One canonical node referenced by @id keeps Google's and LLMs' view of the company consistent, and it is the cheapest E-E-A-T plumbing available: every article provably attached to a named author, every author attached to the organization.

Organization completeness, since this node feeds knowledge panels: logo at 112x112 px or larger on a crawlable URL, legal identifiers where applicable (vatID, iso6523Code), founder and foundingDate when public. Registry-grade identifiers give LLMs unambiguous hooks to reconcile the entity against company databases.

### Step 6: Implement as JSON-LD

- One script tag of type application/ld+json per graph, in head or body (Google accepts both).
- JSON-LD is the format Google recommends over microdata and RDFa: decoupled from the HTML, it survives redesigns and template changes (https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data).
- If microdata already exists (theme-generated), either remove it or keep its values strictly identical to the JSON-LD. Conflicting duplicate markup is worse than either alone because engines pick unpredictably.
- Bind values to CMS fields, never hardcode prices or dates into templates: hardcoded values drift from the visible page within weeks (field observation).

### Step 7: Validate twice, then verify in production

1. https://validator.schema.org checks vocabulary and syntax (catches typos, wrong types, broken nesting).
2. https://search.google.com/test/rich-results checks Google eligibility (catches missing required fields per rich result type). Both are free, web-based, and need no API key.
3. After deploy: curl the production URL and confirm the JSON-LD survived the build. SPA and static-site builds sometimes strip it or move it to client-side injection, which AI crawlers never see.
4. Over the following weeks: watch the GSC Enhancements reports per type (error counts, valid item trends). A rich result that disappears with zero new errors usually means Google changed the feature, not the site; check the status table before debugging.

### Step 8: Scale across hundreds of pages

- Generate from data, never by hand: bind template fields to the product database or CMS collections. Hand-edited JSON drifts from the page and breaks on the first locale-formatted date.
- Roll out one template at a time (all product pages, then all articles), validate a sample of 3 to 5 URLs per template, and watch the matching GSC Enhancements report for a week before starting the next type.
- Spot-check after every theme or plugin update: updates silently duplicate or reorder markup more often than they break it visibly (field observation from 115+ audits).
- Keep a one-page registry of which template outputs which types and where the code lives. The next audit starts there instead of rediscovering everything.

### Troubleshooting lost rich results (runbook)

Stars, prices, or breadcrumbs vanished from the SERP. Check in this order; most cases resolve at 1 or 2:

1. Did Google remove the feature for everyone? Check the status table: FAQ (May 2026), HowTo (2023), sitelinks search box (2024) are gone regardless of markup quality.
2. GSC Enhancements: new errors, or valid items dropping to zero, indicate a deploy that stripped or broke the block. Confirm with the Step 1 curl against production.
3. Policy trip: self-serving reviews, markup describing content that was edited off the visible page, or ratings that no longer match displayed reviews.
4. SERP-level reduction: when the markup validates and competitors lost the same feature on the same queries, Google reduced rich result density there; nothing to fix on the site.
5. Manual action: GSC Manual Actions, structured data section, after aggressive or invisible markup. Clean, then request reconsideration.

## Rules and thresholds

### The 2026 status table

| Type | Status | Verdict |
|---|---|---|
| FAQPage | Rich results restricted to government and health sites in August 2023, removed entirely on May 7, 2026 (https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/) | No SERP gain for anyone. The markup stays valid and harmless. What helps AI extraction is the visible question-and-answer format of the content, not the markup (see geo-visibility) |
| HowTo | Rich results removed in 2023, no surface since (https://developers.google.com/search/blog/2023/08/howto-faq-changes) | Skip |
| Article, BlogPosting | No visual badge, but supplies machine-readable author, datePublished, dateModified | Implement on every post; honest dateModified is the freshness signal answer engines read |
| Product, Offer, AggregateRating, Review | Active rich results (price, stars, availability) and the basis of Merchant listings (https://developers.google.com/search/docs/appearance/structured-data/product) | Implement on every product page, visible data only |
| Organization plus sameAs | The entity anchor: logo, founder, identifiers, official profiles (https://developers.google.com/search/docs/appearance/structured-data/organization) | Implement sitewide; this is the node LLM entity reconciliation leans on |
| WebSite | Sitelinks search box retired in 2024 (https://developers.google.com/search/blog/2024/10/sitelinks-search-box), still names the site entity | Implement, minimal effort |
| BreadcrumbList | Active breadcrumb display in results | Implement sitewide |
| LocalBusiness | Active (maps and knowledge panel context) | Implement on location pages; pair with the seo-local skill |
| Person | No direct rich result; E-E-A-T and author entity plumbing | Implement for every named author |
| VideoObject | Active video surfaces | When a video is on the page |
| Event | Active event surfaces | When events exist |

### Hard rules

1. Visible content only. Markup must describe content the user can see on that page. Invisible or inflated markup is a structured data manual action waiting to happen (https://developers.google.com/search/docs/appearance/structured-data/sd-policies).
2. Never invent ratings or reviews. No aggregateRating without real reviews displayed on the page. Self-serving review snippets are explicitly ineligible: LocalBusiness and Organization cannot carry ratings they collected and display about themselves (https://developers.google.com/search/docs/appearance/structured-data/review-snippet).
3. Dates tell the truth. dateModified changes when content meaningfully changes, never on every rebuild. Engines that detect systematic date-bumping discount the signal entirely.
4. Values match the page exactly: same price, same currency, same availability as the visible offer, byte for byte where possible.
5. Google eligibility comes from Google's per-type documentation, not from schema.org validity alone. A block can be perfectly valid Schema.org and still miss a required field for the rich result.
6. Images referenced in markup (logo, product, article) must live on crawlable URLs you control and meet Google's minimum sizes. A hotlinked image that disappears voids the rich result silently.

### High-impact fields per type (eligibility checklist)

The fields that most often make the difference between valid markup and an actual rich result:

| Type | Must have for the surface | Highest-value optional fields |
|---|---|---|
| Product | name, offers with price, priceCurrency, availability | aggregateRating and review (when real), brand, sku, gtin, image, priceValidUntil |
| AggregateRating | ratingValue plus ratingCount or reviewCount | bestRating when the scale is not 1 to 5 |
| Article | headline, image, datePublished | dateModified, author with url, mainEntityOfPage |
| Organization | name, url, logo | sameAs, founder, foundingDate, contactPoint, legal identifiers (iso6523Code, vatID) |
| LocalBusiness | name, address | telephone, geo, openingHoursSpecification, priceRange, specific subtype |
| BreadcrumbList | itemListElement with position and name; item URL on all but the last element | |
| VideoObject | name, thumbnailUrl, uploadDate | duration, contentUrl, description |
| Course | name, description, provider | offers (price, priceCurrency, category), hasCourseInstance (courseMode, courseWorkload or courseSchedule), inLanguage, educationalLevel |

When in doubt, the Rich Results Test reports exactly which required field is missing for the targeted surface; trust it over memory.

### Decoding frequent validator errors

| Error (Rich Results Test) | Actual cause | Fix |
|---|---|---|
| Missing field "aggregateRating" or "review" (warning) | Product has no rating surface filled | Acceptable when no reviews exist; never fill it with invented values to clear the warning |
| Invalid object type for field "author" | author set to a plain string | Use a Person object, ideally an @id reference to the author node |
| Either "ratingCount" or "reviewCount" should be specified | AggregateRating missing its count | Add the real displayed count |
| Date not in ISO 8601 | Locale-formatted dates from the CMS | Output YYYY-MM-DD (or full ISO timestamps) |
| Empty `name` on Question or empty `text` on Answer | Template outputs FAQ or Q&A markup before the CMS fields are filled | Render the node only when the field has content; `seo_audit.py` flags it as `schema_fields` |
| Duplicate field or duplicate type on the page | Plugin @graph plus a manually pasted block | One source of truth per page (Step 3) |
| Parsing error: missing comma, unclosed brace | Hand-edited JSON | Generate from references/jsonld-templates.md; lint before deploy |

### Multilingual sites

- Each localized page carries markup in its own language: name, description, and every visible value translated exactly as that locale's page displays them, with inLanguage set per locale.
- Keep @id values distinct per localized page (the FR article node is not the EN article node). The shared anchor across locales is the Organization, which stays one node sitewide.
- A translated page with source-language markup fails the visible-content rule in practice and confuses entity reconciliation: engines see a French page claiming English facts.
- Currency and price localize too: the EUR offer on the FR page, the USD offer on the US page, each matching its visible price.
- Routing users between language versions is hreflang work: see the seo-technical skill.

## GEO layer: structured data as a fact feed for answer engines

Structured data is the densest machine-readable declaration of facts a page can make: price, availability, rating value and count, publication and modification dates, author identity, and entity relationships. LLM grounding and shopping pipelines parse these fields when composing and verifying answers; what is ambiguous in prose becomes explicit in JSON-LD.

What earns the most for AI visibility:

1. Organization plus sameAs: links the site entity to its profiles (LinkedIn, Crunchbase, G2, Wikipedia). LLMs cross-reference entities across sources; consistent naming and linked profiles consolidate the brand into one entity instead of fragments. The wider entity strategy (mentions, third-party profiles, consistency) belongs to the geo-visibility skill.
2. Honest dateModified on Article: 2025 citation analyses report that answer engines favor recently updated sources on commercial and news intents; treat the exact effect size as directional, but machine-readable freshness costs nothing when it is honest.
3. Product facts: engines answering "how much does X cost" prefer sources where price, currency, and availability are declared and consistent with the visible page. Shopping surfaces in AI assistants consume the same product facts that feed Merchant listings.
4. Author Person nodes: answer engines increasingly attribute claims to named sources; a provable author entity (Person with url and sameAs, linked from every Article) is machine-readable accountability.
5. The Bing path: Bing's webmaster guidelines list Schema.org markup among the signals it uses to understand pages (https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a), and Bing's index feeds ChatGPT search (see seo-technical). Product and organization facts travel that route too.
6. The FAQ paradox, stated precisely: FAQPage markup earns nothing in 2026, while visibly formatted questions and answers remain one of the most extractable content shapes for AI engines. Keep the format, deprioritize the markup.

Two prerequisites from the seo-technical skill: AI crawlers read raw HTML only, so JSON-LD injected client-side does not exist for them; and a page blocked or unindexed never gets the chance to be parsed at all. Measuring whether any of this wins citations is the geo-tracking skill's job.

## Output format

When auditing, return one table plus prioritized fixes:

    # Structured data audit: {domain} ({date})

    | Page type | Types found | Valid | Matches visible content | Action |
    |---|---|---|---|---|
    | Blog post | Article (Yoast @graph) | Yes | dateModified auto-bumped | Stop date-bumping, add author Person |

    ## Fixes in priority order
    1. {fix}: why it matters, the exact JSON-LD block, where it goes

When implementing, deliver for each page type:

1. The JSON-LD block, adapted from references/jsonld-templates.md with every placeholder resolved (search the output for {{ before shipping)
2. Placement instruction: which template file or CMS field, server-rendered
3. The two validation URLs and what a pass looks like for that type
4. The GSC Enhancements report to watch afterward

Label every recommendation as one of: official requirement (Google documentation), eligibility requirement (rich result), or judgment call.

Definition of done for any schema task:

1. Block present in the raw served HTML of production (verified with curl, not in the browser)
2. Zero errors in validator.schema.org AND in the Rich Results Test for the targeted surface
3. Every value verifiable on the visible page by a human
4. No {{ placeholder left anywhere in the build output
5. Entity nodes linked by @id, no duplicate or diverging Organization declarations
6. The matching GSC Enhancements report identified and on a watch list

## Common mistakes

| Mistake | Consequence | Do instead |
|---|---|---|
| Marking up content not visible on the page | Manual action risk, trust loss | Markup mirrors the visible page |
| Inventing aggregateRating or importing third-party stars | Ineligible, penalizable | Real on-page reviews only; none displayed means no rating markup |
| Self-collected ratings on Organization or LocalBusiness | Ignored per review snippet rules | Earn ratings on third-party platforms; connect them via sameAs |
| Shipping FAQPage for rich results in 2026 | Zero SERP return on the effort | Visible question-and-answer formatting for AI extraction (geo-visibility) |
| JSON-LD injected via Tag Manager or client-side hydration | AI crawlers and source-level validators never see it | Server-render the script tag |
| Adding a manual block next to the SEO plugin's @graph | Two diverging Organizations, engines pick unpredictably | Configure the plugin; one source of truth per page |
| dateModified bumped on every deploy | Freshness signal discounted | Bump only on real content changes |
| Isolated blocks without @id linking | Fragmented entity, weaker reconciliation | One Organization node, referenced by @id everywhere |
| Templates shipped with {{PLACEHOLDERS}} left in | Broken facts in production | Search the build output for {{ before release |
| LocalBusiness on a business with no physical premises | Misleading markup, knowledge panel confusion | Organization for online-only businesses |
| Hardcoding prices and dates in templates | Markup drifts from the visible page within weeks | Bind every value to a CMS field |
| Marking category or tag pages as Article | Type noise, no surface | CollectionPage or nothing; reserve Article for actual posts |
| Adding Speakable outside news sites | No surface; it never left its limited news beta | Skip it |
| Stuffing keywords into name and description fields | Spam signal, mismatch with the visible page | Names match the visible H1 and title |
| Treating schema.org validity as Google eligibility | Missing required fields, no rich result | Validate with both validator.schema.org and the Rich Results Test |

## Sources

- Structured data intro, JSON-LD recommended: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- General policies (visible content, manual actions): https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- FAQ and HowTo restriction, August 2023: https://developers.google.com/search/blog/2023/08/howto-faq-changes
- FAQ rich results full removal, May 7, 2026: https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/
- Product structured data: https://developers.google.com/search/docs/appearance/structured-data/product
- Merchant listings: https://developers.google.com/search/docs/appearance/structured-data/merchant-listing
- Review snippet rules, self-serving ban: https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Organization (including identifiers): https://developers.google.com/search/docs/appearance/structured-data/organization
- Sitelinks search box retirement: https://developers.google.com/search/blog/2024/10/sitelinks-search-box
- Bing webmaster guidelines (structured data): https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a
- Validators, free, no API key: https://validator.schema.org and https://search.google.com/test/rich-results
- Field notes: 115+ agency audits, labeled as such throughout
