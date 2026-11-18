---
name: materials-figures
description: Publication-quality figure conventions for common materials science plot types — phase diagrams, pole figures, stress-strain curves, and band structure/DOS plots. Use this when the deliverable is a figure, not just an analysis result — correctness of the underlying analysis is covered by the relevant technique skill; this is specifically about clear, honest visual presentation.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use matplotlib; pymatgen's plotting utilities for phase diagrams and band structure/DOS specifically.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: materials-figures
---

# Materials Science Figures

## Overview

A correct analysis can still be misrepresented by a misleading figure — this skill covers the
conventions specific to common materials-science plot types that make the difference between a
figure that accurately conveys uncertainty/methodology and one that doesn't, on top of general good
plotting practice.

## When to use this skill

Activate when the request involves:
- Making a publication figure or plot from materials characterization or simulation results
- Terms: phase diagram plot, pole figure, stress-strain curve figure, band structure plot, DOS plot
- "Make a figure of this result," "plot this phase diagram," "visualize this stress-strain data"

## Core usage

### Stress-strain curve with clearly marked derived quantities

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(strain, stress, color="black")
ax.axhline(yield_strength, color="gray", linestyle="--", linewidth=0.8, label=f"Yield (0.2% offset): {yield_strength:.0f} MPa")
ax.scatter([strain[np.argmax(stress)]], [stress.max()], color="red", zorder=5, label=f"UTS: {stress.max():.0f} MPa")
ax.set_xlabel("Engineering strain")   # state explicitly: engineering, not true strain — see mechanical-testing pitfalls
ax.set_ylabel("Engineering stress (MPa)")
ax.legend()
```

### Phase diagram (pymatgen's plotter, with stability annotation)

```python
from pymatgen.analysis.phase_diagram import PDPlotter

plotter = PDPlotter(phase_diagram, show_unstable=0.05)   # show near-hull unstable entries up to 50 meV/atom
plot = plotter.get_plot()
# Label energy-above-hull explicitly for any entry called out in the figure —
# a phase diagram figure without hull-distance context invites readers to
# assume everything shown is equally stable, which is rarely the intent.
```

### Pole figures (crystallographic texture)

```python
# Pole figures plot crystallographic orientation density on a stereographic
# projection — typically produced by dedicated texture-analysis software
# (e.g. MTEX, a MATLAB toolbox) rather than general plotting libraries, since
# the stereographic projection and orientation-distribution-function machinery
# is specialized. When building one manually, always include the projection
# convention (upper/lower hemisphere) and intensity scale explicitly.
```

### Band structure and density of states (combined plot)

```python
from pymatgen.electronic_structure.plotter import BSDOSPlotter

plotter = BSDOSPlotter(bs_projection="elements", dos_projection="elements")
plot = plotter.get_plot(band_structure, dos)
# Mark the Fermi level explicitly (usually a horizontal line at E=0 by
# convention) — a band structure/DOS plot without a clear Fermi level reference
# is not interpretable for metallic/insulating character at a glance.
```

## Validation & Pitfalls

- **A phase diagram figure showing entries without their energy-above-hull value invites a reader to
  assume all shown phases are equally accessible/stable** — always provide hull-distance context
  (via labels, color-coding, or a stated cutoff for what's shown), consistent with
  `materials-structure-analysis/references/phase-diagrams.md`'s point that a small positive hull
  distance still may (or may not) be synthesizable.
- **Engineering vs. true stress-strain must be labeled explicitly on any plotted curve** — the same
  pitfall as in `mechanical-testing`, but specifically a figure-labeling failure mode: an unlabeled
  axis lets a reader assume whichever convention they're used to, which can be wrong.
- **Color scale and axis range choices can visually exaggerate or hide effect size**, the same
  general principle as this repo's sibling neuroscience figures skill — choose ranges justified by
  the data's actual distribution, and state them, rather than defaulting to auto-scaled ranges that
  may mislead about magnitude.
- **DFT-computed and experimentally measured quantities (e.g. a computed vs. measured band gap) must
  be visually distinguishable when shown together** — using identical visual treatment for a computed
  prediction and a measured value in the same figure invites equal-confidence interpretation, which
  the systematic DFT band-gap underestimate (see `computational-materials/references/dft.md`) doesn't
  support; use distinct markers/line styles and label which is which.
- **Simulated/projected results (a candidate material's predicted property, an extrapolated trend)
  must be visually distinguished from measured results** — matching this repo's sibling neuroscience
  figures skill's principle exactly: use a distinct visual treatment (dashed lines, hatching, explicit
  labeling) for anything that isn't a direct measurement.
