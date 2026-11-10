---
name: pfc-fast-calibration
description: Child skill of pfc-workflow for rapid calibration of an improved PFC3D linear parallel-bond model using 13 micro-parameters, strong/weak contact grouping, Weibull damage, 13-factor orthogonal tests, Pearson correlation, regression formulas, and macro-target back-solving.
---

# PFC Fast Calibration

Use this skill to design, explain, or implement rapid micro-parameter calibration for an improved linear parallel-bond model (LPBM / `linearpbond`) in PFC3D. The route is: 13 micro-parameters -> strong/weak contact grouping -> Weibull damage -> 27-run orthogonal design -> PFC3D UCS/UTS/triaxial tests -> Pearson correlation -> regression formulas -> back-solve micro-parameters from macro targets.

## Parent Skill Relationship

`pfc-fast-calibration` is a child skill of `pfc-workflow`. It owns the fast-calibration specialist portion, not the full model lifecycle.

Use these handoffs:

- Parent `pfc-workflow`: owns full planning, case orchestration, solve campaign control, V&V, and delivery.
- Sibling `pfc-contact-models`: owns contact-law selection and detailed LPBM / CMAT / contact property ordering.
- Sibling `pfc-servo-calibration`: owns wall-servo, confining pressure, stress-control stability, and loading boundary details.
- Sibling `pfc-standard-tests`: owns UCS, UTS/Brazilian, triaxial, and other canonical laboratory-test command flows.
- Sibling `pfc-mineral-heterogeneity`: owns mineral phase grouping, multi-mineral parameter assignment, and mineral-style Weibull damage.
- Sibling `pfc-fish`: owns reusable FISH function refactoring, callback cleanup, histories, and object traversal helpers.
- Sibling `pfc-postprocessing`: owns exported curves, summary tables, and figure production after calibration runs.

If an older project mentions `pfc-foundations` or `pfc-modeling-techniques`, map them to the current split as follows:

```text
pfc-foundations -> pfc-contact-models + pfc-basics
pfc-modeling-techniques -> pfc-servo-calibration + pfc-standard-tests + pfc-postprocessing
```

## When To Use

Use through `pfc-workflow` when the task asks to:

- raise a low PFC UCS/UTS ratio from about `3-4` toward realistic rock values such as `10-30`
- calibrate many LPBM micro-parameters faster than manual trial-and-error
- run or reproduce a 13-factor, 3-level, 27-run orthogonal calibration campaign
- derive macro-micro regression formulas from PFC numerical experiments
- back-solve improved LPBM micro-parameters from target `E`, `nu`, `UCS`, `UCS/UTS`, `phi`, `c`, and `sigma_cd/UCS`
- implement strong/weak ball-ball contact grouping plus Weibull damage
- compare traditional LPBM and improved LPBM calibration behavior

## Required Inputs

Ask for these if missing:

- PFC version and dimensionality; this source route is PFC3D-oriented.
- Target specimen geometry, particle size range, porosity, and density.
- Macro target values: `E`, `nu`, `UCS`, `UTS` or `UCS/UTS`, `phi`, `c`, and `sigma_cd/UCS` if available.
- Whether the task is source reproduction, new calibration, or just skill documentation.
- Parameter bounds or whether to use the source 3-level table.
- Loading paths required: UCS, UTS, triaxial, or all.
- Random seed policy and acceptable error tolerance.

## Core Method

The improved LPBM has 13 micro-parameters:

```text
Ebar_star          bonded effective modulus
E_ratio            E_star / Ebar_star
kbar_star          bonded normal/shear stiffness ratio
sigma_c_bar        bonded tensile strength
coh_ratio          c_bar / sigma_c_bar
mu                 friction coefficient
phi_bar            bond friction angle
beta_bar_moment    moment contribution factor
Rf                 weak-contact filling ratio
beta_weibull       Weibull shape parameter
R_sigma            weak/strong strength ratio
R_E                weak/strong bond modulus ratio
R_k                bond stiffness-ratio multiplier
```

Macro targets:

```text
E, nu, UCS, phi, c, sigma_cd/UCS, UCS/UTS
```

Default logic:

1. Build a reproducible PFC3D bonded cylinder.
2. Randomly split ball-ball contacts into strong and weak groups using `Rf`.
3. Assign weak contacts reduced modulus/strength by `R_E`, `R_sigma`, and `R_k`.
4. Apply Weibull random multipliers to bond strength and stiffness.
5. Run UCS, UTS, and triaxial tests for each orthogonal trial.
6. Extract macro values using standard strain/stress definitions.
7. Fit or reuse regression equations.
8. Back-solve micro-parameters from macro targets.
9. Re-run and iterate until target error is acceptable.

## Documentation-Backed Rules

PFC command families checked through `pfc-mcp` or previous PFC 6.0 documentation enrichment are summarized in `references/pfc-doc-notes.md`.

Relevant command families:

- `model random`, `model clean`, `model calm`, `model save`, `model restore`
- `contact cmat`, `contact model`, `contact method`, `contact property`, `contact group`
- `ball group`, `wall generate`, `wall attribute`, `ball attribute`
- `fish define`, `fish callback`, `fish history`, `history export`
- `measure create`, `measure history`
- `program call`

## Formula And Code Migration Rules

When the request asks about formulas, theory, exact regression equations, or source-code migration, load these first:

- `references/formulas.md`: LPBM, strong/weak grouping, Weibull, orthogonal analysis, macro extraction, Pearson correlation, and regression formulas.
- `references/orthogonal-design.md`: 13-factor level table, 27-run design, result table, correlation table, and calibration example.
- `references/source-code-complete-pfc6.md`: staged PFC 6.0-oriented source-code route from specimen generation through UTS.
- `scripts/canonical/`: reusable templates for orthogonal design generation, regression back-solving, improved LPBM assignment, and metric extraction.

## Operating Rules

- Always state whether source regression equations are being reused or recalibrated for a new specimen.
- Treat source regression equations as initial-value predictors, not universal material laws.
- Keep strong/weak contact grouping, Weibull damage, loading tests, metric extraction, and regression analysis as separate stages.
- Fix random seeds for orthogonal comparisons; vary seeds only as a deliberate robustness study.
- Save staged models after packing, consolidation, improved LPBM assignment, and each loading setup.
- Verify `sigma_cd/UCS` carefully because the source example reports the largest validation error for this metric.
- Use a few confirmation simulations after back-solving; do not stop at algebraic inversion.

## Output Contract

A complete fast-calibration handoff back to `pfc-workflow` should include:

- target macro values and tolerances
- chosen fixed parameters and back-solved parameters
- orthogonal design table or selected trial set
- strong/weak contact grouping rule and seed
- Weibull `alpha` and `beta` settings
- PFC staged command files and save-state names
- extracted macro metrics and error table
- regression formula source and fit quality
- downstream routes for standard tests, servo, post-processing, and V&V

## Local Contents

- `references/overview.md`: workflow boundary, use cases, and routing.
- `references/formulas.md`: complete formula migration.
- `references/orthogonal-design.md`: 13-factor tables, 27-run design, correlations, and example calibration.
- `references/source-code-complete-pfc6.md`: complete staged PFC command-flow migration.
- `references/pfc-doc-notes.md`: PFC 6.0 command documentation notes.
- `examples/README.md`: how to materialize and validate a calibration campaign.
- `scripts/canonical/orthogonal_design_13params.csv`: source 27-run design table.
- `scripts/canonical/regression_fast_calibration.py`: regression/back-solve helper.
- `scripts/canonical/improved_lpbm_assign.p3fis`: strong/weak contact and Weibull assignment template.
- `scripts/canonical/extract_macro_metrics.py`: macro metric extraction helper template.
- `scripts/canonical/manifest.json`: script inventory.
