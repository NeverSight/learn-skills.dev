---
name: trakt
description: >-
  Discover and compare Trakt.tv trending, popular, and anticipated movies and shows, and
  manage user-scoped history and watchlists from the terminal. Do not use this skill for
  general TMDb catalog metadata, credits, images, or provider lookups; use `tmdb` for
  those tasks.
license: MIT
compatibility: Requires TRAKT_CLIENT_ID, Python 3.8+, and requests. Public discovery
  reads use an application Client ID; OAuth is only needed for user-scoped operations.
metadata:
  tags: trakt, media-discovery, movies, tv-shows, trending, api-client
  sources: https://docs.trakt.tv/docs/required-headers
---

# Trakt media discovery

Use this skill to inspect what is being watched, what is broadly popular, and what is anticipated. It is a read-only discovery surface, not a catalog metadata service.

## Setup and authentication

Register an app at [Trakt OAuth applications](https://trakt.tv/oauth/applications) and export its Client ID:

```sh
export TRAKT_CLIENT_ID="YOUR_TRAKT_CLIENT_ID"
```

Every request must send `trakt-api-key: <client id>` together with the mandatory companion header `trakt-api-version: 2`, plus JSON content type and a descriptive User-Agent. Public discovery endpoints use the key header, not `Authorization: Bearer`. OAuth bearer tokens are for endpoints marked OAuth-required or for user-scoped lists, history, collection, watchlist, and mutations; a bearer token does not replace the key/version pair.

## Essential commands

All six discovery commands accept `--page N` alongside `--limit N`; both default to 1 and 10 respectively and are forwarded to the API's query string.

### Trending: watched in the last 24 hours

```sh
trakt movie trending --limit 20
trakt tv trending --limit 20 --page 2 --json
```

Trending responses wrap each media object in `movie` or `show` and include a `watchers` count.

### Popular: broad popularity ranking

```sh
trakt movie popular --limit 25 --json
trakt tv popular --page 2 --limit 25
```

Popular is a ranking based on rating percentage and number of ratings, not a personalized recommendation.

### Anticipated: upcoming interest

```sh
trakt movie anticipated --page 3 --limit 10
trakt tv anticipated --limit 10 --json
```

Anticipated reflects list appearances and upcoming interest. It is not the same as a release calendar.

Global flags can appear before or after the resource: `--json`, `--dry-run`, `--quiet`, and `--verbose`.

## Pipeline recipes

### Trending handoff to another tool

1. Run `trakt --json movie trending --limit 20`.
2. Unwrap `.movie`, retaining `.watchers` as the watch signal.
3. Pass an available `.movie.ids.tmdb` or `.movie.ids.imdb` to a downstream tool; do not assume a missing ID can be synthesized.

```sh
trakt --json movie trending --limit 20 |
  jq '.movies[] | {title: (.movie.title // .title), year: (.movie.year // null), watchers: (.watchers // null), ids: (.movie.ids // .ids)}'
```

### Compare discovery signals

Fetch matching pages of trending, popular, and anticipated (e.g. `--page 1` for each), then label each dataset before combining it. Trending is recent watching, popular is broad ranking, and anticipated is upcoming interest.

### Page through anticipated until the feed ends

Loop `--page`, read `pagination.page_count` from JSON output to pick the stop page, and break early if a page returns no items:

```sh
for p in $(seq 1 "$(trakt --json movie anticipated --page 1 --limit 100 | jq -r '.pagination.page_count')"); do
  trakt --json movie anticipated --page "$p" --limit 100 |
    jq --arg p "$p" '{page: ($p|tonumber), pagination: .pagination,
                      movies: [.movies[] | {title: (.movie.title // .title), year: (.movie.year // null)}]}'
done
```

Keep per-page output as labeled NDJSON; merge afterwards. On 429, wait out `Retry-After` before continuing the loop.

## JSON and pagination

`--json` emits an object with a `movies` or `shows` array (trending entries retain their wrapper) plus a `pagination` object whose keys mirror the API's `X-Pagination-*` headers: `page`, `limit`, `page_count`, `item_count`. Pagination keys are ints when the headers were present and the object is empty `{}` when they were absent, so jq like `.pagination.page_count // 1` degrades safely. Human output appends a `Page N of M` line when the headers are present and stays silent otherwise. The API defaults to page 1 with limit 10 for compatibility; set both explicitly for reproducible automation, and stop at `page_count` rather than assuming a short page is the end.

## Known gotchas

- **Header pair is mandatory:** sending `trakt-api-key` without `trakt-api-version: 2` (or vice versa) can yield an invalid-request/authentication-style failure. The bundled script injects both on every live request.
- **401 versus 403:** 401 commonly indicates an OAuth requirement or invalid authorization; 403 indicates an invalid or unapproved application key. Do not retry either blindly.
- **Rate limits:** on 429, honor `Retry-After` and inspect `X-Ratelimit`. Use bounded retries; transient 502/503/504 responses may be retried with backoff.
- **OAuth refresh:** access tokens last seven days and refresh tokens are single-use. Replace the stored refresh token after a successful refresh; `invalid_grant` requires reauthorization.
- **Trakt is not TMDb:** Trakt IDs and discovery rankings are not TMDb metadata. Use the `tmdb` skill for credits, images, provider metadata, and catalog enrichment.
- **Trending shape:** read `.movie` or `.show` before title/IDs, while preserving `watchers`.
- **Pagination is per invocation:** one CLI call fetches exactly one page (`--page`); loop invocations reading `pagination.page_count` rather than expecting the script to follow links itself.

## When to use

Use Trakt for current watching signals, broad popularity, anticipated interest, and identifiers that feed a media workflow.

## When not to use

Do not use Trakt for TMDb catalog metadata, credits, images, provider availability, or for writing a user's lists without an explicit OAuth-enabled workflow. Use `tmdb` for metadata and a dedicated authenticated operation for mutations.

## Reference files

| File | Topic |
|---|---|
| [references/auth-and-request-contract.md](references/auth-and-request-contract.md) | Required headers, OAuth boundary, errors, and rate limits |
| [references/discovery-endpoints.md](references/discovery-endpoints.md) | Endpoint semantics, filters, response shapes, and pagination |
| [references/recipes-and-operations.md](references/recipes-and-operations.md) | Pipelines, jq normalization, and operational handling |

## Available script and prerequisites

- `scripts/trakt` is an executable Python CLI using only stdlib and `requests`.
- `--dry-run` works without a Client ID and never performs network I/O.
- Live discovery requires `TRAKT_CLIENT_ID`; tests are mock-only.
