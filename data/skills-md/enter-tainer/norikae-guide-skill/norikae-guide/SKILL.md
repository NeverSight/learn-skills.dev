---
name: norikae-guide
description: Plan Japan train routes with Yahoo! 乗換案内 and fetch real route content from transit.yahoo.co.jp without MCP servers. Use when users ask for station-to-station routing in Japan, provide natural-language constraints (arrival/departure time, first/last train, cheapest/fastest/fewest transfers, transport exclusions, via stations), or provide English/Chinese station names that must be normalized to Japanese station names before querying.
---

# Norikae Guide

## Goal

Turn a travel request into Yahoo! 乗換案内 query parameters, fetch the result page, and return useful route content.

## Workflow

1. Normalize station names.
- Convert English/Chinese station names to Japanese names used in Yahoo queries.
- Keep the exact station form users expect in Japan (for example `渋谷`, `新宿`, `東京`).
- Ask one clarification question when station name is ambiguous.

2. Extract canonical fields.
- Required: `from`, `to`
- Optional: `via` (max 3), `year`, `month`, `day`, `hour`, `minute`
- Preferences: `timeType`, `ticket`, `seatPreference`, `walkSpeed`, `sortBy`
- Transport toggles: `useAirline`, `useShinkansen`, `useExpress`, `useHighwayBus`, `useLocalBus`, `useFerry`

3. Resolve time intent.
- "arrive by" / "XX点前到" -> `timeType=arrival`
- "first train" / "始発" -> `timeType=first_train`
- "last train" / "終電" -> `timeType=last_train`
- If user gives no time, default to current local time.
- If user gives relative date words (today/tomorrow/next Friday), resolve to an absolute date before querying.

4. Build URL and fetch page content.
- Preferred command:
  `python3 scripts/fetch_norikae_routes.py --from ... --to ... --show-url`
- If URL already exists:
  `python3 scripts/fetch_norikae_routes.py --url '<url>' --show-url`
- Use `--format html` only when structured HTML fragments are needed.

5. Return concise results.
- Include URL.
- Include normalized parameters.
- Include extracted route content summary (top routes, times, transfer count, fare when available).
- If constraints conflict (for example "cheapest" and "fastest"), ask which one has higher priority.

## Intent Mapping Quick Rules

- "最便宜 / cheapest" -> `sortBy=fare`
- "最快 / fastest" -> `sortBy=time`
- "换乘最少 / fewest transfers" -> `sortBy=transfer`
- "不要新干线 / no shinkansen" -> `useShinkansen=false`
- "在来线 only / local trains only" -> `useShinkansen=false`, `useExpress=false`
- "不要巴士 / no buses" -> `useHighwayBus=false`, `useLocalBus=false`
- "现金票价" -> `ticket=cash`
- "指定席 / reserved" -> `seatPreference=reserved`
- "绿车 / Green Car" -> `seatPreference=green`

## Defaults

- `timeType=departure`
- `ticket=ic`
- `seatPreference=non_reserved`
- `walkSpeed=slightly_slow`
- `sortBy=time`
- All transport toggles default to `true`

## Output Contract

Return these sections in order:

1. `Resolved request`
- Normalized station names
- Final canonical parameters

2. `Yahoo URL`
- Full query URL

3. `Route content`
- Extracted route text (or summarized top routes)
- If live fetch fails, state failure reason and still provide URL

## Resources

- Parameter and query mapping: [references/yahoo-transit-params.md](references/yahoo-transit-params.md)
- Natural language examples: [references/natural-language-examples.md](references/natural-language-examples.md)
- URL builder: `scripts/build_norikae_url.py`
- Fetch and extractor: `scripts/fetch_norikae_routes.py`

Use `fetch_norikae_routes.py` by default when users ask for actual route content.
