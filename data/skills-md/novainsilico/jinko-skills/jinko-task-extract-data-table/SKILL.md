---
name: jinko-task-extract-data-table
description: >-
  Extract or digitize reported biomedical values from papers, figures, tables,
  supplements, images, or web sources into traceable CSV/Markdown, optionally as
  a calibration-ready Jinkō data table. Use when numeric evidence must be
  transcribed, normalized, unit-converted, or bound to model observables. Do not
  use for literature discovery, evidence synthesis, or inventing values absent
  from the source.
compatibility: >-
  Jinkō upload requires jinko-sdk-setup and project write access. Extraction from
  images or PDFs requires a suitable reader, OCR, or digitization tool.
metadata:
  author: Nova In Silico
  requires_sdk: ">=1.10,<2.0"
license: MIT
---

# Extract Data Table

> **PREREQUISITE:** This skill needs an initialized `jinko-sdk` connection and an
> SDK satisfying its `metadata.requires_sdk` range. Run the `jinko-sdk-setup` skill
> (`../jinko-sdk-setup/SKILL.md`) and proceed only once its check passes. If that
> skill is not found, install it from `novainsilico/jinko-skills`.

Preserve what the source reports. Keep estimated, transformed, and directly
transcribed values distinguishable.

## Inputs

Require the source artifact and the requested series. For a Jinkō-ready output,
also require the target `obsId` mapping, model units, and any scenario/arm scope.
Ask for missing mappings rather than guessing them.

## Workflow

1. Locate each requested series and record its citation plus page, table, figure,
   panel, or supplement. Prefer machine-readable tables over OCR and OCR over
   graphical digitization. If no suitable extraction tool is available, request
   a tabular source instead of estimating visually.
2. Extract only reported values. For graphical digitization, retain the raw
   digitized points and identify them as estimates. Do not fit, smooth, aggregate,
   or impute unless explicitly requested; record any such transformation.
3. Preserve the reported statistic. Do not interchange raw values, means,
   medians, SD, SE, confidence intervals, IQR, or min/max. Convert units only when
   the source and target units are known, recording the formula and original
   values. Express Jinkō time values as ISO-8601 durations.
4. For general extraction, emit a readable CSV or Markdown table with series,
   time/condition, value or bounds, unit, and source locator.
5. For Jinkō output, follow the row schema owned by `jinko-data-table`. Use point
   rows for reported point values and range rows only for reported lower/upper
   bounds. Set `obsId`, `armScope`, `unit`, and `experimentRef` explicitly.
6. Run the `jinko-data-table` creation script in dry-run mode with the expected
   `--allowed-obs-id` values, `--require-unit`, and `--require-experiment-ref`.
   On approval, add `--require-fitness --apply`. The script owns row/schema
   checks, upload, and the server `validForFitnessFunction` gate.

## Return

Return the extracted file and a compact report containing:

- source locator and extraction method for each series;
- original statistic, units, and any transformations or conversions;
- assumptions, unreadable values, and digitization uncertainty;
- for Jinkō output, data-table SID, URL, observable mapping, and confirmed
  `validForFitnessFunction: True`.

If the server does not explicitly report fitness compatibility as true, return
the table as not calibration-ready. Never silently replace or manufacture values
to make a table pass validation.
