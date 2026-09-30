---
name: spatial-statistics
description: >-
  Always invoke before testing a geographic pattern for clustering, hotspots,
  dependence, or explanatory regression, even when aggregation or ordinary
  OLS is proposed as routine. Covers Moran's I, LISA, Getis-Ord Gi*, weights,
  MAUP and scale sensitivity for areas/grids, residual dependence, and
  spatial lag/error/GWR/MGWR models. Use ML standards for predictive
  evaluation and geostatistics for continuous surfaces from sparse samples.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# Spatial Statistics

Purpose: answer "is it clustered, where, and why" with defensible inference.
The core discipline: spatial data violates independence assumptions, so
standard statistics silently overstate significance — every analysis here
starts with weights design and ends with residual diagnostics.

## Spatial weights (W) — the analysis IS the weights

Every result downstream depends on W; choose it for substantive reasons and
run a sensitivity check with one alternative:

| Weights | Use when |
|---|---|
| Queen/Rook contiguity | Irregular polygons (admin units, parcels) |
| K-nearest neighbors | Points; islands present (contiguity leaves them unconnected) |
| Distance band | Physical process with known range |
| Kernel (distance-decayed) | Smooth influence, GWR-style local models |

```python
from libpysal.weights import Queen

w = Queen.from_dataframe(gdf, use_index=True)
print(f"islands: {w.islands}")   # unconnected units break stats — fix or document
w.transform = "r"                # row-standardize (default for Moran/lag models)
```

Always report: weights type, parameters, number of islands, and whether
results survive an alternative W.

## Global → local workflow

1. **Global Moran's I** (`esda.Moran`, permutation inference ≥999) —
   answers "any clustering at all?" Report I, p_sim, and the permutation
   distribution, not the analytical p.
2. **LISA / local Moran** (`esda.Moran_Local`) — maps WHERE: High-High,
   Low-Low clusters, High-Low/Low-High outliers. Correct for multiple
   testing (FDR at minimum) before coloring a map — uncorrected LISA maps
   overstate clusters and this is the field's most common abuse.
3. **Getis-Ord Gi\*** (`esda.G_Local`, star=True) — hot/cold spots of
   intensity (a distinct question from Moran clusters — Gi* finds
   concentrations of high values, LISA finds similarity structure).
4. Rates, not counts, for population-based phenomena; use Empirical Bayes
   smoothing (`esda.smoothing`) for small-population units before any of
   the above — raw rates in sparse units are noise.

## Point patterns

- Separate first-order intensity (density varies) from second-order
  interaction (points attract/repel) — KDE describes the former, Ripley's
  K/L (`pointpats`) tests the latter.
- Always test against an inhomogeneous null when the study area has obvious
  density gradients (population, roads); CSR against a city is a strawman.
- KDE bandwidth drives the story: report it, justify it (Silverman/CV), and
  show one alternative.

## Spatial regression decision path

Run OLS first, then diagnose — never start with a spatial model:

```python
from spreg import OLS
ols = OLS(y, X, w=w, spat_diag=True, moran=True, name_y="price", name_x=xnames)
```

Decision (Anselin's rule via LM tests): LM-Lag significant & LM-Error not →
**spatial lag (SAR)**; reverse → **spatial error (SEM)**; both → compare
robust LM versions; neither → OLS stands (report that as a finding).
Interpretation caveats: in SAR, coefficients are NOT marginal effects —
report direct/indirect (spillover) effects. In SEM, spatial structure is
nuisance correlation, no spillover story allowed.

**GWR/MGWR** (`mgwr`): when relationships plausibly vary over space.
Bandwidth by AICc search; map local coefficients WITH local t-values masked
for insignificance; MGWR when predictors operate at different scales.
GWR is exploratory — resist causal language on local coefficients.

## Inference honesty

- Permutation p-values over analytical ones wherever available.
- Multiple testing: n local tests = n units; FDR-correct.
- MAUP (modifiable areal unit problem): results can flip with unit
  aggregation — if the aggregation level is a choice, test one alternative
  and disclose.
- Spatial autocorrelation in residuals after modeling = model still wrong;
  report residual Moran's I for every final model.
- Correlation ≠ causation applies doubly here: spatially confounded
  variables (everything correlates with "distance to coast") demand
  explicit identification strategies before causal claims.

## Reporting template

```
## Spatial analysis: <question>
- Units & n, variable(s), rate smoothing: <...>
- W: <type/params>, islands: <n>, sensitivity W: <type>
- Global: Moran's I = <> (p_perm = <>)
- Local: <k> significant clusters after FDR; map attached
- Model: <OLS/SAR/SEM/GWR> chosen because <LM diagnostics>
- Residual Moran's I: <> — <interpretation>
- Caveats: MAUP, W-sensitivity, causal limits
```

## Execution contract

- **Workflow:** define inferential question and unit; inspect distributions and rates; construct and justify spatial weights; run global before local tests; fit models if needed; diagnose residual dependence; report uncertainty.
- **Decision rules:** use spatial statistics for dependence and inference, geostatistics for interpolating sampled continuous surfaces, and predictive ML when out-of-sample prediction is the primary goal.
- **Verification protocol:** test alternative weights and aggregation, use valid permutation or model inference, correct local multiplicity, inspect residual Moran's I, and distinguish association from causation.
- **Failure modes:** withhold inferential claims for arbitrary weights, islands ignored, unstable MAUP results, uncorrected multiple tests, residual autocorrelation, or unsupported causal language.
- **Deliverables:** analysis-ready variables, weights specification, global and local results, corrected significance, diagnostic maps, model and residual checks, sensitivity analysis, and caveats.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before applying version-sensitive statistical APIs or defaults.
