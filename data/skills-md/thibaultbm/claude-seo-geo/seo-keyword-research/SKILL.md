---
name: seo-keyword-research
description: "Get a keyword map and an AI prompt panel grounded in how buyers actually search. Input: a site, niche, or seed topics (plus Google Search Console if available). Output: keywords mapped one-to-one to intent and pages, quick wins, a cannibalization check, an on-page placement matrix, and a 50-100 buyer prompt panel for ChatGPT, Perplexity, and Google AI Mode. Works without paid tools. Use for keyword research, search intent, keyword mapping, cannibalization, content gaps, prompt research, or deciding what to write and which queries to target."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# SEO Keyword Research and AI Prompt Research

Keyword research matches the exact language buyers use to the pages a site offers. In 2026 it produces two deliverables, not one:

1. A keyword map: every target query validated against real usage, assigned to one search intent and one page.
2. A buyer prompt panel: 50-100 questions buyers ask AI assistants (ChatGPT, Perplexity, Google AI Mode, Claude, Gemini), each mapped to a page that can earn the citation.

Everything in this skill works with free sources: Google Search Console, Google autocomplete, People Also Ask, competitor sitemaps, Reddit, Wikipedia, and the words customers already use in support tickets and sales calls. Paid tools are an optional final layer, never a prerequisite.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed.

## When to use this skill

Use this skill when the user:

- Asks which keywords to target, what to write about, or how people search for their product or service.
- Wants a content plan, an editorial calendar, a topic cluster, or a content gap analysis.
- Suspects two pages compete for the same query (cannibalization).
- Wants quick wins from existing Google Search Console data.
- Asks which prompts buyers type into ChatGPT or Perplexity (prompt research, query fan-out, AI topic selection).
- Is about to brief any new page: blog post (seo-content-blog), product page (seo-content-product-page), service page (seo-content-service-page), or collection page (seo-content-collection-page).

Hand off afterwards: the prompt panel built here is the measurement input for geo-tracking, and page-level citability work belongs to geo-visibility.

## Quick start (30 minutes)

When time is short, run this compressed loop; the full workflow below scales it.

1. Export Google Search Console queries at average positions 5-20: that is the quick win list (10 minutes).
2. Type the top 5 candidate keywords into Google; harvest autocomplete and People Also Ask (10 minutes).
3. Run one cannibalization test on the two most similar pages of the site (5 minutes).
4. Draft 20 buyer prompts with the four prompt patterns from the GEO layer (5 minutes).

The output of the quick start is a defensible shortlist; the full workflow turns it into a complete map.

## Core principles

### 1. Nobody types what you think they type

The most frequent finding in the field (field heuristic from 115+ agency audits): teams target their internal vocabulary while buyers type something else entirely. A consultancy writes "digital transformation enablement"; the buyer types "how to digitize invoices". A keyword is an empirical fact about other people's language, never a branding decision.

Validate every candidate keyword against at least two independent evidence sources before it enters the map:

- Google autocomplete (only shows queries people actually type)
- People Also Ask boxes (questions Google has verified at scale)
- Related searches at the bottom of the results page
- Reddit and niche forum threads (unfiltered buyer vocabulary)
- Customer words: support tickets, sales call notes, onboarding survey answers

If a keyword appears in none of these sources, treat it as jargon and find the variant that does appear.

Granularity matters: a keyword is a short expression people actually type, not the full article title. "how to invoice a client in germany" is a keyword; "the complete 2026 guide to invoicing your first international client in germany" is a headline that matches a query with zero volume. Title the page around the keyword, do not promote the title to a keyword.

### 2. One keyword, one intent, one page

Google ranks one page per intent per site in most cases, and a page built for two intents serves neither. Every keyword in the map points to exactly one URL, and every URL targets exactly one primary intent. Secondary keywords are allowed only when they share the primary intent (verified by the cannibalization test in step 6).

### 3. Long tail and head work together

The long tail (specific, lower-volume queries) converts better and ranks faster because competition is thin. The head (broad, high-volume queries) takes quarters of authority building. Start with the long tail to generate revenue now, plan head terms as a program. Two traps frame this rule:

- Ranking first on a query nobody types is worth nothing. Zero-volume trophies are a recurring audit finding (field heuristic from 115+ agency audits): validate demand before celebrating positions.
- No keyword strategy compensates for broken technical foundations. If the site has crawl, indexation, or rendering problems, fix them first with seo-technical; new pages would inherit the same invisibility.

### 4. Keywords and prompts are two maps of the same demand

Classic engines rank pages for queries; AI assistants decompose a prompt into subqueries and sample a handful of sources. The same buyer generates both. Research them together: the keyword map drives pages and rankings, the prompt panel (GEO layer below) drives citations, and geo-tracking measures the panel monthly.

## Workflow

Run the steps in order. Steps 1 to 4 collect evidence, steps 5 to 7 turn evidence into page decisions, the GEO layer extends the map to AI assistants.

### Step 1: Pull quick wins from Google Search Console

Why first: GSC is the only free source showing queries where Google already considers the site relevant, with real impression and click counts instead of tool estimates. Improving position 8 to position 3 takes weeks; building position 3 from nothing takes months.

1. Open Performance, Search results, date range last 3 months (12 for seasonal businesses).
2. Filter queries with average position between 5 and 20, sort by impressions.
3. Add the Pages dimension to identify which URL ranks for each query.
4. Treat these as quick wins: the page already ranks, so it needs the full placement matrix (step 7), stronger internal anchors (seo-internal-linking), or a content refresh, not a new page.

| Position band | Diagnosis | Action |
|---|---|---|
| 1-4 | Working | Protect, refresh on a schedule |
| 5-10 | Quick win | Complete the placement matrix, add internal anchors |
| 11-20 | Near miss | Deepen content, add one section per related People Also Ask question |
| 21+ | Weak signal | Re-evaluate as a brand new keyword |

Also filter GSC queries containing "how", "what", "why", "vs", "best": they seed both blog topics and the prompt panel.

Prioritize by commercial value, not raw impressions. A high-volume informational query that ranks well but sends visitors who never buy is worth little; a lower-volume query with a strong click-through rate and buyer intent is worth more. Weight the quick win list toward queries that bring customers, not toward the biggest impression counts.

### Step 2: Validate the real query language

Why: this step kills the jargon problem from principle 1 and it costs nothing. Examples of the gap it closes:

| Internal jargon | What buyers actually type | Where the evidence shows up |
|---|---|---|
| revenue enablement platform | sales crm for small business | autocomplete, Reddit |
| managed WordPress maintenance | wordpress support monthly cost | autocomplete, People Also Ask |
| generative engine optimization services | how to appear in chatgpt answers | People Also Ask, forums |

Method per source:

- Autocomplete: type the seed keyword and record suggestions, then "seed + a" through "seed + z", then question prefixes ("how seed", "best seed", "seed vs"). Use a clean browser profile to limit personalization.
- People Also Ask: expand 3-4 questions so Google loads more, harvest the whole tree. Each PAA question is a candidate H2 (geo-visibility turns question H2s into citable answer blocks).
- Related searches: bottom of the results page, usually intent variants of the seed.
- Reddit and forums: search "site:reddit.com" plus the topic, copy exact thread titles and complaint phrasings, sort by recent for fresh vocabulary.
- Customer words: pull the last 50 support tickets and sales call notes, extract the nouns and verbs prospects use before buying. These phrases are simultaneously keywords, prompt phrasings, and ad copy.
- Google Trends (free): a separate validation, not a phrasing source. Before committing to a niche or market, check that interest in the theme is rising rather than declining over 12 to 24 months, and compare relative interest between candidate terms and regions. Use it to confirm demand direction; autocomplete and People Also Ask confirm the exact words people type.

### Step 3: Reverse-engineer competitor coverage

Why: a competitor's URL inventory is their keyword strategy published in plain sight, and reading it requires no tool.

1. Fetch /sitemap.xml for 3-5 competitors (check /robots.txt when the sitemap is elsewhere).
2. Classify URLs by directory pattern: /blog/, /features/, /integrations/, /vs/, /alternatives/, /templates/, /glossary/, /tools/.
3. Read patterns as strategies: 30 pages under /vs/ means 30 comparison keywords; a /glossary/ directory means definitional coverage (definitional pages also feed AI citations, see geo-visibility).
4. Diff against the site's own inventory. Every pattern a competitor maintains and the site lacks is a pre-validated gap: a competitor already invested to prove the demand.

### Step 4: Structure topics with Wikipedia

Why: a Wikipedia table of contents is an editorially curated decomposition of a topic into subtopics, which is exactly what a pillar page outline needs and close to what AI engines produce during query fan-out. Open the topic's article, copy the table of contents as the candidate H2 list, and check the "See also" section for adjacent topics that deserve their own pages.

### Step 5: Map every keyword to one intent and one page

Why: intent decides the page type, and the page type decides which content skill builds it. Misreading intent wastes the entire production budget: a blog post can almost never outrank product pages on a transactional query, whatever its quality.

| Intent | Query signals | Target page type | Build with |
|---|---|---|---|
| Transactional | buy, pricing, hire, agency, software, tool, near me | Product or service page | seo-content-product-page, seo-content-service-page |
| Informational | how, what, why, guide, examples, checklist | Blog article that links to the commercial page | seo-content-blog, seo-internal-linking |
| Commercial investigation | best, top, vs, alternatives, review, worth it | Comparison page or listicle | seo-content-blog |
| Navigational | brand and product names | Brand pages, homepage | geo-visibility (entity consistency) |

Two non-negotiables:

- Every informational article links to the commercial page it supports. An article that converts nobody and links to nothing is decoration. This internal link is also how the commercial page accumulates authority (seo-internal-linking).
- Local queries follow the local pattern: keyword + city present in title, URL, H1, meta description, first paragraph, and image alt. Full pattern and Google Business Profile work in seo-local.

When intent is ambiguous, read the live results page: what Google already ranks is its verdict on intent, and it overrules any opinion in the room.

- Mostly product and category pages: transactional, build a commercial page.
- Mostly articles and guides: informational, build a blog post.
- Map pack present: local intent, apply seo-local.
- Mix of product pages and listicles: commercial investigation, a comparison listicle can win.
- Video carousel prominent: produce or embed video alongside the page (also a GEO surface, see geo-visibility).

### Step 6: Run the cannibalization test

Why: two pages targeting the same intent split internal links and ranking signals, and the merged page usually outranks both originals (field heuristic from 115+ agency audits). The test costs two searches and settles every "should these be separate pages" debate with evidence instead of opinion.

1. Search variant A in Google and note the top 10 URLs.
2. Search variant B and compare.
3. Largely the same results: same intent, one page only. Merge the content into the stronger URL and 301 the weaker one to it.
4. Clearly different results: different intents, two pages are justified.

Typical symptom that triggers this test: rankings for one query flip-flopping between two URLs week over week.

Cannibalization is a within-site problem: two pages of the SAME site competing for one intent. Two separate properties on the same theme (for example a brand site plus a standalone comparator) do not cannibalize each other; they occupy two distinct SERP slots and can both rank. The standalone comparator site strategy: seo-internal-linking.

### Step 7: Build the placement matrix

Why: ranking signals concentrate in a few locations. A keyword absent from these locations is a keyword the page does not target, whatever the body text says. This matrix is the recurring on-page checklist from 115+ agency audits (field heuristic).

For each of the 5 priority keywords, verify presence in all 8 placements:

| Placement | Check |
|---|---|
| Title tag | Keyword present, front-loaded when natural |
| H1 | Present once |
| At least one H2 | Present, phrased as a question where natural |
| URL slug | Present, short, descriptive, natural language |
| First paragraph | Present, in bold |
| Meta description | Present |
| Image alt text | Present on at least one relevant image |
| Inbound internal anchors | 2-3 internal links use the keyword as anchor text (seo-internal-linking) |

Audit existing pages against this matrix at scale with the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py).

### Step 8 (optional): Scale with paid tools

Only after the free workflow, because tools refine prioritization but cannot replace step 2: no volume metric tells you whether a phrase is the buyer's language or your jargon.

| Tool | What it adds | Access |
|---|---|---|
| DataForSEO | Search volumes and SERP data programmatically | API, pay per call |
| Ahrefs | Volumes, keyword difficulty, competitor keyword lists | Subscription, MCP server available |
| Semrush | Volumes, difficulty, rank tracking at scale | Subscription, MCP server available |

If an MCP server for one of these is connected, use it to enrich the existing map with volumes and difficulty; never to generate the map from scratch.

## GEO layer: prompt research

Prompt research is keyword research for AI assistants, and it is a separate discipline because assistants process queries differently: they explode one prompt into multiple subqueries, retrieve a small set of sources per subquery, and synthesize one answer. Google documents this mechanism as query fan-out for its AI features (https://developers.google.com/search/docs/appearance/ai-features), with a practical optimization guide at https://searchengineland.com/guide/how-to-optimize-for-query-fan-out.

Two consequences change targeting entirely:

1. AI engines sample roughly 10-20 sources per answer instead of ranking 1000. A page that answers exactly one ultra-niche subquestion often wins its citation against a bigger generalist page (field heuristic from 115+ agency audits). Niche precision beats broad authority more often in AI answers than in classic rankings.
2. Semantic similarity between the page title and the fan-out subqueries is the strongest measured citation predictor in Ahrefs' study of 1.4M prompts (https://ahrefs.com/blog/why-chatgpt-cites-pages/). Title the page like the subquestion it answers.

Example fan-out for "best invoicing software for freelancers":

| Likely subquery | Page that can win the citation |
|---|---|
| invoicing software pricing comparison | Comparison table page |
| invoicing software for freelancers in [country] | Localized landing page |
| free vs paid invoicing tools | Blog comparison |
| how freelancers send compliant invoices | How-to article with an answer-first section |

### Build the buyer prompt panel (50-100 prompts)

Generate prompts with these four patterns, then replace the placeholders with the real language collected in step 2:

| Pattern | Example | Maps to |
|---|---|---|
| best [category] for [use case] | best invoicing software for freelancers | Comparison listicle |
| [brand] vs [competitor] | BillingKit vs FreshBooks | Versus page |
| is [brand] worth it, [brand] reviews | is BillingKit worth it | Reviews coverage, third-party review profiles |
| how to [job to be done] | how to invoice a client in Germany | Blog article with answer-first sections |

Sources for real prompt phrasing:

- ChatGPT follow-up suggestions and Perplexity related questions on seed topics.
- AlsoAsked (free tier) for question trees.
- Sales calls and demo recordings: the questions prospects ask out loud are the prompts buyers type.
- Support tickets: pre-sale questions, verbatim.

Aim for 50-100 prompts. Below 50, the share of voice numbers computed in geo-tracking are too noisy to act on; above 100, monthly manual measurement stops being sustainable.

### Map prompts to pages

For each prompt record: prompt, pattern, engines where it matters, current answering page (or none), action. Possible actions:

- Create a comparison or versus page (commercial investigation prompts).
- Add an FAQ section answering the prompt verbatim.
- Add a definitional section (a clean "X is Y" sentence a model can quote).
- Restructure an existing page answer-first (rules and thresholds in geo-visibility).

Freeze the finished panel and hand it to geo-tracking unchanged, so visibility numbers stay comparable month over month.

## Rules and thresholds

| Rule | Threshold | Why |
|---|---|---|
| Real language validation | Keyword present in at least 2 free evidence sources | Internal jargon attracts zero searches |
| One keyword, one page | 1 intent = 1 page, no exceptions | Two pages on one intent cannibalize each other |
| Cannibalization verdict | Same top 10 for both variants = merge + 301 | The live results page is the ground truth for intent |
| Quick wins first | Work GSC positions 5-20 before creating new content | Existing relevance compounds fastest |
| Long tail and head | Long tail now, head as a quarterly program | Long tail converts and ranks fast; head needs authority |
| Zero-volume trap | Demand evidence required before targeting | First place on a query nobody types is worth nothing |
| Volumes | Never invent numbers; leave blank without a tool | Fake precision corrupts prioritization |
| Prompt panel size | 50-100 prompts, 4 patterns, real phrasing | Smaller panels make geo-tracking metrics noise |
| Title similarity | Page title phrased like the subquery it answers | Strongest measured citation predictor (Ahrefs, 1.4M prompts) |

## Output format

Deliver three artifacts, in this order:

1. Keyword map table. Columns: keyword, intent, evidence (which free sources validated it), volume (paid tool value or blank, never invented), target URL (existing or to create), page type, priority (quick win, short term, long term).
2. Placement matrix for the top 5 keywords against the 8 placements, pass or fail per cell.
3. Prompt panel table. Columns: prompt, pattern, phrasing source, target engines, answering page, action. Label it explicitly as the measurement input for geo-tracking.

Example keyword map rows:

| Keyword | Intent | Evidence | Volume | Target URL | Page type | Priority |
|---|---|---|---|---|---|---|
| invoicing software for freelancers | Commercial investigation | autocomplete, PAA, Reddit | blank (no tool) | /best-invoicing-software-for-freelancers (create) | Listicle | Short term |
| how to invoice a client in germany | Informational | PAA, support tickets | blank (no tool) | /blog/invoice-client-germany (create) | Blog article | Short term |
| invoice generator | Transactional | autocomplete, GSC position 12 | blank (no tool) | /tools/invoice-generator (exists) | Tool page | Quick win |

Example prompt panel rows:

| Prompt | Pattern | Phrasing source | Engines | Answering page | Action |
|---|---|---|---|---|---|
| best invoicing software for freelancers | best for | autocomplete, sales calls | chatgpt, perplexity, google-aio | none | create listicle with comparison table |
| billingkit vs freshbooks | vs | ChatGPT follow-up suggestions | chatgpt, gemini | none | create versus page |
| how to invoice a client in germany | job to be done | support tickets | chatgpt, claude | /blog/invoice-client-germany | restructure answer-first (geo-visibility) |

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Targeting internal jargon | Zero impressions forever | Step 2 validation, customer words |
| Inventing search volumes | Fake prioritization | Leave volume blank; validation is mandatory, volume is optional |
| Many intents on one page | Diluted relevance, ranks for nothing | One intent per page, split |
| Separate pages for same-intent variants | Cannibalization, flip-flopping rankings | Two-search SERP test, merge + 301 |
| Only head keywords | No traffic for months, morale collapse | Long tail first, head as a program |
| Only long tail | Growth ceiling | Plan head terms with pillar and cluster pages |
| Blog posts that link to nothing | Traffic without revenue | Every article links to the commercial page it supports |
| Chasing keywords on a broken site | New pages inherit the invisibility | Fix seo-technical issues first |
| Skipping prompt research | Invisible in AI answers while competitors map the prompts | Build the 50-100 prompt panel |
| Rewriting the prompt panel monthly | No comparable trend data | Freeze the panel, hand it to geo-tracking, revise quarterly at most |

## Cross-references

- seo-geo-audit: run the bundled audit script (scripts/seo_audit.py) to check placements and on-page state at scale.
- seo-technical: fix crawl, indexation, and JS rendering before chasing rankings.
- seo-content-blog, seo-content-product-page, seo-content-service-page, seo-content-collection-page: build the pages this map calls for.
- seo-internal-linking: inbound anchors required by the placement matrix.
- seo-local: the keyword + city pattern in full.
- geo-visibility: make the mapped pages citable by AI engines (canonical citability rules).
- geo-tracking: measure the prompt panel monthly (canonical measurement protocol).

## Sources

- Google Search Central, AI features and your website (official query fan-out documentation): https://developers.google.com/search/docs/appearance/ai-features
- Search Engine Land, How to optimize for query fan-out: https://searchengineland.com/guide/how-to-optimize-for-query-fan-out
- Ahrefs, study of 1.4M prompts on why ChatGPT cites pages (title similarity as top predictor, measured): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Items marked "field heuristic from 115+ agency audits" are practitioner observations from agency audit calls (2024-2026), not controlled studies. Treat them as strong priors to verify on each site, not as laws.
