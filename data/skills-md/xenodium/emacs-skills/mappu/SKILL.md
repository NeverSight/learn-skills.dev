---
name: mappu
description: 'Use when the user asks about a specific place — restaurant, cafe, shop, business, landmark — or when context implies a location-based lookup ("where is X", "find Y", "X in Z", "X near A"). Calls the mappu CLI to search Apple Maps and returns local results with addresses, websites, preview images, and a map snapshot.'
tools: Bash
---

# Search places with mappu

When the user asks about a specific place or implies a location-based query, use the `mappu` CLI to search Apple Maps and present the results.

Examples of triggering contexts:

- "where can I get good ramen?"
- "is Roti King open?"
- "find sushi places in Soho"
- "what cafes are near St James's Park?"
- "any good Malaysian food around Chinatown?"

## Locating context (always set --near)

`mappu` requires a `--near` value. Determine it like this:

1. If the user mentioned a location ("in Soho", "near Charing Cross", "around Tokyo"), use that.
2. If recent conversation context establishes a location (e.g., they have been talking about restaurants in London), use that.
3. Otherwise, **ask the user** "Near where?" before running `mappu`. Do not guess silently and do not fall back to a default city.

## How to invoke

Run via the Bash tool. Always include `--preview --map` for richer output:

```sh
mappu --preview --map --near "Soho London" "roti king"
```

Flags:

- `--near "<location>"` — required, set every call.
- `--limit <N>` — max results; mappu's default is 10.
- `--radius <KM>` — search radius in kilometers.
- `--preview` — include website preview images per result (use by default).
- `--map` — include a map snapshot with numbered pins (use by default).

## Output schema

`mappu` prints JSON to stdout:

```json
{
  "map": "/path/to/map.png",
  "results": [
    {
      "name": "Roti King",
      "address": "6 Artillery Lane, London, England, E1 7LS, United Kingdom",
      "neighborhood": "City of London",
      "category": "Restaurant",
      "url": "https://rotiking.com/location/spitalfields",
      "mapsUrl": "https://maps.apple.com/?ll=51.5183405,-0.0790983&q=Roti%20King",
      "image": "/path/to/preview.png",
      "phone": "+44 20 1234 5678",
      "countryCode": "GB",
      "timeZone": "Europe/London",
      "coordinate": { "lat": 51.5183405, "lng": -0.0790983 }
    }
  ]
}
```

On failure, `mappu` prints `{"error": "..."}` and exits non-zero.

## Render as markdown

For successful responses, output in this order: top-level map (if present), then each result as image + name link + category + address. Pin numbers on the map match the order of `results[]` (1-based).

```
![map of results](path/to/map.png)

![Roti King](path/to/preview1.png)
[Roti King](https://rotiking.com/location/spitalfields)
Restaurant
6 Artillery Lane, London, England, E1 7LS, United Kingdom

![Roti King](path/to/preview2.png)
[Roti King](https://rotiking.com/location/waterloo)
Restaurant
97 Lower Marsh, London, England, SE1 7AB, United Kingdom
```

## Rules

- Always set `--near`; ask the user "Near where?" if it is not obvious from the request or recent context.
- Always include `--preview --map` unless the user explicitly asks for fast / text-only results.
- Use the result's `url` as the link target. Fall back to `mapsUrl` if `url` is missing.
- Omit the image line for results without an `image` field rather than fabricating one.
- Do not invent ratings, opening hours, prices, or any fields not present in the JSON.
- If `mappu` returns `{"error": "..."}`, surface that error to the user and stop.
- Requires the `mappu` binary on `$PATH`. If invocation fails with "command not found", tell the user to install it (e.g. copy the release binary to `/usr/local/bin/`).
