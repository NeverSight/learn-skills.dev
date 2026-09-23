---
name: raleigh
description: >-
  Query, search, and download public datasets and civic information for the City
  of Raleigh. Use for live ArcGIS Hub catalog discovery, ArcGIS FeatureServer
  and MapServer queries, ImageServer imagery exports, official Raleigh
  geocoding, GoRaleigh transit feeds, guest-public development records, public
  RaleighNC.gov content, eSCRIBE public meetings, Raleigh fire reports and
  inspections, and the Raleigh-Wake ECC active incident feed. Do not use for
  private data, authenticated operations, payments, submissions, bulk crawling,
  or non-public portals.
license: MIT
metadata:
  source: https://data.raleighnc.gov
  author: Jasper
  datasets: live
---

# Raleigh Civic Data

A read-only CLI for the City of Raleigh's public civic data and services. It discovers datasets from the live ArcGIS Hub catalog, queries ArcGIS layers, exports imagery, geocodes and reverse-geocodes addresses, reads GoRaleigh GTFS and GTFS-Realtime feeds, searches the guest-public Permit and Development Portal, lists public RaleighNC.gov content, and extracts public eSCRIBE meetings.

All operations are read-only and use fixed endpoint contracts. HTTPS is required except for explicitly acknowledged RFD report lookups, whose upstream site supports only plain HTTP. No API key, sign-in, payment, or submission flow is implemented.

## Quick Start

```bash
# List live datasets
scripts/raleigh catalog

# Search the catalog
scripts/raleigh search "food inspection"

# Show a dataset's live metadata
scripts/raleigh info "Raleigh Dog Parks"

# Query records
scripts/raleigh query "Food Inspections" --where "SCORE < 70" --limit 20

# Export to CSV
scripts/raleigh download "Raleigh Dog Parks" -f csv -o dog_parks.csv
```

## Commands

### Dataset discovery

| Command | Purpose | Example |
|---------|---------|---------|
| `catalog` | List live Hub datasets | `scripts/raleigh catalog --json` |
| `search` | Search catalog metadata | `scripts/raleigh search "building permit" --limit 10` |
| `info` | Show a dataset by title or ID | `scripts/raleigh info "Raleigh Dog Parks" --json` |
| `query` | Query records with filters | `scripts/raleigh query "Food Inspections" --where "SCORE<70" --limit 20` |
| `download` | Export to CSV, GeoJSON, or JSON | `scripts/raleigh download "Parcels" -f geojson -o parcels.geojson` |
| `categories` | List categories from the catalog | `scripts/raleigh categories` |
| `catalog-check` | Validate cached endpoints | `scripts/raleigh catalog-check --sample 10` |

### Imagery

| Command | Purpose | Example |
|---------|---------|---------|
| `imagery catalog` | List ImageServer services | `scripts/raleigh imagery catalog --json` |
| `imagery info` | Show service metadata | `scripts/raleigh imagery info Orthos2025` |
| `imagery export` | Export bounded image | `scripts/raleigh imagery export Orthos2025 --bbox=-78.7,35.7,-78.6,35.8 --size 400,400 -o ortho.jpg` |
| `imagery identify` | Identify pixel value at point | `scripts/raleigh imagery identify Orthos2025 --point=-78.65,35.75` |
| `imagery statistics` | Compute extent statistics | `scripts/raleigh imagery statistics Orthos2025 --bbox=-78.7,35.7,-78.6,35.8` |

`imagery catalog` lists only publicly readable services. Folders whose
listing requires a token (currently `Imagery` and `Utilities`) are skipped
and reported as restricted rather than failing the command; the daily live
canary tracks them the same way.

### Geocoding

| Command | Purpose | Example |
|---------|---------|---------|
| `geocode` | Forward geocode | `scripts/raleigh geocode "222 W Hargett St"` |
| `reverse-geocode` | Reverse geocode | `scripts/raleigh reverse-geocode --lat 35.78 --lon -78.64` |
| `suggest` | Address autocomplete | `scripts/raleigh suggest "222 W Har"` |
| `geocode-batch` | Batch geocode CSV | `scripts/raleigh geocode-batch addresses.csv --address-field address -o out.csv` |

Batch output preserves every original CSV column and adds `input_id`,
`match_address`, `score`, `lat`, `lon`, and `status`. If an input already uses
one of those names, the added result column receives a `geocode_` prefix.

### Transit

| Command | Purpose | Example |
|---------|---------|---------|
| `transit routes` | List routes | `scripts/raleigh transit routes --json` |
| `transit stops` | List stops | `scripts/raleigh transit stops --near 35.78,-78.64 --limit 10` |
| `transit schedule` | Schedule for a route | `scripts/raleigh transit schedule --route 1 --date 20260723` |
| `transit arrivals` | Arrivals for a stop | `scripts/raleigh transit arrivals --stop S1` |
| `transit vehicles` | Live vehicle positions | `scripts/raleigh transit vehicles --json` |
| `transit alerts` | Service alerts | `scripts/raleigh transit alerts` |
| `transit trip-updates` | Live trip updates | `scripts/raleigh transit trip-updates --json` |
| `transit download-gtfs` | Save static feed | `scripts/raleigh transit download-gtfs` |

### Development records

| Command | Purpose | Example |
|---------|---------|---------|
| `development search` | Search public records | `scripts/raleigh development search permits --query "2024-001"` |
| `development search project` | Search public projects | `scripts/raleigh development search project --query "downtown"` |
| `development permit` | Permit details | `scripts/raleigh development permit BP-2024-001` |
| `development inspections` | Inspections for a record | `scripts/raleigh development inspections --record BP-2024-001` |
| `development code-cases` | Code cases | `scripts/raleigh development code-cases --query "nuisance"` |
| `development licenses` | Licenses | `scripts/raleigh development licenses --query "coffee"` |

### Civic content

| Command | Purpose | Example |
|---------|---------|---------|
| `news` | RaleighNC.gov news | `scripts/raleigh news --limit 10` |
| `events` | Events | `scripts/raleigh events --from 2026-07-01 --to 2026-07-31` |
| `projects` | Projects | `scripts/raleigh projects --search "park"` |
| `places` | Places | `scripts/raleigh places --search "library"` |
| `services` | Services | `scripts/raleigh services --search "trash"` |
| `directory` | Directory entries | `scripts/raleigh directory --search "parks"` |
| `alerts` | Public alerts | `scripts/raleigh alerts` |
| `rss` | RSS feed | `scripts/raleigh rss --limit 10` |

### Police incidents

| Command | Purpose | Example |
|---------|---------|---------|
| `police incidents` | Query NIBRS incidents (June 2014–present) | `scripts/raleigh police incidents --since 7d --category burglary` |
| `police recent` | Query CrimeMapper past-90-day feed | `scripts/raleigh police recent --days 30 --district Downtown` |
| `police previous-day` | Query previous-day incidents | `scripts/raleigh police previous-day --json` |
| `police history` | Query historical incidents (SRS or NIBRS) | `scripts/raleigh police history --reporting-system srs --since 30d` |
| `police stats` | Official published statistics availability and document links | `scripts/raleigh police stats --year 2025` |
| `police reports` | Official annual and quarterly report links | `scripts/raleigh police reports --year 2025 --quarter 4` |

### Fire incidents

| Command | Purpose | Example |
|---------|---------|---------|
| `fire incidents` | Query RFD incidents (full history 2007–present or past month) | `scripts/raleigh fire incidents --since 30d --group Fire` |
| `fire response-times` | Compute labeled response durations | `scripts/raleigh fire response-times --since 1y --group Fire` |
| `fire protection` | Wake County MAR fire-protection proximity lookup | `scripts/raleigh fire protection --address "222 W Hargett St"` |
| `fire stats` | Official published incident totals and sprinkler-save statistics | `scripts/raleigh fire stats --year 2026` |
| `fire reports` | Published aggregate-report links or exact incident-report lookup | `scripts/raleigh fire reports --year 2025 --quarter 1` |
| `fire reports --date` | Exact ArcGIS incident-report summary, with optional guarded RFD fallback | `scripts/raleigh fire reports --date 2026-07-24` |
| `fire inspections` | Business/address inspection lookup through fragile RFD HTML | `scripts/raleigh fire inspections --business "Example" --acknowledge-insecure-rfd` |

### Active incidents (RWECC)

| Command | Purpose | Example |
|---------|---------|---------|
| `incidents active` | Currently active public incidents from RWECC | `scripts/raleigh incidents active --agency raleigh-fire` |
| `incidents active --json` | JSON output with source metadata | `scripts/raleigh incidents active --agency raleigh-police --json` |

### Public meetings

| Command | Purpose | Example |
|---------|---------|---------|
| `meetings upcoming` | Upcoming meetings | `scripts/raleigh meetings upcoming --json` |
| `meetings list` | Filter by body/year | `scripts/raleigh meetings list --body "City Council" --year 2026` |
| `meetings search` | Search meetings | `scripts/raleigh meetings search "budget"` |
| `meetings show` | Meeting details | `scripts/raleigh meetings show 37126a80-175a-4b38-974d-a7006bc7db85` |
| `meetings download-agenda` | Download agenda | `scripts/raleigh meetings download-agenda 37126a80-175a-4b38-974d-a7006bc7db85 -o agenda.pdf` |
| `meetings download-minutes` | Download minutes | `scripts/raleigh meetings download-minutes 37126a80-175a-4b38-974d-a7006bc7db85 -o minutes.pdf` |

## Output Flags

| Flag | Effect |
|------|--------|
| `--json` | JSON output |
| `--refresh` | Bypass catalog cache |
| `--cache-dir DIR` | Use a custom cache directory |
| `--timeout SECONDS` | HTTP timeout (default 30) |

## References

| Reference | Load when | File |
|-----------|-----------|------|
| API contracts and endpoints | Building custom queries | `references/api-reference.md` |
| Imagery and ImageServer details | Working with aerial photography or raster services | `references/imagery-reference.md` |
| GTFS and GTFS-Realtime | Transit commands | `references/transit-reference.md` |
| Guest development portal | Permit and development records | `references/development-reference.md` |
| Civic content | JSON:API and RSS | `references/civic-content-reference.md` |
| Public meetings | eSCRIBE extraction | `references/meetings-reference.md` |
| Police incidents | RPD data sources, field schemas, and privacy caveats | `references/police-reference.md` |
| Fire incidents | RFD data sources, 2026 schema transition, durations, and privacy caveats | `references/fire-reference.md` |
| Fire reports and inspections | ArcGIS-first contract, RFD forms, insecure transport, and exclusions | `references/fire-reports-reference.md` |
| Published police and fire statistics | Official page contract, report indexes, structured totals, and privacy boundary | `references/public-safety-statistics-reference.md` |
| Active incidents (RWECC) | Undocumented feed contract, schema guard, and disable switch | `references/incidents-reference.md` |

## Pitfalls

- **Live catalog**: The catalog is discovered from the Hub at runtime. Cache it with `--cache-dir` for repeated use.
- **ImageServer**: Never append `/0` to an ImageServer root. Use the dedicated `imagery` commands.
- **MapServer tables**: Some layers are tabular (`type: Table`). The CLI automatically omits geometry for non-spatial layers.
- **WHERE clauses**: Strings must be single-quoted: `NAME='Millbrook-Exchange'`.
- **ArcGIS dates**: Returned as Unix milliseconds; divide by 1000 for standard timestamps.
- **Guest development portal**: Uses an undocumented public application API. The adapter is isolated and may change if the upstream UI changes; set `RALEIGH_DISABLE_DEVELOPMENT=1` to disable it independently.
- **Civic relationships**: Public content commands accept `--relationship FIELD=ID`; text, date, and relationship matching is client-side after bounded pagination.
- **eSCRIBE**: HTML-based extraction with a weaker compatibility contract than structured APIs.
- **Police incidents**: Locations are block-level and may be randomized or redacted. Empty coordinates are suppressed, not presented as points. This data does not include arrests, convictions, or dispositions. The CrimeMapper 90-day feed is not in the curated Hub catalog and is resolved by item ID.
- **Fire incidents**: RFD deprecated `incident_type`/`incident_type_description` for records after 2026-01-01, replaced by `incident_group_name`, `incident_subgroup_code`, and `incident_type_name`. The `fire` commands normalize both eras into stable `_` keys without fabricating cross-era mappings, and preserve raw fields in JSON. Incident types 300–399 and 661 are excluded by RFD for EMS/privacy. The full-history `station` field is unpopulated for most records after early 2021; the past-month feed provides `station_name`.
- **Fire reports and inspections**: Report summaries use the structured ArcGIS past-month layer first. RFD fallback, narratives, and inspection searches cross unencrypted HTTP and require `--acknowledge-insecure-rfd` on every invocation. Date fallback also requires `--allow-rfd-fallback` and only runs after ArcGIS returns no records. Empty searches, redirects, unexpected markup, and schema drift fail closed. Invoice links are neither followed nor exposed.
- **Published public-safety statistics**: `police stats/reports` and year-based `fire stats/reports` read the official RaleighNC.gov publication indexes at runtime. Inline values are labeled `official_published_statistics`; PDF links are returned without extracting their contents. These outputs are not recomputed from incident rows. RFD medical totals remain aggregate-only and must never be joined to or used to infer incident records excluded for privacy.
- **Fire protection**: The Wake County MAR Fire Protection table is a non-spatial table keyed by CSAID. Address input is composed through the Raleigh locator and the Wake County MAR Addresses layer; if the address cannot be resolved to a unique CSAID, supply `--csaid` directly. Distances are source-provided road-network values; the source does not advertise units. This data does not expose hydrant locations, only nearest-hydrant distance. It must not be used for emergency response.
- **Active incidents (RWECC)**: Uses an undocumented public application endpoint (`incidents.rwecc.com/getdata`). The adapter is isolated and may break if the upstream contract changes; set `RALEIGH_DISABLE_INCIDENTS=1` to disable it independently. This is a filtered active feed, NOT all 911 calls and NOT authoritative emergency status. An empty response does not prove zero incidents. Cache lifetime is 90 seconds.
- **URL allowlist**: Only fixed public hosts are dereferenced; arbitrary URLs are rejected.
- **Transit realtime**: Requires `google.protobuf>=6.31.1,<7`. The vendored GTFS-Realtime binding was generated with protoc 31.1 and does not replace the runtime.

## Safety Boundaries

- Read-only operations only. No auth, write, payment, submission, or private-data endpoints.
- All remote hosts and paths are fixed. The general client remains HTTPS-only; the isolated RFD adapter permits only four documented plain-HTTP read contracts after explicit acknowledgement.
- Cached data is refreshed with `--refresh` or when the cache expires.
- Report stale or unavailable endpoints via `catalog-check`.

## When not to use

- Do not use this skill for private, authenticated, or non-public city data. It cannot sign in, pay fees, submit forms, or access internal systems.
- Do not use it for non-Raleigh jurisdictions. The host allowlist is fixed to City of Raleigh and GoRaleigh endpoints.
- Do not rely on it for write operations, real-time emergency dispatch, or legally authoritative records. Data is read-only and may be cached.
- Do not use it when the task requires GTFS-Realtime and a compatible `protobuf` runtime is unavailable. Install `protobuf>=6.31.1,<7` first or stick to static GTFS commands.
- For general web scraping, research outside Raleigh civic data, or interactive browser tasks, use a more appropriate skill instead.
