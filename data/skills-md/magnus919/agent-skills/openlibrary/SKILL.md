---
name: openlibrary
description: >-
  Query the Open Library catalog from the terminal: search books and authors,
  look up works, editions, and ISBNs, enumerate every edition of a work, read
  community ratings, and resolve cover-image URLs. Fully keyless public API.
  Includes the OL…M/W/A key-graph reference, ISBN 302-redirect resolution,
  search query syntax, covers-host rules, and worked pipelines. Do not use for
  library-IT administration (Koha/MARC/ILS migration), commercial book-data
  feeds, or managing your reading account on Open Library itself.
license: MIT
compatibility: Python 3.8+ and the `requests` library. No API key or registration
  required — reads are fully public. Optional OL_EMAIL env var adds a contact to
  the User-Agent for better rate-limit treatment.
metadata:
  tags: open-library, books, authors, isbn, library, book-search, api-client, catalog
  sources: https://openlibrary.org/developers/api, https://openlibrary.org/dev/docs/api/books
---

# openlibrary — Book Metadata from Open Library

Query Open Library's 50M+ record catalog over its public HTTP API: search works
and authors, walk the edition/work/author graph by ISBN or OLID, enumerate
editions, and read community ratings. No API key exists; everything here is a
keyless GET.

## Setup

Nothing to authenticate: **the public Open Library API requires no API key** for
reads. There is no token, no registration step, no lazy-auth dance.

```bash
# Optional etiquette: identified User-Agent gets ~3x rate budget (~3 req/s vs ~1)
export OL_EMAIL="you@example.com"
```

Requires Python 3.8+ and `requests` only. `--help` and `--dry-run` work with no
environment at all. Write endpoints exist upstream but require an authenticated
Internet Archive session and are effectively internal — treat this surface as
read-only.

Three hosts matter and they serve different things:

| Host | Serves |
|------|--------|
| `openlibrary.org` | metadata JSON: search, records, ratings |
| `covers.openlibrary.org` | cover images + author photos (separate service) |
| `archive.org` | scan content / bulk dumps (redirect targets) |

## Essential Commands

### find books — search

```bash
openlibrary search --query "dune"                       # relevance order
openlibrary search --query "dune" --sort editions       # most editions first
openlibrary search --query "dune" --sort new            # newest first
openlibrary search --query "foundation" --lang fr       # prefer French editions
openlibrary search --query "dune" --limit 5 --offset 10 # paginate
openlibrary search --query "dune" --json                # machine-readable
```

Results carry title, authors, `first_publish_year`, edition count, and the work
key (`/works/OL…W`) that feeds the other commands. The CLI validates `--sort`
choices client-side because an unknown sort value makes the server return a
plain-text HTTP 500.

### find people who write — author search

```bash
openlibrary search-authors --query "asimov"             # name candidates
openlibrary search-authors --query "le guin" --limit 5
openlibrary search-authors --query "asimov" --json      # includes top_work, work_count
```

Author docs arrive with bare keys (`OL23919A`), unlike book search's path keys.

### inspect records — author / work

```bash
openlibrary author OL23919A                # bio, dates, photo URL
openlibrary work OL1168083W                # description, subjects, cover URL
openlibrary work OL1168083W --json         # full record
```

Keys may be passed bare (`OL23919A`) or as paths (`/authors/OL23919A`) — the CLI
normalizes both.

### resolve an ISBN

```bash
openlibrary isbn 9780451524935             # ISBN-10 or ISBN-13
openlibrary isbn 9780451524935 --json      # + resolved edition_key, work_keys, cover_url
```

Upstream, `/isbn/<isbn>.json` answers a **302 redirect** to the canonical
edition JSON (`/books/<OL…M>.json`). The CLI follows it and reports which
edition matched via `edition_key`. If the edition record lacks author names
(some ship `authors:null`), the CLI recovers them from the linked work.

### list every edition of a work

```bash
openlibrary editions OL81699W                          # publisher/date/ISBN per edition
openlibrary editions OL81699W --limit 50 --offset 50   # page through large sets
openlibrary editions OL81699W --json                   # + next_offset when more exist
```

Backs onto `/works/<key>/editions.json`; `next_offset` is computed from the
server's prebuilt next-page link.

### read the room — community signals

```bash
openlibrary ratings OL45804W               # average rating + shelf counts
openlibrary ratings OL45804W --json        # full distribution + bookshelves
```

Joins `/works/<key>/ratings.json` (`summary.average`, per-star `counts`) with
`/works/<key>/bookshelves.json` (`want_to_read`, `currently_reading`,
`already_read`).

## Global Flags

Position-independent; put them before or after the subcommand:

```bash
openlibrary --json search --query "dune"     # machine output anywhere
openlibrary --dry-run isbn 9780451524935     # preview the exact URL, no network
openlibrary --quiet search --query "dune"    # suppress diagnostics
```

| Flag | Effect |
|------|--------|
| `--json` | One JSON object on stdout instead of human text |
| `--dry-run` | Print the planned request as JSON without executing it |
| `--quiet` | Suppress non-essential output |
| `--verbose` | Verbose logging |

## Multi-Step Pipeline Recipes

### ISBN → edition → work → author bio

The canonical walk across all three key types:

```bash
openlibrary isbn 9780451524935 --json | jq -r '.work_keys[0]'   # OL1168083W
openlibrary work OL1168083W --json | jq -r '.authors[0]'        # bare OL…A key
openlibrary author OL118077A                                    # bio, dates
```

The CLI keeps this pipeline type-safe: every command that emits an `authors`
field under `--json` (`isbn`, `work`) uses the same shape — an array of bare
OL…A keys — while human output renders comma-separated labels instead. Each hop
uses a different key suffix (M → W → A); see Known Gotchas before hand-assembling
these URLs yourself.

### Rank a series by community love

```bash
for w in $(openlibrary search --query 'series:dune' --limit 8 --json | jq -r '.results[].key'); do
  openlibrary ratings "${w##*/}" --json \
    | jq -c '{work: .key, avg: .average, rated: .ratings_count,
              want_to_read: .bookshelves.want_to_read}'
done
```

### Find readable ebooks, then their print editions

```bash
openlibrary search --query 'title:"moby dick"' --sort editions --json \
  | jq '.results[] | select(.has_fulltext) | {title, key}'
openlibrary editions OL81699W --json | jq '.editions[] | {key, isbn_13}'
```

## Using --json with jq

```bash
openlibrary search --query "voracious" --json | jq '.results[] | {title, first_publish_year}'
openlibrary search-authors --query "butler" --json | jq '.results[0] | {name, key, top_work}'
openlibrary isbn 9780451524935 --json | jq -r '.cover_url'          # covers host URL
openlibrary editions OL81699W --json | jq '[.editions[].publish_date]'
openlibrary ratings OL45804W --json | jq '.rating_distribution'
```

## Known Gotchas

- **ISBN endpoints answer 302, not JSON** — `/isbn/<isbn>.json`, `/lccn/*.json`,
  `/oclc/*.json` redirect to `/books/<OL…M>.json`. Clients must follow redirects
  (`curl -L`; `requests` does by default) or they parse an HTML redirect page.
  Direct `/books/<OLID>.json` calls return 200 immediately.
- **Merged keys return redirect stubs inside HTTP 200** — Open Library is a wiki;
  when duplicate works merge, the old key keeps answering 200 with
  `{"type":{"key":"/type/redirect"},"location":"/works/<master>"}` instead of a
  3xx. Detect the stub type in success responses and re-fetch. The bundled CLI
  does this automatically (and appends `.json` to stub locations, since
  extension-less URLs redirect to HTML pages).
- **Key types are encoded in the suffix** — `OL…M` = edition (`/books/`),
  `OL…W` = work (`/works/`), `OL…A` = author (`/authors/`). Works link to
  authors double-nested (`authors[].author.key`); editions nest flat
  (`authors[].key`) — or ship `authors:null` entirely, recovering names from the
  linked work. Requesting a key under the wrong collection yields a 301 reroute.
- **Search empties are not errors** — malformed queries parse loosely and come
  back HTTP 200 with `numFound:0`; conversely a bad `sort=` enum is a plain-text
  HTTP 500 and non-integer `limit` is a FastAPI 422. Branch on bodies, not just
  status codes.
- **`availability` needs `ia`** — in raw `/search.json` calls, requesting
  `fields=availability` silently returns nothing unless `ia` is also requested.
- **Covers live on another host** — image URLs are always
  `covers.openlibrary.org/b/id/<cover_id>-{S,M,L}.jpg` (or `/b/isbn/...`,
  `/a/id/...` for author photos). Missing covers return a blank placeholder with
  HTTP 200 unless you add `?default=false`; non-ID/non-OLID lookups cap at 100
  req/IP per 5 min then 403; cover URLs often 302 into archive.org zip shards.
- **Rate limits are policy, not headers** — no Retry-After/X-Rate-Limit headers
  exist. Anonymous ≈1 req/s; a `User-Agent: App (email)` (set `OL_EMAIL`)
  raises it to ≈3 req/s. Batch with one search rather than hundreds of lookups;
  bulk belongs in monthly dumps.
- **Text fields nest `{type,value}` objects** — older records wrap `bio`,
  `description`, `notes` as `{"type":"/type/text","value":"..."}` while newer
  ones use plain strings. Handle both; the CLI unwraps centrally.
- **OLID ≠ long-term identity** — deleted keys can be reassigned to unrelated
  books, and merged-away keys become redirect stubs. Pair OLIDs with title/ISBN
  in any cache.
- **`.json` placement matters for slugged URLs** — append `.json` to the bare
  key (`/authors/OL23919A.json`), never after a slug path.

## When to use

- Any question about books, authors, or works Open Library's public catalog can answer
- Resolving ISBNs/OLID keys to canonical records and walking edition/work/author graphs
- Finding readable or borrowable scans, cover images, community ratings/shelf counts

## When not to use

Do not use this skill for local library-catalog administration — Koha/Evergreen
ILS configuration, MARC batch processing, patron management — or for licensed
commercial data feeds (ISBNdb, Google Books), citation formatting, or managing
your own Open Library reading account/lists (that requires site login this skill
deliberately does not handle). For movie/TV metadata use tmdb instead.

## Reference Files

| File | Topic | Read when |
|------|-------|-----------|
| [references/api-overview-and-key-graph.md](references/api-overview-and-key-graph.md) | Access model, rate-limit etiquette, OLID M/W/A key graph, cross-collection 301s, merge-stub handling, `{type,value}` text wrapping | Assembling record URLs by hand, handling merges/wrong-key errors, or planning request pacing |
| [references/search-api-guide.md](references/search-api-guide.md) | `/search.json` parameters, sort keys, field scopes (`title:`, `isbn:`, …), `fields=` projection incl. the availability/ia interaction, `/search/authors.json`, `/subjects/<name>.json`, inside-book search, error model | Building precise queries, paginating deep result sets, or debugging empty results |
| [references/books-isbn-and-covers.md](references/books-isbn-and-covers.md) | Identifier endpoints and their 302 resolution, raw records vs legacy `/api/books` view models, editions listing, ratings/bookshelves shapes, covers-host URL rules and limits | Working with ISBNs/LCCNs/OCLCs, enumerating editions, or fetching images |
| [references/recipes-and-gotchas.md](references/recipes-and-gotchas.md) | End-to-end curl/jq pipelines (ISBN→work→author chain, ebook discovery, cover assembly, disambiguation) plus a symptom-indexed gotcha table | Wiring multi-step workflows or diagnosing an unexpected response |

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/openlibrary` | The CLI this skill drives: `search`, `search-authors`, `author`, `work`, `isbn`, `editions`, `ratings` — all with `--json`/`--dry-run`, automatic 302 + merge-stub resolution, `{type,value}` unwrapping, covers-host URL assembly, and client-side sort validation. Run it for every book-metadata question above. | `scripts/openlibrary search --query "dune" --json` |
| `scripts/test_openlibrary.py` | Offline pytest/unittest suite covering help, argument errors, dry-run plans, mocked-client logic (redirect stubs, author fallback, editions paging), plus two env-guarded live probes (`OPENLIBRARY_LIVE_TESTS=1`). Zero egress otherwise. | `.venv/bin/python3 -m pytest -p no:cacheprovider --strict-markers scripts/test_openlibrary.py` |

## Prerequisites

- Python 3.8+ with `requests` (stdlib otherwise); invoke as `python3 scripts/openlibrary ...` if not executable directly
- No credentials of any kind; optional `OL_EMAIL` for rate-limit etiquette
- `jq` recommended for `--json` post-processing
