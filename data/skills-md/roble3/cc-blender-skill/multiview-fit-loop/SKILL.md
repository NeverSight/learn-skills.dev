---
name: multiview-fit-loop
description: Closed-loop compare-adjust-repeat workflow for fitting Blender models to supplied front/side/back/top templates and originals. Use when the user asks to compare the product to templates/originals and adjust until it fits across all dimensions, or when all views must pass measurable bbox/centroid/silhouette/edge validation before export.
when_to_use: Multi-view validation and iterative fitting against reference templates, all-dimension mascot/object reconstruction, front/side/back/top overlay reports, fit deltas, automated adjustment loops.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info
---

# Multiview Fit Loop

This skill closes the missing loop: **render → compare → adjust → render again**. It is mandatory when a user says the model still does not fit the templates/originals.

## Required loop

1. Render flat, material-independent silhouettes for every available template view: front, side, back, top.
2. Extract the template object mask, excluding labels, cyan guides, and background.
3. Compare template vs render per view:
   - bbox center and size
   - centroid drift
   - silhouette coverage/IoU where modality is valid
   - visual overlay
4. Convert measured deltas into model/camera/recipe adjustments.
5. Rebuild or transform the model.
6. Repeat until all hard gates pass or document the remaining conflict.

## Constraint inconsistency gate

Before forcing adjustments, check whether the supplied orthographic templates are mutually consistent. A single rigid 3D model cannot simultaneously satisfy contradictory physical ratios, for example if side view says total depth is 0.39 of height but top view says depth is 0.98 of width. When this occurs, stop claiming final fit, write a conflict report, and create separate variants or ask which view is canonical.

## Hard gates

- all required views have validation reports and overlays;
- bbox center drift <= 1.5% of image width;
- bbox size drift <= 3% for front, <= 5% for side/top/back first-pass depth;
- structural part count exact;
- texture UV regions still valid after geometry changes.

## View mask rule

For annotated wireframes, choose a template mask mode that isolates the intended construction/object lines and excludes guide colors, labels, captions, and background annotations. For Blender validation renders, use a flat white silhouette on black, not beauty renders with glow/context elements.

## Scripts

- `scripts/multiview_fit_report.py` compares view pairs and writes JSON + overlays.

## Adjustment rule

Prefer changing recipe parameters or source geometry over camera scale tricks. Camera scale may be used only after model dimensions are correct.
