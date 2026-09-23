---
name: data-dictionary-document
description: Generate a professional Data Dictionary as a Word (.docx) document from a database's DDL (CREATE TABLE scripts, SQL Server database projects, or EF Core migrations), enriched by scanning the .NET repository and docs for what each table and column actually means — with Entity Relationship Diagrams (broken down by module when the schema is large) whose editable sources (Mermaid .mmd and draw.io files) are exported to a diagrams/ subfolder. Use this skill whenever the user asks for a data dictionary, database documentation, schema documentation, table/column reference, ERD or entity relationship diagram, or wants to "document the database/tables/schema" — especially when they mention DDL, SQL scripts, Word, or docx.
metadata:
  origin: dotnet-skills
  targets: .NET 8, 9, and 10 solutions; SQL Server, PostgreSQL, MySQL, SQLite DDL
  requires: Python 3.9+ with python-docx; internet access or local mermaid-cli for diagram rendering
---

# Data Dictionary Document (.NET)

Produce a complete, professional Data Dictionary for a database: a styled
Word document with cover page, table of contents, an ERD (split by module
for large schemas), and a column-level reference for every table — grounded
in the DDL and enriched with meaning mined from the codebase. This is a
**read-only analysis** — the only writes are the new files in the output
folder.

`<skill>` below means the folder containing this SKILL.md. `<output>` means
the output folder chosen in step 2.

## Deliverables

```
<output>/                                  (default: <repo>/docs/data-dictionary/)
├── Data-Dictionary.docx                   the document
├── data-dictionary.md                     markdown source (kept for regeneration)
└── diagrams/
    ├── 00-erd-overview.mmd / .png         module map (only when split)
    ├── 01-erd-<module>.mmd / .png         one ERD per module — editable
    ├── 02-erd-<module>.mmd / .png         Mermaid source + rendered image
    ├── 01-erd-<module>.drawio(.json)      editable draw.io twin of every
    └── 02-erd-<module>.drawio(.json)      module ERD
```

## Prerequisites — check before starting

1. `python --version` (3.9+; on Windows try `py` if `python` is missing) and
   `python -c "import docx"`. If the import fails, run
   `pip install python-docx` (the only required package).
2. Diagram rendering needs **one** of: `mmdc` on PATH (best, fully local),
   internet access to kroki.io, or `npx` (Node). The render script picks
   automatically. **Privacy note:** the kroki.io fallback sends diagram text
   (table/column names, not data) to a public web service — if the schema is
   confidential and no local renderer exists, tell the user and ask before
   rendering with kroki.

## Step 1 — Locate the DDL

The DDL is the source of truth for this document; everything else only adds
meaning on top. In order of preference:

1. **User-provided DDL** — a `.sql` file or path the user pointed at. Use
   exactly that; don't merge in other sources without saying so.
2. **DDL in the repo** — look for `**/*.sql` (database projects/`.sqlproj`,
   `db/`, `migrations/`, `scripts/` folders). Idempotent migration scripts:
   the *latest* full schema wins; apply ALTERs in order when that's what
   exists.
3. **EF Core migrations, no SQL** — generate the DDL rather than guessing:
   `dotnet ef migrations script --idempotent` (needs the tool; ask before
   running builds). If that isn't possible, reconstruct the schema from the
   latest `*ModelSnapshot.cs` — it lists every table, column, type, key, and
   index — and state in the document that the source was the EF model
   snapshot, not executed DDL.

If none of these exist, stop and ask the user for the DDL — a data
dictionary invented from entity classes alone would misstate types,
defaults, and constraints.

Then parse it into working notes: per table — schema, name, columns (order,
exact type, nullability, default, identity/computed), PK, FKs (with ON
DELETE/UPDATE), unique/check constraints, indexes, triggers; plus any
comment syntax (`MS_Description`, PostgreSQL `COMMENT ON`). Count the
tables — the count drives the ERD strategy in step 4.

## Step 2 — Choose the output folder

Default to `<repo>/docs/data-dictionary/`; use whatever location the user
asked for instead. Create it plus the `diagrams/` subfolder. If a previous
run's files exist there, tell the user before overwriting.

## Step 3 — Mine the repo for meaning

The DDL says what exists; the codebase says what it *means*. For each table,
find (keep notes with evidence):

1. **Entity classes** — the class mapped to the table; XML doc comments,
   property attributes (`[MaxLength]`, `[Required]`), enums backing string/
   int columns (the enum members become the column's documented values).
2. **EF configuration** — `OnModelCreating` / `IEntityTypeConfiguration`:
   `HasComment`, conversions, owned types, query filters (soft delete),
   `HasData` seed rows (these feed the Reference Data chapter).
3. **Usage** — which services/handlers write each table; lifecycle facts
   ("append-only audit log", "rows soft-deleted via IsDeleted").
4. **Docs** — README, `docs/`, ADRs mentioning tables or domain terms;
   reuse their vocabulary in descriptions.

Descriptions found in DDL comments, code comments, or docs are used as-is;
descriptions you infer from naming and usage get a `†` marker (the template
defines the legend). Never leave a description cell empty.

## Step 4 — Author and render the ERDs

Read [references/erd-recipes.md](references/erd-recipes.md) first — it has
the module-split rules (≤ 12 tables → one ERD; more → module ERDs of 5–12
entities plus a `00-erd-overview` module map), the grouping signals (schemas,
FK clusters, DbContext/namespace structure, name prefixes), stub-entity
handling for cross-module FKs, and the Mermaid `erDiagram` syntax rules that
keep renders from failing (single-word types — `nvarchar`, never
`nvarchar(200)`).

Write the `.mmd` files into `<output>/diagrams/`, then render and keep
fixing + re-running until every diagram passes:

```
python "<skill>/scripts/render_diagrams.py" "<output>/diagrams"
```

The script prints the renderer's syntax error for any failing file. Do not
continue with missing PNGs.

## Step 5 — Export editable draw.io copies

Read [references/drawio-erd-spec.md](references/drawio-erd-spec.md), write a
`NN-erd-<module>.drawio.json` spec for **every module ERD** (same entities,
relationships, and key markers as its Mermaid twin — full column types are
fine here), then:

```
python "<skill>/scripts/make_drawio_erd.py" "<output>/diagrams/01-erd-<module>.drawio.json" ...
```

## Step 6 — Write the document

Read [references/document-template.md](references/document-template.md) and
write `<output>/data-dictionary.md` following its skeleton exactly —
frontmatter (drives the cover page), overview with module table, one chapter
per module with its ERD figure and per-table sections (columns, keys &
constraints, indexes), the flat relationship reference, and reference data.

The quality bar: every table in the DDL gets a section, every column gets a
row with its exact type, every description is grounded or marked inferred,
and schema-vs-code drift is reported, not papered over.

## Step 7 — Build the .docx

```
python "<skill>/scripts/build_docx.py" "<output>/data-dictionary.md" "<output>/Data-Dictionary.docx"
```

The script exits non-zero and lists any image it could not find — fix the
paths and re-run. A clean run prints only `Wrote <path>`.

## Step 8 — Deliver

Confirm the `.docx` exists and is non-trivial in size, then report to the
user:

- the path of the `.docx` and the `diagrams/` folder;
- which DDL source was used (and, if it was an EF model snapshot, that
  executed DDL would be more authoritative);
- that Word will offer to update the table of contents on open (or Ctrl+A,
  F9 populates it manually);
- how to edit diagrams later: change a `.mmd` and re-run
  `render_diagrams.py`, or open the `.drawio` files at app.diagrams.net /
  in the draw.io desktop or VS Code extension;
- one or two sentences on notable findings (module structure, drift between
  code and DDL, tables with no code usage).

## Rules

- **Read-only scan.** Never modify source files; all writes go to `<output>`.
- **The DDL is the truth.** Types, defaults, constraints come from the DDL
  verbatim; entity classes only ever add *meaning*, never structure. Drift
  between them is documented as a finding.
- **Complete or flagged.** Every table, every column — anything skipped or
  ambiguous is stated in the document, not silently dropped.
- **Diagrams must render.** A failed `.mmd` is fixed, not skipped — the docx
  build will flag the missing image anyway.
- **Scripts own the rendering.** Never hand-write draw.io XML or docx
  markup; the markdown file and the JSON specs are the interface.
- **Keep the sources.** The `.md`, `.mmd`, and `.drawio.json` files are part
  of the deliverable; they make the document regenerable and the diagrams
  editable.
