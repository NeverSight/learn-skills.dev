---
name: recover-content
description: >
  Diagnose and reverse traffic loss on existing pages. Use when the user asks
  about content decay, pages losing traffic, declining rankings, traffic drops,
  why a page stopped ranking, content refresh strategy, or when to consolidate
  vs redirect old content. For creating new content, see brief.
metadata:
  version: 1.0.0
---

# Recover Content

Diagnose and reverse traffic loss on existing pages using the decay triage
framework: refresh, consolidate, redirect, or retire.

## Before You Start

Gather this context (ask if not provided):

1. **Which pages are losing traffic?** Specific URLs or a general "the whole blog is declining."
2. **How much traffic was lost?** Percentage drop or absolute numbers.
3. **Over what timeframe?** Gradual decline over months vs sudden drop.
4. **Any recent changes?** Site redesign, CMS migration, content edits, algorithm update timing.

If the user doesn't know which pages are declining, suggest checking Google Search
Console → Performance → Pages, sorted by click change over the last 6 months.

## Identifying Decay

Content decay happens when a page gradually loses search traffic over time.
Common signals:

- Clicks declining month-over-month for 3+ months
- Position slipping from page 1 to page 2+
- Impressions stable but CTR dropping (competitors have better titles/snippets)
- Impressions declining (Google no longer considers the page relevant)

### Composite Decay Score

Score each page across 5 weighted signals to prioritize action:

| Signal | Weight | How to Score (0-100) |
|--------|--------|---------------------|
| Traffic decline | 30% | 0 = no decline, 50 = 20-40% drop, 100 = >60% drop |
| Position drops | 25% | 0 = stable, 50 = lost 3-5 positions, 100 = dropped off page 1 |
| CTR decline | 15% | 0 = stable, 50 = 20% decline, 100 = >40% decline |
| Content freshness | 15% | 0 = updated this quarter, 50 = 6-12 months stale, 100 = >2 years stale |
| Competitive displacement | 15% | 0 = no new competitors, 50 = new entrants on page 1, 100 = displaced from top 3 |

```
Composite Decay Score = (Traffic x 0.30) + (Position x 0.25) + (CTR x 0.15)
                      + (Freshness x 0.15) + (Displacement x 0.15)
```

| Score | Stage | Response |
|-------|-------|----------|
| 0-20 | Healthy | Continue monitoring |
| 21-40 | Early decay | Add to refresh queue (next month) |
| 41-60 | Active decay | Schedule refresh this week |
| 61-80 | Significant decay | Immediate refresh or rewrite decision |
| 81-100 | Terminal decay | Rewrite, redirect, or retire |

### Alert Priority Matrix

When multiple signals fire together, escalate:

| Signal Combination | Priority | Response Time |
|-------------------|----------|---------------|
| Traffic decline + Position drop | P1 Critical | Refresh within 48 hours |
| Traffic decline + CTR decline | P1 Critical | Rewrite title/meta immediately |
| Position drop + Competitor displacement | P2 High | Refresh within 1 week |
| CTR decline only | P3 Medium | Rewrite title and meta this week |
| Freshness indicators only | P3 Medium | Schedule refresh within 2 weeks |

## The Decay Triage Framework

For each decaying page, apply this decision tree:

### Decision 1: Is the topic still relevant?

- **Yes** → proceed to Decision 2
- **No** (product discontinued, event passed, technology obsolete) → **Retire**. 301 redirect to the closest relevant page or parent category.

### Decision 2: Is there another page on the site targeting the same topic?

- **Yes** → **Consolidate**. Merge the best content from both pages into one. 301 redirect the weaker page.
- **No** → proceed to Decision 3

### Decision 3: Has the search intent shifted?

Check what currently ranks for the target keyword. Has the SERP changed from:
- Listicles → long-form guides?
- Blog posts → product pages?
- Text → video?
- General → specific?

- **Yes, intent shifted** → **Rewrite**. Rebuild the page to match current intent. Keep the URL.
- **No** → proceed to Decision 4

### Decision 4: Is the content simply outdated?

Check for: stale statistics, outdated screenshots, deprecated tools/methods,
old dates in the title, broken external links.

- **Yes, outdated** → **Refresh**. Update facts, screenshots, examples, and dates. Add new sections covering recent developments.
- **No** → **Investigate deeper**. The issue may be technical (lost backlinks, slower page speed, mobile issues) or competitive (stronger pages now outrank).

## Refresh Playbooks by Content Type

Different content types require different refresh approaches. Use the matching playbook:

### Blog Post / Article (3-4 hours)

1. Update title with current year or fresh hook (10 min)
2. Rewrite introduction with a new angle (20 min)
3. Update all statistics with current sources (30-60 min)
4. Add 1-2 new sections covering gaps competitors address (60-90 min)
5. Update screenshots and images (30 min)
6. Add or refresh FAQ section with current PAA questions (20 min)
7. Refresh internal links to recent related content (15 min)
8. Update meta description (5 min)
9. Add or update schema markup — dateModified at minimum (10 min)
10. Republish with updated date and re-submit to Search Console (5 min)

### Statistics / Data Roundup (4-5 hours)

1. Verify every statistic — remove any without a current source
2. Replace outdated stats with current data (within 2 years)
3. Add new statistics from recent studies
4. Update all source links — replace broken citations
5. Update year references in title and body
6. Add a data visualization if none exists
7. Update meta description and title

### How-To Guide (3-3.5 hours)

1. Verify all steps still work as written
2. Update screenshots for any changed interfaces
3. Add new alternative methods if any have emerged
4. Update tool recommendations (remove deprecated, add current)
5. Add a troubleshooting section for common failure points
6. Update FAQ with recent questions
7. Test all external links

### Refresh Checklist (General)

For any content type, always complete:

- [ ] Update all statistics and data points to current year
- [ ] Replace outdated examples and screenshots
- [ ] Add new sections covering developments since last update
- [ ] Remove or update broken external links
- [ ] Improve the title and meta description (check competitor titles for CTR ideas)
- [ ] Add internal links from recent, related content
- [ ] Expand thin sections that competitors cover better
- [ ] Add original insights, data, or expert quotes (E-E-A-T signals)
- [ ] Update the published/modified date
- [ ] Re-submit to Google Search Console for re-indexing

## Consolidation Checklist

When merging two pages:

- [ ] Identify the stronger URL (more backlinks, better position, older)
- [ ] Move the best content from the weaker page into the stronger one
- [ ] Set up a 301 redirect from the weaker URL to the stronger one
- [ ] Update all internal links that pointed to the weaker URL
- [ ] Check for backlinks to the weaker URL — the redirect will pass authority

## Prioritization

Score each page for refresh priority:

| Factor | Weight |
|--------|--------|
| Current traffic value | 25% |
| Decay severity (composite score) | 20% |
| Competitive opportunity | 20% |
| Refresh difficulty (inverse — easier = higher) | 15% |
| Strategic importance (conversions, brand) | 10% |
| Backlink equity at risk | 10% |

Then rank pages:

| Page | Decay Score | Traffic Lost | Priority Score | Action | Effort |
|------|------------|-------------|---------------|--------|--------|
| ... | 72 (significant) | 1,200/mo | 85 | Refresh | 3-4 hrs |
| ... | 45 (active) | 300/mo | 60 | Consolidate | 2 hrs |

Focus on pages that (a) had the most traffic, (b) drive conversions, and (c) are
easiest to fix. A quick refresh on a high-traffic page beats a full rewrite on a
low-traffic one.

### Content Retirement Options

When a page can't be saved, choose the right exit:

| Option | When to Use |
|--------|------------|
| 301 redirect | Content has backlinks or residual traffic — send equity to closest relevant page |
| Consolidate | Multiple weak pages on same topic — merge best content into one URL |
| Noindex | Internal utility page that shouldn't rank but serves users |
| Delete (410) | No value, no links, no traffic — clean removal |

## Output Format

### Content Recovery Plan: [domain]

**Decay Summary**
- Pages analyzed: [count]
- Pages needing action: [count]
- Estimated traffic recoverable: [sum of lost traffic]

**Triage Results**

| Page | Traffic Lost | Diagnosis | Action | Effort |
|------|-------------|-----------|--------|--------|
| ... | ... | intent shift / outdated / cannibalization / irrelevant | refresh / consolidate / redirect / retire | low / medium / high |

**Priority Actions**

For each high-priority page:
- What specifically needs to change
- Which sections to update, expand, or remove
- Estimated impact if recovered

---

> **Pro Tip:** Use the free [Keyword Density Analyzer](https://seojuice.com/tools/keyword-density/)
> to check whether a declining page is still optimized for its target keyword. SEOJuice MCP
> users can run `/seojuice:content-strategy` to see active content decay alerts with severity
> ratings — the `list_content_decay` tool pulls pages losing traffic automatically.
