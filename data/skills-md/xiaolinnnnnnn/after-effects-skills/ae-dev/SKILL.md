---
name: ae-dev
description: Build, inspect, automate, and troubleshoot Adobe After Effects projects using ExtendScript/JSX and Computer Use. Use when the user says AE Generation, After Effects scripting, AE automation, create AE animation, render AE output, write JSX, control AE 2025, generate shape/text/keyframe/effect animations, or fix AE script errors.
---

# AE Development

## Core Workflow

Use this skill to control After Effects through JSX first, then use Computer Use only to verify the visible UI, dismiss non-risky AE dialogs, or inspect the comp viewer.

1. Confirm the target AE path. On this machine prefer `D:\AE2025\Adobe After Effects 2025\Support Files\AfterFX.com`.
2. Create or patch a `.jsx` script in the workspace. Use UTF-8. Keep syntax ExtendScript-safe: `var`, function declarations, no modern JS-only syntax unless verified in AE.
3. Wrap all project mutations in `app.beginUndoGroup("...")` / `app.endUndoGroup()` and `try/catch`; always write a log file before claiming success.
4. Execute with `scripts/run-ae-script.ps1 -ScriptPath <path-to-jsx>`. The official docs describe `afterfx -r <script.jsx>` as running the script in the existing AE instance.
5. Verify by checking expected output files, log contents, project save path, and optionally the AE window via Computer Use.
6. For animation work, create editable comps and named layers; avoid flattening everything into footage unless the user asked for final render only.

## Required References

Load these only as needed:

- `references/official-guide.md`: condensed official AE scripting guide, object model, workflow, imports, rendering, keyframes, text, and common failure modes.
- `references/match-names.md`: high-value match names for transforms, shape layers, text, effects, and safe effect-property inspection.
- `references/common-jsx-control-scripts.md`: detailed extraction of the local `assets/` JSX library, including all 164 scripts organized under subfolders (Compositions, Expressions, Keyframes, Layers, etc.) and reusable AE control recipes.
- `assets/templates/safe-ae-script-template.jsx`: starting template for robust AE scripts with logging, undo handling, property helpers, shape/text helpers, and keyframe easing.

## Reliability Rules

- Prefer match names over localized display names. Examples: `ADBE Transform Group`, `ADBE Position`, `ADBE Scale`, `ADBE Rotate Z`, `ADBE Opacity`, `ADBE Root Vectors Group`.
- Never guess effect child-property indexes. Add the effect by match name, dump its child properties with `property(i).name`, `matchName`, and `propertyValueType`, then set values.
- Check every property lookup before calling `setValue`, `setValueAtTime`, or `setTemporalEaseAtKey`. A null property causes `TypeError: null is not an object`.
- Use `setValue()` only for static properties with no keyframes; use `setValueAtTime()` for animated properties.
- Build `KeyframeEase` arrays with the correct dimensionality: one object for scalar/color/text-like values, two for 2D, three for 3D.
- Use 1-based AE collection indexes: `project.item(1)`, `layer.property(1)`, key indexes `1..numKeys`.
- Avoid scripts that depend on UI language. Chinese AE menus and English docs differ; match names are stable.
- Do not use `app.executeCommand()` unless no API exists, and record the menu command id source in the script comment.
- Preserve existing user work unless the user explicitly asked for a fresh project. Put generated assets in a clearly named folder and save to an explicit `.aep` path.
- If the script needs file writing and fails silently, verify AE Preferences > General > "Allow Scripts To Write Files And Access Network" is enabled. Do not change that setting through UI automation unless the user confirms.

## AE Generation Defaults

For "AE Generation" or similar requests, create a 1920x1080, 30 fps, 6-10 second comp with:

- a named project folder and named comp
- background solid or shape-based color field
- shape layers for rectangles, ellipses, strokes, trim paths, or orbit dots
- title/subtitle text with `TextDocument` settings
- Position/Scale/Opacity/Rotation keyframes with Bezier interpolation and temporal ease
- optional preview PNG or saved `.aep`

Prefer shape layers and text layers over raster assets for editability. Use visual assets or imported footage when the brief calls for a real product, person, logo, or reference image.

## Validation Checklist

Before final response:

- The JSX file exists and was executed through AE.
- The AE log says `Saved project` or records the intended final action.
- The output `.aep`, `.png`, or render exists when requested.
- The AE window title or project panel shows the generated comp if visual verification was possible.
- Any remaining limitation is explicit, such as a skipped effect because child properties need inspection.
