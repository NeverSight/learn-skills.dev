---
name: arcgis-custom-data-feeds
description: Build ArcGIS Enterprise Custom Data Feeds (CDF) — Node.js/Koop providers that expose an external system as an ArcGIS Feature Service. Use when the user writes a CDF provider or model.js (getData/editData/authorize/getMetadata), uses the cdf CLI, or wants to expose a database, API, or other external system as a feature service in ArcGIS Enterprise.
---

# ArcGIS Enterprise Custom Data Feeds (CDF)

A Custom Data Feed is a **Node.js provider** — running on **Koop.js** inside the ArcGIS Enterprise SDK runtime — that pulls from any external source (REST API, database, file) and exposes it as a standard ArcGIS Feature Service. Your provider returns GeoJSON; the framework translates it into the GeoServices REST spec that ArcGIS clients consume.

Deployment and registration on ArcGIS Server (uploading `.cdpk`, `cdf register`) is **out of scope** here — this skill covers authoring and local testing of the provider.

## Confirm the target Enterprise version first — before any code

CDF arrived in **ArcGIS Enterprise 11.1** (it does not exist in 10.x), and its capabilities are gated by release. The provider you write depends entirely on the version it must run against, so pin it before writing anything:

- Ask which ArcGIS Enterprise version(s) must run this provider. A provider compiled against a newer runtime does not run on an older server — build against the **lowest** target release.
- **12.x requires a recompile.** Providers must be recompiled in 12.x to run there; a provider built on 11.x is not binary-compatible with a 12.x runtime.
- Match the **OS family and Node.js major version** of the development machine to the target server, or the compiled provider fails to load.

For the current release, the per-version capability list, and any breaking changes, read the live **[ArcGIS Enterprise SDK CDF guide](https://developers.arcgis.com/enterprise-sdk/guide/custom-data-feeds/)** and its "What's New" pages — do not rely on a restated matrix, which goes stale. To confirm a class, method, or option exists at a version, defer to the `arcgis-docs-lookup` skill.

## The 12.0 generation boundary

CDF **fundamentally changed at 12.0** — treat pre-12.0 and 12.0+ as two generations and never mix their assumptions:

- **The `config` npm module is retired in 12.0.** Store credentials in a local JSON file inside `src/` and `require()` it directly. On 11.1–11.5, `config/default.json` is standard (top-level keys must be unique across all providers in the app).
- **12.0 upgrade trap:** a provider that used the `config` module will **not** auto-re-register after an upgrade to 12.0. Migrate it to local JSON config _before_ upgrading.
- `getMetadata()` (below) exists only from 12.0.

## Project scaffolding — the cdf CLI

```bash
cdf createapp my-cdf-app          # once per project
cd my-cdf-app
cdf createprovider my-provider    # a provider inside the app
npm start                         # local dev server (HTTP :8080)
cdf export my-provider            # produce a deployable .cdpk
```

Generated shape (essentials): `providers/my-provider/src/index.js` (registration), `.../src/model.js` (core logic), `.../cdconfig.json` (provider config), `.../package.json` (provider deps).

> **Install npm packages at the provider level** (`providers/my-provider/`), never at the app level. Never modify `framework/` — the bundled Koop packages are read-only.

## The Model class

`model.js` exports a class with up to four methods. The "since" column is durable release history, not a live matrix:

| Method                 | Required | Since | Purpose                                             |
| ---------------------- | -------- | ----- | --------------------------------------------------- |
| `getData(req)`         | **Yes**  | 11.1  | Fetch data; return a GeoJSON FeatureCollection      |
| `editData(req, edits)` | No       | 11.4  | Handle applyEdits (adds / updates / deletes)        |
| `authorize(req)`       | No       | 11.5  | Pre-request authorization; throw to reject          |
| `getMetadata()`        | No       | 12.0  | Return `idField` + `inputCrs` for edit reprojection |

`getData(req)` returns a GeoJSON `FeatureCollection` with a `metadata` block. Use the **async/await** form and **never mix async and callback patterns in the same method** — doing so crashes the process. See [references/geojson-response-format.md](references/geojson-response-format.md) for the full response schema and [references/provider-patterns.md](references/provider-patterns.md) for the full-fetch vs. pass-through patterns.

Key `req` properties: `req.params.layer` (`'0'`, `'1'`, …), `req.params.<key>` (service parameter values), `req.query.where`, `req.query.resultOffset` / `req.query.resultRecordCount` (pagination), `req.query.returnCountOnly` (`'true'` → return `{ count: N }`), `req._user` (requires `forwardUserIdentity: true` on the service).

## GeoJSON response rules

- All features in a layer must share the **same geometry type**.
- **Always declare `fields` explicitly** — never rely on type inference from the first feature; it produces wrong types.
- **Always set `idField`** to a unique numeric property. Omitting it forces full-feature hashing (slow, collision-prone). For editable providers, `idField` must reference a real field — auto-generated OIDs are unsupported.
- Default CRS is WGS84 (4326); set `metadata.inputCrs` to the WKID when your data uses another.
- For multi-layer services, return `{ layers: [...], tables: [], metadata: { name, inputCrs } }` when `req.params.layer` is undefined.
- In the pass-through pattern, set `filtersApplied` (`where`, `geometry`, `objectIds`, `resultOffset`, `resultRecordCount`) to `true` for each filter you handled upstream so the framework does not double-apply it.
- `ttl` sets the LRU cache TTL in seconds (cache capacity: 500 elements).

## Guard destructive edits in editData()

`editData()` writes `adds` / `updates` / `deletes` to the provider's **upstream store** (a database, an external API) — these are irreversible data operations, so before generating any `editData` code that updates or deletes, satisfy every point in order:

1. **Name the target.** State the upstream system and the exact store/collection/table the writes hit. An unnamed target is a stop.
2. **Show what it is.** Surface what the update/delete affects (which records, roughly how many) so the user sees what they are about to change or lose.
3. **Confirm it is not production.** Say so explicitly and get the user's confirmation before proceeding.
4. **Prefer the reversible form first.** Offer a read-first / count-first path so the blast radius is known before the destructive write runs.
5. **Never emit blind.** Withhold the update/delete code until 1–4 are satisfied and the user confirms — even when the user sounds confident.

Return `{ addResults, updateResults, deleteResults }` with per-item `{ objectId, success, error? }`. Error codes: `1017` insert, `1018` delete, `1019` update. `rollbackOnFailure` is **not** enforced by the framework — implement transaction logic in `editData()` yourself. Gate writes with `authorize(req)` (throw to reject).

## Configuration and secrets

- **12.0+:** `require()` a local JSON config file inside `src/`. Add it to `.gitignore`.
- **11.1–11.5:** the `config` module (`config/default.json`).
- Never hardcode credentials; never commit config JSON with real secrets.

## Done when

The target Enterprise version is fixed (and the provider built against the lowest target, recompiled for 12.x if needed); pre-12.0 vs 12.0+ config handling matches that version; every `getData` response declares `fields` and a numeric `idField` with one geometry type per layer; secrets live in gitignored config, never inline; any `editData` update/delete has passed through the guard; and version-specific claims were confirmed against the live Enterprise SDK CDF guide via `arcgis-docs-lookup`.

## Reference files

| File                                                                                 | When to read                                                                      |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| [references/geojson-response-format.md](references/geojson-response-format.md)       | Full metadata schema, field types, multi-layer format, edit templates             |
| [references/provider-patterns.md](references/provider-patterns.md)                   | Full-fetch vs. pass-through, count/extent shortcuts, upstream auth                |
| [references/examples/minimal-provider.md](references/examples/minimal-provider.md)   | Complete working read-only provider (illustrative, targeting 12.0)                |
| [references/examples/editable-provider.md](references/examples/editable-provider.md) | Complete editable provider with a database backend (illustrative, targeting 12.0) |
