---
name: schema-markup
description: Audit the structured data a page actually declares, decide which entities belong on it, and draft validated JSON-LD from verified facts only, separating Schema.org validity from Google rich-result eligibility. Use when the user asks about schema markup, structured data, JSON-LD, or whether a page is eligible for rich results.
---

# Schema markup

Audit what a page actually declares, decide which entities belong there, and produce validated JSON-LD only from verified facts. Never promise rankings, rich results, CTR gains, or AI citations.

## Rule provenance

Interpret material rules using these labels:

- **Semrush-supported guidance:** Methodology stated in a cited Semrush article. Preserve its scenario and caveats.
- **Current platform requirement:** A current Google Search Central or Schema.org requirement. This overrides stale editorial examples.
- **Industry implementation heuristic:** A defensible implementation practice, not a search-engine requirement or guaranteed outcome.
- **Configurable default:** A workflow or output choice that can change with the user's system and needs.

Keep the evidence source separate from the rule classification. Semrush MCP data, rendered-page evidence, validator output, user-provided facts, and model judgment must remain distinguishable in every result.

## Non-negotiable guardrails

- **Semrush-supported guidance:** Treat schema as machine-readable context and possible rich-result eligibility, not a direct ranking factor. State that valid markup does not guarantee a rich result.
- **Semrush-supported guidance:** Treat AI-visibility impact as uncertain. Do not claim that schema directly improves visibility in ChatGPT, Claude, Gemini, or other AI systems.
- **Current platform requirement:** Require markup to match visible page content and current facts. Use current Google Search Central requirements and Schema.org vocabulary when an editorial example is stale.
- **Current platform requirement:** Never invent ratings, review counts, prices, availability, dates, authors, addresses, logos, or other entity facts.
- **Workflow safety rule:** Never edit or deploy production code unless the user separately authorizes implementation.

## Before you start

Collect these inputs once:

- **Target:** exact URL, supplied markup, or domain with an existing Semrush project.
- **Mode:** audit, recommend, draft, validate, or monitor.
- **Page purpose:** homepage, article, product, review, video, local business, or another clearly identified type.
- **Evidence access:** rendered browser, raw HTML, Google validation output, Semrush MCP, Site Audit export, or user-provided facts.
- **Implementation context:** CMS or framework only when the user wants placement guidance.

If the page type or factual entity data is unclear, audit first. Do not generate deployment-ready code from guesses.

## Use the official Semrush MCP

Follow discovery → schema → execution. Do not substitute product-UI names for public MCP report identifiers.

### Project-backed Site Audit flow

1. Call `projects` to discover `list_projects`.
2. Call `get_report_schema` for `list_projects`, then `execute_report` to find an existing project for the domain.
3. Call `site_audit` to confirm the reports currently exposed.
4. Get the current `snapshots` schema, pass the project identifier using its required parameter (currently `id`, not `project_id`), then select the latest completed audit and record its date.
5. Use `meta_issues` to discover the issue catalog and its IDs and descriptions. Treat this as issue-definition metadata, not evidence that any listed issue occurred in the selected snapshot.
6. Select only issues whose returned descriptions concern markup or structured data.
7. Get the current `issue_details` schema, then use its required project, snapshot, and issue parameters with a small result limit to retrieve affected URLs. Do not send an optional `sort` value unless the discovered schema and execution both accept it; if execution rejects the optional sort, omit it rather than changing the evidence request.
8. For one exact crawled URL, use `page_list` to obtain candidate page IDs. Normalize the requested and returned URLs, select the exact match, and do not assume the first result is exact because the report can return prefix or approximate matches. Then use `page_info` for page-level evidence.

The verified public MCP does not expose a report named `markup` or the product UI's Markup thematic report. Never promise that report, a markup score, or hardcoded issue IDs.

### MCP constraints

- Projects access is read-only. Do not promise project creation, setting changes, or a fresh crawl.
- Report calls consume API units. Request only the fields and rows needed, then expand if necessary.
- Label findings with the Site Audit snapshot date and crawl coverage.
- Treat `issue_details` rows as occurrence evidence. An empty result means no matching rows were returned for that project, snapshot, and issue request; it does not prove that the rendered page is valid or free of all schema problems.
- A missing project, campaign, snapshot, issue type, field, subscription, or API-unit balance is an access limitation, not proof that the site has no schema problems.

## Evidence ladder

**Configurable default:** Use the strongest available evidence in this order and label it. Change the order when the user supplies more authoritative first-party or platform evidence.

1. Existing Semrush project and completed Site Audit snapshot.
2. User-supplied Site Audit or structured-data export.
3. Browser-rendered DOM inspection.
4. Google Rich Results Test or supplied validator output.
5. Raw HTML inspection.
6. User-supplied schema code and verified page facts.

Raw HTML can miss JSON-LD injected after page load. Do not report “no schema found” from a static fetch alone when JavaScript injection is possible.

## Supported v1 schema types

**Configurable product scope:** The types below define the first release; they are not a claim that other Schema.org types are unimportant.

Recheck current Google Search Central documentation before generating code because eligibility and property requirements change.

### Shared selection rules

- **Semrush-supported guidance:** Describe the primary visible entity, not the keyword the page targets, and prefer the most specific valid type that accurately fits the entity.
- **Current platform requirement:** Include properties only when their values are visible or user-confirmed. Do not add ratings, offers, authors, addresses, or media solely to satisfy a validator.
- **Industry implementation heuristic:** Reuse stable `@id` values to connect the same entities consistently across the site.

### Organization

Use on the canonical homepage or organization-defining page. Verify `name`, canonical `url`, crawlable `logo`, stable `@id`, and genuine `sameAs` profiles. Keep the identity consistent with publisher, seller, or provider references. Do not promise a Knowledge Panel.

Source: [Organization Schema](https://www.semrush.com/blog/schema-markup-for-company-corporations/)

### Article and BlogPosting

Use for visible editorial content. Verify `headline`, canonical URL or `@id`, representative `image`, truthful `datePublished` and `dateModified`, identified `author`, and a `publisher` linked to the site's Organization entity. Do not change dates merely to appear fresh or invent author credentials.

Source: [Schema Markup](https://www.semrush.com/blog/schema-markup/)

### Product and merchant listing

Use for a specific purchasable product. Verify `name`, image, description, product identifiers, and visible `offers` data such as price, currency, availability, URL, and seller. Add ratings or reviews only when genuine reviews are visible. Distinguish product-snippet eligibility from merchant-listing requirements using current Google documentation.

Sources: [Schema Markup](https://www.semrush.com/blog/schema-markup/) and [Rich Snippets](https://www.semrush.com/blog/rich-snippets/)

### Review and AggregateRating

Use only when the review or aggregate rating is visible and the reviewed item is unambiguous. Verify `itemReviewed`, author, review body when represented, rating value and scale, truthful rating or review counts, and visible dates. Check current Google policies for supported item types and self-serving review restrictions.

Source: [Review Schema](https://www.semrush.com/blog/review-schema/)

### VideoObject

Use when a video is a primary, watchable part of the page. Verify `name`, description, crawlable `thumbnailUrl`, truthful `uploadDate`, `contentUrl` or `embedUrl`, and duration when known. Add clip or live-stream properties only when supported by the page and video.

Source: [Video Schema](https://www.semrush.com/blog/video-schema/)

### LocalBusiness

Use for a physical business location. Prefer the most specific accurate subtype. Verify name, canonical URL, address, public telephone, opening hours, coordinates when known, relevant imagery, and one stable `@id` per distinct location. Do not merge locations with different addresses, hours, or phone numbers.

The reviewed English inventory has no dedicated current LocalBusiness article. Confirm this module against the canonical Semrush schema guide and current Google documentation before publication.

Source: [Schema Markup](https://www.semrush.com/blog/schema-markup/)

### Other detected types

Audit other types at a generic level: syntax, vocabulary, visible-content parity, identity, and duplication. Before generating code, review the current Schema.org definition and the corresponding Google feature documentation when one exists.

Do not prioritize FAQPage or HowTo generation in v1. Their Google search-feature treatment has changed, and the reviewed English Semrush inventory does not provide a strong current foundation for making them flagship modules.

## Workflow

**Industry workflow heuristic:** Use this sequence to keep detection, type selection, implementation review, drafting, and validation separate. Adapt it when the selected mode requires only part of the workflow.

### 1. Inventory existing markup

- Inspect rendered `script[type="application/ld+json"]` blocks.
- Inspect Microdata and RDFa when present.
- Parse JSON-LD objects, arrays, and `@graph` nodes; report parse failures without silently repairing the evidence.
- Record each entity's `@type`, `@id`, key properties, source URL, and extraction method.
- Identify duplicate IDs, conflicting properties, disconnected entities, and stale values.

Keep page evidence separate from Semrush crawl evidence. A Site Audit issue can identify affected URLs, but it does not replace inspecting the final rendered markup.

### 2. Determine schema fit

- Identify the page's primary entity and user-facing purpose.
- Select only schema types that describe visible content.
- Distinguish Schema.org validity from eligibility for a Google search feature.
- Explain why each proposed type applies or does not apply.
- Use the supported v1 guidance above before generating one of those types.

Diagnose other detected types when possible, but review current Google and Schema.org documentation before generating type-specific code outside the supported set.

### 3. Audit implementation quality

Check:

- JSON syntax and valid Schema.org terms.
- Current required and recommended properties for the relevant Google feature.
- Agreement with visible names, prices, currencies, availability, ratings, review counts, dates, authors, logos, addresses, and media.
- Canonical URLs, absolute asset URLs, and stable `@id` values.
- Correct entity nesting and relationships.
- Duplicate, contradictory, misleading, hidden, or stale properties.
- Whether the markup is crawlable and present in the rendered DOM.

**Industry implementation heuristic:** Prioritize issues by technical validity, policy risk, page importance, and likely search-presentation impact. Do not invent universal scoring bands.

### 4. Draft or correct JSON-LD

- **Current platform recommendation:** Prefer JSON-LD for new code when the site's setup allows it. Google also supports valid Microdata and RDFa.
- Generate only from visible or user-confirmed facts.
- Preserve valid identifiers when correcting existing markup.
- Use one coherent `@graph` when multiple entities need explicit relationships.
- Use stable absolute `@id` values, usually canonical URL fragments such as `#organization` or `#article`.
- Include only relevant properties. More markup is not automatically better.
- If required facts are missing, return a missing-information list instead of deployment-ready code.
- If a template is still useful, mark every placeholder clearly and label the block non-deployable.

### 5. Validate

**Industry workflow heuristic:** Validate in this order:

1. Parse the JSON-LD.
2. Confirm all terms against Schema.org.
3. Compare every factual property with visible page content.
4. Run Google's Rich Results Test for Google-supported features.
5. Reinspect the rendered page after implementation.

Do not treat a Schema.org-valid result as proof of Google rich-result eligibility. Do not treat validator warnings as errors without checking their meaning.

### 6. Hand off

Provide placement guidance appropriate to the user's CMS or framework, but do not deploy. Name the validation step and retest action when the user is coordinating implementation.

## Output contract

**Configurable default:** Return only the sections the selected mode needs:

1. **Executive verdict:** pass, needs work, or insufficient evidence.
2. **Evidence used:** Semrush snapshot, rendered page, raw HTML, validator, supplied code, and user facts.
3. **Markup inventory:** entity, type, key properties, extraction method, and source URL.
4. **Issue table:** priority, issue, affected property or URL, evidence, consequence, and fix.
5. **Recommended schema map:** page type → schema type → rationale.
6. **Corrected JSON-LD:** only when sufficient verified facts exist.
7. **Validation checklist:** syntax, vocabulary, content parity, Google eligibility, and rendered confirmation.
8. **Implementation notes:** placement, unresolved limitations, and retest action.

Keep these evidence classes visibly separate:

- **Semrush MCP:** project and Site Audit snapshot data.
- **Page evidence:** rendered or raw page content.
- **Validator evidence:** Google or Schema.org validation output.
- **User-provided facts:** business or entity information supplied directly.
- **Model judgment:** type selection, prioritization, and recommended relationships.

## Sources

Semrush methodology:

- [Schema Markup](https://www.semrush.com/blog/schema-markup/)
- [Video Schema](https://www.semrush.com/blog/video-schema/)
- [Rich Snippets](https://www.semrush.com/blog/rich-snippets/)
- [Review Schema](https://www.semrush.com/blog/review-schema/)
- [Organization Schema](https://www.semrush.com/blog/schema-markup-for-company-corporations/)

Technical sources of truth:

- [Google: Introduction to structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Google: General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org vocabulary](https://schema.org/docs/schemas.html)
