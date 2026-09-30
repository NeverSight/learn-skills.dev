---
name: arcgis-pro-automation
description: >-
  Automate controlled local ArcGIS Pro and ArcPy workflows through
  arcgis-mcp-bridge: inspect .aprx projects and file geodatabases, run
  geoprocessing, projection, raster, network, spatial-statistics, editing,
  symbology, and layout export with path and mutation guards. Use when the
  user explicitly names ArcGIS Pro, ArcPy, .aprx, .gdb, Esri geoprocessing,
  muend/arcgis-mcp-bridge, its health_check, PathGuard, or confirmation
  gates, or sketch-to-GIS extraction. Do not trigger for ArcGIS Online or
  Enterprise administration, QGIS or PyQGIS, generic open-source GIS, or
  live GUI control of an already-open ArcGIS Pro session.
license: MIT
metadata:
  author: Muhammed Enes Duran
---

# ArcGIS Pro Automation

Operate saved ArcGIS Pro projects and local GIS datasets through the guarded
`arcgis-mcp-bridge` tool surface. Treat the bridge as an execution backend,
not as permission to mutate data or claim a result that was never observed.

## Establish the boundary

- Require Windows, a licensed ArcGIS Pro installation, and a bridge worker
  interpreter that can import ArcPy for real geoprocessing.
- Use the bridge for local, headless, repeatable ArcPy work. It does not drive
  the visible ArcGIS Pro UI and does not administer ArcGIS Online or Enterprise.
- If the bridge tools are not callable, provide setup or a dry execution plan.
  Never simulate tool output or imply that an `.aprx` or `.gdb` changed.
- Use the schemas exposed by the connected MCP server. Tool names may be host-
  namespaced; match the semantic catalog name and never invent parameters.
- Keep every read and write inside the configured allowed roots. Use absolute
  paths and a dedicated scratch geodatabase for intermediate outputs.

Read [runtime and licensing](references/runtime-and-licensing.md) before the
first execution or whenever setup, extension availability, or worker failures
are in scope.

## Execute the workflow

1. **Define the contract.** Identify inputs, intended output artifacts, CRS and
   units, whether a saved `.aprx` must change, and which operations create,
   overwrite, append, or edit data.
2. **Preflight.** Call `health_check` first. Inspect its worker interpreter,
   allowed roots, scratch GDB, timeout, and concurrency. Because this call does
   not import ArcPy, follow it with a non-mutating ArcPy-backed request such as
   `get_spatial_reference`, `describe_dataset`, or `list_layers` before treating
   the runtime as execution-ready.
3. **Inspect before acting.** Read dataset descriptions, counts, fields, CRS,
   extents, project maps/layers, and required extension licenses. Resolve datum
   transformations, units, and output naming before analysis.
4. **Plan exact tools.** Select the smallest declarative sequence from
   [tool routing](references/tool-routing.md). Separate read-only inspection,
   new-output creation, and in-place mutation. Prefer new outputs and working
   copies over edits to source data.
5. **Authorize mutations.** Read [safety and validation](references/safety-and-validation.md)
   before any write. Set `confirm=true` only when the user's request clearly
   authorizes the exact mutating operation and target. Treat `overwrite=true`
   as a separate explicit decision. Stop on ambiguous target, scope, or intent.
6. **Execute incrementally.** Run one dependent step at a time; preserve returned
   output paths and geoprocessing messages. Parallelize only independent jobs
   when license seats, memory, and `max_workers` are known to support them.
7. **Verify independently.** Re-open outputs and test the relevant invariants:
   existence, count, geometry validity, CRS and units, raster statistics and
   NoData, network solve status, project contents, or exported layout dimensions.
   A success status alone is not evidence of a correct GIS result.

## Route domain method and execution separately

Use this skill for the ArcGIS execution layer. Pair it with the relevant domain
skill when method choice or scientific validity is substantive:

- DEM, slope, drainage, or viewsheds → `terrain-hydrology`
- routing, service areas, OD, or facilities → `network-accessibility-analysis`
- Moran's I, Gi*, kernel density, or spatial inference → `spatial-statistics`
- raster/imagery preprocessing and interpretation → `remote-sensing-analysis`
- map design before `.aprx` styling or layout export → `cartography-geoviz`
- multi-stage cross-domain delivery → `geoai-orchestrator`

Do not activate ArcGIS automation merely because an open format can be read by
ArcGIS. A GeoPackage, GeoJSON, raster, or `.gdb` request that explicitly chooses
GDAL, GeoPandas, QGIS, PostGIS, or another runtime belongs to that specialist.

## Handle failures without bypasses

- `validation`: correct the payload against the live schema; do not relax types.
- `security`: move or copy only with user authorization; never broaden allowed
  roots merely to make a call pass.
- `license`: report the unavailable base or extension license. Use an alternative
  only when it is methodologically equivalent and disclose the change.
- `geoprocessing`: preserve ArcPy messages, inspect inputs/environment, and retry
  only after a concrete correction. Never retry an in-place mutation blindly.
- `internal` or worker crash: preserve the error boundary and stop claiming state.

## Deliver evidence

Report the tool sequence, inspected inputs, exact output paths, mutations and
authorization basis, relevant ArcPy messages, verification results, license and
runtime constraints, and unresolved limitations. For current tool or platform
claims, consult [the authoritative source registry](references/authoritative-sources.md)
and record the checked date.

## Execution contract

- **Workflow:** establish the local ArcGIS boundary; preflight server and ArcPy separately; inspect data and project state; plan exact tools; authorize writes; execute incrementally; reopen and verify outputs.
- **Decision rules:** use the bridge only for explicit local ArcGIS Pro or ArcPy work, pair it with domain-method skills when needed, prefer new outputs, and reserve confirmation and overwrite flags for clearly authorized targets.
- **Verification protocol:** reconcile counts, geometry, CRS and units, raster or network diagnostics, `.aprx` contents, exported artifacts, returned paths, and geoprocessing messages against the stated success criteria.
- **Failure modes:** stop for absent bridge tools, failed ArcPy preflight, unknown CRS or datum transform, paths outside allowed roots, missing licenses, ambiguous mutation scope, worker crashes, or unverified output state.
- **Deliverables:** reproducible tool plan and calls, exact inputs and outputs, mutation record, ArcPy messages, validation evidence, runtime and license provenance, and limitations.
- **Source freshness:** consult [the authoritative source registry](references/authoritative-sources.md) before applying bridge, ArcPy, licensing, or platform rules and record the checked date.
