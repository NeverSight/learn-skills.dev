---
name: geoai-orchestrator
description: >-
  Route genuinely ambiguous or multi-stage geospatial work across specialist
  skills while enforcing shared CRS, validity, leakage, units, verification,
  and reproducibility rules. Use for requests spanning multiple stages such as
  acquisition, imagery, modeling, analysis, and map delivery, or for an
  explicit end-to-end pipeline. Never invoke for one domain merely because a
  parameter is unclear. Code implementation/review, backend or platform
  choice, and production-readiness review are direct specialist tasks. Do not
  add this skill as a layer around one specialist.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# GeoAI Orchestrator

The hub of an 18-skill geospatial module. Activate it for routing or pipeline
composition, not as a mandatory wrapper around every spatial task. Its job:
(1) diagnose what kind of
spatial problem the user actually has, (2) design the pipeline across
stages, (3) route each stage to the right specialist skill, and (4) enforce
the module-wide invariants that every stage must obey.

## Routing gate — read before producing any output

This orchestrator routes by **invoking**, never by naming. The gate below
overrides every other section of this document, including the pipeline
template.

1. **Invoke, do not list.** Every specialist you select must be invoked with
   the `Skill` tool in the same response that selects it. Naming a skill in a
   table, plan, or prose sentence is not a handoff. A response that identifies
   the right specialist but does not invoke it has failed this skill's core
   function, no matter how accurate the diagnosis is.
2. **Route every correction, not the first one.** When a request contains
   multiple findings, defects, or stages, each one gets its own routing
   decision and its own invocation. Routing one item and handling the rest
   inline is a partial failure; the count of routed items must equal the count
   of items found.
3. **Never make routing conditional on permission.** Do not write "say the
   word and I'll route", "I can hand this off if you want", "let me know and
   I'll bring in the specialist", or any equivalent. Offering to route later is
   the single most common failure of this skill. If you have identified the
   specialist, invoke it now.
4. **Clarification is not a substitute for routing.** Missing detail about
   *scope* (which deliverable, which study area) does not block routing of the
   stages you have already identified. Ask the scope question and route in the
   same response. Only a request whose entire domain is undetermined may be
   routed-free, and then you must say which specialist becomes available under
   each candidate answer.
5. **Audit requests are `deliver` requests.** "Audit this plan", "review this
   pipeline", "what is wrong with this workflow" require the completed audit,
   the routed corrections, and the revised plan in one response. Do not return
   findings and hold the corrections back for a follow-up turn.

If you cannot satisfy the gate, do not activate this skill — route the request
directly to the single narrowest specialist instead.

## Module map — route by problem type

| Stage / problem | Specialist skill |
|---|---|
| Data acquisition, formats, CRS, tiling, pipelines | `geo-data-engineering` |
| Satellite/aerial imagery, spectral indices, classification | `remote-sensing-analysis` |
| Planetary-scale archives, GEE Python API, cloud compositing | `google-earth-engine` |
| CNN/U-Net/ViT on EO data, segmentation, detection | `geo-deep-learning` |
| Autocorrelation, hotspots, clusters, spatial regression | `spatial-statistics` |
| Site selection, suitability, AHP/weighted overlay | `mcda-suitability-analysis` |
| Interpolation from point samples, kriging, variograms | `geostatistics-interpolation` |
| DEM, slope, watersheds, flow, viewshed | `terrain-hydrology` |
| LiDAR / point clouds, DTM/DSM/CHM, PDAL | `point-cloud-lidar` |
| Routing, service areas, accessibility, OD matrices | `network-accessibility-analysis` |
| GPS tracks, trajectories, stops/trips, map matching | `movement-trajectory` |
| Multi-temporal comparison, land cover change, trends | `change-detection` |
| Map design, choropleths, web maps, publication figures | `cartography-geoviz` |
| Spatial SQL, PostGIS, large-scale spatial joins | `postgis-spatial-sql` |
| Local ArcGIS Pro, ArcPy, `.aprx`, or `.gdb` execution | `arcgis-pro-automation` |

This table selects specialists; it does not hand off to them. Every row you
select must be invoked under the routing gate. For cross-cutting method
standards (leakage, metrics, reproducibility), invoke `ml-experiment-standards`
and `swe-devops-standards` when their rules apply.

## Pipeline design protocol

For any multi-stage request, produce a short pipeline plan BEFORE writing
code, then invoke the specialists that plan names in the same response:

```
## Pipeline: <goal>
1. <stage> → <skill> → output: <artifact> → check: <verification criterion>
2. ...
Success criterion: <what the user can inspect to accept the result>
```

The plan is a routing manifest, not a proposal awaiting approval. Publishing
the plan and stopping there is the failure mode this skill exists to prevent.
Do not wait for confirmation before routing; confirmation is only ever sought
for *scope* (which deliverable, which extent, which decision), and it is
requested alongside the routed stages, never instead of them.

Every stage ends with a verification criterion. Spatial work fails silently
(wrong CRS, empty joins, inverted axes produce plausible-looking garbage),
so a stage without a check is not a stage.

## Module-wide invariants (enforced in every stage)

1. **CRS is explicit, always.** Report the CRS of every input on first
   contact. Never compute area/distance/buffer in a geographic (degree)
   CRS — reproject to an appropriate projected CRS (local UTM zone by
   default via `gdf.estimate_utm_crs()`; equal-area such as EPSG:6933 for
   global area statistics). If a CRS is undefined, stop and resolve it;
   never guess silently.
2. **Axis order discipline.** GeoJSON is lon/lat; many APIs and humans say
   lat/lon. Verify with a known landmark before pipeline-scale processing.
3. **Geometry validity before analysis.** Check `is_valid`; repair with
   `shapely.make_valid` (not `buffer(0)`, which can silently drop parts).
4. **Row-count accounting.** After every join/overlay/filter, report rows
   in vs rows out. Silent duplication or loss is the top geospatial bug.
5. **Spatial autocorrelation awareness.** Random train/test splits on
   spatial data leak. Any ML stage follows the canonical protocol in
   `ml-experiment-standards` → `references/spatial-cv-protocol.md`.
6. **Units in column names.** `area_ha`, `dist_km`, `elev_m` — never bare
   `area`. Unit confusion survives code review; column names don't lie.
7. **Visual + numeric verification.** Every spatial output gets both a
   summary table AND a quick map check (`.explore()`, a PNG, or GIS
   software). A confusion matrix cannot show spatially clustered errors.
8. **Reproducibility.** Pin package versions, seed randomness, log
   parameters. Intermediate artifacts go to GeoPackage or GeoParquet, never
   shapefile (10-char column truncation, 2 GB limit, no proper encoding).

## Internationalization note

Attribute tables in non-ASCII locales break naive string handling.
Canonical example: Turkish dotted/dotless I — `'İ'.lower()` yields a
2-character string in Python. Before any string matching on attributes,
apply a locale-aware normalization step and show `value_counts()` of
cleaned categorical fields. Prefer UTF-8 formats; legacy shapefiles may
carry cp1252/cp125x mojibake silently.

## Choosing the stack

Default to the open Python stack: GeoPandas + Shapely 2 + Rasterio +
xarray/rioxarray + PyProj. Route to PostGIS when data exceeds comfortable
memory (~millions of features) or needs concurrent/repeated querying; to
Earth Engine when the data is a planetary archive rather than local files.
Use GDAL CLI for bulk format conversion. If the user works in ArcGIS Pro or
QGIS, generate headless-runnable scripts (arcpy / PyQGIS) rather than click
instructions, and keep the analysis logic portable.

## Anti-patterns to catch early

- Buffering in degrees ("0.01 degree buffer") — reproject first.
- `EPSG:4326 → Web Mercator` area statistics — Mercator distorts area
  massively away from the equator.
- Joining datasets from different CRS without alignment.
- Treating a DEM's nodata value (-9999, 3.4e38) as real elevation.
- Classifying imagery without checking cloud/shadow masks.
- Reporting model accuracy without a spatially independent test set.

## Execution contract

- **Workflow:** clarify objective and deliverable; decompose the multi-stage problem; route each stage to the narrowest skill by invoking it with the `Skill` tool; declare handoffs and invariants; integrate and verify the final artifact.
- **Decision rules:** invoke this orchestrator only for ambiguous or cross-domain work; route a single well-scoped task directly to its specialist skill.
- **Verification protocol:** require stage-level acceptance checks, count and CRS handoff assertions, end-to-end provenance, and final-product review against the original question. Before returning, confirm that every specialist named in the response was actually invoked and that the number of routed corrections equals the number of findings.
- **Failure modes:** pause when ownership, units, CRS, temporal alignment, evidence standards, or stage interfaces remain ambiguous; never hide unresolved specialist failures. Never substitute an offer to route for an invocation, and never defer routed corrections to a later turn.
- **Deliverables:** pipeline plan, skill-routing table, stage inputs and outputs, verification gates, risk register, and final integration checklist.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) and the selected specialists' registries before fixing interfaces.
