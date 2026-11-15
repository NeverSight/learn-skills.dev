---
name: jinko-trial-viz
description: >-
  Create, update, inspect, sanity-check, and retrieve Jinkō TrialVisualization project items for completed or running trials. Use this skill whenever the user wants a trial visualization, trial viz, time-series plot setup, scalar result plots, scatter plots, contribution analysis, survival analysis, data overlays, or to fetch the current visualization JSON. The SDK exposes a typed TrialVisualization API: creation helpers plus a per-section subservice for every plot type.
compatibility: >-
  Check set-up with the `jinko-sdk-setup` skill. Creating or patching trial visualizations requires write access to the Jinkō project.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.16,<2.0"
license: MIT
---

# Jinkō Trial Visualization Workflows

Use this skill for TrialVisualization project items: creating a visualization for a trial, configuring plot sections, retrieving the stored visualization payload, and running visualization sanity checks.

Keep trial execution, result downloads, and calculated plot data (`trial.results.aggregate_*`) in `jinko-trial`; do not create a visualization only to read data. Use this skill after a trial exists and the user wants the Jinkō visualization artifact or its plot configuration.

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. A
> session code can be exchanged only once, so call `get_session_code` again
> before this skill's own SDK process. If that skill is not found, install it
> from `novainsilico/jinko-skills`.

## Core Workflow

1. Resolve the trial: `trial = client.get_trial(trial_sid)`.
2. After explicit user confirmation, create an empty visualization bound to the trial: `viz = trial.create_empty_trial_visualization(folder=..., name=..., description=...)`.
3. Decide the plot sections needed and configure each through its typed subservice:
   - `viz.timeseries` for time-course outputs.
   - `viz.scalars` for scalar result distributions and central-location plots.
   - `viz.scatter_plots` for X-vs-X arms or X-vs-Y variables.
   - `viz.survival_analysis` for time-to-event visualizations.
   - `viz.contribution_analysis` for tornado-style sensitivity/contribution views.
   - `viz.data_overlay` / `viz.patients_overlay` when observed data or patient-level data should appear.
   - `viz.filters` / `viz.groups` for scoping and grouping.
   - `viz.set_selected_arms(...)`, `viz.set_equate_baseline(...)`, `viz.set_time_unit(...)` for top-level options.
4. Run and print `viz.sanity` after every create or update. Return failure and fix the visualization when it reports errors.
5. Reconfigure a section at any time by calling its setter again (e.g. `viz.timeseries.set_selectors([...])`) — each call patches only that section.

## SDK Surface

- `trial.create_empty_trial_visualization(folder=, name=, description=, version=)` and `trial.create_trial_visualization_from_json(data, ...)` — creation, bound to a trial.
- `client.list_trial_visualizations(...)`, `client.iter_trial_visualizations(...)`, `client.get_trial_visualization(sid)` — metadata lookup.
- `viz.content(revision=...)` — full typed content; `viz.sanity` / `viz.sanity_at(revision, only=[...])` — diagnostics (`.errors()`, `.warnings()`, `.has_errors()`, `.for_field(...)`, `.by_field()`).
- Section subservices, each with `get()`/`clear()` plus section-specific setters: `viz.timeseries.set_selectors(...)`/`add_selectors(...)`, `viz.scalars.set_selectors(...)`/`add_selectors(...)`, `viz.survival_analysis.set_selectors(...)`/`set_observation_window_from_start_until_end(...)`/`set_observation_window_from_start_until_time(...)`/`set_confidence_interval(...)`, `viz.contribution_analysis.set_selectors(...)`/`set_quantile(...)`/`set_input_baseline_only(...)`/`set_all_baseline(...)`/`set_custom_baseline(...)`, `viz.scatter_plots.add_x_vs_x_plot(...)`/`add_x_vs_y_plot(...)`/`set_config(...)`/`set_regression(...)`, `viz.data_overlay.add_table(...)`/`set_tables(...)`/`set_ranges_enabled(...)`, `viz.filters.add_numeric(...)`/`add_categorical(...)`/`add_patient_list(...)`, `viz.groups.set_group_by_arm(...)`/`add_scalar_*_grouping(...)`/`add_categorical_grouping(...)`.

Read `references/trial-viz-typed-api.md` for full examples of each subservice.

## SDK Script

Use the script for repeatable create, update, get, list, and sanity operations
through the typed API. It is on `PATH` as a console script once the SDK is
installed, and also runnable via `python -m` as shown below.

```bash
python -m jinko.cli.trial_viz list --limit 20
python -m jinko.cli.trial_viz create --trial-sid tr-... --name "My trial viz" --timeseries Drug --scalar AUC
python -m jinko.cli.trial_viz create --trial-sid tr-... --name "My trial viz" --timeseries Drug --scalar AUC --apply
python -m jinko.cli.trial_viz get --trial-viz-sid tv-... --output-file viz.content.json
python -m jinko.cli.trial_viz update --trial-viz-sid tv-... --scatter-xvsy "AUC,Cmax,control,treated" --apply
python -m jinko.cli.trial_viz sanity --trial-viz-sid tv-... --only timeseries --only scatterPlots
```

For scatter, overlay, filter, or grouping configuration beyond the script's flags, use the typed subservices directly in Python (see `references/trial-viz-typed-api.md`).

## Project Folder Hygiene

- Prefer creating trial visualizations in the same folder as the trial or in a dedicated analysis folder.
- Pass a folder id or exact folder name through the script's `--folder`, or `folder=folder` on `create_empty_trial_visualization(...)` directly.
- Treat an explicit folder that cannot be resolved as an error; never silently create the visualization in the project root.
- Reuse existing trial visualizations when the user wants an additional plot on the same analysis; call the relevant section's setter instead of creating duplicates.

## Reference Routing

- Read `references/trial-viz-typed-api.md` for the typed subservice API.

## Output Expectations

When creating or modifying a visualization, report:

- TrialVisualization SID, core item id, snapshot id, revision when available, and URL when available.
- Plot sections created or patched.
- Any sanity errors or warnings, preserving the backend field names so the next fix is direct.

When retrieving a visualization, return or save the full JSON content if the user needs to inspect, diff, or reuse plot settings.
