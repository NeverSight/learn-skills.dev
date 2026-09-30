---
name: remote-sensing-analysis
description: >-
  Always invoke for classical analysis, classification, validation, or
  comparability of satellite, aerial, or drone imagery. This skill owns
  sensor, product, processing-level and processing-baseline harmonization,
  including multi-date inputs; add change-detection only after comparable
  observations exist. Two scenes of the same product level are not
  automatically comparable: Sentinel-2 L2A crossed a reflectance offset at
  Processing Baseline 04.00 in January 2022, so any pair spanning that date
  starts here. Covers spectral indices, masking, compositing, SAR, land cover,
  and accuracy assessment. Route neural methods to geo-deep-learning and
  planetary server-side execution to google-earth-engine.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Remote Sensing Analysis

Purpose: turn raw Earth observation imagery into defensible analytical
products. The failure modes here are subtle — uncorrected DNs treated as
reflectance, clouds counted as land cover change, indices computed on the
wrong bands — so this skill front-loads the checks.

## Data access (STAC-first)

Search via STAC APIs rather than per-provider portals; the workflow is
uniform and scriptable:

```python
import pystac_client
import odc.stac

catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")
items = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[27.0, 38.3, 27.4, 38.6],
    datetime="2025-05-01/2025-09-30",
    query={"eo:cloud_cover": {"lt": 20}},
).item_collection()
ds = odc.stac.load(items, bands=["red", "nir", "scl"], resolution=10, chunks={})
```

Key collections: `sentinel-2-l2a` (10 m optical, surface reflectance),
`landsat-c2-l2` (30 m, 1982→), `sentinel-1-grd` (SAR, weather-independent).
Microsoft Planetary Computer mirrors most (needs `planetary_computer`
signing). For continental/global extents or decades-long stacks, route to
`google-earth-engine` instead of downloading. Record collection + item IDs +
search parameters for reproducibility.

## Processing-level discipline

| Level | Meaning | Analysis-ready? |
|---|---|---|
| L1C / L1TP | Top-of-atmosphere (TOA) | Indices OK-ish; cross-date comparison risky |
| **L2A / L2SP** | Surface reflectance (BOA) | Yes — default choice |
| GRD (SAR) | Detected amplitude | Needs terrain correction + speckle filter |

Always state which level you used. Never mix TOA and BOA scenes in one
composite or time series. Landsat Collection 2 L2 needs its scale factors
applied (`reflectance = DN * 0.0000275 - 0.2`).

### The Sentinel-2 baseline discontinuity — passes the level check above

Processing Baseline 04.00, applied from **25 January 2022**, added a constant
`BOA_ADD_OFFSET` (currently −1000) to L2A digital numbers so that negative
surface reflectance can be encoded. Two scenes on opposite sides of that date
are **both L2A**: the level check above sees nothing wrong while their DNs sit
1000 apart. Differencing them yields a systematic reflectance shift that reads
as real change and survives every mask, threshold and accuracy report you
apply afterwards.

- Read `BOA_ADD_OFFSET` and `QUANTIFICATION_VALUE` from each product's
  metadata rather than hardcoding −1000 and 10000; both are per-band and the
  baseline has changed before.
- Convert with `reflectance = (DN + BOA_ADD_OFFSET) / QUANTIFICATION_VALUE`.
- Record the **processing baseline of every scene** in the manifest, not just
  the product level. Two L2A scenes is not a sufficient statement.
- **Do not correct twice.** Harmonised collections — Earth Engine's
  `COPERNICUS/S2_SR_HARMONIZED` and several commercial mirrors — have already
  shifted post-baseline data back to the pre-2022 range. Applying the offset
  again inverts the error rather than removing it.
- If the baseline is undocumented for either scene, the comparison is not
  defensible. Say that instead of assuming pre- or post-2022.

## Cloud and quality masking — before anything else

- Sentinel-2: mask with SCL band (drop classes 3 cloud shadow, 8-9 clouds,
  10 cirrus, 11 snow — keep 4 vegetation, 5 bare, 6 water, 7 unclassified
  with care).
- Landsat C2: decode `QA_PIXEL` bitfields (cloud, shadow, cirrus bits).
- Report the % of valid pixels after masking per scene; scenes below ~60%
  valid usually deserve exclusion.
- For gap-free products, build median composites over a season rather than
  cherry-picking single scenes.

## Spectral indices

Compute on surface reflectance, guard against division by zero, and name
bands explicitly — band **numbers differ across sensors** (NIR is B8 on
Sentinel-2, B5 on Landsat 8/9):

```python
import numpy as np
import xarray as xr

def normalized_diff(a: xr.DataArray, b: xr.DataArray) -> xr.DataArray:
    """(a - b) / (a + b) with zero-denominator protection."""
    return xr.where(a + b == 0, np.nan, (a - b) / (a + b))

ndvi = normalized_diff(ds.nir, ds.red)     # vegetation
ndwi = normalized_diff(ds.green, ds.nir)   # open water (McFeeters)
ndbi = normalized_diff(ds.swir16, ds.nir)  # built-up
```

Interpretation guardrails: NDVI thresholds are scene- and season-dependent;
never hardcode "NDVI > 0.3 = vegetation" without checking the histogram.
Water confuses NDBI; shadows mimic water in NDWI — cross-check indices
against each other and against true-color.

## Classification workflow

1. Define a legend with mutually exclusive, imagery-separable classes.
2. Collect training samples spatially spread across the scene; record them
   as a versioned vector file.
3. Features: bands + indices + texture (GLCM) + temporal statistics if
   multi-date. For deep learning routes, hand off to `geo-deep-learning`.
4. Validate with a **spatially independent** test set (see
   `ml-experiment-standards` → `references/spatial-cv-protocol.md`) and
   report per-class F1/IoU plus a confusion matrix — overall accuracy alone
   hides rare-class failure.
5. Map the errors: a spatial plot of misclassifications reveals systematic
   problems (terrain shadow, urban/bare confusion) that global metrics hide.

## SAR notes (Sentinel-1)

Preprocess: orbit file → thermal noise removal → calibration (σ⁰) →
terrain correction (Range-Doppler with a DEM) → speckle filter (Lee/Refined
Lee) → dB conversion. Work in dB for statistics; VV/VH ratio is a strong
water/vegetation discriminator. SAR sees through clouds — prefer it for
flood mapping and continuous monitoring.

## Pitfalls checklist

- Comparing scenes across dates without consistent atmospheric correction.
- Mixing Sentinel-2 scenes across the 2022-01-25 baseline change without
  applying `BOA_ADD_OFFSET` — or applying it a second time on a collection
  that is already harmonised.
- Ignoring 20 m→10 m band mixing on Sentinel-2 (B11/B12 are natively 20 m).
- Computing indices on integer DNs without scale factors → nonsense ranges.
- Median composites of SAR in linear units (do statistics in dB).
- Training and test pixels from the same field/polygon → leaked accuracy.
- Forgetting nodata masks after reprojection (edges become zeros → fake
  land cover).

## Execution contract

- **Workflow:** define phenomenon and scale; select sensor, product level, and dates; harmonize calibration, masks, CRS, and resolution; derive features; analyze; validate spatially; publish provenance.
- **Decision rules:** use this skill for imagery preparation and classical analysis, change detection for explicit temporal differencing, deep learning for neural training, and Earth Engine for archive-scale execution.
- **Verification protocol:** inspect masks and valid counts, confirm scale factors, offsets and processing baseline per scene, confirm band resolution, overlay outputs, use spatially independent validation, map errors, and test seasonal or sensor sensitivity.
- **Failure modes:** reject results for cloud or shadow leakage, incomparable processing levels, undocumented or mismatched processing baselines, resampling artifacts, label leakage, nodata contamination, or claims beyond sensor resolution.
- **Deliverables:** analysis-ready imagery or features, processing manifest, masks, derived products, validation metrics and error map, reproducible code, and limitations.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) at execution time for product, calibration, and catalog changes.
