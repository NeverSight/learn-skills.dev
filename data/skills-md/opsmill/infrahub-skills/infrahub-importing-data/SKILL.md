---
name: infrahub-importing-data
description: >-
  Converts CSV/TSV inputs into Infrahub object YAML and loads them onto a fresh branch.
  Handles a single file, a folder of files, an explicit list of paths, and one-big-denormalized-sheet exports.
  TRIGGER when: importing CSV, loading CSV/TSV into Infrahub, ingesting spreadsheet data, converting CSV to Infrahub objects, splitting a denormalized CSV across multiple kinds, re-running an import after changing a column mapping, debugging why a row fails to convert or load.
  DO NOT TRIGGER when: running `infrahubctl load` against an LDJSON dump (different format and tool), designing or modifying schemas (this skill is read-only against the schema and fails closed on unmapped columns), exporting data from Infrahub (use `infrahubctl object get -o csv` for single-kind export), or ingesting JSON/XLSX (v1 is CSV+TSV only).
argument-hint: "[csv-file-or-folder] [more-paths...]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# CSV/TSV Import to Infrahub Objects

## Overview

Expert guidance for turning user-provided CSV or TSV
inputs — a single file, a folder of files, or any
combination — into Infrahub object YAML that
`infrahubctl object load` accepts. The skill is the
bridge between "I have a spreadsheet" and "the
objects exist on a reviewable branch."

The skill is **strictly a consumer of the live
schema**. If a CSV column has no schema home, it
stops, lists the offending columns, and routes the
user to `infrahub-managing-schemas` to make the
schema decision separately. It never proposes
attribute additions, dropdown choices, or any other
schema edit, and it never writes directly to the
default branch.

## Project Context

Existing schema files:
!`find . -name "*.yml" -path "*/schemas/*" -o -name "*schema*" -name "*.yml" 2>/dev/null | head -10`

Existing object files:
!`find . -name "*.yml" -path "*/objects/*" 2>/dev/null | head -10`

`.infrahub.yml` if present:
!`find . -maxdepth 2 -name ".infrahub.yml" 2>/dev/null | head -1`

Candidate CSV/TSV inputs in the working tree:
!`find . -maxdepth 3 \( -name "*.csv" -o -name "*.tsv" \) 2>/dev/null | head -10`

If invoked with arguments (e.g.,
`/infrahub:importing-data inventory.csv`), treat the
first argument as the input file or folder; treat
remaining arguments as additional paths to include.

## When to Use

- A user hands you one or more CSV or TSV files and
  wants the data in Infrahub.
- The input is denormalized — a single sheet
  conflating multiple kinds — and you need to split
  it across the right schema nodes with correct
  load order.
- The CSV has columns that look like dropdown
  labels (e.g., `Status: Active`) and you need to
  emit the choice **name** (e.g., `active`).
- A parent kind's rows are repeated per child in
  the CSV, and the children belong inline as
  component children of the parent.
- Interface-shaped names (`eth0..eth47`) appear in
  sequence and you want range-collapsed emission.
- The user wants every imported value stamped with
  a lineage tag.

## When NOT to Use

- The input is an LDJSON dump from `infrahubctl
  dump`. Use `infrahubctl load`; it reads a
  different format and is the wrong tool for CSV.
  Both are top-level commands; there is no
  `import` or `export` command group. The skills
  disambiguate so you don't conflate them.
- The user needs schema changes. This skill is
  read-only against the schema. Hand off to
  `infrahub-managing-schemas`.
- The user needs to export data from Infrahub to
  CSV. Single-kind export already works via
  `infrahubctl object get -o csv`; a future
  companion skill will cover multi-kind export.
- The input is JSON, XLSX, Parquet, or any other
  non-CSV format. v1 covers CSV + TSV only.

## Rule Categories

| Priority | Category | Prefix | Description |
| -------- | -------- | ------ | ----------- |
| CRITICAL | Workflow | `workflow-` | Schema introspection, profile-sample, fail-closed gate, up-front interview, self-check, pre-flight closure, branch-first, validate-error mapping |
| HIGH | Inputs | `inputs-` | File / folder / list normalization, CSV dialect detection, same-kind merge |
| CRITICAL | Mapping | `mapping-` | Column → attribute, value coercion, empty/null handling, dropdown label → name, reference HFID detection |
| HIGH | Decomposition | `decomposition-` | Splitting a denormalized CSV across kinds |
| MEDIUM | Range | `range-` | Interface-shape detection and collapse |
| LOW | Lineage | `lineage-` | Optional source/owner stamping at import time |
| LOW | Outputs | `outputs-` | File-level shape concerns (provenance comment) |

## Schema Features This Skill Depends On

The skill emits object YAML that conforms to the
target schema's actual shape. If the schema is
missing a feature the CSV requires, the load fails —
which is why the skill checks these upfront and
escalates rather than silently working around them.

| If the CSV has... | The schema must... | See |
| ----------------- | ------------------ | --- |
| A reference column pointing to another kind | Define `human_friendly_id` on the target node; the HFID length determines scalar vs list reference shape | [../infrahub-managing-schemas/rules/display-human-friendly-id.md](../infrahub-managing-schemas/rules/display-human-friendly-id.md) |
| A label-style value for a Dropdown column (`Active` rather than `active`) | Declare the dropdown `choices` as objects with both `name` and `label`; the emitter writes the `name` and reads `label` from the schema | [../infrahub-managing-schemas/rules/attribute-defaults-and-types.md](../infrahub-managing-schemas/rules/attribute-defaults-and-types.md) |
| Repeated parent rows with per-child columns | Pair Component (parent) and Parent (child) relationships with the same identifier, and `optional: false` on the child side | [../infrahub-managing-schemas/rules/relationship-component-parent.md](../infrahub-managing-schemas/rules/relationship-component-parent.md) |
| A column with no obvious schema home | Be extended via `infrahub-managing-schemas` — this skill fails closed and hands off | [../infrahub-managing-schemas/SKILL.md](../infrahub-managing-schemas/SKILL.md) |

If any of these is missing for the data the user
wants to load, that's a schema migration, not an
import fix. The skill stops and says so.

## Workflow

Follow these 14 steps in order. The numbering is
load-bearing — earlier steps gate later ones.

1. **Normalize input to a flat file list.** Accept a
   single path, a directory (recursive scan for
   `*.csv` / `*.tsv`), or a list, and resolve to a
   flat list before profiling. For each file, detect
   the CSV dialect (delimiter, encoding, BOM, line
   endings) before reading rows. Read
   [rules/inputs-file-folder-list.md](./rules/inputs-file-folder-list.md)
   and
   [rules/inputs-csv-dialect.md](./rules/inputs-csv-dialect.md).

2. **Discover the schema — read-only.** Try sources
   in priority order and stop at the first one that
   returns the kinds the CSV needs:
   1. **MCP server** — the same surface
      `infrahub-analyzing-data` uses; sees deployed
      state including branch-specific dropdown
      choices and HFIDs.
   2. **`infrahubctl schema export --branch <name>`** —
      CLI export against the configured server when
      MCP is not connected.
   3. **`/api/schema?branch=<name>` REST endpoint** —
      direct HTTP fetch when `infrahubctl` is
      unavailable or pointing at a different server.
   4. **Local `schemas/*.yml`** in the repo — last
      resort; may lag the deployed state, so the
      step 11 server validate is required to catch
      divergence.

   Record which source you used so the user knows
   how authoritative the mapping is. **Never propose
   a schema edit.** Read
   [rules/workflow-introspect-first.md](./rules/workflow-introspect-first.md).

3. **Profile each file.** Read header + sample
   rows (default 20; more if needed for dropdown,
   range, or denormalization detection). Note
   column data shapes, per-column distinct value
   counts, sample values, and sequence patterns.
   Read
   [rules/workflow-profile-sample.md](./rules/workflow-profile-sample.md).

4. **Build a mapping draft per file** using the
   heuristics in [reference.md](./reference.md):
   - **Column → attribute:** exact name match,
     then snake_case round-trip, then display-label
     fuzzy match, then unit-strip (`(GB)`, `(MHz)`)
     — anything past that defers to the interview.
     Read [rules/mapping-column-to-attribute.md](./rules/mapping-column-to-attribute.md).
   - **Value coercion:** Boolean / Number /
     DateTime / JSON attribute kinds require
     explicit type coercion before emission. Read
     [rules/mapping-value-coercion.md](./rules/mapping-value-coercion.md).
   - **Empty cells:** decide omit vs fail by the
     schema's `optional` and `default_value`
     declarations. Read
     [rules/mapping-empty-and-null.md](./rules/mapping-empty-and-null.md).
   - **Dropdown columns:** build a label→name
     lookup from the schema and translate. Read
     [rules/mapping-dropdown-label-to-name.md](./rules/mapping-dropdown-label-to-name.md).
   - **Reference columns:** detect by name match
     against a relationship plus value shape
     against the target kind's HFID. Read
     [rules/mapping-reference-and-hfid.md](./rules/mapping-reference-and-hfid.md).
   - **Range columns:** collapse contiguous
     interface-style sequences. Read
     [rules/range-detection.md](./rules/range-detection.md).
   - **Denormalized columns:** detect repeated
     parent groups and split the input across
     kinds. Read
     [rules/decomposition-denormalized-csv.md](./rules/decomposition-denormalized-csv.md).
   - **Same kind in multiple inputs:** merge into
     one numbered output file, dedupe by HFID,
     surface conflicts in the interview. Read
     [rules/inputs-merge-same-kind.md](./rules/inputs-merge-same-kind.md).

5. **Fail-closed gate.** If any column has no
   schema home, **stop.** Emit a structured report
   listing the unmapped columns and the kinds you
   checked, point the user at
   `infrahub-managing-schemas`, and exit. No
   partial writes. Read
   [rules/workflow-fail-closed-on-unmapped-columns.md](./rules/workflow-fail-closed-on-unmapped-columns.md).

6. **Up-front interview.** Batch every remaining
   ambiguity into one round of multi-choice
   questions before any file is written. Read
   [rules/workflow-up-front-interview.md](./rules/workflow-up-front-interview.md).

7. **Confirm and lock the mapping.** Echo back the
   complete plan (target files, kinds, column
   bindings, branch name, lineage opt-in) before
   the first file is written.

8. **Emit object YAML** to a local working
   directory (default `./output_dir/`). Each file
   conforms to the managing-objects envelope:
   `apiVersion: infrahub.app/v1`, `kind: Object`,
   `spec.kind`, `spec.data`. Files are numbered for
   load order (`NN_<kind-plural>.yml`). Each file
   carries a leading provenance comment naming the
   source CSV(s) + sha256 + emission timestamp.
   Cross-reference the format rules in
   [../infrahub-managing-objects/rules/format-structure.md](../infrahub-managing-objects/rules/format-structure.md),
   the file naming convention in
   [../infrahub-managing-objects/rules/organization-load-order.md](../infrahub-managing-objects/rules/organization-load-order.md),
   and the comment shape in
   [rules/outputs-provenance-comment.md](./rules/outputs-provenance-comment.md).

9. **Self-check against managing-objects.** Re-read
   the listed managing-objects rules and walk the
   emission against each one. Local only — no CLI,
   no server, no branch. Fix in place before moving
   on. Read
   [rules/workflow-self-check-against-managing-objects.md](./rules/workflow-self-check-against-managing-objects.md).

10. **Pre-flight reference closure.** Walk every
    relationship reference in the emission and
    verify the target resolves either to a row in
    an upstream file or to a live object the
    introspection captured. Orphan references fail
    closed before any branch is touched. Read
    [rules/workflow-pre-flight-closure.md](./rules/workflow-pre-flight-closure.md).

11. **Create the branch.** Only after the
    self-check and pre-flight closure pass, run
    `infrahubctl branch create <name>` (default
    `csv-import-YYYYMMDD-HHMM`, user-overridable in
    the interview). Doing this last keeps
    throwaway branches out of the branch list. Read
    [rules/workflow-branch-before-load.md](./rules/workflow-branch-before-load.md).

12. **Server validate** on the branch:
    `infrahubctl object validate ./output_dir/
    --branch <name>`. Catches schema-resolution
    errors the local checks can't (kind not in
    schema, attribute name miss, reference target
    missing). On error, translate the diagnostic
    back to the source CSV cell and ask the user
    to fix the input — don't hand-edit the emitted
    YAML. Read
    [rules/workflow-validate-error-mapping.md](./rules/workflow-validate-error-mapping.md).

13. **Load** on the branch: `infrahubctl object
    load ./output_dir/ --branch <name>`. **Object
    load is not transactional across files** — if
    file 17 of 20 fails, files 1–16 are already on
    the branch. The branch-first design means you
    discard the branch and re-run with a fresh
    branch name; you never clean up partial state
    by hand.

14. **Hand off.** Tell the user the branch is
    ready for review, the validate/load commands
    that were run, and how to open a proposed
    change in the UI. Don't auto-merge.

## Supporting References

- **[examples.md](./examples.md)** — 8 worked CSV
  patterns: flat list, denormalized split,
  parent-with-children, dropdown label normalization,
  range collapse, lineage stamping, fail-closed
  report, merge + dedup
- **[reference.md](./reference.md)** — heuristic
  order, file envelope reminder, HFID decision
  matrix, file naming convention
- **[rules/](./rules/)** — individual rules by
  category prefix; start at
  [rules/_sections.md](./rules/_sections.md)
- **[../infrahub-managing-objects/SKILL.md](../infrahub-managing-objects/SKILL.md)**
  — the consumer-side rules every emitted file must
  conform to (envelope, value mapping, components,
  range, load order, branch-first)
- **[../infrahub-analyzing-data/SKILL.md](../infrahub-analyzing-data/SKILL.md)**
  — MCP introspection pattern for live schema
  discovery
- **[../infrahub-managing-schemas/SKILL.md](../infrahub-managing-schemas/SKILL.md)**
  — escape hatch when a column has no schema home
- **[../infrahub-common/metadata-lineage.md](../infrahub-common/metadata-lineage.md)**
  — value metadata semantics (`source` is lineage
  only; locking needs `owner` + `is_protected`)
- **[../infrahub-common/rules/workflow-branch-for-crud.md](../infrahub-common/rules/workflow-branch-for-crud.md)**
  — shared branch-first rule that both schema and
  object writes inherit from
- **[../infrahub-common/rules/connectivity-server-check.md](../infrahub-common/rules/connectivity-server-check.md)**
  — verify the server is reachable with `infrahubctl
  info` before any server-dependent command in the
  workflow
- **[../infrahub-common/rules/connectivity-python-environment.md](../infrahub-common/rules/connectivity-python-environment.md)**
  — detect the project's Python env prefix
  (`uv run` / `poetry run`) for all `infrahubctl`
  invocations
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)
