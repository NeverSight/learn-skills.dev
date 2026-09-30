---
name: geo-data-engineering
description: >-
  Always invoke when geospatial data must be acquired, prepared, repaired,
  scaled, or moved through a repeatable pipeline. Covers open-data/OSM/STAC
  acquisition, spatial formats, CRS transforms, quality checks, and batch ETL
  architecture for growing or recurring joins. Invoke alongside PostGIS for
  database execution and alongside SWE standards when code is delivered. Do
  not trigger merely because another specialist reads analysis-ready data.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Geospatial Data Engineering

Purpose: get spatial data into a clean, validated, analysis-ready state with
a repeatable pipeline — the stage where most real-world GIS time is spent
and most silent errors are born.

## Format selection

| Format | Use for | Avoid because |
|---|---|---|
| **GeoParquet** | Analysis interchange, big vector, columnar workflows | Not yet readable by some legacy desktop GIS |
| **GeoPackage** | Desktop GIS exchange, multi-layer projects | Slower than Parquet at scale; SQLite locking |
| **FlatGeobuf** | Streaming, HTTP range reads | Single layer |
| **COG** (Cloud-Optimized GeoTIFF) | All raster deliverables | — (make every GeoTIFF a COG) |
| **Zarr/NetCDF** | Multi-dimensional (time × band × y × x) | Overkill for single rasters |
| Shapefile | Only when a legacy tool demands it | 10-char columns, 2 GB cap, encoding chaos, multi-file fragility |
| CSV + WKT/lon-lat | Simple point exchange | No CRS metadata — document it explicitly |

## Acquisition playbook

- **OpenStreetMap**: small areas → `osmnx`; large extracts → Geofabrik PBF +
  `pyrosm`/`osmium`. Respect tag heterogeneity: always inspect tag value
  distributions before filtering.
- **Buildings/places at scale**: Overture Maps (GeoParquet on S3/Azure,
  query with DuckDB spatial — often the fastest path).
- **Satellite/raster**: STAC APIs via `pystac-client` + `odc-stac` — see
  `remote-sensing-analysis`; planetary archives → `google-earth-engine`.
- **Boundaries**: authoritative national source first; Natural Earth / GADM /
  geoBoundaries for global work — record which, versions differ materially.
- Record every acquisition: source URL, query parameters, retrieval date,
  license. Put it in a `DATA_SOURCES.md` next to the data.

## CRS engineering

- Store in EPSG:4326 or source CRS; **analyze** in a projected CRS suited to
  the extent: local UTM zone (`gdf.estimate_utm_crs()`), national grid, or
  equal-area (EPSG:6933/Mollweide) for cross-region area stats.
- Datum shifts matter at sub-meter precision: transformations between datums
  need the right transformation grid (`pyproj.network.set_network_enabled(True)`
  when accuracy matters).
- Never strip or overwrite a CRS to "fix" misaligned layers — diagnose which
  layer is wrong with a known landmark instead.

## Cleaning pipeline

Run `scripts/clean_vector.py` (or import its `clean_vector()` function) as
the standard hygiene pass: drops empty/null geometries, repairs invalid ones
with `make_valid`, de-duplicates, reprojects, and **prints an accounting
report** so silent data loss is impossible.

Then: normalize text attributes (trim, collapse whitespace, locale-aware
casefold — beware Turkish İ/ı, German ß), coerce dtypes explicitly, and show
`value_counts()` of every categorical you will later filter on.

## Scale strategies

- **Fits in RAM**: GeoPandas + Shapely 2 vectorized ops. Ensure the spatial
  index is used (`sjoin`, `query_bulk`) — hand-rolled loops are O(n²).
- **Bigger than RAM, single machine**: DuckDB `spatial` extension over
  GeoParquet (predicate pushdown + spatial SQL), or `dask-geopandas`.
- **Served / concurrent / transactional**: PostGIS — see `postgis-spatial-sql`.
- Rasters: windowed reads (`rasterio.windows`), chunked xarray + dask;
  never `read()` a 50 GB mosaic into memory.

## Pipeline standards

- Idempotent steps with explicit inputs/outputs on disk; re-running never
  corrupts state.
- Checkpoint after expensive stages (download, big join) in GeoParquet/GPKG.
- Log an accounting line per stage: rows/features/pixels in → out.
- Deterministic ordering before writing (sort by stable key) so diffs are
  meaningful.

## Pitfalls checklist

- CSV opened without declaring lon/lat columns' CRS.
- Shapefile column names silently truncated on export.
- Encoding mojibake from legacy files (try `encoding="utf-8"` then cp1252).
- Mixed geometry types in one layer (Polygon + MultiPolygon breaks some
  tools — normalize with `.explode()` or promote to Multi*).
- Antimeridian and pole-crossing geometries after naive reprojection.
- Downloaded "latest" data with no recorded version/date — unreproducible.

## Execution contract

- **Workflow:** inventory sources and contracts; acquire with provenance; inspect CRS, schema, geometry, and scale; clean deterministically; validate; write an analysis-ready artifact.
- **Decision rules:** select formats and engines from size, geometry, concurrency, and downstream access needs; never infer CRS or destructive repairs silently.
- **Verification protocol:** reconcile feature or pixel counts at every stage, assert CRS and geometry invariants, sample outputs spatially, and rerun to confirm idempotence.
- **Failure modes:** quarantine ambiguous CRS, mixed units, invalid encodings, lossy format conversions, or unexplained row loss instead of guessing.
- **Deliverables:** validated dataset, machine-readable schema and CRS, provenance manifest, accounting log, rejected-record report, and reproducible pipeline.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before using version-sensitive formats or APIs and record the checked date.
