---
name: gmaps
description: >-
  Google Maps via CDP — three modes, all keyless (no Google Places or Directions
  API key, no quota): (1) local business search returning structured results
  (name, rating, reviews, price, category, address, hours, coords, place ID,
  URL) — the data the metered Google Places API sells; (2) --route for real
  directions (total time + distance, current traffic) for an ordered list of
  places, in any travel mode (--mode driving|transit|walking|cycling|flights|best,
  default driving); (3) --optimize for a best-effort fastest visiting order
  (open-path TSP, fixed start) whose edges are virtualized as straight-line
  distance — N parallel place lookups plus one real directions call. Use when the
  user asks to find local businesses, get directions/time between places (by any
  mode), or plan a multi-stop route order. Requires browser-harness-js on PATH
  and a running Chromium-based browser with remote debugging.
setup: bash <skill-dir>/scripts/setup
compatibility: >-
  Requires browser-harness-js on PATH and a running Chromium browser with remote
  debugging (chrome://inspect or --remote-debugging-port). No API key. All data
  comes from the live google.com/maps page rendered through your own browser.
---

# gmaps — Google Maps via CDP (search, directions, best-effort TSP)

Free, keyless access to Google Maps through CDP — the same data the metered **Google Places** and **Directions** APIs sell, sourced directly from the rendered page. No API key, no quota, no `jq`. Three modes:

- **search** (default) — local business results for a query.
- **`--route`** — real driving directions (total time + distance, current traffic) for an *ordered* list of places.
- **`--optimize`** — best-effort fastest *visiting order* (open-path TSP, fixed start = first place).

Every call opens its own background tab and WebSocket session — safe for parallel use.

## Commands

### Search (default)

```bash
gmaps "coffee shops in Austin TX"            # up to 10 results, pretty
gmaps "sushi near Times Square" 5            # 5 results
gmaps "pharmacy open now Berlin" 20          # 20 (scrolls the feed)
gmaps --json "coffee shops in Austin TX" 5   # raw JSON
```

| Arg | Meaning |
|------|---------|
| `--json` | Emit raw JSON instead of pretty-printed text |
| `<query>` | A Google Maps search, e.g. `coffee shops in Austin TX` |
| `[count]` | Number of results (default 10, capped at 30 — the feed is scrolled to load more) |

### Directions (`--route`)

```bash
gmaps --route "Austin, TX" "Houston, TX"                       # real time + distance (driving)
gmaps --route --mode transit "London, UK" "Paris, France"     # by travel mode
gmaps --route "Austin, TX" "Houston, TX" "Dallas, TX"           # ordered multi-stop, total
gmaps --route --json --mode cycling "Austin, TX" "Houston, TX" # raw JSON
```

Real directions for the **given order** in a travel `--mode` (default `driving`). Reads the total time + distance (current traffic) and the resolved waypoint names. The first place is the origin. Up to 25 places. Per-leg times are not in the collapsed route summary (Maps shows only the total) — open `url` for the full turn-by-turn.

### Best-effort order (`--optimize`)

```bash
gmaps --optimize "Austin, TX" "Houston, TX" "Dallas, TX" "San Antonio, TX"
gmaps --optimize --mode transit "Austin, TX" "Houston, TX" "Dallas, TX"
gmaps --optimize --json "Austin, TX" "Houston, TX" "Dallas, TX"
```

Fastest *visiting order* as an **open-path TSP with a fixed start** (the first place). The first place is where you start; the rest are ordered to minimize total straight-line distance, then **one real directions call** is made for that order (in the chosen `--mode`, default `driving`) — so the reported time/distance is real even though the *order* is a straight-line estimate.

- Each place is resolved to exact lat/lng in parallel (background tabs poll the resolved place URL for its `!3d!4d` coords) — **N lookups**, not N².
- Edges are **virtualized** as straight-line (haversine) distance; each leg also reports its compass bearing. The travel `--mode` affects only the final real directions call, not the TSP ordering.
- The TSP is solved exactly (Held-Karp) for up to **12 places**.
- Total browser calls: **N + 1** (N place resolutions + 1 directions render).

### Travel modes (`--mode`)

| `--mode` | What it returns |
|------|---------|
| `driving` *(default)* | time + distance + via + tolls (the usual Maps route) |
| `transit` | time of the best bus/train/ferry/subway option (no distance/via) |
| `walking` | time + distance (durations render in hours, e.g. `62 hr`) |
| `cycling` | time + distance (may include a ferry/car-transport note) |
| `flights` | nonstop flight time only (best-effort — the flight card is outside the route panel) |
| `best` | whatever Maps' "Best" tab picks (driving for most routes; transit/flight where those are faster) |

- **No `motorcycle` or `ferry` mode.** Maps' top-level tabs are the six above; motorcycling routes via `driving`, and ferries appear as segments within `driving`/`transit` routes. (A dedicated two-wheeler tab does not appear in Maps for Vietnam or the US — only some regions/countries.)
- The page loads in `best`; for any other mode `gmaps` clicks that travel-mode tab. An unavailable mode (e.g. `cycling` for an island route) reports a clean error.
- Applies to both `--route` and `--optimize`.

### Parallel use

Each call opens its own background tab — safe to run concurrently:

```bash
gmaps "coffee Austin" 5 &  gmaps "coffee Seattle" 5 &  wait
gmaps --route "Austin, TX" "Houston, TX" &  gmaps --route "Dallas, TX" "San Antonio, TX" &  wait
```

## Result shape

### Search — pretty (default)
```
coffee shops in Austin TX  ·  5 results

1. Jo's Coffee – South Congress   ★4.4 (1972)   $1–10   Coffee shop
   1300 S Congress Ave   ·   Open · Closes 7 PM
   30.2510458, -97.7493717   ·   ChIJ1S_Bov20RIYRe7MiR8
   https://www.google.com/maps/place/Jo%27s+Coffee...
```

### Search — `--json`
```json
{
  "query": "coffee shops in Austin TX",
  "count": 5,
  "results": [
    {
      "name": "Jo's Coffee – South Congress",
      "rating": 4.4,
      "review_count": 1972,
      "price": "$1–10",
      "category": "Coffee shop",
      "address": "1300 S Congress Ave",
      "hours": "Open · Closes 7 PM",
      "lat": 30.2510458,
      "lng": -97.7493717,
      "place_id": "ChIJ1S_Bov20RIYRe7MiR8",
      "url": "https://www.google.com/maps/place/Jo%27s+Coffee…"
    }
  ]
}
```

Each result carries: `name, rating, review_count, price, category, address, hours, lat, lng, place_id, url`. Missing fields are `null` (or `-` in pretty mode) — e.g. a place with no price tier or no street address.

### Route — pretty
```
Route (driving): Austin, TX  →  Houston, TX

  2 hr 31 min   165 miles   via State Hwy 71 E and I-10 E
  Fastest route, the usual traffic  ·  tolls

  1. Austin, Texas, USA
  2. Houston, Texas, USA

  https://www.google.com/maps/dir/Austin,+TX/Houston,+TX/
```
The `(driving)` is the `--mode` (default). `distance` (and `via`) can be null on a trivially short route, and for `transit`/`flights` (no distance). `tolls` appears only when the route has tolls.

### Route — `--json`
```json
{
  "mode": "route",
  "travel_mode": "driving",
  "places": ["Austin, TX", "Houston, TX"],
  "route": {
    "duration": "2 hr 31 min",
    "distance": "165 miles",
    "via": "via State Hwy 71 E and I-10 E",
    "label": "Fastest route, the usual traffic",
    "tolls": true,
    "waypoints": ["Austin, Texas, USA", "Houston, Texas, USA"],
    "url": "https://www.google.com/maps/dir/Austin,+TX/Houston,+TX/"
  }
}
```

### Optimize — pretty
```
Optimized route  ·  best-effort (straight-line TSP)  ·  driving  ·  fixed start: Austin, TX, USA

  1. Austin, TX, USA  (30.267153, -97.7430608)   start
  2. San Antonio, TX, USA  (29.4251905, -98.4945922)   ← 118.4 km SW (218°)
  3. Houston, TX, USA  (29.7600771, -95.3701108)   ← 304.4 km E (82°)
  4. Dallas, TX, USA  (32.7766642, -96.7969879)   ← 361.8 km N (338°)

  Straight-line total: 784.6 km

Real driving for this order:
  7 hr 50 min   516 miles   via I-35 S
  Fastest route now due to traffic conditions  ·  tolls
  Austin, TX, USA  →  San Antonio, TX, USA  →  Houston, TX, USA  →  Dallas, TX, USA

  https://www.google.com/maps/dir/Austin,+TX/San+Antonio,+TX/Houston,+TX/Dallas,+TX/

Note: order is a best-effort estimate from straight-line (haversine) distances;
the driving time above is the real route for that order.
```

### Optimize — `--json`
```json
{
  "mode": "optimize",
  "travel_mode": "driving",
  "places": [{ "query": "Austin, TX", "name": "Austin, TX, USA", "lat": 30.267153, "lng": -97.7430608, "url": "…" }, …],
  "order": ["Austin, TX, USA", "San Antonio, TX, USA", "Houston, TX, USA", "Dallas, TX, USA"],
  "order_indices": [0, 3, 1, 2],
  "legs": [{ "from": "Austin, TX, USA", "to": "San Antonio, TX, USA", "km": 118.4, "bearing": 218, "dir": "SW" }, …],
  "straight_line_total_km": 784.6,
  "route": { "duration": "7 hr 50 min", "distance": "516 miles", "via": "via I-35 S", "label": "…", "tolls": true, "waypoints": […], "url": "…" },
  "note": "Order is a best-effort estimate from straight-line (haversine) distances; the driving time/distance is the real route for that order."
}
```

## How it works

### Search
| Step | What happens |
|------|---------------|
| 1 | `session.connect()` (once) — shared WebSocket to the browser |
| 2 | `Target.createTarget({ background: true })` + `attachToTarget` — isolated background tab + per-call `sessionId` |
| 3 | `Page.navigate` to `https://www.google.com/maps/search/<query>` (URI-encoded; spaces as `+`) |
| 4 | **Poll for `a[href*='/maps/place/']` count > 0** — the real readiness signal. Chrome never fires `networkIdle` for Maps (continuous XHR polling keeps the 500ms quiet window from ever opening), so waiting on lifecycle events times out. Polling the feed is both faster and reliable. |
| 5 | **Scroll the feed** to load up to `count` results. The feed renders ~7 cards up front; more stream in as the feed is scrolled to its bottom. Stops at `count`, after two consecutive no-growth scrolls (end of results), or after a 25-scroll cap. |
| 6 | **One `Runtime.evaluate`** parses every result card and returns a JSON array. |
| 7 | Fire-and-forget `closeTab` in `finally` — cleanup without blocking the response. |

### Directions (`--route` / `--optimize`)
| Step | What happens |
|------|---------------|
| 1 | `Page.navigate` to `https://www.google.com/maps/dir/<p0>/<p1>/…/` (path form with `+` for spaces). The `?query=` form does not render. The page loads in Maps' "Best" mode. |
| 2 | **Poll the Directions panel for a route duration.** Like the feed, `networkIdle` never fires. Route-list durations end in `min`/`hr`; the travel-mode tabs use a compact form (`2h 30m`, `16 hr`) with no `min` token, so polling `/\d+\s*min\b/` in the `[aria-label="Directions"]` panel waits for the real route and ignores the mode tabs. A distance leaf (`miles`/`km`) is also accepted so an exact-hour route (`2 hr`, no min) still triggers. The map scale bar `50 km` is outside the panel. |
| 3 | **Select the travel `--mode`** (unless `best`). The mode tabs are the `button[role=radio]` that contain an `[aria-label]` icon, in a stable order `[Best, Driving, Transit, Walking, Cycling, Flights]` (the map-type Default/Satellite radios have no icon aria-label, so they're excluded). Tab aria-labels are *localized* ("Driving" → "Lái xe"), so the tab is selected by **index**, not label; the tabs are waited-for (they can lag the initial paint), and an unavailable tab is detected (DOM `disabled` property, with a fallback: no route after the click ⇒ "not available"). After a real click the panel **clears (duration → null) then repopulates** with the new mode's duration, so the re-render is waited out by polling null → non-null — no race with the previous mode's duration. |
| 4 | **One `Runtime.evaluate`** extracts the primary route: the first full-format duration leaf **not inside a travel-mode `BUTTON[role=radio]`** (those hold the compact per-mode best-times); the distance leaf in its nearest ancestor; and the unique `via …` / `Fastest route …` / `This route has tolls.` leaves (transit alternates like RedCoach/FlixBus have none of these, so they don't pollute). Resolved waypoint names come from `input[aria-label]` (`Starting point …` / `Destination …`). For `flights` the duration is read body-wide (the flight card is outside the Directions panel) and distance/via/tolls are null. |
| 5 | Fire-and-forget `closeTab` in `finally`. |

### Optimize extras
| Step | What happens |
|------|---------------|
| A | **Resolve each place** in parallel background tabs: a place-name search does *not* render a feed — it resolves to a single place page whose URL updates (in ~3-7 s) to `/maps/place/<name>/@<view>/data=…!8m2!3d<lat>!4d<lng>…`. Each tab polls `location.href` for the `!3d!4d` token (the place's exact coords — the `@lat,lng` is only the viewport). The place name is read from the `/maps/place/<name>/` path segment. |
| B | Build the **haversine** distance matrix and solve the **open-path TSP with fixed start = place[0]** (exact Held-Karp, ≤12 places). |
| C | Compute per-leg straight-line km + compass bearing. |
| D | **One real `--route` call** (in the chosen `--mode`, default driving) for the chosen order → the reported time/distance is real; only the *order* is a straight-line estimate. |

Per call: search ~2-3 s (feed render + scrolls); route ~2-3 s; optimize ~5-9 s (N parallel place resolutions + 1 directions render). Background tabs keep it unobtrusive (unlike `ytdl`, Maps needs no playback/poToken).

## Why a real browser for Maps

- **The Google Places and Directions APIs are metered and gated** — a key, a billing account, and per-call cost. The Maps web page renders the same data for free; driving your own browser reads it with no key and no quota. The one thing the paid Directions API gives that the free page genuinely can't is `optimizeWaypoints` (TSP for ≤9 stops) — `--optimize` replaces that with a best-effort straight-line TSP.
- **A real browser renders the feed and the route panel.** Maps is a heavy SPA: results stream into `div[role=feed]` as it scrolls, and the directions panel renders route durations with class names that are obfuscated and rotate. A single `Runtime.evaluate` extracts every card / the primary route in one CDP call — no HTML fetching, no proxy, no Cloudflare wall (the page is rendered as you, in your own browser).
- **Per-query use, not bulk harvest.** This is the agent-call shape: one query (or one route of ≤25 / one TSP of ≤12 places), returned as structured JSON or text. It is *not* a bulk scraper (that needs proxy rotation + rate management, which a real-browser-per-call approach doesn't scale to).

## Traps

### Search
- **`networkIdle` never fires for Maps.** Continuous XHR polling holds the network busy, so the lifecycle-event wait gsearch/findata use would time out every time. `gmaps` polls `a[href*='/maps/place/']` count instead — the actual readiness signal.
- **No class-name selectors.** Google's class names are obfuscated (`.Nv2PK`, `.bfdHYd`, `.MW4etd`, …) and rotate across releases. The parser relies only on **stable signals**: the result link's `aria-label` (name), the card's leaf-text DOM order (rating/reviews/price/category/address/hours), and the `href` (`!3d<lat>!4d<lng>` for coords, `!19sChIJ…` / `!1s0x..:0x..` for the place id). If Maps changes the card text order, the address/hours heuristics are the first things to revisit.
- **`?query=` URL form does not render the feed** (returns a redirect shell with no results) — only the path form `/maps/search/<query>` does. Spaces are sent as `+`.
- **Address is a heuristic.** It's the first leaf starting with a street number (`^\d{1,5}[-A-Za-z]*\s`). A place with no street address (an area/region result, or a named building) yields `address: null` rather than a guess.
- **Hours is a heuristic.** It's the `Open` / `Closed` / `Open 24 hours` / `Temporarily closed` leaf, plus the following `· Closes/Opens …` leaf when present. `Open 24 hours` rendered as two leaves (`Open` + `24 hours`) would be read as just `Open`.
- **Phone, website, and full weekly hours are NOT in the feed card** — they live on the place-detail page and need a per-place navigation to read. Not implemented (would be a `--details` mode); for now use `url` to open a place.
- **Sponsored results** may appear (Maps sometimes shows one ad, which is also a `/maps/place/` link). They are not filtered out — check the data if it matters.
- **Consent / cookie wall** (rare in an already-warmed browser) returns zero results. If results come back empty, open the search URL in the browser once to clear it.

### Directions
- **Per-leg times are not in the collapsed route summary.** Maps shows only the total for an ordered multi-stop route. Per-leg durations live behind the "Details" expansion (not implemented); use `url` for turn-by-turn.
- **`distance` can be null** on a trivially short route (Maps may render no distance leaf).
- **The primary route is "first full-format duration not inside a travel-mode radio."** The mode tabs (`BUTTON[role=radio]`) carry compact best-times (`2h 30m`) that must be excluded; the route list uses the full form (`2 hr 31 min`). Transit alternates (RedCoach/FlixBus) appear in the same panel but have no `via`/`Fastest route`/distance leaves, so they don't contaminate the primary extraction.
- **Times are current-traffic ("now").** The page gives *now*, not a predictive future departure (the paid API's `departure_time`/`traffic_model` is the one thing the page doesn't give). The label varies: "Fastest route, the usual traffic" vs "Fastest route now due to traffic conditions" — both are matched by `^Fastest route`.
- **Place-name searches don't render a feed** — that's why `--optimize` resolves places by polling the place-page URL for `!3d!4d`, not by parsing feed cards. A background tab takes ~3-7 s to update the URL; `resolvePlace` polls up to 20 s.

### Travel modes (`--mode`)
- **`best` is Maps' default and may not be driving.** For routes where transit/flight is faster (e.g. London→Paris, where Best = the Eurostar), `best` returns the transit time. Pass `--mode driving` to force driving. The skill's *default* is `driving` (not `best`) for this reason.
- **Mode tabs are selected by INDEX, not aria-label** — the labels are localized ("Driving" → "Lái xe" in vi). The order `[Best, Driving, Transit, Walking, Cycling, Flights]` has been stable across locales, but if Maps reorders or drops a tab the index mapping breaks.
- **Unavailable modes are detected two ways** — the tab's DOM `disabled` property (which can lag its render), with a fallback: if clicking produces no route (panel clears but never repopulates), the mode is reported as "not available for this route".
- **`flights` is best-effort.** The flight card renders *outside* the Directions panel, so the nonstop flight time is read body-wide; there is no distance/via/tolls. Connecting flights and booking details are not parsed.
- **No `motorcycle` or `ferry` mode.** Maps exposes only the six tabs above; motorcycling routes via `driving`, ferries appear as segments within `driving`/`transit` routes. (A two-wheeler tab does not appear in Maps for Vietnam or the US.)
- **Walking/cycling durations render in hours** in the route list (e.g. `62 hr`), not the "days" shown on the mode tab — both are matched.

### Optimize
- **The order is a straight-line estimate, not the true driving-optimal order.** Straight-line (haversine) distance is the "virtualized" edge cost; road-network detours can reorder the true optimum. The reported *driving time/distance* is real (one directions call for the chosen order) — only the *order* is best-effort.
- **Fixed start, open path.** The first place is the start and is fixed; the path visits every place once and ends anywhere (no return). Not a round trip.
- **≤12 places, exact.** Held-Karp is exact but exponential; above 12 the command errors rather than guess. N place resolutions run in parallel (N background tabs) + 1 directions call = N+1 browser calls.

### General
- **No `jq` dependency** — parsing, TSP, and pretty-printing are done in-page / in JS.
- **Inputs reach the heredoc by placeholder substitution** (node `JSON.stringify` + function-replacements), immune to `&` / `$` / `\` in place names (e.g. `AT&T Stadium`, `Café du Monde`) — the same mechanism the search query uses.
