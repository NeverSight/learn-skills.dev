---
name: radiology-preprocessing
description: Structural MRI/CT preprocessing pipeline for radiology workflows covering skull stripping, bias field correction, registration, and intensity normalization. Triggers on skull stripping, bias correction, registration, ANTs, FSL, HD-BET, N4, brain extraction, normalization, FLIRT, FNIRT, SyN, fslreorient2std, MNI registration, T1 preprocessing.
usage: Invoke when preprocessing structural MRI/CT data, including skull stripping, bias correction, registration, or intensity normalization.
version: 1.0.0
validated_against:
  date: 2025-01-15
  packages: {ants: "2.5", fsl: "6.0.7", hd-bet: "2.0"}
tags: [skill, category:pipeline, medical-imaging, radiology, preprocessing, ants, fsl, hcls]
---

# Radiology Preprocessing

## Overview

Deterministic commands for preprocessing structural brain MRI (T1w, T2w, FLAIR) and related volumetric radiology data. Covers the canonical pipeline used by most downstream analyses (segmentation, registration studies, deep-learning training): **reorient → bias correction → skull strip → registration → intensity normalization**.

Tools used:
- **HD-BET** — CNN-based brain extraction (state-of-the-art on pathological brains).
- **FSL** — `bet`, `flirt`, `fnirt`, `fslmaths`, `fslreorient2std`.
- **ANTs** — `N4BiasFieldCorrection`, `antsRegistrationSyNQuick.sh`, `antsApplyTransforms`.
- **FreeSurfer** — `mri_convert` for resampling/format conversion.

All commands operate on NIfTI (`.nii` / `.nii.gz`). Run in a POSIX shell with the respective tool on `PATH`.

## Usage

### Standard T1w preprocessing pipeline

Run these steps in order on a single subject volume:

```bash
# 1. Reorient to standard (MNI-style RAS orientation)
fslreorient2std input.nii.gz reoriented.nii.gz

# 2. N4 bias field correction (BEFORE skull stripping)
N4BiasFieldCorrection -d 3 \
  -i reoriented.nii.gz \
  -o [n4.nii.gz,bias_field.nii.gz] \
  -s 3 \
  -c [50x50x30x20,1e-6] \
  -b [300]

# 3. Skull strip with HD-BET
hd-bet -i n4.nii.gz -o brain.nii.gz -device 0 -mode fast -tta 0
# CPU fallback (slower, no CUDA required): -device cpu

# 4. Register to MNI152 template (SyN nonlinear)
antsRegistrationSyNQuick.sh -d 3 \
  -f $FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz \
  -m brain.nii.gz \
  -o sub2mni_ \
  -t s

# 5. Z-score intensity normalization within brain mask
fslmaths brain.nii.gz -mas brain_mask.nii.gz brain_masked.nii.gz
MEAN=$(fslstats brain_masked.nii.gz -k brain_mask.nii.gz -M)
STD=$(fslstats brain_masked.nii.gz -k brain_mask.nii.gz -S)
fslmaths brain_masked.nii.gz -sub $MEAN -div $STD -mas brain_mask.nii.gz brain_zscore.nii.gz
```

HD-BET writes `brain.nii.gz` and `brain_mask.nii.gz` (mask has `_mask` suffix by default).

### GPU acceleration

HD-BET defaults to GPU; use `-device 0` for first CUDA device. `-mode fast -tta 0` disables test-time augmentation for ~5x speedup with minimal quality loss.

```bash
hd-bet -i n4.nii.gz -o brain.nii.gz -device 0
```


## Response Format

- Lead with the command or code the user needs — explain after
- Structure as: confirm inputs → working code → key parameters explained → gotchas
- One complete working example per task; do not show every alternative
- Keep code comments minimal and functional (what, not why-it-exists)
- Target: 50-100 lines of code with brief surrounding explanation

Do not narrate the pipeline ordering rationale or preprocessing theory unless explicitly asked — produce the correct commands in sequence with brief parameter justification.

## Core Concepts

### 1. Skull stripping (brain extraction)

**HD-BET** (preferred — robust to pathology):
```bash
hd-bet -i input.nii.gz -o output_bet.nii.gz -device cpu -mode fast -tta 0
```

**FSL BET** (fallback, classical):
```bash
bet input.nii.gz output_bet.nii.gz -R -f 0.3 -g 0
```
- `-R`: robust centre-of-gravity estimation.
- `-f 0.3`: fractional intensity threshold (lower = larger brain mask).
- `-g 0`: vertical gradient in threshold.

### 2. Bias field correction — N4 (ANTs)

Correct low-frequency intensity inhomogeneity from RF coil / B1 field. **Always run before skull stripping** — the bias field estimate is better with the skull in place, and a skull-stripped input produces artifacts near the brain boundary.

```bash
N4BiasFieldCorrection -d 3 \
  -i input.nii.gz \
  -o [corrected.nii.gz,bias_field.nii.gz] \
  -s 3 \
  -c [50x50x30x20,1e-6] \
  -b [300]
```
- `-d 3`: 3D image.
- `-s 3`: shrink factor (speedup).
- `-c [50x50x30x20,1e-6]`: max iterations per level + convergence threshold.
- `-b [300]`: B-spline mesh resolution (mm).

### 3. Registration — ANTs

`antsRegistrationSyNQuick.sh` is the sensible default wrapper.

```bash
# Rigid (6 DOF) — same subject, different timepoint/modality
antsRegistrationSyNQuick.sh -d 3 -f fixed.nii.gz -m moving.nii.gz -o output_ -t r

# Affine (12 DOF) — cross-subject coarse alignment
antsRegistrationSyNQuick.sh -d 3 -f fixed.nii.gz -m moving.nii.gz -o output_ -t a

# SyN (nonlinear) — atlas / MNI registration
antsRegistrationSyNQuick.sh -d 3 -f fixed.nii.gz -m moving.nii.gz -o output_ -t s
```

Outputs (for `-t s`):
- `output_0GenericAffine.mat` — affine transform.
- `output_1Warp.nii.gz` / `output_1InverseWarp.nii.gz` — displacement fields.
- `output_Warped.nii.gz` — moving resampled into fixed space.

Apply the saved transform to another image (e.g., a segmentation):
```bash
# For intensity images — Linear interpolation
antsApplyTransforms -d 3 \
  -i input.nii.gz \
  -r reference.nii.gz \
  -o output.nii.gz \
  -t output_1Warp.nii.gz \
  -t output_0GenericAffine.mat

# For label maps — NearestNeighbor interpolation
antsApplyTransforms -d 3 \
  -i labels.nii.gz \
  -r reference.nii.gz \
  -o labels_in_ref.nii.gz \
  -n NearestNeighbor \
  -t output_1Warp.nii.gz \
  -t output_0GenericAffine.mat
```

**ANTs applies transforms in reverse order**: the last `-t` is applied first. For moving→fixed, the affine is applied before the warp, so the CLI order is `-t warp -t affine`.

### 4. Registration — FSL FLIRT + FNIRT

Linear (affine):
```bash
flirt -in moving.nii.gz -ref fixed.nii.gz \
  -out output.nii.gz -omat affine.mat -dof 12
```

Nonlinear (requires affine init):
```bash
fnirt --in=moving.nii.gz \
  --ref=$FSLDIR/data/standard/MNI152_T1_1mm.nii.gz \
  --aff=affine.mat \
  --cout=warp \
  --iout=output.nii.gz
```

Apply warp to another image:
```bash
applywarp -i input.nii.gz -r MNI152_T1_1mm.nii.gz -w warp -o output.nii.gz
# For labels:
applywarp -i labels.nii.gz -r MNI152_T1_1mm.nii.gz -w warp -o labels_mni.nii.gz --interp=nn
```

### 5. Intensity normalization

Needed before most ML models — raw MRI intensities are arbitrary units and vary across scanners/sessions.

**Z-score within brain mask** (most common):
```bash
MEAN=$(fslstats brain.nii.gz -k brain_mask.nii.gz -M)
STD=$(fslstats brain.nii.gz -k brain_mask.nii.gz -S)
fslmaths brain.nii.gz -sub $MEAN -div $STD -mas brain_mask.nii.gz zscore.nii.gz
```

**White matter normalization** (scanner-invariant):
1. Segment WM with FSL FAST or FreeSurfer.
2. Compute mean intensity inside WM mask: `fslstats brain.nii.gz -k wm_mask.nii.gz -M`.
3. Divide volume by that mean.

**Histogram matching** — match the intensity histogram to a reference subject:
- ANTs: `ImageMath 3 out.nii.gz HistogramMatch moving.nii.gz reference.nii.gz`.
- SimpleITK: `sitk.HistogramMatchingImageFilter()`.

### 6. Resampling

FreeSurfer (preferred for isotropic resampling):
```bash
mri_convert --voxel-size 1 1 1 input.nii.gz output_1mm.nii.gz
```

FSL:
```bash
flirt -in input.nii.gz -ref input.nii.gz -applyisoxfm 1 -out output_1mm.nii.gz
# For labels use: -interp nearestneighbour
```

### Standard pipeline order

```
reorient (fslreorient2std)
  → N4 bias correction
  → skull strip (HD-BET)
  → registration (ANTs SyN or FSL FNIRT)
  → intensity normalization (z-score / WM)
```

Resampling to isotropic 1 mm is usually done either at reorient time (if input is anisotropic) or implicitly by registration to a 1 mm template.

## Quick Reference

| Task | Command |
| --- | --- |
| Reorient to standard | `fslreorient2std in.nii.gz out.nii.gz` |
| N4 bias correction | `N4BiasFieldCorrection -d 3 -i in.nii.gz -o [out.nii.gz,bias.nii.gz] -s 3 -c [50x50x30x20,1e-6] -b [300]` |
| Skull strip (HD-BET) | `hd-bet -i in.nii.gz -o brain.nii.gz -device cpu -mode fast -tta 0` |
| Skull strip (BET) | `bet in.nii.gz brain.nii.gz -R -f 0.3 -g 0` |
| Rigid register (ANTs) | `antsRegistrationSyNQuick.sh -d 3 -f fix.nii.gz -m mov.nii.gz -o out_ -t r` |
| Affine register (ANTs) | `antsRegistrationSyNQuick.sh -d 3 -f fix.nii.gz -m mov.nii.gz -o out_ -t a` |
| SyN register (ANTs) | `antsRegistrationSyNQuick.sh -d 3 -f fix.nii.gz -m mov.nii.gz -o out_ -t s` |
| Apply ANTs transform (image) | `antsApplyTransforms -d 3 -i in.nii.gz -r ref.nii.gz -o out.nii.gz -t out_1Warp.nii.gz -t out_0GenericAffine.mat` |
| Apply ANTs transform (labels) | Add `-n NearestNeighbor` |
| FLIRT affine | `flirt -in mov.nii.gz -ref fix.nii.gz -out out.nii.gz -omat aff.mat -dof 12` |
| FNIRT nonlinear | `fnirt --in=mov.nii.gz --ref=MNI152_T1_1mm.nii.gz --aff=aff.mat --cout=warp --iout=out.nii.gz` |
| Z-score normalize | `fslmaths in.nii.gz -sub $MEAN -div $STD -mas mask.nii.gz out.nii.gz` |
| Histogram match (ANTs) | `ImageMath 3 out.nii.gz HistogramMatch mov.nii.gz ref.nii.gz` |
| Resample isotropic 1 mm | `mri_convert --voxel-size 1 1 1 in.nii.gz out.nii.gz` |

### Standard templates (FSL)
- `$FSLDIR/data/standard/MNI152_T1_1mm.nii.gz` — whole-head.
- `$FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz` — brain-only.
- `$FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz` — 2 mm for faster registration.

## Common Mistakes

- **Wrong:** Running skull stripping before bias field correction
  **Right:** Always run N4 bias correction first, then skull strip
  **Why:** Bias field estimation needs the full field of view including skull/neck to fit a smooth B-spline; N4 on an already-stripped brain introduces edge artifacts and leaves residual inhomogeneity

- **Wrong:** Using linear/trilinear interpolation when resampling label maps
  **Right:** Use `NearestNeighbor` (ANTs: `-n NearestNeighbor`; FSL: `--interp=nn`) for any discrete label volume
  **Why:** Linear interpolation on integer segmentation labels produces meaningless fractional values and destroys class boundaries

- **Wrong:** Specifying ANTs transforms in forward CLI order (affine then warp)
  **Right:** Use `-t output_1Warp.nii.gz -t output_0GenericAffine.mat` — warp first in CLI, affine second
  **Why:** `antsApplyTransforms` composes in reverse CLI order (last `-t` applied first); reversing them silently produces misregistered output

- **Wrong:** Registering each longitudinal timepoint independently to MNI
  **Right:** Build a subject-specific midpoint template, register each timepoint to it, then register the midpoint once to MNI
  **Why:** Independent registration introduces asymmetric interpolation bias that corrupts longitudinal measurements (e.g., atrophy)

- **Wrong:** Skipping reorientation at the start of the pipeline
  **Right:** Always run `fslreorient2std` first on inputs from different scanners/vendors
  **Why:** Inconsistent storage orientations cause downstream tools to misinterpret coordinate frames

- **Wrong:** Computing z-score normalization over the full volume including background
  **Right:** Compute mean/std within the brain mask only (`fslstats -k brain_mask.nii.gz`)
  **Why:** Including background zeros drags the mean down and inflates the standard deviation, producing incorrect normalization

## References

- HD-BET: Isensee et al. Hum Brain Mapp 2019, https://doi.org/10.1002/hbm.24750
- ANTs: Avants et al. NeuroImage 2011, https://doi.org/10.1016/j.neuroimage.2010.09.025
- N4 bias correction: Tustison et al. IEEE TMI 2010, https://doi.org/10.1109/TMI.2010.2046908
- FSL: Jenkinson et al. NeuroImage 2012, https://doi.org/10.1016/j.neuroimage.2011.09.015
