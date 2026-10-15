---
name: keyword-research
description: Run a keyword research workflow on a topic or domain — existing rankings, keyword ideas from a seed, intent classification, filtering by volume, difficulty, CPC and business value, then clustering by topic. Use when the user asks for keyword research, keyword ideas, search volume or keyword difficulty, or which keywords to target.
---

# Keyword research

This skill runs a real keyword research workflow on a topic or domain, in the order a working SEO would tackle it. Each step has a clear input, a clear output, and a Semrush MCP call where one fits.

The workflow is intentionally weighted toward keywords that drive conversions, not keywords that look big in a screenshot. A 50-volume term that closes deals beats a 50,000-volume term nobody buys from.

## Before you start

Ask for these inputs once. Do not skip this step. The research you run for a 10-page SaaS site is not the research you run for a 50,000-product ecommerce store.

- **Topic or seed keywords.** What is the user actually trying to rank for? "SEO tools" is a topic. "Best SEO tools for solopreneurs" is closer to a real query.
- **Domain.** Optional. Use it for existing-ranking research, competitor comparison, and business-context checks when the selected report accepts a domain. The tested public Semrush MCP keyword reports return generic Keyword Difficulty (KD), not personalised keyword difficulty (PKD).
- **Whether the Semrush MCP is connected.** This unlocks Semrush keyword reports for live volume, difficulty, intent, CPC, and SERP feature data. If it is not connected, you can still classify intent, but the metrics should be marked unknown rather than guessed. The Semrush MCP connects through Semrush's own auth flow, so there is no API key to paste.
- **Whether the user has Google Search Console data available.** GSC reveals queries and pages already receiving impressions and clicks. Use it to identify opportunities relative to the site's own performance rather than imposing one universal position, impression, or click threshold. If GSC is unavailable, ask for an export or continue with Semrush index data and disclose the limitation.
- **Goal.** Brand awareness, lead generation, direct sales, or AI search visibility. The goal determines which keywords matter and how to prioritise.

## How to use the Semrush MCP

Prefer the MCP over manual brainstorming when it is connected. Use Semrush MCP only. The canonical workflow:

1. Call the relevant discovery tool to list the reports currently exposed by the MCP.
2. Call `get_report_schema` for the exact report identifier returned by discovery.
3. Call `execute_report` with the parameters from the schema.

The MCP discovery tools relevant to this workflow are `keyword_research`, `organic_research`, and `competitors_research`. Use `get_report_schema` and `execute_report` after discovery. Do not substitute Semrush product-UI names for public MCP report identifiers.

- Use `keyword_research` → `phrase_this` for one keyword's volume, CPC, competition, intent, trend, and generic KD. Its tested schema has no domain input and no PKD field.
- Use `keyword_research` → `phrase_related` and `phrase_questions` for expansion. These reports return keyword rows and metrics, not Keyword Magic Tool groups, subgroups, or automatic clusters.
- Use `keyword_research` → `phrase_organic` with `positions_type: organic` for the ranked organic URLs. Use `positions_type: all` only when feature-position rows are intentionally required; keep those rows separate from organic rankings and do not count repeated feature/organic URLs as separate competitors. Do not assign human-readable feature names unless the current discovered schema or official documentation supplies the mapping.
- Use `competitors_research` → `domain_domains` for Keyword Gap comparisons. The tested report accepts domains directly and does not require a Semrush project.
- Use `organic_research` → `resource_organic` for the keywords and pages an existing domain or URL ranks for. Verify its schema before execution.

Legacy SEO API-style keyword reports may return intent as numeric codes rather than labels. Decode only the documented values: `0` = Commercial, `1` = Informational, `2` = Navigational, and `3` = Transactional. Treat comma-separated values such as `1,0` as mixed intent, preserve the raw value in the evidence layer, and never guess an unfamiliar or missing code.

## Report interpretation and data quality

Apply these rules to every candidate source, including seed metrics, related terms, questions, existing rankings, Keyword Gap rows, supplied exports, and GSC data:

- Preserve raw report rows separately from the analyzed shortlist. Normalize capitalization and whitespace and remove exact duplicates, but never rewrite a query, URL, code, or metric in the evidence layer.
- Screen for explicit search operators, broken encoding, malformed tokens, obvious misspellings, and terms unrelated to the user's topic, audience, market, or goal. Record the screening rule and excluded count when cleanup materially changes the set. Do not transfer a removed row's metrics to a corrected spelling.
- Preserve numeric SERP-feature codes exactly as returned. Translate a code only when the current discovered schema or official documentation provides its meaning; otherwise label it unresolved. Keep any manual feature classification separate as a manual observation or model judgment.
- Treat `phrase_organic` rows with `position_type: -1` as traditional organic positions in the tested contract. Preserve every raw row, but deduplicate identical URLs for page-review and competitor-count purposes while recording every returned position. When `positions_type: all` returns additional feature-position rows, do not mix those rows into the organic top 10 or count duplicate URLs more than once.
- When two reports disagree, retain both values with the report name, database, target, and available date or snapshot context. Do not silently merge them or choose the more favorable value. Explain which value, if any, supports the decision and why; otherwise mark the metric inconsistent.
- If execution rejects a field or operation that appeared valid in the discovered schema, do not keep retrying or claim that the server-side filter ran. Request the smallest useful unfiltered result set and apply the equivalent transparent client-side filter when possible; otherwise mark that branch incomplete.

## MCP access and cost guardrails

- Before the first `execute_report` call, tell the user that Semrush MCP queries consume API units. Request only the fields needed, use the smallest result limit that answers the question, and expand only after reviewing the first batch. Never request all rows by default.
- If authentication is incomplete, a required tool, report, schema, or field is unavailable, or execution fails because of access or units, stop that MCP branch. State what is unavailable and which findings are affected, then use the strongest fallback below. Never guess missing keyword metrics.

## Fallback ladder

Use the strongest available data source and state which one you used.

1. Semrush MCP keyword and organic reports.
2. Semrush UI exports supplied by the user.
3. Google Search Console queries and pages.
4. Manual SERP inspection and first-party customer language. Label metrics as unknown rather than guessing.

## Research framework

Run these six steps in order. The list is priority-sorted so a finding in step 1 matters more than a finding in step 5.

1. Audit existing rankings
2. Pull keyword ideas from a seed
3. Classify search intent
4. Filter by the metrics that matter
5. Cluster by topic and intent
6. Prioritise by business value

End with a prioritised keyword plan. Each cluster should have one primary keyword and only the supporting variants justified by shared intent and SERP overlap; there is no universal cluster size.

---

## 1. Audit existing rankings

The strongest signal here is what the site is already showing up for. Pages on page 2 of Google can often reach page 1 with light work, which is the cheapest traffic available.

If GSC is available, pull the Performance report and agree on a recent date range that matches the site's traffic level and decision cycle. Find queries or pages with meaningful impressions but relatively weak clicks or CTR, plus rankings near a result range the site can realistically improve. Make the filters configurable and state them in the output.

Semrush uses positions 11+, volume of at least 100, and KD 0–49 as one adjustable existing-ranking example. Offer that only as a named starting preset for a less-established site, never as the definition of a GSC opportunity.

For each candidate keyword, note the current position, the impressions, and the page that currently ranks. These are warm leads.

If Semrush MCP is available, use `phrase_this` or the current batch-keyword report discovered through `keyword_research` to retrieve generic KD and the other requested metrics. Do not claim that the public MCP has personalised difficulty or accepts a supplied domain for keyword-level personalisation.

Without GSC, use Semrush Organic Research on the user's domain to see similar ranking data from Semrush's index. Note this is index data, not direct Google data, and may lag GSC.

---

## 2. Pull keyword ideas from a seed

Start from a real seed term. A bad seed produces bad ideas. Pick the term a customer would actually type, not the marketing-friendly version. "Email validation" is a real seed. "Email deliverability optimisation platform" is not.

Use `keyword_research` to discover `phrase_related` and `phrase_questions`, then run each required report through `get_report_schema` and `execute_report`. They can return:

- Related terms
- Questions (who, what, where, when, why, how variants). These are the long-tail goldmine.
- Available metrics such as volume, generic KD, intent, CPC, trend, and relevance, depending on the live schema.

Start with the MCP's recommended exploratory limit of 30–50 rows per report. Expand only when the first batch does not cover the relevant intents, modifiers, questions, or competitor gaps. The appropriate collection size depends on the site's scope, goals, and available API units.

Apply the shared quality-control rules above before clustering. Do not discard a keyword merely because its volume is low or zero. Treat every exclusion as a model-assisted judgment rather than Semrush data.

A few filters cut the noise.

- **Questions only.** Question-format keywords drive AI Overview citations and PAA appearances. They tend to have lower volume but higher click value.
- **User-controlled difficulty.** For a newer or less-authoritative site, KD 0–49 can be offered as a Semrush-supported starting preset. Adjust it to the site's authority, topical relevance, and goals.
- **User-controlled volume.** Volume of at least 100 can be included in the same optional preset, but low-volume or zero-volume terms may still matter when first-party evidence shows demand. Do not impose a universal upper limit.

---

## 3. Classify search intent

Search intent is the most important keyword metric you can read. It determines what content to write, what format to use, and whether the keyword can ever convert.

Four categories. Tag every candidate with one (or two, when overlap is real).

- **Informational.** User wants to learn. Phrases like "how to", "what is", "why does", "guide to". Content type is article, guide, or video. Conversion is indirect (awareness or top of funnel).
- **Navigational.** User wants a specific brand or product. Phrases like brand names, "login", "pricing page". Content type is the actual product page. Conversion is direct if the user is already a customer.
- **Commercial.** User is comparing options. Phrases like "best", "vs", "review", "alternatives to". Content type is comparison, listicle, or roundup. Conversion is high if the content positions the user's product well.
- **Transactional.** User is ready to buy or sign up. Phrases like "buy", "download", "discount code", "free trial". Content type is product or pricing page. Conversion is direct and immediate.

Three ways to read intent.

- **From the query language.** "How to fix indexation errors" is informational. "Best indexation tools" is commercial. "Buy SEO software" is transactional.
- **From the SERP features.** A featured snippet at the top usually means informational. A shopping carousel means transactional. Product comparison sites in the top 5 means commercial.
- **From word order.** "Ingredients for dog food" (someone making it at home) is different from "dog food ingredients" (someone reading labels in a store).

If the Semrush MCP returned an intent label, trust it as a starting point but verify by looking at the actual top 3 SERP results. Tools mis-classify intent on ambiguous queries.

Watch for these common misreads.

- Treating a keyword as single-intent when the SERP shows mixed intent (some informational results, some commercial). When this happens, both intents are valid. The page that wins is usually the one that addresses both.
- Writing a "how to" guide for a commercial keyword. The user wants a comparison, not a tutorial.
- Ignoring intent layers. "How to start a vegetable garden" needs soil prep, seasonality, and pest control to fully serve the searcher.

---

## 4. Filter by the metrics that matter

Six metrics. Read them together, not one at a time.

### Search volume

The number of times a keyword is searched per month, on average. Reported by Semrush for the database you query.

Interpret volume relative to the market, conversion value, site size, and first-party demand. Do not treat a low-volume term as skippable or a high-volume term as unattainable based on volume alone.

One trap to watch. Global vs country-specific volume. The Semrush MCP defaults to the database you specified. A US site looking at "tax filing software" returns very different numbers than a UK site.

### Keyword Difficulty (KD)

Semrush's generic estimate of how hard a keyword is to rank for, scored from 0 to 100 in the tested public MCP.

Treat KD as comparative evidence, not a promise of whether a specific site will rank. Consider it alongside topical relevance, current rankings, SERP competitors, content quality, links, and business value. Do not relabel generic KD as PKD or create universal attainability bands.

### Cost per click (CPC)

Average paid bid for the keyword. A commercial-value signal, not a ranking signal.

CPC can indicate paid-search competition and commercial interest, but a high or low value is industry-dependent. Do not use fixed dollar cutoffs as proof of business value. Validate value with the user's products, margins, conversions, and customer language.

### Search trend

12-month volume trajectory. Rising trends suggest emerging opportunities. Declining trends suggest a topic past its peak.

Use direction, stability, and seasonality as context. A rising trend may indicate an emerging opportunity, while a decline may change the priority, but no fixed percentage determines the decision.

Watch for seasonality. "Black Friday deals" looks like it is declining if you check in February.

### Search intent

Already classified in step 3. Carry the classification through to filtering.

### SERP features

What appears on the SERP for the keyword: featured snippet, PAA boxes, shopping carousel, AI Overview, local pack.

SERP features matter for two reasons.

- Some features absorb the click. If the AI Overview answers the query in full, organic CTR is low even at position 1. Deprioritise unless the keyword is bottom-of-funnel.
- Some features create opportunities. Featured snippets and PAA results can reward clear headings, concise direct answers, and formatting suited to the question. Do not impose a fixed answer length.

---

## 5. Cluster by topic and intent

A keyword in isolation is rarely a target. Group only the related keywords that one page can satisfy without mixing incompatible intents. Cluster size should follow the evidence rather than a fixed count.

Cluster by following two rules.

- Group keywords that share both topic and intent. "What is a backlink" and "how do backlinks work" are the same cluster. "What is a backlink" and "best backlink tools" are not. Different intent.
- Pick a primary keyword per cluster based on intent fit, business value, demand, and attainability—not volume alone. The remaining keywords are supporting variants the page should naturally cover.

The tested public MCP does not return automatic clusters from `phrase_related` or `phrase_questions`. Cluster transparently as a model-assisted or manual step using shared intent and, when warranted, overlap among the ranking URLs returned by `phrase_organic`. Label the cluster assignment as inference rather than Semrush-returned data.

Two common mistakes.

- Mixing intents within one cluster. The page cannot serve "how to write meta descriptions" (informational) and "meta description generator" (transactional) well.
- Cannibalisation. Two pages on the same site targeting the same cluster compete with each other. Pick one page and consolidate.

---

## 6. Prioritise by business value

Order clusters by where they sit in the funnel and how much revenue they move.

When the user's immediate goal is revenue, use this Semrush-supported revenue-first preset:

1. **Bottom of funnel (transactional, commercial-comparison).** "Best [your category] tools", "[your product] alternatives", "[your product] vs [competitor]". Lowest volume but closest to revenue.
2. **Middle of funnel (commercial-investigation).** "How to choose [your category]", "[problem your product solves]". Educates and qualifies.
3. **Top of funnel (informational).** "What is [your category]", "guide to [your topic]". Builds authority over time but converts slowly.

Do not impose this order when the user's primary goal is brand awareness, category education, retention, or another outcome. Adapt the ordering to the stated goal while covering the funnel stages relevant to the strategy.

Within each tier, the secondary sort is by:

- Conversion potential (does this user have intent to buy from us?)
- Click potential (is the SERP dominated by features that absorb clicks?)
- Real-world demand (does this term show up in sales calls, support tickets, or Reddit threads?)
- Attainability (generic KD interpreted alongside the site's authority, relevance, and SERP competition)
- Trend (rising > stable > declining)

---

## How to report findings

Output a single table of clusters sorted by the user's stated goal. Keep Semrush metrics, first-party evidence, and model or manual judgments visibly distinguishable.

| Priority | Goal/funnel     | Cluster        | Primary keyword   | Volume          | KD              | Intent                       | Supporting keywords   | Evidence and rationale                                    | Next action                                |
| -------- | --------------- | -------------- | ----------------- | --------------- | --------------- | ---------------------------- | --------------------- | --------------------------------------------------------- | ------------------------------------------ |
| 1        | [goal or stage] | [cluster name] | [primary keyword] | [Semrush value] | [Semrush value] | [Semrush or verified intent] | [supporting variants] | [GSC/first-party signal + clearly labeled model judgment] | [create, refresh, consolidate, or monitor] |

Three rules for the report itself.

- State actual values and their source. "Semrush volume [value], generic KD [value]" is useful. "Decent volume, doable difficulty" is not.
- When an intent code is returned, show the decoded label while retaining the raw Semrush code in the evidence. Label mixed codes as mixed intent and leave unknown values undecoded.
- Suggest a concrete next step for each cluster (write the page, refresh an existing one, build links). The user should know what to do, not just what to know.
- Mark assumptions and inferences. If intent, clustering, business value, or attainability is a model or manual judgment, say so.

## Sources

This skill is grounded in the following Semrush editorial sources:

- [Keyword research for SEO](https://www.semrush.com/blog/keyword-research/)
- [The ultimate keyword research checklist](https://www.semrush.com/blog/keyword-research-checklist/)
- [6 important keyword metrics](https://www.semrush.com/blog/keyword-metrics/)
- [What is search intent](https://www.semrush.com/blog/search-intent/)
- [Keyword clustering](https://www.semrush.com/blog/keyword-clustering/)
- [Long-tail keywords guide](https://www.semrush.com/blog/how-to-choose-long-tail-keywords/)

When citing a specific check or threshold inline, link to the relevant article so the user can verify.
