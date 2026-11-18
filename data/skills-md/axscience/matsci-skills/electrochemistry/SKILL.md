---
name: electrochemistry
description: Electrochemical characterization — cyclic voltammetry, battery cycling analysis, electrochemical impedance spectroscopy (EIS), and corrosion testing. A distinct tooling and analysis ecosystem from the rest of materials characterization, driven by the energy-materials and corrosion-science communities. Use this for any technique that measures electrochemical response (current, voltage, impedance) as a function of an applied electrical stimulus.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use numpy/scipy; impedance.py for EIS equivalent-circuit fitting specifically.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: electrochemistry
---

# Electrochemistry

## Overview

Electrochemical techniques probe redox behavior, energy storage performance, and corrosion
susceptibility by measuring current/voltage/impedance response. Cyclic voltammetry identifies redox
processes and their kinetics; battery cycling quantifies capacity, efficiency, and degradation over
repeated charge/discharge; EIS separates different resistive/capacitive processes by their
characteristic frequency response; corrosion testing quantifies material degradation in a
electrolytic environment.

## When to use this skill

Activate when the request involves:
- Cyclic voltammetry, CV, battery cycling, capacity fade, Coulombic efficiency, EIS, impedance
  spectroscopy, corrosion, Tafel, polarization curve
- Terms: Nyquist plot, equivalent circuit, C-rate, iR-drop, Randles circuit, corrosion current density
- File formats: potentiostat exports (Biologic `.mpr`, Gamry `.DTA`, common CSV)
- "Analyze this CV scan," "compute capacity fade from cycling data," "fit an equivalent circuit to this EIS"

## Core usage

### Cyclic voltammetry — peak identification and kinetics

```python
import numpy as np
from scipy.signal import find_peaks

def cv_peak_analysis(potential, current, prominence=1e-5):
    """Identifies anodic (oxidation) and cathodic (reduction) peaks — separate
    passes since CV data has both forward and reverse scan directions."""
    ox_peaks, _ = find_peaks(current, prominence=prominence)
    red_peaks, _ = find_peaks(-current, prominence=prominence)
    return {"oxidation_peaks_V": potential[ox_peaks], "reduction_peaks_V": potential[red_peaks]}

def peak_separation_reversibility(e_pa, e_pc):
    """Peak-to-peak separation — ~59mV/n at 25C for an ideal reversible (Nernstian)
    one-electron process; larger separation indicates quasi-reversible/irreversible kinetics."""
    return abs(e_pa - e_pc) * 1000  # mV
```

### Battery cycling — capacity fade and Coulombic efficiency

```python
def coulombic_efficiency(charge_capacity, discharge_capacity):
    return (discharge_capacity / charge_capacity) * 100

def capacity_fade_analysis(cycle_number, discharge_capacity):
    """Capacity retention relative to an early-cycle baseline (not cycle 1, which
    often has formation-cycle artifacts) — see pitfalls."""
    baseline = discharge_capacity[2]  # e.g. cycle 3, past initial formation cycles
    retention_percent = (discharge_capacity / baseline) * 100
    return cycle_number, retention_percent
```

### EIS — equivalent circuit fitting

```python
from impedance.models.circuits import CustomCircuit

def fit_randles_circuit(frequencies, impedance_complex):
    """Randles circuit: solution resistance + charge-transfer resistance (parallel
    with double-layer capacitance) + Warburg diffusion — a standard starting model
    for a simple electrode process, not universally applicable (see pitfalls)."""
    circuit = CustomCircuit("R0-p(R1,C1)-W1", initial_guess=[10, 100, 1e-5, 100])
    circuit.fit(frequencies, impedance_complex)
    return circuit
```

### Corrosion — Tafel analysis

```python
def tafel_analysis(potential, log_current_density, linear_region_mask):
    """Linear (Tafel) regions of a polarization curve, extrapolated to the
    corrosion potential, give corrosion current density — the standard
    quantitative corrosion-rate measure."""
    slope, intercept = np.polyfit(potential[linear_region_mask], log_current_density[linear_region_mask], 1)
    return {"tafel_slope": slope, "intercept": intercept}
```

## Validation & Pitfalls

Canonical references: Bard & Faulkner, *Electrochemical Methods* (2nd ed., 2001), for CV/general
electrochemistry; Orazem & Tribollet, *Electrochemical Impedance Spectroscopy* (2nd ed., 2017), for
EIS; ASTM G3/G59 for corrosion polarization conventions.

- **Uncompensated solution resistance (iR drop) shifts apparent potentials and must be corrected
  before kinetic interpretation** — a CV or polarization curve without iR compensation gives
  systematically shifted peak/onset potentials, especially at high current or in low-conductivity
  electrolytes; confirm whether iR compensation was applied.
- **Early battery cycles (formation cycles) have distinct, non-representative behavior (SEI
  formation, initial irreversible capacity loss)** — computing capacity fade relative to cycle 1
  rather than a post-formation baseline (e.g. cycle 3-5) overstates apparent degradation; state which
  baseline was used.
- **EIS equivalent-circuit models are not unique — multiple different circuit topologies can fit the
  same impedance data comparably well, especially with limited frequency range or noisy data.** A
  good fit (low residual) doesn't validate the physical model; the circuit elements should be
  physically motivated by the known electrochemical system, and fit quality checked via the
  Kramers-Kronig relations (a model-independent consistency check) before trusting extracted
  parameters.
- **Tafel slope extraction requires identifying a genuinely linear region, and the "linear region"
  choice is a real analytic decision that changes the extracted corrosion current** — mass-transport
  limitations or multiple overlapping reactions can curve the polarization curve outside a narrow true
  Tafel region; report the potential window used for the linear fit.
- **C-rate (charge/discharge rate) strongly affects measured capacity, and capacity values at
  different C-rates aren't directly comparable** — always report C-rate alongside any capacity value,
  and don't compare capacity fade trends measured at different rates as equivalent degradation
  measures.
