---
name: geo-visibility
description: "Get cited and recommended by AI engines (ChatGPT, AI Overviews and AI Mode, Perplexity, Claude, Gemini). Input: a page or piece of content. Output: passage-level citability fixes (answer-first H2 blocks, self-contained chunks, definitions, sourced stats, comparison tables), a 5-pillar GEO score (0-100), an AI-crawler visibility check, and entity plus third-party consistency. Repo reference for citability. Use for GEO, AEO, LLM SEO, AI citations, citability, llms.txt, entity SEO, or why competitors appear in AI answers and you do not."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# GEO Visibility: Getting Cited by AI Engines

Generative Engine Optimization (GEO) is the work of becoming a source AI engines retrieve, quote, and recommend. This skill is the canonical reference in this repo for passage-level citability rules: when another skill needs "how to write so AI engines cite it", the rules live here.

One framing governs everything below: AI engines do not rank 1000 pages, they sample a short list of sources per subquery and quote passages from them. That changes the job from "rank the page" to "make every passage quotable and make the brand legible everywhere models look". GEO sits on top of SEO, never instead of it: a page that is not indexed cannot be retrieved, and a page that is not retrieved cannot be cited.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed.

## Definitions

- GEO (Generative Engine Optimization): the practice of earning citations and recommendations inside AI-generated answers.
- AEO (Answer Engine Optimization): an earlier name for the same goal; treat the terms as interchangeable.
- Citability: how easily one passage can be lifted out of a page and quoted as a standalone, correct answer.
- Query fan-out: the engine-side decomposition of one prompt into multiple subqueries, each retrieved separately.
- Entity: the machine-readable identity of a brand (name, category, key facts) that models learn from co-occurrence across the web.

## When to use this skill

Use this skill when the user:

- Asks how to appear in ChatGPT answers, AI Overviews, AI Mode, Perplexity, Claude, or Gemini.
- Asks why a competitor is recommended by AI assistants and they are not.
- Mentions GEO, AEO, AIO, LLM SEO, answer engine optimization, or AI citations.
- Wants a page or blog post optimized, scored, or audited for AI citability.
- Asks about llms.txt, blocking AI crawlers, or any rumored GEO tactic (the myths section answers these honestly).
- Wants brand entity work: consistent descriptions, schema, third-party profiles.

Boundaries: build target prompt lists with seo-keyword-research first; measure results with geo-tracking after. This skill is the middle step, improving citation rates.

## How each AI engine selects sources

Treat each engine as a distinct channel with its own retrieval pipeline. Only 11% of cited domains are cited by both ChatGPT and Perplexity in a 2026 per-engine audit (https://authoritytech.io/curated/ai-citation-11-percent-platform-overlap-per-engine-audit-2026): winning one engine does not transfer automatically.

| Engine | Index and retrieval | What decides a citation | Key measured facts |
|---|---|---|---|
| ChatGPT search | Own index crawled by OAI-SearchBot, with Bing as a complementary gateway | Fans the prompt out into subqueries, retrieves a short list, cites roughly half of the URLs it fetches | Title and content similarity to the subquery is the top citation predictor across 1.4M prompts (https://ahrefs.com/blog/why-chatgpt-cites-pages/); OpenAI roughly tripled its crawl volume since August 2025 (https://www.botify.com/blog/openai-tripled-web-crawl) |
| Google AI Overviews and AI Mode | Standard Googlebot index | Official query fan-out, answers assembled passage by passage from multiple sources | Only 32% of AI Mode cited URLs overlap the organic top 10 (51% at domain level; links shown below responses track organic much more closely) (https://www.semrush.com/blog/ai-mode-comparison-study/) |
| Perplexity | Own index (PerplexityBot) plus real-time fetching | Retrieval-heavy, favors fresh sources and user-generated content | Overweights YouTube, Reddit, and review content, and cites Wikipedia far less than ChatGPT does (0.6% vs 7.8% of citations, https://www.tryprofound.com/blog/ai-platform-citation-patterns) |
| Claude | Brave Search as web search backend plus Anthropic's own fetchers | Search-grounded answers from Brave results | Brave powers Claude web search (https://techcrunch.com/2025/03/21/anthropic-appears-to-be-using-brave-to-power-web-searches-for-its-claude-chatbot/) |
| Gemini | Google Search grounding | Same index and fan-out family as AI Overviews | Optimize through the same Googlebot index and passage rules |

Read the table offensively:

- The 32% overlap number is the central GEO opportunity. A page ranking 15th (or a page with no ranking head term at all) gets cited when it answers one fan-out subquery better than anything in the top 10. Passage relevance beats page rank. This is why niche, precisely-titled pages punch above their domain authority in AI answers.
- ChatGPT citing about half of what it fetches means retrieval is necessary but not sufficient: the passage must then be the easiest one to quote. The citability rules below exist for that second step.
- Perplexity's UGC bias means some prompts are won on YouTube, Reddit, or review platforms, not on your domain. Plan surfaces per engine, not one site-only strategy.
- Bing still matters: it feeds ChatGPT as a gateway, so verify indexation in Bing Webmaster Tools, not only Google.

### Per-engine playbook

| Engine | First moves |
|---|---|
| ChatGPT | Verify Bing indexation (Bing Webmaster Tools) and OAI-SearchBot access in robots.txt. Title and slug pages to match fan-out subqueries. A page must be fetchable first, quotable second. |
| Google AI Overviews and AI Mode | Target subqueries, not only head terms. Restructure target pages answer-first. Top 10 ranking is not required (32% URL overlap, 51% domain overlap), indexation and passage relevance are. |
| Perplexity | Publish dated, recently updated content. Build YouTube and review platform presence; monitor the Reddit threads where the category is discussed. |
| Claude | Search the target queries on Brave Search (search.brave.com); Brave has its own index, and a site invisible in Brave is invisible to Claude's web search. |
| Gemini | Inherits the Google work; confirm AI Overviews presence first, then check Gemini separately in geo-tracking. |

## Workflow

### Step 1: Verify the foundation

No indexation, no citation. Before any GEO work, confirm with seo-technical: page indexed (Google and Bing), clean canonical, present in the sitemap, no accidental blocking of AI crawlers in robots.txt, and content present in raw server HTML (no major AI crawler executes JavaScript; Googlebot is the only reliable renderer).

### Step 2: Pick target prompts and pages

Take the buyer prompt panel from seo-keyword-research (50-100 prompts mapped to pages). Prioritize prompts where geo-tracking shows competitors mentioned and the brand absent: those are winnable gaps with proof of demand.

### Step 3: Rewrite pages passage by passage

Apply the citability rules from the Rules and thresholds section to each target page. Work section by section: each H2 block must survive being lifted out of the page and quoted alone.

### Step 4: Score and prioritize

Score each page with the 5-pillar GEO rubric (below), manually or with the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py). Fix the largest point gaps first; citability gaps usually pay back fastest because they change what models can quote.

### Step 5: Check the AI crawler view

Why: no major AI crawler (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot) executes JavaScript; only Googlebot reliably renders. Content that exists only after rendering does not exist for them.

1. Fetch the raw HTML of the page (view-source or curl) and search for the page's key answers verbatim.
2. Compare with the rendered page in a browser.
3. Classify what is missing from the raw HTML: JS-injected sections, tab and accordion content loaded on click, iframes, Shadow DOM components.
4. Apply the nuance: content present in the HTML but collapsed by CSS is still readable by text crawlers; content injected by JavaScript on interaction is not. The first is a UX choice, the second is invisibility.
5. Surface every answer that must be retrievable in server HTML; rendering fixes (SSR, prerendering) live in seo-technical.

### Step 6: Enforce entity consistency

Models learn brands from repeated co-occurrence of the brand name with its category and facts. Make every surface tell the same story (checklist below).

### Step 7: Build third-party presence

For commercial prompts, engines often cite reviews, listicles, and videos instead of vendor sites. Be present where the citations already go (surfaces table below).

### Step 8: Hand off measurement

Send the prompt panel and target pages to geo-tracking. Expect movement over weeks to months, not days, and judge trends, not single answers.

## Rules and thresholds

### Passage-level citability rules (canonical)

Engines quote passages, not pages. Write so any single section can stand alone as a complete answer.

1. Answer-first blocks. Phrase every H2 as a real question a buyer asks, then answer it directly in 2-4 sentences (40-60 words), then develop. Why: the model lifts the first complete answer it finds; burying the answer after 300 words of context hands the citation to someone else.
2. Self-contained chunks. One idea per paragraph. Ban "as mentioned above" and pronoun chains across paragraphs; restate the subject noun. Why: retrieval pulls chunks out of context, and a chunk that only makes sense inside the page is unusable alone.
3. Clean definitional sentences. Give every important concept one quotable "X is Y" sentence near the top of its section. Why: definitional sentences are the easiest passages for a model to reuse verbatim, and they anchor what the model believes the entity is.
4. Evidence density. In the GEO study's controlled benchmark across 10,000 queries (Princeton et al., https://arxiv.org/abs/2311.09735), adding expert quotes lifted generative visibility by about 41%, adding statistics by about 32%, citing sources by about 30%, and improving fluency by about 28%, while keyword stuffing reduced visibility. Honest framing: these lifts were measured in the paper's benchmark of generative answers, not guaranteed on live engines, but the direction is corroborated by live citation pattern studies. Practical rule: every major claim gets a number with a source or a named expert quote.
5. Tables and lists. Comparison tables are the most extractable format for "best X" and "X vs Y" prompts. Measured citation share by format: comparative listicles ("Best X for Y") 32.5% of citations, other listicles 21.9%, articles 16.7%, product pages 13.7% (https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/). If the site has no comparison content, it is absent from the single most cited format.
6. Descriptive natural-language slugs. Pages with descriptive slugs were cited at 89.78% vs 81.11% for non-descriptive ones in Ahrefs' dataset (https://ahrefs.com/blog/why-chatgpt-cites-pages/). Slug the page like the question it answers.
7. Zero em dashes. Never leave an em dash (U+2014) or an en dash (U+2013) in a rewritten passage. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. Why: the em dash is the single most recognizable tell of AI-written text, so it costs the page reader trust and client trust at the same time, and a quoted passage carries the tell straight into the answer. Sweep every rewritten passage for both characters before delivery. Hyphens in compound words and ranges written with "to" are untouched.
8. Freshness without churn. Maintain dateModified in JSON-LD plus a visible date, and make substantive updates every 60-90 days on commercial and comparison pages (prices, versions, screenshots). At the same time, the median cited page is roughly 500 days old in the same Ahrefs dataset: URL authority accumulates. Update in place, never rotate URLs for fake freshness.

### Example: rewriting a passage for citability

Before (typical, not citable):

```
Many construction teams struggle with project visibility. As we discussed
above, the landscape has evolved considerably, and there are many factors
to consider. Our platform takes a different approach to this problem,
building on the insights from the previous section.
```

Why it fails: no question, no answer, references to content outside the chunk ("as we discussed above"), no definition, not one fact a model can quote.

After (citable):

```
## What is construction project management software?

Construction project management software is a tool that centralizes
schedules, budgets, subcontractors, and site documents for building
projects. Mid-size contractors use it to replace spreadsheets and email
threads with one shared system. Typical plans cost 30 to 60 USD per user
per month (pricing survey: [source URL]).
```

Why it works: a question H2 matching a fan-out subquery, a definitional "X is Y" first sentence, fully self-contained, a sourced number, and the whole direct answer inside 40-60 words. (Illustrative figures: replace with real, sourced ones.)

### The GEO scoring rubric (0-100)

Five pillars, raw score out of 80. Adapted from a scoring model used in production audit tooling; apply it as an evaluation grid, manually or via the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py).

| Pillar | Points | What earns points |
|---|---|---|
| Citability | /20 | Numerous H2s phrased as questions, lists, tables, statistics, definitional sentences, paragraphs of 10-80 words |
| E-E-A-T signals | /20 | Visible author with bio, datePublished and dateModified, outbound links to authoritative sources |
| Structured data | /20 | JSON-LD present, key types correct (Article or Product, plus Organization), BreadcrumbList |
| AI accessibility | /10 | Indexable, clean canonical, in the sitemap, content present in server-rendered HTML |
| Multi-format | /10 | Descriptive image alts, at least one table, video where relevant |

Detailed grid (keep pillar totals fixed even when adapting sub-items):

| Pillar | Sub-item | Points |
|---|---|---|
| Citability /20 | H2s phrased as questions, roughly one per 150-300 words | 4 |
| | Direct 2-4 sentence answer immediately under each H2 | 4 |
| | At least one comparison or data table | 3 |
| | Bulleted or numbered lists wherever enumerations exist | 2 |
| | Statistics with sources in the body | 3 |
| | One definitional "X is Y" sentence per key concept | 2 |
| | Paragraphs mostly between 10 and 80 words | 2 |
| E-E-A-T /20 | Visible author with a real bio | 6 |
| | datePublished present (visible and in JSON-LD) | 3 |
| | dateModified present and honest | 4 |
| | Outbound links to authoritative sources | 7 |
| Structured data /20 | Valid JSON-LD present | 8 |
| | Correct primary type (Article or Product) | 6 |
| | Organization with sameAs | 3 |
| | BreadcrumbList | 3 |
| AI accessibility /10 | Indexable (no noindex, no accidental robots block) | 3 |
| | Clean self-referencing canonical | 2 |
| | Present in the XML sitemap | 2 |
| | Full content in raw server HTML | 3 |
| Multi-format /10 | Descriptive image alts | 4 |
| | At least one table | 3 |
| | Video embedded where the topic warrants one | 3 |

Normalization, and why it exists: editorial pages are scored against the full 80; non-editorial pages (product, collection, service) are scored against an attainable maximum of 70, because full editorial E-E-A-T (author bios, citation apparatus) is structurally out of reach for a product page, and a grade that punishes a page for its template teaches nothing. Normalized score = raw score divided by the attainable maximum, times 100.

| Grade | Normalized score |
|---|---|
| A | 90 or above |
| B | 75 to 89 |
| C | 60 to 74 |
| D | 40 to 59 |
| F | below 40 |

Report the pillar breakdown with every grade: the gaps, not the letter, drive the fix list.

### Entity consistency rules

The training and retrieval signal models learn from is co-occurrence: "brand + category + same facts" repeated across independent surfaces. Inconsistency dilutes the entity; a model that has seen three different one-line descriptions trusts none of them.

Template for the canonical one-line description:

```
[Brand] is a [category] for [audience] that [one differentiator].
Example: SitePilot is construction project management software for
mid-size contractors that links daily site reports to budgets.
```

Checklist:

- Write one canonical one-line description (name, category, who it serves, one differentiator). Reuse it verbatim on the site footer or about page, LinkedIn, G2, Crunchbase, directories, and every profile. Verbatim matters: paraphrases weaken the co-occurrence signal the consistency exists to create.
- Same name spelling, same founding facts, same positioning everywhere. Fix old profiles; models read them too.
- Organization JSON-LD on the site with sameAs links to every official profile (implementation in seo-schema-markup).
- Control the brand SERP: own page 1 for the brand query with the site plus profiles you control. Engines resolve "what is [brand]" from those results.
- Wikipedia only if notability criteria are genuinely met; a deleted draft helps nobody.
- Brand web mentions correlate with AI Overview brand visibility at 0.664 versus 0.218 for backlinks (https://ahrefs.com/blog/ai-overview-brand-correlation/). Correlation, not proven causation, but the gap is large enough to justify a mentions-first program: run the brand mentions workflow in seo-backlinks.

### Third-party surfaces

For commercial prompts, the engines often cite about the brand rather than the brand. Be present where citations already go.

| Surface | Why it matters | Action |
|---|---|---|
| Review platforms (G2, Capterra, Trustpilot) | Heavily retrieved for "best X" and "is X good" prompts | Complete profile, steady flow of recent reviews, canonical one-line description |
| YouTube | A significant share of AI answer citations, around 15% (field heuristic from 115+ agency audits); Perplexity overweights it (measured, Profound) | Product walkthroughs and comparison videos, titles phrased as the buyer question |
| Reddit and forums | Retrieved for authenticity-seeking prompts | Genuine participation where the brand is discussed; never astroturf |
| LinkedIn | Entity corroboration, B2B prompts | Complete company page, same one-line description |
| Your own /vs/ and /alternatives/ pages | Capture comparison fan-out subqueries | One page per major competitor pairing (seo-content-blog) |
| Third-party listicles | Comparative listicles take 32.5% of citations (measured, ALM) | Pitch inclusion and updates in existing "best X" articles that engines already cite |

Volatility warning: Reddit's share of ChatGPT citations moved from roughly 60% to roughly 10% within about a month after platform shifts (https://www.semrush.com/blog/most-cited-domains-ai/). Any single-surface strategy can be erased by one partnership or model update. Diversify deliberately across at least three surfaces.

## Dead tactics and myths

Answer these plainly when asked; wrong beliefs here waste entire quarters.

| Claim | Verdict | Reality |
|---|---|---|
| "Add llms.txt to get cited" | No evidence | No AI engine has announced reading it. Google's John Mueller: none of the AI services say they use it, and server logs show they do not even check for it (https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/). Published log analyses measure fetches at roughly 0.1% of AI bot hits. Ship it in ten minutes if a stakeholder insists, expect nothing from it. |
| "Block Google-Extended to exit AI Overviews" | False | Google-Extended controls Gemini model training, not AI Overviews. AI Overviews are built from normal Google Search indexing (https://developers.google.com/search/docs/appearance/ai-features). Leaving search means leaving search. |
| "Keyword stuffing helps LLMs" | False | It reduced visibility in the GEO benchmark (https://arxiv.org/abs/2311.09735). Models reward answers, not token repetition. |
| "GEO replaces SEO" | False | Citation requires retrieval, retrieval requires indexation and crawlable HTML. GEO is a layer on top of working SEO. |
| "Rank #1 in Google and AI visibility follows" | False | 32% URL overlap (51% at domain level) between AI Mode citations and the organic top 10 (Semrush); 11% domain overlap between ChatGPT and Perplexity (AuthorityTech). Plan per engine. |
| "Blocking AI crawlers is free protection" | Trade-off, not free | Blocking OAI-SearchBot removes ChatGPT search visibility; blocking GPTBot affects training only. Decide per business goal, per crawler (crawler table in seo-technical). |

## Output format

Deliver a GEO visibility plan with five blocks:

1. Engine status summary: for each engine, current presence (from geo-tracking if available), the retrieval mechanism that matters, and the single biggest blocker.
2. Page rewrite list: page, target prompt(s), rubric score and grade with pillar breakdown, top 3 fixes in priority order.
3. Entity consistency audit: the canonical one-line description, plus a surface-by-surface pass/fail table (site, LinkedIn, G2, Crunchbase, directories) with exact text mismatches quoted.
4. Third-party surface plan: which surfaces to build or fix, per priority prompt, with the existing third-party listicles to pitch.
5. Measurement handoff: prompt panel reference and the geo-tracking cadence, with expected lag (weeks to months) stated explicitly.

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Optimizing only the brand's own site | Absent from listicle and review citations, the most cited formats | Third-party surfaces plan, pitch existing listicles |
| Treating all engines as one | Wins on one engine, invisible on others | Per-engine plan; 11% overlap is the rule, not the exception |
| Burying answers after long intros | Model quotes a competitor's tighter passage | Answer-first blocks, 2-4 sentences within 40-60 words |
| Pronoun chains and "as seen above" | Chunks unusable out of context | Self-contained sections, restate subjects |
| Hiding content in tabs, accordions, JS | Invisible to the AI crawlers (none of the major ones executes JavaScript) | Server-rendered HTML, check raw source (seo-technical) |
| Churning URLs for freshness | Resets the roughly 500-day authority curve | Update in place, keep the URL |
| Stuffing statistics without sources | No lift, credibility damage | Every number gets a URL or a named source |
| Betting everything on one surface | One platform shift erases visibility (Reddit precedent) | Minimum three surfaces |
| Shipping llms.txt as the GEO strategy | Quarter wasted on a no-evidence tactic | Citability rewrites, entity work, third-party presence |
| Penalizing product pages with editorial criteria | Meaningless grades, wrong priorities | Normalize against 70 for non-editorial pages |

## Cross-references

- seo-keyword-research: builds the prompt panel and maps prompts to pages (do this first).
- geo-tracking: measures mention rate, citation rate, and share of voice (do this after, canonical measurement).
- seo-geo-audit: bundled audit script (scripts/seo_audit.py) implementing the scoring rubric at scale.
- seo-technical: canonical AI crawler table, JS rendering, robots.txt decisions.
- seo-schema-markup: Organization, Article, Product JSON-LD and sameAs implementation.
- seo-backlinks: the brand mentions workflow (mentions over backlinks for AI visibility).
- seo-content-blog: writing comparison listicles and versus pages.
- seo-local: entity consistency for local businesses (profiles, citations).

## Sources

- Ahrefs, 1.4M prompt study on ChatGPT citation predictors (title similarity, slug rates, page age): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Botify, OpenAI tripled web crawl since August 2025: https://www.botify.com/blog/openai-tripled-web-crawl
- Semrush, AI Mode vs organic results comparison study (32% overlap): https://www.semrush.com/blog/ai-mode-comparison-study/
- Semrush, most cited domains in AI answers (Reddit volatility): https://www.semrush.com/blog/most-cited-domains-ai/
- Profound, AI platform citation patterns (Perplexity source bias): https://www.tryprofound.com/blog/ai-platform-citation-patterns
- TechCrunch, Brave powers Claude web search: https://techcrunch.com/2025/03/21/anthropic-appears-to-be-using-brave-to-power-web-searches-for-its-claude-chatbot/
- AuthorityTech, per-engine citation audit, 11% domain overlap: https://authoritytech.io/curated/ai-citation-11-percent-platform-overlap-per-engine-audit-2026
- GEO: Generative Engine Optimization, controlled benchmark on 10,000 queries (Princeton et al.): https://arxiv.org/abs/2311.09735
- ALM, citation share by content format: https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/
- Ahrefs, brand mentions vs backlinks correlation with AI Overview visibility (0.664 vs 0.218): https://ahrefs.com/blog/ai-overview-brand-correlation/
- Search Engine Journal, John Mueller on llms.txt (no engine uses it): https://www.searchenginejournal.com/google-says-llms-txt-comparable-to-keywords-meta-tag/544804/
- Google Search Central, AI features documentation (query fan-out, Google-Extended scope): https://developers.google.com/search/docs/appearance/ai-features
- Items marked "field heuristic from 115+ agency audits" are practitioner observations from agency audit calls (2024-2026), not controlled studies.
