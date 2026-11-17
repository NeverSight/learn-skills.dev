---
name: build-with-arcgis-and-openlayers
license: Apache-2.0
description: Use to build, extend, and troubleshoot browser based mapping applications with OpenLayers and ArcGIS services. Covers how to combine OpenLayers with ArcGIS basemaps, feature services, vector or raster tiles, location services, geocoding, routing, places, elevation, or secure ArcGIS resources. Includes ESM setup, ol-mapbox-style, ArcGIS REST JS, API keys and OAuth, projections, queries and pagination, styling, popups, editing, attribution, and performance.
---

# Build with OpenLayers and ArcGIS

OpenLayers (OL) renders browser maps with ArcGIS services. Use **`ol`** (maps/layers), **`ol-mapbox-style`** (ArcGIS Basemap Styles v2), and **ArcGIS REST JS** (`@esri/arcgis-rest-*`; auth, queries, location services).

OpenLayers is not an ArcGIS Maps SDK: it has no `FeatureLayer`/`WebMap` classes and does not interpret ArcGIS popup templates or renderers. Resolve endpoints and translate ArcGIS JSON explicitly.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

Use `ol-mapbox-style` for vector basemaps and REST JS for location services including geocoding, routing, elevation, geoenrichment, and authentication. Load OpenLayers CSS, give the map container a definite non-zero width/height, serve over HTTP(S), never `file://`, and verify current APIs/versions.

### New application

Infer requirements from the prompt/project; clarify uncertainties before scaffolding.

#### New application with CDN

Use current [ArcGIS OpenLayers examples](https://developers.arcgis.com/openlayers/): link `ol.css` as a stylesheet; load `dist/ol.js`, and needed REST JS UMD scripts in dependency order. These bundles expose globals; don't load them as ESM. Check URLs/versions via MCP. Most ArcGIS documentation shows CDN imports; use them for testing, demos, tutorials, samples, and lightweight quickstarts.

#### New application with npm

Use `npm create ol-app my-app` or Vite unless a framework is specified. Install `ol`, `ol-mapbox-style`, and any required `@esri/arcgis-rest-*` packages (request, feature-service, geocoding, routing, places). Use ESM imports and import `ol/ol.css` through the bundler; pin compatible versions per `ol-mapbox-style` notes. Prefer this for production, larger, or framework apps; use the project's package manager. React, Angular, Vue, and Svelte are supported frameworks. If using a framework-specific template other than `create ol-app`, remove all template files that are not relevant to the user's request (e.g. counter.js).

### Existing application

Before installing, identify package manager/lockfile, framework, CDN vs modules, TypeScript/ESLint config, and bundler. Conform; add only needed `ol`, `ol-mapbox-style`, and REST JS packages. Preserve credential/environment conventions, import `ol/ol.css`, size the map, and check compatibility before upgrades.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `openlayers` as the `focus_area` parameter in addition to a specified `search_term`; use the `arcgis-rest-js` focus area for ArcGIS REST JS queries. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

- [ArcGIS OpenLayers](https://developers.arcgis.com/openlayers/)
- [OpenLayers API](https://openlayers.org/en/latest/apidoc/)
- [ol-mapbox-style](https://openlayers.org/ol-mapbox-style/)
- [REST JS](https://developers.arcgis.com/arcgis-rest-js/api-reference/)
- [Attribution](https://esriurl.com/attribution)

## Patterns and guidelines

### Authentication integration
- Verify service-specific account support: Enterprise credentials alone do not authorize ArcGIS Location Services; use a supported Location Platform/Online credential for those services.
- **API keys**: Use `ApiKeyManager.fromKey(apiKey)` from `@esri/arcgis-rest-request` as REST JS `authentication`. Grant least privileges/item access; restrict browser keys by referrer. Browser keys are visible, even when set via build-time env vars. Never expose client secrets.
- **OAuth**: Use REST JS `ArcGISIdentityManager` with PKCE and exact redirect URIs.
- **Native OL sources**: REST JS does not integrate directly. Attach/refresh credentials in source loaders or `tileLoadFunction`; never expose client secrets or log tokenized URLs.
- See `arcgis-rest-js` and `follow-esri-authentication-patterns` skills.

### Basemaps, styles, and attribution
- Apply Basemap Styles v2 with `ol-mapbox-style` `apply(layerGroup, styleUrl)` to a dedicated `LayerGroup`, then add it to the map.
- Await style application before adding dependent layers; handle failures. Replace only this group when switching styles.
- Preserve visible **Powered by Esri** and each data item's required attribution/acknowledgments; do not overwrite source credits.

### Layer and source selection
- **Feature services**: Query the layer endpoint (`FeatureServer/<layerId>`) with REST JS. Parse with `EsriJSON`/`GeoJSON` and add to `VectorSource`. Set read options `dataProjection` to response CRS and `featureProjection` to view CRS. Use `bbox` from `ol/loadingstrategy.js` for viewport loading; assign stable feature IDs from service object IDs to avoid duplicates. On loader failure, `removeLoadedExtent(extent)` permits reloading but does not trigger it; retry on a later load cycle or deliberate trigger, with bounded retries.
- **Feature styling**: Inspect layer metadata (`drawingInfo.renderer`); translate relevant symbols, unique-value/class-break rules, and scale limits into OpenLayers styles. Keep legends consistent with rendered symbols. Report unsupported renderer details rather than claiming faithful reproduction.
- **Editing**: Check capability/privileges. Submit ArcGIS geometry/attributes, not OpenLayers feature objects, with REST JS `applyEdits`. Inspect each add/update/delete result; a resolved request can contain failed edits. Update/refresh only successful edits and surface failures.
- **Vector tiles**: `VectorTileLayer` + `VectorTileSource` (`ol/format/MVT`) for large data/hit detection. Use `ol-mapbox-style` with the service's style JSON for published styling, or explicit OpenLayers styles for intentional overrides. Attributes vary by tile/zoom; use feature services for full queries/edits.
- **Cached tiles**: `TileLayer` + `XYZ` with `/MapServer/tile/{z}/{y}/{x}`. Inspect `tileInfo` and the service spatial reference; verify tile size, origin, resolutions, and level IDs before assuming a standard XYZ grid. Configure a matching tile grid and level mapping when needed. For canvas export set `crossOrigin: "anonymous"` and verify service CORS; the option alone is insufficient.
- **Dynamic map services**: Use `ImageLayer` + `ImageArcGISRest` or `TileLayer` + `TileArcGISRest` for exported `MapServer` images.
- **Popups**: Treat attributes as untrusted. Prefer DOM `textContent`; sanitize any HTML.

### Coordinate systems and geometry handling

- OpenLayers’ default view projection is Web Mercator (`EPSG:3857`). Many ArcGIS location-service examples use WGS 84 (`EPSG:4326`) coordinates in `[longitude, latitude]` order, but supported input and output spatial references vary by service and operation. Check the service requirements, and use `fromLonLat` / `toLonLat` when converting between geographic coordinates and the map view projection. For non-default views, register unsupported projections as needed and pass the actual view projection to `fromLonLat`/`toLonLat` and `ol/sphere` measurements.
- Set query `inSR` to the input geometry's spatial reference and `outSR` to the requested output CRS; do not hardcode 3857 for non-Web-Mercator views.
- Match response format (`EsriJSON`/`GeoJSON`); set reader `dataProjection` and `featureProjection`.
- Use `ol/sphere` for real-world distance/area; Web Mercator planar measurements distort, especially at high latitudes.

### Queries, pagination, and performance
- Check `?f=pjson` for `maxRecordCount` and capabilities.
- On `exceededTransferLimit`, use `resultOffset`/`resultRecordCount` only if supported, with stable ordering where supported; otherwise retrieve object IDs and query them in batches. See [Query docs](https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/).
- Request needed `outFields`; set `returnGeometry: false` for attribute-only queries.
- For large datasets, limit request concurrency and query at useful zoom levels. `bbox` loading retains features as users pan; choose bounded caching or viewport replacement. Keep loaded-extent bookkeeping consistent with feature eviction so revisiting an area reloads missing data.
- Build `where` clauses from known fields and validated/escaped values, never raw user input.
- Restrict popup hit tests with `layerFilter` in `forEachFeatureAtPixel`.
- Debounce geocoding; prevent stale results. Show loading/empty/error states; don't treat failures as empty data.

### Framework lifecycle and resilience
- In React/Vue/Angular, initialize in lifecycle hooks (`useEffect`, `onMounted`, `ngAfterViewInit`) after DOM mount; keep map in a ref/service, not reactive state.
- On unmount, `unByKey` listeners, remove controls/overlays, cancel pending work/observers, and call `map.setTarget(undefined)` to detach the map. Ignore late async results after teardown.
- Call `map.updateSize()` when the container resizes or becomes visible.
- Handle rejected requests and source load errors (`tileloaderror`, `imageloaderror`, `featuresloaderror`); make errors actionable without exposing tokens.
- Require labeled controls, keyboard access, accessible status messages, touch-friendly layouts, and an alternative list/table for important results.
- Give the map container a definite height and verify the rendered viewport is nonzero.

## Validation process

- [ ] Compatible packages install and build.
- [ ] CSS/container dimensions are set; map renders without layout collapse.
- [ ] Auth succeeds without client secrets in browser code.
- [ ] Basemap/layers render with required Esri and data credits.
- [ ] Feature styles and legends match intended renderer rules; unsupported details are documented.
- [ ] Queries use correct `inSR`/`outSR`, request needed data, handle limits, and render correctly.
- [ ] Repeated panning keeps requests/features bounded; evicted areas reload and failed loads can be retried.
- [ ] Interactions handle empty/error results, partial edit failures, and stale responses without unsafe HTML or unhandled rejections.
- [ ] Teardown removes listeners, detaches map, and handles `updateSize()`.
- [ ] Controls/results work with keyboard and touch, status messages are accessible, and layouts adapt to small screens.
- [ ] Browser smoke test covers rendering, service requests, interactions, resizing, and teardown; check console/network errors. If browser testing is unavailable, report what remains unverified.
