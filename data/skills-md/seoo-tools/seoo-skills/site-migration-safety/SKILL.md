---
name: site-migration-safety
description: >
  Protect search performance during any change that alters URLs or how pages are served: domain
  move, HTTPS/www/subdomain change, replatform or framework change, URL restructure, template or
  rendering rewrite, CMS change, hreflang/international restructure, or merging/deleting pages.
  Use when a user says "I'm moving my site," "we're changing our URL structure," "I'm merging
  these pages," or "did my migration break SEO?" Not for diagnosing an unexplained traffic drop
  (traffic-drop-diagnosis) or a general technical audit.
---

# Site Migration Safety

Changes to URLs, templates or serving lose rankings through avoidable mechanical errors. This
skill makes the change reversible, verified before launch, and monitored after it. Re-check every
time-sensitive detail below against current Google Search Central and Bing Webmaster docs.

---

## Step 0 — Ask before assuming

1. What is changing: domain, protocol/www/subdomain, URL paths, platform/CMS, templates or JavaScript rendering, languages/hreflang, or a set of pages?
2. Already live, or planned? (If live, start at Step 7.)
3. Scale: how many URLs, and which carry the traffic and links?
4. Can every old URL map to a new equivalent, or will some pages disappear?
5. Is there a staging environment that mirrors production, and who can run the rollback?

**If none of this can be answered:** infer from observable state (crawl the live site, read the
sitemap, test redirects on a sample, compare old and new hosts or templates) and label each
finding inferred vs confirmed. If the change already happened, run Step 7 first (and fix any
mechanical fault found, with confirmation), then rebuild Steps 2-3 from archives, sitemaps and logs.

Search Console and Bing Webmaster Tools are free; ownership is verified by DNS record, HTML file
or meta tag. Connect both (old and new properties) before any move; the baseline comes from them.
The skill still runs without them at reduced precision; never block on access. Use a
search/analytics MCP or CSV export if present; otherwise crawl, sitemap and server logs.

**Gate:** irreversible or live-traffic steps (redirect cutover, DNS change, deleting URLs or
content, removing the old host) need explicit user confirmation and a named rollback point first.

---

## Step 1 — Decide if it is necessary; scope the blast radius

- Name the benefit. If cosmetic or speculative, recommend not doing it. Check `seo-growth-stage-strategy`: a site early in growth has least to gain and the same exposure.
- Risk, lowest to highest: identical URLs and output; protocol/www change; path restructure or merge; domain move; any combined with a replatform or rendering change.
- Never bundle URL changes, redesign and content rewrites in one launch.
- Avoid the site's seasonal peaks. Large sites can move in sections to catch problems early; small and medium sites generally move at once (verify current guidance).
- Replatforms: confirm content, links and metadata reach Googlebot's rendered output, not only client-side JavaScript.

---

## Step 2 — Baseline and URL inventory

Capture, dated, before touching anything:

1. URL inventory: union of crawl, sitemap, Search Console pages with clicks (longest window available), analytics landing pages and server logs.
2. Most-linked URLs from a backlink export or links report; they get map priority.
3. Per URL: status, title, description, canonical, H1, robots directives, schema types, internal links in/out, hreflang.
4. Sitewide: robots.txt, sitemaps, redirect rules, analytics and verification tags, structured-data and image URLs.
5. Performance: clicks (primary), impressions, position, indexed count, top queries, sessions by landing page.
6. A rollback point: old site or config preserved and redeployable.

Record what could not be captured; it limits later verification.

---

## Step 3 — Redirect map rules

- 1:1 mapping to the closest equivalent: same topic and intent.
- Never redirect many URLs to the homepage or an unrelated page (Google documents this as a soft-404 risk).
- No equivalent: return 404 or 410 (Google treats both as removal). Do not redirect just to avoid a 404.
- Permanent moves: server-side 301 or 308 (Google treats both as a strong canonical signal). 302/307 only for genuinely temporary moves. Avoid JavaScript and meta-refresh unless server-side is impossible.
- No chains, no loops: point each source at the final destination; re-run a chain check after every addition. Aim for one hop; Googlebot's documented hop limit and chain advice are higher but verify them live.
- Every destination returns 200 (not a soft-404 page), with and without trailing slash.
- Handle protocol, www, trailing-slash, case and query-string variants by rule, not per URL.
- Update internal links, canonicals, sitemaps and hreflang to final URLs so nothing depends on a redirect.
- Do not block the old host's redirecting URLs in robots.txt; crawlers must reach them to see the redirect.

---

## Step 4 — Elements to preserve

Diff against the baseline: titles and descriptions; one real `<h1>`; self-referencing
canonicals; schema types and values (check each is still a supported type); internal links
including nav, footer and related modules; body content in the initial HTML; status codes;
hreflang (reciprocal, pointing at new URLs); image URLs; analytics and verification tags; robots
directives; anchors other links target. Anything dropped needs a stated reason.

---

## Step 5 — Staging and pre-launch tests

1. Crawl staging and diff against baseline: URL set, titles, canonicals, schema, links, statuses. Explain every difference.
2. Run the whole redirect map: one hop, correct type, final 200, no chains or loops; hand-check a sample.
3. Keep staging out of the index with noindex or access control (robots.txt alone does not prevent indexing). Never let staging be crawlable or linked. Put "remove staging block" in the launch checklist.
4. Sitemaps list only new canonical URLs; canonicals, sitemaps and redirects agree.
5. Crawlers can reach the new host (firewall, bot protection, valid TLS, CDN/edge rules); confirm with URL Inspection or a bot-user-agent fetch.
6. DNS or hosting moves: lower TTL ahead of the change (Google suggests at least a week; verify). Keep the verification method in the new copy.

---

## Step 6 — Launch checklist

- [ ] User confirmed go-live; rollback point, owner and command named.
- [ ] Staging blocks removed; production robots.txt, noindex and canonicals checked.
- [ ] Redirects live; top URLs by traffic and external links spot-checked.
- [ ] New sitemap submitted; old sitemap kept during transition.
- [ ] Search Console and Bing properties exist and are verified for the new host/domain (and old, kept); analytics firing; deploy annotated.
- [ ] Internal links point to final URLs; owned external profiles and key backlinks updated or requested.
- [ ] Change logged with baseline (Step 9).

**Domain or subdomain moves:** once redirects are live, use Google's Change of Address tool. It
covers only domain or subdomain changes (not HTTP-to-HTTPS, www-only, or path moves), needs
ownership of both properties and working redirects, and has a limited active period (documented
as 180 days; verify). Bing's Site Move tool is reported no longer in the current console; check
the live console, and rely on 301s either way. Keep the old property and verification in place.

---

## Step 7 — Post-launch monitoring and thresholds

Judge trends on clicks and sessions. Google has logged reporting errors that distorted
impressions, CTR and average position while clicks were unaffected; check its Search Console
data-anomalies page for the period before reading any of those. Compare like-for-like windows.

| Window | Check | Roll back if | Wait if |
|---|---|---|---|
| 0-24 hours | Top-URL statuses, 5xx/404 logs, crawler access, analytics | Site-wide errors, leftover noindex/robots block, broken redirects on top URLs | Brief crawl-rate dip |
| Days 2-14 | Indexed old vs new, new 404s, clicks vs baseline | Mass 404s on formerly working URLs, wrong canonicals | Gradual shift; fluctuation is expected |
| Weeks 2-6 | Clicks and top queries by page group | A traced mechanical fault with no quick fix | Partial recovery |
| Later | Like-for-like clicks vs baseline | Persistent loss, no cause: `traffic-drop-diagnosis` | Stabilising |

Roll back (with confirmation) for a traceable mechanical failure that cannot be quickly fixed; a
drop with no cause means diagnose first. Owner sets numeric thresholds and check cadence before
launch; no universal figure is documented. Google says moves take weeks or longer to reflect.
Keep redirects at least a year (Google); Bing suggests 1-2 years or longer; users may justify
keeping them indefinitely. Do not shut the old host while it still receives traffic. Route
crawl/index problems to `indexing-crawl-health-audit`.

---

## Step 8 — Consolidation (merging or deleting pages)

1. Find candidates with `duplicate-intent-audit`; check query-level data: complementary intents merge well, unrelated ones do not.
2. Pick the survivor by clicks, content quality, URL fit and backlinks. The higher-ranking page is not always the better content.
3. Merge unique content into the survivor, serving both intents; re-verify every moved figure (`verify-primary-source`).
4. With confirmation, 301 the retired URL to the survivor; point internal links straight at it; drop the retired URL from sitemaps; update canonicals.
5. Re-run the chain check; re-measure on the Step 7 windows, with a later final read.

---

## Step 9 — What not to do, and record-keeping

Do not: add noindex "to tidy up" without checking clicks; judge success from week one or from
impressions or position alone; remove the old host or properties early; make a second change
before the first window closes; repeat any Step 3-5 prohibition.

Log the change, baseline, map location, rollback point and re-check dates via
`change-and-decision-log`; measure per `measurement-discipline`. Hand off leftovers to
`technical-seo-audit` (templates) and `internal-linking-audit` (links to old URLs, orphans).

---

## Output shape

- Change type, risk level and reason; baseline captured (gaps).
- Redirect-map status: coverage, chains/loops, 404/410 decisions.
- Pre-launch test results and launch checklist, with confirmations obtained.
- Monitoring plan: windows, clicks-based signals, owner-set thresholds; rollback criteria and owner.
- Inferred vs confirmed, and anything unverified.
