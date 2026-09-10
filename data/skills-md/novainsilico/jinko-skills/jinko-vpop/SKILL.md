---
name: jinko-vpop
description: >-
  Create, generate, inspect, or work with Jinkō virtual populations (vpops) and vpop designs via the jinko-sdk. Use this skill whenever the user wants to upload a vpop from CSV or pandas DataFrame, create a vpop generator from marginal distributions, generate a vpop from a vpop design, inspect vpop content/statistics, or edit an existing vpop design. Vpops generated or uploaded as Vpop project items are not editable; edit the vpop design instead and regenerate.
compatibility: >-
   Check set-up with the `jinko-sdk-setup` skill. Creating vpops or vpop designs requires write access to the Jinkō project. DataFrame creation requires pandas.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Jinkō Vpop SDK Workflows

Use this skill for technical vpop and vpop-design workflows through the SDK. Keep distribution guidance minimal; use the allowed distribution shapes in `assets/distrib.json` and defer deeper distribution design to a dedicated distribution skill when available.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

## Core Rules

- Use `client.create_vpop_from_csv()` or `client.create_vpop_from_dataframe()` for direct vpop upload.
- Use `client.create_vpop_design_from_design()` for marginal-distribution vpop designs.
- Use `design.generate_vpop()` to generate an immutable Vpop from a `VpopDesign`.
- Check `design.diagnostics` (or `design.get_sanity()`) before generating, and fix reported errors first.
- Edit an existing design's descriptors/correlations with `design.descriptors` (`create*`/`set_distribution*`) and `design.correlations`, not by replacing the raw payload.
- Treat Vpop project items as generated/uploaded artifacts that are not edited in place.
- Edit vpop designs, not generated vpops, then regenerate a new vpop.
- Require explicit confirmation or script `--apply` before creating or updating project items.
- Descriptor IDs in CSV headers and marginal designs must match real model component IDs when the vpop will be used with that model.
- Reject duplicate descriptor IDs in marginal lists; converting duplicates to a mapping would otherwise silently discard earlier entries.

## Project Folder Hygiene

- Prefer creating vpops and vpop designs inside a dedicated Jinkō folder instead of the project root. At the start of a workflow, ask for or propose a folder name, for example `YYYY-MM-DD-<experiment-name>`.
- Reuse an existing exact-match folder when possible: `client.get_folder_by_name(name, exact_match_only=True)`.
- If the folder does not exist, create it only after user confirmation or when a script is run with `--apply`.
- Resolve one folder object or folder id, then pass `folder=folder` to SDK creation calls that support it.

## Bundled Assets

- `assets/toy_vpop.csv`: two-patient vpop CSV using the toy model descriptors `Dose` and `k_elim`.
- `assets/toy_marginals.json`: list-of-marginals vpop design for `Dose` and `k_elim`.
- `assets/distrib.json`: source of truth for admissible marginal distribution shapes.

## SDK Scripts

Use scripts rather than embedding long Python examples in chat. These are on
`PATH` as console scripts once the SDK is installed, and also runnable via
`python -m` as shown below.

- `jinko.cli.create_vpop_from_csv`: uploads a CSV directly, or via pandas DataFrame with `--method dataframe`.
- `jinko.cli.create_vpop_design_from_design`: creates a vpop design from a list of unique `{ "id": ..., "distribution": ... }` entries and can optionally generate a vpop after diagnostics pass.
- `jinko.cli.inspect_vpop`: inspects content, description, or statistics for an existing vpop.
- `jinko.cli.edit_vpop_design`: updates or adds descriptors sequentially, reports already-applied IDs if a later edit fails, and runs post-edit diagnostics before success.

Examples:

```bash
python -m jinko.cli.create_vpop_from_csv --csv skills/jinko-vpop/assets/toy_vpop.csv
python -m jinko.cli.create_vpop_from_csv --csv skills/jinko-vpop/assets/toy_vpop.csv --apply
python -m jinko.cli.create_vpop_from_csv --csv skills/jinko-vpop/assets/toy_vpop.csv --folder 2026-06-15-vpop-study --create-folder --apply
python -m jinko.cli.create_vpop_design_from_design --design skills/jinko-vpop/assets/toy_marginals.json --model-sid cm-... --apply --generate
python -m jinko.cli.inspect_vpop --vpop-sid vp-... --statistics --correlations
python -m jinko.cli.edit_vpop_design --vpop-design-sid vd-... --design skills/jinko-vpop/assets/toy_marginals.json --apply
```

## CSV Upload Pattern

The minimal CSV shape is one row per patient:

```csv
patientIndex,Dose,k_elim
1,1.0,0.08
2,1.2,0.12
```

Use actual component IDs, not biological labels such as `age` or `weight`, when the vpop is meant to drive a model.

## Marginal Design Pattern

Use a list of marginal entries in skill assets and scripts:

```json
[
  {"id": "Dose", "distribution": {"tag": "Uniform", "lowBound": 0.8, "highBound": 1.2}},
  {"id": "k_elim", "distribution": {"tag": "NormalTruncated", "mean": 0.1, "stdev": 0.02, "lowBound": 0.01, "highBound": 0.3}}
]
```

The script converts this list to the SDK mapping expected by `create_vpop_design_from_design(marginal_distributions=...)`.

## Reference Routing

- Read `references/csv-vpop.md` for direct CSV/DataFrame upload details.
- Read `references/vpop-design.md` for marginal vpop design and generation details.
- Read `assets/distrib.json` before adding or changing marginal distribution shapes.
