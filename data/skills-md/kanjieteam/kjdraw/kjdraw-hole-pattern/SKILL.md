---
name: kjdraw-hole-pattern
description: Create a reviewable 2D circular pattern of equal round holes in KJD or DXF from explicitly supplied center, pitch diameter, hole diameter, count, first-hole direction and drawing units, using KJDraw native polar arrays. Use for mechanical hole-layout drafting, not a complete flange or manufacturing certification.
---

# Circular hole pattern

Draft only the requested holes in native model-space XY geometry. Use the existing KJDraw CAD core; this package contains no geometry engine, template matcher or dependency on another Skill.

## Inputs and runtime

Obtain the workspace, new or existing drawing, center `(cx, cy)`, pitch-circle diameter `D`, hole diameter `d`, integer hole count `N`, and first-hole angle or unambiguous direction. Require explicit drawing units and a defined angle convention; convert a supplied direction to degrees from +X, counterclockwise. Do not assume origin, first angle, units or a drilling standard. Missing facts need clarification before a creation call. This workflow accepts `millimeter` or `meter`, `D > 0`, `d > 0`, and `2 <= N <= 512`; values must be finite. Coordinates, radii and expanded centers must satisfy the installed schema and native numeric range. Unsupported values are reported, never clipped or replaced.

Use an installed `kjdraw` CLI and `kjdraw-review` with a terminal. In a KJDraw checkout, substitute `node packages/kjdraw-sdk/bin/kjdraw.mjs` and `node packages/kjdraw-sdk/bin/kjdraw-review.mjs`. Installing the Skill does not install CAD tools. Inspect the installed `cad_propose_drawing_pattern` schema with `kjdraw agent tools cad_propose_drawing_pattern --units <millimeter|meter>`; stop if native `polarArrays` or host review is unavailable. Reuse already inspected schemas for the same runtime and unit binding.

For existing KJD, use `kjdraw inspect <source.kjd>` once to obtain the actual revision and units; all supplied lengths must use those units. Unknown units or a mismatch cannot be resolved by assuming a scale. For existing DXF, record its byte digest and import once with `kjdraw convert <source.dxf> <new-scratch/source.kjd>` into a fresh workspace directory. Check that the output is absent before conversion: `convert` can overwrite files. Inspect that immutable KJD snapshot, then use it for every proposal and review. Independent CLI DXF imports regenerate document/owner/object IDs; a DXF ledger cannot safely be reviewed as if those IDs were stable. Preserve both original and snapshot bytes. Conversion covers supported imported records; the CLI does not provide proof of lossless import. If scratch files are forbidden, report this limitation.

For a new drawing, use `--blank <new-relative-source.kjd> --units <explicit-units>` with `expectedRevision: 0`; the CLI creates an immutable blank baseline, then a proposal. Validate inputs before this call. A blank baseline or empty ledger left by a failed call is not a completed drawing.

## One native proposal

Let `R = D/2`, `r = d/2`, normalize the supplied angle modulo 360 and convert it to radians `a`. Calculate only the seed input `(sx, sy) = (cx + R*cos(a), cy + R*sin(a))`; simple deterministic arithmetic is allowed for this input planning. KJDraw performs all copies, IDs, previews, transactions and exports. Do not expand the holes in a script or repeat primitive calls.

Create a new workspace JSON argument file with the actual revision and units:

```json
{
  "expectedRevision": 0,
  "units": "millimeter",
  "lines": [],
  "circles": [[10, 40, 2]],
  "arcs": [],
  "polylines": [],
  "arrays": [],
  "polarArrays": [{"sources": ["circles:0"], "center": {"x": 10, "y": 20}, "count": 8, "angleDegrees": 360}]
}
```

This example means center `(10,20)`, pitch diameter `40`, hole diameter `4`, eight holes, first angle `90°` from +X counterclockwise, all lengths in millimeters. Replace these facts for the current request. `circles` stores radius, not diameter. `sources` is a zero-based reference within the proposal's circle group, not an existing drawing object ID. The full-circle `count` includes the seed; `360/N` spacing produces exactly `N` circles without a duplicate endpoint. `angleDegrees: 360` is the sweep, not the first-hole angle. Keep all other groups empty; do not add a pitch circle, flange body, center lines, notes, dimensions or material data without a separate request.

Call `kjdraw agent call cad_propose_drawing_pattern --input <relative-source.kjd> --args-file <relative-request.json> --workspace <absolute-workspace>` once; for a new drawing replace `--input` with the blank options above. Inspect the complete native preview in the returned ledger: exactly `N` new `CIRCLE` objects, distinct centers on radius `R`, circle radius `r`, and the requested orientation. Stop on error, stale revision, omitted evidence or numeric loss of distinct centers; preserve the source and report the actual failure. A successful proposal must remain `awaiting-host-approval`, with no source mutation.

## Review and evidence

Read [acceptance cases](references/acceptance.md) before reporting a completed candidate or validating this contribution. Return the source/snapshot digest, revision, supplied facts, tool name, native count/geometry checks, ledger path and actual proposal sequence. A preview or model statement is not approval.

When the caller wants a candidate, give the authorized host this command using the actual ledger, sequence and an unused candidate stem whose parent directory already exists:

```sh
kjdraw-review --workspace <absolute-workspace> --ledger <returned-relative-ledger.json> --sequence <returned-sequence> --candidate <new-relative-candidate.kjd> --approve
```

The human runs it in an independent interactive terminal and reviews the exact preview. Never answer, pipe or automate its `KJDRAW` challenge; `--approve` alone does not confirm it. Host review handles native `CREATEBATCH`, creates new KJD/DXF/receipt files, independently reopens them and checks live undo/redo. It never overwrites the source. Do not manufacture a host receipt or call a trusted SDK approval method from the model.

After a real receipt, verify the requested dimensions in reopened output using available native `cad_read_drawing`/`cad_query_drawing` tools as described in the acceptance reference. Discover their installed schemas only when needed. Report missing checks explicitly; host review's DXF type counts alone do not prove circle positions/radii. Keep “awaiting review”, “host-created candidate”, and “geometry verified” distinct. KJD retains native objects; DXF interchange is not a promise to retain every group or source metadata. No strength, clearance, thread size, drilling tolerance or compliance conclusion follows from these circles.
