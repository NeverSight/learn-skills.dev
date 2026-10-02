---
name: ctr-snippet-optimization
description: >
  Improve click-through on pages that already rank, via titles, meta descriptions and
  snippet-level elements, safely and measurably. Use when a user says "my CTR is low," "improve
  my titles/meta descriptions," "pages at positions 3-15 get few clicks," "Google rewrote my
  title," or "A/B test titles." Not for pages that don't rank or aren't indexed (use
  content-opportunity-discovery / indexing-crawl-health-audit), traffic drops
  (traffic-drop-diagnosis), or length/uniqueness checks (technical-seo-audit).
---

# CTR and Snippet Optimization

Finds pages that rank but under-earn clicks versus the site's own norm, diagnoses why, rewrites truthfully, and measures on clicks. Title changes can move rankings: in bulk or untested they can lose position.

---

## Step 0 — Ask before assuming

1. Is Search Console (or Bing Webmaster Tools) data available via MCP, API or CSV export (page + query, last 3+ months)?
2. Are the pages templated (one title pattern across many) or unique?
3. Any title/description change on these pages in the last 6 weeks? (Open window: do not stack.)
4. Any brand-placement rule?
5. Success target: clicks on a page set, or one query?
6. Gate: run `seo-growth-stage-strategy` first; a site with very few impressions lacks the data for this work (prefer content/indexing work).

Search Console and Bing Webmaster Tools are free, need ownership verification, and are worth connecting. This skill still runs without them at reduced precision. Never block on it. No MCP connection: ask for a CSV export.

**If none of this can be answered:** work from observable data. Read live titles, descriptions, H1s and openings; search the target queries and note what is displayed; identify templates from URL patterns. Without click data you cannot rank by lost clicks or prove a lift: state "candidates inferred from on-page and SERP review, not confirmed by performance data" and give a measurement plan for when data exists.

---

## Step 1 — Find candidates from the site's own data

1. Pull page and page+query clicks, impressions, CTR, position: 28 days minimum, ideally 90. Split desktop/mobile.
2. Merge URL variants (trailing slash, parameters, www) first; split impressions mislead.
3. Bucket by position (1, 2-3, 4-5, 6-10, 11-20). Compute the site's OWN median CTR per bucket. Do not import external CTR-by-position tables.
4. Candidate = position roughly 3-15; impressions above a floor set relative to the site's distribution (agree it with the user; small counts are noise); CTR clearly below the own-bucket median; stable position (average position blends results; a wandering one makes CTR meaningless).
5. Exclude: branded queries; queries where a SERP feature, answer box or AI answer likely absorbs clicks (check in Step 2); intent mismatch (hand off to `content-opportunity-discovery`); indexing/canonical problems (hand off to `indexing-crawl-health-audit`); queries with a recent unexplained position drop (`traffic-drop-diagnosis`).
6. Rank by estimated lost clicks = impressions x (bucket median CTR - page CTR).
7. Google has documented logging errors that distorted impressions, CTR and average position (not clicks) over long periods. Check "Data anomalies in Search Console" against your window; if affected, rank on clicks and treat CTR gaps as provisional. Anonymized queries are omitted from query rows, so rows may not sum to totals.

## Step 2 — Look at the live result

For each candidate's top queries, check the live results (desktop and mobile, signed-out, right country/language). Record: the title and description Google actually displays (may differ from your tags and vary by query), competitors' framing, and any AI summary, answer box, rich result or sitelinks. Google documents that titles are generated automatically from several sources (title element, headings, og:title, prominent text, anchor text) and snippets from page content, sometimes the meta description, varying by query.

## Step 3 — Diagnose why clicks are low

Check in order:
- **Rewritten display:** Google replaced your title. Fix the cause (title contradicts H1/body, boilerplate, obsolete year/figure, several equally prominent headings) rather than polishing the tag.
- **Answer absorbed:** the result itself answers the query. Rewriting rarely helps; watch list.
- **Intent/relevance:** title does not match what the top queries ask.
- **Specificity:** generic wording; no concrete differentiator.
- **Truncation:** key term or value cut off. Google documents shortening only "to fit the device width" and gives no character or pixel limit. Any figure (for example the ~600px or ~60-character rules of thumb) is a practitioner heuristic: judge by the rendered live result on desktop and mobile.
- **Brand placement:** brand crowding out the topic.
- **Staleness/duplicates:** obsolete year or figure; near-identical titles competing for one query (`duplicate-intent-audit`).
- **Snippet controls:** nosnippet/max-snippet/data-nosnippet can cut the description; confirm intended.

## Step 4 — Write replacements

- Keep the primary query term near the front unless Step 3 shows it is the problem. Do not broaden into generic wording: more impressions with worse position is a regression.
- Lead with a specific value proposition the body delivers (figure, scope, audience, format). Brand short, at one end after a delimiter. No keyword lists, clickbait or unsupported superlatives.
- Every title and description must pass `protected-field-audit`: each figure, claim, year and superlative verified true against the body (use `verify-primary-source` for the value). Add a year only if the content truly reflects it.
- The meta description is a snippet candidate, not a ranking lever: unique, value matched to the query; Google may substitute page text. Length/uniqueness checks live in `technical-seo-audit`.
- Give 2-3 variants with reasoning; recommend one. Templated pages: change the pattern once, pilot on a small subset. Unique pages: one-off edits.
- An accuracy correction replaces only the wrong token; do not fold wording, length or brand changes into it.

## Step 5 — Gate, cap, baseline, control

Route every change through `measurement-discipline`. Do not edit pages ranking 1-3 or earning steady clicks without a documented diagnosis and user approval. Never rewrite many titles at once: pilot a handful of comparable pages (lowest impressions first); ask before any larger rollout. Before editing record per page: date, old/new text, 28-day clicks, impressions, CTR, position. One variable per batch (title OR description). Keep comparable unchanged pages as a control. Leave a page, and any competing page for its query, untouched while its window is open.

## Step 6 — Measure on clicks

Success metric is clicks. Compare equal-length, whole-week periods before and after, with the control over the same dates. Allow for recrawl (Google says days to weeks), then a full window; 4-6 weeks is a reasonable default, not a Google rule. Watch position: a click gain with a position drop, or a CTR rise from falling impressions, is not a win. CTR, impressions and position are supporting evidence only (Step 1 anomalies). Account for seasonality and algorithm updates via the control or year-on-year.

## Step 7 — Decide

- Clicks up vs control, position stable: keep; apply the pattern to similar pages next batch.
- Flat: iterate once on a different diagnosis; if still flat, watch list (likely SERP-level cause); revisit only with new SERP evidence.
- Clicks or position down vs control: revert to the logged previous text and note it.

## Step 8 — Log it

Record changes, baselines, measurement dates, results, reverts and watch-list decisions via `change-and-decision-log`.

---

## Output shape

1. Candidate list: page, top query, position, impressions, clicks, CTR, gap to site curve, estimated lost clicks; exclusions with reasons; data-anomaly check result.
2. Per candidate: what Google actually displays, diagnosis (Step 3 category), actionable or watch-list.
3. Proposed title/description (2-3 variants, one recommended) with truthfulness check result.
4. Batch size, baseline values, control group, template or page set, growth-stage gate result.
5. Measurement window (dates), success criterion in clicks vs control, revert rule.
6. Inferred vs confirmed statement, and log entry.
