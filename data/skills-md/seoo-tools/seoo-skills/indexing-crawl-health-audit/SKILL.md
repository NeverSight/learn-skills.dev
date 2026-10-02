---
name: indexing-crawl-health-audit
description: >
  Diagnose why pages are not indexed or crawled properly: triage Search Console and Bing
  page-indexing statuses, check robots.txt, sitemaps, canonical/noindex signals, redirects, status
  codes, soft 404s, rendering and server health, then fix and verify. Use when a user asks "why
  isn't my page indexed," "check my robots/sitemap/noindex/canonical setup," or what "Crawled -
  currently not indexed" means. NOT for traffic-drop investigation (traffic-drop-diagnosis), on-page
  tags (technical-seo-audit) or content quality (page-quality-audit).
---

# Indexing and Crawl Health Audit

Separates three causes of missing URLs: a technical block, a signal conflict, or an engine
quality/priority decision. Check and fix in that order. Weigh recommendations by site maturity per
`seo-growth-stage-strategy`; real emergencies (site blocked, mass noindex, sitewide 5xx) bypass it.

---

## Step 0 — Ask before assuming

1. Which URLs or page types are affected, how many versus how many exist, and which matter?
2. When did it start, and what changed just before (deploy, migration, CMS/plugin, robots.txt, CDN/firewall, URL structure)?
3. Is Google Search Console or Bing Webmaster Tools connected, and can the page-indexing report be exported?
4. How are pages rendered (server HTML, static build, client-side JavaScript), and are they templated?

Search Console and Bing Webmaster Tools are free, need ownership verification, and are worth
connecting. The skill still runs without them at reduced precision — do not block on it. If a
search/analytics MCP or CSV export is available, use it; otherwise fall back to the steps below.

**If none of this can be answered:** work from what is directly observable — fetch robots.txt, the
sitemap and a sample of live URLs (status, redirects, canonical, robots meta/header, raw versus
rendered HTML); treat a `site:` query as a rough signal only. State plainly what is confirmed
(observed now) versus inferred (engine behaviour you could not see).

---

## Step 1 — Triage with the page-indexing report

Export every not-indexed status with counts. Status names, meanings and sample caps change —
**re-verify against current Search Console Help and Bing documentation before reporting.** Samples
are capped, so confirm patterns at template level. Classify:

- **Technical blocks (fix):** server error (5xx), redirect error, blocked by robots.txt, noindex, 401/403/other 4xx, soft 404.
- **Signal outcomes (check intent):** page with redirect, alternate page with proper canonical, duplicate without user-selected canonical, duplicate where the engine chose a different canonical.
- **Engine decisions (not errors):** discovered - not indexed, crawled - not indexed.
- **Warnings:** indexed though blocked by robots.txt; indexed without content.
- **Not found (404):** fine if intentionally gone; a problem only if linked internally or in the sitemap.

Count only URLs you want indexed; excluded variants and retired pages are usually healthy.

## Step 2 — Check robots.txt

- Fetch per host and protocol: 200, within the size limit (re-verify). Per Google, a 4xx (except 429) means "no restrictions" and a persistent 5xx halts crawling.
- No blanket `Disallow: /` (common after staging deploys). Test `*`/`$` wildcards and precedence against sample URLs, including ones that must stay crawlable.
- robots.txt controls crawling, not indexing: a blocked URL can still be indexed from links, and a `noindex` on a blocked page is never seen. To de-index, allow crawling and use noindex (or 404/410).
- Do not block CSS, JS or data needed to render. Unsupported directives (e.g. crawl-delay for Google) do nothing.

## Step 3 — Audit the sitemap

- Only canonical, indexable, 200 URLs, absolute, matching canonical tags exactly (host, protocol, slash, case); no redirects, 404s, noindex, blocked or parameter URLs.
- Check per-file limits and index files against current Google and Bing docs. `lastmod` only for real content changes. Google ignores `priority` and `changefreq`.
- Compare submitted versus indexed per sitemap; confirm each is submitted in each engine and listed in robots.txt. Sitemaps are hints, not guarantees.

## Step 4 — Check canonical and noindex signals

- Indexable pages: one absolute self-referencing canonical, consistent with sitemap, internal links and redirects.
- Flag: noindex plus canonical elsewhere, canonical to a redirected/404/noindex page, chains, a template canonicalizing every page to one URL, JS-only canonical/noindex, multiple conflicting canonicals.
- Check meta robots AND `X-Robots-Tag` (including CDN/server rules) and staging or password settings leaked to production. Noindex is not a way to pick a canonical.
- Do not mix signals: Google documents redirects and `rel=canonical` as strong, sitemaps as weak; the engine may still choose its own.

## Step 5 — Redirects, status codes, server health

- Each URL resolves in one hop to a 200; flag chains and loops. Normalise variants (http/https, www, slash, case, tracking parameters): one form returns 200, the rest 301 or canonicalise.
- Redirect a removed URL only to a genuinely equivalent page; blanket redirects to a homepage or hub may be treated as soft 404s. A clean 404/410 is better.
- Error and empty-result pages must return 404/410, not 200.
- Intermittent 5xx/429 slows crawling. Check logs (verify genuine bots by reverse DNS, not user-agent), crawl stats, uptime, and whether a CDN, firewall or bot rule blocks crawlers that browsers pass.

## Step 6 — Rendering and discoverability

- Compare raw HTML with rendered DOM: are content, canonical and robots meta in raw HTML? JS cannot reliably remove a noindex.
- Key pages need crawlable `<a href>` links. Find orphans and dead internal links (`internal-linking-audit`); strip tracking parameters from internal links.

## Step 7 — Templated and programmatic pages

- Compare indexed versus not-indexed pages within a template. A whole template or thin subset excluded points to quality or duplication, not a fault (`duplicate-intent-audit`, `page-quality-audit`).
- "Crawled - not indexed" is an engine quality/priority decision; resubmitting does not fix it, improving or consolidating content might. Many are stale variants that clear once signals agree.
- "Discovered - not indexed" on a small site usually means low priority or weak internal links. Crawl budget matters mainly for very large or fast-changing sites (verify Google's current guidance).
- Faceted navigation, pagination and parameter URLs: keep crawl paths into near-infinite URL spaces closed and make sure each canonical URL is linked and in the sitemap (check Google's current guidance on faceted navigation). `hreflang` alternates must be reciprocal and point at canonical, indexable URLs.
- Do not noindex or delete URLs that earn clicks; if in doubt, leave them alone.

## Step 8 — Inspect individual URLs

- Sample with URL Inspection: indexed view = what the engine last stored (declared versus selected canonical, last crawl); live test = what is fetchable now.
- A passing live test does not guarantee indexing and follows redirects silently. Check manual-action and security reports separately.
- Request-indexing is quota-limited and repeats do not help; fix the cause, then use sitemaps for volume. Bing has URL Inspection and IndexNow; re-verify labels.

## Step 9 — Prioritise and fix

1. Site-wide blocks first (robots, mass noindex, server errors, firewall, broken deploys).
2. Template-level signal fixes (canonical, sitemap contents, redirect rules).
3. Sample before bulk: prove a fix on a few URLs before applying it to thousands.
4. Content and consolidation decisions last.

Gate risky changes (robots.txt, template-wide noindex/canonical, redirect rules, removals): sample test, rollback path, owner confirmation; chain/loop-check redirect rules. Never mass-submit URLs instead of fixing the cause, add noindex/redirects or delete pages just to tidy counts, or call a status an error without checking intent.

## Step 10 — Verify

- Re-fetch to confirm the fix is live (status, headers, canonical, robots).
- Use the report's validate-fix flow; validation and recrawls take days to weeks. Recheck at 2, 4 and 8-12 weeks.
- Measure by indexed counts and clicks. Search Console has documented logging errors affecting impressions, CTR and average position for some periods, and some search types affected clicks too; **check Google's Search Console data-anomalies page for the period before using any trend as evidence.**
- Log baseline and change (`change-and-decision-log`); isolate changes (`measurement-discipline`). Hand off: moved URLs to `site-migration-safety`, traffic loss to `traffic-drop-diagnosis`, ongoing watching to `seo-health-monitoring`, on-page tags to `technical-seo-audit`.

---

## Output shape

1. **Status table:** each not-indexed status, count, sample URLs, verdict (technical / signal conflict / engine decision / intentional), confirmed versus inferred.
2. **Findings by layer:** robots, sitemap, canonical/noindex, redirects/status/server, rendering/discovery, template quality — each with evidence.
3. **Prioritised fix list:** template-level first, with expected effect, risk and rollback.
4. **Verification plan:** what to recheck, when, and target counts (clicks and indexed URLs).
5. **Not checked / needs access:** what could not be examined and why.
