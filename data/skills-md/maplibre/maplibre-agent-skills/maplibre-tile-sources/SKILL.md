---
name: maplibre-tile-sources
description: How to choose and configure data sources for MapLibre GL JS — rendering your own data without tiles, hosted tile services, serverless PMTiles, self-hosted tile servers, tile schemas, glyphs, and sprites.
---

# MapLibre Tile Sources

MapLibre GL JS does not ship with map data. You provide a **style** that references **sources** — URLs or inline data that MapLibre fetches and renders. MapLibre works equally well for a store locator with 200 addresses, a city transit map, and a global basemap — the right source type depends on geographic scale and level of detail, update frequency, infrastructure constraints, and use case.

## When to Use This Skill

- Setting up a new MapLibre map and choosing where your data comes from
- Deciding between GeoJSON, serverless tiles, hosted services, a combination thereof, or self-hosted options
- Configuring glyphs (fonts) and sprites so labels and icons render
- Debugging blank maps or missing tiles
- Migrating from Mapbox and need equivalent tile sources and style setup

## How styles and sources work

A **style** (a style JSON, style document, or style object) is the configuration you pass to MapLibre. It contains the specific rendering rules governed by the [MapLibre Style Specification](https://maplibre.org/maplibre-style-spec/), maintained with parity for MapLibre GL JS and MapLibre Native.

You can use a **style URL** from a provider — that URL references a style with sources, layers, glyphs, and sprite. Or you can **build your own style** and configure each yourself.

A style has three main components:

- **Sources** — Point to the actual data. Each source has a `type` and either inline data or a URL. MapLibre requests tiles or data as the viewport changes. The same source can back many layers (e.g. roads, water, and labels all from one vector URL).
- **Layers** — An ordered list defining what to draw and how. Each layer references a source (and for vector tiles, a `source-layer` name) and specifies paint/layout properties.
- **Glyphs and sprite** — Required for text and icons: URLs to font SDF stacks and icon spritesheets. Without them, labels and symbols won't appear.

**Source types:**

| Type         | Description                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------- |
| `vector`     | Vector tiles — binary-encoded geometry and attributes; the primary format for basemaps and data overlays |
| `raster`     | Raster tile imagery — satellite photos, WMS/WMTS layers                                                  |
| `raster-dem` | Elevation tiles — for terrain rendering and hillshading                                                  |
| `geojson`    | GeoJSON data — inline object or URL; no tile server needed                                               |
| `image`      | A single georeferenced image — scanned maps, annotated overlays                                          |
| `video`      | Georeferenced video                                                                                      |

`vector` and `raster` are the most common for basemaps and data overlays. `geojson` is ideal for small datasets or interactive data that doesn't need tiling. `raster-dem` is used for terrain and hillshade effects, as well as emerging use cases in scientific visualization. `image` and `video` sources are the least common, but let you georeference static images (such as a scanned map, chart, or overlay) or georeferenced videos as map layers.

## GeoJSON and Direct Data Sources

For many use cases you don't need a tile service. MapLibre can render points, lines, or polygons directly from an inline GeoJSON object or a URL to a GeoJSON file. The entire dataset is downloaded and parsed in the browser; MapLibre handles rendering client-side.

```javascript
map.addSource('my-data', {
  type: 'geojson',
  data: '/path/to/data.geojson' // or an inline GeoJSON object
});
map.addLayer({
  id: 'my-layer',
  type: 'fill',
  source: 'my-data',
  paint: { 'fill-color': '#0080ff', 'fill-opacity': 0.5 }
});
```

### GeoJSON performance thresholds

GeoJSON downloads the entire file on every load. This works well at small scale and degrades predictably:

| Range      | File size / feature count        | Behavior                                                                                                    |
| ---------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Sweet spot | < 2 MB / < 5,000 features        | Instantaneous loading, smooth interaction                                                                   |
| Lag zone   | 5–20 MB / up to ~50,000 features | 1–3s parse delay; mobile may struggle; optimize by simplifying geometries and reducing coordinate precision |
| Crash zone | > 50 MB / > 100,000 features     | High risk of browser freeze or crash; switch to vector tiles                                                |

GeoJSON is **lossless** (exact coordinates preserved) and gives you full client-side access to feature properties — ideal for interactive data, dynamic updates, and datasets where you need to query or modify features without a server round-trip.

If your dataset exceeds these thresholds, or if you need zoom-dependent rendering (less detail at lower zoom levels), consider vector tiles instead.

### Other formats and the cloud-native ecosystem

The choice of data source is shaped by more than performance: data type, update frequency, access patterns, and the broader geospatial ecosystem all factor in. Many formats (FlatGeobuf, GeoParquet, Cloud-Optimized GeoTIFF, KML, GPX, and more) can be displayed in MapLibre via plugins and custom protocols. The cloud-native geospatial ecosystem — formats designed for HTTP range requests and distributed storage — is evolving rapidly and increasingly relevant for web maps. A separate skill will cover this in depth; for now, see the [Map Rendering Plugins](https://github.com/maplibre/awesome-maplibre#map-rendering-plugins) and [Utility Libraries](https://github.com/maplibre/awesome-maplibre#utility-libraries) sections of awesome-maplibre.

## When You Need Tiles

Vector tiles load only the data visible in the current viewport, in a compact binary format. Use them when:

- Your dataset exceeds GeoJSON's practical limits
- You need zoom-dependent rendering (different levels of detail at different zoom levels)
- You need global or regional reference layers, such as land and water, roads, place names, etc. (i.e., basemap data)
- Bandwidth efficiency matters at scale

### Vector tiles vs. raster tiles

When you need tiles, you'll choose between two tile types:

**Vector tiles** encode geometry and feature attributes as compact binary data (Mapbox Vector Tile format, or the newer [MapLibre Tile / MLT](https://maplibre.org/maplibre-tile-spec/)). MapLibre renders and styles them client-side:

- Styles can be changed without regenerating tiles
- Features are queryable (click, hover interactions)
- Text renders crisply at any zoom or screen density
- Significantly smaller file sizes than equivalent raster tiles

**Raster tiles** are pre-rendered images (PNG, JPEG, or WebP) at each zoom level, displayed by MapLibre as-is:

- No client-side styling or feature querying
- Larger file sizes, but simpler to generate and serve
- Good fit for satellite/aerial imagery, WMS/WMTS integration, or rendered styles that don't need client-side customization

Most MapLibre workflows use vector tiles; increasing numbers are integrating `raster-dem` sources e.g. for terrain rendering. Use raster tiles when you need satellite/aerial imagery, when integrating with existing WMS or WMTS services, or when you need a pre-rendered cartographic style.

### Using MapLibre with Leaflet

[Leaflet](https://leafletjs.com/) is a widely used JavaScript mapping library that supports only raster tiles. If your app is built on Leaflet, [MapLibre GL Leaflet](https://github.com/maplibre/maplibre-gl-leaflet) lets you pre-render a MapLibre GL compatible style as a raster layer — allowing you to use hosted vector tile sources in your Leaflet app.

### Combining source types

A MapLibre style can have any number of sources of any types simultaneously. Layers from different sources are composited in draw order. This makes it natural to mix sources for different purposes.

Sources can be composited in a custom style sheet or at run-time. Be aware that layer order matters: layers are drawn bottom-to-top in the order they appear in the style. A raster layer added after vector layers will obscure them.

- **Vector basemap + GeoJSON overlay** — the most common pattern. Use a provider's style URL (or any vector tile source) as your basemap and add your own data on top with `map.addSource()` and `map.addLayer()`. To keep labels readable, insert your layer before the first symbol layer rather than appending to the top of the stack.

```javascript
// Start with any basemap style URL, then add your own data below labels
map.on('load', () => {
  // Find the first symbol (label) layer to insert below
  const firstSymbolId = map.getStyle().layers.find((l) => l.type === 'symbol')?.id;

  map.addSource('my-data', { type: 'geojson', data: '/path/to/data.geojson' });
  map.addLayer(
    { id: 'my-layer', type: 'circle', source: 'my-data' },
    firstSymbolId // insert before labels; omit to append above everything
  );
});
```

- **Raster imagery + vector labels** — add a raster source for satellite imagery, weather radar, historical imagery, heatmaps rendered server-side, or any imagery that isn't available as vector data. Add a vector source for roads, place names and other labels. This gives crisp imagery with crisp, resolution-independent vector geometries and labels on top.
- **Vector basemap + raster-dem terrain** — add hillshading or 3D terrain to any vector basemap using a `raster-dem` source (elevation tiles). This is how MapLibre renders terrain and hillshade without a separate basemap style.

## Hosting Tile Sources

"Hosting" tile data can mean two different things:

- **Storing files on the web** — A `.pmtiles` archive (or pre-generated tile directory) lives on static storage like S3, R2, or GitHub Pages. No server process runs; MapLibre fetches tiles over HTTP using range requests or standard HTTP. Updates require regenerating and re-uploading the file.
- **Running a tile server** — A server process handles tile requests dynamically, often from a database (PostGIS) or source file (MBTiles, PMTiles). Supports live data and on-the-fly generation, but requires deployment and ongoing maintenance.

The three options below map to these two approaches: PMTiles is file-based and serverless; hosted tile services run tile server infrastructure on your behalf; self-hosted means you run your own server.

### Serverless (PMTiles)

[PMTiles](https://docs.protomaps.com/pmtiles/) is an open single-file tile format that supports vector or raster tiles — MapLibre fetches only the byte ranges it needs via HTTP range requests, with no tile server. Extract only the geographic scale you need, and host a `.pmtiles` file on static storage (S3, R2, GitHub Pages).

See [maplibre-pmtiles-patterns](../maplibre-pmtiles-patterns/SKILL.md) for setup.

### Hosted tile services

Many providers offer hosted vector or raster tiles and pre-built style and tile URLs — no server to run. See [Map/Tile Providers in awesome-maplibre](https://github.com/maplibre/awesome-maplibre#maptile-providers) for a full list.

- ✅ Global CDN; pre-built styles available
- ✅ Handles global to local scale
- ⚠️ Custom style layer definitions must match the schema of the hosted tile source
- ⚠️ Vendor dependency
- ⚠️ API keys required by most; check license, usage limits and pricing
- ⚠️ Attribution requirements vary; verify before launch

Store API keys in environment variables; never commit to source control.

### Self-hosted tile server

Run your own server for full control over data, cost, and deployment. See [Tile Servers in awesome-maplibre](https://github.com/maplibre/awesome-maplibre#tile-servers) for options, including the MapLibre-maintained 💙 [Martin](https://maplibre.org/martin/). Use an existing tile schema or generate custom tiles with [Planetiler](https://github.com/onthegomap/planetiler) or [tippecanoe](https://github.com/felt/tippecanoe).

- ✅ Full control; no per-request cost at scale
- ✅ Can serve dynamic data and convert to tiles on the fly
- ✅ Supports air-gapped deployments
- ⚠️ Data to process, and infrastructure to deploy and maintain
- ⚠️ You must configure CORS and supply glyphs and sprite in your style

## Custom styles

A custom style is one you write yourself, rather than using a provider's pre-built style URL. Custom styles can reference either hosted or self-hosted tile sources — and in practice, the most common pattern is both:

- **Hosted tile sources** — Your style JSON points to a provider's tile URL. You control visual appearance while relying on the provider for tile delivery. Your layer definitions must match the provider's tile schema, and you typically reuse their glyphs and sprite.
- **Self-hosted tile sources** — Your style JSON points to your own tile server or PMTiles file. You control both style and data, but must supply glyphs and sprite yourself (or reuse publicly available ones that match your tile schema).

The most common real-world pattern is a hybrid: a custom style that references a hosted provider's basemap tiles — and often reuses their glyphs and sprite — while adding self-hosted tile sources or GeoJSON overlays for your own data. This gives you full control over your data layers without building basemap tile infrastructure from scratch.

### Pre-Defined Tile Schemas

When building a custom style (rather than using a provider's pre-built style URL), you need to know the **tile schema** — the source-layer names and their properties. Your style's layer definitions must match the schema of your tile source.

Common schemas:

- **OpenMapTiles** — the most widely adopted schema, based on OpenStreetMap data. Rich and detailed, with source-layers like `transportation`, `water`, `landuse`, `poi`. The largest ecosystem of community styles targets this schema.
- **Shortbread** — an open standard designed to be minimal and interoperable, not tied to any single vendor. Simpler structure than OpenMapTiles; a clean foundation if you're building styles from scratch.
- **Protomaps** — purpose-built for the Protomaps PMTiles basemap ecosystem. Flat, simple structure with source-layers like `land`, `water`, `roads`, `places`; optimized for serverless delivery.

If you use a provider's pre-built style URL, the schema is already matched.

### Glyphs (Fonts) and Sprites

Every MapLibre style that shows text or icons needs:

- **glyphs:** URL template for font stacks — `"glyphs": "https://example.com/fonts/{fontstack}/{range}.pbf"`
- **sprite:** Base URL for sprite sheet and metadata (serves both `.json` and `.png`) — `"sprite": "https://example.com/sprites/basic"`

Pre-built style URLs from hosted providers include their own glyphs and sprite. When building a custom style or self-hosting, you must supply these URLs.

If you are modifying a style based on a pre-defined tile schema, look for an existing style that matches that schema and reuse the glyphs and sprites. Pay attention to licensing and attribution requirements when reusing assets. If needed you can host the same glyphs and sprites yourself by downloading the files and serving them from your own storage or tile server.

The alternative is to generate your own glyphs and sprite sheets. See [Font Glyph Generation](https://github.com/maplibre/awesome-maplibre#font-glyph-generation) and [Sprite Generation](https://github.com/maplibre/awesome-maplibre#sprite-generation) in awesome-maplibre for tools to generate your own.

## TileJSON

[TileJSON](https://github.com/mapbox/tilejson-spec) is a standard JSON format for describing a tileset — its tile URL template, zoom range, bounds, center, attribution, and (for vector tiles) the available source-layers. Tile servers and providers expose TileJSON endpoints; MapLibre can consume them directly.

### Referencing tiles in a source

Tiles are addressed by zoom (Z), column (X), and row (Y) — a universal scheme across raster and vector tile sources (see [the OpenStreetMap wiki](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames) for more information). In a MapLibre source, you reference tiles either directly via a `tiles` URL template or via a `url` pointing to a TileJSON endpoint.

When a TileJSON endpoint is available, prefer `url`: MapLibre fetches the document and reads the tile URL template, zoom range, bounds, attribution, and (for vector tiles) the available source-layers automatically. Tile servers like Martin and tileserver-gl generate TileJSON endpoints for every tileset they serve, as do many hosted providers.

When no TileJSON endpoint exists — for example, a raw raster tile service that gives you a URL template directly — use the `tiles` array and specify any metadata (minzoom, maxzoom, attribution) in the source definition yourself.

**`tiles` array:**

```json
{
  "type": "vector",
  "tiles": ["https://example.com/tiles/{z}/{x}/{y}.pbf"],
  "minzoom": 0,
  "maxzoom": 14
}
```

**`url` to TileJSON endpoint:**

```json
{
  "type": "vector",
  "url": "https://example.com/tiles.json"
}
```

### TileJSON and custom styles

For vector sources, the TileJSON `vector_layers` field lists each available `source-layer`, its attribute fields, and its zoom range. This is the authoritative reference when building a custom style: your layer definitions must reference `source-layer` names exactly as they appear here.

When generating tiles with Planetiler or tippecanoe, the output embeds TileJSON metadata in the MBTiles or PMTiles file. Tile servers like Martin read this metadata and expose it as a TileJSON endpoint automatically.

## CORS

If your tiles, glyphs, or sprites are on a different origin, the server must send CORS headers (`Access-Control-Allow-Origin`). Otherwise the browser blocks requests and the map will be blank or missing labels.

Hosted providers handle CORS for you. For self-hosted servers or static storage, configure CORS on the server or CDN.

## Related Skills

- [**maplibre-pmtiles-patterns**](../maplibre-pmtiles-patterns/SKILL.md) — Serverless PMTiles hosting and MapLibre integration.
- **maplibre-style-patterns** — Layer and source configuration for common use cases. (Not yet in repo.)
- [**maplibre-mapbox-migration**](../maplibre-mapbox-migration/SKILL.md) — Replacing Mapbox tiles with MapLibre-compatible sources.

## References

1. **GeoJSON performance thresholds** (file size / feature count ranges) — community rules of thumb aggregated from Stack Overflow, Reddit, Medium, and Cesium Community Forum discussions. ⚑ _not authoritative or canonical_
2. **PMTiles format and HTTP range request protocol** — [docs.protomaps.com/pmtiles/](https://docs.protomaps.com/pmtiles/)
3. **Protomaps** (pre-built PMTiles basemaps) — [protomaps.com](https://protomaps.com)
4. **Planetiler** (generate vector tiles from OSM) — [GitHub](https://github.com/onthegomap/planetiler)
5. **tippecanoe** (generate vector tiles from GeoJSON) — [github.com/felt/tippecanoe](https://github.com/felt/tippecanoe)
6. **Martin tile server** — [maplibre.org/martin/](https://maplibre.org/martin/)
7. **MapLibre Tile (MLT) specification** — [maplibre.org/maplibre-tile-spec/](https://maplibre.org/maplibre-tile-spec/)
8. **OpenMapTiles schema** — [OpenMapTiles.org](https://openmaptiles.org/schema/)
9. **Shortbread tile schema** — [shortbread-tiles.org](https://shortbread-tiles.org/)
10. **Leaflet** — [leaflet.js](https://leafletjs.com/)
11. **MapLibre GL Leaflet** — [github.com/maplibre/maplibre-gl-leaflet](https://github.com/maplibre/maplibre-gl-leaflet)
12. **Cloud-native geospatial formats**: FlatGeobuf ([flatgeobuf.org](https://flatgeobuf.org/)), GeoParquet ([GeoParquet](https://geoparquet.org/)), Cloud-Optimized GeoTIFF ([COG website](https://cogeo.org/))
13. **awesome-maplibre** — [github.com/maplibre/awesome-maplibre](https://github.com/maplibre/awesome-maplibre)
