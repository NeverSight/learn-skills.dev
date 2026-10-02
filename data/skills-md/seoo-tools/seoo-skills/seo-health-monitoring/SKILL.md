---
name: seo-health-monitoring
description: >
  Set up and run an ongoing SEO monitoring routine: what to check weekly, monthly and after
  changes, which movements are real alerts versus normal noise, how to calibrate thresholds to a
  site's own history, how to write a short health report, and which diagnostic skill to escalate
  to. Use for "set up SEO monitoring," "what should I check each week," "write my monthly SEO
  report," "how do I know if something's wrong," "set up alerts." Not for root-cause diagnosis
  (traffic-drop-diagnosis) or a one-off audit (site-audit-orchestrator).
---

# SEO Health Monitoring

A small, repeatable routine that notices real problems early without reacting to noise. Clicks are the primary metric; everything else supports or explains it. Alerts trigger diagnosis and an owner decision, never automatic site changes.

---

## Step 0 — Ask before assuming

1. What data exists: Search Console, Bing Webmaster Tools, analytics, server logs, an MCP connection, CSV exports?
2. How often will this run, and by whom (human, agent, scheduler)? Who reads the report?
3. Which page groups (by template/type) are critical, and roughly how many search clicks per day?
4. Is there a change ledger (`measurement-discipline`, `change-and-decision-log`)?
5. Growth stage: run `seo-growth-stage-strategy` if unknown. Early or small sites need only the minimal routine; mature sites add segments and event checks.

Search Console and Bing Webmaster Tools are free, need ownership verification, and are worth connecting. The skill still runs without them at reduced precision (analytics, spot-checks); say so, never block. Use an MCP connection or API if present, else CSV exports, else give the human the exact screens to read and a template for pasting results.

**If none of this can be answered:** propose a minimal default: a 10-minute weekly check (Step 3), a monthly review (Step 6), and event checks after deploys. Assume clicks are the only trend metric, segments are "whole site," the homepage and one top template, and the reader is a human. Label thresholds as defaults; mark inferred versus confirmed.

---

## Step 1 — Define "healthy"

- Primary metric: clicks from search, per engine (Google and Bing separately).
- Secondary signals, fixed and few: the Step 3 items.
- Segment by page template or group (and branded versus non-branded if available) so one failing template is not hidden in a flat total.
- Record a baseline: weekday and weekend clicks, 28-day total, indexed count.

## Step 2 — Cadence

- **Weekly (about 10 minutes):** Step 3.
- **Monthly (30-60 minutes):** Step 6, 28 days versus the prior 28.
- **Event-driven:** after any deploy, template, redirect, robots or sitemap change, or confirmed Google update, check the affected group around days 2, 7 and 14.
- Too heavy to run? Cut signals, not cadence. Do not watch clicks daily.

## Step 3 — Weekly checklist

1. **Known issues:** read Search Console's "Data anomalies" help page and Google's Search Status Dashboard. Google discloses logging errors with dates, metrics and reports. A web-search error affecting impressions, CTR and position did not affect clicks, but other disclosed errors (for example Discover and job-listing appearance data) did reduce clicks for those reports. Read the live entry before trusting or discounting any figure.
2. **Clicks:** last full 7 days versus the prior 7 and versus the same weekdays 4 weeks back, by segment. Never judge preliminary days (dotted line); default margin 2 days.
3. **Indexing:** indexed and not-indexed counts versus last week; new error or exclusion reasons. Example URL lists are capped; trust counts and trends.
4. **Crawl/server errors:** 5xx, 404 spikes, redirect errors, blocked resources (Crawl stats report, server logs).
5. **Sitemaps:** processed without errors.
6. **Messages:** Search Console Messages, Manual actions and Security issues reports, and Bing's equivalents. Email is not a sufficient check alone.
7. **Top pages and queries:** biggest gainers and losers; any top-20 page that vanished. Anonymized queries are omitted from rows, so rows will not sum to totals.
8. **Spot-check 3-5 key pages:** status 200, indexable, canonical correct, content renders.
9. **Cross-reference** movements with the ledger and deploys first.

## Step 4 — Alerts and noise

Impressions, CTR and average position are never alert triggers on their own; they can support a clicks- or indexing-based finding but are skewed by reporting errors and SERP changes.

**Thresholds below are practitioner starting defaults, not Google figures.** Calibrate: take 8-12 weeks (more if available; Search Console history is limited (check current retention), so export to preserve history) of same-weekday week-over-week click changes per segment. Set Warning near the edge of normal variation (for example the 90th percentile of absolute changes), Critical at about twice that. Re-calibrate quarterly and after traffic-level changes.

- **Critical (diagnose now, notify owner):** site or key templates unreachable or erroring; robots.txt or noindex blocking key pages; manual action or security issue; sharp indexed-count drop (default: more than 30% in a week); clicks down more than 50% versus same-weekday baseline for 3+ consecutive complete days with no seasonal explanation.
- **Warning (investigate this week):** clicks down 25-50% two weeks running; one segment down 30%+ while others are flat; a new indexing error type or growing not-indexed count; sitemap errors; a top-10 page losing most of its clicks.
- **Info (log only):** single-day swings, weekend dips, flat-net page moves, impression or position drift, gains.

Noise rules, applied before alerting:
- Same weekday to same weekday.
- Search Console dates are Pacific Time.
- Small numbers (default: under about 100 clicks per segment per period): use a longer window.
- Seasonality: compare with the same period last year where history exists.
- One day is never a trend; require duration plus a second signal.
- Broad movement (many unrelated pages, same time) suggests technical or external cause; narrow suggests page-level. State which.
- More than a couple of alerts a month: thresholds are too tight.

## Step 5 — Escalation

| Signal | Route to |
|---|---|
| Sustained clicks decline, cause unknown | `traffic-drop-diagnosis` |
| Indexed count falling, rising not-indexed, crawl or sitemap problems | `indexing-crawl-health-audit` |
| Template-level canonical, robots or structured-data faults | `technical-seo-audit` |
| Drop after migration, domain, URL or platform change | `site-migration-safety` |
| Stable position, clicks falling | `ctr-snippet-optimization` |
| Slow decay on aging pages | `content-freshness-audit` |
| Link-related manual action | `backlink-profile-audit` |

Before escalating, check the ledger and known issues. Make no page edits, rollbacks or removals in response to an alert until the cause is classified and the owner has decided.

## Step 6 — Monthly review

1. **What changed:** deploys, content batches, known Google updates.
2. **What moved:** 28-day clicks versus prior 28 by segment; gainers and losers; indexed trend.
3. **Ledger check:** measure changes whose window (`measurement-discipline`) has closed; record results.
4. **Decisions:** at most 3-5 actions, each with owner, expected effect, re-check date; log per `change-and-decision-log`.

## Step 7 — Report rules and automation

- Lead with a one-line verdict (Healthy / Watch / Problem) and the single recommended next action.
- Show date ranges and an as-of date; note excluded days. Mark claims confirmed or inferred; name data gaps.
- Only Step 1 signals; no vanity metrics; weekly report fits one screen.
- Agent can automate: data pulls, same-weekday comparisons, threshold checks, spot-check fetches, drafting. A human must: verify ownership, read Messages if not exposed to the agent, decide and make any site change.
- Verify time-sensitive facts (latency, retention, notification behavior) against current Search Console Help. Analytics sessions are not search clicks (consent, tagging, time zone, bots differ).

## Step 8 — What not to do

- React to daily data, or to impressions, CTR or position alone.
- Treat one day or an unfinished period as a trend.
- Change several things in an open measurement window.
- Auto-revert, auto-redirect or auto-edit because an alert fired.
- Report everything.

---

## Output shape

**Weekly health check:** as-of date and data range, verdict, one next action, then one line per Step 3 signal (OK / Warning / Critical plus evidence). End with what is inferred rather than confirmed.

**Monthly report:** 1) Verdict and top action. 2) Clicks by segment, current versus prior 28 days, with dates. 3) Indexing and technical status. 4) Changes and ledger results. 5) Alerts and resolutions. 6) Decisions and plan with re-check dates. 7) Data caveats and what was not checked.
