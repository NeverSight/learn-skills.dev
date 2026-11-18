---
name: polymer-characterization
description: Polymer-specific characterization — gel permeation/size-exclusion chromatography (GPC/SEC) for molecular weight distribution, rheology, and dynamic mechanical analysis (DMA). A distinct tooling and analysis ecosystem from small-molecule/inorganic materials characterization, driven by molecular-weight distributions and viscoelastic (not purely elastic) mechanical response.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use numpy/scipy; conventions follow ASTM/ISO standards where cited.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: polymer-characterization
---

# Polymer Characterization

## Overview

Polymers require characterization approaches that don't apply to small molecules or inorganic
crystals: molecular weight is a *distribution*, not a single value (GPC/SEC), and mechanical response
is viscoelastic — time/temperature/frequency-dependent — rather than the purely elastic response
`mechanical-testing`'s tensile framework assumes at short timescales. This skill covers what's
polymer-specific; for glass transition/melting via DSC, see `thermal-analysis` (applies to polymers
too, just not repeated here).

## When to use this skill

Activate when the request involves:
- GPC, SEC, gel permeation chromatography, size-exclusion chromatography, molecular weight
  distribution, PDI, rheology, DMA, dynamic mechanical analysis
- Terms: Mn, Mw, polydispersity index, storage modulus, loss modulus, tan delta, viscoelasticity,
  time-temperature superposition
- "Analyze this GPC trace," "compute molecular weight distribution," "interpret this DMA curve"

## Core usage

### GPC/SEC — molecular weight moments from a chromatogram

```python
import numpy as np

def molecular_weight_moments(retention_time, intensity, calibration_curve):
    """calibration_curve: function mapping retention_time -> molecular weight,
    from a calibration standard set (e.g. narrow-PDI polystyrene standards) —
    GPC separates by hydrodynamic volume, not molecular weight directly, so this
    calibration step is required, not optional (see pitfalls)."""
    mw = calibration_curve(retention_time)
    weight_fraction = intensity / intensity.sum()

    mn = 1 / np.sum(weight_fraction / mw)              # number-average MW
    mw_avg = np.sum(weight_fraction * mw)                # weight-average MW
    pdi = mw_avg / mn                                     # polydispersity index (>=1; 1 = perfectly monodisperse)
    return {"Mn": mn, "Mw": mw_avg, "PDI": pdi}
```

### Rheology — storage/loss modulus and tan delta from oscillatory shear

```python
def viscoelastic_moduli(stress_amplitude, strain_amplitude, phase_angle_rad):
    """Oscillatory shear rheology: complex modulus decomposed into storage
    (elastic, in-phase) and loss (viscous, out-of-phase) components."""
    complex_modulus = stress_amplitude / strain_amplitude
    storage_modulus = complex_modulus * np.cos(phase_angle_rad)   # G'
    loss_modulus = complex_modulus * np.sin(phase_angle_rad)       # G''
    tan_delta = loss_modulus / storage_modulus                      # damping ratio
    return {"G_prime": storage_modulus, "G_double_prime": loss_modulus, "tan_delta": tan_delta}
```

### DMA — glass transition from tan delta peak (an alternative to DSC's Tg)

```python
from scipy.signal import find_peaks

def dma_tg_from_tan_delta(temperature, tan_delta):
    """DMA-derived Tg (tan delta peak) is typically higher than DSC-derived Tg
    (different physical definition — a mechanical vs. calorimetric transition) —
    don't treat them as interchangeable, see pitfalls."""
    peak_idx, _ = find_peaks(tan_delta)
    return temperature[peak_idx[np.argmax(tan_delta[peak_idx])]] if len(peak_idx) > 0 else None
```

## Validation & Pitfalls

Canonical references: Striegel et al., *Modern Size-Exclusion Liquid Chromatography* (2nd ed., 2009);
Ferry, *Viscoelastic Properties of Polymers* (3rd ed., 1980), for rheology/DMA.

- **GPC molecular weight is relative to the calibration standard, not absolute, unless measured with
  additional detectors (light scattering, viscometry) or a matched calibration standard.**
  Polystyrene-calibrated GPC on a chemically different polymer (e.g. a polyolefin) gives
  "polystyrene-equivalent" molecular weight, which can differ substantially from true molecular
  weight — state this explicitly rather than reporting GPC Mn/Mw as if absolute.
- **PDI depends on the full distribution shape, not just Mn and Mw — two distributions with the same
  Mn/Mw/PDI can have meaningfully different shapes** (bimodal vs. unimodal, for instance). Look at
  the full chromatogram/distribution, not just the summary moments, when distribution shape matters
  for the question being asked.
- **Tg from DMA (tan delta or loss modulus peak) and Tg from DSC are measuring different physical
  signatures and routinely differ by 10-20°C or more** — this is not measurement error, it's a
  genuine difference in what's being detected (mechanical relaxation vs. heat capacity change).
  Report which technique produced a stated Tg, and don't treat DMA and DSC Tg values as directly
  comparable without acknowledging this.
- **Rheological and DMA measurements are strongly frequency- and temperature-dependent, and a single
  frequency/temperature measurement is a snapshot, not a complete characterization** — time-
  temperature superposition (constructing a master curve from measurements at multiple temperatures)
  is standard practice for characterizing behavior across a wider effective frequency range than
  directly measurable; a single-condition measurement should be reported as such, not generalized.
- **Sample preparation (film thickness uniformity for DMA, complete dissolution for GPC) directly
  affects data quality in ways specific to polymers** — incomplete dissolution in GPC systematically
  biases toward reporting only the soluble (often lower-MW or less-crosslinked) fraction; confirm and
  report dissolution completeness for cross-linked or high-MW samples.
