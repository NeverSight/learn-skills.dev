---
name: tixbit
description: Find the cheapest live event tickets on TixBit in seconds — search sports and concerts, compare listings and seatmaps, and generate instant checkout links.
---

# TixBit Skill

Use the official CLI package:

```bash
npx tixbit <command>
```

Prefer `--json` for agent-readable output.

## When to use

- Find events and ticket options on TixBit.
- Compare listing prices/sections for a known event.
- Generate checkout links for a selected listing.

## When not to use

- Finalize payment (checkout is completed by the user in browser).
- Access private account/order history workflows.
- Perform non-TixBit ticketing operations.

## Core commands

```bash
# Search events
npx tixbit search "Braves" --city Atlanta --state GA --size 10 --json

# Browse local events
npx tixbit browse --city Atlanta --state GA --json

# Listings for an event
npx tixbit listings <eventId> --size 10 --sort asc --json

# Venue seatmap
npx tixbit seatmap <eventId> --json

# Checkout link for a listing
npx tixbit checkout <listingId> --quantity 2 --json

# Event URL
npx tixbit url <slugOrId>
```

## End-to-end example (search → listings → checkout)

```bash
# 1) Find Braves games in Atlanta
npx tixbit search "Braves" --city Atlanta --state GA --size 10 --json

# 2) Pick an eventId from step 1, then fetch cheapest listings
npx tixbit listings V6DJKPG --size 10 --sort asc --json

# 3) Pick a listingId from step 2, then generate checkout URL
npx tixbit checkout 7JOLYY5R --quantity 2 --json
```

## Notes

- No API key is required for standard public ticket discovery.
- `checkout` returns a link; payment is completed by the user in browser.
- Optional env vars: `TIXBIT_BASE_URL`, `TIXBIT_API_KEY`.
