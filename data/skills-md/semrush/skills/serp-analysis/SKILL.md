---
name: serp-analysis
description: Analyse the current Google top 10 for one keyword — keyword metrics, search intent, SERP features, the winning content format, and the gap the user can realistically win. Use when the user asks what ranks for a keyword, what the SERP looks like, which format to write, or why competitors outrank them.
---

# SERP analysis

Analyse the current Google results for one keyword and produce an evidence-labeled content decision. Answer three questions:

1. What content format wins for this keyword (guide, listicle, tool, product page)?
2. What SERP features will absorb clicks no matter where you rank?
3. What can you do that the top 10 do not?

Treat format concentration as evidence about search intent, not a guarantee that one format will rank.

## Rule provenance

Interpret material rules using these labels:

- **Semrush-supported guidance:** Methodology stated in a cited Semrush article. Preserve its scenario and caveats.
- **MCP contract requirement:** A behavior or limitation verified in the current official Semrush MCP discovery and report schemas.
- **Industry heuristic:** A defensible analyst practice, not a Semrush metric or search-engine requirement.
- **Configurable default:** A workflow or output choice the user can change.

Keep Semrush data, manual page observations, user-provided evidence, and model judgment visibly separate. Never turn a Semrush product-interface example into a public MCP capability.

## Before you start

Ask for these inputs once.

- **Target keyword.** One per analysis. Multi-keyword analysis is a different skill (see `keyword-research`).
- **Country / database.** Default to US if the user does not specify. SERPs are wildly different in different geos.
- **The user's domain.** Optional. Use it only for current-ranking or domain-context research through a report whose schema accepts a target. The tested keyword reports do not accept a domain and do not return Personal Keyword Difficulty (PKD).
- **Whether the Semrush MCP is connected.** This unlocks Semrush keyword, organic, SERP, and URL/domain reports for live SERP data. If it is not connected, the analysis falls back to manual SERP inspection. The Semrush MCP connects through Semrush's own auth flow, so there is no API key to paste.

## How to use the Semrush MCP

Use Semrush MCP only.

The MCP uses a three-step pattern for every report:

1. Call the discovery tool (`keyword_research`, `organic_research`, or `domain_overview`) to see available reports.
2. Call `get_report_schema` on the specific report you need to get its required parameters.
3. Call `execute_report` with those parameters to fetch the data.

The reports that do most of the work for this skill:

- `phrase_this` (via `keyword_research`) — request only the needed fields from volume, CPC, competitive density, results, trend, raw intent, and generic Keyword Difficulty.
- `phrase_organic` (via `keyword_research`) — position, position type, domain, URL, and returned SERP-feature codes. It does not return title tags, word count, Authority Score, page traffic, or referring domains.
- `domain_rank` (via `domain_overview`) — optional aggregate domain or URL rank, keyword, traffic, cost, and SERP-feature totals. It does not return Authority Score.

Call `get_report_schema` every time the contract may have changed. Use only fields present in that schema and returned by execution.

If no Semrush MCP is available, run manual SERP inspection in the target country. Do not present manually gathered SERP data as exhaustive.

## MCP access and cost guardrails

- Before the first `execute_report` call, tell the user that Semrush MCP queries consume API units. Limit `phrase_organic` to the results required for the analysis, request only the fields needed, and expand only after reviewing the first batch. Never request all rows by default.
- If authentication is incomplete, a required tool, report, schema, or field is unavailable, or execution fails because of access or units, stop that MCP branch. State what is unavailable and which findings are affected, then use the strongest fallback below. Never guess missing SERP or competitor metrics.

## Fallback ladder

Use the strongest available data source and state which one you used.

1. Semrush MCP keyword, SERP, organic, and URL/domain reports.
2. Semrush UI exports supplied by the user.
3. Manual browser inspection in the target country and language.
4. User-provided top-10 URLs. Label missing metrics as unknown rather than guessing.

## Analysis framework

Run these six steps in order.

1. Pull keyword metrics
2. Identify search intent
3. Catalog SERP features
4. Analyse the top 10 results
5. Determine the winning format
6. Find the gap

End with a reusable SERP evidence object and a short content recommendation. The `content-brief` skill should consume this evidence instead of rerunning the same reports.

---

## 1. Pull keyword metrics

Use `keyword_research` to discover `phrase_this`, then call `get_report_schema` and `execute_report`. Request the fields needed for the decision:

- **Search volume** for the database that matches the user's geo.
- **Generic Keyword Difficulty** as a comparative Semrush estimate, not a prediction for the user's domain.
- **CPC and competitive density** as paid-search market signals, not proof of business value.
- **Trend and raw intent** when returned.

Preserve actual values and the report name. If an intent code or trend value cannot be decoded from verified documentation, keep the raw value and label the interpretation unresolved. Do not manufacture PKD or personalized ranking potential.

---

## 2. Identify search intent

Use the heuristic chain from the `keyword-research` skill if not already classified.

- **From the query language.** "How to" and "what is" point to informational. "Best" and "vs" point to commercial. "Buy" and "free trial" point to transactional.
- **From the SERP itself.** Review the returned result set and current rendered SERP before relying on a single intent label.
- **From SERP features.** Treat features as supporting evidence. Shopping results can support transactional intent; featured snippets and PAA can support informational intent; mixed features can indicate fractured intent.

Watch for **fractured intent**. Some SERPs mix formats. "Best laptops for video editing" might show a product carousel (transactional), three comparison articles (commercial), and a YouTube buying guide (commercial-informational). When intent is fractured, name it in the analysis. You will need to address more than one format on the page that wins.

---

## 3. Catalog SERP features

List every feature returned by `phrase_organic` or confirmed through a current manual SERP. Preserve raw feature codes when their mapping is not verified.

- **Featured snippet.** Record its format and current source when observable. Treat click impact as query-dependent.
- **AI Overview.** AI-generated summary above the organic results. It can change click behavior, so note whether it appears and whether it cites the user or competitors.
- **People Also Ask (PAA).** Use relevant questions as topic evidence, not an automatic outline or H2 list.
- **Knowledge panel.** Right-side entity box. Mostly relevant for brand keywords.
- **Image pack.** Image carousel. Indicates visual intent (recipes, diagrams, products).
- **Video carousel.** Treat it as evidence of video or mixed-format demand.
- **Popular products carousel.** Treat it as evidence of shopping or transactional demand.
- **Local pack.** Treat it as evidence of local intent.
- **Discussions and forums.** Treat it as evidence that community or first-person perspectives are present; do not infer why Google selected them.
- **Rich results.** Record visible enhancements and the eligible result type. Do not promise a CTR improvement.

For each feature present, capture two things:

- Which of the user's competitors hold the feature today (if any).
- What evidence supports targeting it and what platform requirements apply.

Recommend a feature only when the page type and visible content can satisfy it. Do not label one feature universally easy or difficult to win.

---

## 4. Analyse the top 10 results

Run `phrase_organic` with `positions_type: organic` and the smallest limit that covers the requested organic result set. Use `positions_type: all` only as a separate SERP-feature discovery pass; feature-position rows are not additional organic rankings. Capture only returned fields as Semrush data:

- **Position and position type.** Preserve the raw values.
- **Domain and URL.** Keep the ranking URL, not only the root domain.
- **Triggered and domain SERP-feature codes.** Decode only from verified documentation.

Preserve the raw rows, but deduplicate identical ranking URLs when counting page formats, competitors, or the top-result set. If the same URL appears at multiple organic positions, record the positions and treat it as one page for page-level analysis. Never let duplicate feature rows inflate the number of competitors or observations.

Add the following only through a separate evidence source:

- **Manual page evidence:** title tag, visible page format, date, named experts, original data, tools, templates, examples, and directly measurable word count when useful.
- **Additional Semrush reports:** aggregate traffic, keyword, backlink, or Authority Score evidence only when the appropriate discovered report actually returns that field for the requested target.
- **Model judgment:** format classification, content angle, missing information, and opportunity assessment.

Do not attribute page traffic, referring domains, word count, Authority Score, or title tags to `phrase_organic`. Do not infer topical authority or ranking attainability from a fixed count of domains, URLs, links, or visits.

---

## 5. Determine the winning format

Classify each observed result, then report the actual distribution. Describe concentration as high, mixed, or uncertain and show the counts used for that judgment. Do not impose fixed universal cutoffs.

Flag outliers and explain what they add to the intent picture. Do not infer a publisher's topical authority solely from one ranking result.

Match format to intent:

- Informational: guide or article.
- Commercial-comparison: listicle, comparison table, or roundup.
- Transactional: product or pricing page.
- Conversational or troubleshooting: a direct answer, community perspective, support resource, or another format supported by the observed SERP.

---

## 6. Find the gap

The gap is a model-assisted hypothesis about how the user could better satisfy the observed intent. A gap does not guarantee ranking movement.

Four common gap categories.

- **Original data.** A survey, an internal study, a benchmark. The top 10 cite each other's data. New data instantly stands out.
- **Specific scope.** The top 10 are generic. Yours is for one industry, one use case, one persona.
- **Better-fit format.** The observed results leave a user need that a tool, calculator, template, checklist, video, or another suitable experience could address.
- **Recency and accuracy.** The top 10 cite stale facts. Yours cites current facts. The top 10 are wrong about something a specialist would catch. Yours is correct.

If none of these gaps is achievable, name that in the output. Some SERPs are saturated. The honest call is sometimes "don't write this; write something adjacent where the gap is real."

---

## How to report findings

Output a single evidence package with these sections.

### Keyword snapshot

State available volume, generic KD, intent, CPC, competitive density, and trend. Include the database, report, and unavailable fields.

### SERP features

List returned and manually observed features separately. For each, state the evidence, current holder when visible, applicable requirements, and confidence.

### Top 10 table

| Pos/type            | URL           | Returned features     | Observed format  | Page evidence         | Additional Semrush evidence               | Gap hypothesis              | Evidence status           |
| ------------------- | ------------- | --------------------- | ---------------- | --------------------- | ----------------------------------------- | --------------------------- | ------------------------- |
| [raw position/type] | [ranking URL] | [raw + decoded codes] | [model judgment] | [manual observations] | [report and actual value, or unavailable] | [clearly labeled inference] | [complete/partial/manual] |

### Recommended strategy

Recommend the best-supported format, angle, and relevant SERP features. State confidence and name the evidence that would change the recommendation.

### Reusable SERP evidence object

Return a compact structured block containing:

- keyword, database, collection date, and data sources;
- available keyword metrics and raw intent;
- ranked URLs with raw positions and feature codes;
- manually observed formats and page evidence;
- format distribution and fractured-intent assessment;
- gap hypotheses, limitations, and confidence.

Pass this object to `content-brief` when the user continues into brief creation.

Three rules for the report itself.

- State actual values with the evidence source. Never populate a metric column with a model estimate.
- Name one specific competitor URL for each pattern you flag. "Competitor.com/foo holds the featured snippet with a 3-row table" is actionable.
- If evidence suggests a poor fit or unusually strong competition, explain the evidence and recommend an adjacent target. Do not declare a SERP objectively unwinnable.

## Sources

This skill is grounded in the following Semrush editorial sources:

- [SERP analysis guide](https://www.semrush.com/blog/serp-analysis/)
- [SERP features reference](https://www.semrush.com/blog/serp-features-guide/)
- [What is search intent](https://www.semrush.com/blog/search-intent/)
- [People Also Ask guide](https://www.semrush.com/blog/people-also-ask/)
- [Featured snippets guide](https://www.semrush.com/blog/featured-snippets/)

When citing a specific recommendation inline, link to the article so the user can verify.
