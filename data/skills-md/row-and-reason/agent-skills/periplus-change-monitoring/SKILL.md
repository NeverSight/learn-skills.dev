---
name: periplus-change-monitoring
description: Compare web observations and set up recurring source acquisition with Periplus. Use for price, policy, catalogue or announcement changes that need a stable baseline, meaningful differences and explicit monitoring coverage.
---

# Change monitoring

Define the change that matters and connect its evidence to a repeatable comparison. Distinguish a one-time historical comparison from ongoing collection and from notification delivery. Proceed within the user's existing authorization; do not add a planning gate.

## Establish comparable observations

Choose the comparison unit, relevant fields or sections, source URLs, cadence, lookback and any requested end date. Keep locale, currency, product variant and other context stable. Set a meaningful change rule: a numeric threshold, a policy clause, a new record or a changed status. Avoid treating timestamps, rotating content, navigation or unrelated page bytes as the requested change.

Inspect contrasting examples, including unchanged content, a meaningful change, a template change and a failed capture where available. Compare like-for-like observations using page identity and observation times; page-local node positions are not stable across captures. Preserve both baseline and later evidence. A missing field after a template change may be extraction failure, not removal.

Represent unavailable observations as unknown. A blocked request or incomplete listing does not prove a product disappeared or a price became zero. Count additions and removals only when the comparable source coverage supports them. Report the observation interval; do not claim the exact real-world change time from two captures.

## Build only the requested monitoring

Periplus schedules collect a fixed selection of URLs repeatedly. They do not themselves run a semantic comparison or deliver alerts. A saved query is reusable SQL, not a scheduled job. An end-to-end alerting setup also needs a separately available runner, comparison logic, persisted baseline/delivery state and an authorized notification destination.

Use an available automation service only when ongoing execution is requested and supported. Resolve any missing delivery or timing requirement before configuring the dependent part; continue independent baseline work. Verify the runner and delivery setup before claiming alerts are active. If only acquisition is configured, say exactly that and identify the missing comparison or delivery layer.

Check existing schedules to avoid duplicate work. Select retention long enough to cover the comparison window, including the baseline. Monitor acquisition failures and stale observations as health issues distinct from content changes. A fixed URL watchlist will not automatically include new pages or new SQL matches; add a discovery/refresh process when the task requires new listings. Confirm configured cadence, end time, URL coverage and current status from returned state. Cadence is a target, not an exact-time guarantee.

## Deliver evidence

For a comparison, provide old/new values or a concise section diff, each source URL, both capture IDs and observation times, and unresolved gaps. Keep raw observations separate from normalized comparison fields. For ongoing work, state which collection, comparison and notification components are verified and how to inspect or stop them.

Pinning observations retains evidence; saving SQL retains the definition; exporting a comparison result with its query, parameters and capture manifest freezes that result. Do not describe any one of these as preserving all three.

## Live product reference

Read [MCP operational contracts](https://docs.periplus.dev/mcp#agent-workflow), [schedules](https://docs.periplus.dev/schedules), [pins and schedules](https://docs.periplus.dev/pins-and-schedules) and [extraction](https://docs.periplus.dev/extraction) for live scheduling, retention and comparison mechanics. Use current schema discovery and tool contracts rather than copied signatures.
