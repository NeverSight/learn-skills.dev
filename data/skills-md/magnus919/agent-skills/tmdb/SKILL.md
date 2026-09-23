---
name: tmdb
description: >-
  Query TMDb metadata for films and television, then enrich results with details, credits,
  providers, and external IDs. Do not use this skill for personal watch history,
  watchlists, or tracking; use `trakt` for user activity and watch-state workflows.
license: MIT
compatibility: Requires TMDB_ACCESS_TOKEN or TMDB_API_KEY, Python 3.8+, and requests.
metadata:
  tags: tmdb, movies, tv, film, cinema, metadata
  sources: https://developer.themoviedb.org/reference
---

# TMDb metadata from the terminal

## Setup

Create credentials at [TMDb API settings](https://www.themoviedb.org/settings/api). Prefer the API Read Access Token:

```bash
export TMDB_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
# Or use the v3 key: export TMDB_API_KEY="YOUR_API_KEY"
```

The CLI sends either `Authorization: Bearer $TMDB_ACCESS_TOKEN` or `?api_key=$TMDB_API_KEY`. Both forms have the same v3 access level; configure only one. `--help` and `--dry-run` do not need credentials.

## Essential commands

### Search and identify

```bash
tmdb movie search --term "dune" --limit 5 --json
tmdb tv search --term "severance" --limit 5
tmdb find tt0111161 --source imdb_id --json
```

`--source` accepts one of the official external-source values: `imdb_id`, `facebook_id`, `instagram_id`, `tvdb_id`, `tiktok_id`, `twitter_id`, `wikidata_id`, and `youtube_id`. Freebase lookups are not supported: the retired `freebase_mid` and `freebase_id` values are rejected. The response is split into `movie_results`, `tv_results`, `person_results`, `tv_season_results`, and `tv_episode_results`.

### Details and enrichment

```bash
tmdb movie detail 550 --append credits,videos --json
tmdb movie detail 550 --append 'credits,watch/providers,external_ids' --json
```

Compound responses use the requested names as top-level keys. Encode the slash in `watch/providers` when constructing raw URLs.

### Discover and browse

```bash
tmdb movie discover --genre horror --rating 7 --limit 10
tmdb movie discover --genre horror --certification R --from 2024-01-01 --to 2024-12-31
tmdb trending --type all --window week --limit 20 --json
tmdb genre list --type movie --json
tmdb genre list --type tv --json
tmdb certification --json
```

Use `vote_count.gte` with `vote_average.desc` in raw discover requests so a title with very few votes does not dominate. In current TMDb docs, comma-separated genre IDs are AND and pipe-separated IDs are OR.

## Pipeline recipes

### IMDb ID to enriched movie

1. Resolve the IMDb identifier:

```bash
curl -s -H "Authorization: Bearer $TMDB_ACCESS_TOKEN" \
  'https://api.themoviedb.org/3/find/tt0111161?external_source=imdb_id' > /tmp/find.json
id=$(jq -r '.movie_results[0].id' /tmp/find.json)
```

2. Fetch details and compound resources:

```bash
curl -s -H "Authorization: Bearer $TMDB_ACCESS_TOKEN" \
  "https://api.themoviedb.org/3/movie/$id?append_to_response=credits,videos,watch%2Fproviders" \
  | jq '{title, runtime, director: [.credits.crew[] | select(.job == "Director") | .name], cast: [.credits.cast[0:5][].name], providers: .["watch/providers"].results.US}'
```

### Search then detail

```bash
tmdb movie search --term "dune" --limit 1 --json > /tmp/search.json
id=$(jq -r '.results[0].id' /tmp/search.json)
tmdb movie detail "$id" --append recommendations,similar --json
```

### Filter reliable discoveries

For direct API use, combine a date window, pipe-OR or comma-AND genre expression, `vote_count.gte`, and `sort_by=vote_average.desc`. Then retain only the fields needed by the next workflow step with jq.

## JSON and jq

Put `--json` before or after the subcommand. JSON search output has `results` and usually pagination fields `page`, `total_pages`, and `total_results`; the service limits page numbers to 500. Use `jq -r '.results[] | [.id, (.title // .name)] | @tsv'` for stable tabular handoff.

## Known gotchas

- **Credential duality:** `api_key` and Bearer are alternatives, not values to mix. A rejected credential commonly produces HTTP 401, `status_code: 7`, and `Invalid API key: You must be granted a valid key.` Permission failures use code 3. Code 33 means an invalid request token, not this API-key message.
- **Pagination ceiling:** pages start at 1 and max at 500; over-limit requests fail. Search/discover access is effectively capped at 10,000 results, even where totals look larger. Rate guidance is around 40 requests/second and 429 responses should honor `Retry-After`.
- **Compound syntax:** append values are comma-separated and limited to 20 calls. `watch/providers` contains a slash, so URL-encode it in curl and use jq's `.\"watch/providers\"` notation.
- **External-ID shape:** `/find/` does not return one generic `id`; inspect the appropriate nested array before choosing movie or TV detail. Only the eight documented `external_source` values are valid, and the retired Freebase sources (`freebase_mid`, `freebase_id`) are rejected.
- **Provider filters:** `with_watch_providers` requires `watch_region`; provider data carries JustWatch attribution requirements.
- **Localization and images:** use `language=en-US` and a market `region` when reproducibility matters. Build image URLs from `/3/configuration`'s secure base URL, a valid size, and the returned path.

## When to use

Use this skill for read-only film and TV metadata discovery, credits, release information, certifications, images, recommendations, and provider metadata.

## When not to use

Do not use it for torrent or piracy searches, playing or downloading a stream, or maintaining personal watched/unwatched state. Use `trakt` for watch-history workflows and a playback/catalog integration for availability actions.

## Reference files

| File | Use it for |
| --- | --- |
| [references/auth-pagination-and-errors.md](references/auth-pagination-and-errors.md) | Credentials, pagination, rate limits, errors, language, regions, and images |
| [references/find-and-details.md](references/find-and-details.md) | IMDb/TVDB lookup, response mapping, detail fields, compound requests |
| [references/search-discover-trending.md](references/search-discover-trending.md) | Search, discover filters, trending, genre, certification, and release lists |

## Available scripts and prerequisites

- `scripts/tmdb` is an executable Python CLI using only the standard library and `requests`; it preserves `--json`, `--dry-run`, `--quiet`, and `--verbose`.
- `scripts/test_tmdb.py` is an offline unittest/pytest suite; all HTTP behavior is mocked.
- Requires Python 3.8+ and `requests`. No service is started by this skill.
