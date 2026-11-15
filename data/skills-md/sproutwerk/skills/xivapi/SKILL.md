---
name: xivapi
description: Query XIVAPI v2 for FFXIV (Final Fantasy XIV) game IDs, sheet data, NPC shops, currencies, map coordinates, and datamining lookups. Use when resolving FFXIV items, actions, statuses, quests, territories, or aetherytes without a running game client; covers query syntax, schema fields, joins, pagination, and coordinate conversion. Does not provide live actor state or plugin automation.
license: "MIT; bundled upstream files retain their own licenses, listed in NOTICE.md."
compatibility: Needs network access to v2.xivapi.com. The optional helper CLI needs Go 1.26 or newer and has no module dependencies.
---

# XIVAPI v2

`https://v2.xivapi.com/api` (server: **boilmaster**, `ackwell/boilmaster` on
GitHub). Read-only REST over the game's Excel (EXD) sheets, decoded with
`xivdev/EXDSchema`. Legacy v1 at `xivapi.com` still answers
(`/item/48` → flat JSON, `BaseParam0TargetID` style) but is frozen; use v2.
No auth. **Cloudflare returns 403 for the default `Python-urllib/x.y`
User-Agent** — set any other UA (curl's default is fine).

## Lookup workflow

1. Choose the game version from `/version`. Inspect field names in the
   [schema directory](references/schemas/), checking its revision against the
   response's `schema`. For another revision, read that sheet in EXDSchema at
   the returned commit. [OpenAPI](references/openapi.json) describes request
   parameters and response envelopes; it does not enumerate game-sheet fields.
2. Request only needed `fields=`. Use `+` on every required search clause
   and URL-encode queries once. Start with a bounded result count.
3. Resolve linked IDs using the returned `sheet` and `row_id`; disambiguate
   duplicate names by territory, title, job, or other task-specific fields.
4. On empty fields or HTTP 400, check the schema and query grammar before
   concluding that data is missing. Pin version/schema for reproducible work.
5. Return the IDs and query used, noting the returned version/schema and any
   ambiguity. Historical examples are not evidence of current shop contents.

For item, shop, currency, NPC, map, and alternate-service recipes, read
[lookup recipes](references/lookup-recipes.md). Full captured responses are in
[the cookbook](references/cookbook.md); dates and source limits are in
[provenance](references/provenance.md).

The optional [Go helper](scripts/xivapi/main.go) uses only the standard
library and has its own `go.mod`, so it builds without fetching modules. Run
`go run -C scripts/xivapi . --json search Item 'Name="Potion"' -f Name`
from the skill directory. Global options precede the subcommand. It exits 0
on success, 1 on a request or data error, and 2 on a usage error; `go run`
reports any failure as 1, so use `go build -C scripts/xivapi -o <path> .`
when the exact code matters. `--all` holds
results in memory; `--max-pages` defaults to 1000 and stops with an error when
exhausted. Repeated cursors or changing page metadata also fail without
emitting partial results. `XIVAPI_BASE` overrides the request destination;
use it only for an endpoint selected for the task.

A complete HTTP lookup, without the helper:

```sh
curl --max-time 30 --get 'https://v2.xivapi.com/api/search' \
  --data-urlencode 'sheets=Item' \
  --data-urlencode 'query=+Name~"Potion"' \
  --data-urlencode 'fields=Name,ItemUICategory.Name' \
  --data-urlencode 'limit=10'
```

## Endpoints (all GET)

| Path | Purpose | Params |
|---|---|---|
| `/version` | game versions known (`key` + `names`; `latest` alias) | – |
| `/sheet` | list available sheets | `version` |
| `/sheet/{Sheet}` | rows | `rows=1,2,262144:1` **or** `after=ROW[:SUB]`, `limit` (max 500, default 100), `fields`, `transient`, `language`, `schema`, `version` |
| `/sheet/{Sheet}/{row[:subrow]}` | one row | `fields`, `transient`, `language`, `schema`, `version` |
| `/search` | query across sheets | `sheets=A,B`, `query`, `limit` (max 500, default 100), `cursor`, `fields`, `transient`, `language`, `schema`, `version` |
| `/asset?path=…&format=png` or `/asset/{path}?format=png` | any game file → `png`/`jpg`/`webp` (`format` is required) | `version` |
| `/asset/map/{territory}/{index}` | composed 2048×2048 map (default `jpg`, `format=png` ≈6 MB) | `version` |
| `/docs`, `/openapi.json` | Scalar UI / OpenAPI 3 | – |

Errors are JSON `{"code":404,"message":"not found: the Excel row (none)/10566589:0 could not be found"}`.
`400 … no queries could be resolved` = a field in `query` doesn't exist on that
sheet (also what an unknown sheet name in `sheets=` produces).

### Field filter (`fields=`)

Comma-separated paths. **Always set it** — an unfiltered row expands every
relation recursively (SpecialShop 1770925 is ~1.7 MB, Aetheryte→Level→
TerritoryType inflates the same way).

- Nested: `PlaceName.Name`, `Map.OffsetX`, `Object.ENpcData`.
- Arrays must be targeted with `[]`: `Level[].X`, `ENpcData[].Name`,
  `Item[].Item[].Name`. **`Item[0].X` is a 400** (`error Eof at: [0]…`).
- Decorators: `Field@lang(ja)` (per-field language), `Field@as(raw)`
  (return the link's integer instead of expanding; works on arrays of links:
  `PreviousQuest@as(raw)` → `[65575,0,0]`, but **not** `PreviousQuest[]@as(raw)`),
  `Description@as(html)` (colour spans, `<br>`).
- Unknown field names are **silently dropped** (`fields=Nope,Name` returns just
  `Name`; a wrong array path returns `Item:[{},{},…]`). Empty output can mean a wrong
  path or schema mismatch; check the sheet at the returned schema revision.
- `transient=…` selects fields from the paired `*Transient` sheet
  (Action → ActionTransient.Description, Aetheryte → AetheryteTransient…).

Response shape: `{"schema","version","row_id","subrow_id?","fields":{…},"transient"?}`.
A link field is `{"value":N,"sheet":"Item","row_id":N,"fields":{…}}`; when the
target row doesn't exist (or is 0 in a sparse sheet) it is just `{"value":N}`.
Icons are `{"id":65122,"path":"ui/icon/065000/065122.tex","path_hr1":"…_hr1.tex"}`.

### Language / version / schema

- `language=en|ja|de|fr`. The OpenAPI enum also lists `chs|cht|kr`, but the
  global service has no data for them and answers 400 `invalid or unsupported
  language`.
  Default `en`. Some sheets are single-language and hold Japanese only
  (SpecialShopItemCategory 4 → `その他` even with `language=en`).
- `version=7.2` / `version=latest` / `version=<key>`; unknown → 400.
  Pinning the version also picks the matching EXDSchema rev automatically
  (`version=7.2` → `exdschema@2:rev:468f06ee…`).
- `schema=exdschema@2:rev:<sha>` pins a schema commit; `schema=exdschema@2:latest`
  uses the head of EXDSchema's `latest` branch, which can differ from the
  server default. Bare `schema=exdschema@2` → 500.
  Field names come from EXDSchema, so pin `schema` if you want stable names.

## Query grammar (`/search`)

`[specifier][op][value]` clauses separated by whitespace.

| Piece | Example | Notes |
|---|---|---|
| exact string | `Name="Sprint"` | **case-sensitive**; `Name="potion"` → 0 hits |
| partial | `Name~"hi-potion"` | case-insensitive substring; score ≈ `len(needle)/len(field)` (`"Allagan Tomestone of"` vs `…of Law` = 20/24 = 0.833) |
| number | `Territory=1278`, `LevelItem>=790`, `<`, `<=`, `>` | |
| boolean | `IsAetheryte=true` | |
| nested | `PlaceName.Name="Tuliyollal"`, `ItemUICategory.Name="Other"` | |
| array | `ENpcData[]=1770925` (any slot), `ENpcData[1]=1770925` (slot 1) | index **is** allowed in queries, unlike `fields` |
| language | `Name@ja="新月鉱石"` | or `language=ja` for the whole request |
| required / excluded | `+Name~"Tomestone" -Name~"Allagan"` | |
| grouping | `+(Name="Potion" Name="Hi-Potion") +LevelItem>=1` | OR inside parens |

**Bare clauses are optional and only affect score.** `PlaceName.Name="Tuliyollal"
IsAetheryte=true` returns *every* aetheryte with `IsAetheryte=true` (score 1.0)
plus Tuliyollal at 2.0. To filter, prefix every clause with `+`. A single
clause behaves as required. Score = number of matched clauses (exact/numeric
contribute 1.0, partial contributes its ratio); results sort by score.

URL-encode the query: a raw `+` in the URL becomes a space and yields
`error AlphaNumeric`. Use `curl -G --data-urlencode 'query=…'`.
`Name=Ecliptic` (unquoted string) → `error Char at: Ecliptic`.

Pagination: `limit` ≤ 500 (default 100); the response carries `next` (uuid) when more exist;
re-request with `cursor=<next>&limit=…` (`sheets`/`query` not needed, `fields`
still applies). No total count. `/sheet` paginates with `after=<last row_id>`
(or `after=ROW:SUB` for subrow sheets; `after=262156:65535` starts at row 262157).

Searchability: every sheet is indexed (Level, MapMarker, GilShopItem, ENpcBase
with 1M+ rows all work). "Not searchable" errors are really field-name errors.

## Gotchas (all observed)

- 403 with the `Python-urllib` default UA (Cloudflare). Set `User-Agent`;
  the Go helper sends its own.
- `fields=` typos/unknown paths are silent; array paths without `[]` return nothing.
- Bare search clauses are scored, not filtered — use `+`.
- `=` on strings is case-sensitive; `~` is not.
- `limit` caps at 500 on both `/search` and `/sheet` (default 100); pass more and you silently get 500.
- `rows=a,b` 404s the whole request if **any** row is missing.
- `rows=262144` on a subrow sheet returns only subrow 0; use `after=`.
- Link to a missing/sparse row → `{"value":N}` with no `fields` (Aetheryte.Level
  for main aetherytes, Action.ClassJob = −1/0).
- SpecialShop `ItemCost` is an indirect currency slot when `UseCurrencyType=4`
  (tomestones, via `TomestonesItem.Tomestones`); Garland Tools shows the
  resolved item, XIVAPI shows the raw slot.
- EXDSchema `relations:` groupings (`ReceiveItems`, `ItemCosts`) are schema-only.
- Same name, several rows: ENpcResident (per placement), Status, Action (PvP
  copies), Quest (NG+ copies), BNpcName. Disambiguate with `Title`, `IsPvP`,
  `ClassJob`, `Id`.
- Level sheet ≠ LGB layout: only event-referenced placements exist; many NPCs
  and all main-city aetherytes have no row. For those use MapMarker (map pixel)
  or in-game (Dalamud `ObjectTable`, Lifestream).
- Territory ↔ Map is many-to-one (`Map.TerritoryType` points at one of them).
- Default server schema rev can lag `exdschema@2:latest`; pin `schema=` for
  reproducible field names across days.

