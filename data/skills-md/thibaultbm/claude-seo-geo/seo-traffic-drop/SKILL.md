---
name: seo-traffic-drop
description: "Diagnose a traffic or ranking loss before fixing anything. Input: Search Console exports from a healthy period and a damaged one, plus what changed on the site. Output: whether the drop is real or a reporting artifact, the exact date and shape of the loss (visibility, ranking, click-through, demand), the pages and queries carrying it, a differential diagnosis with the test that confirms each cause, and the handoff to the skill that fixes it. Bundled zero-dependency script compares two exports and dates the drop. Use when traffic fell, rankings dropped, impressions or clicks collapsed, a core update landed, pages got deindexed, a migration or redesign went wrong, or a client asks what happened."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Traffic drop: find what changed before changing anything

A drop is a diagnostic problem, not a content problem. The failure mode of this work is not missing the cause, it is acting on the first plausible one: a core update landed near the date, so the team rewrites 40 articles, while the actual cause was a `noindex` shipped in a template on the same week. The rewrite then hides the evidence.

So the order is fixed. Confirm the loss is real, date it, shape it, name the candidate causes, confirm one with a test that could have failed, and only then fix. Every step below produces evidence someone else can check.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: the SEO action log (what was shipped and when), past incidents, the site's seasonality, migrations, and known technical debt. The action log is the highest-value note in a drop investigation, because it answers "what changed" without waiting for the client. At the end of the session, append the diagnosis, the evidence and the remediation to that log so the next incident starts with a history.

## When to use this skill

Use it for:

- "Our traffic dropped", "we lost rankings", "clicks fell off a cliff"
- Impressions or clicks collapsing in Search Console, on the whole site or one section
- Pages disappearing from the index, or a sudden coverage change
- A suspected core update, a manual action, or a penalty
- Traffic loss after a migration, a redesign, a replatform or a big deploy
- Sessions falling in GA4 while Search Console looks fine, or the reverse
- AI referral traffic falling, or the brand losing its citations in AI answers

Hand off once the cause is named:

| Confirmed cause | Skill that fixes it |
|---|---|
| Indexation, robots, rendering, speed, migration, hack | seo-technical |
| Client-rendered site built by an AI generator | seo-ai-site-builders |
| Thin, stale or outranked content | seo-content-blog and the page-type content skills |
| Blocks missing from a page that competitors have | seo-page-sections |
| Cannibalization, orphaned pages, weak internal links | seo-internal-linking |
| Lost or toxic backlinks | seo-backlinks |
| Local pack or Business Profile loss | seo-local |
| Lost AI citations, AI Overview displacement | geo-visibility |
| No measurement to detect the next one | geo-tracking |

## Step 0: Freeze the scene

Before any analysis, stop changes to the site. Every deploy during an investigation destroys evidence and adds a variable, and a drop that gets "fixed" mid-diagnosis by three simultaneous changes teaches nobody anything.

Collect, in this order:

1. Search Console exports: the performance report for the damaged period and for an equal-length healthy period, same property, same filters. Export Queries, Pages, and Dates. Equal length matters: comparing 28 days against 90 measures the calendar.
2. The deployment and release log, or a git log, covering the six weeks before the drop.
3. Anything non-technical that changed: a rebrand, a price change, a product discontinued, a campaign that ended, a season that turned, a competitor that launched.
4. Search Console Manual Actions and Security Issues. Two clicks, binary answer, and it reframes everything if positive.

If the client cannot say what shipped and when, that gap is itself a finding worth reporting.

## Step 1: Is the loss real

Three things masquerade as traffic drops. Rule them out before spending a day on causes.

**Reporting artifacts.** Two documented events sit inside the window most investigations look at:

- The num=100 removal of September 2025. Rank trackers stopped loading 100-result pages, so many properties saw desktop impressions collapse and average position improve overnight, with clicks flat (https://searchengineland.com/google-num100-impact-data-462231).
- The Search Console impression logging error, disclosed on the Data Anomalies page: from 13 May 2025 until the fix rolled out on 27 April 2026, impressions were logged inaccurately, which also distorted CTR and average position. Clicks were not affected, and Google did not reconstruct the historical data. Any before-and-after comparison spanning 27 April 2026 therefore compares inflated impressions against corrected ones (https://support.google.com/webmasters/answer/6211453 and https://www.seroundtable.com/google-search-console-fix-data-logging-issue-41260.html).

The operating rule that survives both: **clicks are the metric that pays**. An impressions drop with flat clicks is a measurement story until proven otherwise. Check the Data Anomalies page for the period under investigation before writing any conclusion.

**Measurement breakage.** If GA4 fell but Search Console did not, the problem is downstream of Google: a tag removed in a redesign, a consent banner change, a bot filter, a new cookie mode, a GA4 property or filter change. Compare Search Console clicks against GA4 organic sessions over the same days. They never match exactly; they should move together.

**Seasonality and demand.** Compare against the same period last year, not last month. A B2B site in August and a tax service in May both look catastrophic month-over-month and are perfectly normal year-over-year. When rankings hold and impressions fall, verify the trend in Google Trends before diagnosing anything on the site.

## Step 2: Date the drop

    python3 scripts/gsc_diff.py --dates Dates.csv

The script reads a day-level export and reports the shape: a **cliff** (one day carries most of the decline, and the site stays down) or a **slope** (the loss accumulates over weeks). It dates the onset and lists the steepest steps. It discriminates by asking how much of the total decline the single steepest step explains, which is robust where counting days over a threshold is not.

The distinction sets the whole investigation:

| Shape | What it means | First question |
|---|---|---|
| Cliff | A site event or a switch being flipped | What shipped on that exact date |
| Slope over 1 to 3 weeks | An update rollout, or a competitor gaining | Which confirmed update overlaps this window |
| Slope over months | Decay, staleness, or a market moving | Which pages lost first, and what replaced them |
| Step down then partial recovery | A temporary block, an outage, a crawl issue | What was broken and for how long |

For update windows, use the Google Search Status Dashboard, which publishes confirmed ranking updates with official start and end dates (https://developers.google.com/search/help/status-dashboard). A drop that starts three days before an update window did not come from that update, and this single check kills most false attributions.

## Step 3: Shape the loss

    python3 scripts/gsc_diff.py before/Pages.csv after/Pages.csv --sections 2
    python3 scripts/gsc_diff.py before/Queries.csv after/Queries.csv --top 25

The script reports totals with deltas, names the mechanism, measures how concentrated the loss is, lists the biggest losers with a per-row reason, flags rows that disappeared entirely, and shows what gained while the rest fell. `--sections N` aggregates URLs by path prefix, which is how a template-level cause becomes visible in one line.

Four mechanisms, distinguished by which metric moved:

| Mechanism | Signature | Reading |
|---|---|---|
| Visibility collapse | Impressions and clicks fall together, rows disappear | The pages are not being shown. Indexation, not ranking |
| Ranking loss | Position worsens materially, impressions follow | Being outranked. Update, regression, lost links, cannibalization |
| Click-through loss | Impressions and position hold, clicks fall | Still ranking, not being clicked. SERP layout, AI Overviews, titles |
| Demand or coverage loss | Position holds, impressions fall, CTR holds | Fewer searches or fewer matching queries. Verify externally |

Then read concentration and gainers together. A loss carried by a handful of URLs is a page-level cause; a loss spread across one directory is a template cause; a loss across everything is an update, a sitewide technical regression, or demand. And a page that gained while a similar page fell is the signature of cannibalization or internal redistribution, which has an internal cause and no amount of update analysis will explain it.

## Step 4: Differential diagnosis

Match the shape to the candidates, then run the confirming test. The test matters more than the table: a cause you cannot confirm is a guess with a citation.

| Signature | Likely causes | Test that confirms or kills it |
|---|---|---|
| Cliff, everything, impressions to near zero | noindex shipped, robots.txt Disallow, DNS or certificate expiry, server outage, domain not renewed, WAF blocking Googlebot, hack | Fetch the raw HTML and robots.txt; Search Console URL Inspection on three URLs; check the Pages report reason; check server logs for Googlebot 4xx and 5xx |
| Cliff, everything, impressions intact | Manual action, or a tracking or property change | Search Console Manual Actions; confirm the property and filters are the same in both exports |
| Cliff, one section or template | A template regression: canonical pointing elsewhere, noindex on a template, internal links removed, rendering switched to client-side, pagination broken | Compare the raw HTML of a losing page against an archived copy; check the canonical and meta robots as served; run the rendering check from the seo-ai-site-builders skill |
| Cliff, right after a migration or redesign | Redirects missing or chained, URLs changed, content dropped, hreflang broken | Crawl the old URL inventory and check every 301 resolves in one hop to a relevant page; the migration protocol lives in seo-technical Step 7 |
| Slope over 1 to 3 weeks, sitewide, positions worse | A core or ranking system update | Confirm the window on the Search Status Dashboard; check whether losses concentrate on a content type; compare against competitors in the same SERPs |
| Slope, positions hold, CTR falls | AI Overviews or a new SERP feature on those queries, rewritten titles, competitor snippets | Inspect the live SERP for the top losing queries; measure how many now carry an AI Overview; check whether Google rewrote the titles |
| A handful of URLs, others gaining | Cannibalization from a page published recently, or an internal link change | Query-level export: does the losing URL's query now map to another URL of yours; check what was published in the six weeks before |
| Gradual, oldest content first | Content decay, staleness, competitors publishing better | Run `scripts/content_decay.py` (below) to list the decaying pages by mechanism; compare the losing pages against what now ranks with page_benchmark.py; check publication and update dates |
| One country or one language only | Geo-blocking by a WAF or CDN, hreflang regression, a local competitor, a market event | Fetch the site through an exit in that country; check hreflang reciprocity |
| One device only | Mobile rendering or speed regression, an interstitial, a mobile template bug | Test the mobile page directly; compare Core Web Vitals per device |
| Clicks fell, conversions and revenue did not | The lost traffic was low value, or the loss is in a non-commercial section | Segment by page group and by landing page revenue before treating this as an emergency |
| Impressions fell, clicks flat | A reporting artifact, or lost long-tail visibility | Check the Data Anomalies page for the period; confirm whether the loss is in positions 20 to 100 |
| Search Console flat, GA4 down | Tagging, consent, bot filtering, a GA4 configuration change | Compare Search Console clicks against GA4 sessions day by day; check the tag fires |

**Content decay, page by page.** When the shape is a slope and no update or event explains it, the loss is usually many pages eroding at once. Export Pages.csv for the last 3 months, the 3 months before, and the same months a year earlier (and optionally crawl the site), then:

```
python3 scripts/content_decay.py --current last3m.csv --previous prev3m.csv --last-year ly3m.csv --crawl crawl.json
```

Each page that lost 20%+ of its clicks is classified: ranking loss (position worse by 1+), CTR loss (position and impressions flat, CTR down: often an AI Overview), demand loss (impressions down, position flat), seasonal (flat year over year), or vanished (absent from the latest export: check status, noindex, redirect). Stale pages (a past year in the title, no update for 12+ months, from `site_crawl.py --out crawl.json` in seo-internal-linking) are listed first. The refresh itself follows the page skill of the page type.

Rules that keep this honest:

- Correlation with an update date is not a diagnosis. Updates are the most over-attributed cause in the field, because the date is public and the alternative requires work.
- Two causes can coexist, and often do. A site can lose to an update and ship a broken canonical in the same month. Quantify each rather than picking a winner.
- The absence of a finding is a finding. Write down what you checked and ruled out, or the next person repeats it.

## Step 5: Quantify, then decide what is worth fixing

Not every loss is worth recovering. Before recommending work, split the loss into: recoverable by fixing something broken, recoverable by outcompeting, and structurally gone.

Structurally gone is a real category in 2026: queries absorbed by AI Overviews, informational traffic that now resolves in the answer, a product line discontinued, a market that shrank. On the AI Overview side the measured impact varies widely by study and query set, from roughly 15 percent to over 50 percent fewer clicks on affected queries (Amsive across 700,000 keywords at the conservative end, Pew across 68,000 queries near the middle, Ahrefs and Seer at the high end), so treat any single figure quoted at you as a range and measure your own queries rather than importing someone else's number.

One split in that data is directly diagnostic. In the Amsive set, non-branded queries with an AI Overview lost about 20 percent of their CTR while branded queries with one gained about 19 percent, and the worst case was a query carrying both an AI Overview and a featured snippet, at roughly 37 percent lost. So a CTR loss concentrated on non-branded, informational queries fits the AI Overview explanation; a CTR loss that includes branded queries does not, and points instead at a title rewrite, a brand problem, or a SERP competitor. Segment branded against non-branded before accepting the easy answer.

What this traffic is not is recoverable by rewriting the page: the fix is to compete for the citation and for the queries that still produce clicks, which is the geo-visibility skill's territory.

Say this plainly in the deliverable. A recovery plan that implicitly promises a return to a pre-AI-Overview baseline sets up a failure that no amount of good work will avoid.

## Step 6: Fix, then verify with a date

Hand the confirmed cause to the skill that owns it (table in the "When to use" section), then:

1. Record the fix date. Recovery is measured from it, not from the drop.
2. Set the re-measure date honestly: a technical fix needs a recrawl before anything moves, so weeks on a site of any size. Recovery from an update usually waits for the next update; Google's own guidance is that there is nothing to fix in the sense of a penalty, and that broad recoveries often come with later updates (https://developers.google.com/search/docs/appearance/core-updates).
3. Re-run the same comparison on the same dimension after the fix, so the before and after come from the same instrument.
4. Write the incident into the vault action log: date, shape, evidence, cause, fix, outcome. The second occurrence of the same cause is diagnosed in minutes if this exists.

## Rules and thresholds

| Check | Target | Basis |
|---|---|---|
| Compared periods | Equal length, same property, same filters | Field rule |
| Material drop | 10 percent of clicks or more | Field heuristic |
| Metric of record | Clicks, always. Impressions are context | Field rule after two documented logging artifacts |
| Manual actions check | Before any analysis | Official (binary and cheap) |
| Seasonality | Year over year, never month over month | Field rule |
| Update attribution | Only when the window is confirmed on the Search Status Dashboard and the drop starts inside it | Official plus field rule |
| Cause confirmation | Every named cause has a test that could have falsified it | Field rule |
| Site changes during diagnosis | Frozen until the cause is named | Field rule |
| Recovery expectation | Weeks after recrawl for technical fixes; next update for update losses | Official (core updates guidance) |
| Incident record | Written to the vault action log with evidence | Field rule |

## GEO layer

Two AI-specific failure modes do not appear in Search Console at all, so a drop investigation that stops at GSC will miss them.

**Losing the citation while keeping the ranking.** A page can hold position 3 and stop being the source AI Overviews, ChatGPT or Perplexity quote. Classic metrics stay flat while the brand disappears from the answers that increasingly precede the click. Detection is a prompt panel, not a rank tracker: the protocol is in the geo-tracking skill, and the citability work is in geo-visibility.

**Losing AI referral traffic.** Referrals from chatgpt.com, perplexity.ai and similar sources fall when the site stops being retrievable: a rendering regression makes content invisible to crawlers that never execute JavaScript, a robots.txt change blocks an AI crawler, or a migration breaks the URLs the engines had learned. This drop is invisible in Search Console by construction. Check the AI channel in GA4 first, then the crawler access rules in the seo-technical reference, then rendering with the seo-ai-site-builders script.

The reverse case matters for honest reporting: when classic clicks fall while AI referrals and branded search rise, the site is not losing, the channel is shifting. Report both or the conclusion is wrong.

## Output format

    # Traffic drop diagnosis: {domain} ({date})

    ## Verdict
    One sentence: what happened, when, and how confident you are.

    ## Is it real
    Artifacts, measurement and seasonality ruled out, with the check that ruled each one out.

    ## When
    The date or window, the shape (cliff or slope), and what shipped around it.

    ## Where
    The mechanism (visibility, ranking, click-through, demand), how concentrated,
    which sections, pages and queries carry the loss, with the numbers.

    ## Why
    The confirmed cause, the test that confirmed it, and the causes ruled out
    with the evidence that ruled them out.

    ## What is recoverable
    Split into: broken and fixable, competitive, structurally gone. With numbers.

    ## Plan
    Ordered fixes, each with its owning skill, effort, and expected effect.

    ## Re-measure
    The date, the exact comparison to re-run, and the baseline to beat.

Never deliver a diagnosis without the two numbers that anchor it: clicks lost, and the share of that loss the named cause explains.

## Common mistakes

| Mistake | Consequence | Do instead |
|---|---|---|
| Blaming the nearest core update | Months of content work on a broken canonical | Confirm the window on the Status Dashboard and check the drop starts inside it |
| Reading an impressions drop as a traffic loss | Emergency response to a logging fix | Check clicks first, then the Data Anomalies page |
| Comparing unequal periods | Measuring the calendar | Equal length, same property, same filters |
| Month-over-month on a seasonal site | Diagnosing August | Year over year |
| Fixing during the investigation | Evidence destroyed, cause never known | Freeze the site until the cause is named |
| Shipping five fixes at once | No attribution, no learning | One change at a time on a dated timeline |
| Skipping the manual actions check | Weeks lost on the wrong hypothesis | Two clicks, first |
| Stopping at the first plausible cause | The real one keeps operating | Run the confirming test, and quantify each cause |
| Treating AI Overview losses as recoverable by rewriting | Promises that cannot be kept | Segment it as structural, compete for the citation |
| Ignoring gainers in the same export | Missing cannibalization entirely | Read gainers against losers |
| Diagnosing only in Search Console | AI citation and referral losses invisible | Check the AI channel and the prompt panel too |
| No incident record | The same cause diagnosed from scratch next year | Write it to the vault action log |

## Sources

- Search Console Data Anomalies (the official list of known reporting issues): https://support.google.com/webmasters/answer/6211453
- The 50-week impression logging error and its 27 April 2026 fix: https://www.seroundtable.com/google-search-console-fix-data-logging-issue-41260.html
- num=100 removal and its impression impact: https://searchengineland.com/google-num100-impact-data-462231
- Google Search Status Dashboard, confirmed update windows: https://developers.google.com/search/help/status-dashboard
- Google guidance on core updates and recovery: https://developers.google.com/search/docs/appearance/core-updates
- AI Overviews click impact, conservative end, with the branded and non-branded split (Amsive, 700,000 keywords): https://www.amsive.com/insights/seo/google-ai-overviews-new-research-reveals-how-to-navigate-click-drop-off/
- AI Overviews click impact (Ahrefs): https://ahrefs.com/blog/ai-overviews-reduce-clicks/
- Zero-click and CTR trend into 2026: https://searchengineland.com/google-ai-overviews-ctr-recovery-study-475566
- Field heuristics: 115+ agency audits, labeled as such throughout
