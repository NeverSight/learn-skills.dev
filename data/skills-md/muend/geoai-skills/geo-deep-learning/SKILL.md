---
name: geo-deep-learning
description: >-
  Invoke before recommending, training, or auditing a neural method for
  geospatial imagery, including vision transformers, U-Net/DeepLab/SegFormer,
  object detection, pixel classification, building/road extraction, and EO
  foundation-model fine-tuning. Also invoke for neural chip-split validity,
  IoU/accuracy claims, augmentation, imbalanced losses, spatial validation,
  or sliding-window inference. Use remote-sensing-analysis for non-neural
  methods and change-detection when temporal change is the deliverable.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Geospatial Deep Learning

Purpose: deep learning on Earth observation with the two failure modes that
dominate this field designed out from the start: **spatial leakage**
(inflated metrics from nearby train/test pixels) and **georeferencing loss**
(predictions that no longer align with the map).

## Characterise the label set before naming an architecture

Architecture advice given without knowing the label set is guesswork. Before
recommending U-Net versus a foundation model versus a non-deep baseline, state
or ask for:

- **Label count and labelled area** — polygons alone say nothing; 40 polygons
  covering 2 ha and 40 covering 2 000 km² are different problems.
- **Geographic spread** — are the labels clustered in one scene, one season and
  one sensor, or distributed across the deployment domain? Clustered labels cap
  what any model can generalise to, and they decide whether a geographically
  independent validation split is even constructible.
- **Class balance and minority-class pixel fraction**, so loss and sampling
  choices are grounded rather than assumed.
- **Deployment geography** — where predictions will be made, relative to where
  the labels are.

Do not answer "fine-tune a large model or use a simpler approach" before these
are known. When the user has not supplied them, ask and give the provisional
recommendation *conditioned on* the answers ("if the 40 polygons sit in one
scene, then …; if they span the region, then …"), never a single unconditional
recommendation.

## Problem framing first

| Task | Head/architecture default | Metric |
|---|---|---|
| Pixel-wise classes (land cover) | U-Net / DeepLabv3+ (pretrained encoder) | mIoU, per-class IoU |
| Binary extraction (buildings, water, roads) | U-Net + Dice/CE hybrid | IoU, F1; boundary F1 for roads |
| Object detection (vehicles, ships, trees) | YOLO-family / Faster R-CNN, rotated boxes if oriented | mAP@50 |
| Scene classification | Fine-tuned CNN/ViT | F1 (macro) |
| Regression (height, biomass, density) | U-Net with regression head | RMSE/MAE + spatial residual map |

Before any deep model: run a cheap baseline (random forest on bands+indices,
or thresholded index). If the DL model can't beat it clearly, the problem is
data, not architecture. `segmentation-models-pytorch` and `torchgeo` cover
most needs — don't hand-build architectures without a reason.

## Chipping (dataset construction)

- Chip size: 256–512 px; stride < chip size only for training (overlap
  augments), never let overlapping chips straddle the train/val boundary.
- **Preserve georeferencing**: store each chip's transform/bounds (torchgeo
  datasets or a sidecar index in GeoParquet). A prediction you can't put
  back on the map is worthless.
- Keep chips in the native data range; normalize with **dataset-computed**
  per-band statistics (ImageNet stats only for 3-band RGB with a pretrained
  encoder, and say so).
- Class imbalance is the norm (buildings ≈ 2-5% of pixels). Log per-chip
  class fractions; oversample positive-containing chips rather than
  distorting the loss beyond recognition.

## Split policy — the non-negotiable

Split by **geographic block or scene**, never by random chip. Adjacent
chips are near-duplicates; random splits produce beautiful, fake validation
curves. Follow the canonical protocol:
`ml-experiment-standards` → `references/spatial-cv-protocol.md`.
For generalization claims across regions, hold out an entire region.

## Training defaults

- Loss: Dice + CE (segmentation, imbalanced); plain CE when balanced; Focal
  only after comparing — it's not a free win.
- Augmentation: flips/rot90 are safe for nadir imagery; be careful with
  color jitter on multispectral (it breaks radiometric meaning — prefer
  band dropout or slight scaling); never augment in ways that violate the
  physics.
- Encoder pretrained; multispectral input → inflate/replace first conv, or
  use an EO foundation model checkpoint (Prithvi, SatMAE, Clay) when bands
  match.
- Early stopping on val mIoU (patience 10-15); cosine or plateau LR
  schedule; AMP on by default.
- Log config + metrics + git hash per run — see `ml-experiment-standards`.

## Inference on large scenes

Sliding window with overlap (25-50%) and blending (feather/gaussian or
center-crop stitching) to kill tile-edge artifacts. Then:

```python
import rasterio

with rasterio.open(scene_path) as src:
    profile = src.profile
profile.update(count=1, dtype="uint8", nodata=255, compress="deflate")
with rasterio.open(out_path, "w", **profile) as dst:
    dst.write(mask.astype("uint8"), 1)  # same transform/CRS as the scene
```

Post-process: sieve tiny blobs (min mapping unit), optionally regularize
building polygons, and vectorize (`rasterio.features.shapes`) for GIS
delivery. Report metrics AFTER post-processing too — that's what the user
ships.

## Verification protocol

1. Metrics table: per-class IoU/F1 with CI across seeds or folds.
2. **Error map**: prediction vs reference overlaid on imagery for 3+
   representative areas including a known-hard one.
3. Sanity inference on an out-of-distribution patch (different season/
   region) with an honest note on degradation.
4. Alignment check: overlay predictions on the source scene in a GIS at
   two zoom levels — catches transform bugs instantly.

## Pitfalls checklist

- Random chip split → leaked, unreproducible "SOTA".
- Normalizing test data with train-time stats not saved → skewed inference.
- Losing the geotransform in NumPy-land; writing predictions with default
  north-up transform.
- Tile-edge seams from no-overlap inference.
- uint16 imagery fed to a float pipeline without scaling → dead gradients.
- Accuracy reported on chip level while the product is a stitched map.

## Execution contract

- **Workflow:** frame target and unit of prediction; build chips and labels; create spatial splits; train against a baseline; run overlap-aware inference; validate the stitched product.
- **Decision rules:** use deep learning only when label volume, spatial texture, compute, and expected uplift justify it; otherwise prefer a simpler remote-sensing or ML workflow.
- **Verification protocol:** report spatial holdout metrics across seeds or folds, inspect error maps and hard areas, test geographic transfer, and check output georeferencing.
- **Failure modes:** invalidate results for leaked chips, label misalignment, train/inference normalization drift, tile seams, or metrics computed at the wrong product unit.
- **Deliverables:** model and configuration, split manifest, preprocessing contract, metrics with uncertainty, georeferenced predictions, error maps, and model card limitations.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before selecting framework APIs, datasets, or weights and record the checked date.
