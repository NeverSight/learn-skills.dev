---
name: finite-element-modeling
description: Continuum-scale mechanical, thermal, and multiphysics simulation — Abaqus/COMSOL conventions, mesh generation, and boundary-condition setup. The macroscale end of the modeling spectrum in this repo, consuming material properties measured or computed by other skills as model inputs.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples reference Abaqus/COMSOL conventions conceptually; both are primarily GUI/proprietary-scripting-driven, so this skill focuses on setup principles and pitfalls rather than a specific open-source API.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: finite-element-modeling
---

# Finite Element Modeling

## Overview

Finite element analysis (FEA) solves continuum mechanics, heat transfer, and coupled multiphysics
problems over a discretized (meshed) geometry — the macroscale end of this repo's modeling spectrum,
consuming material properties (elastic modulus, thermal conductivity, CTE) that `mechanical-testing`
and `thermal-analysis` measure, or that `computational-materials`/`phase-field-calphad` predict, as
model inputs rather than computing them from first principles.

## When to use this skill

Activate when the request involves:
- FEA, finite element analysis, Abaqus, COMSOL, ANSYS, mesh generation, boundary conditions,
  multiphysics simulation
- Terms: mesh convergence, element type, constitutive model, von Mises stress, thermal-stress coupling
- "Set up an FEA model of...," "check mesh convergence," "what boundary conditions for..."

## Core usage

### Mesh convergence checking (the first validity check for any FEA result)

```python
def mesh_convergence_check(mesh_sizes, result_values, tolerance_percent=2):
    """Run the same model at progressively finer mesh sizes; the result should
    plateau. Report as converged only once consecutive refinements change the
    result by less than the tolerance."""
    percent_changes = [
        abs((result_values[i] - result_values[i - 1]) / result_values[i - 1]) * 100
        for i in range(1, len(result_values))
    ]
    converged_at_index = next((i for i, pc in enumerate(percent_changes) if pc < tolerance_percent), None)
    return {
        "converged_mesh_size": mesh_sizes[converged_at_index + 1] if converged_at_index is not None else None,
        "percent_changes": percent_changes,
    }
```

### Material property input from measured/computed data

```python
def elastic_properties_from_testing(elastic_modulus_gpa, poisson_ratio):
    """The FEA model's constitutive behavior is only as good as these inputs —
    typically sourced from mechanical-testing's stress-strain analysis, or
    computational-materials' elastic-constant calculations, not assumed generic
    handbook values unless the specific material/condition is genuinely
    well-represented by a handbook value."""
    lame_lambda = (elastic_modulus_gpa * poisson_ratio) / ((1 + poisson_ratio) * (1 - 2 * poisson_ratio))
    shear_modulus = elastic_modulus_gpa / (2 * (1 + poisson_ratio))
    return {"lame_lambda_gpa": lame_lambda, "shear_modulus_gpa": shear_modulus}
```

### Thermal-stress coupling setup considerations

```python
def thermal_stress_estimate(cte_per_k, delta_T, elastic_modulus_gpa, constrained_fraction=1.0):
    """First-order estimate of thermal stress under full constraint — a sanity
    check before a full coupled simulation, not a substitute for one when the
    actual constraint condition is more complex than fully fixed."""
    thermal_strain = cte_per_k * delta_T
    return thermal_strain * elastic_modulus_gpa * constrained_fraction  # GPa
```

## Validation & Pitfalls

Canonical reference: Zienkiewicz, Taylor & Zhu, *The Finite Element Method: Its Basis and
Fundamentals* (7th ed., 2013), for FEA methodology generally.

- **Mesh convergence must be checked for every new geometry/loading condition, not assumed from a
  prior similar model** — a mesh density adequate for one geometry or stress concentration doesn't
  automatically transfer to a different one, especially near geometric features (sharp corners,
  holes) where stress gradients are steep.
- **Boundary condition choice is often the single largest source of discrepancy between simulation
  and reality, more than mesh resolution or material model refinement** — an overly idealized
  boundary condition (perfectly fixed, perfectly frictionless) can dominate model error; justify
  boundary conditions against the actual physical constraint being modeled, and check sensitivity to
  reasonable alternative choices.
- **Material property inputs sourced from a different material state/condition than what's being
  modeled produce a precise but wrong answer** — e.g. using room-temperature elastic modulus for a
  high-temperature simulation, or bulk properties for a thin-film/small-scale structure where
  size-dependent effects matter. Match input data conditions to the model's actual conditions.
- **A converged, non-crashing simulation is not the same as a validated one** — numerical convergence
  confirms the solver found a stable solution to the equations as posed, not that those equations
  (material model, boundary conditions, geometry simplifications) correctly represent reality.
  Validate against at least one independent data point (analytical solution for a simplified case, or
  experimental measurement) before trusting predictions for conditions without such a check.
- **Element type choice (linear vs. quadratic, reduced vs. full integration) affects both accuracy and
  characteristic numerical artifacts** (e.g. shear locking in linear elements for bending-dominated
  problems, hourglassing in reduced-integration elements) — match element type to the problem physics,
  and watch for these specific artifact signatures rather than assuming a default element type is
  always appropriate.
