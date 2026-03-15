---
name: tripgo-api
description: Comprehensive interface for the SkedGo TripGo API, covering routing, public transport, trips, and location services. Use for multimodal journey planning, public transport data, and geocoding.
---

# SkedGo TripGo API Skill

This skill provides a complete interface to the SkedGo TripGo API, enabling agents to perform multimodal routing, retrieve public transport information, manage trips, and perform geocoding.

## Overview

The TripGo API is a platform for multimodal transport, allowing users to plan trips combining public transport, car, bike, taxi, rideshare, and more. This skill encapsulates the API endpoints into modular scripts and documentation references.


## Configuration

To use this skill, you must set the following environment variables:

- `TRIPGO_API_KEY`: Your TripGo API key (header: `X-TripGo-Key`). Get it here: https://skedgo.com/tripgo-api/
- `TRIPGO_BASE_URL`: (Optional) Base URL for the API. Defaults to `https://api.tripgo.com/v1`.
- `TRIPGO_WEBHOOK_ALLOWLIST`: (Optional, recommended) Comma-separated allowlist of webhook domains (e.g. `example.com,webhooks.example.org`).
- `TRIPGO_ALLOW_UNSAFE_WEBHOOK`: (Optional, default `false`) Set to `true` to bypass webhook allowlist checks for trusted/manual debugging only.


## Runtime Requirements

Install these binaries before running scripts:

- `curl` (required): API requests
- `jq` (required): JSON validation, safe JSON construction, and URL encoding
- `python3` (optional): pretty-printing for a few scripts

## Security Notes

- Scripts that accept JSON parameters validate those values with `jq` before sending requests.
- Scripts that send query parameters URL-encode user-provided values.
- Webhook hook registration enforces `https://` and domain allowlisting by default (`TRIPGO_WEBHOOK_ALLOWLIST`) to reduce exfiltration risk.
- API key usage is expected: requests send `X-TripGo-Key` to the configured TripGo base URL.

## Directory Structure

- `SKILL.md`: This file.
- `references/`: Detailed documentation for each API section.
- `scripts/`: Executable Bash scripts for each API endpoint.

### References (`references/`)
Documentation is organized by API section. Load these files to understand specific endpoints, parameters, and response structures.

- `references/configuration.md`: Regions, TSPs, and POIs.
- `references/routing.md`: Journey planning and routing (A-to-B, multi-point).
- `references/trips.md`: Trip management (save, update, real-time hooks).
- `references/ttp.md`: Travelling Tourist Problem (Deprecated).
- `references/geocode.md`: Search and autocompletion.
- `references/locations.md`: Location services and POIs.
- `references/public-transport.md`: Public transport operators, routes, services, and real-time data.

### Scripts (`scripts/`)
Each script corresponds to a specific API endpoint. They are designed to be executed directly or used as templates.

**Naming Convention:** `scripts/<section>-<function-name>.sh`

#### Configuration
- `scripts/configuration-available-regions.sh`
- `scripts/configuration-tsps-per-region.sh`
- `scripts/configuration-pois-for-a-transport-mode.sh`

#### Routing
- `scripts/routing-a-to-b-trips.sh`
- `scripts/routing-a-to-b-to-c-trip.sh`
- `scripts/routing-all-day-routing-between-events.sh`
- `scripts/routing-all-day-routing-between-events-deprecated.sh` (Deprecated)

#### Trips
- `scripts/trips-retrieve-previously-computed-trip.sh`
- `scripts/trips-save-trip-for-later-use.sh`
- `scripts/trips-update-trip-with-real-time-data.sh`
- `scripts/trips-gets-hooked-urls.sh`
- `scripts/trips-hooks-a-trip-to-real-time-updates.sh`
- `scripts/trips-removes-a-hooks-from-a-trip.sh`
- `scripts/trips-mark-trip-as-planned-by-a-user.sh`

#### TTP (Deprecated)
- `scripts/ttp-create-travelling-tourist-problem-deprecated.sh`
- `scripts/ttp-delete-travelling-tourist-problem-deprecated.sh`
- `scripts/ttp-delete-travelling-tourist-problem-solution-deprecated.sh`

#### Geocode
- `scripts/geocode-search-and-autocompletion.sh`

#### Locations
- `scripts/locations-pois-for-a-circular-region.sh`
- `scripts/locations-pois-for-map-region-using-cell-ids.sh`
- `scripts/locations-additional-details-for-a-coordinate.sh`

#### Public Transport
- `scripts/public-transport-operators-for-a-region-or-group-of-regions.sh`
- `scripts/public-transport-routes-for-a-region-or-operator.sh`
- `scripts/public-transport-details-of-a-route.sh`
- `scripts/public-transport-services-for-a-route.sh`
- `scripts/public-transport-departure-timetable-for-a-stop.sh`
- `scripts/public-transport-real-time-information-for-a-service.sh`
- `scripts/public-transport-get-details-of-a-service.sh`
- `scripts/public-transport-get-real-time-alerts.sh`

## Usage Constraints

- **Do NOT invent parameters.** All scripts use parameters explicitly documented in `references/`.
- **Deprecated Endpoints:** Some scripts are marked as deprecated (e.g., TTP section). Use with caution or avoid if possible.
- **Verification:** If a parameter or field is marked as "To be confirmed" in the references, verify with a live API call before relying on it in production.
- **Environment:** Ensure `TRIPGO_API_KEY` is set in the environment before running any script.

## Example

**Searching for a location:**

```bash
export TRIPGO_API_KEY="your_key_here"
./scripts/geocode-search-and-autocompletion.sh --query "Sydney Opera House" --near "(-33.8688,151.2093)"
```

**Planning a trip:**

```bash
./scripts/routing-a-to-b-trips.sh --from "(lat,lng)" --to "(lat,lng)" --region "AU_NSW_Sydney"
```
