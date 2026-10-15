---
name: internal-link-audit
description: Audit internal linking to find orphan pages, broken internal links, crawl-depth problems, and weak anchor distribution, then plan the hub-and-spoke structure that fixes them. Use when the user asks about internal links, orphan pages, site architecture, crawl depth, or how to pass authority to priority pages.
---

# Internal link audit

Audit a site's internal linking and produce an evidence-labeled remediation plan. Answer three questions:

1. Which important pages are difficult or impossible to reach through internal links?
2. Which internal links are broken, redirected, non-descriptive, or otherwise inefficient?
3. Which contextual links and hub relationships would make the architecture clearer?

Do not treat internal linking as a quota exercise. Recommend links only when the source, destination, and user journey are contextually related.

## Rule provenance

Keep these evidence classes distinct in the analysis and final output.

- **Semrush-supported guidance:** internal links help search engines discover pages, communicate hierarchy and context, and distribute authority. Semrush recommends descriptive anchors, relevant hub-and-spoke relationships, and supporting new content with contextual incoming links.
- **MCP contract requirement:** project-backed findings come only from reports and fields returned by the official Semrush MCP. A product-UI feature name is not an MCP report name.
- **Industry heuristic:** prioritization based on business importance, likely user impact, or remediation effort is analyst judgment unless backed by supplied first-party data.
- **User-configurable default:** limits, samples, and priority weights must adapt to the site's size, goals, and available data. Never turn them into universal SEO rules.

## Inputs

Ask once for:

- the root domain;
- the pages or page types most important to the business;
- any known migrations, redesigns, or architecture constraints;
- whether the user wants a full project-backed audit or a supplied-export/manual sample.

Do not ask the user to paste a Semrush API key. The official MCP uses Semrush authentication.

## Official Semrush MCP workflow

Use discovery and schema retrieval before every report whose parameters are not already known.

1. Call `projects`.
2. Discover `list_projects`, retrieve its schema, execute it, and match the requested domain exactly. Confirm that `siteaudit` is activated.
3. Call `site_audit`.
4. Discover and execute `snapshots` with the project ID. Select the latest completed snapshot and retain its `snapshot_id` and finish date.
5. Execute `info` for crawl status, pages crawled, issue counts, redirect counts, and crawl-depth distribution.
6. Execute `meta_issues` to get the valid issue IDs and definitions. This is a catalog, not proof that every issue exists on the site.
7. Read the current issue counts from `info.defects`. For each relevant issue that has a nonzero count, execute `issue_details` with the project ID, issue ID, snapshot ID, and a controlled limit. Paginate only as needed.
8. Use `page_list` and then `page_info` only when an exact crawled URL needs page-level inspection.

The tested public MCP exposes issue-based Site Audit reports, not a literal **Internal Linking thematic report**. Relevant issue IDs discovered during the live contract test included broken internal links, orphaned sitemap/Google Analytics pages, page crawl depth, pages with only one internal link, redirect chains, permanent and temporary redirects, nofollow internal links, links with no anchor text, and non-descriptive anchors. Always rediscover the live catalog instead of hardcoding those IDs as a permanent contract.

Projects access is read-only. Never promise to create a project, change crawl settings, connect Analytics, or run a new audit. If no matching project or completed snapshot exists, state that limitation and use the fallback ladder.

## Access and evidence guardrails

- Tell the user before execution that Semrush queries may consume API units. Start with the smallest result set that can establish the issue, then expand when the user wants exhaustive rows.
- An empty `issue_details` response means the selected snapshot has no returned occurrences for that issue. Do not turn it into a tool failure or invent examples.
- A missing project, inactive Site Audit tool, missing snapshot, unavailable field, or execution error ends only that data branch. Explain what cannot be established.
- Do not infer sitewide coverage from a sample, sitemap alone, or manually supplied URL list.
- Do not claim that Site Audit returns organic traffic, conversions, keyword volume, anchor distribution, or a complete inbound-link graph unless the executed report actually contains those fields.

## Fallback ladder

Use the strongest available source and name it in the output.

1. Existing Semrush project with a completed Site Audit snapshot.
2. User-supplied Semrush Site Audit exports.
3. Crawler export plus sitemap and, if supplied, Analytics or Search Console landing-page data.
4. Sitemap and a manual sample centered on the user's important pages.
5. User-provided URL list.

Label levels 3–5 as sampled unless the supplied data demonstrably covers the full site.

## Workflow

### 1. Establish coverage and architecture

Record:

- domain and selected snapshot date;
- audit status and pages crawled;
- available depth distribution;
- important pages supplied by the user;
- data sources and coverage limitations.

Infer the architecture only from observed navigation, URLs, sitemaps, or supplied documentation. A flat distribution does not by itself prove that search engines cannot understand the site.

### 2. Find orphaned or underlinked pages

An orphan page has no crawlable incoming internal link in the dataset used to identify it. Site Audit may expose separate orphan issues based on sitemap or connected Analytics data; report the source because those populations differ.

For each returned URL, determine whether the page should be:

- linked from contextually related pages or an appropriate hub;
- consolidated or redirected to a current equivalent;
- intentionally excluded from search; or
- removed, subject to content, traffic, conversion, and backlink review.

Semrush's editorial guidance suggests aiming for two or three contextual incoming links when publishing new content. Treat that as an editorial aim, not an automatic failure threshold for every existing URL and not a promise of ranking improvement.

Do not call a page a high-traffic orphan unless first-party or executed Semrush data actually establishes its traffic.

### 3. Review broken links and redirects

For every occurrence returned by `issue_details`, retain the source URL, destination URL when present, HTTP status or issue information when present, issue ID, and snapshot date.

Recommend one of:

- update the source link to the correct live destination;
- redirect the obsolete destination when a true replacement exists and broader inbound references justify it;
- remove the link when no useful destination exists;
- update internal links to the final URL when they traverse avoidable redirect chains.

Use a 301 or 308 for a permanent move and a 302 or 307 for a temporary move. Do not claim that temporary redirects inherently fail to pass link equity.

### 4. Review crawl depth

Use `info.depths` for the distribution and the current depth issue from `info.defects` plus `issue_details` for affected URLs. Semrush Site Audit may flag pages that require more than three clicks, but this is a product check, not a universal ranking law.

Prioritize depth changes when the user identifies the page as important or when supplied first-party evidence shows meaningful demand or business value. Do not impose keyword-volume cutoffs or require every important page to be linked from the homepage.

### 5. Review anchor and nofollow issues

Use the discovered issues for missing anchors, non-descriptive anchors, and internal nofollow links when they have current occurrences.

- Prefer concise anchor text that describes the destination in natural language.
- Avoid generic text such as “click here” when a descriptive phrase would help users understand the destination.
- Do not flag exact-match internal anchors merely because they are exact match. Review repetition, context, and readability.
- Do not claim a destination's complete anchor distribution unless the data source provides it.
- Review internal `nofollow` case by case. Do not say the attribute categorically prevents all value from flowing or automatically order its removal.

### 6. Recommend contextual hubs and links

Identify hub-and-spoke opportunities from observed topical relationships, navigation, and supplied content data. A hub should organize a meaningful topic for users; it is not automatically the URL with the most internal links.

For every proposed link, name:

- the source URL;
- the destination URL;
- why the relationship is useful;
- a descriptive anchor suggestion;
- the evidence source;
- confidence.

Do not require a fixed number of sideways links, a homepage link for every hub, or a new pillar page for every cluster.

## Output

Start with an evidence summary:

| Evidence class     | Source                           | Coverage                       | Snapshot or date | Limitations                   |
| ------------------ | -------------------------------- | ------------------------------ | ---------------- | ----------------------------- |
| Semrush Site Audit | Project and snapshot             | Full crawl or configured crawl | Date             | Crawl limits and integrations |
| User data          | Analytics/export/sitemap         | State actual scope             | Date             | Missing fields or date range  |
| Manual observation | Reviewed URLs                    | Sample                         | Date             | Not sitewide                  |
| Model inference    | Architecture/link recommendation | Derived                        | Date             | Requires human validation     |

Then provide a prioritized remediation table:

| Priority | Issue | Source URL | Destination or affected URL | Evidence | Recommended action | Confidence |
| -------- | ----- | ---------- | --------------------------- | -------- | ------------------ | ---------- |

Prioritize using observed business importance, severity, scale, and effort. If the user has not supplied business or performance data, say so and avoid pretending that priority equals expected traffic or revenue impact.

End with:

1. **Fix now:** confirmed defects affecting important pages or navigation.
2. **Improve next:** well-supported contextual-link or architecture opportunities.
3. **Validate first:** sampled, inferred, or integration-dependent findings.
4. **Unavailable evidence:** reports or fields the audit could not access.

## Sources

Semrush methodology:

- [Internal Links: Ultimate Guide + Strategies](https://www.semrush.com/blog/internal-links/)
- [9 Common Internal Linking Mistakes](https://www.semrush.com/blog/internal-linking-mistakes/)
- [Orphan Pages: How to Find and Fix Them](https://www.semrush.com/blog/orphan-pages/)
- [Website Architecture: Best Practices for SEO](https://www.semrush.com/blog/website-structure/)

Primary technical reference:

- [Google Search Central: Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
