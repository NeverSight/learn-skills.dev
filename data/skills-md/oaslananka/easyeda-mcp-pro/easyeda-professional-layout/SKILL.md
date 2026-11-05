---
name: easyeda-professional-layout
description: Plan, preview, apply, and verify professional EasyEDA Pro schematic layouts with page/title-block geometry, rendered bounds, functional blocks, relationship-aware spacing, deterministic templates, staged readback, connectivity fingerprints, and visual QA. Use for schematic placement, cleanup, fit-to-page work, or any request to make a schematic professional or readable.
---

# EasyEDA Professional Layout

Use this skill for schematic layout work through EasyEDA MCP Pro. Treat layout as a constrained engineering workflow, not coordinate styling. Read-only inspection may start immediately; request the user's explicit approval before the first schematic write.

## Engineering evidence handoff

For schematic placement following component/datasheet review or before power,
PCB routing and DRC validation, use the existing staged router at
`skills/design-validation/references/engineering-review.md`. This
layout skill enforces geometry/preview/write/readback discipline and never
authenticates pin electrical limits, live pad-net continuity, physical
high-frequency return paths or a manufacturer's process profile. Do not
promote suggested proximity or model-guessed geometry into electrical proof.

## Non-negotiable policies

- `PAGE_GEOMETRY_REQUIRED`: read health, bridge, project, active document, sheet bounds, drawable bounds, grid, frame, coordinate origin, and title-block bounds before any placement write.
- `TITLE_BLOCK_KEEP_OUT`: title block, border margin, and caller-reserved regions are hard constraints. Never downgrade them to score penalties.
- `RENDERED_BOUNDS_ONLY`: collision and page-fit decisions use rotation-aware combined symbol and text bounds. Component origins are not collision bounds.
- `NO_BLIND_RETRY`: a timeout is ambiguous. Read back real state before deciding whether any write should be retried.
- `STAGED_PREVIEW_READBACK_QA`: preview and validate every batch, then read back and run layout QA before proceeding.
- `CONNECTIVITY_FINGERPRINT_REQUIRED`: cosmetic moves require matching component-pin net membership and wire endpoints before and after.
- `NO_SAVE_WITH_CRITICALS`: do not save while any critical page, title-block, overlap, or connectivity violation remains. Return blockers instead.

If sheet, rendered primitive, or title-block geometry is unavailable, stop with `LAYOUT_GEOMETRY_REQUIRED`. Templates remain advisory and must never substitute guessed coordinates.

## Numeric defaults

Defaults use EasyEDA schematic mil coordinates. Runtime units and grid remain authoritative; convert explicitly when they differ.

| Constraint                            | Default |
| ------------------------------------- | ------: |
| Page-border clearance                 | 100 mil |
| Title-block margin                    | 150 mil |
| Component-to-component clearance      |  50 mil |
| Text-to-body/text clearance           |  25 mil |
| Section-to-circuit clearance          |  75 mil |
| Decoupling-to-parent maximum          | 200 mil |
| Crystal/load-to-parent maximum        | 150 mil |
| Connector-protection maximum          | 250 mil |
| Bulk-capacitor-to-power-stage maximum | 350 mil |

Use stricter caller constraints when provided. Approximate/derived geometry may guide a preview, but it cannot authorize placement without an explicit low-confidence result and human review.

## Mandatory workflow

1. Read health, bridge status, active project/document, sheet geometry, grid, frame, title block, and coordinate origin.
2. Inventory every required component, net, connector, support relationship, and existing occupied region before placing anything.
3. Resolve rotation-aware symbol/body/reference/value/pin/label bounds. Reserve support-component space around parent devices.
4. Create hard border/title-block/caller keep-outs and named functional-block regions.
5. Select a versioned template from `src/professional-layout-templates/index.ts`; generate a deterministic placement plan and inspect all conflicts, reservations, page attempts, and componentized scores.
6. Preview main-component placement. Apply only after the write gate, then read back rendered bounds and run placement QA. Repeat for support components.
7. Wire only after placement QA has zero critical issues. Prefer visible orthogonal local connections; detached netports are not acceptable in normal circuit workflows.
8. Run a cosmetic-only cleanup preview for alignment, spacing, labels, and wire length. Do not alter electrical intent.
9. Capture a connectivity fingerprint immediately before cleanup and compare it after every cosmetic batch. Roll back any mismatch.
10. Run geometric QA, netlist/ERC validation, full-page fit capture, and visual QA. Inspect issue codes and every critical score dimension, not only the aggregate score.
11. Save only when critical violations are zero. Otherwise return the exact blockers, affected regions, confidence, and next safe action.

## Stage gates

For each write batch, record:

- preview input, deterministic plan hash, selected page size, and hard-constraint result
- intended primitive IDs or component references
- apply result and ambiguous timeout state
- readback bounds and changed region
- geometric/layout issue codes and per-dimension scores
- connectivity fingerprint comparison when the change is cosmetic

A4 is preferred. A3 fallback is permitted only after a deterministic A4 attempt proves hard constraints cannot be satisfied. Never enlarge the page only to hide excessive whitespace or poor grouping.

## Templates

The versioned catalog includes:

- USB-powered MCU board
- ESP32 sensor node
- battery-powered IoT node
- CAN/RS-485 interface
- simple analog/timer circuit
- medium-complexity MCU peripheral board

Templates define signal flow, block order, keep-outs, clearances, support proximity, and A4/A3 policy. They do not define device-specific electrical design or replace MCP-side enforcement.

## Output contract

Report the selected template/version, geometry source/confidence, plan hash, page-size decision, placed/read-back bounds, issue codes/counts, componentized scores, changed regions, fingerprint result, rollback state, and remaining human-review items. Automated success is not production approval.

See [professional schematic layout](../../docs/professional-schematic-layout.md) for the operator prompt and worked example. See [schematic layout benchmarks](../../docs/schematic-layout-benchmarks.md) before updating golden fixtures.
