---
name: fs-mds-document
description: Scan an entire .NET repository (.NET 8–10, ASP.NET Core, workers, class libraries) and generate a Functional Specification (FS) and a Module Design Specification (MDS) as professional Word (.docx) documents, illustrated with rendered diagrams (context, feature map, process flows, state, module structure, class, sequence, ER) whose editable sources (Mermaid .mmd and draw.io files) are exported to a diagrams/ subfolder. Use this skill whenever the user asks for a functional spec, FS, module design spec, MDS, detailed design document, software/system specification, requirements documentation reverse-engineered from code, or any "spec" deliverable for a .NET system — especially when they mention Word, docx, or diagrams.
metadata:
  origin: dotnet-skills
  targets: .NET 8, 9, and 10 solutions
  requires: Python 3.9+ with python-docx; internet access or local mermaid-cli for diagram rendering
---

# Functional Spec + Module Design Spec (.NET)

Reverse-engineer two complementary specification documents from a .NET
solution:

- **Functional Specification (FS)** — *what* the system does: features,
  inputs, processing rules, outputs, error conditions, business rules, actor
  roles. Written for business analysts, testers, and product owners.
- **Module Design Specification (MDS)** — *how* each module is designed:
  responsibilities, public interfaces, key classes, interactions, database
  and API design. Written for developers and reviewers.

This is a **read-only analysis** — the only writes are the new files in the
output folder. `<skill>` below means the folder containing this SKILL.md;
`<output>` means the output folder chosen in step 2.

## Deliverables

```
<output>/                                  (default: <repo>/docs/specs/)
├── Functional-Specification.docx
├── functional-specification.md            markdown sources are kept —
├── Module-Design-Specification.docx       they make the documents
├── module-design-specification.md         regenerable
└── diagrams/                              every diagram: editable source + png
    ├── 01-context.mmd / .png / .drawio(.json)
    ├── 02-feature-map.mmd / .png
    ├── 03-process-<flow>.mmd / .png
    ├── 04-state-<entity>.mmd / .png            (when a status/state field exists)
    ├── 05-module-structure.mmd / .png / .drawio(.json)
    ├── 06-class-<module>.mmd / .png
    ├── 07-sequence-<operation>.mmd / .png
    └── 08-data-model.mmd / .png
```

## Prerequisites — check before starting

1. `python --version` (3.9+) and `python -c "import docx"`; if the import
   fails run `pip install python-docx` (the only required package).
2. Diagram rendering needs **one** of: `mmdc` on PATH (best, fully local),
   internet access to kroki.io, or `npx` (Node). **Privacy note:** the
   kroki.io fallback sends diagram text (feature, class and entity names —
   not code) to a public web service; if the codebase is confidential and no
   local renderer exists, tell the user and ask before rendering with kroki.

## Step 1 — Scan the repository

Read broadly before writing. Both documents are built from the same scan, so
collect facts once, with two lenses:

**Functional lens (feeds the FS):**

1. **Entry points** — every controller action / minimal-API `Map*` call /
   Razor page / gRPC service: route, verb, auth attributes or policies.
   Group them into feature areas (Orders, Catalog, Accounts…) — these become
   the FS's functional requirement sections.
2. **Inputs and validation** — request DTOs, data annotations,
   FluentValidation validators: field, type, constraint, error message.
3. **Processing rules** — what each handler/service actually does, step by
   step: checks, calculations, side effects, emitted events/emails.
4. **Outputs and errors** — response DTOs, status codes, ProblemDetails,
   thrown/handled exceptions.
5. **Business rules** — domain invariants: guard clauses in entities,
   validator conditions, policy checks. Note the file and member for each.
6. **Actors and roles** — auth schemes, `[Authorize]` roles/policies,
   role seeds. Status/state enums and the transitions code allows.

**Design lens (feeds the MDS):**

7. **Solution shape** — every `.sln`/`.csproj`: target framework, project
   kind, `PackageReference`s, `ProjectReference` graph.
8. **Composition root** — `Program.cs`/`Startup.cs` and extension methods:
   DI registrations, middleware order, hosted services.
9. **Module internals** — for each significant project: key public types,
   main abstractions and their implementations, folder organization.
10. **Data layer** — `DbContext`(s), entities, navigation properties, value
    conversions, migrations, connection strings in `appsettings*.json`.
11. **Integrations & cross-cutting** — HttpClients, message buses, email,
    storage; logging, error-handling middleware, caching, resilience.

Large solutions (>15 projects): read every csproj, but reserve deep source
reading for the 3–5 projects where behavior lives, and say in each
document's Scope section which projects were analyzed in depth.

## Step 2 — Choose the output folder

Default to `<repo>/docs/specs/`; honor any location the user asked for.
Create it plus `diagrams/`. If a previous run's files exist, tell the user
before overwriting.

## Step 3 — Author and render the diagrams

Read [references/diagram-recipes.md](references/diagram-recipes.md) first —
it has the syntax rules that keep renders from failing and a recipe per
diagram type. Write the `.mmd` files into `<output>/diagrams/`:

| File | Feeds | Shows |
|------|-------|-------|
| `01-context.mmd` | FS | actors, system boundary, external systems |
| `02-feature-map.mmd` | FS | feature areas and the operations inside each |
| `03-process-<flow>.mmd` | FS | 1–3 key business processes end to end |
| `04-state-<entity>.mmd` | FS | lifecycle of the central entity (skip if no state field) |
| `05-module-structure.mmd` | MDS | projects/modules and dependency edges |
| `06-class-<module>.mmd` | MDS | key classes of 1–3 core modules |
| `07-sequence-<operation>.mmd` | MDS | 1–2 key operations across modules |
| `08-data-model.mmd` | MDS | entities and relationships from the DbContext |

Then render, and keep fixing + re-running until every diagram passes:

```
python "<skill>/scripts/render_diagrams.py" "<output>/diagrams"
```

The script prints the renderer's syntax error for any failing file. Do not
continue with missing PNGs.

## Step 4 — Export editable draw.io copies

Read [references/drawio-spec.md](references/drawio-spec.md), write
`01-context.drawio.json` and `05-module-structure.drawio.json` specs (same
nodes/edges/labels as their Mermaid twins), then:

```
python "<skill>/scripts/make_drawio.py" "<output>/diagrams/01-context.drawio.json" "<output>/diagrams/05-module-structure.drawio.json"
```

## Step 5 — Write the two documents

Write `<output>/functional-specification.md` following
[references/fs-template.md](references/fs-template.md), then
`<output>/module-design-specification.md` following
[references/mds-template.md](references/mds-template.md). Both use only the
Markdown subset that `build_docx.py` supports (stated at the top of each
template), with figures referenced as `![caption](diagrams/xx.png)`.

The quality bar for both: every claim cites evidence (file, class, package);
requirement and rule IDs (`FR-…`, `BR-…`) are used consistently so the
documents cross-reference cleanly; gaps are stated honestly ("no
authorization checks were found on these endpoints") rather than papered
over; nothing is invented.

## Step 6 — Build the .docx files

```
python "<skill>/scripts/build_docx.py" "<output>/functional-specification.md" "<output>/Functional-Specification.docx"
python "<skill>/scripts/build_docx.py" "<output>/module-design-specification.md" "<output>/Module-Design-Specification.docx"
```

The script exits non-zero listing any image it could not find — fix the
paths and re-run. A clean run prints only `Wrote <path>`.

## Step 7 — Deliver

Confirm both `.docx` files exist and are non-trivial in size, then report:

- the paths of both documents and the `diagrams/` folder;
- that Word will offer to update each table of contents on open (Ctrl+A, F9
  populates it manually);
- how to edit diagrams later: change a `.mmd` and re-run
  `render_diagrams.py`, or open the `.drawio` files at app.diagrams.net /
  in the draw.io desktop or VS Code extension;
- two or three sentences of notable findings (feature coverage, design
  observations, any risks documented).

## Rules

- **Read-only scan.** Never modify source files; all writes go to `<output>`.
- **Evidence or silence.** Anything not grounded in a file you read is
  either omitted or explicitly marked as an assumption.
- **Behavior as implemented.** The FS documents what the code *does*, not
  what it arguably should do. Where behavior looks like a bug, record it
  factually and flag it in "Assumptions and Open Questions".
- **Diagrams must render.** A failed `.mmd` is fixed, not skipped — the
  docx build will flag the missing image anyway.
- **Keep the sources.** The `.md`, `.mmd`, and `.drawio.json` files are part
  of the deliverable.
