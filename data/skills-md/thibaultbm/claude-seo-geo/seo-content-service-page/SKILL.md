---
name: seo-content-service-page
description: "Spec, audit, competitor benchmark and build for service pages and service landing pages (agencies, consultants, coaches, trades, clinics, law firms, SaaS), plus region and city pages. Input: a service, the business, a target area, the page URL if any. Runs four phases: the spec (SVC-01 to SVC-24 on top of the common C rows), the audit of the existing page with seo_audit.py and section_audit.py --type service, the competitor benchmark with page_benchmark.py on the pages that rank and the providers AI assistants name, and the build on a field-tested 9-block wireframe (hero + CTA, proof, benefits, process, founder with checkable credentials, 750+ word question-led text with price, dated reviews, FAQ, final CTA), with metadata patterns, Service JSON-LD, a GEO layer and a scripted acceptance test. Delivers a spec scorecard, audit findings, benchmark, build and acceptance. Use for a service page, landing page, lead-generation page or city page that gets no organic leads."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "2.0.0"
---

# Service Page SEO: Money Pages That Rank and Convert

Service pages are where rankings turn into revenue. A blog post attracts readers; a service page attracts buyers typing "web design agency", "divorce lawyer geneva" or "emergency plumber lyon", and AI assistants now recommend providers directly from these pages. They usually fail the same way: one page for every service, a slogan instead of the keyword, no price, no named human, 300 words against competitors at 1500, and a single contact form at the bottom.

This skill runs the four phases of the page skill standard (`docs/page-skill-standard.md`): spec, audit, competitor benchmark, build. Two evidence levels are labeled throughout:

- **Field heuristic**: rules derived from 115+ real agency audits of service-business websites (2024-2026). Consistently observed, not lab-measured.
- **Measured**: claims backed by a published study, a benchmark with its date, or official documentation, with the source.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed.

## When to use this skill

Use it to create a new service page, rewrite an underperforming one, split a one-page site into service pages, plan city or region pages for a multi-area business, or audit an existing money page against the spec below.

Stay in scope. Hand adjacent work to the right skill:

| Task | Skill |
|---|---|
| Service pages, service landing pages, city pages (this skill) | seo-content-service-page |
| Homepage and flagship offer (sales) page | seo-content-homepage |
| Blog articles and informational content | seo-content-blog |
| Ecommerce product pages | seo-content-product-page |
| Category and collection pages | seo-content-collection-page |
| "X vs Y", alternatives and segment pages | seo-content-comparison-page |
| Block-by-block gap audit of any page type | seo-page-sections |
| Keyword selection and SERP intent analysis | seo-keyword-research |
| Google Business Profile, reviews, Maps, NAP | seo-local |
| Crawlability, Core Web Vitals, AI crawler access | seo-technical |
| Structured data implementation details | seo-schema-markup |
| Site-wide internal link architecture | seo-internal-linking |
| Citation and directory link building | seo-backlinks |
| Writing rules for AI answer citability | geo-visibility |
| Measuring AI assistant visibility | geo-tracking |
| Full-site audit | seo-geo-audit |

## Phase 1. The spec

### 1a. Map services to pages first (one service = one page)

The single most common audit finding (field heuristic): a brochure site with one page that lists every service, invisible on all of them. Each service has its own keyword, its own SERP and its own search intent; one page cannot win five different SERPs.

1. List every billable service the business sells.
2. For each, identify the query a buyer actually types, in buyer language, not internal jargon ("emergency plumber", not "rapid hydraulic intervention"); see seo-keyword-research.
3. Apply the SERP test: if two service names show different top 10 results, they need two pages. If Google returns the same results for both, one page covers both.
4. Plan one URL per service, plus a parent "Services" hub page that links to all of them.
5. If splitting an existing page, 301-redirect nothing that ranks; build the new pages first, then re-point internal links.

Competitor page mapping (field heuristic): to surface missing service and sector pages fast, paste the sitemap or page list of the 10 largest competitors into an AI model and ask it to list the page types they have that the audited site lacks. This exposes one-page sites and absent service, sector and use-case pages in one pass, before manual SERP testing. Cross-check each suggested page against real buyer demand before committing it.

Why: Google ranks pages, not sites, for transactional queries. A page about everything has diluted relevance for each thing. Splitting also gives each service its own title, H1, FAQ and proof, which a combined page cannot do.

### 1b. The service page spec

Common requirements C-01 to C-27: skills/seo-geo-audit/references/common-page-spec.md. Every C row applies to a service page; the rows below add what is specific to it. "Verified by" is a `seo_audit.py` finding code, a `section_audit.py --type service` block, or manual.

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| SVC-01 | One service, one intent, one primary keyword from buyer language | No other page on the site targets the same SERP (1a test) | manual (SERP test, site search) | Diluted relevance wins no SERP (field heuristic, most common finding) |
| SVC-02 | Service keyword placement (C-09, C-10, C-11 applied to the service term, + city when local) | In title, H1, URL, meta, first 100 words, 2+ H2, 1+ image alt; bold once in the first paragraph, then one bold phrase on a fact or benefit every 100-150 words; placement coverage 60%+; no term above 2.5% | kw_placement_low, kw_not_in_intro, kw_not_bold, no_bold, keyword_stuffing | The placement matrix the audit measures; bold is what skimmers read (field heuristic) |
| SVC-03 | Metadata pattern | Title "service keyword (+ city) \| brand", about 50-60 characters; one H1 = the keyword phrased for humans; slug = keyword (+ city), no dates or stop words; handwritten meta = promise + proof + CTA, 160 characters max | title_short, title_long, h1_missing, h1_multiple, meta_missing, meta_long, url_hygiene; manual for the pattern | Keyword first carries the signal; "Services \| Brand" carries none (display heuristic + Google title link docs) |
| SVC-04 | Hero passes the 5-second test | H1 as outcome; subline names the audience + one number (rating, clients, years); one primary CTA above the fold, sticky on mobile; no carousel or autoplay video delaying the promise | section_audit "cta"; manual (above the fold) | Visitors decide to stay within seconds (field heuristic) |
| SVC-05 | Proof strip | 4-8 client logos, press mentions, certifications or a review-platform rating, near the top | section_audit "social_proof_logos", "trust_badges" | Borrowed trust, scannable before any claim |
| SVC-06 | Benefits as outcomes | 3-6 cards: feature, then the outcome it buys, then a number when one exists | manual | Buyers pay for outcomes and will not translate features (field heuristic) |
| SVC-07 | Numbered process | 3-4 steps from first contact to delivered result, each with what happens and how long | section_audit "process_block" | Makes the purchase feel managed; matches "how does X work" answers |
| SVC-08 | Founder or expert block | Real photo (never stock), first and last name, role, story (why, for whom, since when); credentials that can be checked (registrations, certifications, years, results) linked to third-party profiles; link to the about page; the same profile URLs in Person `sameAs` (C-20) | section_audit "author_block"; social_placeholder; manual | E-E-A-T (measured: Google Search Quality Rater Guidelines); stock "teams" kill trust (field heuristic) |
| SVC-09 | Text block depth | 750+ words floor, raised to the competitor median when higher (C-08); H2s phrased as buyer questions (3+, C-13), each opened by a 2-4 sentence direct answer; covers what is included and excluded, for whom and not, price, duration, method, tools, guarantees, why this provider | thin_content, page_benchmark.py "words", no_question_h2, long_paragraphs | The semantic reservoir that ranks; also the GEO layer (field heuristic) |
| SVC-10 | Price shown or explained | Price, range or "from" in plain HTML text, with what drives it; if the price only comes after a call, say so and why; date it ("rates as of {month year}") when prices change | section_audit "price_in_text", "pricing_block" | Filters unqualified leads; the passage assistants quote for "how much does X cost" (field heuristic); 12 of 14 benchmarked coaching sites show a price (measured, Oct 2026) |
| SVC-11 | Qualification and coverage | "For / not for" stated; for local services, the service area (cities, response or travel time) and contact details (phone, address) as text | section_audit "contact_details", "opening_hours", "map_embed"; manual | Qualifies out bad leads and captures local intent |
| SVC-12 | Case result | 1+ case study or before and after with numbers, timeframe and date, linked to the full story when it exists | manual | The strongest asset a service business owns |
| SVC-13 | Reviews and rating | 3+ reviews as first name + situation + problem + result; video when available; never invented or embellished; rating shown with platform + count + date read ("4.9/5 Google, 312 reviews, read on 2 Oct 2026") | section_audit "reviews", "rating_summary", "video"; manual | Peer proof; a dated, counted rating is checkable, a bare star row is not; fake reviews are a legal risk |
| SVC-14 | FAQ of real objections | 3+ questions (5-8 for high-ticket services) from People Also Ask + sales objections, 2-4 sentence answers, text in the HTML | section_audit "faq"; C-21 | Feeds People Also Ask, AI Overviews and assistants; closes objections |
| SVC-15 | CTA cadence | Above the fold, then after benefits, process, reviews and at the end; one primary action (book, call, quote); click-to-call for trades | section_audit "cta"; no_cta_money | Readiness arrives at different points; one bottom CTA catches only the patient (field heuristic) |
| SVC-16 | Comparison with the alternatives | One HTML table versus the usual alternatives (doing it yourself, a freelancer, an in-house hire, another provider type), 5-8 buyer criteria, including one the alternative wins | section_audit "comparison_table"; no_table | Tables are the most extracted format in AI answers; 8 of 14 benchmarked coaching sites ship one (measured, Oct 2026) |
| SVC-17 | Guarantee or risk reversal, when one exists | Exact terms (duration, condition); no guarantee shown if none exists | section_audit "guarantee" | Risk reversal; vague guarantees read as traps |
| SVC-18 | Honest claims (C-24 for services) | Results promises carry a "results not guaranteed" disclaimer; superlatives ("n°1", "best", "leader") carry a source; regulated professions (law, health, finance, gambling) carry their legal notices and registrations; urgency only when real | claim_no_disclaimer, superlative_claim, gambling_notice_missing; manual | Your Money or Your Life scrutiny; advertising law (FTC endorsement guides, ARPP, EU consumer law) |
| SVC-19 | Self-sufficient, extractable page | Proof, process, FAQ and price in HTML text, not in a PDF, an image or a JS tab; key facts in stable sentences ("serves Lyon and 12 surrounding cities, response under 60 minutes") | likely_js_rendered (C-21); manual | Assistants quote only what they can read; service and product pages are about 13.7% of AI-cited pages (measured, single study) |
| SVC-20 | Sourced statistics and quotations | 1+ sourced statistic and 1+ expert or client quotation in the text block (C-14) | no_stats, citability counts | Quotations up to +41%, statistics up to +32% on GEO visibility (measured: Princeton GEO study) |
| SVC-21 | Mini silo and internal links | Breadcrumb Home > Services > service (C-19); links in from homepage, services hub, related posts (and footer if core); links out to the hub and sibling services; 2-3 related posts at the bottom, each linking back; descriptive anchors with the service keyword | breadcrumb_missing, generic_anchor, section_audit "internal_links"; manual (links in) | Concentrates relevance and equity on the money page; orphan money pages are a recurring finding (field heuristic) |
| SVC-22 | Service JSON-LD graph (C-18) | Service (name, serviceType, provider by `@id` to the Organization, areaServed, offers only when a price is shown) or LocalBusiness subtype for a local single-location business; Organization reference with `sameAs`; Person for the founder with `sameAs`; BreadcrumbList; FAQPage optional; no empty nodes; nothing marked up that the page does not show | schema_none, schema_fields, jsonld_invalid | Entity graph for AI engines (seo-schema-markup) |
| SVC-23 | No self-serving review markup | No Review or AggregateRating about your own business on your own site | manual (read the JSON-LD) | Ineligible per Google review snippet guidelines (measured) |
| SVC-24 | City and region pages carry unique local substance | Per city: 1+ local review, 1+ local project with a real photo, neighborhoods, response time, local rules or permits, local phone if any; city in title, URL, H1, meta, first paragraph, 1+ alt; links up to the region page and the main service page; side-by-side test passes | section_audit --type location; manual (side-by-side test) | Find-and-replace city pages are doorway pages (measured: Google spam policies) |

Rows SVC-12, SVC-16 and SVC-17 are "when available" rows: Not applicable is a valid status when the business has no case study yet, no relevant alternative or no guarantee, stated in the scorecard.

## Phase 2. Audit the existing page

Skip this phase for a new page; Phase 3 then sets the bar. Otherwise run both collectors on the live URL (and on each city page):

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/services/emergency-plumber-lyon/
python3 skills/seo-page-sections/scripts/section_audit.py --type service https://example.com/services/emergency-plumber-lyon/
python3 skills/seo-page-sections/scripts/section_audit.py --type location https://example.com/emergency-plumber-villeurbanne/
```

Map the output to the spec, then mark every C and SVC row Pass, Fail or Not verifiable, with the evidence:

| Script output | Spec rows |
|---|---|
| title_*, meta_*, h1_*, url_hygiene | C-01 to C-03, C-23, SVC-03 |
| kw_placement_low, kw_not_in_intro, kw_not_bold, no_bold, keyword_stuffing; the placement matrix and top terms | C-09 to C-11, SVC-02 |
| thin_content, no_question_h2, long_paragraphs, readability | C-08, C-12, C-13, SVC-09 |
| no_stats, citability counts (statistics, quotes, question headings) | C-14, SVC-20 |
| schema_none, schema_fields, jsonld_invalid; JSON-LD properties missing per type | C-18, SVC-22, SVC-23 |
| claim_no_disclaimer, superlative_claim, gambling_notice_missing | C-24, SVC-18 |
| social_placeholder, social_missing; social profiles found | C-20, SVC-08 |
| breadcrumb_missing, generic_anchor, no_cta_money, money page links | C-16, C-19, SVC-15, SVC-21 |
| section_audit blocks: cta, social_proof_logos, trust_badges, process_block, author_block, price_in_text, pricing_block, reviews, rating_summary, faq, comparison_table, guarantee, contact_details, internal_links | SVC-04 to SVC-17, SVC-21 |

Rows the scripts cannot judge stay manual: SVC-01 (SERP test), SVC-06 (benefits as outcomes), SVC-08 (is the photo real, are the credentials checkable), SVC-12, SVC-13 (are reviews real and formatted), SVC-19 (stable fact sentences), SVC-24 (side-by-side test), and links pointing in to the page (crawl or Search Console links report). The section detector is keyword based: a block it reports missing may exist under an unusual label, so open the page before writing a Fail.

## Phase 3. Benchmark the competitors

The master volume rule: match or exceed the competitors who currently rank, then fill their gaps. 750+ words is the floor that works in most service SERPs (field heuristic), but if the top 3 average 1800 words with pricing tables and case studies, 800 words will not be enough.

**Pick 3-5 competitors.** Search the target keyword (with the city for a local service) from the target location, then read the SERP like a brief:

| SERP signal | Implication for the page and the competitor set |
|---|---|
| Local pack and city-modified results dominate | Treat the page as local: city in title, H1, URL (SVC-24); take the service pages of the local pack providers; build the profile side with seo-local |
| Comparison listicles rank ("top 10 CRO agencies") | Add the proof depth listicles quote: client numbers, pricing, named differentiators; benchmark the providers the listicles name |
| Competitor service pages rank | Direct wireframe battle: benchmark them and exceed |
| Informational guides rank | The query is not transactional; cover it with a blog post (seo-content-blog) and aim the service page at the buyer query |
| People Also Ask and AI Overviews present | Harvest the questions for the FAQ (SVC-14) and the question H2s (SVC-09) |

Then ask two or three assistants (ChatGPT, Perplexity, Gemini or AI Overviews) "best {service} in {city}" or "recommend a {service} for {audience}", and add the providers they name, even when they rank lower: they show what assistants find quotable. Benchmark service pages against service pages, never against directories, marketplaces or the competitor's homepage.

**Run the benchmark** (client first, then the competitors):

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type service https://example.com/services/cro-agency/ https://rival1.com/cro/ https://rival2.com/services/cro/ https://rival3.com/shopify-cro/
```

**Read the output:**

- **Blocks half or more of the competitors have and the client does not**: each becomes a Fail on its SVC row, whatever the earlier audit said.
- **Schema types competitors use and the client does not**: input for SVC-22.
- **Client below the competitor median**: `words` sets the real SVC-09 target; `bold`, `placement`, `question_h`, `statistics`, `tables`, `money_links`, `videos` move the matching C and SVC rows up in priority.
- **Read by hand on each competitor**: section list, proof formats (logos, numbers, video reviews, case studies), how the price is shown, process durations, guarantee terms, credentials, comparison tables. The script counts blocks, it does not judge their quality; for a competitor's full title, heading tree and word count, run `seo_audit.py` on its URL.

Reference frequencies for coaching, training and consulting services (measured: Sorank benchmark of 14 coaching and training sites, October 2026, in seo-content-homepage/references/block-library.md section 5): price shown 12/14, comparison against alternatives 8/14, discovery call or application process 5/14, rating with review count 5/14, strong numbers-based proof 4/14, expert linked to a checkable third-party profile 4/14, money-back guarantee 3/14. The rare ones are the cheapest differentiators.

**Define the information gain.** Matching the median gets the page into the set; ranking and being cited needs something the others lack. Pick 1-3 items no benchmarked page has and write them into the Phase 4 brief, for example: a real price grid with what drives each price, original numbers from the business (median response time over the last 200 jobs, projects delivered, retention), a dated case study with before and after, a comparison table versus the alternatives, a named method, local data per city page, a cost calculator or checklist.

## Phase 4. Build

Read `references/service-page-wireframe.md` when drafting: it holds the fill-in skeleton with spec IDs per block, the city page and bookable-service variants, and the JSON-LD skeleton. Facts the owner has not confirmed stay as `{to confirm}`, never inventions.

### The wireframe: nine blocks in decision order

The order follows how a skeptical visitor decides: promise, proof, benefit, process, human, depth, peers, objections, action.

| # | Block | Job | Spec |
|---|---|---|---|
| 1 | Hero: promise + CTA above the fold | Pass the 5-second test | SVC-04, SVC-02 |
| 2 | Client and press logos | Borrowed trust, instantly scannable | SVC-05 |
| 3 | Benefits (outcomes, not features) | Answer "what do I get" | SVC-06 |
| 4 | How it works, 3-4 numbered steps | Reduce perceived risk and effort | SVC-07 |
| 5 | About the founder: real photo + story | E-E-A-T and human connection | SVC-08 |
| 6 | SEO text block, 750+ words (with price, for / not for, comparison table) | The semantic reservoir that ranks | SVC-09, SVC-10, SVC-11, SVC-16, SVC-20 |
| 7 | Client reviews (+ case result, guarantee) | Peer proof in the buyer's words | SVC-12, SVC-13, SVC-17 |
| 8 | FAQ, 3+ questions | Kill the last objections | SVC-14 |
| 9 | Final CTA + 2-3 related blog posts | Convert or keep them in the silo | SVC-15, SVC-21 |

**1. Hero.** State the outcome the client gets, in their words, with the primary keyword in the H1. Why: most visitors decide to stay or bounce within seconds; if they must scroll to learn what the page sells, the page loses.

**2. Logo strip.** Client logos, press mentions, certifications, review-platform ratings. Why: visitors scan for evidence that people like them already trust this business; logos deliver that faster than any sentence.

**3. Benefits.** Translate every feature into what the client obtains: "weekly report" becomes "you know exactly what changed and why, every Monday". Why: buyers pay for outcomes; features force them to do the translation themselves, and most will not.

**4. How it works.** Each step one short paragraph. Why: a clear process makes the purchase feel reversible and managed; numbered steps also match how AI assistants and featured snippets present "how does X work" answers.

**5. About the founder.** Why: Google's quality rater guidelines evaluate experience and trustworthiness, and a named, visible human is concrete evidence (measured: E-E-A-T in Google's Search Quality Rater Guidelines). On the conversion side, a real face with real imperfections connects better than polished stock imagery (field heuristic: stock-photo "teams" are a recurring trust killer in audits). Credentials an assistant can cross-check on third-party profiles become entity facts; claims it cannot check are ignored.

**6. SEO text block.** Structured with H2/H3 subheadings. Service pages are conversion-first up top, but Google needs substantial text to understand and rank the page, and this block carries that load without hurting the sections above it. Cover, as question-form H2s each opened by a direct 2-4 sentence answer: what the service includes (deliverables, scope, what is excluded); who it is for, and who it is not for; how much it costs and what drives the price; how long it takes, from start to delivered result; method, tools and guarantees; why this provider, a proof recap with numbers. Place the comparison table versus the alternatives under the "why this provider" or "how much" question.

**7. Reviews.** Format: "Marc, bakery owner in Lyon: bookings doubled in 3 months". Video reviews outperform written ones (field heuristic). Never invent or embellish testimonials: fake reviews are a legal risk in many markets and a trust risk everywhere.

**8. FAQ.** Answer each in 2-4 direct sentences. FAQ rich results were restricted to government and health sites in August 2023 and fully retired for all sites on May 7, 2026 (measured: Google, see Sources), but the content still feeds People Also Ask, AI Overviews and assistant answers, and it closes real objections on the page. Write objections (price, timeline, what if it does not work, how to start), not definitions.

**9. Final CTA + related articles.** Repeat the CTA, then link 2-3 supporting blog posts on the same topic, each linking back. This builds a mini silo, concentrating topical relevance and link equity on the money page (architecture: seo-internal-linking).

**CTA placement.** One CTA above the fold, then after benefits, after the process, after reviews and at the end. Vary the framing (book, call, get a quote) but keep one primary action (field heuristic: pages with one bottom CTA are a recurring conversion finding in audits).

**Adapt the wireframe to the business type.** The 9 blocks stay; the emphasis shifts:

| Business type | Keep everything, plus |
|---|---|
| Agency, consultant | Case results with numbers in blocks 2-3, portfolio links, team credentials |
| Trade (plumber, electrician, roofer) | Click-to-call as the primary CTA, emergency hours in the hero, service-area list, photos of real jobs |
| Solo professional (physio, coach, doctor, lawyer) | Block 5 (founder bio) is the page's lead sales argument, not a footnote: the buyer is choosing a person, so the named-and-photographed practitioner is the differentiator. Make the bio prominent, with credentials, registrations and a real story (field heuristic) |
| Clinic, lawyer, regulated profession | Practitioner credentials and registrations in block 5, claims reviewed for regulatory compliance and legal notices (SVC-18), consultation-booking CTA |
| SaaS or productized service | Demo or trial CTA, integration logos, security and compliance proof, transparent pricing table. Extend one service = one page into one target sector = one page (e.g. "for construction firms"), one persona = one page and one feature = one page: tighter specialization wins more long tail and converts better (field heuristic) |

### Copy rules

- **Bolding and placement (SVC-02).** Service keyword bold once in the first paragraph, then one bold phrase every 100-150 words on a number, an outcome or a key fact; never whole sentences, never decoration. Keyword (+ city) within the first 100 words: "Looking for an **emergency plumber in Lyon**? ...". Density under 2.5%, brand aside.
- **Numbers everywhere, each attributed.** Every block carries a figure (clients, years, response time, price, timeframe) and says where it comes from (client, platform, date). Unattributed numbers read as marketing.
- **Paragraphs of 40-80 words**, each understandable alone: assistants lift isolated passages (C-12).
- **Punctuation, non-negotiable (C-25).** Never leave an em dash (U+2014) or an en dash (U+2013) in copy that goes live on a client site. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and one is enough for a prospect, or the client, to file the page as machine output. The rule covers every field you deliver: page copy, H1 and H2s, FAQ answers, testimonials you format, title tag, meta description, alt text, CTA labels, schema strings. Sweep the finished draft for both characters before handing it over. Hyphens in compound words and ranges written with "to" are untouched.

### Metadata pattern (SVC-03)

| Element | Pattern | Example |
|---|---|---|
| Title | Service keyword + brand (+ city if local), about 50-60 characters | Emergency Plumber in Lyon \| Dupont Plomberie |
| H1 | The service keyword, phrased for humans, one per page | Emergency plumber in Lyon |
| Slug | Short, keyword only, no dates or stop words | /emergency-plumber-lyon/ |
| Meta description | Handwritten, 160 characters or fewer: promise + proof + call to action | On site in under 1 hour, 24/7. 4.9/5 from 312 clients. Call now. |
| First paragraph | Primary keyword (+ city) within the first 100 words, bolded once | "Looking for an emergency plumber in Lyon? ..." |
| Image alts | Describe the image; include service and city where natural, never on every image | "Dupont Plomberie technician repairing a burst pipe in a Lyon apartment" |

Why handwritten metas: Google rewrites weak ones, and the meta is ad copy for the click, not a ranking factor. The 160-character limit is a display truncation heuristic, not a Google rule.

### Multi-area services: region and city pages (SVC-24)

For a service business covering several cities, build a hub-and-spoke structure:

1. One parent region page targeting "service + region".
2. One child city page per city with real search demand, targeting "service + city".
3. Parent links to all children; each child links back to the parent and to the main service page.

The parent region page covers: the full city list with links to every child page, region-wide proof (total clients, years in the region), how the business covers the territory (dispatch, travel times, local teams), and a region-level FAQ.

Each city page must contain genuinely unique content: testimonials from clients in that city, completed projects with local photos, city specifics (neighborhoods served, response times, local regulations or permits), local phone number if one exists, and the city in the title, URL, H1, meta description, first paragraph and image alts.

**Explicit Google guidelines risk:** generating city pages by find-and-replace on the city name produces doorway pages, which violate Google's spam policies and can trigger manual actions (measured: Google spam policies, see Sources). The test: put two city pages side by side; if only the city name differs, they are doorways. Programmatic generation is acceptable only when each page receives unique local substance. If a city has nothing unique to say and no demand, do not create the page.

### Schema and internal links (SVC-21 to SVC-23)

- One `@graph`: Service with `provider` pointing by `@id` to the Organization (defined once, on the homepage, with `sameAs` to every real profile), `areaServed`, `serviceType`, and `offers` only when the price is on the page; a LocalBusiness subtype instead when the page is the local business itself; the founder as Person with `jobTitle` and `sameAs` (LinkedIn, registries); BreadcrumbList (Home, Services, this service). Skeleton in the reference; eligibility details in seo-schema-markup.
- FAQPage markup is optional: harmless, but it earns no rich result since Google retired FAQ rich results in May 2026.
- No Review or AggregateRating about your own business (SVC-23), no empty properties, nothing the page does not show.
- Link to the new page from the homepage, the services hub, relevant blog posts and the footer if the service is core, with descriptive anchors containing the service keyword, never "click here" or "learn more" alone.

### Acceptance test

Re-run the Phase 2 and Phase 3 commands on the published or staged URL. The page is done when:

- `seo_audit.py` shows no critical or high finding; BOLD above zero with the service term among the samples; PLACEMENT at 60% or more; no `schema_none`, `schema_fields` or `jsonld_invalid`; SOCIAL shows real profiles and no placeholders; no `claim_no_disclaimer` or `superlative_claim`; no `em_dashes`.
- `section_audit.py --type service` finds cta, process_block, author_block, price_in_text, reviews, faq and breadcrumb, plus every block that half or more of the benchmarked competitors have.
- `page_benchmark.py` shows `words` at or above the competitor median, and the information gain items are on the page.
- Every C and SVC row is Pass, Not applicable with a reason, or a written owner decision. Then check the GEO layer below and AI crawler access (seo-technical).

## GEO layer

AI assistants now recommend providers directly: "best CRO agency for Shopify", "recommend a dentist in Geneva", "who can redesign my restaurant website". The answer is assembled from pages the assistant can read and trust. A service page earns those citations when it is self-sufficient: a model reading it in isolation can extract who the provider is, what exactly they do, for whom, how the process works, what it costs and why they are credible. Apply all six before publishing:

1. **Make the page self-sufficient (SVC-10, SVC-19).** Proof, process, FAQ and price or price range must live in the page's HTML text, not in a PDF, an image or a "contact us for pricing" dead end. Product and service pages account for roughly 13.7% of pages cited by AI assistants in a large citation analysis (measured: almcorp.com/blog/ai-citations-listicles-articles-product-pages/), so money pages do get quoted, but only when they contain quotable substance.
2. **Write each H2 of the text block as a real question with a direct answer (SVC-09).** Open every section with a 2-4 sentence answer a model can lift verbatim, then elaborate. Full passage-level writing rules: geo-visibility skill.
3. **Add sourced statistics and expert quotations to the text block (SVC-20).** In the GEO benchmark, adding quotations lifted generative visibility by up to 41% and adding statistics by up to 32% on the benchmark's visibility metrics (measured: Princeton GEO study, arxiv.org/abs/2311.09735). Cite real sources; invented numbers destroy trust with both readers and models.
4. **Make E-E-A-T machine-readable (SVC-08, SVC-22).** Person schema for the founder (name, jobTitle, sameAs to LinkedIn and registries), Organization schema with sameAs to every official profile. Implementation: seo-schema-markup skill.
5. **State facts in stable, extractable sentences (SVC-19).** "Dupont Plomberie serves Lyon and 12 surrounding cities, with a response time under 60 minutes" is citable; a hero animation saying "We move fast" is not.
6. **Check AI crawler access (C-21, C-22).** GPTBot, ClaudeBot, PerplexityBot and similar agents must be able to fetch the page; rendering and robots rules live in the seo-technical skill. Measuring whether assistants actually cite the page: geo-tracking skill.

## Deliverable

```markdown
## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable / Not applicable) | Evidence |
(every C row and SVC-01 to SVC-24; the six GEO layer items map to their SVC rows)

## 2. Audit findings
(seo_audit.py SEO and GEO scores, high and medium findings; section_audit.py blocks; or "new page")
| Wireframe block | Present | Gap | Fix | Priority |
| 6. SEO text block | Partial | 280 words vs 1600 median, no pricing | Question-form H2s, add price range | High |
| 8. FAQ | No | Zero questions answered on page | 4 questions from People Also Ask | Medium |
(all 9 blocks; then the prioritized fix list: high = blocks ranking or conversion, medium, low)

## 3. Competitor benchmark
(SERP read and how the competitors were picked; page_benchmark.py table; blocks and schema types the client lacks; metrics below the median; the 1-3 information gain items chosen)

## 4. Build
(target keyword and intent; metadata table; the copy block by block in wireframe order with H1/H2/H3 marked, bolding visible and CTA positions flagged; FAQ 3-5+ questions; internal link plan with the 2-3 supporting posts; JSON-LD graph; city pages when relevant; placeholders {to confirm} for unverified facts)

## 5. Acceptance
(scripts re-run: remaining findings, each either fixed or a written owner decision; GEO layer pass)
```

When the user asks only for an audit, deliver parts 1 to 3 plus the fix list, and keep part 4 to the change list. When the page is new, part 2 reads "new page" and part 3 sets the bar.

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| One page listing all services | Diluted relevance, wins no SERP | One page per service + hub page (SVC-01) |
| Title like "Services \| Brand" | Carries zero keyword signal | Service keyword first, brand last (SVC-03) |
| Features instead of benefits | Buyer must translate, most will not | Rewrite every feature as the outcome obtained (SVC-06) |
| Stock photos, anonymous team | No E-E-A-T evidence, no human trust | Real founder photo + named story + checkable credentials (SVC-08) |
| 250 words vs 1500-word competitors | Outgunned on coverage | Benchmark, close the gap to the median (SVC-09) |
| Zero bold, or whole bold sentences | No visible relevance, or noise | Keyword bold in the intro, one fact every 100-150 words (SVC-02) |
| Single CTA at the bottom | Misses every early-ready visitor | CTA above the fold + after each major section (SVC-15) |
| City pages by find-and-replace | Doorway pages, Google spam policy violation | Unique local proof per city or no page (SVC-24) |
| Vague testimonials ("Great service!"), bare star row | Zero credibility, zero citability | First name + situation + problem + result; rating with platform, count, date (SVC-13) |
| No price information | Loses the "how much" SERP and AI answers, attracts unqualified leads | Price or range in plain HTML, or why it comes after a call (SVC-10) |
| "Best agency in Lyon", "guaranteed results" | Unbacked superlative, undisclosed promise | Source or remove; add the disclaimer (SVC-18) |
| Self-serving review schema | Ineligible per Google guidelines, wasted or risky markup | Mark up reviews only where eligible (SVC-23) |
| Footer icons pointing to `linkedin.com/` | Broken entity link | Real profile URLs, same in `sameAs` (C-20) |
| Text block behind JS tabs or accordions | Content may not be rendered or weighted | Server-rendered visible text (SVC-19, seo-technical) |
| FAQ written for markup, not objections | Answers nothing a buyer asks | Source questions from People Also Ask + sales calls (SVC-14) |

## Sources

- GEO: Generative Engine Optimization, Aggarwal et al., Princeton et al. (KDD 2024): arxiv.org/abs/2311.09735 (measured: +41% quotations, +32% statistics on benchmark visibility metrics)
- Share of AI citations going to product and service pages (13.7%): almcorp.com/blog/ai-citations-listicles-articles-product-pages/ (single-source study, not independently replicated)
- Google spam policies, doorway pages: developers.google.com/search/docs/essentials/spam-policies (official)
- Google Search Quality Rater Guidelines, E-E-A-T and Your Money or Your Life: static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf (official)
- Google title link documentation: developers.google.com/search/docs/appearance/title-link (official)
- Google FAQ rich results restriction, August 2023 (fully retired for all sites May 7, 2026): developers.google.com/search/blog/2023/08/howto-faq-changes (official)
- Google review snippet guidelines (self-serving reviews ineligible): developers.google.com/search/docs/appearance/structured-data/review-snippet (official)
- Google structured data policies (markup must match visible content): developers.google.com/search/docs/appearance/structured-data/sd-policies (official)
- FTC Endorsement Guides (testimonials with results): ftc.gov/legal-library/browse/rules/guides-concerning-use-endorsements-testimonials-advertising (official)
- Sorank benchmark of 14 coaching and training sites, October 2026: seo-content-homepage/references/block-library.md section 5 (measured, one niche, generic lessons)
- Field heuristics: 115+ real agency audits of service-business websites, 2024-2026 (observational, labeled as such throughout)
