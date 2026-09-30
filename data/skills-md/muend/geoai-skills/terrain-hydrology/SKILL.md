---
name: terrain-hydrology
description: >-
  Always invoke for terrain, drainage, viewshed, or visibility analysis from
  elevation, even before the DEM or correct surface is chosen. Covers
  DTM-versus-DSM selection, slope, aspect, curvature, hillshade, conditioning,
  flow direction/accumulation, streams, watersheds, and catchments. Use
  point-cloud-lidar first only when an elevation surface must be created from
  LiDAR or photogrammetric points.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Terrain & Hydrology

Purpose: terrain products whose numbers are physically meaningful. The two
recurring failure modes: **unit mismatch** (degree coordinates with meter
elevations silently corrupts every derivative) and **unconditioned DEMs**
(flow routed into spurious pits produces fragmented, fictional streams).

## DEM hygiene first

| Check | Rule |
|---|---|
| Surface type | **DTM** (bare earth) for hydrology/slope; **DSM** (with canopy/buildings) for viewshed/solar. Using a DSM for watersheds routes rivers over treetops. |
| Source | Copernicus GLO-30 > SRTM for most global work; national LiDAR DTMs when available (see `point-cloud-lidar` to make your own). Record source + acquisition date. |
| Nodata | Identify the nodata value (-9999, -32768, 3.4e38) and mask it — never let it enter statistics or fill algorithms as "very deep hole". |
| Voids | Fill data voids (interpolation from edges) BEFORE hydrological conditioning; document filled areas. |
| **CRS + units** | Reproject to a projected CRS so horizontal units = vertical units (meters). Slope from a 4326 DEM without z-factor correction is the classic silent error. If staying geographic, apply a latitude-dependent z-factor — better: don't. |

## Derivatives

```python
import whitebox
wbt = whitebox.WhiteboxTools()
wbt.slope("dem.tif", "slope_deg.tif", units="degrees")
wbt.aspect("dem.tif", "aspect_deg.tif")
wbt.plan_curvature("dem.tif", "plan_curv.tif")
```

- Slope: state units (degrees vs percent — 45° = 100%); Horn's method
  (3×3) is the standard; steeper terrain → consider resolution effects
  (slope flattens as cell size grows — report cell size with every slope
  statistic).
- Aspect: circular variable — never average it arithmetically; use vector
  (sin/cos) averaging; flat cells have undefined aspect (mask, don't zero).
- Curvature: plan (flow convergence) vs profile (flow acceleration) —
  pick per question.
- Hillshade is for cartography (see `cartography-geoviz`), never analysis
  input.
- Ruggedness/position: TRI, TPI (radius-dependent — report the radius),
  geomorphons for landform classification.

## Hydrological conditioning — order matters

```
voids filled → breach depressions (preferred) → fill remaining pits
→ flow direction → flow accumulation → streams → watersheds
```

- **Breaching before filling** (WhiteboxTools
  `BreachDepressionsLeastCost`): carves through barriers (road embankments
  over culverts) instead of flooding upstream areas flat. Pure fill on
  flat/embanked terrain creates large artificial lakes with arbitrary flow
  paths.
- Real depressions exist (karst, prairie potholes, reservoirs). If the
  landscape genuinely holds water, don't condition it away — model with
  explicit sink handling and say so.
- Flow direction: **D8** for stream networks/watersheds (discrete,
  standard); **D-infinity/MFD** for dispersal quantities (wetness index,
  erosion) on hillslopes.

## Streams and watersheds

- Stream extraction threshold (min. accumulation) is a MODELING choice:
  derive from a mapped reference network (match total stream length) or
  report the threshold and show two alternatives — never present one
  threshold's network as "the" rivers.
- **Pour point snapping**: outlet coordinates rarely fall on the modeled
  stream cell. Snap to the highest-accumulation cell within a search
  radius (`wbt.jenson_snap_pour_points`) — an unsnapped pour point yields
  a tiny, wrong watershed silently.
- Verify delineation: watershed area vs authoritative basin data (±5-10%),
  and the modeled network overlaid on imagery/topo maps at 3 locations.
- Wetness index (TWI), stream power (SPA): compute from conditioned DEM +
  MFD accumulation; they are relative indices — don't read absolute
  thresholds across regions.

## Viewshed

- Use a **DSM** (or DTM + feature heights) — bare-earth viewsheds
  overstate visibility wherever trees/buildings exist; state which surface
  was used.
- Set observer height (~1.7 m person, tower height for infrastructure) and
  target height explicitly; defaults differ across tools.
- Account for earth curvature + refraction beyond ~5 km
  (`wbt.viewshed` handles it; verify the flag).
- Deliver binary visible/not plus the observer point(s) and parameters in
  the metadata; for siting problems, cumulative viewsheds from candidate
  sets feed `mcda-suitability-analysis`.

## Tooling

WhiteboxTools (conditioning, full hydrology suite, fast) · `pysheds`
(lightweight Python watersheds) · `richdem` (derivatives) · GDAL
(`gdaldem`) for quick slope/hillshade · GRASS (`r.watershed`) for very
large DEMs (no explicit fill needed — least-cost routing).

## Verification protocol

1. Derivative histograms: slope > 60° over large areas or negative
   accumulation = unit/nodata bug.
2. Stream network overlay on imagery at 3 locations, including one flat
   area (where artifacts concentrate).
3. Watershed area cross-check vs authoritative basin polygons.
4. Report: DEM source/date/resolution, conditioning method, flow
   algorithm, stream threshold, all in the deliverable.

## Pitfalls checklist

- Slope from a geographic-CRS DEM without z-factor (values ~100× off).
- DSM used for watershed delineation (rivers over treetops).
- Fill-only conditioning across road embankments → phantom lakes.
- Unsnapped pour point → 3-cell "watershed".
- Arithmetic mean of aspect (350° and 10° average to south, not north).
- Nodata treated as elevation in fill/statistics.
- One arbitrary stream threshold presented as the drainage network.

## Execution contract

- **Workflow:** inspect DEM source, CRS, vertical units, datum, resolution, and nodata; condition terrain; derive gradients and flow; delineate products; test thresholds; validate against imagery and controls.
- **Decision rules:** use terrain workflows on raster elevation products, point-cloud workflows before DEM generation, and choose conditioning and flow algorithms from landscape and scale.
- **Verification protocol:** inspect derivative distributions, hillshade artifacts, stream overlays, watershed area, pour-point snapping, threshold sensitivity, and elevation-control residuals.
- **Failure modes:** reject products from DSM misuse, geographic-unit slope, vertical datum mismatch, unconditioned barriers, nodata contamination, unsnapped outlets, or resolution unsupported by source data.
- **Deliverables:** conditioned DEM, derivatives and hydrologic products, parameter and threshold record, CRS and vertical datum, QA maps, validation metrics, and limitations.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before applying tool algorithms or product rules and record the checked date.
