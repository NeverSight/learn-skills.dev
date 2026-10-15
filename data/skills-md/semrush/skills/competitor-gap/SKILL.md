---
name: competitor-gap
description: Identify a domain's real search competitors from shared rankings, then map keyword, content, backlink, and traffic-channel gaps with a prioritised closing plan. Use when the user asks who competes with them in search, which keywords or content they are missing, or how they compare against a named competitor.
---

# Competitor gap analysis

Compare a domain with relevant search competitors and turn the evidence into actions the user can take. Keep these competitor types distinct:

- **Search competitors:** domains competing for the same organic queries.
- **Direct business competitors:** companies offering similar products or services to the same customer segment.
- **Indirect business competitors:** companies serving a similar audience or need with a different or substitute offer.
- **Brand competitors:** established brands the user may want to benchmark against.

Do not assume the four groups are identical. Publishers, marketplaces, social networks, and user-generated-content sites can be legitimate search competitors when they repeatedly satisfy the same queries. Label their type and relevance instead of excluding them automatically.

## Rule provenance

Interpret material rules using these labels:

- **Semrush-supported guidance:** Methodology stated in a cited Semrush article. Preserve its scenario and caveats.
- **MCP contract requirement:** A limit, field, operation, or access condition confirmed through official documentation or live schema discovery.
- **Industry heuristic:** Analyst judgment that can help prioritize evidence but is not an official Semrush rule.
- **Configurable default:** A workflow or output choice that the user can change.

Keep rule provenance separate from evidence provenance. Label Semrush estimates, first-party data, supplied exports, manual observations, and model judgments distinctly in every output.

## Inputs

Collect only what the user has not already supplied:

- The user's domain.
- Any known business competitors.
- The market and regional database. **Configurable default:** Use the US only when the user gives no geographic context.
- The goal: keyword discovery, content planning, backlink opportunities, channel benchmarking, or a complete comparison.

Use the user's goal to run only the necessary modules. **Configurable default:** A complete comparison uses all five.

## Official Semrush MCP workflow

For every MCP branch, follow discovery tool → `get_report_schema` → `execute_report`. Copy current report names and parameters from discovery and schema results rather than relying on memory.

Use these verified routes:

| Module             | Discovery tool         | Report                                | Purpose                                                                                                 |
| ------------------ | ---------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Search competitors | `competitors_research` | `domain_organic_organic`              | Organic competitors, relevance, shared keywords, and traffic estimates                                  |
| Keyword gap        | `competitors_research` | `domain_domains`                      | Shared, missing, untapped, and weak keyword evidence across up to five domains total                    |
| Content gap        | `organic_research`     | `resource_organic_unique`             | Top organic pages, keyword counts, traffic, and traffic share                                           |
| Page enrichment    | `organic_research`     | `resource_organic`                    | Keywords and rankings for a shortlisted domain, subfolder, or URL                                       |
| Backlink gap       | `competitors_research` | `backlinks_matrix`                    | Referring domains shared across multiple targets                                                        |
| Backlink detail    | `backlinks_research`   | `backlinks_refdomains`                | Authority Score, backlink counts, and first/last-seen evidence for one target                           |
| Backlink context   | `backlinks_research`   | `backlinks`                           | Source page, target page, anchor, response code, and link attributes for a shortlisted referring domain |
| Traffic comparison | `traffic_overview`     | `summary` and, when needed, `sources` | Cross-domain traffic and channel estimates                                                              |
| Paid search        | `paid_search_research` | `resource_adwords`                    | Paid keywords, positions, CPC, and traffic estimates                                                    |

Before the first `execute_report` call, tell the user that Semrush MCP queries consume API units. **Configurable default:** Start with the fields required for the decision and a limit of 30–50 rows. Expand or paginate only when the first result set is insufficient.

`traffic_overview` requires the corresponding Trends subscription. If access is unavailable, use a supplied Semrush Trends export or mark the traffic comparison unavailable. Do not substitute organic-search estimates for total traffic or channel data.

If authentication, access, units, a report, or a required field is unavailable, stop that branch and state what is missing. Never invent a replacement metric.

## Fallbacks

**Configurable default:** Use the strongest available source in this order and label it. Prefer more authoritative user-supplied first-party evidence when available.

1. Official Semrush MCP reports.
2. User-supplied Semrush exports.
3. The user's connected Google Search Console data or export for their own site, plus manual SERP inspection for competitors.
4. User-supplied competitor URLs or backlink exports.

Keep Semrush estimates, first-party data, manually observed facts, and model judgments distinguishable in the final output.

## Data-quality safeguards

Keep the returned rows as source evidence and build a separate analyzed shortlist. Never silently rewrite a query, URL, domain, metric, or report value.

- Screen keyword rows for explicit search operators such as `inurl:`, broken encoding, duplicates, obvious misspellings, and off-topic queries before recommending them. Exclude a row only when it is irrelevant to the user's goal; record the screening rule and excluded count. Do not transfer a removed row's metrics to a corrected spelling.
- Inspect a competitor page's URL, topic, page type, and relationship to the user's audience before treating it as a content opportunity. Keep autogenerated, off-topic, unsafe, or brand-inappropriate pages out of the action list while recording that they were excluded from analysis.
- If a valid field or operation discovered in the report schema is rejected during execution, do not keep retrying or claim that the server-side filter was applied. Request the smallest useful result set and perform the equivalent transparent client-side filtering when possible; otherwise mark that branch incomplete.
- Preserve raw report rows separately from model-assisted relevance, clustering, safety, and prioritization judgments.

## Module 1: Discover and select search competitors

**Semrush-supported guidance:** Identify organic competitors from shared rankings, then compare them with the user's direct, indirect, and brand competitors rather than relying on intuition alone.

Run `competitors_research` → `domain_organic_organic` for the user's domain. Review competitor relevance, shared keyword count, and organic traffic estimates.

Compare the results with the user's known competitors and flag:

- Business competitors with little organic overlap.
- Search competitors the user did not name.
- Domains with unusually strong overlap in the target market.

Let the user select competitors when they have a preference. Otherwise, choose the smallest relevant comparison set that answers the question. **Configurable default:** Start with three for a manageable analysis and expand to four when the additional domain represents a meaningfully different competitor or changes the conclusion.

Evaluate candidate relevance using shared queries, target audience, market, search intent, and page types. Do not require a self-reported competitor to appear in an arbitrary top-10 list. If a business competitor has limited search overlap, explain the distinction instead of removing it silently.

## Module 2: Find keyword gaps

Run `competitors_research` → `domain_domains`. **MCP contract requirement:** The report supports up to five domains total, so compare the user's domain with no more than four competitors in one request.

Construct the requested set using the current schema operations:

- **Missing across every selected competitor:** list the competitor domains first with intersection (`*`) signs and the user's domain last with a difference (`-`) sign.
- **Untapped across any selected competitor:** begin with one competitor using intersection (`*`), add other competitors with union (`+`), and subtract the user's domain with difference (`-`).
- **Shared:** use intersection (`*`) for every compared domain.
- **Weak:** retrieve shared keywords and compare the returned position columns; label a keyword weak only when the user ranks and selected competitors rank higher.

“Missing” always refers to all competitors included in that request. Do not hardcode “all three.” Preserve the domain order so each position column remains attributable.

Use only filters that serve the user's goal. Available report evidence includes position, volume, CPC, competitive density, trend, and generic Keyword Difficulty. The tested public MCP does not return Personal Keyword Difficulty for this report.

When server-side display filters fail despite appearing in the discovered `domain_domains` schema, retrieve only the smallest useful row set and screen it client-side under the data-quality safeguards above. State that the cleanup was applied after retrieval and preserve the original values.

**Semrush-supported guidance:** For a site that is not well known or has not built much authority, KD 0–49 may be offered as a starting preset. Preserve that scenario and state that the range is adjustable. Do not infer a different cutoff from Authority Score. Treat volume ranges as optional user filters, not definitions of value. Prioritize relevance, intent, business value, attainability, and first-party demand together.

Return as many relevant rows as the decision requires. Do not promise a predetermined number of opportunities. Cluster shortlisted keywords by shared intent and SERP overlap, and label clustering as model-assisted analysis rather than a field returned by this report.

## Module 3: Find content gaps

Run `organic_research` → `resource_organic_unique` for each selected competitor and the user's domain. **Configurable default:** Start with a small set sorted by traffic and compare:

- Topics where a competitor has a strong page and the user has no relevant page.
- Topics where both have a page but the user's page underperforms.
- Areas where a competitor demonstrates broader topical coverage.

Do not assume the top 20 pages or a fixed number of recommendations is always appropriate. Expand only when the initial pages do not represent the competitor's relevant content.

For shortlisted pages, use `resource_organic` with the exact URL when keyword-level enrichment is needed. Keep page format and topical-depth classifications as manual or model judgments.

Apply the data-quality safeguards before recommending a competitor page. A high-traffic or high-ranking autogenerated, off-topic, or brand-inappropriate URL is evidence about the raw report, not automatically a useful content gap.

Describe coverage depth with the observed page and topic evidence. Do not use a fixed “five competitor pages versus one user page” rule to declare a cluster gap.

## Module 4: Find backlink gaps

Run `competitors_research` → `backlinks_matrix` with the user and selected competitors as targets. Preserve the target order and map every returned backlink bucket to its domain before filtering.

For a true gap, require the user's backlink bucket to equal zero and at least one selected competitor bucket to be greater than zero. If the current execution contract supports only equality filters reliably, filter the user's bucket with `equals 0`, then either exclude `equals 0` from every competitor bucket for an all-competitor intersection or select rows with any competitor bucket above zero client-side. Do not infer a gap from match count alone, and do not depend on a `greater_than` operation unless both the current schema and a small execution test accept it.

Use `backlinks_research` → `backlinks_refdomains` when a shortlisted domain needs single-target aggregate detail such as Authority Score, backlink count, or first/last-seen dates. Before calling a row a direct prospect, use `backlinks_research` → `backlinks` for at least one linked competitor with the referring domain filter when the current schema supports it. Inspect the returned source URL, source title, target URL, anchor, response code, and link attributes. A matrix row without relevant editorial context is only a candidate, not an outreach recommendation.

**Industry heuristic informed by Semrush methodology:** Evaluate prospects using:

- Topical and audience relevance.
- The page and editorial context in which competitors were linked.
- Evidence that the source is legitimate and active.
- Whether the user has an asset that deserves the same link.
- Authority Score as one quality signal, not an automatic pass/fail threshold.

Do not require Authority Score 30+, a 12-month recency window, or links to a fixed number of competitors. Let the evidence and niche determine whether a prospect is worthwhile.

Separate the output into:

- **Direct prospects:** relevant pages or domains where the user's asset could credibly be added.
- **Relationship patterns:** recurring authors, publishers, journalists, or communities worth understanding.

## Module 5: Compare traffic and channel strategy

**Semrush-supported guidance:** Compare the channels competitors use to reach the same audience, but measure only channels relevant to the user's decision.

Run `traffic_overview` → `summary` for side-by-side traffic and channel estimates across up to five domains. Use `sources` only when a channel requires detailed source analysis.

Use `paid_search_research` → `resource_adwords` for Semrush paid-search estimates. Manual search observations may supplement the report but must be labeled anecdotal and location/time dependent.

For newsletters, social accounts, communities, podcasts, or video channels, inspect first-party pages where possible. Do not present search snippets, follower counts, or subscriber claims as Semrush MCP data.

Name material channel differences without assuming the user should copy every competitor channel.

## Shared prioritization layer

**Configurable prioritization framework:** Combine findings from the selected modules and rank them using:

- **Relevance:** fit with the user's audience, market, goal, and search intent.
- **Evidence strength:** direct first-party evidence, Semrush data, manual observation, or model inference.
- **Feasibility:** content, technical, relationship, and operational requirements.
- **Expected value:** Semrush traffic or traffic-value estimates, first-party conversion evidence, and strategic value.

Do not promise fixed time-to-impact ranges. Do not describe Semrush estimated traffic or traffic value as revenue. Estimate revenue only when the user supplies conversion rates and customer or transaction value, and show the calculation and assumptions.

## Output

**Configurable output default:** Return one prioritized action list followed by concise evidence tables for the modules used.

| Priority | Gap type        | Evidence                                                                                         | Competitor reference | Recommended action                                                            | Feasibility | Expected value                         | Confidence |
| -------- | --------------- | ------------------------------------------------------------------------------------------------ | -------------------- | ----------------------------------------------------------------------------- | ----------- | -------------------------------------- | ---------- |
| 1        | Content refresh | Competitor page ranks for the shared cluster while the user's existing page has weaker positions | Exact competitor URL | Refresh the existing page around the demonstrated intent and missing evidence | Medium      | Semrush-estimated opportunity, labeled | High       |

For every recommendation:

- Name the competitor domain, URL, referring domain, or channel asset that supports it.
- Report actual returned values with their source and date or database when available.
- Separate an underperforming existing asset from a genuinely missing asset.
- Mark unavailable fields rather than estimating them silently.
- Explain model-inferred clusters, page types, relevance, and priorities as judgments.
- Summarize material noise, safety, and relevance filters, including how many rows were excluded and why.

## Sources

Methodology:

- [How to do digital marketing competitor analysis](https://www.semrush.com/blog/how-to-do-competitor-analysis-in-digital-marketing/)
- [Keyword gap analysis](https://www.semrush.com/blog/keyword-gap-analysis/)
- [How to find competitor backlinks](https://www.semrush.com/blog/competitor-backlinks/)
- [Keyword research for SEO](https://www.semrush.com/blog/keyword-research/)

Technical contract:

- [Semrush MCP documentation](https://developer.semrush.com/api/introduction/semrush-mcp/)
- [Semrush Domain vs. Domain report](https://developer.semrush.com/api/seo/domain-reports/)

When presenting a specific threshold or recommendation as Semrush-supported, cite the article that states it and preserve the scenario or qualification attached to it.
