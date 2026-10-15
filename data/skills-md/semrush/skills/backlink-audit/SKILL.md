---
name: backlink-audit
description: Audit a domain's backlink profile — anchor distribution, referring domains, toxic patterns, competitor link gaps, and broken-link recovery — and produce an evidence-labeled action plan. Use when the user asks for a backlink audit, whether their links are toxic or spammy, where competitors get links they do not have, or how to recover lost links.
---

# Backlink audit

Audit a domain's backlink profile and produce an evidence-labeled action plan. Answer four questions:

1. What does the current backlink profile actually contain?
2. Which links or patterns deserve human review?
3. Which competitor referring domains are plausible opportunities?
4. Which linked target pages may need restoration, updating, or redirection?

Do not call a backlink toxic, harmful, or safe from one metric. Do not recommend disavowal from an automated pattern alone.

## Rule provenance

- **Semrush-supported guidance:** evaluate relevance, authority, placement, anchor context, referring-domain diversity, link attributes, historical patterns, and competitor overlap together. Manual review is required for risk decisions.
- **MCP contract requirement:** the public MCP exposes Backlink Analytics reports. It does not expose Backlink Audit Toxicity Score, toxic markers, removal lists, or disavow workflows in the tested contract.
- **Industry heuristic:** risk labels, opportunity tiers, and outreach priority are analyst judgments unless the user adopts explicit criteria.
- **User-configurable default:** competitor count, row limits, date windows, and weighting must fit the site's market and purpose. No Authority Score or link-count cutoff is universally valid.

## Inputs

Ask once for:

- the root domain or exact URL to audit;
- competitors, if the user wants a gap analysis; otherwise offer to identify search competitors separately;
- known link-building, sponsorship, affiliate, migration, or negative-SEO history;
- whether Google Search Console shows a manual action for unnatural links;
- the user's priority pages and markets.

Use a product-approved connector or supplied Search Console evidence. If the user has not verified Manual Actions, label that status **unconfirmed**. Do not ask for a Semrush API key; the official MCP uses Semrush authentication.

## Official Semrush MCP workflow

Discover the report family, retrieve the schema, and then execute only supported reports.

### Profile reports from `backlinks_research`

- `backlinks_overview`: aggregate Authority Score, backlinks, referring domains, referring IPs, indexed URLs, and follow/nofollow/sponsored/UGC counts when requested.
- `backlinks_refdomains`: referring domains, domain Authority Score when explicitly requested, backlink count, first/last seen, IP, and country.
- `backlinks_anchors`: anchor, referring-domain count, backlink count, and first/last seen.
- `backlinks`: source and target URLs, anchor, dates, and supported link flags. Use it for row-level inspection, not as proof of editorial placement without reviewing the source page.
- `backlinks_historical`: monthly backlink and referring-domain trends.
- `backlinks_pages`: target pages with response code, backlink count, referring-domain count, and last seen. Use the exact returned field meanings; this report does not itself prove current referral traffic or conversions.

### Comparison reports from `competitors_research`

- `backlinks_comparison`: one aggregate row per supplied target.
- `backlinks_matrix`: referring domains and backlink counts across supplied targets. To find gaps, filter the analyzed domain's bucket to zero and retain rows where at least one competitor's count is greater than zero.

`targets` and `target_types` are parallel arrays and must have equal lengths in the same order. Never describe `backlinks_matrix` as a separate Backlink Gap product report or add product-UI fields the schema did not return.

## Access and evidence guardrails

- Tell the user that Semrush calls may consume API units. Start with a useful sample and paginate when thorough coverage is requested.
- Request `authority_score` or `domain_authority_score` explicitly when needed. Use the label **Authority Score** only when that exact field was returned.
- Keep Semrush metrics, user-supplied evidence, manual page inspection, and model judgments separate.
- Authority Score is a comparative Semrush metric, not Google's score and not proof that a link is good or bad.
- Follow/nofollow composition, country, IP, first-seen date, and anchor text are context—not standalone risk verdicts.
- The tested public MCP does not return Toxicity Score. If the user supplies a Backlink Audit export, label its toxicity fields as product data that still requires human review.
- If a report is empty or fails validation, state what is unavailable. Do not silently substitute a different metric or fabricate a risk assessment.

## Fallback ladder

1. Official Semrush MCP Backlink Analytics reports.
2. User-supplied Semrush Backlinks or Backlink Audit exports.
3. Google Search Console Links export for the user's own sampled data.
4. Other user-supplied backlink data.

Competitor gaps are unavailable unless competitor backlink data exists. Search Console's Links report is a sample and must not be described as a complete backlink index.

## Workflow

### 1. Establish the profile snapshot

Run `backlinks_overview` and record:

- target and target type;
- Authority Score when requested and returned;
- backlinks and referring domains;
- referring IPs and indexed URLs when returned;
- follow, nofollow, sponsored, and UGC counts when returned;
- data source and retrieval date.

Use `backlinks_comparison` when competitors are supplied. Compare scale and composition without claiming that the domain with more referring domains will rank higher.

### 2. Review referring domains and links

Run `backlinks_refdomains`, then inspect selected rows with `backlinks` where context matters. Evaluate:

- topical and audience relevance;
- editorial standards and real user value;
- source-page context and placement;
- link attributes;
- patterns across domains, IPs, dates, anchors, and target pages;
- whether compensated links are appropriately qualified.

Do not infer a PBN from low Authority Score, shared IP, or timing alone. Do not call repeated links from one domain worthless; identify possible sitewide placement and review the source pages.

### 3. Review anchors

Run `backlinks_anchors`. Classify anchors transparently when useful—such as branded, compound, exact match, partial match, related, naked URL, generic, image/empty, or page title—but label this categorization as model or analyst inference unless supplied by a report.

Investigate unusual concentration in context. There is no universal healthy percentage for any anchor class, and exact-match text is not proof of manipulation. Consider target page, referring domains, placement, acquisition history, and whether the pattern was intentionally created.

### 4. Review risk without inventing toxicity data

Use Backlink Analytics to surface review candidates, not to issue a toxicity verdict. Look for combinations such as:

- paid follow links or large-scale exchanges;
- automated, low-editorial-control placements;
- networks that appear controlled for link manipulation;
- unrelated or misleading anchors at scale;
- unexplained historical spikes;
- contractual, widget, affiliate, or sponsored links without suitable qualification.

For every candidate, state the retrieved evidence and what still requires manual review. A language or country mismatch can be normal for an international business.

### 5. Apply the disavow safety gate

Google says the disavow tool is an advanced feature that can harm performance if used incorrectly. Recommend considering it only when both conditions are supported:

1. there is a considerable number of spammy, artificial, or low-quality links; and
2. those links caused a manual action or are likely to cause one.

First consider removal or proper qualification for links the site owner created or controls. Do not generate or upload a disavow file unless the user explicitly requests that separate high-risk action after reviewing the evidence. Do not promise a recovery timeline.

### 6. Find competitor referring-domain gaps

Run `backlinks_matrix` with the user's domain first, followed by valid competitors, and matching `target_types`. Filter for zero links to the user's target and one or more links to competitors.

For each returned referring domain:

- preserve the per-target counts and Authority Score only if returned;
- inspect actual competitor source pages before calling it an opportunity;
- assess relevance, editorial fit, link context, and whether the user's asset genuinely belongs;
- distinguish editorial outreach, partnership/sponsored possibilities, broken-link replacement, and “not a fit.”

Do not apply blanket Authority Score, recency, or competitor-count cutoffs. A matrix row proves backlink overlap, not the precise linking page, contactability, or likelihood of winning a link.

### 7. Review linked target pages

Run `backlinks_pages` to identify target pages and returned response codes. A non-200 response or obsolete target deserves investigation, but verify the live URL and replacement relationship before prescribing a redirect.

Choose among:

- restore or update the original resource;
- redirect permanently to a genuinely equivalent page;
- contact linking sites to update the destination;
- leave the URL unchanged when the response or replacement cannot be validated.

Do not say a redirect recovers a fixed percentage of value, and do not prioritize solely by an Authority Score or referring-domain threshold.

## Output

Start with evidence coverage:

| Evidence class | Source/report | Scope | Available fields | Limitations |
| -------------- | ------------- | ----- | ---------------- | ----------- |

Then present:

### Profile comparison

| Target | Authority Score | Backlinks | Referring domains | Follow | Nofollow | Evidence date |
| ------ | --------------: | --------: | ----------------: | -----: | -------: | ------------- |

### Review candidates

| Priority | Referring domain/source | Target | Retrieved evidence | Manual finding | Recommended action | Confidence |
| -------- | ----------------------- | ------ | ------------------ | -------------- | ------------------ | ---------- |

### Competitor opportunities

| Referring domain | User links | Competitor links | Retrieved AS | Source-page fit | Opportunity type | Confidence |
| ---------------- | ---------: | ---------------: | -----------: | --------------- | ---------------- | ---------- |

### Linked target-page recovery

| Target URL | Response code | Backlinks | Referring domains | Verified replacement | Action | Confidence |
| ---------- | ------------: | --------: | ----------------: | -------------------- | ------ | ---------- |

End with:

1. **Act now:** confirmed issues with clear ownership and low ambiguity.
2. **Review manually:** candidates that need source-page or acquisition-history validation.
3. **Build next:** credible competitor or recovery opportunities.
4. **Do not act:** automated or isolated signals without corroborating evidence.
5. **Unavailable:** Toxicity Score, manual-action status, or other data not actually supplied.

## Sources

Semrush methodology:

- [Toxic Backlinks: What They Are & How to Find Them](https://www.semrush.com/blog/toxic-links-guidelines/)
- [How to Get Backlinks](https://www.semrush.com/blog/how-to-get-backlinks/)
- [What Are Backlinks?](https://www.semrush.com/blog/what-are-backlinks/)
- [How to Find Competitor Backlinks](https://www.semrush.com/blog/competitor-backlinks/)
- [What Is Anchor Text?](https://www.semrush.com/blog/anchor-text/)
- [Link Building in SEO](https://www.semrush.com/blog/link-building/)
- [How to Find Backlinks to Your Site](https://www.semrush.com/blog/find-backlinks/)

Primary safety reference:

- [Google Search Console: Disavow links to your site](https://support.google.com/webmasters/answer/2648487)
