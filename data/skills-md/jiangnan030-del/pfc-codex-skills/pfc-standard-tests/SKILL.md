---
name: pfc-standard-tests
description: Self-contained PFC 6.0 standard mechanical-test skill with canonical UCS, biaxial, triaxial, direct shear, Brazilian, and three-point bending templates.
---

# PFC Standard Tests

Use this skill to explain, adapt, or generate canonical PFC 6.0 rock/soil mechanics test cases. The skill is now self-contained: the reusable `.dat`, `.p2fis`, `.p3fis`, and supporting geometry assets are stored under `scripts/canonical/` instead of relying on machine-local paths.

## Parent Skill Relationship

`pfc-standard-tests` is a child skill of `pfc-workflow`. It does not own the full PFC lifecycle. Use it only for standard laboratory-test template selection, stage normalization, and bundled command-flow handoff. Return to `pfc-workflow` for calibration, solve orchestration, post-processing routing, verification, and delivery.

Parent/child split:

- Parent `pfc-workflow`: owns planning, parameterization, calibration, solve management, post-processing routing, V&V, and final delivery.
- Child `pfc-standard-tests`: owns canonical UCS, biaxial, triaxial, direct shear, Brazilian, and three-point bending templates plus their standard stage vocabulary.
- Sibling child `pfc-postprocessing`: owns standard figures and field exports after solve.
- Sibling child `pfc-ae-energy`: owns AE, energy, and source-mechanism outputs after solve.

## When To Use

Use through `pfc-workflow` when the workflow reaches standard-test selection or template materialization:

- Set up or explain UCS, biaxial, triaxial, direct shear, Brazilian splitting, or three-point bending models.
- Extract a reproducible PFC 6.0 command-flow template for a standard laboratory test.
- Normalize stage names, saved-state names, and expected output curves across teaching examples.
- Compare rigid-wall and flexible-membrane triaxial workflows.
- Prepare a GitHub-ready, reproducible standard-test template package.

## Required Inputs

Ask for these if they are missing:

- Test type: `ucs`, `biaxial`, `brazilian`, `direct-shear`, `three-point-bending`, `triaxial-rigid`, or `triaxial-flexible-membrane`.
- Target dimension and model type: 2D or 3D, specimen width/height/radius, target porosity, particle radius range.
- Boundary style: rigid walls, platens, shear box, cylinders, or membrane/shell boundary.
- Material model: usually linear before bonding, then linearpbond for bonded specimen tests.
- Required saved states: sample generation, isotropic/preload, bonding, confinement, load-ready, peak/final.
- Required outputs: stress-strain, force-displacement, crack count, fracture DFNs, fragment IDs, or energy/AE add-ons.

## Canonical Template Map

| Test | Folder | Main stages | Crack tracker |
| --- | --- | --- | --- |
| Biaxial compression | `scripts/canonical/biaxial/` | `1chengyang` -> `2yuya` -> `3jiaojiaojie` -> `4weiya` -> `5jiazai` | none by default |
| UCS / uniaxial compression | `scripts/canonical/ucs/` | `1chengyang` -> `2yuya` -> `3jiaojiaojie` -> optional crack preload/unload -> `5jiazai` | `fracture.p2fis` |
| Brazilian splitting | `scripts/canonical/brazilian/` | `1chengyang` -> `2yuya` -> `3jiajiaojie` -> `4xiezai` -> `5jiazai` | `fracture.p2fis` |
| Direct shear | `scripts/canonical/direct-shear/` | `1chengyang` -> `2yuya` -> `3jiajiaojie` -> `4jiazhouya` -> `5jiazai` | `fracture.p2fis` |
| Three-point bending | `scripts/canonical/three-point-bending/` | `1chengyang` -> `2tihuan` -> `3jiajiaojie` -> `4addjiazai` -> `5jiazai` | `fracture.p2fis` plus `11.dxf` |
| Conventional triaxial, rigid wall | `scripts/canonical/triaxial-rigid/` | `1chengyang` -> `2yuya` -> `3jiajiaojie` -> `4weiya` -> `5jiazai` | `fracture.p3fis` |
| Conventional triaxial, flexible membrane | `scripts/canonical/triaxial-flexible-membrane/` | `1chengyang` -> `2yuya` -> `3jiajiaojie` -> `4jiarouxing` -> `5jiazai` | `fracture.p3fis` |

## Stage Vocabulary

Normalize user-facing stages to these labels even when source filenames differ:

1. `sample`: create domain, walls/geometry, particle assembly, density/damping, initial calm/solve, save `sample`.
2. `preload` or `isotropic`: apply initial stress or compact specimen, save `yuya`/preload state.
3. `bond`: install parallel bonds or bonded contact model, save `jiaojie`.
4. `boundary`: add/load confinement, platens, shear box, Brazilian loading walls, or membrane shell.
5. `load`: apply monotonic or cyclic displacement/strain loading, histories, solve criteria, final save.
6. `postprocess`: export stress-strain/force-displacement, crack/fragment data, and saved-state snapshots.

## Working Rules

- Prefer PFC 6.0-compatible command flow and FISH syntax unless the user explicitly asks for a newer PFC version.
- Treat files in `scripts/canonical/` as reference templates, not black-box final models. Adapt dimensions, parameters, histories, and output filenames to the user's project.
- Keep stage names explicit when creating new cases. Do not hide important setup inside GUI-only project metadata.
- Preserve milestone saves (`sample`, `yuya`/preload, `jiaojie`/bonded, boundary-loaded, `result`) so failures can be debugged stage by stage.
- For fracture-aware tests, include the correct `fracture.p2fis` or `fracture.p3fis`, register the bond-break callback, and export DFN/fragment outputs if requested.
- When publishing to GitHub, avoid absolute local paths. Reference bundled files with relative paths only.

## Output Contract

A complete child-skill handoff back to `pfc-workflow` should include:

- The selected canonical template folder and why it fits.
- A stage-by-stage execution list with input and output state names.
- Required files to copy from `scripts/canonical/<case>/`.
- Any template parameters that `pfc-workflow` must adapt for specimen size, porosity, stiffness, bond strength, loading rate, or confinement.
- Expected curves: UCS/biaxial/triaxial stress-strain, Brazilian force-displacement or tensile stress proxy, direct shear shear stress-displacement, bending load-CMOD/deflection if available.
- Expected fracture outputs when fracture tracking is enabled.
- A clear note that calibration, solve execution, post-processing routing, and final delivery continue in `pfc-workflow`.

## Local Contents

- `references/overview.md`: detailed self-contained source map and stage descriptions.
- `examples/README.md`: how to use and validate each bundled canonical case.
- `scripts/canonical/`: copied source code and assets for all supported test families.
- `scripts/canonical/manifest.json`: file inventory with sizes and SHA-256 hashes.
- `scripts/README.md`: helper-script policy and suggested materialization workflow.
