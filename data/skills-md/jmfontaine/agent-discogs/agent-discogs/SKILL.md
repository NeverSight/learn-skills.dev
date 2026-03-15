---
name: agent-discogs
description: >
  Discogs music database CLI for AI agents. Search releases, artists,
  labels, and master releases. Look up album details, tracklists, and
  vinyl prices. Explore artist discographies and compare pressings.
  Use when asked to "find a record", "look up an album", "check vinyl
  prices", "what pressings exist", "explore an artist's discography",
  "identify a pressing by catalog number", "compare different pressings",
  "how much is this record worth", "what's this album's value",
  "what label released this", "who played on this album",
  "find this song's album", "what year did this come out",
  "look up this catalog number", "search the music database",
  or any task involving music collecting and the Discogs database.
allowed-tools: Bash(agent-discogs:*)
---

# agent-discogs

CLI for searching and exploring the Discogs music database. Returns compact text output with a ref system for chaining commands.

## Setup

Requires `DISCOGS_TOKEN` for full access (60 req/min, search, price data):

```bash
export DISCOGS_TOKEN=<your-token>  # discogs.com/settings/developers
```

Without a token: 25 req/min, no search, no price suggestions.

Check status: `agent-discogs status`

## Core Workflow

1. **Search** — find entities by name
   ```bash
   agent-discogs search release "The Downward Spiral" --year 1994
   ```
2. **Inspect** — get full details using refs from search output
   ```bash
   agent-discogs get release @r367113
   ```
3. **Drill down** — tracklist, pricing
   ```bash
   agent-discogs tracks @r367113
   agent-discogs price @r367113
   ```
4. **Explore** — discography, versions
   ```bash
   agent-discogs get versions @m4917 --country US
   ```

## Output Format

- **search** — numbered list of matches with refs, title, year, format. Replaces all stored refs.
- **get release** — title, artists, label, format, tracklist summary, notes. Adds ref.
- **get release --verbose** — full details including inline `[@a...]` and `[@l...]` refs for chaining.
- **tracks** — numbered tracklist with durations and per-track artists (for VA releases).
- **price** — price suggestions by condition (Mint, Near Mint, VG+, etc.) and marketplace stats.
- **get versions** — table of pressings with country, year, format, label, and refs.
- **get releases** — artist discography with type, year, and refs.

## Common Patterns

| Goal | Commands |
|------|----------|
| Find a specific pressing | `search release "<title>" --year --country` → `get release @r...` |
| Compare pressings | `search master "<title>"` → `get versions @m...` |
| Explore discography | `search artist "<name>"` → `get releases @a...` |
| Check price | `search release "<title>"` → `price @r...` |
| Identify by catalog number | `search release --catno "INT-92346"` → `get release @r...` |
| Find by barcode | `search release --barcode "606949235024"` |
| Get original pressing | `search master "<title>"` → `get versions @m...` → `get release @r...` |
| Narrow release search | `search release "<title>" --artist "<name>"` |
| Get release notes | `get release @r... --verbose` |
| Get artist/label IDs from a release | `get release @r... --verbose` — inline `[@a...]` and `[@l...]` refs |
| VA compilation tracks | `get release @r...` — per-track artists shown automatically |
| Machine-readable output | Add `--json` to any command for raw JSON |

## Machine-Readable Output

All commands support `--json` for raw JSON output, useful for piping into other tools or extracting structured data:

```bash
agent-discogs search release "Blue Monday" --artist "New Order" --json
agent-discogs get release @r367113 --json
```

## Anti-Patterns

- **Don't search without a type filter** when you know the entity type.
- **Don't fetch full release details just to check price.** Use `price @r...` directly.
- **Don't paginate through all results.** Narrow with filters first.
- **Don't guess IDs.** Always search first to find the right entity.
- **Don't use `get versions` on a release ID.** Use a master ref (smart resolution costs an extra API call).

## Error Recovery

- **0 results** — broaden filters (drop `--year`, `--country`), try a different type (`master` instead of `release`), or simplify the query.
- **Auth required** — price suggestions and search require `DISCOGS_TOKEN`. Run `agent-discogs status` to check.
- **Invalid ref** — refs are session-scoped and reset on each search. Re-search to get fresh refs.
- **Rate limited** — wait briefly and retry. Authenticated requests get 60/min; unauthenticated get 25/min.

## Refs

Refs encode entity type and Discogs ID: `@a3857` (artist), `@r367113` (release), `@m4917` (master), `@l2919` (label). Raw numeric IDs also work.

**Ref chaining:** `get release @r... --verbose` embeds inline `[@a...]` and `[@l...]` refs in the output. Use these to chain into artist discographies or label catalogs without an extra search.

## Key Concepts

**Master** = canonical album. **Release** = specific pressing. **Version** = a release belonging to a master. Search masters to find all pressings; search releases to find a specific one. See [references/pressings-guide.md](references/pressings-guide.md) for details.

**Formats**, **genres**, **identifiers**, and other Discogs-specific data conventions are documented in [references/discogs-domain.md](references/discogs-domain.md).

## Token Efficiency

Prefer the most specific command: `tracks @r...` over `get release @r...` when you only need the tracklist, and `price @r...` over `get release @r...` when you only need pricing. This reduces output tokens and avoids unnecessary data.

## Reference Docs

| Document | Content |
|----------|---------|
| [references/commands.md](references/commands.md) | Full command reference with all flags |
| [references/search-patterns.md](references/search-patterns.md) | Effective search strategies |
| [references/pressings-guide.md](references/pressings-guide.md) | Master/release/version mental model |
| [references/discogs-domain.md](references/discogs-domain.md) | Discogs data model: formats, genres, country, artists, labels, identifiers |
