---
name: spatial-sql
description: "Write, review, debug or optimize spatial SQL on an already chosen engine, including DuckDB Spatial, PostGIS, BigQuery GIS, Snowflake and Sedona. Use for spatial predicates, joins, indexes, query plans, CRS and metric/geodesic correctness. Route unresolved engine or cross-system architecture choices to open-map-stack; ordinary non-spatial SQL and casual place questions are outside this skill."
metadata:
  version: "0.4.0"
---

# Spatial SQL

Solve the query in the engine the user has chosen. Read
`references/spatial-sql.md` for the relevant engine and query patterns, and
`references/formats-and-crs.md` when coordinate or format semantics matter.

## Query workflow

1. Establish the engine/version, available spatial functions, geometry versus
   geography types, CRS/SRID, input grain, expected result and scale. Inspect
   the existing query and plan when available. Do not assume different engines
   share function signatures, boundary semantics or index behavior.
2. Express the intended spatial relationship precisely. Resolve intersects
   versus contains/covers, boundary inclusion, null/empty/invalid geometries,
   and whether several spatial matches should duplicate an entity or produce
   a single membership result.
3. Make distance, area and buffers use the intended units and method. A
   geographic geometry in EPSG:4326 does not acquire metre units from a numeric
   threshold. Use the engine's explicitly supported geodesic/geography
   operation, or a projected CRS whose area of use contains the data's known
   extent. For distance and within-distance tests on an unknown or wide
   extent, prefer an operation the engine documents as geodesic for the
   geometry types involved; do not guess a UTM zone or national grid. A
   geography type does not make every operation geodesic: check buffers and
   other constructions per operation. Assigning an SRID is not coordinate
   transformation; Web Mercator is not a general metric-analysis CRS.
4. Preserve analytical correctness while improving execution. Consider spatial
   indexes or candidate filters, predicate pushdown, partition pruning and
   join cardinality. An expression or cast can prevent use of an existing
   index; verify the relevant plan instead of promising index use by syntax.
5. Run a small meaningful control when an engine is available: qualifying and
   non-qualifying features, a boundary, and duplicate matches where relevant.
   Report actual execution evidence separately from a reasoned SQL review.
   An unavailable engine is `not_testable`, not a successful query run.

Return corrected SQL, consequential assumptions and a short explanation of
correctness and performance. Do not create a full GIS project for a bounded
query review. Preserve source data; an optimization must not silently change
the metric, feature population or authoritative geometry.

## When the task expands

Engine selection, shared-system design and joint compute/storage/delivery
trade-offs belong with an installed `open-map-stack` or an explicit architecture
discussion. Compiling a material analysis belongs with the generalist or
`reproducible-gis-project`. Keep the SQL contribution bounded and supply the
assumptions/evidence needed for that handoff; do not claim to have completed
the whole analysis.

No project template, worked example or OpenMapStack CLI is needed for a bounded
query task. Hand off the SQL and its assumptions to an installed `open-map-stack`
or `reproducible-gis-project` if the user also wants a full project. Sibling
skills are optional and are never automatically installed.

For optional product expertise, read `references/companion-skills.md`.
Keep GIS correctness and the task boundaries above when using a companion.
