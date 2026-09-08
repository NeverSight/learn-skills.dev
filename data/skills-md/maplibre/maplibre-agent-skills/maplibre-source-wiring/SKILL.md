---
name: maplibre-source-wiring
description: Getting a MapLibre GL JS source to actually render — TileJSON `url` versus hand-wired `tiles` templates, matching `source-layer` names to the tile schema, layer order and inserting below labels, `promoteId` and the feature ids that feature state needs, and the CORS and glyph failures behind a blank map. Use when a source is configured but nothing is drawing, or when setFeatureState does nothing.
status: verified
---

# MapLibre Source Wiring

You have a tile URL or a data file and a style, and the map is blank, drawing at the wrong
scale, or drawing in the wrong order. This skill covers connecting a source to a style
correctly, and the failure modes that look identical from the outside.

## When to Use This Skill

The source is already configured and the map is wrong in a way that produces no error. These are
symptoms as you would observe them, before you know the cause:

- The map is blank, or a layer you added draws nothing, and the console is clean
- A custom style renders nothing against a tile source that works with the provider's own style
- The basemap is blurry, or sits at a different scale than everything drawn on top of it
- Data you added has covered the street names
- Icons are missing while the rest of the map draws fine
- Hover or click highlighting does nothing at all, and no error is raised
- You have a tile endpoint and are unsure which source type it needs, or whether to point `url`
  at its TileJSON instead of hand-writing `tiles`

**Not this skill.** Text in the wrong font, missing scripts, or self-hosting glyph
PBFs — [maplibre-fonts-glyphs](../maplibre-fonts-glyphs/SKILL.md). Deciding the colors, type,
and drawing order of a style you are designing — [maplibre-cartography](../maplibre-cartography/SKILL.md).
Deciding whether a dataset belongs in GeoJSON or vector tiles at
all — [maplibre-tile-sources](../maplibre-tile-sources/SKILL.md).

## Referencing tiles: `url` vs `tiles`

Tiles are addressed by zoom (Z), column (X), and row (Y) — a universal scheme across raster and vector tile sources (see [the OpenStreetMap wiki](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames) for more information). In a MapLibre source, you reference tiles either directly via a `tiles` URL template or via a `url` pointing to a TileJSON endpoint.

**When a TileJSON endpoint is available, prefer `url`.** MapLibre fetches the document and reads the tile URL template, zoom range, bounds, attribution, and (for vector tiles) the available source-layers automatically. Tile servers like Martin and tileserver-gl generate TileJSON endpoints for every tileset they serve, as do many hosted providers.

When no TileJSON endpoint exists — for example, a raw raster tile service that gives you a URL template directly — use the `tiles` array and specify any metadata (minzoom, maxzoom, attribution) in the source definition yourself.

**`url` to a TileJSON endpoint:**

```json
{
  "type": "vector",
  "url": "https://example.com/tiles.json"
}
```

**`tiles` array:**

```json
{
  "type": "vector",
  "tiles": ["https://example.com/tiles/{z}/{x}/{y}.pbf"],
  "minzoom": 0,
  "maxzoom": 14
}
```

The cost of hand-wiring `tiles` is that MapLibre has no zoom range unless you supply one, and will assume `maxzoom: 22` — requesting zoom levels the tileset doesn't contain, which come back empty. This is why `url` is the default advice wherever a TileJSON endpoint exists. (For PMTiles specifically the same rule applies and the consequence is sharper — see [maplibre-pmtiles-patterns](../maplibre-pmtiles-patterns/SKILL.md).)

## Nothing renders: `source-layer` and the tile schema

The most common cause of a custom style rendering nothing against a working tile source is a `source-layer` mismatch.

A vector tile source contains named layers — `transportation`, `water`, `landuse` and so on — and every style layer that draws from it must name one exactly:

```json
{
  "id": "roads",
  "type": "line",
  "source": "basemap",
  "source-layer": "transportation"
}
```

`source-layer` is required for vector sources and must match the tile schema exactly. A typo or a name from a different schema produces no error and no output — the layer simply draws nothing.

**Find the real names in the TileJSON.** For vector sources, the TileJSON `vector_layers` field lists each available `source-layer`, its attribute fields, and its zoom range. This is the authoritative reference **when it is present** — but `vector_layers` is optional in TileJSON 3.0, and providers are inconsistent about supplying it. Its absence does not mean there is no schema: identify the schema by name (below) and work from its published layer list. If you use a provider's pre-built style URL, the schema is already matched for you; the mismatch only appears when you write your own layers.

### Pre-defined tile schemas

When building a custom style you need to know the **tile schema** — the source-layer names and their properties. Common schemas:

- **OpenMapTiles** — the most widely adopted schema, based on OpenStreetMap data. Rich and detailed, with source-layers like `transportation`, `water`, `landuse`, `poi`. The largest ecosystem of community styles targets this schema.
- **Shortbread** — an open standard designed to be minimal and interoperable, not tied to any single vendor. Simpler structure than OpenMapTiles; a clean foundation if you're building styles from scratch.
- **Protomaps** — purpose-built for the Protomaps PMTiles basemap ecosystem. Flat, simple structure with source-layers like `land`, `water`, `roads`, `places`; optimized for serverless delivery. Published layer list: [docs.protomaps.com/basemaps/layers](https://docs.protomaps.com/basemaps/layers).

Each of these publishes its layer list as documentation (see References). None carries a machine-readable version marker, so checking a schema means re-reading the page; nothing can poll it for changes.

When generating tiles with Planetiler or tippecanoe, the output embeds TileJSON metadata in the MBTiles or PMTiles file. Tile servers like Martin read this metadata and expose it as a TileJSON endpoint automatically.

## Layer order: drawing below labels

Layers are drawn bottom-to-top in the order they appear in the style. `map.addLayer()` with no second argument appends the layer **above everything**, including street names — which is why a data overlay added this way hides the basemap's labels. The fix is to pass the ID of the first `symbol` layer as `addLayer`'s second argument, found programmatically rather than hardcoded (`road-label` and friends are schema-specific and break the moment you change basemaps). A raster layer added after vector layers obscures them for the same reason.

For the injection pattern in full, and the canonical layer order for a style built from scratch, see [maplibre-cartography](../maplibre-cartography/SKILL.md).

## Missing labels and icons: `glyphs` and `sprite`

Two style-root properties supply the assets that symbol layers draw with:

- **`glyphs`** — URL template for font stacks: `"glyphs": "https://example.com/fonts/{fontstack}/{range}.pbf"`
- **`sprite`** — base URL for the sprite sheet and metadata, serving both `.json` and `.png`: `"sprite": "https://example.com/sprites/basic"`

Pre-built style URLs from hosted providers include their own. When building a custom style or self-hosting, you must supply them.

**The two fail differently when absent, and the difference is what makes a symptom readable backwards to a cause.** Since GL JS 5.11.0 an absent `glyphs` does _not_ remove text: MapLibre renders it in a local system font instead, so the symptom is text in the wrong face, not missing text. Reach for `glyphs` when the labels are there but wrong, not when they are absent entirely. An absent `sprite` has no equivalent fallback — icons are silently omitted.

For the fallback's mechanism and its limits (it is GL JS only; Native still needs served PBFs), font stacks, self-hosting versus generating, and script coverage, see [maplibre-fonts-glyphs](../maplibre-fonts-glyphs/SKILL.md).

## Raster sources: `tileSize` and naming traps

Two raster-specific pitfalls that wire without error but render wrong or against the wrong assumption:

**`tileSize` defaults to 512; classic OSM tiles are 256.** `tile.openstreetmap.org` and other classic slippy-map tile servers serve 256px tiles, but MapLibre's raster `tileSize` defaults to 512px. Omitting `tileSize: 256` for a 256px source doesn't error — it renders at the wrong effective zoom level, with imagery and labels appearing a zoom level off, with no error or warning:

```json
{
  "type": "raster",
  "tiles": ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
  "tileSize": 256
}
```

**A raster endpoint's name is not its type.** An endpoint named "hillshade," "terrain," or similar is not necessarily a `raster-dem` source. `raster-dem` requires the tiles to encode elevation as pixel-packed RGB (Mapbox or Terrarium encoding) in PNG or WebP — TileJSON's `encoding` field, when present, names which. A tile format that can't hold that encoding (JPEG, for instance) with no `encoding` field is ordinary `raster` imagery whatever the endpoint is named — a "hillshade" endpoint is often a pre-rendered hillshade _image_, not raw elevation data for MapLibre to shade client-side. Check the tile format and any `encoding` field before treating a name as evidence of `raster-dem`.

## Feature state: the source needs an id, and `promoteId` is usually how it gets one

`setFeatureState` and the `feature-state` expression key on a feature's **`id`** — a top-level member of the feature object, not a value inside `properties`. A source whose features have no id gives `setFeatureState` nothing to attach to, so it fails silently: no console error, the paint expression never fires, and `getFeatureState` returns empty.

**Set `promoteId` to the property you already key on.** It tells MapLibre to use that property as the feature id, and it is the right answer whenever the identifier lives in `properties`:

```js
map.addSource('parcels', {
  type: 'geojson',
  data: parcels,
  promoteId: 'parcel_id'
});
map.setFeatureState({ source: 'parcels', id: 'APN-1234' }, { hover: true });
```

For a vector source, `promoteId` is either a property name applied across all source-layers, or an object of the form `{<sourceLayer>: <propertyName>}`.[9]

**Do not reach for `generateId` or a hand-written `id` when a business key exists.** Both look like fixes and both fail this case:

- `generateId: true` assigns ids **by index in the `features` array, overwriting any existing values**.[9] The ids are not stable across a `setData` that reorders, filters, or appends, so state silently attaches to the wrong feature after an update.
- Writing a top-level `id` works only for integers: without `promoteId`, a feature's id "must be an integer or a string that can be cast to an integer."[9] A key like `APN-1234` is accepted and then never matches. With `promoteId` the value may be any primitive.

## CORS

If your tiles, glyphs, or sprites are on a different origin, the server must send CORS headers (`Access-Control-Allow-Origin`). Otherwise the browser blocks the requests and the map is blank or missing labels.

Hosted providers handle CORS for you. For self-hosted servers or static storage, configure CORS on the server or CDN. Range-request sources (PMTiles) additionally need `Access-Control-Allow-Headers: Range`.

## Diagnosing a blank map

Work down this list — the symptoms overlap heavily:

| Symptom                                       | Check first                                                          |
| --------------------------------------------- | -------------------------------------------------------------------- |
| Nothing at all, network shows failed requests | CORS headers; the tile URL itself (404s in the network tab)          |
| Nothing at all, network shows 200s            | `source-layer` names against the TileJSON `vector_layers`            |
| Tiles appear then vanish as you zoom in       | Missing zoom range on a hand-wired `tiles` source; use `url` instead |
| Tiles render, text in the wrong font          | `glyphs` missing, or its URL failing to load                         |
| Tiles render, no text at all                  | No `text-field` on any symbol layer; or GL JS older than 5.11        |
| Tiles render, no icons                        | Missing `sprite` at the style root                                   |
| Data draws but hides labels                   | Layer order; insert before the first `symbol` layer                  |
| Vector source draws nothing, raster fine      | `source-layer` missing entirely — it is required for vector sources  |
| Raster tiles render a zoom level off          | Missing `tileSize: 256` on a classic 256px source (default is 512)   |
| `setFeatureState` does nothing, no error      | Features have no `id`; set `promoteId` to the identifying property   |

## Related Skills

- [**maplibre-tile-sources**](../maplibre-tile-sources/SKILL.md) — Choosing between GeoJSON and tiles for a dataset.
- [**maplibre-pmtiles-patterns**](../maplibre-pmtiles-patterns/SKILL.md) — Registering the `pmtiles://` protocol and PMTiles-specific source setup.
- [**maplibre-fonts-glyphs**](../maplibre-fonts-glyphs/SKILL.md) — Font stacks, glyph endpoints, and script coverage.
- [**maplibre-cartography**](../maplibre-cartography/SKILL.md) — The layer-injection pattern in full, and canonical layer order for a custom style.

## References

1. **MapLibre Style Specification** — [maplibre.org/maplibre-style-spec/](https://maplibre.org/maplibre-style-spec/)
2. **TileJSON specification** — [specification repository on GitHub](https://github.com/mapbox/tilejson-spec)
3. **Slippy map tile naming (Z/X/Y scheme)** — [OpenStreetMap wiki](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)
4. **OpenMapTiles schema** — [openmaptiles.org/schema/](https://openmaptiles.org/schema/)
5. **Shortbread tile schema** — [shortbread-tiles.org](https://shortbread-tiles.org/)
6. **Protomaps basemap layers** — [docs.protomaps.com/basemaps/layers](https://docs.protomaps.com/basemaps/layers)
7. **Martin tile server** (TileJSON endpoints) — [maplibre.org/martin/](https://maplibre.org/martin/)
8. **MapLibre GL JS docs** — [maplibre.org/maplibre-gl-js/docs/](https://maplibre.org/maplibre-gl-js/docs/)
9. **`promoteId`, `generateId`, and `feature-state`** — [Style Specification: sources](https://maplibre.org/maplibre-style-spec/sources/) and [expressions](https://maplibre.org/maplibre-style-spec/expressions/)

---

**This skill is a snapshot.** Where a primary source contradicts it — the References above, MapLibre's current documentation, or what MapLibre does when you run it — that source wins. Follow it, then [report the disagreement](https://github.com/maplibre/maplibre-agent-skills/issues/new?template=ai-failure-report.md), citing the source and your MapLibre version: editing your installed copy helps no one else and is overwritten on the next update.
