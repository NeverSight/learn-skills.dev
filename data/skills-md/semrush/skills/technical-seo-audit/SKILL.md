---
name: technical-seo-audit
description: Audit crawlability, indexability, HTTPS and redirects, Core Web Vitals, mobile parity, metadata, canonicals, structured data, and internal architecture using Semrush Site Audit data, separating confirmed defects from analyst judgment. Use when the user asks for a technical SEO audit or a site health check, why pages are not indexed, or why a site is losing search visibility for technical reasons.
---

# Technical SEO audit

Run a modular technical SEO audit that separates confirmed defects from product checks, external measurements, and analyst judgment. A missing meta description and an accidental `noindex` on a critical page are not equivalent.

## Rule provenance

- **Semrush-supported guidance:** crawlability, indexability, site architecture, HTTPS, redirects, mobile parity, performance, canonicalization, metadata, structured data, and rendered content are core technical SEO concerns.
- **MCP contract requirement:** project-backed findings come from the reports and fields exposed by the official Semrush MCP. The tested contract is issue-based; it does not expose named product-UI thematic reports.
- **Current platform standard:** sitemap limits, Core Web Vitals thresholds, mobile-first requirements, crawler controls, and structured-data eligibility come from the relevant primary platform documentation.
- **Industry heuristic:** business priority, expected impact, and remediation order are judgments unless supported by first-party data.
- **User-configurable default:** URL samples, pagination limits, and module depth depend on scope and available evidence. Do not use a fixed site-size or traffic cutoff.

## Inputs

Ask once for:

- root domain, exact URL, or URL set;
- full-site, template, or page-level scope;
- important page types and any known migration, rendering, or indexing incident;
- access to an existing Semrush Site Audit project;
- supplied Search Console, Analytics, CMS, crawler, performance, or server-log evidence.

Do not ask for a Semrush API key. The official MCP uses Semrush authentication.

## Official Semrush MCP workflow

1. Call `projects`, discover `list_projects`, retrieve its schema, and execute it.
2. Match the requested domain and confirm `siteaudit` is active.
3. Call `site_audit`, then discover and execute `snapshots` for the project.
4. Select the latest completed snapshot and retain its ID and finish date.
5. Execute `info` for crawl status, pages crawled, limits, issue totals, defects, redirects, blocked/broken counts, markup totals, and depth distribution.
6. Execute `meta_issues` to obtain the current issue catalog. Definitions are not current occurrences.
7. Join `info.defects` to `meta_issues`. Execute `issue_details` only for relevant issues with current counts, using the project ID, snapshot ID, issue ID, and a controlled limit.
8. For exact-URL investigation, use `page_list` to obtain the crawled page ID, then `page_info` to retrieve that page's issue rows.

Projects access is read-only. Never promise to create a project, change crawl settings, connect integrations, or launch a crawl. Issue IDs can change; rediscover them rather than hardcoding a permanent list.

## Evidence and access guardrails

- Tell the user that Semrush queries may consume API units. Use small diagnostic batches first and paginate when thorough coverage is requested.
- State the crawl's configured coverage. “Full audit” means the completed crawl within its settings and limits, not proof that every live or indexed URL was covered.
- An empty issue response is valid evidence of no returned occurrences for that issue and snapshot.
- Do not translate Semrush Error/Warning/Notice labels into Google penalties or ranking guarantees.
- Keep Semrush crawl data, Search Console evidence, performance measurements, direct HTTP/browser observations, and model inference separate.
- Search Console Performance has no “Last modified” dimension. Publication and modification dates must come from the CMS, sitemap, page metadata, or another supplied source.
- A `site:` query is a rough observation, not an authoritative index count.

## Fallback ladder

1. Existing Semrush project and completed Site Audit snapshot.
2. User-supplied Semrush Site Audit export.
3. Supplied crawler export plus Search Console, performance, CMS, or log data.
4. Direct HTTP and rendered-browser checks of a representative URL set.
5. User-supplied URLs and evidence.

Label levels 3–5 as sampled unless the supplied dataset establishes full coverage.

## Audit modules

Run crawlability and indexability first. Run the other modules required by the user's scope, then combine the findings.

### 1. Crawlability and indexability

Check:

- HTTP status and redirect behavior for important URLs;
- robots.txt syntax and rules that affect important pages or resources;
- XML sitemap availability, parsing, canonical URL format, and whether listed URLs are intended to be indexable;
- robots meta and `X-Robots-Tag` directives;
- canonical targets and conflicts;
- Search Console indexing evidence when supplied;
- blocked, uncrawled, 4xx, 5xx, sitemap, canonical, and duplicate-content issues returned by Site Audit.

A robots.txt block prevents crawling but does not guarantee deindexing. A missing robots.txt file is not automatically an SEO failure. A sitemap reference in robots.txt is useful but not required for a sitemap to work.

Google's XML sitemap limits are 50,000 URLs or 50 MB uncompressed per file. Treat these as platform limits, not Semrush heuristics.

### 2. HTTP, HTTPS, and redirects

Review:

- certificate validity and hostname match;
- consistent preferred HTTPS/host version;
- internal mixed-content links and resources;
- 4xx/5xx occurrences and the source URLs that expose them;
- redirect chains, loops, and avoidable internal redirect hops;
- permanent versus temporary redirect intent.

Use 301/308 for genuinely permanent moves and 302/307 for temporary moves. Do not claim temporary redirects inherently fail to pass link equity. A 404 can be correct for intentionally removed content; it becomes actionable when navigation, business importance, backlinks, or replacement intent justify a fix.

### 3. Core Web Vitals and performance

Use current Chrome UX Report/PageSpeed field data when available and distinguish it from Lighthouse lab data. Apply Google's current “good,” “needs improvement,” and “poor” thresholds at the 75th percentile:

| Metric |     Good |  Needs improvement |     Poor |
| ------ | -------: | -----------------: | -------: |
| LCP    |  ≤ 2.5 s |   > 2.5 s to 4.0 s |  > 4.0 s |
| INP    | ≤ 200 ms | > 200 ms to 500 ms | > 500 ms |
| CLS    |    ≤ 0.1 |      > 0.1 to 0.25 |   > 0.25 |

Do not guess the cause from the metric alone. Use diagnostics or implementation evidence before prescribing image, JavaScript, font, caching, or layout fixes. If field data is unavailable, label lab results as synthetic and page-specific.

### 4. Mobile parity and rendering

Because Google uses mobile-first indexing, compare mobile and desktop for:

- primary content;
- titles and meta descriptions;
- robots directives and canonical tags;
- internal links;
- images and alt text;
- structured data;
- renderable resources and interaction-dependent content.

Compare raw HTML with the rendered DOM when JavaScript supplies critical content or links. Do not infer parity from a desktop screenshot alone. Treat viewport, blocked-resource, JavaScript/CSS, and mobile usability findings as evidence to investigate, not automatic ranking penalties.

### 5. Titles, descriptions, headings, and canonicals

Use current Site Audit issue rows plus page-level inspection.

- **Title tag:** Semrush recommends a concise, descriptive, intent-aligned title at roughly 550 pixels or fewer—typically 50–60 characters—while noting that search and AI systems do not enforce a maximum. Treat this as display guidance, not a ranking guarantee or automatic failure.
- **Meta description:** Semrush's current editorial recommendation is to aim for a maximum of about 135 characters to reduce truncation risk. Meta descriptions are not a direct ranking factor, may be rewritten, and should be judged on accuracy and usefulness rather than length alone.
- **H1/headings:** recommend one clear main heading and a logical H1/H2/H3 hierarchy. Treat a single H1 as an editorial convention, not a universal ranking requirement. Titles and H1s should align on page purpose without having to match exactly.
- **Canonical:** verify syntax, target status, indexability, host/protocol consistency, duplication intent, and conflicts with redirects, sitemaps, hreflang, or internal links. Canonicals are signals, not commands.
- **Images:** require useful alt text for informative images and empty alt text for decorative images. Do not flag every empty alt as an error.

Duplicate or length-related metadata issues warrant review; they do not by themselves prove cannibalization, a penalty, or lost traffic.

### 6. Structured data

Use Site Audit markup counts and current structured-data issue occurrences as screening evidence. Static HTML alone can miss JavaScript-injected markup.

Delegate entity selection, rendered-markup inspection, JSON-LD drafting, and validation to the `schema-markup` skill. Keep only confirmed issue summaries and priority in this audit. Valid markup does not guarantee a rich result, and invalid or mismatched markup is not automatically a ranking penalty.

### 7. Architecture and internal linking

Use the crawl-depth distribution and current issues for orphan pages, broken internal links, redirects, missing/non-descriptive anchors, nofollow internal links, and underlinked pages.

Delegate the detailed remediation plan to `internal-link-audit`. Semrush Site Audit may flag URLs deeper than three clicks, but that product check is not a universal ranking law. Prioritize architecture changes using page importance, user journeys, crawl evidence, and supplied first-party performance data—not fixed keyword-volume or traffic thresholds.

### 8. AI crawler access

Read the current robots.txt rules and primary crawler documentation.

- `OAI-SearchBot` controls automatic crawling for inclusion in ChatGPT search results.
- `GPTBot` controls whether content may be used to train OpenAI's generative AI foundation models.
- `ChatGPT-User` is user-initiated and is not the control for Search inclusion.
- `Google-Extended` controls specified Gemini training and grounding uses; it does not affect Google Search inclusion or rankings.

Evaluate each user agent against the publisher's goals. Do not label blocking training crawlers as a technical SEO defect. For other AI crawlers, verify current first-party documentation before making a claim.

## Prioritization

Prioritize with this evidence-based order:

1. confirmed access, indexability, security, redirect-loop, or server failures affecting important URLs;
2. confirmed template-scale issues with clear user or search consequences;
3. field performance problems and mobile/rendering parity failures;
4. metadata, structured-data, and internal-link improvements;
5. sampled or inferred findings that require validation.

Do not estimate traffic, revenue, recovery time, or ranking impact without the user's first-party baseline and an explicit model.

## Output

Start with coverage:

| Evidence class | Source | Scope | Snapshot/date | Limitations |
| -------------- | ------ | ----- | ------------- | ----------- |

Then provide one remediation table:

| Priority | Module | Affected URL or pattern | Retrieved evidence | Interpretation | Action | Confidence |
| -------- | ------ | ----------------------- | ------------------ | -------------- | ------ | ---------- |

For every row:

- report the exact returned value, issue ID, or observed behavior;
- distinguish confirmed defect, Semrush product check, platform-standard failure, and analyst judgment;
- name the fix owner when it can be inferred—engineering, SEO, content, design, or infrastructure;
- avoid a “pass” unless the data source and tested scope actually support it.

End with:

1. **Fix now:** high-confidence blockers and broken behavior.
2. **Fix next:** validated template or experience improvements.
3. **Delegate:** Schema Markup or Internal Link Audit follow-up.
4. **Validate:** sampled, inferred, or missing first-party evidence.
5. **Unavailable:** modules or fields not tested.

## Sources

Semrush methodology:

- [Technical SEO](https://www.semrush.com/blog/technical-seo/)
- [Technical SEO Audit](https://www.semrush.com/blog/technical-seo-audit/)
- [Technical SEO Checklist](https://www.semrush.com/blog/technical-seo-checklist/)
- [Core Web Vitals](https://www.semrush.com/blog/core-web-vitals/)
- [Title Tags](https://www.semrush.com/blog/title-tag/)
- [Meta Descriptions](https://www.semrush.com/blog/meta-description/)
- [Canonical URLs](https://www.semrush.com/blog/canonical-url-guide/)
- [Robots.txt](https://www.semrush.com/blog/beginners-guide-robots-txt/)

Primary platform references:

- [Google Search Central](https://developers.google.com/search/docs)
- [Web Vitals](https://web.dev/articles/vitals)
- [OpenAI crawlers](https://developers.openai.com/api/docs/bots)
- [Google crawler controls](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)
