---
name: twitch-category-opportunity-research
description: Compare Twitch categories using Crawlora current game totals, top live streams, channel metadata, schedules, VODs, and clips. Use for a streaming category shortlist or content-planning brief with live concentration, top-N sampling, timing, and audience/revenue limits preserved.
---

# Twitch category opportunity research

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Build a content-planning brief for a creator's specified categories, language,
format, timezone, schedule, and goals. These public snapshots describe observed
live supply and visibility, not a forecast of the creator's audience or revenue.

## Discover categories and collect aligned snapshots

- Use top games or Twitch search to resolve actual category slugs. Top games is
  a viewer-ranked list capped at 100, not every category. `viewers_count` is the
  category's current aggregate live viewers, while `streams` returns top live
  channels by viewers with its own limit/cap and no exposed exhaustive pagination.
- Query chosen categories within a narrow collection window and retain each
  timestamp and limit. Game IDs, slugs, broadcaster IDs/logins, stream IDs, VOD
  IDs, and clip IDs are different identifiers. Resolve returned channel logins
  before profile, schedule, videos, or clips.
- Preserve freeform stream tags/language cues with their original evidence;
  tags are not a verified curated demographic taxonomy. Scheduled category is
  planned content, not proof a broadcast happened. Schedules cover up to four
  weeks; an empty configured schedule does not establish channel inactivity.
- Use selected VODs/clips only for visible format/title/duration and dated content
  examples. A clipped moment is a curated sample, not representative coverage
  of all the creator's broadcasts. Missing/expired VODs remain unavailable evidence.

```sh
scripts/crawlora.sh /twitch/top-games limit=10
scripts/crawlora.sh /twitch/search query="strategy games" limit=5
# Select a returned category slug and comparable collection limits:
# scripts/crawlora.sh /twitch/streams game="$CATEGORY_SLUG" limit=20
```

## Compare concentration and practical hypotheses

Show category aggregate viewers separately from the returned top-stream viewer
sum and sample size. A matched near-synchronous top-N share can describe observed
concentration, but do not divide by a top-N subtotal and call it full-category
share. Differently timed calls can disagree; keep a discrepancy rather than forcing
sums to match. The returned stream count is not the total competing stream count. Category totals
are global; a language-tag-filtered top-stream sample does not supply that
language's total audience or competition denominator.

Live concurrent viewers, VOD views, clip views, followers, and schedule hours
are different measures. Do not add them into unique audience, retention, discoverability,
or monetisation forecasts. No audience-demographic or sponsor-ROI conclusion
follows from these fields. Comparisons across time slots need actual repeat
observations with fixed queries and windows, not inferred schedules.

Return a category/snapshot ledger, source-bounded concentration table, relevant
content/schedule examples, fit to the creator's stated constraints, and testable
content hypotheses with uncertainty. A small apparent category is not proof of
an opportunity or unmet demand. Do not start streams, contact creators/sponsors,
create accounts, or schedule ongoing monitoring unless requested.
