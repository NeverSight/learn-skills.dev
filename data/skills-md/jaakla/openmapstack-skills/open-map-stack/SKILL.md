---
name: open-map-stack
description: "Plan and execute ambiguous or multi-stage GIS work, jointly choosing authoritative sources, compute, storage and delivery for the scale and team. Covers vector/raster/point-cloud analysis, routing, QGIS, tiles and web maps. Use for unresolved geospatial architecture and end-to-end analysis; prefer installed geospatial-data-discovery, spatial-sql or reproducible-gis-project for their bounded tasks. Retains standalone GIS support when specialists are absent. Do not use for casual place lookups, ordinary travel directions or non-spatial coding."
metadata:
  version: "0.4.0"
---

# OpenMapStack Toolkit

Production-grade geospatial workflows with an open-first stack and pragmatic hosted/SaaS choices when global scale, latency, SLA, or data quality makes local processing a poor fit. Cloud-native by default: STAC for discovery, GeoParquet + COG + PMTiles for storage, DuckDB and PostGIS for compute, MapLibre and Martin for delivery.

## Choose a primary skill

Keep coupled source, compute, storage and delivery decisions together. Prefer
one primary skill, with focused support only where the task needs it:

| Request | Primary skill when installed |
|---|---|
| Unresolved architecture, changing scale/team needs, or end-to-end GIS analysis | `open-map-stack` |
| Compile or maintain a reproducible project from a chosen workflow | `reproducible-gis-project` |
| Find and assess data against known requirements, including Portolan catalogs | `geospatial-data-discovery` |
| Write/review/debug spatial SQL on an already chosen engine | `spatial-sql` |

If a specialist is absent, use this skill's local references for the bounded
task. Do not require an installation or activate every skill. Material analyses
retain the complete project contract below, including in a generalist-only
install. Product-specific help follows `references/companion-skills.md`;
OpenMapStack retains GIS semantics and cross-stage correctness.

## Reproducible project-first contract

For every material multi-stage GIS analysis, compile or maintain a deterministic,
inspectable, reproducible technical project before delivery. A map, dashboard or
report is a view over that project, not the canonical definition of the analysis.

**Before compiling or delivering a material analysis, read
`references/project-workflow.md` for the mandatory workflow and delivery rules,
and `references/project-spec.md` for the full `openmapstack-project/v1` schema.**
Use `templates/` and the worked `examples/tartu-development` project.
For CLI installation and the example's runtime requirements, read
`references/installation.md`.

Keep authoritative sources real, immutable and pinned; never invent baseline
geometry without explicit informed consent. Record assumptions and every manual
correction as data or canonical pipeline logic, make overrides executable and
verified, and preserve unknown semantic attributes as unknown. The project must
have explicit CRS, deterministic ordered steps, machine-readable validation and
run evidence, provenance, and a documented clean rerun without chat dependencies.
Check whether the CLI is installed (`openmapstack --version` or
`python3 -m openmapstack --version`, then use whichever form works for every
command below); if it is, run `openmapstack validate` and the
canonical `openmapstack run` path, then `openmapstack verify project.yaml --rerun`,
which rebuilds the project from its declared inputs in an empty workspace.
Make that `verify --rerun` your last step and do not deliver until it passes;
a passing `validate` alone is not enough. The canonical pipeline must produce
every file under `data/derived`, every selected deliverable, the run record, and the
manifest's `runs.latest` and `project.status`, never a one-off script or a
hand edit: a rerun writes a new run record, so a hand-patched pointer breaks it. Missing
validation capability is `not_testable`, never an implicit pass. Generate durable
Markdown findings from pipeline results. Follow the referenced workflow's
presentation obligations for the selected targets.
Declare the real author and toolkit; render linked credits with the canonical
run time in every delivered view (see the workflow's credits requirement).
Review the required attribution prose too; field checks cannot certify its meaning.
Record `delivery.schema: openmapstack-delivery/v1` for new projects, defaulting
to the built-in dashboard. Respect explicit external-only or combined delivery;
QGIS and Observable are optional targets. Existing manifests without `delivery`
retain legacy v1 behavior until explicitly migrated. Source provenance, GIS
correctness and clean reruns are required for every selection.

For dashboard basemaps, honor user choices and appropriate local/regional services; otherwise use the preconfigured goplex.ee Protomaps fallback in `references/web-delivery.md`, with light/dark switching and visible provider attribution.

For a bounded one-shot SQL, CRS or conversion question, the relevant domain
reference is sufficient; a full project artifact and its methodology are not needed.

When the user has dlt, Dagster, dbt, QGIS or Observable in their stack, read
`references/established-stack.md` for ownership and integration boundaries.
Preserve their chosen tools; retain source pins, GIS correctness and reproducible
evidence. Do not duplicate their SQL, ingestion or scheduler definitions.

## Modules — read the relevant reference(s) before starting work

| If the task involves... | Read |
|---|---|
| Finding or sourcing data (OSM, Overture, Sentinel, Landsat, building footprints, regional portals, STAC and Portolan catalogs, MCP-based discovery) | `references/data-sources.md` |
| Reading the user's own warehouse or database (PostGIS, BigQuery, MotherDuck, DuckDB, GeoParquet directories): credentials by reference, read-only discovery, approved snapshots, pin classes | `references/user-data-sources.md` |
| Choosing local processing vs online/hosted/SaaS services for global or continental scale; basemaps, elevation, routing, geocoding, place search, postcode lookup APIs | `references/services-and-scale.md` |
| Choosing a format, converting between formats, or any CRS / projection / EPSG question | `references/formats-and-crs.md` |
| Compiling a reproducible GIS project artifact (`project.yaml`, pipeline, overrides, validation, presentation) | `references/project-spec.md` + `templates/` |
| Running GDAL/OGR, GeoPandas, xarray, DuckDB, PostGIS, or PDAL — the actual processing | `references/processing.md` |
| Writing or reviewing spatial SQL / GeoSQL in DuckDB Spatial, PostGIS, BigQuery GIS, Snowflake, or Sedona | `references/spatial-sql.md` |
| Vector analytics, raster analytics, terrain/hydrology, network analysis, point cloud workflows | `references/analytics.md` |
| Tile generation (PMTiles, MVT), tile servers (Martin, TiTiler), delivered rendering (MapLibre, deck.gl), or exploration rendering (kepler.gl, lonboard) | `references/web-delivery.md` |
| Designing a project's dashboard or report pages: archetypes, components, tokens and the state hooks the checks use | `references/design-language.md` |
| QGIS desktop, QGIS plugin ecosystem, QGIS MCP, PyQGIS scripting, Processing toolbox | `references/qgis.md` |
| Reproducibility, validation, license attribution, tile smoke tests, deployment checks | `references/validation-and-ops.md` |

For simple one-shot questions (single CRS conversion, one `ogr2ogr` invocation), the relevant reference alone is sufficient — a full project artifact is not needed. For multi-stage pipelines, read `data-sources.md` and `processing.md` together, and see `project-spec.md` + `templates/` to compile analysis into a rerunnable project. For end-to-end "from raw data to web map" tasks, also read `web-delivery.md`.

## Global defaults — apply unless the user specifies otherwise

* **Storage formats:** GeoParquet (vector analytics), COG (raster), PMTiles (tile delivery), GeoPackage (desktop interchange). Never produce Shapefile as new output.
* **CRS:** WGS84 (EPSG:4326) for storage; Web Mercator (EPSG:3857) for web rendering; local projected CRS for any metric computation (distance, area, buffer). For Estonia, EPSG:3301 (L-EST97).
  For DuckDB, set connection axis order explicitly before reprojection or GDAL I/O (normally `geometry_always_xy = true`); keep `always_xy := true` on `ST_Transform` to make the x/y contract explicit. See `references/spatial-sql.md` for setup. Before delivery, check a transformed feature against its source and a known location; a correct CRS label does not prove correct coordinates. See `references/formats-and-crs.md`.
* **Coordinate order:** treat it as an interface contract, not a CRS guess. Internally prefer GIS `x,y` (`lon,lat` for geographic coordinates), but obey each external format/API contract; GeoJSON, MapLibre `LngLatLike`, and OpenLayers geographic arrays use `lon,lat`, while Leaflet `LatLng` and Google Maps `LatLng` use `lat,lng`. Never infer tuple order from `EPSG:4326` alone. See `references/formats-and-crs.md`.
* **Layer placement:** declare the area of interest (`project.aoi`) and, after loading and after each reprojection, check that every local layer lies inside it. A layer far outside a city or country AOI signals an axis swap, a wrong CRS label or a wrong-area filter; report it, and fix it only with source evidence.
* **Compute placement:** push spatial joins and aggregations to DuckDB or PostGIS — not Python loops. R-tree / GIST / spatial indexing is mandatory at scale.
* **Discovery first:** check STAC catalogs (Microsoft Planetary Computer, Earth Search, Overture STAC) before downloading anything. Lazy load with `odc-stac` or `stackstac` and only materialize what's needed.
* **Cloud-native access:** prefer querying remote GeoParquet/COG over downloading. DuckDB with `httpfs` extension is the default pattern for Overture and similar S3-hosted datasets.
* **Scale first:** local tools are fine for city/state work; at continental/global scale prefer cloud-native partitioned datasets, precomputed tiles, hosted APIs, or SaaS when they are more reliable than local batch processing.
* **License hygiene:** preserve license metadata through every transformation. OSM is ODbL (share-alike); Overture varies by source; Sentinel is free-with-attribution; national data varies.
* **Runtime hygiene:** prefer `conda-forge` environments or containers for GDAL/PROJ/GEOS/QGIS stacks. Avoid pip-only geospatial environments unless the project already proves they work.

## Format decision matrix

| Use case | Format |
|---|---|
| Cloud analytics on vector | GeoParquet |
| Streaming vector over HTTP | FlatGeobuf |
| Desktop interchange | GeoPackage |
| Web map vector tiles | PMTiles (containing MVT) |
| Raster archive / serving | COG |
| n-dimensional raster (time series, climate) | Zarr or NetCDF |
| Point cloud archive | COPC (cloud-optimized LAZ) |
| API response payload (small only) | GeoJSON |
| Legacy compatibility (input only) | Shapefile |

## Compute decision matrix

| Scale / context | Use |
|---|---|
| < 50M features, single machine, ad-hoc | DuckDB Spatial |
| Multi-user, web app backend, OLTP | PostGIS |
| > 100M features, distributed | Apache Sedona |
| Continental/global lookup/search/routing/elevation | Hosted API or SaaS where coverage, SLA, terms, and price fit |
| Planet-scale basemap delivery | Prebuilt PMTiles/vector tiles or managed basemap service |
| n-dim raster, lazy/dask-backed | xarray + rioxarray (+ odc-stac for STAC ingest) |
| CLI batch jobs on raster | GDAL utilities (`gdalwarp`, `gdal_translate -of COG`) |
| Point clouds | PDAL pipelines |
| Terrain & hydrology beyond `gdaldem` | WhiteboxTools or GRASS |
| Desktop styling, cartography, ad-hoc exploration | QGIS (see `qgis.md`) |

## Universal anti-patterns — flag and correct

* Hallucinating or fabricating mock coordinates and geometries instead of retrieving real source data (unless the user gave explicit, informed consent for a synthetic mock test)
* Generating a selected QGIS project that disagrees with the shared presentation layers, omits basemaps, or uses broken OGR datasource syntax (`path.gpkg|layer` without `layername=`), causing layers to load as non-spatial attribute tables
* Writing `.qgs` XML by hand with no `<srs>`, an auth-id-only CRS block, or no `ProjectionsEnabled`, or copying the manifest's layer order straight into the layer tree — these produce a project where every layer is valid and every datasource resolves, yet the map shows the wrong place or silently hides a layer
* Producing Shapefile as new output (column truncation, 2GB limit, no UTF-8, multi-file)
* Calling `.distance()`, `.buffer()`, or `.area` on geographic CRS (EPSG:4326) — degrees are not meters; unless specific tool explicitly supports wgs84 based geodesic calculations
* Treating Web Mercator (EPSG:3857) coordinates as undistorted ground measurements — its coordinate units are metres, but ground-distance and area distortion vary with latitude
* Spatial joins in Python loops when DuckDB / PostGIS / R-tree-backed `sjoin` is one line away
* Using bbox containment for area queries when features can cross the boundary — use bbox overlap as the scan gate, then an exact spatial predicate
* Downloading entire datasets when STAC + cloud-native formats allow lazy/range-request access
* Running planet-scale local processing for lookup/search problems when reliable hosted services or precomputed global products already exist
* Treating MBTiles as the default for new web deployments — PMTiles is the modern default
* Using GeoTIFF when COG is one flag away (`-of COG`)
* Mixing CRS silently — every join must assert matching CRS
* Hand-rolling routing or geocoding when OSRM, Valhalla, or Nominatim are one Docker pull away
* Pinning data to "latest" in a reproducible pipeline — pin Overture release version and STAC item IDs, not just collections. For Overture, verify the pinned release is still available or mirror it.

## Quick triage — recognize the request type

Before diving into a task, classify it:

1. **Discovery** ("what data exists for…?", "is there a dataset of…?", "read this catalog") → start with `data-sources.md`. STAC search if raster; Overture or OSM if vector basemap; for a Portolan catalog read its `AGENTS.md` before querying.
2. **Conversion / CRS** ("convert this to…", "reproject to…", "the projection looks wrong") → `formats-and-crs.md`. Usually one `ogr2ogr` or `gdalwarp` call.
3. **Analysis** ("what's the average elevation in…", "how many buildings within 500m of…", "where are the hotspots?") → `analytics.md` and likely `processing.md`. Push to DuckDB/PostGIS first.
4. **Delivery** ("publish this as a web map", "generate tiles for…") → `web-delivery.md`. PMTiles + Martin + MapLibre is the default.
5. **Desktop / cartography** ("style this in QGIS", "make a print map", "automate this in QGIS") → `qgis.md`. Consider QGIS MCP for agentic workflows.

Most real tasks span 2–3 of these — read the relevant references in order.

## Reproducibility checklist for any pipeline you produce

* Pin dataset versions (Overture release, STAC item IDs, OSM extract dates) — never "latest"
* Document CRS at every stage; never assume
* Use `conda-forge` envs or pinned container images (`ghcr.io/osgeo/gdal:alpine-small-latest` for GDAL, `qgis/qgis:<tag>` for PyQGIS); pip-only geospatial envs break frequently
* Validate outputs: `gpq` for GeoParquet, `rio-cogeo validate` for COG, `pmtiles show` for PMTiles, `is_valid` for geometries
* Preserve license metadata in column or sidecar JSON and carry required attribution into maps/APIs

Command-level detail for each of these lives in `references/validation-and-ops.md`.
